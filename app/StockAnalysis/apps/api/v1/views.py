import datetime
import time

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import yfinance as yf
import matplotlib.pyplot as plt
import yahoo_fin.stock_info as si
from .data.stocks_list import full_stock_list
import pandas as pd
import numpy as np


def get_stock_data(symbol, start_date, end_date):
    try:
        stock_data = yf.download(symbol, start=start_date, end=end_date)
        print(stock_data,"stock_data")
        return stock_data['Close']
    except Exception as e:
        print(e)
        return e, None


def get_stock_info(symbol):
    try:
        stock_info = yf.Ticker(symbol)
        print(stock_info,"stock_info")
        return stock_info
    except Exception as e:
        print(e)
        return e


def get_req_data_keys():
    r_keys = ['sector', 'fullTimeEmployees', 'auditRisk', 'boardRisk', 'compensationRisk',
              'shareHolderRightsRisk', 'overallRisk', 'priceHint', 'previousClose', 'open',
              'dayLow',
              'dayHigh', 'regularMarketPreviousClose', 'regularMarketOpen', 'regularMarketDayLow',
              'regularMarketDayHigh', 'dividendRate', 'dividendYield', 'exDividendDate',
              'payoutRatio',
              'fiveYearAvgDividendYield', 'beta', 'trailingPE', 'forwardPE', 'volume',
              'regularMarketVolume', 'averageVolume', 'averageVolume10days',
              'averageDailyVolume10Day',
              'marketCap', 'fiftyTwoWeekLow', 'fiftyTwoWeekHigh', 'priceToSalesTrailing12Months',
              'fiftyDayAverage', 'twoHundredDayAverage', 'trailingAnnualDividendRate',
              'trailingAnnualDividendYield', 'currency', 'enterpriseValue', 'profitMargins',
              'floatShares', 'sharesOutstanding', 'heldPercentInsiders', 'heldPercentInstitutions',
              'impliedSharesOutstanding', 'bookValue', 'priceToBook', 'earningsQuarterlyGrowth',
              'netIncomeToCommon', 'trailingEps', 'forwardEps', 'lastSplitFactor', 'lastSplitDate',
              'enterpriseToRevenue', 'enterpriseToEbitda', '52WeekChange', 'SandP52WeekChange',
              'lastDividendValue', 'longName', 'firstTradeDateEpochUtc', 'gmtOffSetMilliseconds',
              'targetHighPrice', 'targetLowPrice', 'targetMeanPrice',
              'targetMedianPrice', 'recommendationMean', 'recommendationKey',
              'numberOfAnalystOpinions',
              'totalCash', 'totalCashPerShare', 'ebitda', 'totalDebt', 'quickRatio', 'currentRatio',
              'totalRevenue', 'debtToEquity', 'revenuePerShare', 'returnOnAssets', 'returnOnEquity',
              'grossProfits', 'earningsGrowth', 'revenueGrowth', 'grossMargins', 'ebitdaMargins',
              'operatingMargins']
    return r_keys



def get_stock_list():
    stock_list = si.tickers_nifty50()
    return stock_list


def calculate_rsi(data, period=14):
    # Calculate price changes
    delta = data.diff(1)

    # Calculate gains (positive changes) and losses (negative changes)
    gains = delta.where(delta > 0, 0)
    losses = -delta.where(delta < 0, 0)

    # Calculate average gains and losses over the specified period
    avg_gain = gains.rolling(window=period, min_periods=1).mean()
    avg_loss = losses.rolling(window=period, min_periods=1).mean()

    # Calculate the relative strength (RS)
    rs = avg_gain / avg_loss

    # Calculate the relative strength index (RSI)
    rsi = 100 - (100 / (1 + rs))

    return rsi


