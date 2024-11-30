# 定义一个名为functions的列表，其中包含两个字典，这两个字典分别定义了两个功能的相关参数
# 第一个字典定义了一个名为"get_current_weather"的功能
functions = [
    {
        "name": "get_current_weather",  # 功能的名称
        "description": "Get the current weather",  # 功能的描述
        "parameters": {  # 定义该功能需要的参数
            "type": "object",
            "properties": {  # 参数的属性
                "location": {  # 地点参数
                    "type": "string",  # 参数类型为字符串
                    "description": "The city and state, e.g. San Francisco, CA",  # 参数的描述
                },
                "format": {  # 温度单位参数
                    "type": "string",  # 参数类型为字符串
                    "enum": ["celsius", "fahrenheit"],  # 参数的取值范围
                    "description": "The temperature unit to use. Infer this from the users location.",  # 参数的描述
                },
            },
            "required": ["location", "format"],  # 该功能需要的必要参数
        },
    },
    # 第二个字典定义了一个名为"get_n_day_weather_forecast"的功能
    {
        "name": "get_n_day_weather_forecast",  # 功能的名称
        "description": "Get an N-day weather forecast",  # 功能的描述
        "parameters": {  # 定义该功能需要的参数
            "type": "object",
            "properties": {  # 参数的属性
                "location": {  # 地点参数
                    "type": "string",  # 参数类型为字符串
                    "description": "The city and state, e.g. San Francisco, CA",  # 参数的描述
                },
                "format": {  # 温度单位参数
                    "type": "string",  # 参数类型为字符串
                    "enum": ["celsius", "fahrenheit"],  # 参数的取值范围
                    "description": "The temperature unit to use. Infer this from the users location.",  # 参数的描述
                },
                "num_days": {  # 预测天数参数
                    "type": "integer",  # 参数类型为整数
                    "description": "The number of days to forecast",  # 参数的描述
                }
            },
            "required": ["location", "format", "num_days"]  # 该功能需要的必要参数
        },
    },
]
