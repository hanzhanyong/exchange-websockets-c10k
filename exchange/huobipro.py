from .base import wsBase


class huobipro(wsBase):
    """
    Desc: huobipro websocket
    web : https://www.hbg.com/
    api : https://github.com/huobiapi/API_Docs/wiki/WS_request
    """

    def __init__(self):
        super().__init__()

        self.name = "huobipro"  # same to the class name

        self.wsUrl = "wss://api.huobi.pro/ws"  # websocket url
        self.subData = None  # websocket subscribe data

        self.wsConn = None

    def recv(self):
        """
            parse data (kline tickers depth  trade)
        """
        return self.wsConn.recv()

    def sendPing(self, msg=None):
        if not msg:
            msg = ""  # default ping pong
        self.conn.wsConn.send(msg)

    # parse tikers
    def parseTickers(self, tikers):
        return tikers

    # parse Kline
    def parseKline(self, kline):
        return kline

    # parse Depth
    def parseDepth(self, depth):
        return depth

    # parse Trade
    def parseTrade(self, trade):
        return trade
