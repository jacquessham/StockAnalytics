import pandas as pd
import psycopg2
import plotly.graph_objs as go
from plotly.offline import plot


# Function to plot line chart
def generate_line_chart(df_train, df_pred, ticker):
	layout = {'title': {'text':'Stock Price Prediction of '+ ticker,
	                    'x': 0.5},
	          'xaxis':{'title':'Date'}, 
		      'yaxis':{'title':'Stock Price ($)'},
	          'hovermode':False, 'plot_bgcolor':'white'}
	data = []
	data.append(go.Scatter(x=df_train['tradedate'], y=df_train['closeprice'],
		                   name='Real Stock Price'))
	data.append(go.Scatter(x=df_pred['tradedate'], y=df_pred['closeprice'],
		                   name='Predicted Price of '+ticker))

	return go.Figure({'data':data, 'layout':layout})

# Connect to database
conn = psycopg2.connect(host='localhost', port=5432, database='postgres')

# Ticker
ticker = 'GE'

# Queries
query_real = """select tradedate, closeprice
                 from stock.stockprice
                 where date_part('year', tradedate) >= 2019
                 and ticker = '{}' order by tradedate""".format(ticker)

query_pred = """select tradedate, closeprice
                 from stock.pred_proto_staging
                 where date_part('year', tradedate) >= 2019
                 and date_part('dow', tradedate) between 1 and 5
                 and ticker = '{}' order by tradedate""".format(ticker)

df_train = pd.io.sql.read_sql(query_real, conn)
df_pred = pd.io.sql.read_sql(query_pred, conn)

figure = generate_line_chart(df_train, df_pred, ticker)
filepath = 'stockprice_pred_'+ticker+'.html'
figure.write_html(filepath)
