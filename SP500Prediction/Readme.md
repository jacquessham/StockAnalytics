# Prediction on S&P 500
S&P 500 is a benchmark index in the United States and it is a significant stock market indicator to the US stock market. It is very worth to understand the trend and seasonality of the S&P 500, for stock and future index investing. In this part of the project, we are going to build a model to predict the S&P 500 in the future 6 months.

## Background on S&P 500
S&P 500 is a capitalization-weighted index in the United States. This index takes the the weighted average of the top 500 market capitalization companies to reflect the average of the stock market. There 505 stock components in the S&P 500 because there is about 5 companies offers 2 class stocks. The S&P 500 is calculated by summing all market capitalization of 505 components and divided by divisor. Divisor is an adjusted market capitalization. The formula is:
<br>
<br>
<img src="https://render.githubusercontent.com/render/math?math=\huge\frac{\sum_{n=1}^{505} P_i Q_i}{Divisor}">
<br><br>
The list of stock components is obtained from <a href="https://en.wikipedia.org/wiki/List_of_S%26P_500_companies">Wikipedia</a> and saved in the [Index Components folder](../IndexComponents).
<br><br>
The top 10 weighted components in the S&P 500 order by weight:
<ol>
	<li><b>General Electric</b> (GE): 2.95%</li>
	<li><b>Bank of America</b> (BAC): 2.93%</li>
	<li><b>Microsoft</b> (MSFT): 2.56%</li>
	<li><b>AT&T</b> (T): 2.41%</li>
	<li><b>Pfizer</b> (PFE): 1.88%</li>
	<li><b>Comcast</b> (CMCSA): 1.54%</li>
	<li><b>Apple</b> (AAPL): 1.47%</li>
	<li><b>Coca-cola</b> (KO): 1.45%</li>
	<li><b>Cisco</b> (CSCO): 1.43%</li>
	<li><b>Intel</b> (INTC): 1.43%</li>
</ol>


## Strategy
There are some ideas of how the model can be built:
<ul>
	<li>Model predict index purely on time-series statistical learning</li>
	<li>Model predict index by aggregating predicted stock price of index component companies, which are predicted purely on time-series statistical learning.</li>
	<li>Model predict index by different features on linear regression</li>
	<li>Model predict index by news sentiments</li>
</ul>

## Data
The data comes from Yahoo Finance via yfinance. The data stores in a relational database (Postgre SQL) in local machine. You may find more detail on the data and the database tables in the [Data folder](Data).

## ETL Pipelines
There are pipelines to ingest data into the database. 
<br>
<br>
You may find more detail in the [ETL Pipelines folder](ETLPipelines).


## Approach 1 - Times-series only Model
The baseline model is the first approach to predict S&P 500. The baseline model is a predictive model of S&P 500 using adaptive model in time-series statistical model. This approach trains the predictive model with Facebook Prophet. The baseline model has achieved a 10.69% R-square. You may find more detail and the code in the [Baseline Model folder](BaselineModel).

## Approach 2 - Stock Price Aggregation Model
The Stock Price Aggregation Model takes the nature of index calculation of S&P 500, it predicts the stock price of all S&P 500 components and calculate the S&P 500 using all predicted stock price. This approach consists 4 parts - Data Acquisition, Stock Price Prediction, Index Calculation, and Evaluation. In this part, the goal is to build a prototype S&P 500 predictive model.
<br><br>
In this approach, the first part is Data Acquisition which obtain stock price for model training, and index meta data, including stock floating shares and divisors. To find more detail about this part, you may check out in the [ETL Pipelines folder](ETLPipelines).
<br><br>
After the data is obtained, the next phase is to predict all stock price of the component stocks. Each stock price predictive model of each stock is trained with different algorithms and hyperparameters. You may find more details in the [Prediction Price folder](PredictionPrice). If you wish to find the detail of stock price predictive model built for the prototype S&P 500 predictive model, you may check out the [Dynamic folder](PredictionPrice/Dynamic) in the Prediction Price folder. The stock price predictive model predict the stock price and store in the local relational database.
<br><br>
Once the predicted stock price is saved in the database, we can calculate the index with the predicted stock price. The next step is Index Calculation phase that the S&P 500 predictive model takes all predicted stock price and calculate the index based on the S&P 500 formula and save the predicted index in the local relational database. In the final phase, we evaluate the accuracy with testing data. You may find more detail of Index Calculation, and Evaluation phases in the [Stock Price Aggregation Model folder](Prediction_AggStockPrice).
<br><br>
The accuracy of this approach is 23% R-square.
<br><br>
After the model training phase, the prototype model is built to predict the index 6 months after May 2020. The prototype model has some adjustment to the model in the model training phase. You may find more detail of the prototype model in the [Prototype Model folder](Prototype_Prediction). You may also find the the prediction visualization and the dashboard code in the [Dashboard folder](Prototype_Prediction/Dashboard).
<br><br><br><br>
In this approach, I have written 2 Medium Post on Stock Price Prediction and the reflection of this approach. You may find the supporting detail of those post in the [Stock Price Prediction Post folder](../Post_StockPricePrediction) and the [Stock Price Aggregation Model Post folder](../Post_Prediction_AggStockPrice).

