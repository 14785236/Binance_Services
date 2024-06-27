from binance.lib.utils import parse_proxies
from binance.spot import Spot as Client

proxies = {'https': 'http://127.0.0.1:33210'}


if __name__ == '__main__':
    parse_proxies(proxies)
    client = Client(proxies=proxies, base_url='https://testnet.binance.vision')
    print(client.time())
    # # 获取服务器时间戳
    # print(client.time())
    # # 获取 BTCUSDT 1 分钟间隔的 k线
    # print(client.klines("BTCUSDT", "1m"))
    # # 获取 BNBUSDT 1 小时间隔的最近 10 个 k线
    # print(client.klines("BNBUSDT", "1h", limit=10))
