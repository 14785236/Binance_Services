from binance.error import ParameterArgumentError
from binance.lib.utils import (
    check_required_parameter,
    check_type_parameter,
    convert_list_to_json_array,
)
from binance.lib.utils import check_required_parameters


def ping(self):
    """测试连接
    测试与REST API的连接。

    GET /api/v3/ping

    https://binance-docs.github.io/apidocs/spot/en/#test-connectivity

    """

    url_path = "/api/v3/ping"
    return self.query(url_path)

def time(self):
    """检查服务器时间
    测试与REST API的连接并获取当前服务器时间。

    GET /api/v3/time

    https://binance-docs.github.io/apidocs/spot/en/#check-server-time

    """

    url_path = "/api/v3/time"
    return self.query(url_path)


def exchange_info(
    self, symbol: str = None, symbols: list = None, permissions: list = None
):
    """交易所信息
    当前交易所的交易规则和交易对信息。

    GET /api/v3/exchangeinfo

    https://binance-docs.github.io/apidocs/spot/en/#exchange-information

     Args:
        symbol (str, optional): 交易对
        symbols (list, optional): 交易对列表
        permissions (list, optional): 显示所有符合提供参数的权限的交易对（例如 SPOT、MARGIN、LEVERAGED）
    """

    url_path = "/api/v3/exchangeInfo"
    if symbol and symbols:
        raise ParameterArgumentError("不能同时发送 symbol 和 symbols 参数。")
    if symbol and permissions or symbols and permissions:
        raise ParameterArgumentError(
            "不能将 permissions 参数与 symbol 或 symbols 参数一起发送。"
        )
    check_type_parameter(symbols, "symbols", list)
    check_type_parameter(permissions, "permissions", list)

    params = {
        "symbol": symbol,
        "symbols": convert_list_to_json_array(symbols),
        "permissions": convert_list_to_json_array(permissions),
    }
    return self.query(url_path, params)


def depth(self, symbol: str, **kwargs):
    """获取订单簿.

    GET /api/v3/depth

    https://binance-docs.github.io/apidocs/spot/en/#order-book

    Args:
        symbol (str): 交易对
    Keyword Args:
        limit (int, optional): 限制结果数量。默认 100；最大 5000。如果 limit > 5000，则响应将截断为 5000。
    """

    check_required_parameter(symbol, "symbol")
    params = {"symbol": symbol, **kwargs}
    return self.query("/api/v3/depth", params)


def trades(self, symbol: str, **kwargs):
    """最近交易列表
    获取最近的交易（最多500条）。

    GET /api/v3/trades

    https://binance-docs.github.io/apidocs/spot/en/#recent-trades-list

    Args:
        symbol (str): 交易对
    Keyword Args:
        limit (int, optional): 限制结果数量。默认 500；最大 1000。
    """
    check_required_parameter(symbol, "symbol")
    params = {"symbol": symbol, **kwargs}
    return self.query("/api/v3/trades", params)


def historical_trades(self, symbol: str, **kwargs):
    """旧交易查询
    获取更早的市场交易记录。

    GET /api/v3/historicalTrades

    https://binance-docs.github.io/apidocs/spot/en/#old-trade-lookup

    Args:
        symbol (str): 交易对
    Keyword Args:
        limit (int, optional): 限制结果数量。默认 500；最大 1000。
        formId (int, optional): 要获取的交易 ID。默认获取最近的交易。
    """
    check_required_parameter(symbol, "symbol")
    params = {"symbol": symbol, **kwargs}
    return self.query("/api/v3/historicalTrades", params)


def agg_trades(self, symbol: str, **kwargs):
    """压缩/聚合交易列表

    GET /api/v3/aggTrades

    https://binance-docs.github.io/apidocs/spot/en/#compressed-aggregate-trades-list

    Args:
        symbol (str): 交易对
    Keyword Args:
        limit (int, optional): 限制结果数量。默认 500；最大 1000。
        formId (int, optional): 从该 ID 开始获取聚合交易（包含此 ID）。
        startTime (int, optional): 开始获取聚合交易的时间戳（包含此时间戳）。
        endTime (int, optional): 结束获取聚合交易的时间戳（包含此时间戳）。
    """

    check_required_parameter(symbol, "symbol")
    params = {"symbol": symbol, **kwargs}
    return self.query("/api/v3/aggTrades", params)


def klines(self, symbol: str, interval: str, **kwargs):
    """K线图数据

    GET /api/v3/klines

    https://binance-docs.github.io/apidocs/spot/en/#kline-candlestick-data

    Args:
        symbol (str): 交易对
        interval (str): K线图的时间间隔，例如 1s, 1m, 5m, 1h, 1d 等。
    Keyword Args:
        limit (int, optional): 限制结果数量。默认 500；最大 1000。
        startTime (int, optional): 开始获取K线图数据的时间戳（包含此时间戳）。
        endTime (int, optional): 结束获取K线图数据的时间戳（包含此时间戳）。
    """
    check_required_parameters([[symbol, "symbol"], [interval, "interval"]])

    params = {"symbol": symbol, "interval": interval, **kwargs}
    return self.query("/api/v3/klines", params)


