import numpy as np
import data_misc as d_misc 
import data_retrieve as d_retri 
import data_process as d_proc 
import data_plot as d_plot 
# def build_total_sample_dir_path(ticker):
# 	path = '/Users/huckzou/Desktop/project_research/data_samples/' + ticker + '_total_sample' 
# 	return path

# def build_total_image_sample_path(dir_path, ticker):
# 	path = dir_path + '/' + ticker + '_total_sample.png'

def total_sample(ticker = 'CMG'):
	date, price = d_retri.get_data(ticker)
	if(date.size == 0):
		print 'No observation is retrieved from the database'
		return
	date, macd, signal, hist = d_proc.compute_MACD(date, price)
	macd, signal, hist = d_misc.normalize_MACD_data(macd, signal, hist)
	dir_path = d_misc.build_total_sample_dir_path(ticker)
	d_misc.make_dir(dir_path)
	save_path = d_misc.build_total_image_sample_path(dir_path, ticker)
	d_plot.plot_total_sample_data(save_path,ticker, date, macd, signal, hist)

# This function randomly sample MACD data from the given stock and time frame (in days), sample_ratio is from 0 to 1
def random_sample(ticker = 'CMG', time_frame = 120, sample_ratio = 0.05):
	date, price = d_retri.get_data(ticker)
	if(date.size == 0):
		print 'No observation is retrieved from the database'
		return
	date, macd, signal, hist = d_proc.compute_MACD(date, price)
	macd, signal, hist = d_misc.normalize_MACD_data(macd, signal, hist)
	total_obser = date.size
	sample_num = int(total_obser * sample_ratio)
	# if the total observations are not enough to have the number of samples specified, then we stop the program 
	if(total_obser - time_frame < sample_num):
		print 'not enough observations to support the sampling.'
		return

	# Create a new directory to store sampling data
	dir_path = d_misc.build_dir_path(ticker, time_frame)
	d_misc.make_dir(dir_path)

	samples = np.arange(0,sample_num)
	for sample_index in samples:
		start_index = np.random.randint(0, total_obser - time_frame)
		end_index = start_index + time_frame
		save_path = d_misc.build_image_sample_path(dir_path, ticker, start_index, end_index, sample_index)
		# Truncate the data with specified start index and end index
		temp_date, temp_macd, temp_signal, temp_hist = d_misc.truncate_MACD_data(date, macd, signal, hist, start_index, end_index)
		d_plot.plot_random_sample_data(save_path, ticker, temp_date, temp_macd, temp_signal, temp_hist)

	print 'Done with ' + ticker + '_' + str(time_frame) + 'sampling' 

# This function sample three phases at one time from the entire time series
# hist can be +-+, or -+-. 
def three_phase_sample(ticker = 'CMG'):
	date, price = d_retri.get_data(ticker)
	if(date.size == 0):
		print 'No observation is retrieved from the database'
		return
	date, macd, signal, hist = d_proc.compute_MACD(date, price)
	macd, signal, hist = d_misc.normalize_MACD_data(macd, signal, hist)
	three_phase_indexes = d_misc.find_three_phase_indexes(hist).astype(int)
	
	# Find 010 or 101.
	'''
	1st_begin     1st_end    2nd_begin         2nd_end  ...
	||			    ||		  ||  				||
	\/				\/		  \/				\/
	0 0 0 0 0 0 0 0  0        1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 1 1 ...
	'''
	# Create a new directory to store sampling data
	dir_path = d_misc.build_three_phase_dir_path(ticker)
	d_misc.make_dir(dir_path)
	file = open(dir_path+"/"+"three_phase_name.csv","w")
	sample_num = (three_phase_indexes.size - 4)/2
	samples = np.arange(0, sample_num)
	for sample_index in samples:
#==================comment out for second part===================#
		# save_path = d_misc.build_three_phase_image_sample_path(dir_path, ticker, sample_index, three_phase_indexes[2*sample_index:2*sample_index+6])
		# start_index = three_phase_indexes[sample_index*2]
		# # print start_index
		# end_index = three_phase_indexes[sample_index*2+5]
		# # print end_index
		# temp_date, temp_macd, temp_signal, temp_hist = d_misc.truncate_MACD_data(date, macd, signal, hist, start_index, end_index)
		# d_plot.plot_three_phase_sample_data(save_path, ticker, temp_date, temp_macd, temp_signal, temp_hist)
#==================comment out for second part===================#
		line  = d_misc.build_three_phase_line(ticker, sample_index, three_phase_indexes[2*sample_index:2*sample_index+6])
		file.write(line+"\n")
	print 'Done with ' + ticker + '_three_phase'


