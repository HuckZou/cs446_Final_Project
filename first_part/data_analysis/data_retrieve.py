import pandas as pd
import pandas.io.sql as psql
import MySQLdb as mdb
import numpy as np 

# Connect to the MySQL instance
db_host = 'localhost'
db_user = 'stock_user'
db_pass = 'zQs87873830'
db_name = 'stock_master'
connection = mdb.connect(db_host, db_user, db_pass, db_name)
# Select all of the historic Google adjusted close data
# retrieving_stock_daily_price_from_mysql
# This function retrieve data from mysql database 
# and return two numpy arrays: date(int) and price(float)
def get_data(ticker):
	sql = """SELECT dp.price_date, dp.close_price
			 FROM symbol AS sym
			 INNER JOIN daily_price AS dp
			 ON dp.symbol_id = sym.id
			 WHERE sym.ticker = '%s'
			 ORDER BY dp.price_date ASC;""" % ticker
	# Create a pandas dataframe from the SQL query
	data = psql.read_sql(sql, con=connection, index_col='price_date')
	price = np.array(data.close_price)
	date = pd.to_datetime(data.index).strftime('%Y%m%d').astype(int)
	return date, price
