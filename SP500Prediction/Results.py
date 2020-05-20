def save_result_rmse(model_name, rmse, rsqu):
	filepath = 'Results/'
	filepath += model_name.replace(' ','')
	filepath += '.txt'

	with open(filepath, 'w') as f:
		f.write('### ')
		f.write(model_name)
		f.write(' ###\n')
		f.write(f'R-squared:{rsqu:,.4f}\n')
		f.write(f'RMSE:{rmse:,.2f}')
		f.close()
