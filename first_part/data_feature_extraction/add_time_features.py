import pandas as pd 
import numpy as np 
import os
import sys 

def get_folder_dir(stock_symbol):
	return "../data_samples/"+stock_symbol+"_three_phase"

def get_data_path(folder_dir, stock_symbol):
	return folder_dir+"/progress_"+stock_symbol+"_three_phase_features.csv"

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
	temp = df[num_cols-1]
	df.drop(num_cols-1, axis=1, inplace =True)
	df[num_cols-1] = 0;
	df[num_cols] = 0;
	df[num_cols+1] = 0;
	df = pd.concat([df, temp], axis=1)
	df.columns = range(len(df.columns))
	return df

stock_symbols = [ "KO", "JWN", "AAPL", "AMZN", "CMG", "F","UA","FB","JPM"]

for stock_symbol in stock_symbols:
	directory = get_folder_dir(stock_symbol)
	data_dir = get_data_path(directory, stock_symbol)
	df = pd.read_csv(data_dir, header = None)
	df = initialize_new_df(df)
	num_cols = len(df.columns)
	t1_index = num_cols - 4
	t2_index = num_cols - 3
	t3_index = num_cols - 2
	for filename in os.listdir(directory):
		if(filename.endswith(".png")):
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
	df.to_csv(stock_symbol + "_features.csv", header = False, index = False)

