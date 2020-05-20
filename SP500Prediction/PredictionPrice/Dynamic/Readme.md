# Dynamic Folder - Prototype Stock Price Predictive Model
This folder consists of code of prototype stock price predictive model. 

## Approach
In my <a href="https://medium.com/datadriveninvestor/predict-stock-price-with-time-series-statistical-learning-fec97560439e">Medium Post - Predict Stock Prices with Time-Series Statistical Learning</a>, I have discussed that we cannot use the same algorithm and hyperparameters for the stock price predictive model for all stocks. Each predictive model must be tail-made for each stock. I have concluded that it is necessary to conduct a grid search to find the algorithm and hyperparameters used for the best stock price predictive model for each stock. Each stock will be trained with adaptive model and Holt-winters method with different time interval.
<br><br>
Here is the time interval used for training data set for each stock:
<ul>
	<li>1997-2018</li>
	<li>2000-2018</li>
	<li>2005-2018</li>
	<li>2007-2018</li>
	<li>2010-2018</li>
	<li>2011-2018</li>
	<li>2012-2018</li>
	<li>2013-2018</li>
	<li>2014-2018</li>
	<li>2015-2018</li>
	<li>2016-2018</li>
	<li>2017-2018</li>
</ul>
After the best model is found for each stock, the program will predict the stock price and insert the those stock price to the local database for calculating S&P 500 in the next step.

## Prototype Stock Price Predictive Model
<i>Prediction_Dynamic_StockPrice_50.py</i> is the code for Prototype Stock Price Predictive Model. The program first obtain the list of S&P 500 components and the program will enter a for loop to loop through each stock component. In each stock, the program conduct grid search to train models with different interval for either algorithm (Adaptive model and Holt-winters method) using Facebook Prophet and ExponentialSmoothing() from statsmodels.tsa.holtwinters. Each model is evaluated accuracy with R-square with testing data. The program will save the predict stock prices in the evaluation phase until the best model is determined. The program determine the best model with the highest R-square, then save the predicted stock prices to the local database for next step to calculate S&P 500. Note that, the program does not guarantee the best model achieves positive R-square. The stock price predicted with a positive predictive model will be saved in the <i>pred_dy_staging_sp500_good</i> table, while  the stock price predicted with a negative predictive model will be saved in the <i>pred_dy_staging_sp500_bad</i> table. Due to time, I have split this task into 10 files. Each file is responsible for 50 stocks (While the last one handles 5 more stocks). <i>Prediction_Dynamic_StockPrice_50.py</i> is the template code; other files is identical except the SQL query. The program also returns error log and timer log which keep track the time used for each stock.