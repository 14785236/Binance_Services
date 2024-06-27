import json
import time
import uuid

from urllib.parse import urlparse
from collections import OrderedDict
from urllib.parse import urlencode
from binance.lib.authentication import hmac_hashing
from binance.error import (
    ParameterRequiredError,
    ParameterValueError,
    ParameterTypeError,
    WebsocketClientError,
)


def cleanNoneValue(d) -> dict:
    # 移除字典中值为 None 的键值对
    out = {}
    for k in d.keys():
        if d[k] is not None:
            out[k] = d[k]
    return out


def check_required_parameter(value, name):
    # 检查参数是否存在，如果不存在则抛出 ParameterRequiredError 异常
    if not value and value != 0:
        raise ParameterRequiredError([name])


def check_required_parameters(params):
    """验证多个参数
    参数格式：
    params = [
        ['btcusdt', 'symbol'],
        [10, 'price']
    ]
    """
    for p in params:
        check_required_parameter(p[0], p[1])


def check_enum_parameter(value, enum_class):
    # 检查值是否在枚举类中，如果不在则抛出 ParameterValueError 异常
    if value not in set(item.value for item in enum_class):
        raise ParameterValueError([value])


def check_type_parameter(value, name, data_type):
    # 检查参数的类型是否符合预期，如果不符合则抛出 ParameterTypeError 异常
    if value is not None and not isinstance(value, data_type):
        raise ParameterTypeError([name, data_type])


def get_timestamp():
    # 获取当前时间的时间戳（毫秒）
    return int(time.time() * 1000)


def encoded_string(query):
    # 对查询字符串进行编码，并替换特殊字符
    return urlencode(query, True).replace("%40", "@")


def convert_list_to_json_array(symbols):
    # 将列表转换为 JSON 数组格式的字符串
    if symbols is None:
        return symbols
    res = json.dumps(symbols)
    return res.replace(" ", "")


def config_logging(logging, logging_level, log_file: str = None):
    """配置日志记录格式，包含以 UTC 格式显示的日期时间
    示例: 2021-11-02 19:42:04.849 UTC <日志级别> <日志名称>: <日志消息>

    参数:
        logging: Python 日志模块
        logging_level (int/str): 日志级别，记录大于等于该级别的所有消息。例：10 或 "DEBUG"
                                 日志级别基于 https://docs.python.org/3/library/logging.html#logging-levels
    关键字参数:
        log_file (str, optional): 如果指定，则将日志记录到该文件中，而不是使用控制台。默认文件模式："a"
    """
    logging.Formatter.converter = time.gmtime  # 日期时间设置为 GMT/UTC
    logging.basicConfig(
        level=logging_level,
        filename=log_file,
        format="%(asctime)s.%(msecs)03d UTC %(levelname)s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def get_uuid():
    # 生成一个唯一标识符 (UUID)
    return str(uuid.uuid4())


def purge_map(map: map):
    """从字典中移除值为 None、空字符串或 0 的键值对"""
    return {k: v for k, v in map.items() if v is not None and v != "" and v != 0}


def websocket_api_signature(api_key: str, api_secret: str, parameters: dict):
    """为 Websocket API 生成签名
    参数:
        api_key (str): API 密钥。
        api_secret (str): API 密钥。
        params (dict): 参数。
    """
    if not api_key or not api_secret:
        raise WebsocketClientError(
            "websocket API 签名需要 api_key 和 api_secret"
        )

    parameters["timestamp"] = get_timestamp()
    parameters["apiKey"] = api_key

    parameters = OrderedDict(sorted(parameters.items()))
    parameters["signature"] = hmac_hashing(api_secret, urlencode(parameters))

    return parameters


def parse_proxies(proxies: dict):
    """从字典中解析代理 URL，只支持 http 和 https 代理，不支持 socks5 代理"""
    proxy_url = proxies.get("http") or proxies.get("https")
    if not proxy_url:
        return {}

    parsed = urlparse(proxy_url)
    return {
        "http_proxy_host": parsed.hostname,
        "http_proxy_port": parsed.port,
        "http_proxy_auth": (
            (parsed.username, parsed.password)
            if parsed.username and parsed.password
            else None
        ),
    }
