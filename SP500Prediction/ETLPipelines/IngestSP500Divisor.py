import pandas as pd
import psycopg2
from InsertData import *


# Connect to database
conn = psycopg2.connect(host='localhost', port=5432, database='postgres')

# Read Data
df_divisor = pd.read_csv('../../SupplementalData/SP500Divisor.csv')
df_divisor['Divisor'] = df_divisor['Divisor_million']*1000000

for index, row in df_divisor.iterrows():
	try:
		insert_divisor(conn, row['Tradedate'], row['Divisor'])
	except:
		print('Error ')
		pass

conn.close()