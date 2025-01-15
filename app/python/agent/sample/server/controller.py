from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.responses import FileResponse

from models.models import MessageRequest
from services.openapi_spec_service import OpenApiSpecService
from services.code_interpreter_service import CodeInterpreterService
from utils.file_handler import FileHandler
from services.assistant_manager_service import AssistantManagerService
from startup import code_interpreter_service, assistant_manager_service, openapi_spec_service


router = APIRouter()


def get_file_handler():
    return FileHandler()


@router.get("/health")
def get_health():
    """
    ヘルスチェックエンドポイント。

    Returns:
        dict: アプリケーションのステータスを含む辞書。
    """
    return {"status": "ok"}


@router.post("/prompt")
def post_assistant_manager_service(
    request: MessageRequest, 
    assistant_manager_service: AssistantManagerService = Depends(lambda: assistant_manager_service)
):
    """
    エージェントに対してプロンプトを送信するエンドポイント。

    Args:
        request (MessageRequest): メッセージリクエスト。
    
    Returns:
        dict: エージェントの応答を含む辞書。
    """
    user_message = request.message
    response = assistant_manager_service.send_prompt(user_message)
    return {"response": response}


@router.post("/code_interpreter")
async def post_code_interpreter(
    file: UploadFile = File(...), 
    message: str = Form(...),
    file_handler: FileHandler = Depends(get_file_handler),
    code_interpreter_service: CodeInterpreterService = Depends(lambda: code_interpreter_service)
):
    user_message = message
    file_name = await code_interpreter_service.process_code_interpreter(file, user_message, file_handler)
    return FileResponse(path=file_name, filename=file_name)


@router.post("/openapi")
def post_openapi(
    request: MessageRequest,
    openapi_spec_service: OpenApiSpecService = Depends(lambda: openapi_spec_service)
):
    user_message = request.message
    response = openapi_spec_service.process_openapi_spec(user_message)
    return {"response": response}