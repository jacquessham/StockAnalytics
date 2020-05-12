import pandas as pd
import psycopg2
import yfinance
from InsertData import *


# Obtain the list of companies and ticker
companylist = pd.read_csv('../../IndexComponents/SP500StockList.csv',
	                       engine='python')
# Connect to database
conn = psycopg2.connect(host='localhost', port=5432, database='postgres')

# Error Log
error_log = {'Ticker':[], 'Company':[], 'Issue': []}

# Start upload data
for index, row in companylist.iterrows():
	curr_ticker = row['Ticker']
	print('Now Processing Data of', curr_ticker)
	curr_yfobj = yfinance.Ticker(curr_ticker)

	# Obtain the data from .info(), try-catch to prevent bug from yfinance
	try:
		curr_share_num = curr_yfobj.info['sharesOutstanding']
	except:
		print('Error when Processing', curr_ticker)
		error_log['Ticker'].append(curr_ticker)
		error_log['Company'].append(row['Company'])
		error_log['Issue'].append('Yahoo Finance Info Error')
		continue		

	# Insert to database
	try:
		insert_share(conn, curr_ticker, curr_share_num)
	except:
		print('Error when Processing', curr_ticker)
		error_log['Ticker'].append(curr_ticker)
		error_log['Company'].append(row['Company'])
		error_log['Issue'].append('Share Outstanding Insertion')
		conn.commit()

conn.close()

# Save error log
error_log = pd.DataFrame(error_log)
error_log.to_csv('Logs/ErrorLog_SP500ShareOutstanding.csv', index=False)
