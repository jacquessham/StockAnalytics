# Database Tables
The data comes from Yahoo Finance via yfinance. The data stores in a relational database (Postgre SQL) in local machine. The following tables I have created for storing the data:
<ul>
	<li>stockprice - Table for daily stock price and volume</li>
	<li>stockmeta - Table for meta data of stock</li>
	<li>stockshareoutstanding - Table for numbers of oustanding shares each stock</li>
	<li>sp500_divisor - Table for S&P 500 Divisor</li>
	<li>pred_dy_staging_sp500_good - Table for Stock price obtained from Predictive Model with Positive R-square</li>
	<li>pred_dy_staging_sp500_bad - Table for Stock price obtained from Predictive Model with Negative R-square</li>
	<li>pred_dy_trainresult - Table for R-square and results from Predicitve model of each stock</li>
</ul>
<br>
All tables are stored in <i>stock</i> Schema.

## Tables for Model Training Phase
### stockprice (Table)
The <i>stockprice</i> table stored the daily stock price or index from Yahoo Finance. The columns consist of:
<ul>
	<li><b>ticker</b> (varchar(10)): The ticker of the stock</li>
	<li><b>tradedate</b> (timestamp): The date of transaction of given stock</li>
	<li><b>openprice</b> (float): The opening price</li>
	<li><b>high</b> (float): The daily high price</li>
	<li><b>low</b> (float): The daily low price</li>
	<li><b>closeprice</b> (float): The closing price</li>
	<li><b>volume</b> (bigint): Volume trade on the given date, no scaling</li>
</ul>
<br>
The data in this table are obtained from Yahoo Finance by <i>IngestSP500_init.py</i> and <i>IngestSP500CompanyPrice_init.py</i>. Please find more detail about the pipeline in the [ETL Pipelines folder](ETLPipelines).

### stockmeta (Table)
The <i>stockmeta</i> table stored the meta data of stocks. The columns consist of:
<ul>
	<li><b>ticker</b> (varchar(10)): The ticker of the stock</li>
	<li><b>companyname</b> (varchar(255)): The company name of the stock</li>
	<li><b>gicssector</b> (varchar(100)): The sector the stock belongs to</li>
	<li><b>gicssubindustry</b> (varchar(255)): The subindustry the stock belongs to</li>
	<li><b>countrystockmarket</b> (varchar(50)): Country where the stock is traded</li>
	<li><b>indexcomponent</b> (varchar(50)): The index which the stock is the component of</li>
</ul>
The data in this table are obtained from <a href="https://en.wikipedia.org/wiki/List_of_S%26P_500_companies">Wikipedia</a> by <i>IngestSP500CompanyPrice_init.py</i>. Please find more detail about the pipeline in the [ETL Pipelines folder](ETLPipelines).

### stockshareoutstanding (Table)
The <i>stockshareoutstanding</i> table stored the number of floating shares each stock available in the stock market. The columns consist of:
<ul>
	<li><b>ticker</b> (varchar(10)): The ticker of the stock</li>
	<li><b>shareoutstanding</b> (bigint): The number of floating shares available</li>
</ul>
<br>
The data in this table are obtained from Yahoo Finance by <i>IngestSP500ShareOutstanding_init.py</i> and <i>IngestSP500ShareOutstanding_forerrors.py</i>. Please find more detail about the pipeline in the [ETL Pipelines folder](ETLPipelines).

### sp500_divisor (Table)
The <i>sp500_divisor</i> table stored the S&P 500 divisor for S&P 500 calculation. The columns consist of:
<ul>
	<li><b>tradedate</b> (timestamp): The date of transaction of the index</li>
	<li><b>divisor</b> (bigint): The divisor of the given date (No Adjustment)</li>
</ul>
The data in this table is obtained from <a href="https://ycharts.com/indicators/sp_500_divisor">Y Charts</a> by <i>IngestSP500Divisor.py</i>. Please find more detail about the pipeline in the [ETL Pipelines folder](ETLPipelines).

### pred_dy_staging_sp500_good (Table)
The <i>pred_dy_staging_sp500_good</i> stored the predicted stock price from the predictive models with positive R-square. The columns consist of:
<ul>
	<li><b>ticker</b> (varchar(10)): The ticker of the stock</li>
	<li><b>tradedate</b> (timestamp): The date of transaction of given stock</li>
	<li><b>closeprice</b> (float): The predicted closing price of the given stock on the given date</li>
</ul>

### pred_dy_staging_sp500_bad (Table)
The <i>pred_dy_staging_sp500_good</i> stored the predicted stock price from the predictive models with negative R-square. The columns consist of:
<ul>
	<li><b>ticker</b> (varchar(10)): The ticker of the stock</li>
	<li><b>tradedate</b> (timestamp): The date of transaction of given stock</li>
	<li><b>closeprice</b> (float): The predicted closing price of the given stock on the given date</li>
</ul>

### pred_dy_trainresult (Table)
The <i>pred_dy_trainresult</i> stored the accuracy and meta data of what package and time interval of stock price used in the best model for each stock through the model training phase. The columns consist of:
<ul>
	<li><b>ticker</b> (varchar(10)): The ticker of the stock</li>
	<li><b>rsquare</b> (float): The R-square of the best predictive model for the given stock</li>
	<li><b>start_year</b> (int): The starting year of the time interval for the training data set</li>
	<li><b>package</b> (varchar(10)): The package used for the best predictive model, in other word, it tells you which algorithm used</li>
</ul>

## Tables Used in Model Training Phase for Experimental Purpose
The following Tables was built but did not used for model training phase. 
<ul>
	<li>pred_fbp_price_sp500_base - Table for Predicted price trained with stock price between 1997 and 2018 using Facebook Prophet </li>
	<li>pred_fbp_price_sp500_10yr - Table for Predicted price trained with stock price between 2010 and 2018 using Facebook Prophet</li>
	<li>pred_fbp_price_sp500_5yr - Table for Predicted price trained with stock price between 2013 and 2018 using Facebook Prophet</li>
	<li>pred_fbp_price_sp500_2yr - Table for Predicted price trained with stock price between 2016 and 2018 using Facebook Prophet</li>
</ul>


### pred_price_sp500base (Table)
The <i>pred_price_sp500base</i> table stored the prediction made in Approach 2. The columns consists
<ul>
	<li><b>ticker</b> (varchar(10)): The ticker of the stock</li>
	<li><b>tradedate</b> (timestamp): The date of transaction of given stock</li>
	<li><b>closeprice</b> (float): The predicted closing price of the given stock on the given date</li>
</ul>
The data in this table are obtained in Approach 2 with the following program:
<ul>
	<li>Prediction_StockPrice.py</li>
	<li></li>
</ul>

## Tables Used for the Prototype Predictive Model
Coming Soon...

## ETL Pipelines
You may learn more how the data is ingested into the database in the [ETL Pipelines folder](../ETLPipelines). 