import datetime
import time

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import yfinance as yf
import matplotlib.pyplot as plt
import yahoo_fin.stock_info as si
import pandas as pd
import numpy as np


def get_stock_data(symbol, start_date, end_date):
    try:
        stock_data = yf.download(symbol, start=start_date, end=end_date)
        return stock_data['Close']
    except Exception as e:
        print(e)
        return e, None


def get_stock_info(symbol):
    try:
        stock_info = yf.Ticker(symbol)
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


def get_all_stocks():
    stock_list = ["RELIANCE.NS", "RELIANCE.BO", "TCS.BO", "TCS.NS", "HDFCBANK.BO", "HDFCBANK.NS",
                  "ICICIBANK.BO", "ICICIBANK.NS", "HINDUNILVR.NS", "HINDUNILVR.BO", "INFY.NS", "INFY.BO",
                  "BHARTIARTL.NS", "BHARTIARTL.BO", "ITC.BO", "ITC.NS", "SBIN.BO", "SBIN.NS", "BAJFINANCE.NS",
                  "BAJFINANCE.BO", "LT.NS", "LT.BO", "LICI.NS", "LICI.BO", "HCLTECH.NS", "HCLTECH.BO",
                  "KOTAKBANK.BO", "KOTAKBANK.NS", "AXISBANK.NS", "AXISBANK.BO", "MARUTI.NS", "MARUTI.BO",
                  "TITAN.NS", "TITAN.BO", "ASIANPAINT.NS", "ASIANPAINT.BO", "SUNPHARMA.BO", "SUNPHARMA.NS",
                  "ADANIENT.NS", "ADANIENT.BO", "BAJAJFINSV.NS", "BAJAJFINSV.BO", "NTPC.BO", "NTPC.NS",
                  "ULTRACEMCO.BO", "ULTRACEMCO.NS", "DMART.NS", "DMART.BO", "TATAMOTORS.NS", "TATAMOTORS.BO",
                  "TATAMTRDVR.NS", "TATAMTRDVR.BO", "ONGC.BO", "ONGC.NS", "NESTLEIND.BO", "NESTLEIND.NS",
                  "COALINDIA.BO", "COALINDIA.NS", "WIPRO.NS", "WIPRO.BO", "M&M.BO", "M&M.NS", "JSWSTEEL.BO",
                  "JSWSTEEL.NS", "POWERGRID.NS", "POWERGRID.BO", "ADANIPORTS.NS", "ADANIPORTS.BO", "BAJAJ",
                  "BAJAJ", "ADANIPOWER.NS", "ADANIPOWER.BO", "LTIM.NS", "LTIM.BO", "HAL.NS", "HAL.BO",
                  "ADANIGREEN.NS", "ADANIGREEN.BO", "TATASTEEL.BO", "TATASTEEL.NS", "IOC.BO", "IOC.NS",
                  "DLF.NS", "DLF.BO", "HDFCLIFE.NS", "HDFCLIFE.BO", "JIOFIN.NS", "JIOFIN.BO", "SBILIFE.BO",
                  "SBILIFE.NS", "VBL.BO", "VBL.NS", "SIEMENS.BO", "SIEMENS.NS", "GRASIM.BO", "GRASIM.NS",
                  "PIDILITIND.BO", "PIDILITIND.NS", "HINDZINC.BO", "HINDZINC.NS", "PFC.NS", "PFC.BO",
                  "BRITANNIA.NS", "BRITANNIA.BO", "TECHM.NS", "TECHM.BO", "INDUSINDBK.BO", "INDUSINDBK.NS",
                  "HINDALCO.BO", "HINDALCO.NS", "BEL.BO", "BEL.NS", "EICHERMOT.BO", "EICHERMOT.NS", "INDIGO.BO",
                  "INDIGO.NS", "GODREJCP.NS", "GODREJCP.BO", "BANKBARODA.BO", "BANKBARODA.NS", "DIVISLAB.NS",
                  "DIVISLAB.BO", "TRENT.NS", "TRENT.BO", "ZOMATO.NS", "ZOMATO.BO", "IRFC.NS", "IRFC.BO",
                  "RECLTD.NS", "RECLTD.BO", "SHREECEM.NS", "SHREECEM.BO", "CIPLA.NS", "CIPLA.BO", "DABUR.NS",
                  "DABUR.BO", "DRREDDY.NS", "DRREDDY.BO", "ADANIENSOL.BO", "ADANIENSOL.NS", "CHOLAFIN.BO",
                  "CHOLAFIN.NS", "BPCL.NS", "BPCL.BO", "ABB.NS", "ABB.BO", "TVSMOTOR.NS", "TVSMOTOR.BO",
                  "GAIL.BO", "GAIL.NS", "VEDL.NS", "VEDL.BO", "PNB.NS", "PNB.BO", "LODHA.NS", "LODHA.BO",
                  "TATAPOWER.NS", "TATAPOWER.BO", "AMBUJACEM.BO", "AMBUJACEM.NS", "TATACONSUM.BO",
                  "TATACONSUM.NS", "HAVELLS.NS", "HAVELLS.BO", "BAJAJHLDNG.BO", "BAJAJHLDNG.NS", "UNIONBANK.BO",
                  "UNIONBANK.NS", "ICICIPRULI.NS", "ICICIPRULI.BO", "APOLLOHOSP.NS", "APOLLOHOSP.BO",
                  "POLYCAB.NS", "POLYCAB.BO", "ATGL.NS", "ATGL.BO", "MANKIND.NS", "MANKIND.BO", "MCDOWELL",
                  "SHRIRAMFIN.BO", "SHRIRAMFIN.NS", "HEROMOTOCO.NS", "HEROMOTOCO.BO", "IOB.NS", "IOB.BO",
                  "CANBK.NS", "CANBK.BO", "TORNTPHARM.BO", "TORNTPHARM.NS", "ICICIGI.NS", "ICICIGI.BO",
                  "SRF.NS", "SRF.BO", "JINDALSTEL.NS", "JINDALSTEL.BO", "SBICARD.NS", "SBICARD.BO",
                  "JSWENERGY.BO", "JSWENERGY.NS", "CGPOWER.NS"]
    stock_list = ["AAVAS.NS", "AFFLE.NS", "AMBUJACEM.NS", "BANKBARODA.NS", "BANKINDIA.NS",
                  "BANSWRAS.NS", "BEL.NS", "BORORENEW.NS", "BCG.NS", "CDSL.NS", "CAMS.NS",
                  "CARERATING.NS", "CESC.NS", "DLINKINDIA.NS", "DATAMATICS.NS", "DCW.NS", "DEEPAKFERT.NS",
                  "DEEPAKNTR.NS", "DELTACORP.NS", "DBOL.NS", "DHAMPURSUG.NS", "DHANUKA.NS", "DVL.NS", "DIXON.NS",
                  "FINOLEXIND.NS", "GNFC.NS", "GSFC.NS", "GEOJITFSL.NS", "GLAND.NS", "GNA.NS",
                  "GPIL.NS", "GREENPLY.NS", "GUJGASLTD.NS", "HAPPSTMNDS.NS", "HAVELLS.NS", "HEG.NS", "HERANBA.NS",
                  "INFIBEAM.NS", "INFOBEAN.NS", "INFY.NS", "IOLCP.NS", "JKLAKSHMI.NS", "JKPAPER.NS", "JKTYRE.NS",
                  "JUBLFOOD.NS", "KANCHI.BO", "KRBL.NS", "KRBL.NS", "LT.NS", "LIBERTSHOE.NS",
                  "MANALIPETC.NS", "MIDHANI.NS", "NATIONALUM.NS", "NMDC.NS", "NSLNISP.NS", "NRBBEARING.NS", "NTPC.NS",
                  "NURECA.NS", "ONGC.NS", "ONMOBILE.NS", "PARAS.NS", "PENIND.NS", "PTC.NS",
                  "RCF.NS", "RVNL.NS", "RAJESHEXPO.NS", "RALLIS.NS", "RECLTD.NS", "RELIANCE.NS", "RUPA.NS", "SAIL.NS",
                  "SANOFI.NS", "SIS.NS", "SNOWMAN.NS", "SONACOMS.NS", "SONATSOFTW.NS", "STERLINBIO.NS", "STOVEKRAFT.NS",
                  "TANLA.NS", "TATACHEM.NS", "TATAELXSI.NS", "TATAMOTORS.NS", "TATAPOWER.NS", "TCS.NS", "TEJASNET.NS",
                  "TV18BRDCST.NS", "UNIONBANK.NS", "UPL.NS", "VEDL.NS", "IDEA.NS"]
    return stock_list


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
                print(rsi)
                short_rolling = stock_data.rolling(window=short_window).mean()
                long_rolling = stock_data.rolling(window=long_window).mean()

                # Plotting
                if plot:
                    plt.figure(figsize=(120, 8))
                    plt.title(f'{symbol} Moving Average Crossover')
                    plt.plot(stock_data, label='Close Price', color='blue')
                    plt.plot(short_rolling, label=f'{short_window}-day SMA', color='orange')
                    plt.plot(long_rolling, label=f'{long_window}-day SMA', color='green')
                    manager = plt.get_current_fig_manager()
                    manager.full_screen_toggle()
                # Plot Buy and Sell signals
                buy_signal = short_rolling[short_rolling > long_rolling]
                sell_signal = short_rolling[short_rolling <= long_rolling]
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
        return Response(response)

    def plot_moving_average_crossover(self, short_window, long_window, start_date, end_date, detail):
        # Get stock data
        try:
            stock_err = []
            stock_list = get_all_stocks()
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
                    rsi = calculate_rsi(stock_data, period=14)
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
