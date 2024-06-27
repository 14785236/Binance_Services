import json
from json import JSONDecodeError
import logging
import requests
from .__version__ import __version__
from binance.error import ClientError, ServerError
from binance.lib.utils import get_timestamp
from binance.lib.utils import cleanNoneValue
from binance.lib.utils import encoded_string
from binance.lib.utils import check_required_parameter
from binance.lib.authentication import hmac_hashing, rsa_signature, ed25519_signature


class API(object):
    """API基础类

    Keyword Args:
        base_url (str, optional): API的基础URL，用于切换到测试网等。默认为 https://api.binance.com
        timeout (int, optional): 等待服务器响应的时间，单位秒。参考：https://docs.python-requests.org/en/master/user/advanced/#timeouts
        proxies (obj, optional): 映射协议到代理URL的字典。例如 {'https': 'http://1.2.3.4:8080'}
        show_limit_usage (bool, optional): 是否返回请求和/或订单的使用限制。默认为 False
        show_header (bool, optional): 是否返回完整的响应头。默认为 False
        private_key (str, optional): RSA私钥，用于RSA认证
        private_key_pass(str, optional): PSA私钥的密码
    """

    def __init__(
            self,
            api_key=None,
            api_secret=None,
            base_url=None,
            timeout=None,
            proxies=None,
            show_limit_usage=False,
            show_header=False,
            private_key=None,
            private_key_pass=None,
    ):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url or "https://api.binance.com"
        self.timeout = timeout
        self.proxies = None
        self.show_limit_usage = False
        self.show_header = False
        self.private_key = private_key
        self.private_key_pass = private_key_pass
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/json;charset=utf-8",
                "User-Agent": "binance-connector-python/" + __version__,
                "X-MBX-APIKEY": api_key,
            }
        )

        if show_limit_usage:
            self.show_limit_usage = True

        if show_header:
            self.show_header = True

        if isinstance(proxies, dict):
            self.proxies = proxies

        self._logger = logging.getLogger(__name__)
        return

    def query(self, url_path, payload=None):
        """执行查询请求"""
        return self.send_request("GET", url_path, payload=payload)

    def limit_request(self, http_method, url_path, payload=None):
        """限制请求用于那些需要在头部中包含API密钥的端点"""
        check_required_parameter(self.api_key, "api_key")
        return self.send_request(http_method, url_path, payload=payload)

    def sign_request(self, http_method, url_path, payload=None):
        """签名请求"""
        if payload is None:
            payload = {}
        payload["timestamp"] = get_timestamp()
        query_string = self._prepare_params(payload)
        payload["signature"] = self._get_sign(query_string)
        return self.send_request(http_method, url_path, payload)

    def limited_encoded_sign_request(self, http_method, url_path, payload=None):
        """用于某些端点具有URL中特殊符号的情况"""
        if payload is None:
            payload = {}
        payload["timestamp"] = get_timestamp()
        query_string = self._prepare_params(payload)
        url_path = (
                url_path + "?" + query_string + "&signature=" + self._get_sign(query_string)
        )
        return self.send_request(http_method, url_path)

    def send_request(self, http_method, url_path, payload=None):
        """发送HTTP请求"""
        if payload is None:
            payload = {}
        url = self.base_url + url_path
        self._logger.debug("url: " + url)
        params = cleanNoneValue(
            {
                "url": url,
                "params": self._prepare_params(payload),
                "timeout": self.timeout,
                "proxies": self.proxies,
            }
        )
        response = self._dispatch_request(http_method)(**params)
        self._logger.debug("raw response from server:" + response.text)
        self._handle_exception(response)

        try:
            data = response.json()
        except ValueError:
            data = response.text
        result = {}

        if self.show_limit_usage:
            limit_usage = {}
            for key in response.headers.keys():
                key = key.lower()
                if (
                        key.startswith("x-mbx-used-weight")
                        or key.startswith("x-mbx-order-count")
                        or key.startswith("x-sapi-used")
                ):
                    limit_usage[key] = response.headers[key]
            result["limit_usage"] = limit_usage

        if self.show_header:
            result["header"] = response.headers

        if result:
            result["data"] = data
            return result

        return data

    def _prepare_params(self, params):
        """准备请求参数"""
        return encoded_string(cleanNoneValue(params))

    def _get_sign(self, payload):
        """获取签名"""
        if self.private_key is not None:
            try:
                return ed25519_signature(
                    self.private_key, payload, self.private_key_pass
                )
            except ValueError:
                return rsa_signature(self.private_key, payload, self.private_key_pass)
        else:
            return hmac_hashing(self.api_secret, payload)

    def _dispatch_request(self, http_method):
        """分发请求"""
        return {
            "GET": self.session.get,
            "DELETE": self.session.delete,
            "PUT": self.session.put,
            "POST": self.session.post,
        }.get(http_method, "GET")

    def _handle_exception(self, response):
        """处理异常"""
        status_code = response.status_code
        if status_code < 400:
            return
        if 400 <= status_code < 500:
            try:
                err = json.loads(response.text)
            except JSONDecodeError:
                raise ClientError(
                    status_code, None, response.text, None, response.headers
                )
            error_data = None
            if "data" in err:
                error_data = err["data"]
            raise ClientError(
                status_code, err["code"], err["msg"], response.headers, error_data
            )
        raise ServerError(status_code, response.text)
