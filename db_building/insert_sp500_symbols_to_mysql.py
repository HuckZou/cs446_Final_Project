import datetime
import lxml.html
import urllib2
import MySQLdb as mdb
from math import ceil

def obtain_parse_wiki_snp500():
	"""Download and parse the Wikipedia list of S&P500 
	constituents using requests and libxml.
	Returns a list of tuples for to add to MySQL."""

	# Stores the current time, for the created_at record
	now = datetime.datetime.utcnow()

	# Use urllib2 to open the URL and then use libxml to download the list of S&P500 companies and obtain the symbol table
	page = lxml.html.parse(urllib2.urlopen('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies'))

	# Put more than 500 because there are 505 companies listed in S&P500, the extra space will be truncated automatically.
	symbolslist = page.xpath('//table[1]/tr')[1:600]
	# Obtain the symbol information for each row in the S&P500 constituent table
	symbols = []
	for i, symbol in enumerate(symbolslist):
		tds = symbol.getchildren();
		sd = {'ticker': tds[0].getchildren()[0].text,
			  'name': tds[2].getchildren()[0].text,
			  'sector': tds[3].text }
		# Create a tuple (for the DB format) and append to the grand list
		symbols.append( (sd['ticker'], 'stock', sd['name'], sd['sector'], 'USD', now, now) )

	return symbols


def insert_snp500_symbols(symbols):
	"""Insert the S\&P500 symbols into the MySQL database."""
	# Connect to the MySQL instance
	db_host = 'localhost'
	db_user = 'stock_user'
	db_pass = 'zQs87873830'
	db_name = 'stock_master'
	connection = mdb.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name)

	# Create the insert strings
	column_str = "ticker, instrument, name, sector, currency, created_date, last_updated_date"
	insert_str = ("%s, " * 7)[:-2]
	final_str = "INSERT INTO symbol (%s) VALUES (%s)" % (column_str, insert_str)
	print final_str, len(symbols)
	# Using the MySQL connection, carry out
	# an INSERT INTO for every symbol
	with connection:
		cur = connection.cursor()
	# This line avoids the MySQL MAX_PACKET_SIZE
	# Although of course it could be set larger!
		for i in range(0, int(ceil(len(symbols) / 100.0))):
			cur.executemany(final_str, symbols[i*100:(i+1)*100])

if __name__ == "__main__":
	symbols = obtain_parse_wiki_snp500()
	insert_snp500_symbols(symbols)
