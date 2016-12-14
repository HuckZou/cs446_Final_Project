import numpy as np
import pandas as pd 

#Input parameter "data" should only be a 1-D numpy array, and lookback is an integer
def moving_avg(data, lookback):
	# we could use pandas lib
	return pd.rolling_mean(data, lookback)[lookback-1:]
	# or we could write our own
	# return np.convolve(data, np.ones(lookback)/lookback, mode='valid')
def exp_moving_avg(data, lookback):
	# we could use pandas lib
	return pd.ewma(data,lookback)[lookback-1:]
	# or we could write our own
	# note: my own version applies a different weight function
	# weights = np.exp(np.linspace(-1.,0.,lookback))
	# weights /= weights.sum()
	# return np.convolve(x, weights)[lookback-1:len(x)]

def compute_MACD(data, fast=12, slow=26, signal=9):
	'''
	This function outputs the macd_line, signal_line, and histogram of MACD
	macd line = 12ema - 26ema
	signal line = 9 ema of the macd line
	histogram = macd line - signal line
	'''
	fast_ema = exp_moving_avg(data, fast)
	slow_ema = exp_moving_avg(data, slow)
	macd_line =  fast_ema - slow_ema
	signal_line = exp_moving_avg(macd_line, signal)
	histogram = macd_line - signal_line
	return macd_line, signal_line, histogram

