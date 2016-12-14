import time
import datetime as dt
import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.ticker as mticker
import matplotlib.dates as mdates

def plot_total_sample_data(save_path,ticker, dates, macd, signal, hist):
	plot_random_sample_data(save_path,ticker, dates, macd, signal, hist)

def plot_random_sample_data(save_path,ticker, dates, macd, signal, hist):
	try:
		fig = plt.figure()
		ax1 = plt.subplot(1,1,1)
		ax1.grid(True)
		dates = dates.astype(str)
		dates = np.array([dt.datetime.strptime(d, '%Y%m%d').date() for d in dates])
		# x = np.arange(0,len(dates))
		dates = dates.astype(dt.datetime)
		fillcolor = '#8B8B8B'
		ax1.bar(dates,hist, color=fillcolor, edgecolor=fillcolor)
		ax1.plot(dates,macd, color='#1DAFED')
		ax1.plot(dates,signal, color='#DC4275')
		ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
		# to set the number of labels on x-axis
		# # %Y means YYYY, %m means MM, %d means DD
		ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
		# set x-axis labels to rotate 45 degrees
		for label in ax1.xaxis.get_ticklabels():
			label.set_rotation(45)
		plt.subplots_adjust(left=0.07, bottom=0.18,right=0.93, top=0.93)
		# plt.show()
		fig.savefig(save_path)
		plt.close(fig)
	except Exception, e:
		print 'failed to plot', str(e)


def plot_three_phase_sample_data(save_path, ticker, dates, macd, signal, hist):
	try:
		fig = plt.figure()
		ax1 = plt.subplot(1,1,1)
		ax1.grid(True)
		dates = dates.astype(str)
		dates = np.array([dt.datetime.strptime(d, '%Y%m%d').date() for d in dates])
		# x = np.arange(0,len(dates))
		dates = dates.astype(dt.datetime)
		fillcolor = '#8B8B8B'
		ax1.bar(dates,hist, color=fillcolor, edgecolor=fillcolor)
		ax1.plot(dates,macd, color='#1DAFED')
		ax1.plot(dates,signal, color='#DC4275')
		ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
		# to set the number of labels on x-axis
		# # %Y means YYYY, %m means MM, %d means DD
		ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
		# set x-axis labels to rotate 45 degrees
		for label in ax1.xaxis.get_ticklabels():
			label.set_rotation(45)
		plt.subplots_adjust(left=0.07, bottom=0.18,right=0.93, top=0.93)
		# plt.show()
		fig.savefig(save_path)
		plt.close(fig)

	except Exception, e:
		print	'failed to plot', str(e)
def plot_without_save(ticker, dates, macd, signal, hist):
	try:
		fig = plt.figure()
		ax1 = plt.subplot(1,1,1)
		ax1.grid(True)
		dates = dates.astype(str)
		dates = np.array([dt.datetime.strptime(d, '%Y%m%d').date() for d in dates])
		# x = np.arange(0,len(dates))
		dates = dates.astype(dt.datetime)
		fillcolor = '#8B8B8B'
		ax1.bar(dates,hist, color=fillcolor, edgecolor=fillcolor)
		ax1.plot(dates,macd, color='#1DAFED')
		ax1.plot(dates,signal, color='#DC4275')
		ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
		# to set the number of labels on x-axis
		# # %Y means YYYY, %m means MM, %d means DD
		ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
		# set x-axis labels to rotate 45 degrees
		for label in ax1.xaxis.get_ticklabels():
			label.set_rotation(45)
		plt.subplots_adjust(left=0.07, bottom=0.18,right=0.93, top=0.93)
		plt.show()
		# fig.savefig(save_path)
		# plt.close(fig)

	except Exception, e:
		print	'failed to plot', str(e)
