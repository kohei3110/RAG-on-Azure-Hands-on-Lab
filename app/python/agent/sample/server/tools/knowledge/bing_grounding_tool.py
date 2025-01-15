from azure.ai.projects.models import BingGroundingTool


def create_bing_grounding_tool(connection_id):
    return BingGroundingTool(connection_id=connection_id)