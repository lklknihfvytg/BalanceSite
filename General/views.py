from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from .models import Coin


import json, pickle, traceback, pprint, datetime, pytz
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from time import sleep
from binance.client import Client
from requests import post, get


IlKey = "HtvBGD17DcPa2EZJ00fqsivTUAPpBVmuWhQyFPrwnkG5lNpEl9m5yrVxCDYNEO5q";
IlSecretKey = "4j2DspxkHwRnk12qWnIVmatnjjUnE2Q4izQ6IlSXXawLbmUcJLmAMZJafl6X5p1U"
PolKey = "MwwZsoaSGsd8u0LJhHaBHABZY3fJtSjriWmWKaEJXTxM0dueV2gm06YgO2RrMoDF";
PolSecretKey = 'gN9NN6PZzfZUqp7DCOxA19f0R8IdMQnnEF675pQOfhEGYVpPlaIDNLv2R9Wuru4O'
d = {'0':'0\ufe0f\u20e3', '1':'1\ufe0f\u20e3', '2':'2\ufe0f\u20e3', '3':'3\ufe0f\u20e3', '4':'4\ufe0f\u20e3', '5':'5\ufe0f\u20e3', '6':'6\ufe0f\u20e3', '7':'7\ufe0f\u20e3', '8':'8\ufe0f\u20e3', '9':'9\ufe0f\u20e3', '!':'\u0001f98'}
tg_testbot_token = '5261233907:AAF5IatEANDCpRdo2hTLkR-1LuGbNRdIe-g'
client1 = Client(IlKey, IlSecretKey)
client2 = Client(PolKey, PolSecretKey)
alertid = 4.49937144E8

#{"symbol": "SOLUSDT", "positionAmt": "5", "entryPrice": "34.17666666667", "markPrice": "35.78081975"
#"unRealizedProfit": "8.02076545", "liquidationPrice": "32.79877443", "leverage": "20", "isolatedMargin": "16.55016530", "notional": "178.90409875", "isolatedWallet": "8.52939985", "updateTime": 1657123201992}


def homepage_views1(request):
    with open('iTrade.json', 'r') as riTrade: fut = json.load(riTrade)
    nj = {}
    nj = {el['symbol'].replace('USDT',""): el for el in fut if abs(float(el['notional'])) > 0.0001}
    return render(request, 'General/home_temp.html', {"nj": json.dumps(nj)})



def homepage_views(request):
    #dost = client2.futures_account_balance()[6]['withdrawAvailable']
    #dost = int(dost[0:dost.find('.')])
    fut = client1.futures_position_information()
    #with open('iTrade.json', 'r') as riTrade: fut = json.load(riTrade)
    with open('iTrade.json', 'w') as wiTrade: json.dump(fut, wiTrade)
    who, new_list = 'i', []

    for el in fut:
        if abs(float(el['notional'])) > 0.0001:
            tic = el['symbol'].replace('USDT','')
            new_list.append(tic)
            try:
                coin = Coin.objects.get(tic=tic)
                coin.liquidation_price = float(el['liquidationPrice'])
                coin.mark_price = float(el['markPrice'])
                coin.entry_price = float(el['entryPrice'])
                coin.unrealized_profit = float(el['unRealizedProfit'])
                coin.notional = float(el['notional'])

                if coin.liquidation_price == 0:
                    num = 999
                else:
                    num = abs((coin.mark_price - coin.liquidation_price) / (coin.liquidation_price/100))
                if num < 2:
                    send('&#127384;<b>' + who + tic + ' Ликвидация</b>&#127384;', alertid, False)
                if abs(coin.position_amt - float(el['positionAmt'])) > 0.00001:
                    if (float(el['positionAmt']) - coin.position_amt) > 0.00001: # стало больше кол-во, чем было
                        send('&#127384;<b>' + who + tic + ' Купился</b>&#127384;', alertid, False)
                    else:
                        send('&#127384;<b>' + who + tic + ' Продался</b>&#127384;', alertid, False)

                coin.position_amt = float(el['positionAmt'])
                coin.save(update_fields=["entry_price", "position_amt", "liquidation_price", "mark_price", "unrealized_profit", "notional"])

            except Coin.DoesNotExist:
                send('&#127384;<b>' + who + tic + ' Купился</b>&#127384;', alertid, False)
                new_coin = Coin(
                    tic = tic,
                    leverage = int(el['leverage']),
                    entry_price = float(el['entryPrice']),
                    position_amt = float(el['positionAmt']),
                    liquidation_price = float(el['liquidationPrice']),
                    mark_price = float(el['markPrice']),
                    unrealized_profit = float(el['unRealizedProfit']),
                    notional = float(el['notional']),
                    warning = 1)
                new_coin.save()

    coins = Coin.objects.all().order_by('-unrealized_profit')
    for coin in coins:
        if coin.tic not in new_list:
            send('&#127384;<b>' + who + coin.tic + ' Продался</b>&#127384;', alertid, False)


    return render(request, 'General/home_temp.html', {"nj": coins})


def create_coin():
    new_coin = Coin(
        tic = 'ADA',
        leverage = 20,
        entry_price = 0.1,
        position_amt = 100,
        liquidation_price = 0.05,
        mark_price = 0.11,
        unrealized_profit = 10,
        notional = 10,
        warning = 37)
    new_post.save()


