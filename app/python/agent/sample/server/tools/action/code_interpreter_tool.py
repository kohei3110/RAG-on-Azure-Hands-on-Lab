from typing import List
from azure.ai.projects.models import CodeInterpreterTool


def create_code_interpreter_tool(file_ids: List[str]):
    return CodeInterpreterTool(file_ids=file_ids)