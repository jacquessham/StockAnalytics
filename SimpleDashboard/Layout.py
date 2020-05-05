import pandas as pd
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


##### Layouts for Tab 1 #####
# Dropdown list for single stock choice
def get_tab1_info_box():
	return html.Div([
				html.Div([
					html.H3(id='tab1-stock-price'),
					html.H4(id='tab1-stock-price-change'),
					html.H4(id='tab1-stock-price-percentchange')
					],style={'width':'40%','display': 'inline-block'}),
				html.Div(style={'width':'20%','display': 'inline-block'}),
				html.Div([
					html.Div(dcc.Input(id='tab1-ticker-input',value='',
					                   type='text'),
					                   style={'width':'25%',
					                          'display': 'inline-block'}),
					html.Div(html.Button('Submit',id='tab1-submit'),
						     style={'width':'20%','display': 'inline-block'})
					],style={'width':'40%','display': 'inline-block'})
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
def getLinePlot(df):
	traces = []
	for col in df.columns:
		if col != 'Date':
			traces.append({'x':df['Date'], 'y':df[col],'name':col,
				           'mode':'lines'})
	layout = {'xaxis':{'title':'Date'},
	          'yaxis':{'title':'% Change', 'tickformat':'.0%'},
	          'hovermode':False}
	return {'data':traces, 'layout':layout}

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
# Dictionary for the dropdown list to select index in Tab 2
index_choice = [{'label':' Hong Kong: Heng Seng Index', 'value':'hsi'},
                {'label':' United States: S&P 500', 'value':'sp500'}]
