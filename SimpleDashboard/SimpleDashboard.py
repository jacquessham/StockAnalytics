import pandas as pd
import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import quandl
from dash.dependencies import Input, Output
from Layout import *

"""
def getAPI(filepath):
	with open(filepath, 'r') as f:
		rawtext = f.read()
	textlist = rawtext.split(',')
	return textlist[1]

quandl.ApiConfig.api_key = getAPI('../../../../License/QuandlAPIkey.csv')

start_date  = '2010-01-01'
end_date = '2020-04-30'
data = quandl.get("HKEX/00005", start_date=start_date,
	              end_date=end_date).reset_index()
"""

# Dash Set up
app = dash.Dash()

# Dashboard layout
app.layout = html.Div([
	dcc.Tabs(id='dashboard-tabs', value='price-tab',children=[
		dcc.Tab(label='Stock Price', value='price-tab',children=[
			html.Div([html.H2('Cathay Pacific', 
				           style={'width':'30%','display':'inline-block'}), 
				      html.H4('00293.HK', 
				           style={'width':'10%','display':'inline-block'})],
				      style={'width':'70%','margin':'auto'}),
			# Position 0, Title
			html.Div(get_info_box(),
				     style={'width':'70%','margin':'auto'}),
			# Position 1, Info and dropdown
			html.Div(get_interval_layout('tab1'),
				     style={'width':'70%','margin':'auto'}),
			# Position 2, Range
			html.Div(dcc.Graph(id='price-vis'),
				     style={'width':'80%','margin':'auto'}),
			# Position 3, Graph
			html.Div(get_table_layout('tab1'),
				     style={'width':'80%','margin':'auto'})
			# Position 4, Table of stats
			]), # Tab 1, End price-tab
		dcc.Tab(label='Index Change', value='change-tab',children=[
			html.Div([html.H2('Price Change')]),
			# Position 0, Title
			html.Div([html.P('Position 1')]),
			# Position 1, Info and dropdown
			html.Div(get_interval_layout('tab2')),
			# Position 2, Range
			html.Div(dcc.Graph(id='change-vis')),
			# Position 3, Graph
			html.Div(get_table_layout('tab2'))
			# Position 4, Table of stats
			]) # Tab 2, End change-tab
		]) # End Tabs
	]) # End base Div

if __name__ == '__main__':
    app.run_server(debug=True, port=8000)