import pandas as pd
import numpy as np
import psycopg2
import pmdarima as pm
import plotly
import plotly.graph_objs as go
from plotly.offline import *
from Graph import *
import plotly.io as pio
pio.renderers.default = 'notebook'


# Connect to database
conn = psycopg2.connect(host='localhost', port=5432, database='postgres')

# Query
query_train = """select tradedate, closeprice from stock.stockprice
                 where ticker = 'AAPL' and
                 date_part('year', tradedate) between 1997 and 2018
                 order by 1; """

query_test = """select tradedate as ds, closeprice as realprice
                from stock.stockprice
                where ticker = 'AAPL' and
                date_part('year', tradedate) between 2019 and 2020
                order by 1; """

df_train = pd.io.sql.read_sql(query_train, conn)
df_test = pd.io.sql.read_sql(query_test, conn)

# Calculate SST
ybar_test = df_test['realprice'].mean()*1.0
sst = ((df_test['realprice'] - ybar_test)**2).sum()

### Train model using 1997-2018 data, let's call model_max ###
# Obtain training data between 1997 and 2018
df_train = pd.io.sql.read_sql(query_train, conn)
X_train = df_train['closeprice']
model_max = pm.auto_arima(X_train, start_p=1, start_q=1,
                             max_p=3, max_q=3, m=12,
                             max_P=3, max_Q=3, seasonal=True,
                             d=1, D=1, max_d=3, max_D=3, trace=True,
                             error_action='ignore',
                             suppress_warnings=True,
                             stepwise=True)
print(model_max.summary())
df_test_max = df_test.copy()
pred_max = model_max.predict(df_test.shape[0]) # It returns ndarray
df_test_max['yhat'] = pred_max
sse_max = ((df_test_max['yhat'] - df_test_max['realprice'])**2).sum()
rsqu_max = 1 - sse_max / sst

### Train model using 2010-2018 data, let's call model_max ###
# Obtain training data between 2010 and 2018
query_train = """select tradedate, closeprice from stock.stockprice
                 where ticker = 'AAPL' and
                 date_part('year', tradedate) between 2010 and 2018
                 order by 1; """
df_train = pd.io.sql.read_sql(query_train, conn)
X_train = df_train['closeprice']
model_8yr = pm.auto_arima(X_train, start_p=1, start_q=1,
                             max_p=3, max_q=3, m=12,
                             max_P=3, max_Q=3, seasonal=True,
                             d=1, D=1, max_d=3, max_D=3, trace=True,
                             error_action='ignore',
                             suppress_warnings=True,
                             stepwise=True)
print(model_8yr.summary())
df_test_8yr = df_test.copy()
pred_8yr = model_8yr.predict(df_test.shape[0])
df_test_8yr['yhat'] = pred_8yr
sse_8yr = ((df_test_8yr['yhat'] - df_test_8yr['realprice'])**2).sum()
rsqu_8yr = 1 - sse_8yr / sst

print('The R-square of model_max is',f'{rsqu_max:.2f}')
print('The R-square of model_8yr is',f'{rsqu_8yr:.2f}')


# Generate graph of the results
df_train.columns = ['ds','y']
fig = generate_line_chart(df_train, df_test, df_test_max, 'model_max',
	                      df_test_8yr, 'model_8yr', 
	                      'Prediction with pmdarima')
plotly.offline.plot(fig, filename='AAPLprice_pmdarima.html')


