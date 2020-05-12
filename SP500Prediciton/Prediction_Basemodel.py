import pandas as pd
import numpy as np
import psycopg2
from fbprophet import Prophet
from Results import *


# Connect to database
conn = psycopg2.connect(host='localhost', port=5432, database='postgres')

# Obtain training and testing data and convert dataframe format for fbprophet
query_train = """select tradedate, closeprice from stock.stockprice
                 where date_part('year', tradedate) between 1997 and 2018"""
query_test = """select tradedate, closeprice from stock.stockprice
                where date_part('year', tradedate) between 2019 and 2020"""

sp500_train = pd.io.sql.read_sql(query_train, conn)
sp500_test = pd.io.sql.read_sql(query_test, conn)

sp500_train.columns = ['ds','y']
sp500_test.columns = ['ds','y']

### Baseline model ###
# Obtain the testing data date interval
future_date = pd.DataFrame(sp500_test['ds'])


# Train a baseline model
model_base = Prophet()
model_base.fit(sp500_train)

# Make Prediction and obtain RMSE
pred_base = model_base.predict(future_date)
result_base = pd.merge(sp500_test[['ds','y']], pred_base[['ds','yhat']],
	                   how='left', on='ds')
result_base['se'] = (result_base['y'] - result_base['yhat'])**2


### Time Series Model with Natural Log label ###
# Data Preparsion
sp500_train_log = sp500_train.copy()
sp500_train_log['y'] = np.log(sp500_train_log['y'])
sp500_test_log = sp500_test.copy()
sp500_test_log['y'] = np.log(sp500_test_log['y'])

# Train a log model
model_log = Prophet()
model_log.fit(sp500_train_log)
pred_log = model_log.predict(future_date)
result_log = pd.merge(sp500_test_log[['ds','y']], pred_log[['ds','yhat']],
	                  how='left', on='ds')
result_log['y'] = np.exp(result_log['y'])
result_log['yhat'] = np.exp(result_log['yhat'])
result_log['se'] = (result_log['y'] - result_log['yhat'])**2


### Time Series Growth Prediction Model ###
# Data Preparsion
sp500_train_growth = sp500_train.copy()
sp500_train_growth['y'] = sp500_train_growth.y.pct_change()
model_growth = Prophet()
model_growth.fit(sp500_train_growth)
pred_growth = model_growth.predict(future_date)

# Get the base number for prediction
last_trainX = sp500_train.iloc[-1,1]
yhat = [last_trainX]

# Calculate the index
yhat_growth = pred_growth['yhat'].tolist()
for num in range(len(yhat_growth)):
	curr_index = yhat[num-1]*(1+yhat_growth[num])
	yhat.append(curr_index)

# Calculate RMSE
result_growth = sp500_test.copy()
result_growth['yhat'] = yhat[1:]
result_growth['se'] = (result_growth['y'] - result_growth['yhat'])**2

rmse_baseline = (result_base['se'].sum()/result_base.shape[0])**.5
rmse_log = (result_log['se'].sum()/result_log.shape[0])**.5
rmse_growth = (result_growth['se'].sum()/result_growth.shape[0])**.5

# Calculate R-square
sp500_mean = sp500_test['y'].mean()
sp500_test['st'] = (sp500_test['y'] - sp500_mean)**2
sst = sp500_test['st'].sum()*1.0

rsqu_base = 1-(result_base['se'].sum()/sst)
rsqu_log = 1-(result_log['se'].sum()/sst)
rsqu_growth = 1-(result_growth['se'].sum()/sst)

save_result_rmse('Baseline Model', rmse_baseline, rsqu_base)
save_result_rmse('Time Series Natural Log Model', rmse_log, rsqu_log)
save_result_rmse('Time Series Growth Prediction Model', rmse_growth, rsqu_growth)