def test_foo():
    #dost = client2.futures_account_balance()[6]['withdrawAvailable']
    #dost = int(dost[0:dost.find('.')])
    fut = client1.futures_position_information()
    nj = {el["symbol"].replace("USDT", ""): el for el in fut if abs(float(el["notional"])) > 0.01}
    fut = None
    return nj



def futures_update(client, chat_id, tj, s, who):
    dost = client.futures_account_balance()[6]['withdrawAvailable']
    dost = int(dost[0:dost.find('.')])

    fut = client.futures_position_information()
    nj = {}
    for el in fut:
        if abs(float(el['notional'])) > 0.01:
            nj[el['symbol'].replace('USDT','')] = el
    pprint.pprint(nj)
    
    # Создает словарь с ненулевыми монетами, заменяет весь цикл сверху (списковые включения)
    nj2 = {el['symbol'].replace('USDT',''): el for el in fut if abs(float(el['notional'])) > 0.01}
    pprint.pprint(nj2)
    fut = None
    
    f = 0
    # Проверяем не изменилось ли кол-во монет на фьюч
    if len(nj) != len(tj):
        f = 1
        if len(nj) < len(tj):
            delete = []
            for el in tj:
                if not nj.get(el, None):
                    send('&#127384;<b>' + who + el + ' Продался</b>&#127384;', chat_id, False)
                    delete.append(el)
            for el in delete:
                tj.pop(el)
            delete = None
        else: #len(nj) > len(tj)
            for el in nj:
                if not tj.get(el, None):
                    send('&#127384;<b>' + who + el + ' Купился</b>&#127384;', chat_id, False)
                    a = {el: nj[el]}
                    tj.update(a)

    for el in nj:
        if float(nj[el]['liquidationPrice']) == 0:
            num = 999
        else:
            num = abs((float(nj[el]['markPrice']) - float(nj[el]['liquidationPrice'])) / (float(nj[el]['liquidationPrice'])/100))
        if num <2:
            send('&#127384;<b>' + who + el + ' Ликвидация</b>&#127384;', chat_id, False)
        nj[el]['maxNotionalValue'] = num
        if tj[el]['positionAmt'] != nj[el]['positionAmt']:
            if float(tj[el]['positionAmt']) < float(nj[el]['positionAmt']):
                send('&#127384;<b>' + who + el + ' Купился</b>&#127384;', chat_id, False)
            else:
                send('&#127384;<b>' + who + el + ' Продался</b>&#127384;', chat_id, False)

    tj = nj
    nj = None
    t = [['', 'Total ₽', 'Plus ₽', 'Rub', 'Dost', btc, '', 'Plus%', 'Plus$', 'Got$', datetime.datetime.now(tz).time().strftime('%H:%M')],
         ['', '', '', rub, dost, '', '', 'Plus%', '=СУММ(I4:I21)', '=СУММ(J4:J25)', ''],
         ['', 'x', 'Start', 'Got', 'Liquid', 'Value', 'x', 'Plus%', 'Plus$', 'Got$', '']]
    for el in tj:
        markprice = float(tj[el]['markPrice'])
        entryprice = float(tj[el]['entryPrice'])
        t.append([el, tj[el]['leverage'], entryprice, float(tj[el]['positionAmt']),
                  float(tj[el]['liquidationPrice']), markprice, '',
                  (markprice-entryprice)/(entryprice/100),
                  float(tj[el]['unRealizedProfit']), float(tj[el]['notional']),
                  tj[el]['maxNotionalValue']])

    t = insertion_sort(t)
    if f == 1:
        ser.spreadsheets().values().clear(spreadsheetId=sid, range=s+'!A1:K'+str(1+len(t))).execute()
    ser.spreadsheets().values().batchUpdate(
        spreadsheetId=sid,
        body={
        'valueInputOption': 'USER_ENTERED',
        'data': [
            {'range': s+'!A1:K'+str(1+len(t)),
             'majorDimension': 'ROWS',
             'values': t}]}).execute()
    if who == 'i':
        global jiTrade
        jiTrade = tj
    elif who == 'p':
        global jpTrade
        jpTrade = tj
    tj, t = None, None


def send(msg: str, chat_id, silent, parse = 'HTML'): # Отправляет сообщение в тг
    data={
    'method': 'sendMessage',
    'chat_id': chat_id,
    'text': msg,
    'parse_mode': parse,
    'disable_notification': silent
    }
    d = post('https://api.telegram.org/bot' + tg_testbot_token + '/', data).json()
    return d

def emoji(text: str):
    res = ''
    for el in text:
        res += d[el]
    return res

def insertion_sort(arr):
    for i in range(3, len(arr)):
        profit = arr[i][8]
        cursor = arr[i]
        pos = i
        while pos > 3 and arr[pos-1][8] < profit:
            arr[pos] = arr[pos-1]
            pos = pos - 1
        arr[pos] = cursor
    return arr


def create_json(request):
    fut = client1.futures_position_information()
    with open('iTrade.json', 'w') as wiTrade: json.dump(fut, wiTrade)
    return render(request, 'General/home_temp.html', {"nj": "Found"})