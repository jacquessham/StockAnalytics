import pandas as pd
import psycopg2
import yfinance
from InsertData import *


# Obtain data from Yahoo Finance
sp500_ticker = '^GSPC'
sp500 = yfinance.Ticker(sp500_ticker).history(period='max').reset_index()

# Connect to database
conn = psycopg2.connect(host='localhost', port=5432, database='postgres')

# Error Log
error_log = {'TransactionDate': [], 'Issue': []}

# Documention stated execute() in a loop is faster than executemany()
for index, row in sp500.iterrows():
	try:
		insert_price(conn, row, sp500_ticker)
	except:
		print('Insertion Error -- Transaction Date:', row['Date'])
		error_log['TransactionDate'].append(row['Date'])
		error_log['Issue'].append('Index Insertion')
		conn.commit()

conn.close()

# Save error log
error_log = pd.DataFrame(error_log)
error_log.to_csv('Logs/ErrorLog_SP500.csv', index=False)
