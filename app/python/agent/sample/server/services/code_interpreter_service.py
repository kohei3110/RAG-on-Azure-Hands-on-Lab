from azure.ai.projects.models import FilePurpose
from tools.action.code_interpreter_tool import create_code_interpreter_tool
from utils.file_handler import FileHandler
from pathlib import Path


class CodeInterpreterService:
    def __init__(self, project_client):
        self.project_client = project_client

    async def process_code_interpreter(self, file, user_message: str, file_handler: FileHandler):
        file_location = await file_handler.save_temp_file(file, "/tmp")
        try:
            uploaded_file = self.upload_file_to_project(file_location)
            agent, thread = self.create_agent_and_thread(uploaded_file.id)
            self.send_user_message_to_thread(thread.id, user_message)
            run = self.create_and_execute_run(thread.id, agent.id)
            self.handle_run_completion(run, thread.id, uploaded_file.id)
            file_name = self.save_generated_images(thread.id)
            return file_name
        finally:
            file_handler.delete_file(file_location)
            print("Deleted file")

    def upload_file_to_project(self, file_location: str):
        uploaded_file = self.project_client.agents.upload_file_and_poll(
            file_path=file_location, purpose=FilePurpose.AGENTS
        )
        print(f"Uploaded file, file ID: {uploaded_file.id}")
        return uploaded_file

    def create_agent_and_thread(self, file_id: str):
        code_interpreter = create_code_interpreter_tool(file_ids=[file_id])
        agent = self.project_client.agents.create_agent(
            model="gpt-4o-mini",
            name="code_interpreter",
            instructions="You are helpful agent",
            tools=code_interpreter.definitions,
            tool_resources=code_interpreter.resources,
        )
        thread = self.project_client.agents.create_thread()
        print(f"Created thread, thread ID: {thread.id}")
        return agent, thread

    def send_user_message_to_thread(self, thread_id: str, user_message: str):
        message = self.project_client.agents.create_message(
            thread_id=thread_id,
            role="user",
            content=user_message
        )
        print(f"Created message, message ID: {message.id}")

    def create_and_execute_run(self, thread_id: str, agent_id: str):
        run = self.project_client.agents.create_and_process_run(thread_id=thread_id, assistant_id=agent_id)
        print(f"Run finished with status: {run.status}")
        return run

    def handle_run_completion(self, run, thread_id: str, file_id: str):
        if run.status == "failed":
            print(f"Run failed: {run.last_error}")
        self.project_client.agents.delete_file(file_id)
        print(f"Deleted file, file ID: {file_id}")

    def save_generated_images(self, thread_id: str):
        messages = self.project_client.agents.list_messages(thread_id=thread_id)
        print(f"Messages: {messages}")

        last_msg = messages.get_last_text_message_by_sender("assistant")
        if last_msg:
            print(f"Last Message: {last_msg.text.value}")

        for image_content in messages.image_contents:
            print(f"Image File ID: {image_content.image_file.file_id}")
            file_name = f"{image_content.image_file.file_id}_image_file.png"
            self.project_client.agents.save_file(file_id=image_content.image_file.file_id, file_name=file_name)
            print(f"Saved image file to: {Path.cwd() / file_name}")

        return file_name