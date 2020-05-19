import pandas as pd
import psycopg2
from InsertData import *


# Obtain data
rawdata = pd.read_csv('ShareOutstanding_ForErrors.csv', engine='python')

# Connect to database
conn = psycopg2.connect(host='localhost', port=5432, database='postgres')

# Error Log
error_log = {'Ticker':[], 'Issue': []}

for index, row in rawdata.iterrows():
	try:
		insert_share(conn, row['Ticker'], row['SharesOutstanding'])
	except:
		print('Error when Processing', curr_ticker)
		error_log['Ticker'].append(curr_ticker)
		error_log['Issue'].append('Insertion Error')
		conn.commit()

conn.close()

# Save error log
error_log = pd.DataFrame(error_log)
error_log.to_csv('Logs/ErrorLog_SP500ShareOutstanding_errors.csv', index=False)