def ui_klines(self, symbol: str, interval: str, **kwargs):
    """K线图数据

    GET /api/v3/uiKlines

    https://binance-docs.github.io/apidocs/spot/en/#uiklines

    Args:
        symbol (str): 交易对
        interval (str): K线图的时间间隔，例如 1s, 1m, 5m, 1h, 1d 等。
    Keyword Args:
        limit (int, optional): 限制结果数量。默认 500；最大 1000。
        startTime (int, optional): 开始获取K线图数据的时间戳（包含此时间戳）。
        endTime (int, optional): 结束获取K线图数据的时间戳（包含此时间戳）。
    """
    check_required_parameters([[symbol, "symbol"], [interval, "interval"]])

    params = {"symbol": symbol, "interval": interval, **kwargs}
    return self.query("/api/v3/uiKlines", params)


def avg_price(self, symbol: str):
    """当前平均价格

    GET /api/v3/avgPrice

    https://binance-docs.github.io/apidocs/spot/en/#current-average-price

    Args:
        symbol (str): 交易对
    """

    check_required_parameter(symbol, "symbol")
    params = {
        "symbol": symbol,
    }
    return self.query("/api/v3/avgPrice", params)


def ticker_24hr(self, symbol: str = None, symbols: list = None, **kwargs):
    """24小时价格变动统计

    GET /api/v3/ticker/24hr

    https://binance-docs.github.io/apidocs/spot/en/#24hr-ticker-price-change-statistics

    Args:
        symbol (str, optional): 交易对
        symbols (list, optional): 交易对列表
    """

    if symbol and symbols:
        raise ParameterArgumentError("不能同时发送 symbol 和 symbols 参数。")
    check_type_parameter(symbols, "symbols", list)
    params = {
        "symbol": symbol,
        "symbols": convert_list_to_json_array(symbols),
        **kwargs,
    }
    return self.query("/api/v3/ticker/24hr", params)


def trading_day_ticker(self, symbol: str = None, symbols: list = None):
    """当日交易统计

    GET /api/v3/ticker/tradingDay

    https://binance-docs.github.io/apidocs/spot/en/#trading-day-ticker

    Args:
        symbol (str, optional): 必须提供 symbol 或 symbols 参数之一
        symbols (list, optional): 交易对列表
    Keyword Args:
        timeZone (str, optional): 默认：0 (UTC)
        type (str, optional): 支持的值为 FULL 或 MINI。如果未提供，默认为 FULL。
    """
    if symbol and symbols:
        raise ParameterArgumentError("不能同时发送 symbol 和 symbols 参数。")

    check_type_parameter(symbols, "symbols", list)
    params = {"symbol": symbol, "symbols": convert_list_to_json_array(symbols)}
    return self.query("/api/v3/ticker/tradingDay", params)


def ticker_price(self, symbol: str = None, symbols: list = None):
    """交易对价格
    获取交易对的当前价格信息。

    GET /api/v3/ticker/price

    https://binance-docs.github.io/apidocs/spot/en/#symbol-price-ticker

    Args:
        symbol (str, optional): 交易对
        symbols (list, optional): 交易对列表
    """

    if symbol and symbols:
        raise ParameterArgumentError("不能同时发送 symbol 和 symbols 参数。")
    check_type_parameter(symbols, "symbols", list)
    params = {"symbol": symbol, "symbols": convert_list_to_json_array(symbols)}
    return self.query("/api/v3/ticker/price", params)


def book_ticker(self, symbol: str = None, symbols: list = None):
    """订单簿价格
    获取交易对的当前订单簿价格信息。

    GET /api/v3/ticker/bookTicker

    https://binance-docs.github.io/apidocs/spot/en/#symbol-order-book-ticker

    Args:
        symbol (str, optional): 交易对
        symbols (list, optional): 交易对列表
    """

    if symbol and symbols:
        raise ParameterArgumentError("不能同时发送 symbol 和 symbols 参数。")
    check_type_parameter(symbols, "symbols", list)
    params = {"symbol": symbol, "symbols": convert_list_to_json_array(symbols)}
    return self.query("/api/v3/ticker/bookTicker", params)


def rolling_window_ticker(self, symbol: str = None, symbols: list = None, **kwargs):
    """滚动窗口价格变动统计

    用于计算统计的窗口通常略大于请求的窗口大小。

    /api/v3/ticker 的 openTime 始终从分钟开始，而 closeTime 是请求的当前时间。因此，有效的窗口可能比请求的窗口宽多达 1 分钟。

    例如，如果 closeTime 是 1641287867099（2022年1月4日 09:17:47:099 UTC），而 windowSize 是 1d，则 openTime 将为：1641201420000（2022年1月3日 09:17:00 UTC）

    权重（IP）：对每个请求的交易对权重为2，无论 windowSize 大小如何。一旦请求中的交易对数量超过50，此请求的权重将上限为100。

    GET /api/v3/ticker

    https://binance-docs.github.io/apidocs/spot/en/#rolling-window-price-change-statistics

    Args:
        symbol (str, optional): 交易对
        symbols (str, optional): 交易对列表。请求中允许的交易对数量最大为100。
    Keyword Args:
        windowSize (str, optional): 如果未提供参数，默认为 1d。
    """

    if symbol and symbols:
        raise ParameterArgumentError("不能同时发送 symbol 和 symbols 参数。")
    check_type_parameter(symbols, "symbols", list)
    params = {
        "symbol": symbol,
        "symbols": convert_list_to_json_array(symbols),
        **kwargs,
    }
    url_path = "/api/v3/ticker"
    return self.query(url_path, params)
