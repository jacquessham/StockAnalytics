# Prediction on S&P 500
S&P 500 is a benchmark index in the United States and it is a significant stock market indicator to the US stock market. It is very worth to understand the trend and seasonality of the S&P 500, for stock and future index investing. In this part of the project, we are going to build a model to predict the S&P 500 in the future 12 months.

## Background on S&P 500
Coming Soon...

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

## Packages Used
<ul>
	<li>pandas</li>
	<li>numpy</li>
	<li>psycopg2</li>
	<li>fbprophet</li>
	<li>yfinance</li>
</ul>

## Training and Testing Data
The training data is set the data between 1997 and 2018 to include at least 2 bull markets before recessions. In between 1997 and 2018, there are 2 recessions in the US: Dot Com buddle and 2008 Credit crisis. 1997 is the start of the bull market before the Dot Com buddle, and therefore, the training data starts here. The testing data is set the date between 2019 and May, 2020. 

## Files
There are ...... code in this folder...
<ul>
	<li>Prediction_Basemodel.py</li>
	<li></li>
	<li></li>
	<li></li>
</ul>

## Approach 1 - Times-series only Model
The first approach is to train a time-series model with Prophet. The baseline model is simply training an additive model with Facebook Prophet. In the <i>Prediction_Basemodel.py</i> file, the program first obtain data from the local database with the index between 1997 and 2018 for training data set, and index between 2019 and May, 2020 for testing data set. Then, use the training data set to train the time-series model with Prophet. This model will be called the <b>baseline model</b>. After that, obtain the RMSE with testing data set.
<br>
<br>
There are two modification on the baseline model. The first modification is to take natural log on the index before model training and take an exponential after the prediction is made. This model will be called <b>Times Series Log Prediction Model</b>. Another modification is to convert the index to growth rate and let the growth rate be the response variable for model training. After the model predict the growth rate, calculate the index by scaling the growth with the index of the first prediction period. This model will be called <b>Time Series Growth Prediction Model</b>.
<br>
<br>
The file <i>Prediction_Basemodel.py</i> trained those 3 models and calculate the R-squared and RMSE of each model. It relies the function save_result_rmse() from <i>Results.py</i> to save the results in text files. The result is saved as (Model Name).txt format in the Results folder.
<br>
<br>
The results are:
<ul>
	<li><b>Baseline Model</b> - R-squared: 10.69%    RMSE: 198.32</li>
	<li><b>Times Series Log Prediction Model</b> - R-squared: 3.8%    RMSE: 205.83</li>
	<li><b>Time Series Growth Prediction Model</b> - R-squared: Negative   RMSE: 387.51</li>
</ul>
<br>
The baseline model has the highest R-squared or lowest RMSE, both modificated model did not perform better than the baseline model. As the result, the baseline model is the best model among three models.


## Approach 2 - Stock Price Aggregation Model
Coming Soon...

## Approach 3 - Linear Regression Model
Coming Soon...

## Approach 4 - Emotion Model
Coming Soon...