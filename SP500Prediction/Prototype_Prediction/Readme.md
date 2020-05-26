# Prototype Prediction Model
The prototype prediction model is the final version of the proof-of-concept model. This model is similiar to the model in the model training phase but there are some adjustment to the model. These are the adjustment to the prototype prediction model:
<ul>
	<li>Stock Price Predictive models are only trained with adaptive model (Facebook Prophet)</li>
	<li>Stock Price Predictive models are now able to predict beyond May 2020</li>
	<li>Evaluation phase is taken out, replaced by Visualization</li>
	<li>Dashboard is built to visualize the prediction</li>
</ul>
<br>

## Background
The goal of Prototype Prediction Model is to predict the S&P 500 in the future 6 months. It consists of 505 predictive models to predict stock price of all S&P 500 components, and use all predicted stock price to calculate the future S&P 500.

## Files
There are ... files in ... sub-folders in this folder:
<ul>
	<li>Prototype_PredictionPrice_template.py - In the Prototype Stock Price Prediction folder</li>
	<li>Prototype_PredictionIndex.py - In the Prototype Index Calculation folder</li>
	<li></li>
</ul>

## Data Acquisition
The stock price is obtained from Yahoo Finance via yfinance like in the model training phase. The pipelines are the same in the model training phase. First, set up a local database. If the database is set up in the model training phase, the prototype prediction model may use the same tables to store the data (stock price, stock shares outstanding, S&P 500 divisor) in the <i>stockprice</i>, <i>stockmeta</i>, <i>stockshareoutstanding</i> and <i>divisor</i>tables. The data may ingest using the codes in the [ETL Pipeline folder](../ETLPipelines). The following files are the code to use:
<ul>
	<li>IngestSP500CompanyPrice_init.py</li>
	<li>IngestSP500Divisor.py</li>
	<li>IngestSP500ShareOutstanding_init.py</li>
	<li>IngestSP500ShareOutstanding_forerrors.py</li>
	<li>InsertData.py</li>
</ul>

## Stock Price Prediction
The stock price prediction phase is to use historical stock price data to train a stock price predictive model for each stock of the S&P 500 components. Each stock price predictive model is train with adaptive model (Facebook Prophet) only, while each model is trained with training data between different start year and 2018. We have found that the accuracy is different for every stock if we train the predictive model with different start year, so each stock would conduct a grid search on different start years. We drop out Holt-winters method because the accuracy of models trained with Holt-winters are not opitimal and save time. After the model is trained, the stock price between 2018 and May 2020 will be evaluated, the model with the highest R-square will be selected for the stock price predictive model for that stock. In this phase, the prototype prediction model would build 505 predictive models, which would be used in the Index Calculation phase. The file <i>Prototype_PredictionPrice_template.py</i> in the <i>Prototype_PredictionPrice</i> folder demostrates how to train the model for each stock and make prediction. You may find the detail in the [Prototype Stock Price Prediction folder](Prototype_PredictionPrice) to find more detail. The stock price predictions will be stored in the local database in the <i>pred_proto_staging</i> table and the accuracy result will be stored in the <i>pred_proto_trainresult</i>.

## Index Calculation
The Index Calculation phase is to use the predicted stock price in the Stock Price Prediction phase to calculate future S&P 500. In this phase, the model would obtain predicted stock price to calculate the market capitalization for each stock. The future S&P 500 would be calculated dividing the summation of all daily market capitalization of each stock by the S&P 500 divisor. The file <i>Prototype_PredictionIndex.py</i> in the <i>Prototype_CalculateIndex</i> will demostrates how to calculate the future S&P 500. You may find the detail in the [Prototype Index Calculation folder](Prototype_CalculateIndex). The predicted S&P 500 will be stored in the local database in the <i>pred_proto_sp500</i> table.


## Visualization
The predicted S&P 500 is displayed on a dashboard, which its code and images can be found in the [Dashboard folder](Dashboard). Beside visualizating the predicted S&P 500 between May and December 2020, the dashboard also displayed the predicted growth of stock price of your choice(s) in compare to the growth of S&P 500 between May and December 2020. 

## Suggested Adjustment to Production Model
There are two tasks to be completed if this model is deployed for production:
<ul>
	<li>Improve the accuracy of stock price predictive model of each stock.</li>
	<li>Update the Stock price predictive model daily.</li>
</ul>
More explantation is coming soon...

## Next Part
You may click [here](../) to go back to the front page of the Prediction on S&P 500 project, or go to the [(Coming Soon)](/) for the next part.
