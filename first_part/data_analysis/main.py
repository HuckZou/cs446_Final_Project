import data_sampler as ds 
import data_process as dp 
import data_labeling as dl 


def main(ticker):
	ds.three_phase_sample(ticker)
	dp.extract_three_phase_feature(ticker)
	dl.label_data(ticker, ticker + '_three_phase_features.csv')


def continue_labeling(ticker):
	dl.label_data(ticker, ticker + '_three_phase_features.csv')


def extract_unlabeled_data(ticker):
	ds.three_phase_sample(ticker)
	dp.extract_three_phase_feature(ticker)	
	
def extract_second_part_data():
	tickers = ['MMM','ABT','ABBV','ADBE','ALL','GOOG','AMZN','AEE',\
				'AAL', 'AXP', 'AIG', 'AMT', 'ABC', 'AON', 'AAPL', 'ADM',\
				'AIZ', 'T', 'ADP', 'AZO', 'BBY', 'BLK', 'BA', 'BRK-B', \
				'COG', 'CPB', 'COF', 'CAT', 'CNC', 'CTL', 'SCHW', 'CVX', \
				'CINF', 'CHD', 'CSCO','CME', 'COH', 'KO', 'CMCSA', 'CAG', \
				'COTY', 'CCI', 'CMI', 'CVS', 'ETFC', 'EIX', 'EW','EQT', \
				'EQIX', 'XOM', 'FB', 'FISV', 'FLIR', 'IP', ' IBM', 'KSS', \
				'LOW', 'MRO', 'MAR', 'MJN', 'MU', 'MS', 'MYL','NFLX',\
				'NFX', 'NEE', 'NKE', 'JWN', 'NOC', 'PDCO', 'PEP', 'PFE',\
				'PSX', 'RL', 'PHM', 'COL', 'ROP', 'R', 'SLB','SEE',\
				'SO', 'LUV', 'SE', 'STJ', 'SPLS', 'SYY', 'TGT', 'TEL', \
				'WFC', 'WM', 'DIS', 'WMT', 'XL', 'XYL', 'ZBH', 'ZION','ZTS']
	for ticker in tickers:
		extract_unlabeled_data(ticker)
