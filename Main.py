import sys
import aiohttp
import asyncio
# from websocket import create_connection
import gzip
import json
# import time
import hashlib

PROXY = "http://127.0.0.1:1087"
URL = "wss://api.huobi.pro/ws"


wsList = []


async def push_ws(ws):
    wsList.append(ws)
    print("ws connection count {}".format(len(wsList)))


async def pob_ws(ws):
    wsList.pop(ws)
    print("ws connection count {}".format(len(wsList)))


async def dispatch(sub_data, ws):
    """
    功能:
        接收 ws 消息
    """
    await push_ws(ws)
    
    hash = hashlib.md5()
    hash.update(str(sub_data).encode('utf-8'))
    print(hash.hexdigest())
    wsId = hash.hexdigest()
    if isinstance(sub_data, str):
        await ws.send_str(sub_data)
    elif isinstance(sub_data, dict):
        await ws.send_json(sub_data)
    else:
        await ws.send(sub_data)
    while True:
        try:
            msg = await ws.receive()
        except Exception as e:
            print(e)
            # await ws.close()
            # raise WsReceiveException(f'处理ws receive 错误: {e}')
        if msg.type == aiohttp.WSMsgType.TEXT:
            # 普通字符串
            try:
                # await self.parse(msg.data, ws)
                # print(msg.data)
                print(msg.data)

            except Exception as e:
                await ws.close()
                # raise WsExchangeException(f'处理交易所数据内部错误: {e}')
                print(e)
                break
        elif msg.type == aiohttp.WSMsgType.BINARY:
            # bytes 类型
            try:
                # await self.parse(msg.data, ws)
                result = gzip.decompress(msg.data).decode('utf-8')
                if result[:7] == '{"ping"':
                    ts = result[8:21]
                    pong = '{"pong":' + ts + '}'
                    # print(pong)
                    await ws.send_str(pong)
                    # ws.send(tradeStr)
                # else:
                #     print(wsId, result)
            except Exception as e:
                await ws.close()
                # raise WsExchangeException(f'处理交易所数据内部错误: {e}')
                print(e)
                break
        elif msg.type == aiohttp.WSMsgType.PING:
            print('Ping received')
        elif msg.type == aiohttp.WSMsgType.PONG:
            print('Pong received')
        else:
            if msg.type == aiohttp.WSMsgType.CLOSE:
                print("CLOSE")
                await ws.close()
                # raise WsCloseException(
                #     f'{self.ex.exchange_id}:{self.url} 参数:{self.sub_data} 服务器请求断开 !'
                # )
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print("ERROR")
                await ws.close()
                # raise WsBaseException(
                #     'Error during receive %s' % ws.exception())
            elif msg.type == aiohttp.WSMsgType.CLOSED:
                print("CLOSED")
                await ws.close()
                # raise WsClosedException(
                #     f'{self.ex.exchange_id}:{self.url} 参数:{self.sub_data} websocket 断开重连!'
                # )
                # logger.error(f'{ex.exchange_id}:{url} 参数:{sub_data} websocket 断开重连!')
            break

    await pob_ws(ws)


async def connect_ws(session, url, sub_data, proxy):
    async with session.ws_connect(
            url, autoclose=True, autoping=True, proxy=proxy) as ws:
        if not ws:
            await ws.close()
            print(f'{url} 参数:{sub_data} 没有可用websocket代理!')
            return
        try:
            # 收发信息
            await dispatch(sub_data, ws)
            # await self.close(ws)
            await ws.close()
        # 其他错误
        except Exception as e:
            print(f'{url} 参数:{sub_data} 处理ws 信息其他错误: {e}')
            await ws.close(ws)
            return


