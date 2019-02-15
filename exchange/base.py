idIndex = 1  # exchange id index


class wsBase:
    """
    Desc:
        1. define websocket url and subscribe data
        2. Asynchronous and synchronization support
    """

    # __slots__ = ('id', 'name', 'wsUrl', 'subData')

    def __init__(self):
        global idIndex
        self.id = idIndex
        idIndex += 1

        self.name = ""  # same to the class name

        self.wsUrl = ""  # websocket url
        self.subData = None  # websocket subscribe data

        self.wsConn = None

    # def getConnection(self):
    #     return self.wsConn

    def connect(self, ws, subData=[]):
        self.wsConn = ws
        self.subData = subData

        if isinstance(self.subData, list):
            for sub in self.subData:
                self.wsConn.send(sub)
        elif isinstance(self.subData, str):
            self.conn.send(self.subData)
        else:
            print(f"{self.name}_{self.id}  subdata error")

    def recv(self):
        """
            parse data (kline tickers depth  trade)
        """
        return self.wsConn.recv()

    def send(self, msg):
        self.wsConn.send(msg)

    def sendPing(self, msg=None):
        if not msg:
            msg = ""  # default ping pong
        self.conn.wsConn.send(msg)

    # def parse(self, data):
    #     return data

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
