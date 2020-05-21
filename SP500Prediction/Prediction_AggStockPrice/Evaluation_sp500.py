import pandas as pd
import psycopg2


# Connect to database
conn = psycopg2.connect(host='localhost', port=5432, database='postgres')

# Obtain stock price and predicted stock price of top 20 stock components
query = """select * from stock.pred_dy_sp500 as l
           left join
           (select * from stock.stockprice where ticker = '^GSPC'
            and date_part('year', tradedate) between 2019 and 2020) as r
            on l.tradedate = r.tradedate
           order by l.tradedate; """

sp500 = pd.io.sql.read_sql(query, conn)
print(sp500.head())

# Prepare SST
sp500_testmean = sp500['sp500_testdata'].mean()
sp500['st_test'] = (sp500['sp500_testdata'] - sp500_testmean)**2

sp500_realmean = sp500['closeprice'].mean()
sp500['st_real'] = (sp500['closeprice'] - sp500_realmean)**2



# Calculate SSE for pred and predMod
sp500['se_pred'] = (sp500['sp500_testdata'] - sp500['sp500_pred'])**2
sp500['se_predmod'] = (sp500['sp500_testdata'] - sp500['sp500_predmod'])**2

## Calculate R-square
rsqu_sp500_pred = 1-(sp500['se_pred'].sum()/sp500['st_test'].sum())
rsqu_sp500_predmod = 1-(sp500['se_predmod'].sum()/sp500['st_test'].sum())

rsqu_sp500_pred_real = 1-(sp500['se_pred'].sum()/sp500['st_real'].sum())
rsqu_sp500_predmod_real = 1-(sp500['se_predmod'].sum()/sp500['st_real'].sum())

print('Compare to self-calculated index:')
print('Basic model:',rsqu_sp500_pred)
print('Modified model:',rsqu_sp500_predmod)
print('\n\nCompare to real index:')
print('Basic model:',rsqu_sp500_pred_real)
print('Modified model:',rsqu_sp500_predmod_real)