if __name__ == '__main__':
    print(sys.argv)

    symbols_list = [
            '18C/BTC', '18C/ETH', 'AAC/BTC', 'AAC/ETH', 'ABT/BTC', 'ABT/ETH',
            'ACT/BTC', 'ACT/ETH', 'ACT/USDT', 'ADA/BTC', 'ADA/ETH', 'ADA/USDT',
            'ADX/BTC', 'ADX/ETH', 'AE/BTC', 'AE/ETH', 'AIDOC/BTC', 'AIDOC/ETH',
            'APPC/BTC', 'APPC/ETH', 'ARDR/BTC', 'ARDR/ETH', 'AST/BTC',
            'AST/ETH', 'BAT/BTC', 'BAT/ETH', 'BCD/BTC', 'BCH/BTC', 'BCH/HT',
            'BCH/USDT', 'BCV/BTC', 'BCV/ETH', 'BCX/BTC', 'BFT/BTC', 'BFT/ETH',
            'BIFI/BTC', 'BIX/BTC', 'BIX/ETH', 'BIX/USDT', 'BKBT/BTC',
            'BKBT/ETH', 'BLZ/BTC', 'BLZ/ETH', 'BOX/BTC', 'BOX/ETH', 'BTC/HUSD',
            'BTC/USDT', 'BTG/BTC', 'BTM/BTC', 'BTM/ETH', 'BTM/USDT', 'BTS/BTC',
            'BTS/ETH', 'BTS/USDT', 'BUT/BTC', 'BUT/ETH', 'CDC/BTC', 'CDC/ETH',
            'CHAT/BTC', 'CHAT/ETH', 'CMT/BTC', 'CMT/ETH', 'CMT/USDT',
            'CNN/BTC', 'CNN/ETH', 'CTXC/BTC', 'CTXC/ETH', 'CTXC/USDT',
            'CVC/BTC', 'CVC/ETH', 'CVC/USDT', 'CVCOIN/BTC', 'CVCOIN/ETH',
            'DAC/BTC', 'DAC/ETH', 'DASH/BTC', 'DASH/HT', 'DASH/USDT',
            'DAT/BTC', 'DAT/ETH', 'DATX/BTC', 'DATX/ETH', 'DBC/BTC', 'DBC/ETH',
            'DCR/BTC', 'DCR/ETH', 'DGB/BTC', 'DGB/ETH', 'DGD/BTC', 'DGD/ETH',
            'DTA/BTC', 'DTA/ETH', 'DTA/USDT', 'EDU/BTC', 'EDU/ETH', 'EGCC/BTC',
            'EGCC/ETH', 'EKO/BTC', 'EKO/ETH', 'EKT/BTC', 'EKT/ETH', 'ELA/BTC',
            'ELA/ETH', 'ELA/USDT', 'ELF/BTC', 'ELF/ETH', 'ELF/USDT', 'ENG/BTC',
            'ENG/ETH', 'EOS/BTC', 'EOS/ETH', 'EOS/HT', 'EOS/HUSD', 'EOS/USDT',
            'ETC/BTC', 'ETC/HT', 'ETC/USDT', 'ETH/BTC', 'ETH/HUSD', 'ETH/USDT',
            'EVX/BTC', 'EVX/ETH', 'FAIR/BTC', 'FAIR/ETH', 'FTI/BTC', 'FTI/ETH',
            'GAS/BTC', 'GAS/ETH', 'GET/BTC', 'GET/ETH', 'GNT/BTC', 'GNT/ETH',
            'GNT/USDT', 'GNX/BTC', 'GNX/ETH', 'GRS/BTC', 'GRS/ETH', 'GSC/BTC',
            'GSC/ETH', 'GTC/BTC', 'GTC/ETH', 'GVE/BTC', 'GVE/ETH', 'GXS/BTC',
            'GXS/ETH', 'HB10/USDT', 'HC/BTC', 'HC/ETH', 'HC/USDT', 'HIT/BTC',
            'HIT/ETH', 'HOT/BTC', 'HOT/ETH', 'HPT/BTC', 'HPT/HT', 'HPT/USDT',
            'HT/BTC', 'HT/ETH', 'HT/USDT', 'ICX/BTC', 'ICX/ETH', 'IDT/BTC',
            'IDT/ETH', 'IIC/BTC', 'IIC/ETH', 'IOST/BTC', 'IOST/ETH', 'IOST/HT',
            'IOST/USDT', 'IOTA/BTC', 'IOTA/ETH', 'IOTA/USDT', 'ITC/BTC',
            'ITC/ETH', 'ITC/USDT', 'KAN/BTC', 'KAN/ETH', 'KCASH/BTC',
            'KCASH/ETH', 'KCASH/HT', 'KNC/BTC', 'KNC/ETH', 'LBA/BTC',
            'LBA/ETH', 'LET/BTC', 'LET/ETH', 'LET/USDT', 'LINK/BTC',
            'LINK/ETH', 'LSK/BTC', 'LSK/ETH', 'LTC/BTC', 'LTC/HT', 'LTC/USDT',
            'LUN/BTC', 'LUN/ETH', 'LXT/BTC', 'LXT/ETH', 'LYM/BTC', 'LYM/ETH',
            'MAN/BTC', 'MAN/ETH', 'MANA/BTC', 'MANA/ETH', 'MCO/BTC', 'MCO/ETH',
            'MDS/BTC', 'MDS/ETH', 'MDS/USDT', 'MEET/BTC', 'MEET/ETH',
            'MEX/BTC', 'MEX/ETH', 'MT/BTC', 'MT/ETH', 'MT/HT', 'MTL/BTC',
            'MTN/BTC', 'MTN/ETH', 'MTX/BTC', 'MTX/ETH', 'MUSK/BTC', 'MUSK/ETH',
            'NAS/BTC', 'NAS/ETH', 'NAS/USDT', 'NCASH/BTC', 'NCASH/ETH',
            'NCC/BTC', 'NCC/ETH', 'NEO/BTC', 'NEO/USDT', 'OCN/BTC', 'OCN/ETH',
            'OCN/USDT', 'OMG/BTC', 'OMG/ETH', 'OMG/USDT', 'ONT/BTC', 'ONT/ETH',
            'ONT/USDT', 'OST/BTC', 'OST/ETH', 'PAI/BTC', 'PAI/ETH', 'PAI/USDT',
            'PAY/BTC', 'PAY/ETH', 'PC/BTC', 'PC/ETH', 'PHX/BTC', 'PNT/BTC',
            'PNT/ETH', 'POLY/BTC', 'POLY/ETH', 'PORTAL/BTC', 'PORTAL/ETH',
            'POWR/BTC', 'POWR/ETH', 'PROPY/BTC', 'PROPY/ETH', 'QASH/BTC',
            'QASH/ETH', 'QSP/BTC', 'QSP/ETH', 'QTUM/BTC', 'QTUM/ETH',
            'QTUM/USDT', 'QUN/BTC', 'QUN/ETH', 'RCCC/BTC', 'RCCC/ETH',
            'RCN/BTC', 'RCN/ETH', 'RDN/BTC', 'RDN/ETH', 'REN/BTC', 'REN/ETH',
            'REQ/BTC', 'REQ/ETH', 'RTE/BTC', 'RTE/ETH', 'RUFF/BTC', 'RUFF/ETH',
            'RUFF/USDT', 'SALT/BTC', 'SALT/ETH', 'SBTC/BTC', 'SEELE/BTC',
            'SEELE/ETH', 'SHE/BTC', 'SHE/ETH', 'SMT/BTC', 'SMT/ETH',
            'SMT/USDT', 'SNC/BTC', 'SNC/ETH', 'SNT/BTC', 'SNT/USDT', 'SOC/BTC',
            'SOC/ETH', 'SOC/USDT', 'SRN/BTC', 'SRN/ETH', 'SSP/BTC', 'SSP/ETH',
            'STEEM/BTC', 'STEEM/ETH', 'STEEM/USDT', 'STK/BTC', 'STK/ETH',
            'STORJ/BTC', 'STORJ/USDT', 'SWFTC/BTC', 'SWFTC/ETH', 'THETA/BTC',
            'THETA/ETH', 'THETA/USDT', 'TNB/BTC', 'TNB/ETH', 'TNT/BTC',
            'TNT/ETH', 'TOPC/BTC', 'TOPC/ETH', 'TOS/BTC', 'TOS/ETH',
            'TRIO/BTC', 'TRIO/ETH', 'TRX/BTC', 'TRX/ETH', 'TRX/USDT', 'UC/BTC',
            'UC/ETH', 'UIP/BTC', 'UIP/ETH', 'USDT/HUSD', 'UTK/BTC', 'UTK/ETH',
            'UUU/BTC', 'UUU/ETH', 'VET/BTC', 'VET/ETH', 'VET/USDT', 'WAN/BTC',
            'WAN/ETH', 'WAVES/BTC', 'WAVES/ETH', 'WAX/BTC', 'WAX/ETH',
            'WICC/BTC', 'WICC/ETH', 'WICC/USDT', 'WPR/BTC', 'WPR/ETH',
            'WTC/BTC', 'WTC/ETH', 'XEM/BTC', 'XEM/USDT', 'XLM/BTC', 'XLM/ETH',
            'XLM/USDT', 'XMR/BTC', 'XMR/ETH', 'XMX/BTC', 'XMX/ETH', 'XRP/BTC',
            'XRP/HT', 'XRP/USDT', 'XVG/BTC', 'XVG/ETH', 'XZC/BTC', 'XZC/ETH',
            'YCC/BTC', 'YCC/ETH', 'YEE/BTC', 'YEE/ETH', 'ZEC/BTC', 'ZEC/USDT',
            'ZIL/BTC', 'ZIL/ETH', 'ZIL/USDT', 'ZJLT/BTC', 'ZJLT/ETH',
            'ZLA/BTC', 'ZLA/ETH', 'ZRX/BTC', 'ZRX/ETH'
        ]

    symbol_list_map = [s.replace('/', '').lower() for s in symbols_list]
    kline_subs = [
        json.dumps({
            "sub": "market.{}.kline.1min".format(symbol),
            "id": "ihold2019{}".format(symbol)
            })
        for symbol in symbol_list_map
    ]
    loop = asyncio.get_event_loop()

    conn = aiohttp.TCPConnector(limit=0)  # 不限制连接池数量 默认100
    session = aiohttp.ClientSession(connector=conn)
    tasks = [
        connect_ws(session, URL, sub_data, PROXY) for sub_data in kline_subs
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()