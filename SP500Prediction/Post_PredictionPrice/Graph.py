import pandas as pd
from datetime import datetime
import plotly.graph_objs as go


def generate_line_chart(X_train=None, X_test=None,  df_m1=None, m1Name=None, 
	                    df_m2=None, m2Name=None, title=None):
	data = [{'x': X_train['ds'], 'y': X_train['y'],
	         'name':'Training Data','mode':'lines',
	         'line':{'color': 'royalblue'}},
	        {'x': X_test['ds'], 'y': X_test['realprice'],
	         'name':'Real Price', 'mode':'lines',
	         'line':{'color': 'orange'}},
	        {'x': df_m1['ds'], 'y': df_m1['yhat'],
	         'name': m1Name,'mode':'lines',
	         'line':{'color':'red', 'dash':'dash'}}]
	if df_m2 is not None:
		data.append({'x': df_m2['ds'], 'y': df_m2['yhat'],
		             'name': m2Name,'mode':'lines',
		             'line':{'color':'purple', 'dash':'dash'}})
	layout['title'] = {'text':title, 'x': 0.5}

	return {'data': data, 'layout': layout}

layout = {'xaxis':{'title':'Date',
          'range':[datetime(2016,1,1), datetime(2020,5,8)]},
	      'yaxis':{'title': 'Price ($)'},
	      'hovermode':False,
	      'plot_bgcolor':'white'}