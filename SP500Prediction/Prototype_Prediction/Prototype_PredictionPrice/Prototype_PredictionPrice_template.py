import pandas as pd
import psycopg2
from datetime import datetime
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from fbprophet import Prophet
import sys
sys.path.append('../../ETLPipelines')
from InsertData import *


# Connect to database
conn = psycopg2.connect(host='localhost', port=5432, database='postgres')


start_year = [1997, 2000, 2005, 2007] + list(range(2010, 2018))
num_start = 1
num_end = num_start + 9

query_tickers = """select i.ticker as ticker, i.row_num from(
                       select ticker, 
                       row_number() over(order by ticker) as row_num
                       from stock.stockshareoutstanding) as i
                   where row_num between {} and {}""".format(num_start, 
                   	                                         num_end)
tickers = pd.io.sql.read_sql(query_tickers, conn)

# Error Log
error_log = {'Ticker':[], 'transaction_date':[],
             'Database':[], 'Error':[]}
# Time Log
time_log = {'Ticker': [], 'Timer': []}

whole_starttime = datetime.now()
for ticker in tickers['ticker'].tolist():
	curr_starttime = datetime.now()
	# Query for testing
	query_test = """select tradedate, closeprice from stock.stockprice
	                where ticker = '{}' and
	                date_part('year', tradedate)
	                between 2019 and 2020
	                order by tradedate""".format(ticker)
	# Obtain testing data
	X_test = pd.io.sql.read_sql(query_test, conn)
	X_test.columns = ['ds','closeprice']
	X_test_ds = pd.DataFrame(X_test['ds'])
	
	# For calculate SST
	y_bar = X_test['closeprice'].mean()

	# Store result for each model
	result_ticker = []
	preds = {}

	for year in start_year:
		# Obtain training data 
		query_train = """select tradedate, closeprice from stock.stockprice
	                 where ticker = '{}' and
	                 date_part('year', tradedate)
	                 between {} and 2018""".format(ticker, year)
		X_train = pd.io.sql.read_sql(query_train, conn)
		
		# Train Model
		X_train_copy = X_train.copy()
		X_train_copy.columns = ['ds', 'y']
		try:
			model = Prophet()
			model.fit(X_train_copy)
			# Predict
			pred = model.predict(X_test_ds)
			pred['closeprice'] = X_test['closeprice']
			# Calculate R-square
			pred['st'] = (pred['closeprice']-y_bar)**2
			pred['se'] = (pred['closeprice']-pred['yhat'])**2
			r_square = 1-(pred['se'].sum()/pred['st'].sum())
			# Store result
			temp = (year, r_square, model)
			result_ticker.append(temp)
			preds[temp] = pred
		except:
			pass

	result_ticker = sorted(result_ticker,key=lambda x:x[1], reverse=True)
	rsquare_best = result_ticker[0][1]
	model_best = result_ticker[0][2]
	future = model_best.make_future_dataframe(periods=730)
	chosen_pred = model_best.predict(future)


	for index, row in chosen_pred.iterrows():
		try:
			insert_pred(conn, 'pred_proto_staging', ticker, row)
		except:
			error_log['Ticker'].append(ticker)
			error_log['transaction_date'].append(row['ds'])
			error_log['Database'].append('Good Staging')
			error_log['Error'].append('Insertion Error')

	# Insert the result to data batabase
	insert_result_proto(conn, ticker, rsquare_best, 
		                result_ticker[0][0])
	curr_endtime = datetime.now()
	curr_time = str(curr_endtime - curr_starttime)
	time_log['Ticker'].append(ticker)
	time_log['Timer'].append(curr_time)
	print(f'{curr_time} was spent on processing {ticker}')

whole_endtime = datetime.now()
wholetime = str(whole_endtime - whole_starttime)
time_log['Ticker'].append('All Components')
time_log['Timer'].append(wholetime)
print(f'{wholetime} was spent on processing data for all components')
conn.close()

# Save error log
error_log = pd.DataFrame(error_log)
filepath = 'Logs/ErrorLog_Pred_ProtoPrice_{}.csv'.format(num_end)
error_log.to_csv(filepath, index=False)

# Save timer log
time_log = pd.DataFrame(time_log)
filepath = 'Logs/TimeLog_Pred_ProtoPrice_{}.csv'.format(num_end)
time_log.to_csv(filepath, index=False)
