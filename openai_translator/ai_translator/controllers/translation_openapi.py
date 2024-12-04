import asyncio

from fastapi import APIRouter
from starlette.responses import StreamingResponse

from openai_translator.ai_translator.controllers.openapi_types.user_input import UserInput
from openai_translator.ai_translator.model.openai_model import OpenAIModel
from openai_translator.ai_translator.translator import PDFTranslator
from openai_translator.ai_translator.utils.singleton_service import SingletonService

router = APIRouter()

# 模拟一个生成器，用于逐步生成数据
async def fake_data_stream():
    for i in range(1, 11):  # 模拟10个数据块
        yield f"Data chunk {i}\n"
        await asyncio.sleep(1)  # 模拟每次生成数据需要1秒

@router.post("/translate")
async def translate(user_input: UserInput):
    model_name = user_input.model_name
    book_file_path = user_input.book_file_path
    file_format = user_input.file_format
    global_config = SingletonService().get_service_data()
    openai_api_key = global_config.get("OpenAIModel").get("api_key")

    model = OpenAIModel(model=model_name, api_key=openai_api_key)

    # 实例化 PDFTranslator 类，并调用 translate_pdf() 方法
    translator = PDFTranslator(model)
    translator.translate_pdf(book_file_path, file_format)

    #TODO: 流式返回翻译结果
    return StreamingResponse(fake_data_stream, media_type="application/json")