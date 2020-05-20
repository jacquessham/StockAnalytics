-- Obtain top 20 heavy-weighted stocks in S&P 500
select * from stock.stockprice order by volume desc limit 20;

-- Obtain index weight of top 20 heavy-weighted stocks in S&P 500
select ticker, 
      (1.0*shareoutstanding)/(select sum(shareoutstanding)
      from stock.stockshareoutstanding) as weight
from stock.stockshareoutstanding
order by 2 desc limit 20;

-- Obtain index weight of top 20 heavy-weighted stocks in S&P 500 with names
select l.ticker, r.companyname,
      (1.0*l.shareoutstanding)/(select sum(shareoutstanding)
      from stock.stockshareoutstanding) as weight
from stock.stockshareoutstanding as l
left join
stock.stockmeta as r on l.ticker = r.ticker
order by 3 desc limit 20;

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


-- Obtain the stocks between 301th and 400th stocks in S&P 500
select i.ticker, i.row_num from(
select ticker, 
row_number() over(order by ticker) as row_num
from stock.stockshareoutstanding) as i
where row_num between 301 and 400;

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