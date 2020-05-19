import pandas as pd
import numpy as np
import psycopg2
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.holtwinters import SimpleExpSmoothing


# Connect to database
conn = psycopg2.connect(host='localhost', port=5432, database='postgres')

# Query
query_train = """select closeprice from stock.stockprice
                 where ticker = 'GE' and
                 date_part('year', tradedate) between 2018 and 2019"""

query_test = """select closeprice from stock.stockprice
                where ticker = 'GE' and
                date_part('year', tradedate) = 2020"""

X_train= pd.io.sql.read_sql(query_train, conn)
# X_train['closeprice'] = np.log(X_train['closeprice'])
X_test = pd.io.sql.read_sql(query_test, conn)
print(X_train)

model = ExponentialSmoothing(X_train, trend='add', 
	                         seasonal='add', seasonal_periods=4).fit()
# print(model.summary())
pred = model.forecast(91)
# X_test['predictprice'] = np.exp(pred).tolist()
X_test['predictprice'] = pred.tolist()
print(X_test)

X_test.to_csv('hw_pred.csv', index=False)
y_bar = X_test['closeprice'].mean()
X_test['st'] = (X_test['closeprice']-y_bar)**2
X_test['se'] = (X_test['closeprice']-X_test['predictprice'])**2

r_square = 1-(X_test['se'].sum()/X_test['st'].sum())
print(r_square)

