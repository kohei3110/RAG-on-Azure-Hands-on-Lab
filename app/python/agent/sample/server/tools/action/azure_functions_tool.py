import os
from azure.ai.projects.models import AzureFunctionTool, AzureFunctionStorageQueue

def create_azure_function_tool() -> AzureFunctionTool:
    return AzureFunctionTool(
        name="get_weather",
        description="天気を取得する関数",
        parameters={
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "天気を取得する地域"}
            },
        },
        input_queue=AzureFunctionStorageQueue(
            storage_service_endpoint=os.getenv("AZURE_FUNCTIONS_STORAGE_SERVICE_ENDPOINT"),
            queue_name=os.getenv("AZURE_FUNCTIONS_STORAGE_INPUT_QUEUE_NAME"),
        ),
        output_queue=AzureFunctionStorageQueue(
            storage_service_endpoint=os.getenv("AZURE_FUNCTIONS_STORAGE_SERVICE_ENDPOINT"),
            queue_name=os.getenv("AZURE_FUNCTIONS_STORAGE_OUTPUT_QUEUE_NAME"),
        ),
    )