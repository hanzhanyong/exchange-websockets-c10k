#!/usr/bin/python
# -*- coding: utf-8 -*-

# Stanislav Lazarov

# A practical example showing how to connect to the public and private channels of Bittrex.

# If you want to test the private channels, you will have to uncomment the
# Private methods block in the main body and define the API_KEY and API_SECRET.

# Requires Python3.5+
# pip install git+https://github.com/slazarov/python-signalr-client.git
import sys
print(sys.path)

from websocket import create_connection
from signalr_aio import Connection
# from .signalr import Connection
from base64 import b64decode
from zlib import decompress, MAX_WBITS
import hashlib
import hmac
import json

global API_KEY, API_SECRET


def process_message(message):
    try:
        deflated_msg = decompress(
            b64decode(message, validate=True), -MAX_WBITS)
    except SyntaxError:
        deflated_msg = decompress(b64decode(message, validate=True))
    return json.loads(deflated_msg.decode())


async def create_signature(api_secret, challenge):
    api_sign = hmac.new(api_secret.encode(), challenge.encode(),
                        hashlib.sha512).hexdigest()
    return api_sign


# Create debug message handler.
async def on_debug(**msg):
    # In case of `queryExchangeState` or `GetAuthContext`
    if 'R' in msg and type(msg['R']) is not bool:
        # For the simplicity of the example I(2) corresponds to `queryExchangeState` and I(3) to `GetAuthContext`
        # Check the main body for more info.
        if msg['I'] == str(2):
            decoded_msg = await process_message(msg['R'])
            print(decoded_msg)
        elif msg['I'] == str(3):
            signature = await create_signature(API_SECRET, msg['R'])
            hub.server.invoke('Authenticate', API_KEY, signature)


# Create error handler
async def on_error(msg):
    print(msg)


# Create hub message handler
async def on_message(msg):
    decoded_msg = await process_message(msg[0])
    print(decoded_msg)


async def on_private(msg):
    decoded_msg = await process_message(msg[0])
    print(decoded_msg)


def main():
    # Create connection
    # Users can optionally pass a session object to the client, e.g a cfscrape session to bypass cloudflare.
    connection = Connection('https://beta.bittrex.com/signalr', session=None)

    # Register hub
    hub = connection.register_hub('c2')

    # Assign debug message handler. It streams unfiltered data, uncomment it to test.
    # connection.received += on_debug

    # Assign error handler
    connection.error += on_error

    # Assign hub message handler
    # Public callbacks
    hub.client.on('uE', on_message)
    hub.client.on('uS', on_message)
    # Private callbacks
    hub.client.on('uB', on_private)
    hub.client.on('uO', on_private)

    # Send a message
    # hub.server.invoke('SubscribeToExchangeDeltas', 'BTC-ETH')  # Invoke 0
    hub.server.invoke('SubscribeToSummaryDeltas')  # Invoke 1
    # hub.server.invoke('queryExchangeState', 'BTC-NEO')  # Invoke 2

    # Private methods
    # API_KEY, API_SECRET = '### API KEY ###', '### API SECRET ###'
    # hub.server.invoke('GetAuthContext', API_KEY) # Invoke 3

    # Start the client
    connection.start()


# def invoke(self, method, *data):
#         message = {
#             'H': self.name,
#             'M': method,
#             'A': data,
#             'I': self.__connection.increment_send_counter()
#         }
#         self.__connection.send(message)

from json import dumps
from urllib.parse import urlparse, urlunparse, urlencode
import requests


class WebSocketParameters:
    def __init__(self, url, hubName):
        self.protocol_version = '1.5'
        self.raw_url = self._clean_url(url)
        self.conn_data = self._get_conn_data(hubName)
        self.session = None
        self.headers = None
        self.socket_conf = None
        self._negotiate()
        self.socket_url = self._get_socket_url()

    @staticmethod
    def _clean_url(url):
        if url[-1] == '/':
            return url[:-1]
        else:
            return url

    @staticmethod
    def _get_conn_data(hub):
        conn_data = dumps([{'name': hub}])
        return conn_data

    @staticmethod
    def _format_url(url, action, query):
        return '{url}/{action}?{query}'.format(
            url=url, action=action, query=query)

    def _negotiate(self):
        if self.session is None:
            self.session = requests.Session()
        query = urlencode({
            'connectionData': self.conn_data,
            'clientProtocol': self.protocol_version,
        })
        url = self._format_url(self.raw_url, 'negotiate', query)
        self.headers = dict(self.session.headers)
        request = self.session.get(url)
        self.headers['Cookie'] = self._get_cookie_str(request.cookies)
        self.socket_conf = request.json()

    @staticmethod
    def _get_cookie_str(request):
        return '; '.join(
            ['%s=%s' % (name, value) for name, value in request.items()])

    def _get_socket_url(self):
        ws_url = self._get_ws_url_from()
        query = urlencode({
            'transport':
            'webSockets',
            'connectionToken':
            self.socket_conf['ConnectionToken'],
            'connectionData':
            self.conn_data,
            'clientProtocol':
            self.socket_conf['ProtocolVersion'],
        })

        return self._format_url(ws_url, 'connect', query)

    def _get_ws_url_from(self):
        parsed = urlparse(self.raw_url)
        scheme = 'wss' if parsed.scheme == 'https' else 'ws'
        url_data = (scheme, parsed.netloc, parsed.path, parsed.params,
                    parsed.query, parsed.fragment)

        return urlunparse(url_data)


def invoke(name, method, *data):
    message = {'H': name, 'M': method, 'A': data, 'I': 1}
    print(message)


if __name__ == "__main__":
    # main()

    hubName = "c2"
    invoke(hubName, "SubscribeToSummaryDeltas")
    while True:
        try:
            socketParameters = WebSocketParameters(
                "https://beta.bittrex.com/signalr", hubName)
            print(socketParameters.socket_url)
            ws = create_connection(socketParameters.socket_url)
            break
        except Exception as ex:
            print('connect ws error,retry...{}'.format(ex))
            exit(0)

    print('connect is started.')

    tradeDict = {
        'H': hubName,
        'M': 'SubscribeToSummaryDeltas',
        'A': (),
        'I': 1
    }
    tradeStr = json.dumps(tradeDict)
    ws.send(tradeStr)
    while (True):
        msg = ws.recv()
        dataJson = json.loads(msg)
        # print(dataJson)
        if "M" in dataJson:
            mdataJson = dataJson["M"]
            if len(mdataJson) > 0:
                # print(mdataJson)
                mdataJson = mdataJson[0]
                if "A" in mdataJson and len(mdataJson["A"]) > 0:
                    mdataJson = mdataJson["A"][0]
                    decoded_msg = process_message(mdataJson)
                    print(decoded_msg)
            # print(mdataJson)
        # decoded_msg = process_message(msg[0])
        # print(decoded_msg)
