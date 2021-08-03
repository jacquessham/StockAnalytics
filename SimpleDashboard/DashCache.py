import datetime
from  dateutil.relativedelta import relativedelta
import json
import pandas as pd
import yfinance as yf

class yfinance:
    """
    yfinance wrapper class to enable cache.

    Only minimal methods, attributes implemented 
    which are used in the Dash app.
    """

    def __init__(self, flask_cache):
        self._cache = flask_cache
        self.ticker = ''
        self.info = {}
        self._history = None

    def Ticker(self, ticker):
        ticker_cached = self._cache.get(ticker)
        
        if ticker_cached:
            self.ticker = ticker_cached['ticker']
            self.info = ticker_cached['info']
            self._history = ticker_cached['history']

        else:
            yf_ticker = yf.Ticker(ticker)
            self.ticker = ticker
            self.info = yf_ticker.info
            self._history = yf_ticker.history('10y')

            self._cache.set(ticker, {
                'ticker': self.ticker,
                'info': self.info,
                'history': self._history, 
            })

        return self

    def history(self, period='10y'):

        if self._history is None:
            return None

        today = datetime.datetime.now()

        time_idx = {
            '1mo': today + relativedelta(months=-1),
            '3mo': today + relativedelta(months=-3),
            '6mo': today + relativedelta(months=-6),
            'ytd': today.replace(month=1, day=1),
            '1y': today + relativedelta(years=-1),
            '2y': today + relativedelta(years=-2),
            '3y': today + relativedelta(years=-3),
            '5y': today + relativedelta(years=-5),
            '10y': today + relativedelta(years=-10)
        }

        if period in time_idx.keys():
            return self._history[self._history.index > time_idx[period]]
        else:
            return None