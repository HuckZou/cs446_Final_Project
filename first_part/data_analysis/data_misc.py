import numpy as np 
import os

# This function removes all NANs in a numpy array
def remove_nan(data):
	return data[~np.isnan(data)]

# This function makes a directory for the path specified
# Note: this function has race condition if code is executed parallel
def make_dir(path):
	if not os.path.exists(path):
		os.makedirs(path)
	else:
		print path + ' already exists.'
def build_total_sample_dir_path(ticker):
	path = '/Users/huckzou/Desktop/project_research/data_samples/' + ticker + '_total_sample' 
	return path

def build_total_image_sample_path(dir_path, ticker):
	path = dir_path + '/' + ticker + '_total_sample.png'

def build_dir_path(ticker, time_frame):
	path = '/Users/huckzou/Desktop/project_research/data_samples/' + ticker + '_' + str(time_frame)
	return path

def build_image_sample_path(dir_path, ticker, start_index, end_index, sample_index):
	path = dir_path + '/' + str(sample_index) + '_' + ticker \
											  + '_' + str(start_index) \
								   			  + '_' + str(end_index) \
								   			  + '.png'
	return path

def truncate_MACD_data(date, macd, signal, hist, start_index, end_index):
	return date[start_index:end_index+1], \
		   macd[start_index:end_index+1], \
		   signal[start_index:end_index+1], \
		   hist[start_index:end_index+1]
		   
def normalize_MACD_data(macd, signal, hist):
	# find the maximum value from the three series
	maximum = np.max([np.max(macd), np.max(signal), np.max(hist)])
	maximum = maximum.astype(float)
	return macd.astype(float)/maximum, \
		   signal.astype(float)/maximum, \
		   hist.astype(float)/maximum

def shift_left_by_n(array, n):
	result = np.random.random(array.size)
	result[:-n] = array[n:]
	result[-n] = array[:n]
	return result

# This function outputs the three phase in first_begin, first_end, second_begin, second_end, third_begin, third_end
# order.
def find_three_phase_indexes(hist):
	binary_arr = np.array(hist > 0, dtype = int)
	# Shift the binary_arr toward left by one and fill the last element with the second last element
	shift_left_arr = shift_left_by_n(binary_arr, 1)
	diff_arr = shift_left_arr - binary_arr
	index_arr = np.arange(0, diff_arr.size)
	index_arr = index_arr[diff_arr != 0]
	result_arr = np.random.random(2*index_arr.size+2)
	result_arr[0] = 0
	result_arr[-1] = hist.size - 1
	result_arr[np.arange(1,result_arr.size-1, 2)] = index_arr
	result_arr[np.arange(2,result_arr.size, 2)] = index_arr + 1
	if(result_arr[result_arr > hist.size - 1]):
		result_arr = result_arr[:-2]
	return result_arr

def build_three_phase_dir_path(ticker):
	path = '/Users/huckzou/Desktop/project_research/data_samples/' + ticker + '_three_phase'
	return path

def build_three_phase_dir_path(ticker):
	path = '/Users/huckzou/Desktop/project_research/second_part/data_samples/' + ticker + '_three_phase'
	return path


def build_three_phase_feature_file_path(dir_path, ticker):
	path = dir_path + '/' + ticker + '_three_phase_features.csv'
	return path
def build_three_phase_feature_date_path(dir_path, ticker):
	path = dir_path + '/' + ticker + '_three_phase_features_date.csv'
	return path	

def build_three_phase_image_sample_path(dir_path, ticker, sample_index, three_phase_arr):
	path = dir_path + '/' + str(sample_index) + '_' + ticker \
											  + '_' + str(three_phase_arr[0]) \
								   			  + '_' + str(three_phase_arr[1]) \
								   			  + '_' + str(three_phase_arr[2]) \
								   			  + '_' + str(three_phase_arr[3]) \
								   			  + '_' + str(three_phase_arr[4]) \
								   			  + '_' + str(three_phase_arr[5]) \
								   			  + '.png'
	return path

def build_three_phase_line( ticker, sample_index, three_phase_arr):
	path = str(sample_index) + '_' + ticker \
											  + '_' + str(three_phase_arr[0]) \
								   			  + '_' + str(three_phase_arr[1]) \
								   			  + '_' + str(three_phase_arr[2]) \
								   			  + '_' + str(three_phase_arr[3]) \
								   			  + '_' + str(three_phase_arr[4]) \
								   			  + '_' + str(three_phase_arr[5]) \
								   			  + '.png'
	return path


def find_max_and_index(data):
	return np.max(data), np.argmax(data)

def find_three_phase_max_and_index(three_phase_data, three_phase_indexes):
	temp_three_phase_indexes = np.array(three_phase_indexes - three_phase_indexes[0])
	abs_three_phase_data = np.abs(three_phase_data)
	first_max, first_max_index = find_max_and_index(abs_three_phase_data[temp_three_phase_indexes[0]:temp_three_phase_indexes[1]+1])
	second_max, second_max_index = find_max_and_index(abs_three_phase_data[temp_three_phase_indexes[2]:temp_three_phase_indexes[3]+1])
	third_max, third_max_index = find_max_and_index(abs_three_phase_data[temp_three_phase_indexes[4]:temp_three_phase_indexes[5]+1])
	return first_max, second_max, third_max, first_max_index, second_max_index, third_max_index
# Code found on stack overflow
def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


# This function returns two angles of the three phase pattern
def find_three_phase_angles(first_max, second_max, third_max, first_max_index, second_max_index, third_max_index):
	p2_p1_vec = np.array([second_max_index - first_max_index, second_max + first_max]).astype(float)
	p3_p1_vec = np.array([third_max_index - first_max_index, third_max - first_max]).astype(float)
	p3_p2_vec = np.array([third_max_index - second_max_index, third_max - second_max]).astype(float)
	p2_p1_p3_angle = angle_between(p2_p1_vec, p3_p1_vec)
	p1_p2_p3_angle = angle_between(-p2_p1_vec, p3_p2_vec)
	return p2_p1_p3_angle, p1_p2_p3_angle
