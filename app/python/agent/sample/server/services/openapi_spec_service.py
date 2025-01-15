import jsonref
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import OpenApiTool, RunStatus, MessageRole, MessageTextContent

from tools.action.openapi_spec_tool import create_openapi_tool


class OpenApiSpecService:
    def __init__(self, project_client: AIProjectClient):
        self.project_client = project_client

    def process_openapi_spec(self, user_message: str):
        openapi_spec = self.load_openapi_spec()
        openapi_tool = self.create_openapi_tool(openapi_spec)
        agent, thread = self.create_agent_and_thread(openapi_tool)
        self.send_user_message_to_thread(thread.id, user_message)
        run = self.create_and_process_run(thread.id, agent.id)
        self.handle_run_completion(run, agent.id)
        messages = self.list_messages(thread.id)
        assistant_response = self.get_last_assistant_message(messages)
        return assistant_response

    def load_openapi_spec(self):
        with open("./tools/action/openapi_spec/weather.json", "r") as f:
            openapi_spec = jsonref.loads(f.read())
        return openapi_spec

    def create_openapi_tool(self, openapi_spec):
        return create_openapi_tool(openapi_spec)

    def create_agent_and_thread(self, openapi: OpenApiTool):
        agent = self.project_client.agents.create_agent(
            model="gpt-4o-mini",
            name="Weather Agent",
            instructions="""
            あなたは天気情報を取得するためのアシスタントです。
            """,
            tools=openapi.definitions,
        )
        thread = self.project_client.agents.create_thread()
        return agent, thread

    def send_user_message_to_thread(self, thread_id: str, user_message: str):
        message = self.project_client.agents.create_message(
            thread_id=thread_id,
            role="user",
            content=user_message,
        )
        return message

    def create_and_process_run(self, thread_id: str, agent_id: str):
        run = self.project_client.agents.create_and_process_run(thread_id=thread_id, assistant_id=agent_id)
        return run
    
    def handle_run_completion(self, run, agent_id: str):
        if run.status == RunStatus.FAILED:
            print(f"Run failed: {run.last_error}")
        self.delete_agent(agent_id)

    def delete_agent(self, agent_id: str):
        self.project_client.agents.delete_agent(agent_id)

    def list_messages(self, thread_id: str):
        messages = self.project_client.agents.list_messages(thread_id=thread_id)
        return messages

    def get_last_assistant_message(self, messages):
        for data_point in reversed(messages.data):
            last_message_content = data_point.content[-1]
            if isinstance(last_message_content, MessageTextContent):
                if data_point.role == MessageRole.AGENT:
                    return last_message_content.text.value
        return None