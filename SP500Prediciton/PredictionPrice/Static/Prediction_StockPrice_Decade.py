import pandas as pd
from datetime import datetime
import psycopg2
from fbprophet import Prophet
from ETLPipelines.InsertData import *


# Connect to database
conn = psycopg2.connect(host='localhost', port=5432, database='postgres')

# Obtain trade days between 2019 and 2020
query_test = """select tradedate from stock.stockprice
                where ticker = '^GSPC' and
                date_part('year', tradedate) between 2019 and 2020"""
ds_test = pd.io.sql.read_sql(query_test, conn)
ds_test.columns = ['ds']

# obtain the list of SP500 components
query_companies = """select ticker from stock.stockmeta
                     where indexcomponent = 'S&P 500' """
sp500_companies = pd.io.sql.read_sql(query_companies, conn)['ticker'].tolist()

# Error Log
error_log = {'Ticker': [], 'TransactionDate': [], 'Issue': []}
# Time Log
time_log = {'Ticker': [], 'Timer': []}


whole_starttime = datetime.now()
# Start upload data
for curr_ticker in sp500_companies:
	curr_starttime = datetime.now()
	# Print Progress
	print('Currently processing data on ',curr_ticker)
	query = """select tradedate, closeprice from stock.stockprice
	           where ticker = '{}' and
	           date_part('year', tradedate)
	           between 2010 and 2018""".format(curr_ticker)

	X_train = pd.io.sql.read_sql(query, conn)
	X_train.columns = ['ds', 'y']
	try:
		model = Prophet()
		model.fit(X_train)
	except:
		print('####################')
		print('Modeling Error on ', curr_ticker)
		error_log['Ticker'].append(curr_ticker)
		error_log['TransactionDate'].append('')
		error_log['Issue'].append('Modeling Error')
		continue

	pred = model.predict(ds_test.copy())
	for index, row in pred.iterrows():
		try:
			insert_pred(conn, 'pred_price_sp500decade', curr_ticker, row)
		except:
			print('####################')
			print('Prediction Insertion Error on ', curr_ticker)
			error_log['Ticker'].append(curr_ticker)
			error_log['TransactionDate'].append(row['ds'])
			error_log['Issue'].append('Prediction Insertion')
			# To end the query
			conn.commit()
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
error_log.to_csv('ETLPipelines/Logs/ErrorLog_SP500PredD.csv', index=False)

# Save timer log
time_log = pd.DataFrame(time_log)
time_log.to_csv('ETLPipelines/Logs/TimeLog_SP500PredD.csv', index=False)
