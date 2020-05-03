import pandas as pd
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


# Layouts for Tab 1
# Dropdown list for single choice
def get_info_box():
	return html.Div([
				html.Div([
					html.H3(id='tab1-stock-price'),
					html.H4(id='tab1-stock-price-change'),
					html.H4(id='tab1-stock-price-percentchange')
					],style={'width':'60%','display': 'inline-block'}),
				html.Div([
					dcc.Dropdown(id='tab1-stock-dropdown')
					],style={'width':'40%','display': 'inline-block'})
			])

# Layout for both Tab 1 and Tab 2
def get_interval_layout(tab):
	id_name = tab+'-time-interval'
	return html.Div([dcc.RadioItems(id=id_name)])

def get_table_layout(tab):
	id_name = tab+'-table'
	return html.Div(html.Table(id=id_name))




def get_single_dropdown(options):
	return dcc.Dropdown(
		id='stock-tab1-dropdown',
		options=[{'label':opt, 'label':opt} for opt in options],
		value='00005',
		style={'text-align':'left'}
		)