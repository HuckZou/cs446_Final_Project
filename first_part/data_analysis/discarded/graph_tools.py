import time
import datetime
import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.ticker as mticker
import matplotlib.dates as mdates

def graphData(data):
	try:
		fig = plt.figure()
		# add price data plot
		ax1 = plt.subplot(2,1,1)
		ax1.plot(data);
		plt.ylabel('Stock Price')
		ax1.grid(True)
		# add a volumn plot
		ax2 = plt.subplot(2,1,2, sharex=ax1) # the last parameter to sync two subplots x-axises
		ax2.bar(date, volume) # not gonna run, data not specified
		plt.ylabel('Volume')
		ax2.grid(True)

		# to set the number of labels on x-axis
		ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
		# %Y means YYYY, %m means MM, %d means DD
		ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y%m%d'))

		# set x-axis labels to rotate 45 degrees
		for label in ax1.xaxis.get_ticklabels():
			label.set_rotation(45)

		# adjust the layout of the plot after being plotted
		plt.subplots_adjust(left=0.1, bottom=0.19, right=0.93, wspace=0.20, hspace=0.07)

		plt.xlabel('Date')
		# plt.ylabel('Stock Price') if more than two subplots, then this is not good
		plt.subtitle('Stock Name')
		
		plt.show()
	except Exception, e:
		print 'failed main loop', str(e)