import os
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import AzureAISearchTool

def create_ai_search_tool(project_client: AIProjectClient) -> AzureAISearchTool:
    ai_search_connection = project_client.connections.get(
        connection_name=os.getenv("AI_SEARCH_CONNECTION_NAME")
    )

    return AzureAISearchTool(
        index_connection_id=ai_search_connection.id,
        index_name="azureblob-index",
    )