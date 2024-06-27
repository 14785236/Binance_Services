
---

# Binance 公共 API 连接器 Python

PyPI 版本 | Python 版本 | 文档 | 代码风格 | 许可证 MIT

这是一个轻量级库，用作 Binance 公共 API 的连接器

### 支持的 API：
- `/api/*`
- `/sapi/*`
- 现货 Websocket 市场流
- 现货用户数据流
- 现货 WebSocket API
- 包含测试用例和示例
- 可定制的基础 URL、请求超时和 HTTP 代理
- 可以显示响应元数据

### 安装

```bash
pip install binance-connector
```

### 文档

[https://binance-connector.readthedocs.io](https://binance-connector.readthedocs.io)

## RESTful API

### 使用示例：

```python
from binance.spot import Spot

client = Spot()

# 获取服务器时间戳
print(client.time())
# 获取 BTCUSDT 1 分钟间隔的 k线
print(client.klines("BTCUSDT", "1m"))
# 获取 BNBUSDT 1 小时间隔的最近 10 个 k线
print(client.klines("BNBUSDT", "1h", limit=10))

# 用户数据端点需要 API key/secret
client = Spot(api_key='<api_key>', api_secret='<api_secret>')

# 获取账户和余额信息
print(client.account())

# 新建订单
params = {
    'symbol': 'BTCUSDT',
    'side': 'SELL',
    'type': 'LIMIT',
    'timeInForce': 'GTC',
    'quantity': 0.002,
    'price': 9500
}

response = client.new_order(**params)
print(response)
```

请查看 `examples` 文件夹以获取更多端点示例。

为了设置示例使用的 API 和 Secret Key，创建一个 `examples/config.ini` 文件并填写你的密钥。
例如：

```ini
# examples/config.ini
[keys]
api_key=abc123456
api_secret=cba654321
```

### 身份验证

Binance 支持 HMAC、RSA 和 ED25519 API 身份验证。

```python
# HMAC：传递 API key 和 secret
client = Client(api_key, api_secret)
print(client.account())

# RSA 密钥
client = Client(api_key=api_key, private_key=private_key)
print(client.account())

# ED25519 密钥
api_key = ""
private_key = "./private_key.pem"
private_key_pass = "<password_if_applicable>"

with open(private_key, 'rb') as f:
    private_key = f.read()

spot_client = Client(api_key=api_key, private_key=private_key, private_key_pass=private_key_pass)

# 加密的 RSA 密钥
client = Client(api_key=api_key, private_key=private_key, private_key_pass='password')
print(client.account())
```

请查看 `examples/spot/wallet/account_snapshot.py` 获取更多关于 ED25519 的细节。请查看 `examples/spot/trade/get_account.py` 获取更多关于 RSA 的细节。

### 测试网络

现货测试网络可用，可用于测试 `/api/*` 端点。

`/sapi/*` 端点不可用。无用户界面。
设置测试网络 API 密钥的步骤： [https://dev.binance.vision/t/99](https://dev.binance.vision/t/99)

要使用测试网络：

```python
from binance.spot import Spot as Client

client = Client(base_url='https://testnet.binance.vision')
print(client.time())
```

### 基础 URL

如果未提供 `base_url`，则默认为 `api.binance.com`。
建议在生产环境中传入 `base_url` 参数，因为 Binance 提供了备用 URL 以防止性能问题：

- `https://api1.binance.com`
- `https://api2.binance.com`
- `https://api3.binance.com`

### 可选参数

PEP8 建议使用小写并用下划线分隔单词，但对于此连接器，方法的可选参数应遵循 API 文档中的确切命名。

```python
# 认可的参数名
response = client.cancel_oco_order('BTCUSDT', orderListId=1)

# 不认可的参数名
response = client.cancel_oco_order('BTCUSDT', order_list_id=1)
```

### RecvWindow 参数

需要签名的端点可用的附加参数 `recvWindow`。默认为 5000（毫秒），可以是任何小于 60000（毫秒）的值。超过此限制将导致 Binance 服务器返回错误响应。

```python
from binance.spot import Spot as Client

client = Client(api_key, api_secret)
response = client.get_order('BTCUSDT', orderId=11, recvWindow=10000)
```

### 超时

`timeout` 可用于设置等待服务器响应的秒数。
请记住该值，因为当在超时秒数内未接收到任何数据时，它不会显示在错误消息中。默认情况下，`timeout` 为 `None`，因此请求不会超时。

```python
from binance.spot import Spot as Client

client = Client(timeout=1)
```

### 代理

支持代理。

```python
from binance.spot import Spot as Client

proxies = { 'https': 'http://1.2.3.4:8080' }

client = Client(proxies=proxies)
```

### 响应元数据

Binance API 服务器在每个响应的头部提供权重使用情况。你可以通过初始化客户端时设置 `show_limit_usage=True` 来显示它们：

```python
from binance.spot import Spot as Client

client = Client(show_limit_usage=True)
print(client.time())
```

返回：

```json
{'data': {'serverTime': 1587990847650}, 'limit_usage': {'x-mbx-used-weight': '31', 'x-mbx-used-weight-1m': '31'}}
```

你还可以显示完整的响应元数据以帮助调试：

```python
client = Client(show_header=True)
print(client.time())
```

返回：

```json
{'data': {'serverTime': 1587990847650}, 'header': {'Context-Type': 'application/json;charset=utf-8', ...}}
```

如果收到 `ClientError`，它会显示完整的响应元信息。

### 显示日志

将日志级别设置为 `DEBUG` 会记录请求 URL、负载和响应文本。

### 错误

库中返回的错误有两种类型：

- `binance.error.ClientError`
  - 当服务器返回 4XX 时抛出，这是客户端的问题。
  - 它有 5 个属性：
    - `status_code` - HTTP 状态码
    - `error_code` - 服务器的错误代码，例如 -1102
    - `error_message` - 服务器的错误消息，例如 "Unknown order sent."
    - `header` - 完整的响应头
    - `error_data`* - 补充 `error_message` 的详细数据。
  - *仅适用于某些端点，例如 `cancelReplace`

- `binance.error.ServerError`
  - 当服务器返回 5XX 时抛出，这是服务器的问题。

## Websocket

### 连接器 v3

WebSocket 可以通过以下类型的连接来建立：

- [WebSocket API](https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-api.md)
- [WebSocket Stream](https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md)

```python
# WebSocket API 客户端
from binance.websocket.spot.websocket_api import SpotWebsocketAPIClient

def message_handler(_, message):
    logging.info(message)

my_client = SpotWebsocketAPIClient(on_message=message_handler)

my_client.ticker(symbol="BNBBUSD", type="FULL")

time.sleep(5)
logging.info("closing ws connection")
my_client.stop()
```

```python
# WebSocket 流客户端
from binance.websocket.spot.websocket_stream import SpotWebsocketStreamClient

def message_handler(_, message):
    logging.info(message)

my_client = SpotWebsocketStreamClient(on_message=message_handler)

# 订阅单个符号流
my_client.agg_trade(symbol="bnbusdt")
time.sleep(5)
logging.info("closing ws connection")
my_client.stop()
```

### 代理

WebSocket API 和 WebSocket 流都支持代理。

要使用它，在初始化客户端时传递 `proxies` 参数。

代理参数的格式与现货 RESTful API 中使用的格式相同。

它由一个字典组成，其中键是代理类型，值是代理 URL：

对于 websockets，代理类型为 `http`。

```python
proxies = { 'http': 'http://1.2.3.4:8080' }
```

你还可以通过在代理 URL 中添加用户名和密码参数来使用代理身份验证：

```python
proxies = { 'http': 'http://username:password@host:port' }
```

```python
# WebSocket API 客户端
from binance.websocket.spot.websocket_api import SpotWebsocketAPIClient

def message_handler(_, message):
    logging.info(message)

proxies = { 'http': '

http://1.2.3.4:8080' }

my_client = SpotWebsocketAPIClient(on_message=message_handler, proxies=proxies, timeout=10)

my_client.ticker(symbol="BNBBUSD", type="FULL")

time.sleep(5)
logging.info("closing ws connection")
my_client.stop()
```

```python
# WebSocket 流客户端
from binance.websocket.spot.websocket_stream import SpotWebsocketStreamClient

def message_handler(_, message):
    logging.info(message)

proxies = { 'http': 'http://1.2.3.4:8080' }

my_client = SpotWebsocketStreamClient(on_message=message_handler, proxies=proxies, timeout=10)

# 订阅单个符号流
my_client.agg_trade(symbol="bnbusdt")
time.sleep(5)
logging.info("closing ws connection")
my_client.stop()
```

### 请求 ID

客户端可以为每个请求分配一个请求 ID。请求 ID 将在响应消息中返回。在库中不是强制性的，如果未提供则生成一个 uuid 格式字符串。

```python
# 客户端提供的 id
my_client.ping_connectivity(id="my_request_id")

# 库将生成一个随机的 uuid 字符串
my_client.ping_connectivity()
```

### 组合流

如果将 `is_combined` 设置为 `True`，将会将 "/stream/" 附加到 `baseURL` 以允许组合流。
`is_combined` 默认为 `False`，将会将 "/ws/"（原始流）附加到 `baseURL`。
更多 websocket 示例可在 `examples` 文件夹中找到。

示例文件 `examples/websocket_api/app_demo.py` 演示了如何一起使用 Websocket API 和 Websocket Stream。

### 连接器 v1 和 v2

```python
from binance.websocket.spot.websocket_client import SpotWebsocketClient as WebsocketClient

def message_handler(message):
    print(message)

ws_client = WebsocketClient()
ws_client.start()

ws_client.mini_ticker(
    symbol='bnbusdt',
    id=1,
    callback=message_handler,
)

# 组合选择的流
ws_client.instant_subscribe(
    stream=['bnbusdt@bookTicker', 'ethusdt@bookTicker'],
    callback=message_handler,
)

ws_client.stop()
```

### 心跳

一旦连接，websocket 服务器每 3 分钟发送一个 ping 帧，并要求在 10 分钟内返回一个 pong 帧。此包会自动处理 pong 响应。

### 测试网络

```python
from binance.websocket.spot.websocket_client import SpotWebsocketClient as WebsocketClient

ws_client = WebsocketClient(stream_url='wss://testnet.binance.vision')
```

### 测试用例

```bash
# 如果包尚未安装
pip install -r requirements/requirements-test.txt

python -m pytest tests/
```

### 限制

不支持期货和普通期权 API：

- `/fapi/*`
- `/dapi/*`
- `/vapi/*`
- 相关的 Websocket 市场和用户数据流

### 贡献

欢迎贡献。
如果你在这个项目中发现了 bug，请打开一个 issue 讨论你想要更改的内容。
如果是 API 的问题，请在 Binance 开发者社区中打开一个主题。

---