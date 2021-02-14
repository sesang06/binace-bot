# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from typing import Any


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

class CandleStickData:
    openTime: int
    open: float
    high: float
    low: float
    close: float
    volumn: float
    closeTime: int
    qouteAssetVolume: float
    numberOfTrades: int
    takerBuyBaseAssetVolume: float
    takerBuyQuoteAssetVolume: float

    def __init__(self, obj: Any) -> None:
        pass




# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    from binance_f import RequestClient
    from binance_f.model import *
    from binance_f.constant.test import *
    from binance_f.base.printobject import *

    request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)

    result = request_client.get_candlestick_data(symbol="BTCUSDT", interval=CandlestickInterval.MIN1,
                                                 startTime=None, endTime=None, limit=10)

    print("======= Kline/Candlestick Data =======")
    PrintMix.print_data(result)
    print("======================================")
    from binance_f import RequestClient
    from binance_f.constant.test import *
    from binance_f.base.printobject import *
    from binance_f.model.constant import *

    request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
    result = request_client.get_balance_v2()
    PrintMix.print_data(result)
from binance_f import RequestClient
from binance_f.model import *
from binance_f.constant.test import *
from binance_f.base.printobject import *
from binance_f.model.candlestickevent import Candlestick
import pandas
from datetime import datetime
import talib
import numpy as np


def printDataAsGraph(df: pandas.DataFrame):
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gridspec
    fig = plt.figure(figsize=(8, 5))
    fig.set_facecolor('w')
    gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1])
    axes = []
    axes.append(plt.subplot(gs[0]))
    axes.append(plt.subplot(gs[1], sharex=axes[0]))
    axes[0].get_xaxis().set_visible(False)
    from mpl_finance import candlestick_ohlc

    x = np.arange(len(df.index))
    ohlc = df[['open', 'high', 'low', 'close']].astype(int).values
    dohlc = np.hstack((np.reshape(x, (-1, 1)), ohlc))

    # 봉차트
    candlestick_ohlc(axes[0], dohlc, width=0.5, colorup='r', colordown='b')

    # 이동평균선 그리기
    # axes[0].plot(index, kospi_df['MA3'], label='MA3', linewidth=0.7)
    # axes[0].plot(index, kospi_df['MA5'], label='MA5', linewidth=0.7)
    axes[0].plot(x, df['ema12'], label='ema12', linewidth=0.7)
    axes[0].plot(x, df['ema26'], label='ema26', linewidth=0.7)

    # 거래량 차트
    print(df['volume'])
    axes[1].bar(x, df['volume'], color='k', width=0.6, align='center')
    import datetime
    _xticks = []
    _xlabels = []
    _wd_prev = 0
    for _x, d in zip(x, df.openTime.values):
        weekday = pandas.to_datetime(d).weekday()
        if weekday <= _wd_prev:
            _xticks.append(_x)
            _xlabels.append(pandas.to_datetime(d).strftime('%m/%d'))
        _wd_prev = weekday
    axes[1].set_xticks(_xticks)
    axes[1].set_xticklabels(_xlabels, rotation=45, minor=False)
    plt.tight_layout()
    plt.show()
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

from backtesting.test import SMA, GOOG
from backtesting import Strategy, Backtest
from backtesting.lib import resample_apply
import pandas as pd


def SMA(array, n):
    """Simple moving average"""
    return pd.Series(array).rolling(n).mean()


def RSI(array, n):
    """Relative strength index"""
    # Approximate; good enough
    gain = pd.Series(array).diff()
    loss = gain.copy()
    gain[gain < 0] = 0
    loss[loss > 0] = 0
    rs = gain.ewm(n).mean() / loss.abs().ewm(n).mean()
    return 100 - 100 / (1 + rs)
class SmaCross(Strategy):
    def init(self):
        price = self.data.Close
        self.ma1 = self.I(SMA, price, 10)
        self.ma2 = self.I(SMA, price, 20)

    def next(self):
        if crossover(self.ma1, self.ma2):
            # if self.position.is_short:
            #     self.()
            self.buy()
        elif crossover(self.ma2, self.ma1):
            # if self.position.is_long:
            #     self.position.close()
            self.sell()