class MACross(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._trade_data = {}

    def get(self, request):
        try:
            params = request.query_params
            symbol = params.get("Stock")
            short_window = int(params.get("ShortWindow"))
            long_window = int(params.get("LongWindow"))
            start_date = params.get("StartDate")
            end_date = params.get("EndDate", datetime.date.today())
            plot = params.get("Plot", False)
            detail = params.get("Detail", False) if params.get("Detail", False) == "True" else False
            self.plot_moving_average_crossover(symbol, short_window, long_window, start_date, end_date, plot, detail)
        except Exception as e:
            print(e, "error in main func.")
        while self._trade_data is None:
            time.sleep(1)
        response = {"code": 200, "status": "success", "data": self._trade_data}
        return Response(response)

    def plot_moving_average_crossover(self, symbol, short_window, long_window, start_date, end_date, plot, detail):
        # Get stock data
        try:
            # get_stock_symbol()
            try:
                stock_data = get_stock_data(symbol, start_date, end_date)
                print(stock_data)
                stock_data.dropna()
                stock_info = get_stock_info(symbol)
                r_data = {}
                if stock_info:
                    if detail:
                        r_keys = get_req_data_keys()
                        for key in r_keys:
                            r_data.setdefault(key, stock_info.info.get(key))
                r_data.setdefault("currentPrice", stock_info.info.get("currentPrice"))
                self._trade_data.setdefault(symbol, {}).update(r_data)
                # Calculate short and long-term moving averages
                # Example usage:
                # Assuming you have a DataFrame 'df' with a column 'Close' representing closing prices
                # and you want to calculate RSI for a 14-day period
                # Add RSI column to the DataFrame
                rsi = calculate_rsi(stock_data, period=14)
                rsi=rsi.dropna()
                print(rsi)
                short_rolling = stock_data.rolling(window=short_window).mean()
                long_rolling = stock_data.rolling(window=long_window).mean()
                print(short_rolling,"qwert")
                print(long_rolling,"wqert")

                # Plotting
                if plot:
                    plt.subplot(1, 6, 6)
                    plt.figure(figsize=(100, 8))
                    plt.title(f'{symbol} Moving Average Crossover')
                    plt.plot(stock_data, label='Close Price', color='blue')
                    plt.plot(short_rolling, label=f'{short_window}-day SMA', color='orange')
                    plt.plot(long_rolling, label=f'{long_window}-day SMA', color='green')
                    manager = plt.get_current_fig_manager()
                    manager.full_screen_toggle()
                # Plot Buy and Sell signals
                buy_signal = short_rolling[short_rolling > long_rolling]
                sell_signal = short_rolling[short_rolling <= long_rolling]
                print(buy_signal,"buyyyyy")
                print(sell_signal,"erty")
                # Calculate RSI
                rsi_data = {"date": rsi.index[-1], "price": rsi.values[-1]} if len(
                    rsi.index) > 0 else {}
                self._trade_data.setdefault(symbol, {}).update({
                    "rsi": rsi_data})
                buy_data = {"date": buy_signal.index[-1], "price": buy_signal.values[-1]} if len(
                    buy_signal.index) > 0 else {}
                self._trade_data.setdefault(symbol, {}).update({
                    "buy_signal": buy_data})
                sell_data = {"date": sell_signal.index[-1], "price": sell_signal.values[-1]} if len(
                    sell_signal.index) > 0 else {}
                self._trade_data.setdefault(symbol, {}).update({"sell_signal": sell_data})
                if plot:
                    plt.scatter(buy_signal.index, buy_signal, label='Buy Signal', marker='^', color='green')
                    plt.scatter(sell_signal.index, sell_signal, label='Sell Signal', marker='v', color='red')
                    plt.xlabel('Date')
                    plt.ylabel('Close Price')
                    plt.legend()
                    plt.tight_layout()
                    plt.show()
            except Exception as e:
                self._trade_data[symbol] = {"error": str(e)}

        except Exception as e:
            self._trade_data = str(e)


class MACrossMulti(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._trade_data = {}

    def get(self, request):
        try:
            params = request.query_params
            short_window = int(params.get("ShortWindow"))
            long_window = int(params.get("LongWindow"))
            start_date = params.get("StartDate")
            end_date = params.get("EndDate", datetime.date.today())
            detail = params.get("Detail", False) if params.get("Detail", False) == "True" else False
            self.plot_moving_average_crossover(short_window, long_window, start_date, end_date, detail)
        except Exception as e:
            print(e, "error in main func.")
        while self._trade_data is None:
            time.sleep(1)
        response = {"code": 200, "status": "success", "data": self._trade_data}
        #print(response)
        return Response(response)

    def plot_moving_average_crossover(self, short_window, long_window, start_date, end_date, detail):
        # Get stock data
        try:
            stock_err = []
            stock_list = full_stock_list
            for stock in stock_list:
                try:
                    stock_data = get_stock_data(stock, start_date, end_date)
                    print(stock_data,"5700000000")
                    stock_data.dropna()
                    stock_info = get_stock_info(stock)
                    r_data = {}
                    if stock_info:
                        if detail:
                            r_keys = get_req_data_keys()
                            for key in r_keys:
                                r_data.setdefault(key, stock_info.info.get(key))
                    r_data.setdefault("current_price", stock_info.info.get("currentPrice"))
                    self._trade_data.setdefault(stock, {}).update(r_data)
                    rsi = calculate_rsi(stock_data, period=14)
                    rsi = rsi.dropna()
                    short_rolling = stock_data.rolling(window=short_window).mean()
                    long_rolling = stock_data.rolling(window=long_window).mean()

                    # Plot Buy and Sell signals
                    buy_signal = short_rolling[short_rolling > long_rolling]
                    sell_signal = short_rolling[short_rolling <= long_rolling]
                    # Calculate RSI
                    rsi_data = {"date": rsi.index[-1], "price": rsi.values[-1]} if len(
                        rsi.index) > 0 else {}
                    self._trade_data.setdefault(stock, {}).update({
                        "rsi": rsi_data})
                    buy_data = {"date": buy_signal.index[-1], "price": buy_signal.values[-1]} if len(
                        buy_signal.index) > 0 else {}
                    if buy_data.get("price"):
                        price_diff = ((buy_signal.values[-1] - stock_info.info.get("currentPrice")) / buy_signal.values[
                            -1]) * 100
                        self._trade_data.setdefault(stock, {}).update({
                            "buy_price_diff": price_diff})
                    self._trade_data.setdefault(stock, {}).update({
                        "buy_signal": buy_data})
                    sell_data = {"date": sell_signal.index[-1], "price": sell_signal.values[-1]} if len(
                        sell_signal.index) > 0 else {}
                    self._trade_data.setdefault(stock, {}).update({"sell_signal": sell_data})
                except Exception as e:
                    stock_err.append(stock)
                    self._trade_data[stock] = {"error": str(e)}
            print(stock_err)
        except Exception as e:
            self._trade_data = str(e)


class MACrossFilter(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._trade_data = {}

    def get(self, request):
        try:
            params = request.query_params
            short_window = int(params.get("ShortWindow"))
            long_window = int(params.get("LongWindow"))
            start_date = params.get("StartDate")
            end_date = params.get("EndDate", datetime.date.today())
            detail = params.get("Detail", False) if params.get("Detail", False) == "True" else False
            self.plot_moving_average_crossover(short_window, long_window, start_date, end_date, detail)
        except Exception as e:
            print(e, "error in main func.")
        while self._trade_data is None:
            time.sleep(1)
        response = {"code": 200, "status": "success", "data": self._trade_data}
        return Response(response)

    def plot_moving_average_crossover(self, short_window, long_window, start_date, end_date, detail):
        # Get stock data
        try:
            stock_list = get_stock_list()
            for stock in stock_list:
                try:
                    stock_data = get_stock_data(stock, start_date, end_date)
                    stock_info = get_stock_info(stock)
                    r_data = {}
                    if stock_info:
                        if detail:
                            r_keys = get_req_data_keys()
                            for key in r_keys:
                                r_data.setdefault(key, stock_info.info.get(key))
                    r_data.setdefault("currentPrice", stock_info.info.get("currentPrice"))
                    self._trade_data.setdefault(stock, {}).update(r_data)
                    short_rolling = stock_data.rolling(window=short_window).mean()
                    long_rolling = stock_data.rolling(window=long_window).mean()
                    # Calculate RSI
                    rsi = calculate_rsi(stock_data, period=14)
                    rsi = rsi.dropna()
                    # Plot Buy and Sell signals
                    buy_signal = short_rolling[short_rolling > long_rolling]
                    sell_signal = short_rolling[short_rolling <= long_rolling]
                    rsi_data = {"date": rsi.index[-1], "price": rsi.values[-1]} if len(
                        rsi.index) > 0 else {}
                    self._trade_data.setdefault(stock, {}).update({
                        "rsi": rsi_data})
                    buy_data = {"date": buy_signal.index[-1], "price": buy_signal.values[-1]} if len(
                        buy_signal.index) > 0 else {}
                    self._trade_data.setdefault(stock, {}).update({
                        "buy_signal": buy_data})
                    sell_data = {"date": sell_signal.index[-1], "price": sell_signal.values[-1]} if len(
                        sell_signal.index) > 0 else {}
                    self._trade_data.setdefault(stock, {}).update({"sell_signal": sell_data})
                except Exception as e:
                    self._trade_data[stock] = {"error": str(e)}

        except Exception as e:
            self._trade_data = str(e)
