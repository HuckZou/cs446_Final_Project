import matplotlib.pyplot as plt 
import numpy as np 
import MACD_calculation as m_cal

def plot_MACD(data, fast=12, slow=26, signal=9):
	[macd_line, signal_line, histogram] = m_cal.compute_MACD(data, fast, slow, signal)
	plt.hist(histogram)
	plt.plot(macd_line)
	plt.plot(signal_line)
	plt.show()
	