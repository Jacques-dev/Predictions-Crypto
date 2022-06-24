import yfinance as yf

data = yf.Ticker('GOOG').history(period='max')

data.to_csv('data/bitcoin.csv')