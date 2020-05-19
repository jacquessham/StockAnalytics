def save_result_rmse(model_name, rmse):
	filepath = 'Results/'
	filepath += model_name.replace(' ','')
	filepath += '.txt'

	with open(filepath, 'w') as f:
		f.write('### ')
		f.write(model_name)
		f.write(' ###\n')
		f.write('RMSE: ')
		f.write(f'{rmse:,.2f}')
		f.close()
