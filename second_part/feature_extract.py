import talib
import numpy as np
import pandas as pd 
import pandas.io.sql as psql
import MySQLdb as mdb
import os

#This function reads daily price and volume data from database (starting from 2000-01-01)
#and returns an pandas dataframe object.
def get_data(ticker):
	db_host = 'localhost'
	db_user = 'stock_user'
	db_pass = 'zQs87873830'
	db_name = 'stock_master'
	connection = mdb.connect(db_host, db_user, db_pass, db_name)
	sql = """SELECT dp.price_date, dp.close_price, dp.volume
		 FROM symbol AS sym
		 INNER JOIN daily_price AS dp
		 ON dp.symbol_id = sym.id
		 WHERE sym.ticker = '%s'
		 ORDER BY dp.price_date ASC;""" % ticker
	# Create a pandas dataframe from the SQL query
	data = psql.read_sql(sql, con=connection, index_col='price_date')
	date = pd.to_datetime(data.index).strftime('%Y%m%d').astype(int)
	data.insert(0, 'numeric_date',date)
	return data

# this method calculates the weekly price from the daily price
# it takes the last of a trading week
# def add_weekly_data(data):
# 	temp = data.index.weekday
# 	temp = temp[1:] - temp[:-1]
# 	data['weekday'] = data['weekday'] < 0

	

#Currently this method adds 13/26 Daily EMA, 50/200 SMA, 
#13 VEMA, 13/26 Weekly EMA to the dataframe that is passed in
#The data passed in currently has index in datetime type, and 
#columns in numeric_date, daily_close_price, and daily_volume.
def add_indicators(data):
	daily_price = np.array(data['close_price'])
	daily_volume = np.array(data['volume'], dtype='double')
	data['EMA_daily_13'] = talib.EMA(daily_price, timeperiod=13)
	data['EMA_daily_26'] = talib.EMA(daily_price, timeperiod=26)
	data['SMA_daily_50'] = talib.SMA(daily_price, timeperiod=50)
	data['SMA_daily_200'] = talib.SMA(daily_price, timeperiod=200)
	data['EMA_daily_v_13'] = talib.EMA(daily_volume, timeperiod=13)
	macd, signal, hist = talib.MACD(daily_price, fastperiod=12, slowperiod=26, signalperiod=9)
	data['macd'] = macd 
	data['signal'] = signal
	data['histo'] = hist
	return data 

def calculate_features(data):
	data['EMA_daily_13_pct'] = data.EMA_daily_13.pct_change(1)
	data['EMA_daily_26_pct'] = data.EMA_daily_26.pct_change(1)
	data['SMA_daily_50_pct'] = data.SMA_daily_50.pct_change(1)
	data['SMA_daily_200_pct'] = data.SMA_daily_200.pct_change(1)
	data['macd_pct'] = data.macd.pct_change(1)
	data['signal_pct'] = data.signal.pct_change(1)
	data['hist_pct'] = data.histo.pct_change(1)
	data['volume_spike_ratio'] = data.volume/data.EMA_daily_v_13
	return data 

	#Assumption about the volatility for stocks is not right
	#different stocks have differnt volatility
def add_label(data):
	future_period = 26
	daily_price = np.array(data.close_price) 
	length = len(daily_price)
	future_pct_up = np.empty(length)
	future_pct_up[:] = np.NAN
	future_pct_down = np.empty(length)
	future_pct_down[:] = np.NAN
	for curr_index in range(0, length-future_period):
		last_index = curr_index + future_period
		future_pct_up[curr_index] = 100*(np.max(daily_price[curr_index+1:last_index+1]) - daily_price[curr_index])/daily_price[curr_index]
		future_pct_down[curr_index] = 100*(np.min(daily_price[curr_index+1:last_index+1]) - daily_price[curr_index])/daily_price[curr_index]
	bench_mark = np.linspace(-15,15,11)
	up_label = np.empty(length)
	down_label = np.empty(length)
	up_label[:] = np.NAN
	down_label[:] = np.NAN
	count = 0
	for elem in future_pct_up:
		up_label[count] = np.argmin(np.abs(elem - bench_mark))
		count = count + 1
	count = 0
	for elem in future_pct_down:
		down_label[count] = np.argmin(np.abs(elem - bench_mark))
		count = count + 1
	up_label[length-future_period:length] = np.NAN
	down_label[length-future_period:length] = np.NAN
	data['up_label'] = up_label
	data['down_label'] = down_label
	return data 
	# data.dropna(inplace=True)
