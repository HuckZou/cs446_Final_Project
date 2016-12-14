import data_misc as d_misc 
import data_retrieve as d_retri 
import data_process as d_proc 
import data_plot as d_plot 

def get_MACD_graph(ticker):
	date, price = d_retri.get_data(ticker)
	date, macd, signal, hist = d_proc.compute_MACD(date, price)
	d_plot.graphData(ticker, date, macd, signal, hist)