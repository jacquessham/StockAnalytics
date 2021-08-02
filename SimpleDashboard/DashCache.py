import datetime
from  dateutil.relativedelta import relativedelta
import yfinance as yf

class yfinance:
    """
    yfinance wrapper class, enabling cache
    """

    def __init__(self, flask_cache):
        self._cache = flask_cache
        self.ticker = ''
        self.info = {}
        self._history = None

    def Ticker(self, ticker):
        yf_ticker = yf.Ticker(ticker)
        self.ticker = ticker
        self.info = yf_ticker.info
        self._history = yf_ticker.history('max')

        return self

    def history(self, period='max'):

        today = datetime.datetime.now()

        time_idx = {
            '1mo': today + relativedelta(months=-1),
            '3mo': today + relativedelta(months=-3),
            '6mo': today + relativedelta(months=-6),
            'ytd': today.replace(month=1, day=1),
            '1y': today + relativedelta(years=-1),
            '3y': today + relativedelta(years=-3),
            '5y': today + relativedelta(years=-5),
            'max': today + relativedelta(years=-200)
        }

        if (self._history is not None) and (period in time_idx):
            return self._history[self._history.index > time_idx[period]]
        else:
            return self._history