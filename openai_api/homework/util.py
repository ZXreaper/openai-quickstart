import os
import time

import jwt
import requests
from dotenv import load_dotenv
from tenacity import retry, wait_random_exponential, stop_after_attempt
from termcolor import colored

GPT_MODEL = "gpt-3.5-turbo"


# 定义一个函数chat_completion_request，主要用于发送 聊天补全 请求到OpenAI服务器
@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, functions=None, function_call=None, model=GPT_MODEL):

    # 设定请求的header信息，包括 API_KEY
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + "sk-3TVqzS5kKYHVI0Ox9280B6314fA2441597E18c5072840dD5",
    }

    # 设定请求的JSON数据，包括GPT 模型名和要进行补全的消息
    json_data = {"model": model, "messages": messages}

    # 如果传入了functions，将其加入到json_data中
    if functions is not None:
        json_data.update({"functions": functions})

    # 如果传入了function_call，将其加入到json_data中
    if function_call is not None:
        json_data.update({"function_call": function_call})

    # 尝试发送POST请求到OpenAI服务器的chat/completions接口
    try:
        response = requests.post(
            "https://4.0.wokaai.com/v1/chat/completions",
            headers=headers,
            json=json_data,
        )
        # 返回服务器的响应
        return response

    # 如果发送请求或处理响应时出现异常，打印异常信息并返回
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e


# 定义一个函数pretty_print_conversation，用于打印消息对话内容
def pretty_print_conversation(messages):

    # 为不同角色设置不同的颜色
    role_to_color = {
        "system": "red",
        "user": "green",
        "assistant": "blue",
        "function": "magenta",
    }

    # 遍历消息列表
    for message in messages:

        # 如果消息的角色是"system"，则用红色打印“content”
        if message["role"] == "system":
            print(colored(f"system: {message['content']}\n", role_to_color[message["role"]]))

        # 如果消息的角色是"user"，则用绿色打印“content”
        elif message["role"] == "user":
            print(colored(f"user: {message['content']}\n", role_to_color[message["role"]]))

        # 如果消息的角色是"assistant"，并且消息中包含"function_call"，则用蓝色打印"function_call"
        elif message["role"] == "assistant" and message.get("function_call"):
            print(colored(f"assistant[function_call]: {message['function_call']}\n", role_to_color[message["role"]]))

        # 如果消息的角色是"assistant"，但是消息中不包含"function_call"，则用蓝色打印“content”
        elif message["role"] == "assistant" and not message.get("function_call"):
            print(colored(f"assistant[content]: {message['content']}\n", role_to_color[message["role"]]))

        # 如果消息的角色是"function"，则用品红色打印“function”
        elif message["role"] == "function":
            print(colored(f"function ({message['name']}): {message['content']}\n", role_to_color[message["role"]]))

def generate_jwt():
    load_dotenv(dotenv_path="/Users/zhangxu/D/openai-quickstart/openai_api/homework/config/config.env")
    private_key_path = os.getenv("JWT_PRIVATE_KEY_PATH")
    print(private_key_path)
    private_key = open(private_key_path, "r", encoding='utf-8').read()

    payload = {
        'iat': int(time.time()) - 30,
        'exp': int(time.time()) + 900,
        'sub': os.getenv("JWT_SUB"),
    }
    headers = {
        'kid': os.getenv("JWT_KID"),
    }

    # Generate JWT
    encoded_jwt = jwt.encode(payload, private_key, algorithm='EdDSA', headers=headers)

    print(f"JWT:  {encoded_jwt}")
    return encoded_jwt

if __name__ == "__main__":
    generate_jwt()