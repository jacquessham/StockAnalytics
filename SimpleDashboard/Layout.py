import pandas as pd
from datetime import datetime
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


##### Layouts for Tab 1 #####
# Dropdown list for single stock choice
def get_tab1_info_box():
	return html.Div([
				html.Div([
					html.Div(id='tab1-stock-price',
						     style={'width':'30%','display':'inline-block',
						            'font-size':'200%'}),
					html.Div(id='tab1-stock-price-change'),
					html.Div(id='tab1-stock-price-percentchange')
					],style={'width':'30%','display': 'inline-block',
			                 'vertical-align':'top'}),
				html.Div(style={'width':'15%','display': 'inline-block'}),
				html.Div(dcc.Dropdown(id='tab1-market-dropdown',
					                  options=tab1_markets,
					                  value=tab1_markets[0]['value'],
				                      style={'text-align':'left'}),
					     style={'width':'20%','display': 'inline-block',
			            		'vertical-align':'top'}),
				html.Div(style={'width':'5%','display': 'inline-block'}),
				html.Div([
					html.Div([
						html.Div(dcc.Input(id='tab1-ticker-input',value='',
						                   type='text'),
						                   style={'display': 'inline-block'}),
						html.Div(html.Button('Submit',id='tab1-submit'),
							     style={'display': 'inline-block'})
						]),
					html.Div(id='tab1-error-message', style={'color':'red'}, children='Error Box')
					],style={'width':'30%','display': 'inline-block'})
			])

##### Layout for Tab 2 #####
# Dropdown list for index and stock growth difference
def get_tab2_info_box():
	return html.Div([
			html.Div([dcc.Dropdown(id='tab2-index-choice',
				                   options=index_choice,
				                   value=index_choice[0]['value'],
								   style={'text-align':'left'})],
				style={'width':'30%','display': 'inline-block'}),
			html.Div(style={'width':'20%','display': 'inline-block'}),
			html.Div([dcc.Dropdown(id='tab2-stock-include',
				                   options=[],
				                   value=[],
				                   multi=True,
				                   style={'text-align':'left'})],
				style={'width':'50%','display': 'inline-block'})
		])

##### Layout for both Tab 1 and Tab 2 #####
# Layout for user to select time interval
def get_interval_layout(tab):
	id_name = tab+'-time-interval'
	layout = html.Div(
		dcc.RadioItems(id=id_name,
                       options=[{'label':'1 Month', 'value':'1mo'},
                                {'label':'3 Months', 'value':'3mo'},
                                {'label':'6 Months', 'value':'6mo'},
                                {'label':'YTD', 'value':'ytd'},
                                {'label':'1 Year', 'value':'1y'},
                                {'label':'3 Years', 'value':'3y'},
                                {'label':'5 Years', 'value':'5y'}
                       ],
                       value='ytd'
		), style={'text-align':'center'})
	return layout

# Layout for graph, include time interval and graph
def get_graph_layout(tab):
	layout = html.Div([
		html.Br(),
		get_interval_layout(tab),
		dcc.Graph(id=tab+'-vis')
		])
	return layout

# Layout for table for stats
def get_table_layout(tab):
	id_name = tab+'-table'
	return html.Div([html.Br(),html.Br(),html.Table(id=id_name)])

# Layout for stats and graph
def get_stats_graph_layout(tab):
	return html.Div([
		html.Div(get_table_layout(tab),
			     style={'width':'30%','display': 'inline-block',
			            'vertical-align':'top'}),
		html.Div(get_graph_layout(tab),
			     style={'width':'70%','display': 'inline-block',
			            'vertical-align':'top'})
		])

##### Generate Plots and Tables#####
# Generate Line charts for stocks and index
def getLinePlot(df, tab):
	traces = []
	for col in df.columns:
		if col != 'Date':
			traces.append({'x':df['Date'], 'y':df[col],'name':col,
				           'mode':'lines'})
	layout = {'xaxis':{'title':'Date'},
	          'hovermode':False}
	if tab == 1:
		layout['yaxis'] = {'title':'Price ($)'}

	elif tab == 2:
		layout['yaxis'] = {'title':'% Change', 'tickformat':'.0%'}
	return {'data':traces, 'layout':layout}

# Generate candlestick
def getCandlestick(df):
	data = []
	data.append(go.Candlestick(x=df['Date'], open=df['Open'],
		                       high=df['High'], low=df['Low'],
		                       close=df['Close']))
	layout = {'xaxis':{'title':'Date','rangeslider':{'visible':False}},
			  'yaxis':{'title':'Price ($)'},
	          'hovermode':False}
	return {'data':data, 'layout':layout}

