import pandas as pd
import psycopg2
import dash
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State


# Connect to database
conn = psycopg2.connect(host='localhost', port=5432, database='postgres')

##### Dashboard layout #####
# Dash Set up
app = dash.Dash()

# Obtain the dropdown list
query = """ select ticker, companyname 
			from stock.stockmeta
			where indexcomponent = 'S&P 500'
			order by 2; """
shares_list = pd.io.sql.read_sql(query, conn)
shares_list['display'] = shares_list['ticker'] + '\t' + \
                         shares_list['companyname']

company_choice = [{'label': row['display'], 'value': row['ticker']}
                  for index, row in shares_list.iterrows()]

# Plot Graph on Tab 1
def get_sp500():
	query_train = """select tradedate, closeprice as sp500
					 from stock.stockprice 
					 where ticker='^GSPC' and 
					 date_part('year', tradedate) >= 2019
					 order by 1; """

	query_pred = """select tradedate, sp500_pred
					from stock.pred_proto_sp500 
					where date_part('year', tradedate) >= 2019
					order by 1; """
	
	df_train = pd.io.sql.read_sql(query_train, conn)
	df_pred = pd.io.sql.read_sql(query_pred, conn)

	data = []

	# Add real world data
	data.append(go.Scatter(x=df_train['tradedate'], y=df_train['sp500'],
		                   name='S&P 500', line={'color':'royalblue'}))
	# Add prediction data
	data.append(go.Scatter(x=df_pred['tradedate'], y=df_pred['sp500_pred'],
		                   name='Prediction', 
		                   line={'color': 'orange'}))
	# Layout for the visualization
	layout = {'xaxis':{'title':'Date','rangeslider':{'visible':False}},
			  'yaxis':{'title':'Index'},
	          'hovermode':False}
	return {'data':data, 'layout':layout}


# Base Layout
app.layout = html.Div([
	dcc.Tabs(id='dashboard-tabs', value='sp500-only', children=[
		dcc.Tab(label='S&P 500 Prediction', value='sp500-only', children=[
			html.Div([
				html.Br(),
				html.H2('S&P 500 Prediction', 
					    style={'width':'70%', 'text-align':'center',
				               'margin':'auto'}), # Position 0, title
				dcc.Graph(id='sp500-vis', figure=get_sp500()) 
				# Position 1, visualization
				]) # Close Div
			]), # 1st Tab
		dcc.Tab(label='S&P 500 Stocks Growth', value='sp500-stocksgrowth', 
			children=[
				html.Br(),
				html.H2('Stock Future Growth vs. S&P 500 Future Growth',
				        style={'width':'70%', 'text-align':'center',
				               'margin':'auto'}), # Position 0, title
				html.Br(),
				html.Div([
					dcc.Dropdown(id='tab2-dropdown',
						         options=company_choice,
						         value=[],
						         multi=True,
						         style={}
					)], style={'width':'50%'}),
				dcc.Graph(id='sp500-stocksgrowth-vis') 
				# Position 2, visualization
			]) # 2nd Tab
		]) # Close Tabs
	], style={'width':'70%', 'margin':'auto'}) # Close Base Div

@app.callback(Output('sp500-stocksgrowth-vis','figure'),
              [Input('tab2-dropdown','value')])
def generate_tab2_graph(tickers):
	query_sp500 = """
					select tradedate,
					sp500_pred/first_value(sp500_pred) 
					over(order by tradedate) -1 as growth
					from stock.pred_proto_sp500
					where tradedate > (select max(tradedate)
					from stock.stockprice)
					and date_part('dow', tradedate)
					between 1 and 5; """
	df_sp500 = pd.io.sql.read_sql(query_sp500, conn)
	data = [go.Scatter(x=df_sp500['tradedate'], y=df_sp500['growth'],
		               name='S&P 500 Growth')]

	
	for ticker in tickers:
		query_curr = """select tradedate,
						closeprice/first_value(closeprice) 
						over(order by tradedate) -1 as growth
						from stock.pred_proto_staging
						where ticker = '{}' and
						tradedate > (select max(tradedate)
						from stock.stockprice)
						and date_part('dow', tradedate)
						between 1 and 5;""".format(ticker)
		df_stock= pd.io.sql.read_sql(query_curr, conn)
		data.append(go.Scatter(x=df_stock['tradedate'],
			                   y=df_stock['growth'],
			                   line=dict(dash='dash'),
			                   name=ticker+' Growth'))
	layout = {'xaxis':{'title':'Date'}, 
		      'yaxis':{'title':'% Change', 'tickformat':'.0%'},
	          'hovermode':False}

	return {'data':data, 'layout':layout}


if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
