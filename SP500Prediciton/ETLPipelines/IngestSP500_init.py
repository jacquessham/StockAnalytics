import pandas as pd
import psycopg2
import yfinance
from InsertData import *


# Obtain data from Yahoo Finance
sp500_ticker = '^GSPC'
sp500 = yfinance.Ticker(sp500_ticker).history(period='max').reset_index()

# Connect to database
conn = psycopg2.connect(host='localhost', port=5432, database='postgres')

# Documention stated execute() in a loop is faster than executemany()
for index, row in sp500.iterrows():
	insert_price(conn, row, sp500_ticker)

conn.close()