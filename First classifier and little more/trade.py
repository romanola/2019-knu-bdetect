import threading
import websocket
import json


def tradeUP(appId, apiKey, asset, duration, price):
    '''
    this functions allows you to invest some money into Rising of any asset's price
    the contract will be opened on Binary.com platform,
    where you should register before and get all the information required

    TRY IT ON DEMO ACCOUNT BEFORE DEPOSIT OR ANY REAL-MONEY TRANSACTIONS

    :param appId: appId created on Binary.com platform
    :param apiKey: your API key
    :param asset: Asset Index you want invest into
    :param duration: duration of your contract in minutes
    :param price: amount you want invest to
    :return: transaction id to track your transaction
    '''
    def on_open(ws):
        ws.send('{"authorize":"<>"}'.replace('<>',apiKey))

    def on_msg(ws, message):
        message = json.loads(message)
        if message['msg_type'] == 'authorize':

            # SORRY FOR THAT
            buy = '{"buy":1,"price":'+str(price)+","+\
                    '"parameters":{'+\
                        '"amount":'+str(price)+','+\
                        '"contract_type":"CALL","basis":"stake",'+\
                        '"currency":"USD","duration":'+str(duration)+','+\
                        '"duration_unit":"m","symbol":"'+asset+'"}'+\
                    '}'
            ws.send(buy)

        if message['msg_type'] == 'buy':
            ws.close()
            return message['buy']['transaction_id']

    ws = websocket.WebSocketApp("wss://ws.binaryws.com/websockets/v3?app_id="+str(appId),
                                on_open=on_open, on_message=on_msg)
    ws.run_forever()

def tradeDOWN(appId, apiKey, asset, duration, price):
    '''
    this functions allows you to invest some money into Rising of any asset's price
    the contract will be opened on Binary.com platform,
    where you should register before and get all the information required

    TRY IT ON DEMO ACCOUNT BEFORE DEPOSIT OR ANY REAL-MONEY TRANSACTIONS

    :param appId: appId created on Binary.com platform
    :param apiKey: your API key
    :param asset: Asset Index you want invest into
    :param duration: duration of your contract in minutes
    :param price: amount you want invest to
    :return: transaction id to track your transaction
    '''
    def on_open(ws):
        ws.send('{"authorize":"<>"}'.replace('<>',apiKey))

    def on_msg(ws, message):
        message = json.loads(message)
        if message['msg_type'] == 'authorize':

            # SORRY FOR THAT
            buy = '{"buy":1,"price":'+str(price)+","+\
                    '"parameters":{'+\
                        '"amount":'+str(price)+','+\
                        '"contract_type":"PUT","basis":"stake",'+\
                        '"currency":"USD","duration":'+str(duration)+','+\
                        '"duration_unit":"m","symbol":"'+asset+'"}'+\
                    '}'
            ws.send(buy)

        if message['msg_type'] == 'buy':
            ws.close()
            return message['buy']['transaction_id']


    ws = websocket.WebSocketApp("wss://ws.binaryws.com/websockets/v3?app_id="+str(appId),
                                on_open=on_open, on_message=on_msg)
    ws.run_forever()

def ticks(asset):
    '''
    Get current tick price as soon as it appears on Binary.com server
    :param asset: Asset Index you want follow to
    :return: None
    '''
    apiUrl = "wss://ws.binaryws.com/websockets/v3?app_id=1089"

    def on_open(ws):
        ws.send('{"ticks":"<>","subscribe":1}'.replace('<>',asset))

    def on_msg(ws, message):
        m = json.loads(message)
        print(m['tick']['quote'])

    ws = websocket.WebSocketApp(apiUrl, on_open=on_open, on_message=on_msg)
    ws.run_forever()
