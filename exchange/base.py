from enum import Enum, unique

idIndex = 1  # exchange id index


@unique
class wsSubscribeType(Enum):
    '''
    websocket type 
    '''
    WS_TICKERS = 1
    WS_KLINE = 2
    WS_TRADE = 3
    WS_DEPTH = 4


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

        self.session = None
        self.wsConn = None
        self.wsSubscribeType = wsSubscribeType.WS_TICKERS

    # def getConnection(self):
    #     return self.wsConn
    async def connect(self, proxy):
        self.wsConn = await self.session.ws_connect(
            self.wsUrl, autoclose=True, autoping=True, proxy=proxy)
        return self.wsConn

    async def subscribe(self):
        # msg = None
        # if self.wsSubscribeType is wsSubscribeType.WS_TICKERS:
        # await self.send(msg)
        pass

    async def send(self, msg):
        if isinstance(msg, str):
            await self.wsConn.send_str(msg)
        elif isinstance(msg, dict):
            await self.wsConn.send_json(msg)
        else:
            await self.wsConn.send(msg)

    async def close(self):
        await self.wsConn.close()

    async def recv(self):
        return await self.wsConn.recv()

    async def sendPing(self):
        pass

    '''
    parse data
    '''

    def parse(self, data):
        """
            parse data (kline tickers depth  trade)
        """
        pass

    # parse tikers
    async def parseTickers(self, tikers):
        return tikers

    # parse Kline
    async def parseKline(self, kline):
        return kline

    # parse Depth
    async def parseDepth(self, depth):
        return depth

    # parse Trade
    async def parseTrade(self, trade):
        return trade
