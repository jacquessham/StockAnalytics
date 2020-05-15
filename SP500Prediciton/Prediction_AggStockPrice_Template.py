import pandas as pd
import psycopg2


# Function to calculate marketshare
def get_mkcap(ticker, price, ticker2shares):
	shares = ticker2shares[ticker]
	return price*shares


# Connect to database
conn = psycopg2.connect(host='localhost', port=5432, database='postgres')

# Obtain Share Outstanding list
query_shares = """select l.ticker, l.shareoutstanding
                  from stock.stockshareoutstanding as l
                  left join
                  stock.stockmeta as r
                  on l.ticker = r.ticker
                  where r.indexcomponent = 'S&P 500'; """

shares_list = pd.io.sql.read_sql(query_shares, conn)
tickers = shares_list['ticker'].tolist()

ticker2shares = {}
for index, row in shares_list.iterrows():
	ticker2shares[row['ticker']] = row['shareoutstanding']

# Obtain stock price
query_prices = """select ticker, tradedate, closeprice
                  from stock.stockprice
                  where date_part('year', tradedate) 
                  between 2019 and 2020
                  and ticker in (
                  select ticker from stock.stockmeta
                  where indexcomponent = 'S&P 500')"""

df_price = pd.io.sql.read_sql(query_prices, conn)

# Calculate market cap
df_price['mkcap_daily'] = df_price.apply(lambda row: get_mkcap(row.ticker, 
	                                                           row.closeprice,
	                                                           ticker2shares),
                                                               axis=1)
sp500 = df_price[['tradedate','mkcap_daily']].groupby('tradedate').sum()
sp500 = sp500.reset_index()

print(sp500.head())
# Obtain SP500 Divisor
query_divisor = """ select l.tradedate, r.divisor 
					from
					    (select tradedate, 
					    date_part('quarter', tradedate) as tradequarter,
					    date_part('year', tradedate) as tradeyear
					    from (select distinct(tradedate) from
					    stock.stockprice where date_part('year',tradedate) 
					    between 2019 and 2020) as i
					    ) as l
					left join (
					    select *, 
					    date_part('quarter', tradedate) as tradequarter,
					    date_part('year', tradedate) as tradeyear
					    from stock.sp500divisor) as r
					on l.tradequarter = r.tradequarter and 
					   l.tradeyear = r.tradeyear"""
df_divisor = pd.io.sql.read_sql(query_divisor, conn)

sp500 = pd.merge(sp500, df_divisor, how='inner', on='tradedate')
print(sp500.head())

sp500['SP500'] = sp500['mkcap_daily']/(1.0*sp500['divisor'])
print(sp500.tail())