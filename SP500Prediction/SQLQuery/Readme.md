# SQL Query Used
This folder stored the SQL query used in the model training phase. There are 3 SQL files in this folder:
<ul>
	<li>db_setup.sql - Queries to set up database</li>
	<li>sp500_info.sql - Queries to look at the insight of S&P 500</li>
	<li>stockprice.sql - Queries to obtain stock price based on different conditions</li>
</ul>

## db_setup.sql
It contains the queries to create tables, rename tables, or delete all entries in a table. Note that the delete query is commented.

## sp500_info.sql
It contains the queries to look at heavy-weighted components and list of stocks in the S&P 500. 

## stockprice.sql
It contains the queries to obtain the real stock price, predictive stock price based on different conditions, including specific stocks, time interval, weight in S&P 500, prediction accuracy. 