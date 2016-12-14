import pandas as pd 
import numpy as np 
import os
import sys 
import csv

def is_folder_valid(stock_symbol):
	path = "./data_samples/"+stock_symbol+"_three_phase"
	return os.path.exists(path)
	
def get_data_path(stock_symbol):
	return "./data_samples/"+stock_symbol+"_three_phase/"+stock_symbol+"_three_phase_features.csv"

def get_index_and_three_periods(filename):
	l = filename.split(".")[0].split("_")
	index = int(l[0])
	t1 = int(l[3]) - int(l[2]) + 1
	t2 = int(l[5]) - int(l[4]) + 1
	t3 = int(l[7]) - int(l[6]) + 1
	# t1 = t1/t2
	# t2 = int(t2>5 or t2<30)
	# t3 = int(t3<10)
	return index, t1, t2, t3

def initialize_new_df(df):
	num_cols = len(df.columns)
	df[num_cols] = 0;
	df[num_cols+1] = 0;
	df[num_cols+2] = 0;
	df.columns = range(len(df.columns))
	return df

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

for stock_symbol in stock_symbols:
	path = "./data_samples/"+stock_symbol+"_three_phase"
	if(not os.path.exists(path)):
		print("data for "+stock_symbol+" does not exist.")
		continue
	data_path = get_data_path(stock_symbol)
	df = pd.read_csv(data_path, header = None)
	df = initialize_new_df(df)
	num_cols = len(df.columns)
	t1_index = num_cols - 3
	t2_index = num_cols - 2
	t3_index = num_cols - 1
	# for filename in os.listdir(directory):
	# 	if(filename.endswith(".png")):
	with open(path+'/three_phase_name.csv') as f:
		reader = csv.reader(f)
		for row in reader:
			filename = row[0]
			index, t1, t2, t3 = get_index_and_three_periods(filename)
			#check if the row is correctly corresponding to the correct image
			if(index != int(df.get_value(index,0).split("_")[0])):
				print(index)
				print(df.get_value(index,0).split("_")[0])
				sys.exit("incorrect rows")
			else:
				df.set_value(index, t1_index, t1)
				df.set_value(index, t2_index, t2)
				df.set_value(index, t3_index, t3)
	df.to_csv(path+"/"+stock_symbol + "_features.csv", header = False, index = False)