# Generate Table for Tab 1 - Stock Stats
def getTab1Table(df, stock_info):
	last_day = df.iloc[-1,1:6]
	# Format the day range of price
	low_day = last_day['Low']
	high_day = last_day['High']
	range_day = f'{low_day:,.2f}'+' - '+f'{high_day:,.2f}'
	# Obtain and format 52 weeks range of price
	low_52weeks = df['Low'].min()
	high_52weeks = df['High'].max()
	range_52weeks = f'{low_day:,.2f}'+' - '+f'{high_day:,.2f}'

	# Format volume and average volume
	vol = last_day['Volume']
	vol = f'{vol:,.0f}'
	avg_vol = stock_info['averageVolume10days']
	avg_vol = f'{avg_vol:,.0f}'

	#Obtain shares outstanding
	shareOutstanding = stock_info['sharesOutstanding']

	# Calculate market cap and format it
	mktcap = last_day['Close']*shareOutstanding
	mktcap = f'{mktcap:,.0f}'

	# Format beta
	beta = stock_info['beta']
	beta = f'{beta:.2f}'

	# Format PE and Forward PE, if no PE, PE not in the dictionary
	if 'trailingPE' in stock_info:
		pe = stock_info['trailingPE']
		pe = f'{pe:.2f}'
	else:
		pe = 'N/A'
	if 'forwardPE' in stock_info:
		fpe = stock_info['forwardPE']
		fpe = f'{fpe:.2f}'
	else:
		fpe = 'N/A'

	# Format EPS
	eps = stock_info['trailingEps']
	eps = f'{eps:.2f}'

	# Format Profit margin
	margin = stock_info['profitMargins']
	margin = f'{margin:.2f}'

	# Prepare data for dividend rate
	if stock_info['dividendRate'] is None or stock_info['dividendRate']=='':
		dividend = 'N/A'
	else:
		dividend = stock_info['dividendRate']

	# Prepare data for ex-dividend date
	if stock_info['exDividendDate'] is not None:
		ex_dividend_date = datetime.fromtimestamp(stock_info['exDividendDate'])
		ex_dividend_date = ex_dividend_date.strftime('%m-%d-%Y')
	else: 
		ex_dividend_date = 'N/A'



	return html.Table([
		html.Tr([html.Td('Industry'), html.Td(),
		         html.Td(stock_info['industry'])]),
		html.Tr([html.Td('Previous Close'), html.Td(),
			     html.Td(stock_info['previousClose'])]),
		html.Tr([html.Td('Open'), html.Td(),
			     html.Td(last_day['Open'])]),
		html.Tr([html.Td('Day Range'), html.Td(),
			     html.Td(range_day)]),
		html.Tr([html.Td('52 Weeks Range'), html.Td(),
			     html.Td(range_52weeks)]),
		html.Tr([html.Td('Volume'), html.Td(),
			     html.Td(vol)]),
		html.Tr([html.Td('Average Volume'), html.Td(),
			     html.Td(avg_vol)]),
		html.Tr([html.Td('Market Capitalization'), html.Td(),
			     html.Td(mktcap)]),
		html.Tr([html.Td('Beta'), html.Td(),
			     html.Td(beta)]),
		html.Tr([html.Td('PE'), html.Td(),
			     html.Td(pe)]),
		html.Tr([html.Td('Forward PE'), html.Td(),
			     html.Td(fpe)]),
		html.Tr([html.Td('Earning Per Share (EPS)'), html.Td(),
			     html.Td(eps)]),
		html.Tr([html.Td('Profit Margin'), html.Td(),
			     html.Td(margin)]),
		html.Tr([html.Td('Dividend'), html.Td(),
			     html.Td(dividend)]),
		html.Tr([html.Td('Ex-Dividend Date'), html.Td(),
			     html.Td(ex_dividend_date)]),
		html.Tr([html.Td('Earning Per Share (EPS)'), html.Td(),
			     html.Td(f'{shareOutstanding:,.0f}')])
		])

# Generate Table for Tab 2 - Index
def getTab2Table(name, last_close, range_period, range_52weeks):
	if last_close >= 0:
		color = 'green'
	else:
		color = 'red'
	last_close = last_close = f'{last_close:.2f}%'
	return html.Table([
		html.Tr(html.Td(html.B(name))),
		html.Tr([html.Td('Close'),
			    html.Td(last_close, style={'color':color})]),
		html.Tr([html.Td('Period Range'),
			     html.Td(f'{range_period[0]:,.2f}'+ \
			     	     ' - '+f'{range_period[1]:,.2f}')]),
		html.Tr([html.Td('52 Weeks Range'),
			     html.Td(f'{range_52weeks[0]:,.2f}'+\
			     	     ' - '+f'{range_52weeks[1]:,.2f}')])
		])

##### Global Variables #####
# Dictionary for the dropdown list to select stock market
tab1_markets = [{'label':'Hong Kong', 'value':'hk'},
                {'label':'United States', 'value':'us'}]
# Dictionary for the dropdown list to select index in Tab 2
index_choice = [{'label':' Hong Kong: Heng Seng Index', 'value':'hsi'},
                {'label':' United States: S&P 500', 'value':'sp500'}]
