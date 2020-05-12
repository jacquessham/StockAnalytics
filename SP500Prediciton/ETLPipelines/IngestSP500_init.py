import pandas as pd
import psycopg2
import yfinance


# Function to insert values to database
def insert_price(conn, query, row, ticker):
	data = (ticker, row['Date'], row['Open'], row['High'], row['Low'],
		    row['Close'], row['Volume'])
	cur = conn.cursor()
	cur.execute(query, data)
	conn.commit()




# Obtain data from Yahoo Finance
sp500_ticker = '^GSPC'
sp500 = yfinance.Ticker(sp500_ticker).history(period='max').reset_index()

# Connect to database
conn = psycopg2.connect(host='localhost', port=5432, database='postgres')

# Insert values into database
query = """insert into stock.stockprice (ticker, tradedate, openprice, high, low,
        closeprice, volume) values (%s, %s, %s, %s, %s, %s, %s)"""

# Documention stated execute() in a loop is faster than executemany()
for index, row in sp500.iterrows():
	insert_price(conn, query, row, sp500_ticker)

conn.close()