# Prediction - Stock Price Aggregation Model
The Stock Price Aggregation Model takes the nature of index calculation of S&P 500, it predicts the stock price of all S&P 500 components and calculate the S&P 500 using all predicted stock price. This approach consists 4 parts - Data Acquisition, Stock Price Prediction, Index Calculation, and Evaluation. In this part, the goal is to build a prototype S&P 500 predictive model. 

## Files
This folder consists of the following files:
<ul>
	<li>Prediction_AggStockPrice_Template.py - For Index Calculation</li>
	<li>Prediction_AggStockPrice_Base.py - For Index Calculation</li>
	<li>Evaluation_sp500.py - For Evaluation</li>
</ul>

## Assumption and Constraint
Our approach is to predict stock price and calculate the index with the predicted stock price. In our model, we only calculate the index with stock components in May 2020, we do not take account of changes of S&P 500 components. All the events related to stock components change will be ignored (In 2019 and 2020, there were about 20 events related to stock components). 
<br><br>
One of the constraints of this approach is lack of access to accurate floating shares and divisors; in the model, we calculate market capitalization with the floating shares of all stocks in May 2020 from Yahoo Finance and quarterly divisor from Y-Chart. Therefore, the predicted S&P 500 index is going to be not accurated that we shall calculate the testing data set with real stock price to evaluate with the prediction.

## Data Acquisition
In this approach, the first part is Data Acquisition which obtain stock price for model training, and index meta data, including stock floating shares and divisors. All the data is obtained from Yahoo Finance and Y Chart, and stored in the local database. To find more detail about this pipelines, you may check out in the [ETL Pipelines folder](../ETLPipelines). To find more detail of the tables in the database, you may check out in the [Data folder](../Data). Or if you you would like to see the SQL queries related to this project, you may check out in the [SQL query folder](../SQLQuery).

## Stock Price Prediction
After the data is obtained, the next phase is to predict all stock price of the component stocks. Each stock price predictive model of each stock is trained with different algorithms and hyperparameters. Each stock price predictive model is trained with adaptive model or Holt-winters method. You may find more details in the [Prediction Price folder](../PredictionPrice). If you wish to find the detail of stock price predictive model built for the prototype S&P 500 predictive model, you may check out the [Dynamic folder](../PredictionPrice/Dynamic) in the Prediction Price folder. The stock price predictive model predict the stock price and store in the local relational database.
<br><br>
In the database, there are 2 tables storing predicted stock price: <i>pred_dy_staging_sp500_good </i> and <i>pred_dy_staging_sp500_bad</i>. Each table stored the stock price from stock price predictive model of each stock. Our model is not able to gurantee high accuracy of stock price predictive model of each stock. The stock price returned from the best predictive models with positive R-square, the predicted stock price would be stored in the <i>pred_dy_staging_sp500_good </i> table; alternatively, the predicted stock price would be stored in the <i>pred_dy_staging_sp500_bad</i> table. For example, the best predictive model of Apple achieved 79% R-Square. The predicted stock price of Apple will be stored in the <i>pred_dy_staging_sp500_good </i> table. In contrast, the best predictive model of General Electrics only gives negative R-square accuracy. The predicted stock price of GE will be stored in the <i>pred_dy_staging_sp500_bad</i> table. The reason we separate the predicted stock price is to be convenient to distinguish the data quality in the next phase of Index Calculation.
<br><br>
In the current algorithm, there are 226 stocks have a positive R-square stock price predicted model, while 271 stocks have a negative R-square stock price predicted model and 8 stocks were failed to build a stock price predictive model.
<br><br>
I have a Medium Post about building stock price predictive model, you may learn more about it in that <a href="https://medium.com/datadriveninvestor/predict-stock-price-with-time-series-statistical-learning-fec97560439e">post</a>.

## Index Calculation
After predicting stock price, the predicted stock prices are used to calculate the index with the S&P 500 formula. First, we retrieve all the predicted stock price and the number of floating shares of each stock in the database and calculate market capitalization by multiplying the daily predicted stock price with number of floating shares of each stock. Then, we sum all daily market capitalization from each stock. After dividing the summation with divisor, we would get the predicted daily index.
<br><br>
Since the stock price predictive models did not guarantee to have high quality of prediction, I have a modified version to calculate the index: Calculate the index with predicted stock price from predictive model with positive R-square and real stock price if the stock price predictive models have negative stock price. This modified version of predicted index is to eliminate the negative effects on poor-quality predicted stock price. This modified version shall be used for evaluation, not final production.
<br><br>
<i>Prediction_AggStockPrice_Template.py</i> is the template how to calculate the index from predicted stock price. <i>Prediction_AggStockPrice_Base.py</i> is the file to calculate the index and save the result in the database.
<br><br>
There are about 8 stocks that we failed to build a stock price predictive model. Since those stocks are very light-weighted and have minimal influence on S&P 500, the calculation would ignore the market capitalization in the summation in this model.

## Evaluation
The goal of evaluation phase is to evaluate the accuracy of the predicted index. Due to the constraint of the prediction accuracy, there are 2 approaches to evaluate:
<ul>
	<li>Compare with the index calculated with real stock price (Testing Data)</li>
	<li>Compare with the index in real world (Real Data)</li>
</ul>
<br>
As mentioned, the accuracy of the index prediction is off with the real world index due to lack of access to accurate data for index calculation. We need to evaluate the predicted index with testing data and real world data for evaluation.
<br><br>
The first evaluation is evaluating the predictive index with testing data. The advantage of this evaluation is to eliminate the effect of inaccurated data on index calculation that we can look at the accuracy of using this approach of predicting S&P 500. The first evaluation is done for concept-proofing. The second evaluation is done for the evaluated whether the model is useful for production.
<br><br>
The file <i>Prediction_AggStockPrice_Base.py</i> prepares predicted index, modified predicted index, and testing data and store in the local database. After all data is stored in the database, <i>Evaluation_sp500.py</i> is used to calculate the R-square.
<br><br>
The accuracy of Predicted S&P 500 are
<ul>
	<li>Testing Data: 23.94%</li>
	<li>Real World Data: 7.84%</li>
</ul>

## Next Step
After the model training phase is over, the next step is to build a prototype predictive model. You may learn more about the prototype predictive model in the [Prototype Predictive Model folder](../Prototype_Prediction).