# df = extract_NN1_feature(data, nn1_data)
def extract_NN1_feature(data, nn1_data):
	nn1_data = nn1_data[nn1_data['pred']!=0]
	data.index = range(0,len(data))
	columns = ['EMA_daily_13_pct', 'EMA_daily_26_pct', 'SMA_daily_50_pct',\
				'SMA_daily_200_pct', 'macd_pct', 'signal_pct', 'hist_pct', \
				'volume_spike_ratio','price_level_ratio','price_level_pct', \
				'phase1','phase2','phase3','divergence_type','label']
	feature_df = np.empty([len(nn1_data), len(columns)])
	feature_df[:] = np.NAN
	index = range(0,len(nn1_data))
	feature_df = pd.DataFrame(feature_df, index=index, columns=columns)
	for row in nn1_data.itertuples():
		row_index = row[0]
		phase1 = row[1]
		phase2 = row[2]
		phase3 = row[3]
		date = row[4]
		pred = row[5]
		data_row = data[data.numeric_date==int(date)]
 		if(len(data_row) == 0):
 			continue
		end_index = data_row.index[0]
		start_index = end_index - phase1 - phase2 - phase3 + 1
		price_range1 = data.close_price[start_index:start_index+phase1]
		price_range3 = data.close_price[start_index+phase1+phase2:end_index+1]
 		if(pred == 1):
 			temp = np.min(price_range1)/np.min(price_range3)
 			feature_df.set_value(row_index, 'price_level_ratio', temp)
 			temp = (np.min(price_range3)-np.min(price_range1))/np.min(price_range1)
 			feature_df.set_value(row_index, 'price_level_pct', temp)
 			feature_df.set_value(row_index, 'label', data_row.up_label)
 		else:
 			temp = np.max(price_range1)/np.max(price_range3)
 			feature_df.set_value(row_index, 'price_level_ratio', temp)
 			temp = (np.max(price_range3)-np.max(price_range1))/np.max(price_range1)
 			feature_df.set_value(row_index, 'price_level_pct', temp)
 			feature_df.set_value(row_index, 'label', data_row.down_label)
 		feature_df.set_value(row_index, "EMA_daily_13_pct", data_row.EMA_daily_13_pct)
 		feature_df.set_value(row_index, 'EMA_daily_26_pct', data_row.EMA_daily_26_pct)
 		feature_df.set_value(row_index, 'SMA_daily_50_pct', data_row.SMA_daily_50_pct)
 		feature_df.set_value(row_index, 'SMA_daily_200_pct', data_row.SMA_daily_200_pct)
 		feature_df.set_value(row_index, 'macd_pct', data_row.macd_pct)
 		feature_df.set_value(row_index, 'signal_pct', data_row.signal_pct)
 		feature_df.set_value(row_index, 'hist_pct', data_row.hist_pct)
 		feature_df.set_value(row_index, 'volume_spike_ratio', data_row.volume_spike_ratio)
 		feature_df.set_value(row_index, 'phase1', phase1)
 		feature_df.set_value(row_index, 'phase2', phase2)
 		feature_df.set_value(row_index, 'phase3', phase3)
 		feature_df.set_value(row_index, 'divergence_type', pred)
 	return feature_df
 		

#output dataframe column names [phase1 phase2 phase3 date pred]
def combine_NN1_feature(ticker):
	datefile = "data_samples/"+ticker+"_three_phase/"+ticker+"_three_phase_features_date.csv"
	predfile = "data_samples/"+ticker+"_three_phase/pred.csv"
	nnfile = "data_samples/"+ticker+"_three_phase/"+ticker+"_features.csv"
	pred = np.loadtxt(predfile)
	date = np.loadtxt(datefile)
	nndata = pd.read_csv(nnfile, header=None)
	nndata = nndata.iloc[:,[11,12,13]]
	nndata.columns=['phase1','phase2','phase3']
	nndata['date'] = date
	nndata['pred']=pred
	return nndata


# def output_training_samples():
stock_symbols = ['MMM','ABT','ABBV','ADBE','ALL','GOOG','AMZN','AEE',\
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
total_df = pd.DataFrame()
for stock_symbol in stock_symbols:
	path = "./data_samples/"+stock_symbol+"_three_phase"
	if(not os.path.exists(path)):
		print("data for "+stock_symbol+" does not exist.")
		continue
	data = get_data(stock_symbol)
	data = add_indicators(data)
	data = calculate_features(data)
	data = add_label(data)
	nndata = combine_NN1_feature(stock_symbol)
	training_samples = extract_NN1_feature(data, nndata)
	total_df=total_df.append(training_samples.dropna())
	print("finished "+stock_symbol)

total_df.index = range(0,len(total_df))
total_df.to_csv("training_samples.csv")

