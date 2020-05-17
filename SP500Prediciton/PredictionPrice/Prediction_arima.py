import pandas as pd
import numpy as np
import psycopg2
import pmdarima as pm
from pmdarima.datasets import load_wineind
from statsmodels.tsa.arima_model import ARIMA


# Connect to database
conn = psycopg2.connect(host='localhost', port=5432, database='postgres')

# Query
query_train = """select closeprice from stock.stockprice
                 where ticker = 'AAPL' and
                 date_part('year', tradedate) between 1997 and 2018"""

query_test = """select closeprice from stock.stockprice
                where ticker = 'AAPL' and
                date_part('year', tradedate) between 2019 and 2020"""

X_train= pd.io.sql.read_sql(query_train, conn)
# X_train['closeprice'] = np.log(X_train['closeprice'])
X_test = pd.io.sql.read_sql(query_test, conn)

model = pm.auto_arima(X_train, start_p=1, start_q=1,
                             max_p=6, max_q=6, m=12,
                             max_P=6, max_Q=6, seasonal=True,
                             d=1, D=1, max_d=6, max_D=6, trace=True,
                             error_action='ignore',
                             suppress_warnings=True,
                             stepwise=True)
print(model.summary())
pred = model.predict(343)
# X_test['predictprice'] = np.exp(pred)
X_test['predictprice'] = pred
print(X_test)
