import json
import re


def camel_to_snake(name):
    """Convert a camel case string to snake case."""
    name_with_underscores = re.sub(r'([A-Z]+)', r'_\1', name)
    snake_case_name = name_with_underscores.lower().lstrip('_')
    return snake_case_name


def convert_dict_keys_to_snake(d):
    """Recursively converts dictionary keys from camelCase to snake_case."""
    if isinstance(d, list):
        return [convert_dict_keys_to_snake(item) for item in d]
    if not isinstance(d, dict):
        return d  # 如果不是字典类型，直接返回

    new_dict = {}
    for key, value in d.items():
        new_key = camel_to_snake(key)
        if isinstance(value, (dict, list)):
            new_dict[new_key] = convert_dict_keys_to_snake(value)
        else:
            new_dict[new_key] = value
    return new_dict


def json_camel_to_snake(json_str):
    """Convert all keys in a JSON string from camelCase to snake_case."""
    try:
        # 将JSON字符串解析为Python对象（字典或列表）
        data = json.loads(json_str)
        # 转换键名为下划线命名法
        converted_data = convert_dict_keys_to_snake(data)
        # 将转换后的数据结构序列化回JSON字符串
        return json.dumps(converted_data)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")
        return None


def snake_to_camel(snake_str):
    """Convert a snake case string to camel case."""
    components = snake_str.split('_')
    # 将第一个单词保持小写，其他单词首字母大写，并连接起来。
    return components[0] + ''.join(x.title() for x in components[1:])


def convert_dict_keys_to_camel(d):
    """Recursively converts dictionary keys from snake_case to camelCase."""
    if isinstance(d, list):
        return [convert_dict_keys_to_camel(item) for item in d]
    if not isinstance(d, dict):
        return d  # 如果不是字典类型，直接返回

    new_dict = {}
    for key, value in d.items():
        new_key = snake_to_camel(key)
        if isinstance(value, (dict, list)):
            new_dict[new_key] = convert_dict_keys_to_camel(value)
        else:
            new_dict[new_key] = value
    return new_dict


def json_snake_to_camel(json_str):
    """Convert all keys in a JSON string from snake_case to camelCase."""
    try:
        # 解析JSON字符串为Python对象（字典或列表）
        data = json.loads(json_str)
        # 转换键名为驼峰命名法
        converted_data = convert_dict_keys_to_camel(data)
        # 序列化回JSON字符串
        return json.dumps(converted_data)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")
        return None
