import yfinance as yf
from yahoo_fin import stock_info as si

def download_history(tickers, period='5d',interval='1d', group_by='ticker'):
    result = yf.download( tickers = tickers,
                          period = period,
                          interval = interval,
                          group_by = group_by
                         )
    return result

def get_info(ticker):
    data = yf.Ticker(ticker)
    return data

def get_realtime(ticker):
    while True:
        yield si.get_live_price(ticker)