import pandas as pd
import psycopg2
import plotly
import plotly.graph_objs as go
from plotly.offline import *
from fbprophet import Prophet
from Graph import *
import plotly.io as pio
pio.renderers.default = 'notebook'


# To initiate ploty to run offline
# init_notebook_mode(connected=True)

# Connect to database
conn = psycopg2.connect(host='localhost', port=5432, database='postgres')

# Obtain testing data between 2019 and 2020
query_test = """select tradedate, closeprice from stock.stockprice
                where ticker = 'LMT' and
                date_part('year', tradedate) between 2019 and 2020
                order by 1"""
df_test = pd.io.sql.read_sql(query_test, conn)
df_test.columns = ['ds', 'realprice']
# Obtain the data frame of dates in testing data
X_test = pd.DataFrame(df_test['ds'])

# Calculate SST
ybar_test = df_test['realprice'].mean()*1.0
sst = ((df_test['realprice'] - ybar_test)**2).sum()

### Train model using 1997-2018 data, let's call model_max ###
# Obtain training data between 1997 and 2018
query_train = """select tradedate, closeprice from stock.stockprice
	             where ticker = 'LMT' and
	             date_part('year', tradedate)
	             between 1997 and 2018
	             order by 1"""
X_train = pd.io.sql.read_sql(query_train, conn)
X_train.columns = ['ds', 'y']

# Model Training
model_max = Prophet()
model_max.fit(X_train)
pred_max = model_max.predict(X_test)
# Calculate R-square
pred_max = pd.merge(pred_max, df_test, how='inner', on='ds')
sse_max = ((pred_max['yhat'] - pred_max['realprice'])**2).sum()
rsqu_max = 1 - sse_max / sst


### Train model using 2010-1018 data, 8 years model ###
query_train = """select tradedate, closeprice from stock.stockprice
	             where ticker = 'LMT' and
	             date_part('year', tradedate)
	             between 2010 and 2018
	             order by 1"""
X_train = pd.io.sql.read_sql(query_train, conn)
X_train.columns = ['ds', 'y']

model_8yr = Prophet()
model_8yr.fit(X_train)
pred_8yr = model_8yr.predict(X_test)
pred_8yr = pd.merge(pred_8yr, df_test, how='inner', on='ds')
sse_8yr = ((pred_8yr['yhat'] - pred_8yr['realprice'])**2).sum()
rsqu_8yr = 1 - sse_8yr / sst

# Generate graph of the results
fig = generate_line_chart(X_train, df_test, pred_max, 'model_max',
	                      pred_8yr, 'model_8yr', 
	                      'Prediction with Facebook Prophet')
plotly.offline.plot(fig, filename='LMTprice_fbp.html')

print('The R-square of model_max is',f'{rsqu_max:.2f}')
print('The R-square of model_8yr is',f'{rsqu_8yr:.2f}')
