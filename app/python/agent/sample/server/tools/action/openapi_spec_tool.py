from azure.ai.projects.models import OpenApiAnonymousAuthDetails, OpenApiTool


def create_openapi_tool(openapi_spec):
    auth = OpenApiAnonymousAuthDetails()
    openapi_tool = OpenApiTool(
        name="get_weather", 
        spec=openapi_spec, 
        description="Retrieve weather information for a location", 
        auth=auth
    )
    return openapi_tool