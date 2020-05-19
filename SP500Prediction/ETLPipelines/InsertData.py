# Function to insert prices to database
def insert_price(conn, row, ticker):
	# Query
	query = """insert into stock.stockprice (ticker, tradedate, openprice, high, low,
            closeprice, volume) values (%s, %s, %s, %s, %s, %s, %s)"""
	# row must be a row from a pandas dataframe from yfinance
	data = (ticker, row['Date'], row['Open'], row['High'], row['Low'],
		    row['Close'], row['Volume'])
	cur = conn.cursor()
	cur.execute(query, data)
	conn.commit()
	

# Function to insert meta data to database
def insert_meta(conn, meta_dict):
	# Query
	query = """insert into stock.stockmeta (ticker, companyname,
	        gicssector, gicssubindustry, countrystockmarket, indexcomponent) 
	        values (%s, %s, %s, %s, %s, %s)"""
	# Take meta data store in dictionary
	data = (meta_dict['ticker'], meta_dict['companyname'],
		    meta_dict['gicssector'], meta_dict['gicssubindustry'], 
		    meta_dict['countrystockmarket'], meta_dict['indexcomponent'])
	cur = conn.cursor()
	cur.execute(query, data)
	conn.commit()

# Function to insert share data to database
def insert_share(conn, ticker, share_num):
	# Query
	query = """insert into stock.stockshareoutstanding (ticker, 
	           shareoutstanding) values (%s, %s)"""
	data = (ticker, share_num)
	cur = conn.cursor()
	cur.execute(query, data)
	conn.commit()

# Function to insert prediction to database
def insert_pred(conn, table, ticker, row):
	# Query
	query = """insert into stock.{} (ticker, tradedate,
	           closeprice)""".format(table)
	query += """values (%s, %s, %s)"""
	data = (ticker, row['ds'], row['yhat'])
	cur = conn.cursor()
	cur.execute(query, data)
	conn.commit()

# Function to insert training result from Prediction_Dynamic_StockPrice
def insert_result(conn, ticker, rsqu, start_year, package):
	# Query
	query = """insert into stock.pred_dy_trainresult (ticker, rsquare,
	           start_year, package) values (%s, %s, %s, %s)"""
	data = (ticker, rsqu, start_year, package)
	cur = conn.cursor()
	cur.execute(query, data)
	conn.commit()

# Function to insert S&P 500 Divisor
def insert_divisor(conn, tradedate, divisor):
	query = """ insert into stock.sp500divisor (tradedate, divisor)
	            values (%s, %s)"""
	data = (tradedate, divisor)
	cur = conn.cursor()
	cur.execute(query, data)
	conn.commit()

# Function to insert pred_dy_sp500
def insert_sp500_db(conn, row):
	query = """ insert into stock.pred_dy_sp500 (tradedate, sp500_testdata,
	            sp500_pred, sp500_predMod) values (%s, %s, %s, %s) """
	data = (row['tradedate'], row['sp500_test'], row['sp500_pred'],
		    row['sp500_predMod'])
	cur = conn.cursor()
	cur.execute(query, data)
	conn.commit()