def executeBacktest(data: pandas.DataFrame):
    data = data.set_index('openTime')
    data['Open'] = data['open']
    data['High'] = data['high']
    data['Low'] = data['low']
    data['Close'] = data['close']
    data['Volume'] = data['volume']
    bt = Backtest(data, SmaCross,
                  cash=100000000000, commission=.002, exclusive_orders=True)

    print(bt.run())
    bt.plot()
def printCandle():
    request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)

    result: [Candlestick] = request_client.get_candlestick_data(symbol="BTCUSDT", interval=CandlestickInterval.MIN1,
                                      startTime=None, endTime=None, limit=500)
    # np = numpy.vectorize(result)
    # print(np)
    # df = pandas.DataFrame(data=np, columns=['startTime', ])
    # print(df)
    df = pandas.DataFrame([vars(s) for s in result])
    print(df)
    print(df['openTime'])
    df['openTime'] = [datetime.fromtimestamp(x//1000.0) for x in df['openTime']]
    df['closeTime'] = [datetime.fromtimestamp(x // 1000.0) for x in df['closeTime']]
    df['close'] = df['close'].astype(float)
    df['open'] = df['open'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    print(df)

    close = np.array(df['close'])
    print(close)
    df['sma5'] = talib.SMA(close, 5)
    df['sma20'] = talib.SMA(close, 20)
    df['sma120'] = talib.SMA(close, 120)

    df['ema12'] = talib.EMA(close, 12)
    df['ema26'] = talib.EMA(close, 26)
    df['rsi14'] = talib.RSI(close, 14)

    macd, macdsignal, macdhist = talib.MACD(close, 12, 26, 9)

    df['macd'] = macd
    print(df)
    df.to_excel("output.xlsx")

    printDataAsGraph(df.tail(90))
    executeBacktest(df)


if __name__ == '__main__':
    printCandle()


def cal_current_price_short(
        buy_price: float,
        current_price: float,
        leverage: int,
        commission_percent: float) -> float :
    """숏 포지션을 했을 때, 현재 매도했을 때 자산의 가격을 계산한다..

    Args:
        buy_price: 구매했을 때 자산의 시세
        current_price: 현재 자산의 시세
        leverage: 1배~125배의 가격
        commission_percent: 거래소에 지불하는 수수료
    Returns:
        현재 거래를 종료했을 때 자산의 가
    """


    liquidation_price: float = buy_price

    pass

def cal_current_price_long(
        buy_price: float,
        current_price: float,
        leverage: int,
        commission_percent: float) -> float :
    """ 포지션을 했을 때, 현재 매도했을 때 자산의 가격을 계산한다.

    Args:
        buy_price: 구매했을 때 자산의 시세
        current_price: 현재 자산의 시세
        leverage: 1배~125배의 가격
        commission_percent: 거래소에 지불하는 수수료
    Returns:
        현재 거래를 종료했을 때 자산의 가
    """


    liquidation_price: float = buy_price
    pass

class Trade:
    """
    현재 등록중인 거래
    """
    """
        구매 당시 코인 가격
    """
    initial_coin_price: float
    """
        구매 당시 구입한 재화
    """
    initial_dollars: float
    """
        포지션
    """
    is_long: bool


    """
        청산 여부
    """
    def is_closed(self) -> bool:
        return False

class BackTest:
    """
    백테스트 과정
    Args:
        initial_budget: 최초 투자 잔고
        chart: 캔들스틱
        current_trades: 현재 종료되지 않은 거래들
    """

    initial_budget: float

    chart: pandas.DataFrame
    current_trades: [Trade]


    """
    """
    def clear_turn(self, turn: int):
        current_price = chart[turn]
        for trade in current_price:
            if trade.is_closed():
                self.close_trade(trade)

        return
                


    def close_trade(self, trade: Trade):
        pass