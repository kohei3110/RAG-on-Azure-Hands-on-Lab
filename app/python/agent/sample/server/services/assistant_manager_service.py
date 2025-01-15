import os
import time
import json
from typing import Any, Callable, Set
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import Agent, AgentThread, AzureAISearchTool, AzureFunctionTool, BingGroundingTool, ConnectionProperties, FileSearchTool, RequiredFunctionToolCall, ToolOutput, ToolSet, RunStatus, MessageRole, MessageTextContent, FunctionTool, VectorStore, VectorStoreDataSource, VectorStoreDataSourceAssetType

from tools.knowledge.azure_ai_search_tool import create_ai_search_tool
from tools.knowledge.bing_grounding_tool import create_bing_grounding_tool
from tools.knowledge.file_search_tool import create_file_search_tool
from tools.action.azure_functions_tool import create_azure_function_tool
from tools.action.user_functions_tool import search_restaurants

class AssistantManagerService:
    def __init__(self, project_client: AIProjectClient):
        self.project_client = project_client

    def create_agent_thread_and_functions(self):

        user_functions: Set[Callable[..., Any]] = {
            search_restaurants
        }

        functions: FunctionTool = FunctionTool(user_functions)
        toolset: ToolSet = ToolSet()

        azure_function_tool: AzureFunctionTool = create_azure_function_tool()
        ai_search_tool: AzureAISearchTool = create_ai_search_tool(self.project_client)
        

        # FIXME: Bing Grounding を使用する際は、モデルを gpt-4o or gpt-35-turbo に変更する
        # bing_grounding_connection: ConnectionProperties = self.project_client.connections.get(
        #     connection_name="bing_search"
        # )
        # bing_grounding_tool: BingGroundingTool = create_bing_grounding_tool(connection_id=bing_grounding_connection.id)

        file_search_tool: FileSearchTool = create_file_search_tool(self.project_client)

        toolset.add(functions)
        toolset.add(azure_function_tool)
        toolset.add(ai_search_tool)
        # toolset.add(bing_grounding_tool)
        toolset.add(file_search_tool)

        thread = self.project_client.agents.create_thread()
        agent: Agent = self.project_client.agents.create_agent(
            # model="gpt-35-turbo",
            model="gpt-4o-mini",
            name="Assistant Manager",
            instructions="""
            あなたは Contoso 社の社員の業務を支援するためのアシスタントです。
            あなたは以下の業務を遂行します。
            - レストランを検索します。
            - 天気を確認します。
            - 「商品」というキーワードがクエリに含まれている場合、アップロードされたファイルから取得します。
            - その他必要な最新情報を取得するために Bing Grounding を使用します。

            #制約事項
            - ユーザーからのメッセージは日本語で入力されます
            - ユーザーからのメッセージから忠実に情報を抽出し、それに基づいて応答を生成します。
            - ユーザーからのメッセージに勝手に情報を追加したり、不要な改行文字 \n を追加してはいけません
            """,
            toolset=toolset,
            headers={"x-ms-enable-preview": "true"},
        )
        print(f"Created agent: {agent}")
        return agent, thread, functions

    def create_and_send_message(self, user_message: str, agent: Agent, thread: AgentThread):
        self.project_client.agents.create_message(
            thread_id=thread.id,
            role="user",
            content=user_message,
        )
        return self.project_client.agents.create_run(thread_id=thread.id, assistant_id=agent.id)
    
    def execute_tool_calls(self, tool_calls, functions: FunctionTool):
        tool_outputs = []
        for tool_call in tool_calls:
            if isinstance(tool_call, RequiredFunctionToolCall):
                try:
                    print(f"Executing tool call: {tool_call}")
                    output = functions.execute(tool_call)
                    response = {"answer": output, "success": True}
                    tool_outputs.append(
                        ToolOutput(
                            tool_call_id=tool_call.id,
                            output=json.dumps(response, ensure_ascii=False),
                        )
                    )
                except Exception as e:
                    print(f"Error executing tool_call {tool_call.id}: {e}")
        return tool_outputs

    def get_assistant_responses(self, thread: AgentThread):
        agent_messages = self.project_client.agents.list_messages(thread_id=thread.id)
        assistant_messages = []
        for data_point in reversed(agent_messages.data):
            last_message_content = data_point.content[-1]
            if isinstance(last_message_content, MessageTextContent):
                print(f"{data_point.role}: {last_message_content.text.value}")
                if data_point.role == MessageRole.AGENT:
                    assistant_messages.append(last_message_content.text.value)
        return assistant_messages

    def send_prompt(self, user_message: str) -> dict:
        agent, thread, functions = self.create_agent_thread_and_functions()
        run = self.create_and_send_message(user_message, agent, thread)

        while run.status in [RunStatus.QUEUED, RunStatus.IN_PROGRESS, RunStatus.REQUIRES_ACTION]:
            time.sleep(1)
            run = self.project_client.agents.get_run(thread_id=thread.id, run_id=run.id)
            print(f"Current run status1: {run.status}")

            if run.status == RunStatus.REQUIRES_ACTION:
                tool_calls = run.required_action.submit_tool_outputs.tool_calls
                if not tool_calls:
                    print("No tool calls provided - cancelling run")
                    self.project_client.agents.cancel_run(thread_id=thread.id, run_id=run.id)
                    break

                tool_outputs = self.execute_tool_calls(tool_calls, functions)

                print(f"Tool outputs: {tool_outputs}")
                if tool_outputs:
                    self.project_client.agents.submit_tool_outputs_to_run(
                        thread_id=thread.id, run_id=run.id, tool_outputs=tool_outputs
                    )
                else:
                    print("No tool outputs to submit - cancelling run")
                    self.project_client.agents.cancel_run(thread_id=thread.id, run_id=run.id)
                    break

            print(f"Current run status2: {run.status}")

        print(f"Run completed with status: {run.status}")

        assistant_messages = self.get_assistant_responses(thread)
        return {"response": assistant_messages[0]}