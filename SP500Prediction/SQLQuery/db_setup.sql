-- Create table example
create table stock.stockshareoutstanding(
    ticker varchar(10),
    shareoutstanding bigint
);

-- Change table name
alter table stock.pred_price_sp500base
rename to pred_fbp_price_sp500_base;

-- Delete table
-- delete from stock.stockprice;