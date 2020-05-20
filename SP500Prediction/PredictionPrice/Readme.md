# Stock Price Prediction
The stock price prediction is the first step of Stock Price Aggregation Model. In this approach, the model predicts the stock prices of all S&P 500 components and calculate the S&P 500 for prediction. In this folder, it consists of all codes that lead to the prototype models.

## Files and Folders
This folder consists of the following files and folders:
<ul>
	<li>Dynamic - Consists the of the model to make stock price prediction for the prototype model</li>
	<li>Static - Consists of codes to make stock price based on different condition</li>
	<li>Prediction_arima.py - Template to predict stock price with Box-Jerkins method</li>
	<li>HeavyPrediction_try.py - Template to find the best predictive model of one stock among adaptive models with different time interval and Holt-winters method</li>
	<li>Evaluation_StockPrice.py - Code evaluate accuracy between predicted stock price and real stock price</li>
</ul>

## Files in this Folder
<i>Prediction_arima.py</i> and <i>HeavyPrediction_try.py</i> are the templates to build predictive models either with Box-Jerkins method and with both adaptive model and Holt-winters method.
<br><br>
<i>Prediction_arima.py</i> relies on auto_arima() from the <i>pmdarima</i> package to find the best hyperparameters of ARIMA model. This file demostrate how to build a predictive model with the Box-Jerkins method with the Apple stock price between 1997 and 2018 and evaluate the accuracy by comparing with Apple stock price between 2019 and May 2020.
<br><br>
<i>HeavyPrediction_try.py</i> is a dynamic grid search model to find the best predictive model between adaptative model and Holt-winters method with different hyperparameters. This file demostrate how to select the best model based on the accuracy by comparing for the top 20 heavy-weighted S&P 500 components. The code selects the model with the highest R-square for each stock. 
<br><br>
Both files are code for experiment to make predictive models for making prototype model.
<br><br>
<i>Evaluation_StockPrice.py</i> is the code evaluate accuracy between predicted stock price and real stock price on ad-hoc basis. It did not used in the prototype predictive model.


## Static Folder
The static folder consists of codes to make stock price prediction with fixed time interval. The code in this folder are experimental code to make predictive models for making prototype model. You may find the codes in the [Static Folder](Static).

## Dynamic Folder
The Dynamic folder consists of code to make stock price prediction for all stock price in the prototype model. The stock price predictive model conducts grid search different time interval and algorithms to build stock price predictive model for each stock. You may find the code in the [Dynamic Folder](Dynamic)
