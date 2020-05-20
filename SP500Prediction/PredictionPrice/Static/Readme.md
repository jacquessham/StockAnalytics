# Static Folder - Stock Price Predictive Models for Experiment
This folder consists of codes to predict stock price for experiment for building prototype model. The code in this folder did not used in the prototype predictive model. 

## Approach
There are 3 different time-series statistical learning can be used for predicting stock price: Adaptive model, Box-Jerkins method, and Holt-winters method. I conducted an experiement of predicting stock price with Box-Jerkins method but resulted in poor accuarcy and very time-consuimg. Also, I have found out that the accuracy can be varied with different time interval of training data using adaptive model. We will conduct another experiments on predicting stock price with different time intervals with adaptive model and Holt-winters method.

## Prediction using Adaptive model
The following files are conducting predicting stock price with different time intervals with adaptive model:
<ul>
	<li>Prediction_StockPrice.py - Train with stock price between 1997 and 2018</li>
	<li>Prediction_StockPrice_Decade.py - Train with stock price between 2010 and 2018</li>
	<li>Prediction_StockPrice_5yr.py - Train with stock price between 2013 and 2018</li>
	<li>Prediction_StockPrice_2yr.py - Train with stock price between 2016 and 2018</li>
</ul>
All the above files are the same, except each file has different SQL query to obtain training data set. Each file has its own SQL query to receive training data set first, then, the program obtain testing data set of stock price between 2019 and May 2020. After that, it will enter a for loop to loop through all stock and build a stock price predictive model with the training data set using Facebook Prophet. Once the predictive model is built, it will predict the stock price between 2019 and May 2020 and insert into the local database. All the files relies on insert_pred() from <i>Insert_Data.py</i> to insert data to the local database. The programs also produces error log and timer log which keeps track on the time used for each stock. In these program, only 1 predictive model is built for each stock in each program. The predicted data is used for experiments but did not used for prototype predictive model.

## Prediction using Holt-winters Method
<i>Prediction_holtwinters.py</i> is an experimental code to look at the accuracy of stock price predictive model of one given stock. The program query stock price for training and test data set first, and build predictive model using Holt-winters method, which uses ExponentialSmoothing() from the <i>statsmodels.tsa.holtwinters</i> package. At last, the program calculate R-square of the predictive model. The program only prints the R-square.
<br><br>
The program uses General Electrics (GE) as the example but you may change other stock by entering different ticker in the SQL queries.