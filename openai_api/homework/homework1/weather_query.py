import gzip
import http.client
import json
import urllib

from openai_api.homework.homework1.functions import functions
from openai_api.homework.util import chat_completion_request, pretty_print_conversation, generate_jwt


def get_location_id(jwt: str, location: str):
    """用于查询城市的location id
    location: 城市名。如：北京、beijing
    """
    conn = http.client.HTTPSConnection("geoapi.qweather.com")
    payload = ''
    headers = {
        'Authorization': f'Bearer {jwt}'
    }
    location_encode = urllib.parse.quote(location) # 对中文需要进行编码
    conn.request("GET", f"/v2/city/lookup?location={location_encode}", payload, headers)
    res = conn.getresponse()
    data = res.read()
    decompressed_data = gzip.decompress(data)
    data = decompressed_data.decode('utf-8')
    # print(data)
    data_json = json.loads(data)
    location_id = data_json['location'][0]['id']
    print(f"location: {location}, location_id: {location_id}")
    return location_id

def get_current_weather(jwt: str, location: str, format: str = "celsius"):
    location_id = get_location_id(jwt, location)
    url = f'/v7/weather/now?location={location_id}'
    conn = http.client.HTTPSConnection("devapi.qweather.com")
    payload = ''
    headers = {
        'Authorization': f'Bearer {jwt}'
    }
    conn.request("GET", url, payload, headers)
    res = conn.getresponse()
    data = res.read()
    decompressed_data = gzip.decompress(data)
    data = decompressed_data.decode('utf-8')
    # print(data)
    data_json = json.loads(data)
    weather = data_json['now']
    return weather

def get_n_day_weather_forecast(jwt: str, location: str, days: int, format: str = "celsius"):
    """用于查询未来几天的天气
    location_id: 城市名
    days：预测的天数。只支持3、7、10、15、30天
    format: 摄氏度/华氏度
    """
    if days not in [3, 7, 10, 15, 30]:
        return f"weather forecast only support [3, 7, 10, 15, 30] days, not support {days}!\n"

    location_id = get_location_id(jwt, location)
    url = f'/v7/weather/{days}d?location={location_id}'
    conn = http.client.HTTPSConnection("devapi.qweather.com")
    payload = ''
    headers = {
        'Authorization': f'Bearer {jwt}'
    }
    conn.request("GET", url, payload, headers)
    res = conn.getresponse()
    data = res.read()
    decompressed_data = gzip.decompress(data)
    data = decompressed_data.decode('utf-8')
    # print(data)
    data_json = json.loads(data)
    weather = data_json['daily']
    return weather

def execute_function_call(jwt: str, message: str):
    """执行函数调用"""
    # 判断功能调用的名称是否为 "get_current_weather"
    if message["function_call"]["name"] == "get_current_weather":
        location = json.loads(message["function_call"]["arguments"])["location"]
        format = json.loads(message["function_call"]["arguments"])["format"]
        results = get_current_weather(jwt, location, format)
    elif message["function_call"]["name"] == "get_n_day_weather_forecast":
        location = json.loads(message["function_call"]["arguments"])["location"]
        format = json.loads(message["function_call"]["arguments"])["format"]
        num_days = json.loads(message["function_call"]["arguments"])["num_days"]
        results = get_n_day_weather_forecast(jwt, location, num_days, format)
    else:
        results = f"Error: function {message['function_call']['name']} does not exist"
    return results  # 返回结果


def main(jwt: str, messages: list):
    # 再次使用定义的chat_completion_request函数发起一个请求，传入更新后的messages和functions作为参数
    chat_response = chat_completion_request(
        messages, functions=functions
    )

    # 解析返回的JSON数据，获取助手的新的回复消息
    assistant_message = chat_response.json()["choices"][0]["message"]

    # 将助手的新的回复消息添加到messages列表中
    messages.append(assistant_message)

    # 如果助手的消息中有功能调用
    if assistant_message.get("function_call"):
        # 使用 execute_function_call 函数执行功能调用，并获取结果
        results = execute_function_call(jwt, assistant_message)
        # 将功能的结果作为一个功能角色的消息添加到消息列表中
        messages.append({"role": "function", "name": assistant_message["function_call"]["name"], "content": results})

    pretty_print_conversation(messages)



if __name__ == "__main__":
    jwt = generate_jwt()

    messages = []
    messages.append({
        "role": "system",  # 消息的角色是"system"
        "content": "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous."
    })
    messages.append({
        "role": "user",  # 消息的角色是"user"
        "content": "what is the weather going to be like in Shanghai, China over the next 3 days"
    })
    main(jwt, messages)