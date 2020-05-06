# Simple Stock Price Dashboard
There are a lot of stock price dashboards in the market but most of those are not suiting my needs. In this part, I am going to develop tail-make a dashbaord for stock analysis. The first dashboard is aimed to develop a dashboard to analyze stocks with fundamental and basic technical analysis. 

## Background
Besides only looking at the fundamentals and technical analysis of a single stock, it is helpful to compare the stock price trend with some benchmark index to understand whether the stock is outperform or underperform in the stock market. However, there are no a lot of tools out aimed to compare the growth trend between stock price and index in my desired format. Therefore, I would like to develop a dashboard to serve my goals for stock price analysis.

## Goal
To develop a dashboard to serve the following goals:
1. Display the trend of stock price, basic statistics of a stock selected by user.
2. Display the trend of growth rate of selected stocks along with the trend of growth rate index for comparsion.

## Data
There are two required data in this dashboard:
<ul>
	<li>List of companies included in the given indexes</li>
	<li>Infomation and Statistics of Stock Price and Index</li>
</ul>
The list of companies included in given indexes are obtained from Wikipedia and saved in csv files in the [Data folder](Data), each file is named in XXXXStockList.csv while XXXX represents the index of a given stock market. Each file contains the list of companies included in the index along with the ticker. The infomation and statistics of stock price and index would be obtained from Yahoo Finance on-demand. In each user's action, the program requests the required infomation and statistic of the selected stock and/or index from yfinance API (Which is an API for Yahoo Finance). yfinance requires a stock/index ticker to request the infomation and statistic of stock/index. The reason of not using Quandl is the data of US stocks and Global indexes are not free while Yahoo Finance is free. If there is other access to the data of stock price or index, it is okay to replace with yfinance.

## Tools
The dashboard is built with Python and Dash. It relies on the following packages:
<ul>
	<li>pandas - Data manipulation</li>
	<li>re - Regex in Python</li>
	<li>datetime - For date format</li>
	<li>plotly - Build visualizations on the dashboard</li>
	<li>dash, dash_core_components, dash_html_components, dash.dependencies - Dashboard tools built with Dash</li>
	<li>yfinance - API for stock price or index</li>
</ul>

## Strategy
The dashboard would be built with 2 tabs to serve the purposes of each goal. Tab 1 would be serving the first goal to display the price and statistics of 1 stock, while Tab 2 would be sering the second goal to compare index growth and selected stock(s) price growth.
<br><br>
On Tab 1, there are a text box for user to enter a stock ticker. Once the user hits the submit button next to it, the program would convert the format which yfinance accepts and request the price and statistic of such stock from yfinance. After the data is obtained, the program would display the company name, ticker, price, price change and percentage of the price change on the top. Then, it would generate a candlestick graph of stock price along with moving averages on the bottom right of the dashboard. Lastly, it would generate a table of statistics of the stock, such as PE ratio, EPS, on the bottom left of the dashboard.
<br><br>
On Tab 2, there are two dropdown lists for user to select. The first dropdown list is for user to select a index; the second dropdown list is for users to select multiple stocks within the index selected in the first dropdown list for comparsion. Once the users has selected a index and a list of stocks, the program would obtain the ticker from the csv files and request the index and the stock price. Then, the program would convert the data to growth rate and display on the dashboard.

## Design
The tabs are designed with HTML format like the following:
<br>
<img src='Images/tab1_structure.png'>
<br><br>
<img src='Images/tab2_structure.png'>
<br><br>
Once it is built in Dash, the default setting looks like the following:
<br>
<img src='Images/tab1_default.png'>
<br>
<br>
<img src='Images/tab2_default.png'>
<br><br>
But once a stock is selected in Tab 1, it would look like this:
<br>
<img src='Images/tab1_selected.png'>

## Files
There are 2 python files:
<ul>
	<li>SimpleDashboard.py - The Driver program.</li>
	<li>Layout.py - The helper code to define layout and generate visualization and Html tables.</li>
</ul>
<br><br>
In the [Data Folder](Data), there are csv files to store the list of companies within a given index. Currently, there are 2 indexes available:
<ul>
	<li>Hong Kong: Heng Seng Index</li>
	<li>United States: S&P 500</li>
</ul>

## Tab 1 - Stock Price

## Tab 2 - Comparsion between the Growth of Stock Price and Index


## Direction
Coming Soon...

## Gallery
Coming Soon...