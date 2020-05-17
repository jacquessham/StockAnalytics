import pandas as pd
import psycopg2
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from fbprophet import Prophet


# Connect to database
conn = psycopg2.connect(host='localhost', port=5432, database='postgres')


start_year = [1997, 2005] + list(range(2010, 2018))
methods = ['fbp', 'hw']

query_tickers = """select ticker from stock.stockshareoutstanding
                   order by shareoutstanding desc limit 20"""
tickers = pd.io.sql.read_sql(query_tickers, conn)


results = {'ticker':[], 'R-Square':[], 'Method':[]}

for ticker in tickers['ticker'].tolist():
	# Query for testing
	query_test = """select tradedate, closeprice from stock.stockprice
	                where ticker = '{}' and
	                date_part('year', tradedate)
	                between 2019 and 2020 order by tradedate""".format(ticker)
	X_test = pd.io.sql.read_sql(query_test, conn)
	X_test_ds = pd.DataFrame(X_test['tradedate'])
	X_test_ds.columns = ['ds']  
	y_bar = X_test['closeprice'].mean()

	result_ticker = []

	for year in start_year:
		query_train = """select tradedate, closeprice from stock.stockprice
	                 where ticker = '{}' and
	                 date_part('year', tradedate)
	                 between {} and 2018""".format(ticker, year)
		X_train = pd.io.sql.read_sql(query_train, conn)

		for method in methods:
			if method == 'hw':
				model = ExponentialSmoothing(X_train['closeprice'], trend='add', 
		                         seasonal='add', seasonal_periods=4).fit()
				pred = model.forecast(X_test.shape[0])
				X_test['predictprice'] = pred.tolist()
				X_test['st'] = (X_test['closeprice']-y_bar)**2
				X_test['se'] = (X_test['closeprice']-X_test['predictprice'])**2
				r_square = 1-(X_test['se'].sum()/X_test['st'].sum())
				result_ticker.append(((year, method), r_square))
			elif method == 'fbp':
				X_train_copy = X_train.copy()
				X_train_copy.columns = ['ds', 'y']
				model = Prophet()
				model.fit(X_train_copy)

				pred = model.predict(X_test_ds)
				pred['closeprice'] = X_test['closeprice']
				pred['st'] = (pred['closeprice']-y_bar)**2
				pred['se'] = (pred['closeprice']-pred['yhat'])**2
				r_square = 1-(pred['se'].sum()/pred['st'].sum())
				result_ticker.append(((year, method), r_square))
	result_ticker = sorted(result_ticker,key=lambda x:x[1], reverse=True)
	results['ticker'].append(ticker)
	results['R-Square'].append(result_ticker[0][1])
	results['Method'].append(result_ticker[0][0])

# Save Result
results = pd.DataFrame(results)
results.to_csv('heavy_result.csv', index=False)


		
