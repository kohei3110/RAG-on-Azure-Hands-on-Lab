import os
from dotenv import load_dotenv
from fastapi import FastAPI
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

from services.openapi_spec_service import OpenApiSpecService
from services.assistant_manager_service import AssistantManagerService
from services.code_interpreter_service import CodeInterpreterService


load_dotenv()

app: FastAPI = FastAPI(
    title="API Sample for Agent SDK",
    description="API for Agent SDK",
    version="1.0.0",
)

project_client: AIProjectClient = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(), conn_str=os.environ["PROJECT_CONNECTION_STRING"]
)

assistant_manager_service = AssistantManagerService(project_client)
code_interpreter_service = CodeInterpreterService(project_client)
openapi_spec_service = OpenApiSpecService(project_client)

import controller
app.include_router(controller.router)