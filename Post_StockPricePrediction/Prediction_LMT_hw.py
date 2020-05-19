import pandas as pd
import numpy as np
import psycopg2
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import plotly
import plotly.graph_objs as go
from plotly.offline import *
from Graph import *


# To initiate ploty to run offline
# init_notebook_mode(connected=True)

# Connect to database
conn = psycopg2.connect(host='localhost', port=5432, database='postgres')

# Query
query_test = """select tradedate as ds, closeprice as realprice
                from stock.stockprice
                where ticker = 'LMT' and
                date_part('year', tradedate) between 2019 and 2020
                order by 1; """
df_test = pd.io.sql.read_sql(query_test, conn)
# Data for graphing
query_prior = """select tradedate as ds, closeprice as y
                from stock.stockprice
                where ticker = 'LMT' and
                date_part('year', tradedate) between 2015 and 2020
                order by 1; """
df_prior = pd.io.sql.read_sql(query_prior, conn)

# Calculate SST
ybar_test = df_test['realprice'].mean()*1.0
sst = ((df_test['realprice'] - ybar_test)**2).sum()


### Train model using 2017-2018 data, let's call model_max ###
# Obtain training data between 2017 and 2018
query_train = """select tradedate, closeprice from stock.stockprice
                 where ticker = 'LMT' and
                 date_part('year', tradedate) = 2018
                 order by 1; """
df_train = pd.io.sql.read_sql(query_train, conn)
X_train = df_train['closeprice']

# Smoothing_leve and smoothing_slope are alpha and beta
# Optimtize through grid search, 0.6 and 0.25 are happened to be the best ones
model = ExponentialSmoothing(X_train, trend='mul',
	                         seasonal='mul', seasonal_periods=4).fit(
	                         smoothing_level=0.8,smoothing_slope=0.25)
pred = model.forecast(df_test.shape[0])
df_test = df_test.copy()
df_test['yhat'] = pred.tolist()
sse = ((df_test['yhat'] - df_test['realprice'])**2).sum()
rsqu = 1 - sse / sst

# Generate graph of the results
fig = generate_line_chart(df_prior, df_test, df_test, 'Prediction',
	                      title='Prediction with Holt-Winters Method')
plotly.offline.plot(fig, filename='LMTprice_hw.html')

print('The R-square of model is',f'{rsqu:.2f}')