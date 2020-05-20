import pandas as pd
import psycopg2
from Results import *


# Connect to database
conn = psycopg2.connect(host='localhost', port=5432, database='postgres')

# Obtain stock price and predicted stock price of top 20 stock components
query = """select l.ticker as ticker, l.tradedate as tradedate,
			l.closeprice as price, r.closeprice as predictedprice
			from stock.stockprice as l join stock.pred_fbp_price_sp500_base as r
			on l.ticker = r.ticker and l.tradedate = r.tradedate
			where l.ticker in (
			select ticker from stock.stockshareoutstanding
			order by shareoutstanding desc limit 20)
			and date_part('year', l.tradedate) between 2019 and 2020
			order by 1, 2; """

stockprice = pd.io.sql.read_sql(query, conn)

## Prepare SST
stockprice_mean = stockprice[['ticker', 'price']].groupby('ticker') \
                            .mean().reset_index()
stockprice_mean.columns = ['ticker','price_mean']
stockprice_sst = pd.merge(stockprice.drop('predictedprice', axis=1), stockprice_mean, 
	                      how='left', on='ticker')
stockprice_sst['st'] = (stockprice_sst['price'] - stockprice_sst['price_mean'])**2
stockprice_sst = stockprice_sst[['ticker','st']].groupby('ticker', 
	                                                      as_index=False).sum()

## Calculate SSE, RMSE, R-square
stockprice['se'] = (stockprice['price']-stockprice['predictedprice'])**2
stockprice_sse = stockprice[['ticker', 'se']].groupby('ticker', as_index=False) \
                           .agg(['sum', 'count']).reset_index()
stockprice_sse['rmse'] = (stockprice_sse['se']['sum']/ \
	                      stockprice_sse['se']['count'])**0.5
stock_anova = pd.merge(stockprice_sse, stockprice_sst, on='ticker')
stock_anova['Rsquare'] = 1-(stock_anova[('se', 'sum')]/stock_anova['st'])
print(stock_anova)
stock_anova.to_csv('fbp_resultbase.csv', index=False)
