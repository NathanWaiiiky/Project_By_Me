from binance.client import Client
from binance.enums import *
import pandas as pd
import ta
from math import *

pairSymbol = 'BTCBUSD'
fiatSymbol = 'BUSD'
cryptoSymbol = 'BTC'

binance_api_key = ''
binance_api_secret = ''

client = Client(api_key=binance_api_key, api_secret=binance_api_secret)

def getHistorical(symbole):
    klinesT = client.get_historical_klines(symbole, Client.KLINE_INTERVAL_15MINUTE, "1 june 2022")
    dataT = pd.DataFrame(klinesT,
                         columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av',
                                  'trades', 'tb_base_av', 'tb_quote_av', 'ignore'])
    dataT['close'] = pd.to_numeric(dataT['close'])
    dataT['high'] = pd.to_numeric(dataT['high'])
    dataT['low'] = pd.to_numeric(dataT['low'])
    dataT['open'] = pd.to_numeric(dataT['open'])
    dataT['volume'] = pd.to_numeric(dataT['volume'])
    dataT.drop(dataT.columns.difference(['open', 'high', 'low', 'close', 'volume']), 1, inplace=True)
    return dataT


def truncate(n, decimals=0):
    r = floor(float(n) * 10 ** decimals) / 10 ** decimals
    return str(r)


df = getHistorical(pairSymbol)
df['SMA200'] = ta.trend.sma_indicator(df['close'], 200)
df['SMA600'] = ta.trend.sma_indicator(df['close'], 600)
df = getHistorical(pairSymbol)
actualPrice = df.iloc[-1]
cryptoAmount = float(client.get_asset_balance(asset=cryptoSymbol)['free'])
fiatAmount = float(client.get_asset_balance(asset=fiatSymbol)['free'])
minToken = 0.0001


def buyCondition(row):
    if row['SMA200'] > row['SMA600']:
        return True
    else:
        return False
def sellCondition(row):
    if row['SMA200'] < row['SMA600']:
        return True
    else:
        return False

if buyCondition(actualPrice) and fiatAmount > 5:
    if float(fiatAmount) > 10:
        quantityBuy = truncate((float(fiatAmount) / actualPrice['close']), 3)
        buyOrder = client.order_market_buy(
            symbol=pairSymbol,
            quantity=quantityBuy)
        print("BUY", buyOrder)
    else:
        print('Nothing')
elif sellCondition(actualPrice) and cryptoAmount > minToken:
    if float(cryptoAmount) > minToken:
        sellOrder = client.order_market_sell(
            symbol=pairSymbol,
            quantity=truncate(cryptoAmount, 4))
        print("SELL", sellOrder)
    else:
        print('Nothing')
else:
    print('Nothing')

