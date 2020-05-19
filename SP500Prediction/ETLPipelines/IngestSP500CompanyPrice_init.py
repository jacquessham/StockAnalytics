import pandas as pd
from datetime import datetime
import psycopg2
import yfinance
from InsertData import *


# Obtain the list of companies and ticker
companylist = pd.read_csv('../../IndexComponents/SP500StockList.csv',
	                       engine='python')

# Connect to database
conn = psycopg2.connect(host='localhost', port=5432, database='postgres')

# Error Log
error_log = {'Ticker': [], 'Company': [], 'TransactionDate': [], 'Issue': []}
# Time Log
time_log = {'Ticker': [], 'Timer': []}


whole_starttime = datetime.now()
# Start upload data
for index, row in companylist.iterrows():
	curr_starttime = datetime.now()
	# Obtain data from Yahoo Finance
	curr_ticker = row['Ticker']
	curr_company = row['Company']
	curr_yfobj = yfinance.Ticker(curr_ticker)
	curr_metadata = {}
	# Print Progress
	print('Currently processing data on ',curr_ticker)
	# Upload metadata
	curr_metadata['ticker'] = curr_ticker
	curr_metadata['companyname'] = curr_company
	curr_metadata['gicssector'] = row['GICSSector']
	curr_metadata['gicssubindustry'] = row['GICSSubIndustry']
	curr_metadata['countrystockmarket'] = 'United States'
	curr_metadata['indexcomponent'] = 'S&P 500'
	try:
		insert_meta(conn, curr_metadata)
	except:
		print('####################')
		print('Meta Data Insertion Error on ', curr_ticker)
		error_log['Ticker'].append(curr_ticker)
		error_log['Company'].append(curr_company)
		error_log['TransactionDate'].append('')
		error_log['Issue'].append('Meta Data Insertion')
		# To end the query
		conn.commit()

	# Upload stock price
	curr_stockprice = curr_yfobj.history(period='max').reset_index()
	for index, row in curr_stockprice.iterrows():
		try:
			insert_price(conn, row, curr_ticker)
			conn.commit()
		except:
			print('####################')
			print('Stock Price Insertion Error on ', curr_ticker)
			# To record on the error log
			error_log['Ticker'].append(curr_ticker)
			error_log['Company'].append(curr_company)
			error_log['TransactionDate'].append(row['Date'])
			error_log['Issue'].append('Stock Price Insertion')
			conn.commit()

	# Update time log
	curr_endtime = datetime.now()
	curr_time = str(curr_endtime - curr_starttime)
	
	time_log['Ticker'].append(curr_ticker)
	time_log['Timer'].append(curr_time)
	print(f'{curr_time} was spent on processing {curr_ticker}')
whole_endtime = datetime.now()
wholetime = str(whole_endtime - whole_starttime)
time_log['Ticker'].append('All Components')
time_log['Timer'].append(wholetime)



print(f'{wholetime} was spent on processing data for all components')
conn.close()

# Save error log
error_log = pd.DataFrame(error_log)
error_log.to_csv('Logs/ErrorLog_SP500Companies.csv', index=False)

# Save timer log
time_log = pd.DataFrame(time_log)
time_log.to_csv('Logs/TimeLog_SP500Companies.csv', index=False)
