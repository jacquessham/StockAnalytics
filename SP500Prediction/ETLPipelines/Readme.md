# ETL Pipelines
This folder is the Data Acquisition part of the Stock Price Aggregation Model. Since the data is stored in the local relational database, this folder is storing the pipeline files that ingest data to the database. The relational database is Postgre. You may find the tables in the [Data folder](../Data).

## Files
There are 6 Python files and 1 csv file. The following list are the files in this folder:
<ul>
	<li>IngestSP500_init.py</li>
	<li>IngestSP500CompanyPrice_init.py</li>
	<li>IngestSP500Divisor.py</li>
	<li>IngestSP500ShareOutstanding_init.py</li>
	<li>IngestSP500ShareOutstanding_forerrors.py</li>
	<li>ShareOutstanding_ForErrors.csv</li>
	<li>InsertData.py</li>
</ul>

## Package Used
Package used:
<ul>
	<li>pandas</li>
	<li>datetime</li>
	<li>pasycopg2</li>
	<li>yfinance</li>
</ul>

## InsertData.py
This is a helper code for insert data into the database. It consists of 7 functions:
<ul>
	<li>insert_price() - function to insert data to <i>stockprice</i> table</li>
	<li>insert_meta() - function to insert data to <i>stockmeta</i> table</li>
	<li>insert_share() - function to insert data to <i>stockshareoutstanding</i> table</li>
	<li>insert_pred() - function to insert data to insert prediction data</li>
	<li>insert_result() - function to insert predictive model accuracy and meta data</li>
	<li>insert_divisor() - function to insert data to <i>sp500divisor</i> table</li>
	<li>insert_sp500_db - function to insert data to <i>pred_dy_sp500</i> table</li>
</ul>

## IngestSP500_init.py
This pipeline obtains the historical closing of S&P 500 from Yahoo Finance and store the entries in <i>stockprice</i> table. Once the data is downloaded from Yahoo Finance, it adds the ticker of S&P 500 in Yahoo Finance format and insert into the table. It relies on insert_price() in <i>InsertData.py</i>. The detail of the database table can be found in the [Data folder](../Data).

## IngestSP500CompanyPrice_init.py
This pipline obtains the historical stock prices of 505 stock prices and stock meta data from Yahoo Finance and store the entries in <i>stockprice</i> table and <i>stockmeta</i> table. The detail of the database table can be found in the [Data folder](../Data). Once the data is downloaded from Yahoo Finance, it adds the ticker of the companies in Yahoo Finance format and insert into the tables. It relies on insert_price() and insert_meta() in <i>InsertData.py</i>. Beside inserting the entries into the tables, it also returns the error log and timer log which time the work of each stock.

## IngestSP500Divisor.py
This pipeline obtains the divisor of S&P 500 from Y Chart and store the quarterly divisor into the <i>sp500divisor</i> table. The detail of the database table can be found in the [Data folder](../Data). It relies on insert_divisor() in the <i>InsertData.py</i>.

## IngestSP500ShareOutstanding_init.py
This pipeline obtains the floating shares of all S&P 500 components from Yahoo Finance in May, 2020 and store the entries in <i>stockshareoutstanding</i> table. Once the data is downloaded from Yahoo Finance, it adds the entries to the table. It relies insert_share() in <i>InsertData.py</i>. Beside inserting the entries into the tables, it also returns the error log. The detail of the database table can be found in the [Data folder](../Data).

## IngestSP500ShareOutstanding_forerrors.py
This pipeline obtains the floating shares of the stocks which is not sucessfully insert in the <i>IngestSP500ShareOutstanding_init.py</i>. <i>ShareOutstanding_ForErrors.csv</i> is the csv files that contains data that is obtained manually that is needed to be inserted into the <i>stockshareoutstanding</i> table. This pipeline takes this csv file and adds the entries into the table. It adds the entries to the table. It relies insert_share() in <i>InsertData.py</i>. Beside inserting the entries into the tables, it also returns the error log. The detail of the database table can be found in the [Data folder](../Data).

## Next Step
The next step is to train the baseline model with approach 1, you may find more detail in the [Baseline Model folder](../BaselineModel)
