-- Obtain S&P 500 in 2020
select count(*) from stock.stockprice
where ticker = '^GSPC'
and date_part('year', tradedate) = 2020;

-- Obtain Apple Stock price between 2010 and 2018
select * from stock.stockprice
where ticker = 'AAPL' and 
date_part('year', tradedate) between 2010 and 2018;


-- Obtain all stock price of Apple stock
select * from stock.stockprice where ticker = 'AAPL' order by tradedate;

-- Obtain real stock price and predicted stock price top 20 heavy-weighted stock
select l.ticker as ticker, l.tradedate as tradedate,
l.closeprice as price, r.closeprice as predictedprice
from stock.stockprice as l join stock.pred_fbp_price_sp500_base as r
on l.ticker = r.ticker and l.tradedate = r.tradedate
where l.ticker in (
select ticker from stock.stockshareoutstanding
order by shareoutstanding desc limit 20)
and date_part('year', l.tradedate) between 2019 and 2020
order by 1, 2;

-- Obtain real stock price and predicted stock price of Microsoft stock
select l.ticker as ticker, l.tradedate as tradedate, r.tradedate,
l.closeprice as price, r.closeprice as predictedprice
from stock.stockprice as l join stock.pred_fbp_price_sp500_5yr as r
on l.ticker = r.ticker and l.tradedate = r.tradedate
where l.ticker = 'MSFT'
and date_part('year', l.tradedate) between 2019 and 2020
order by 1, 2;


-- Obtain the result from model training phase sort by ticker
select * from stock.pred_dy_trainresult
order by 1;

-- Obtain the list of companies with highest R-square along with meta data
select l.ticker, r.companyname,
r.gicssector, l.rsquare,
l.start_year, l.package
from stock.pred_dy_trainresult as l
left join
stock.stockmeta as r
on l.ticker = r.ticker
order by l.rsquare desc;

-- Obtain number of stocks have positive r-square predictive model
select count(*) from stock.pred_dy_trainresult
where rsquare > 0;

-- Obtain number of stocks have negative r-square predictive model
select count(*) from stock.pred_dy_trainresult

-- Expand the quarterly entries of divisor data to daily entries
select l.tradedate, r.divisor 
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
on l.tradequarter = r.tradequarter and l.tradeyear = r.tradeyear
order by 1 desc;
where rsquare < 0;

-- Union all predicitve stock price
select * from stock.pred_dy_staging_sp500_good
union
select * from stock.pred_dy_staging_sp500_bad;

-- Union good predictive stock price and real stock price for negative accuracy models
select * from stock.pred_dy_staging_sp500_good
union
select ticker, tradedate, closeprice 
from stock.stockprice
where ticker not in (
    select distinct ticker
    from stock.pred_dy_staging_sp500_good)
    and ticker in (
        select ticker from stock.stockmeta
        where indexcomponent = 'S&P 500'
    ) 
    and date_part('year', tradedate) 
    between 2019 and 2020
order by ticker, tradedate;