import datetime
import MySQLdb as mdb
import urllib2
# Obtain a database connection to the MySQL instance
db_host = 'localhost'
db_user = 'stock_user'
db_pass = 'zQs87873830'
db_name = 'stock_master'
connection = mdb.connect(db_host, db_user, db_pass, db_name)

def obtain_list_of_db_tickers():
	"""Obtains a list of the ticker symbols in the database."""
	with connection:
		cur = connection.cursor()
		cur.execute("SELECT id, ticker FROM symbol")
		data = cur.fetchall()
		return [(d[0], d[1]) for d in data]

def get_daily_historic_data_yahoo(ticker, 
								  start_date=(2000,1,1), 
								  end_date=datetime.date.today().timetuple()[0:3]):
	"""Obtains data from Yahoo Finance returns and a list of tuples.
	ticker: Yahoo Finance ticker symbol, e.g. "GOOG" for Google, Inc.
	start_date: Start date in (YYYY, M, D) format
	end_date: End date in (YYYY, M, D) format"""
	# Construct the Yahoo URL with the correct integer query parameters
	# for start and end dates. Note that some parameters are zero-based!
	yahoo_url = "http://ichart.finance.yahoo.com/table.csv?s=" \
	"%s&a=%s&b=%s&c=%s&d=%s&e=%s&f=%s" % \
	(ticker, start_date[1] - 1, start_date[2], start_date[0],
	end_date[1] - 1, end_date[2], end_date[0])
	# Try connecting to Yahoo Finance and obtaining the data
	# On failure, print an error message.
	prices = []
	try:
		# Ignore the header ([1:])
		yf_data = urllib2.urlopen(yahoo_url).readlines()[1:]
		for y in yf_data:
			p = y.strip().split(',')
			prices.append( (datetime.datetime.strptime(p[0], '%Y-%m-%d'),
							p[1], p[2], p[3], p[4], p[5], p[6]) )
	except Exception, e:
		print "Could not download Yahoo data: %s\n%s\n" % (ticker, e)
	return prices


def insert_daily_data_into_db(data_vendor_id, symbol_id, daily_data):
	"""Takes a list of tuples of daily data and adds it to the
	MySQL database. Appends the vendor ID and symbol ID to the data.
	daily_data: List of tuples of the OHLC data (with
	adj_close and volume)"""
	# Create the time now
	now = datetime.datetime.utcnow()
	# Amend the data to include the vendor ID and symbol ID
	daily_data = [(data_vendor_id, symbol_id, d[0], now, now,
	d[1], d[2], d[3], d[4], d[5], d[6]) for d in daily_data]
	# Create the insert strings
	column_str = """data_vendor_id, symbol_id, price_date, created_date,
	last_updated_date, open_price, high_price, low_price,
	close_price, volume, adj_close_price"""
	insert_str = ("%s, " * 11)[:-2]
	final_str = "INSERT INTO daily_price (%s) VALUES (%s)" % \
	(column_str, insert_str)
	# Using the MySQL connection, carry out an INSERT INTO for every symbol
	with connection:
		cur = connection.cursor()
		cur.executemany(final_str, daily_data)

if __name__ == "__main__":
	# Loop over the tickers and insert the daily historical
	# data into the database
	tickers = obtain_list_of_db_tickers()
	# print tickers[455]
	# index = tickers.index((956L, 'UA-C'))
	# tickers = tickers[index:]
	for t in tickers:
		print "Adding data for %s" % t[1]
		yf_data = get_daily_historic_data_yahoo(t[1])
		if not yf_data:
			print "%s is not added to database\n" % t[1]
			continue;
		insert_daily_data_into_db('1', t[0], yf_data)