import talib
from data_misc import remove_nan
import data_retrieve as d_retri 
import data_misc as d_misc 
import numpy as np
# This function calculates MACD indicator
# It outputs are [macd, signal, hist]
''' 
	talib.MACD(params)
	Input parameters:
	inReal - array of floats
	startIdx - start index for input data
	endIdx - end index for input data
	optInFastPeriod
	optInSlowPeriod
	optInSignalPeriod
	Returns:
	outMACD outMACDSignal outMACDHist
'''
def compute_MACD(date,data, fast=12, slow=26, signal=9):
	macd, signal, hist = talib.MACD(data, fastperiod=fast, slowperiod=slow, signalperiod=signal)
	macd = remove_nan(macd)
	signal = remove_nan(signal)
	hist = remove_nan(hist)
	date = date[len(date)-len(hist):]
	return date, macd, signal, hist 

'''
	This function extracts sixteen features from the MACD data
	let p1, p2, p3 (x,y) denotes the location of maximum points in a three phase data serie
	feature1: type of hypothesis (0: possibly bearish, 1: possibly bullish)
	feature2: hist: the absolute height of phase1 divide by the absolute height of phase2 
	feature3: hist: the absolute height of phase1 divide by the absolute height of phase3
	feature4: hist: the absolute height of phase2 divide by the absolute height of phase3
	# feature5: hist: the angle between the vector p2-p1 and the vector p3-p1
	# feature6: hist: the angle between the vector p1-p2 and the vector p3-p2
	feature7: macd: the absolute height of phase1 divide by the absolute height of phase2 
	feature8: macd: the absolute height of phase1 divide by the absolute height of phase3
	feature9: macd: the absolute height of phase2 divide by the absolute height of phase3
	# feature10: macd: the angle between the vector p2-p1 and the vector p3-p1
	# feature11: macd: the angle between the vector p1-p2 and the vector p3-p2 
	feature12: signal: the absolute height of phase1 divide by the absolute height of phase2 
	feature13: signal: the absolute height of phase1 divide by the absolute height of phase3
	feature14: signal: the absolute height of phase2 divide by the absolute height of phase3
	# feature15: signal: the angle between the vector p2-p1 and the vector p3-p1
	# feature16: signal: the angle between the vector p1-p2 and the vector p3-p2
	Label: whether or not there is a bullish, bearish or no pattern
		   0: no pattern
		   1: bullish divergence
		   2: bearish divergence
'''

def extract_three_phase_feature(ticker='CMG'):
	date, price = d_retri.get_data(ticker)
	if(date.size == 0):
		print 'No observation is retrieved from the database'
		return
	date, macd, signal, hist = compute_MACD(date, price)
	macd, signal, hist = d_misc.normalize_MACD_data(macd, signal, hist)
	three_phase_indexes = d_misc.find_three_phase_indexes(hist).astype(int)

	'''
	first
	|
	||		 third	
	||||	   |
	|||||	  |||
	---------------
		 |||||
		  |||
		 second
	'''
	dir_path = d_misc.build_three_phase_dir_path(ticker)
	# create a file to store the features
	file_path = d_misc.build_three_phase_feature_file_path(dir_path, ticker)
	datefile_path = d_misc.build_three_phase_feature_date_path(dir_path, ticker)
	# filename = '/' + ticker + '_feature_sample.csv'
	# file_path += filename
	file = open(file_path, 'w')
	datefile = open(datefile_path, 'w')
	sample_num = (three_phase_indexes.size - 4)/2
	samples = np.arange(0, sample_num)
	# features = np.random.random(16)
	for sample_index in samples:
		features = np.random.random(10)
		current_feature = 0
		start_index = three_phase_indexes[sample_index*2]
		# print start_index
		end_index = three_phase_indexes[sample_index*2+5]
		# print end_index
		temp_date, temp_macd, temp_signal, temp_hist = d_misc.truncate_MACD_data(date, macd, signal, hist, start_index, end_index)
		temp_three_phase_indexes = three_phase_indexes[sample_index*2:sample_index*2+6]
		features[current_feature] = int(np.mean(temp_hist[0:temp_three_phase_indexes[1] - temp_three_phase_indexes[0] +1]) < 0)
		current_feature += 1
		for temp_data in [temp_hist, temp_macd, temp_signal]:
			first_max, second_max, third_max, first_max_index, second_max_index, third_max_index \
			= d_misc.find_three_phase_max_and_index(temp_data, temp_three_phase_indexes)
			# feature2, feature7, feature12
			features[current_feature] = float(first_max)/second_max
			current_feature += 1
			# feature3, feature8, feature13
			features[current_feature] = float(first_max)/third_max
			current_feature += 1
			# feature4, feature9, feature14
			features[current_feature] = float(second_max)/third_max
			current_feature += 1

		# write a new line to the feature file:
		# sample_index_ticker feature1-10 label
		build_line = str(sample_index) + '_' + ticker + ','

		for feature in features:
			build_line += str(feature) + ','
		build_line = build_line[:-1]
		build_line += '\n'
		file.write(build_line)
		datefile.write(str(temp_date[-1])+'\n')
	file.close()
	datefile.close()



