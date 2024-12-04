import uvicorn
from fastapi import FastAPI

from openai_translator.ai_translator.utils.singleton_service import SingletonService
from utils import ArgumentParser, ConfigLoader
from controllers import translation_openapi

def init_service():
    argument_parser = ArgumentParser()
    args = argument_parser.parse_arguments()
    config_loader = ConfigLoader(args.config)

    config = config_loader.load_config()

    global_service = SingletonService(config=config)

def main():
    app = FastAPI()

    app.include_router(translation_openapi.router)

    init_service()

    return app



if __name__ == "__main__":
    uvicorn.run("main:main", host="127.0.0.1", port=8000, reload=True)