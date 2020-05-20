# Prediction - Stock Price Aggregation Model
The Stock Price Aggregation Model takes the nature of index calculation of S&P 500, it predicts the stock price of all S&P 500 components and calculate the S&P 500 using all predicted stock price. This approach consists 4 parts - Data Acquisition, Stock Price Prediction, Index Calculation, and Evaluation. In this part, the goal is to build a prototype S&P 500 predictive model.

## Files
This folder consists of the following files:
<ul>
	<li>Prediction_AggStockPrice_Template.py - For Index Calculation</li>
	<li>Prediction_AggStockPrice_Base.py - For Index Calculation</li>
	<li>Evaluation_sp500.py - For Evaluation</li>
</ul>

## Data Acquisition
In this approach, the first part is Data Acquisition which obtain stock price for model training, and index meta data, including stock floating shares and divisors. All the data is obtained from Yahoo Finance and Y Chart, and stored in the local database. To find more detail about this pipelines, you may check out in the [ETL Pipelines folder](../ETLPipelines). To find more detail of the tables in the database, you may check out in the [Data folder](../Data). Or if you you would like to see the SQL queries related to this project, you may check out in the [SQL query folder](../SQLQuery).

## Stock Price Prediction
After the data is obtained, the next phase is to predict all stock price of the component stocks. Each stock price predictive model of each stock is trained with different algorithms and hyperparameters. Each stock price predictive model is trained with adaptive model or Holt-winters method. You may find more details in the [Prediction Price folder](../PredictionPrice). If you wish to find the detail of stock price predictive model built for the prototype S&P 500 predictive model, you may check out the [Dynamic folder](../PredictionPrice/Dynamic) in the Prediction Price folder. The stock price predictive model predict the stock price and store in the local relational database.
<br><br>
In the database, there are 2 tables storing predicted stock price: <i>pred_dy_staging_sp500_good </i> and <i>pred_dy_staging_sp500_bad</i>. Each table stored the stock price from stock price predictive model of each stock. Our model is not able to gurantee high accuracy of stock price predictive model of each stock. The stock price returned from the best predictive models with positive R-square, the predicted stock price would be stored in the <i>pred_dy_staging_sp500_good </i> table; alternatively, the predicted stock price would be stored in the <i>pred_dy_staging_sp500_bad</i> table. For example, the best predictive model of Apple achieved 45% R-Square. The predicted stock price of Apple will be stored in the <i>pred_dy_staging_sp500_good </i> table. In contrast, the best predictive model of General Electrics only gives negative R-square accuracy. The predicted stock price of GE will be stored in the <i>pred_dy_staging_sp500_bad</i> table. The reason we separate the predicted stock price is to be convenient to distinguish the data quality in the next phase of Index Calculation.

## Index Calculation
Coming Soon...

## Evaluation
Coming Soon...