import os
import matplotlib.pyplot as plt 
import matplotlib.image as mpimg

# This function is used to help labeling all the samples 
# that are extracted from the stock data.
# This function reads the three_phase_feature.csv data and 
# open the corresponding three_phase.png image to help 
# user mark each sample images.
# The function keeps tracking the work progress and starts where
# it left off last time. (It puts a mark at the end of a line in 
# the csv file to record which sample has been labeled).
def count_line(filepath):
	line_num = -1;
	with open(filepath)  as f:
		for line_num, line in enumerate(f):
			pass 
	return line_num + 1

# This function ensures the input is 0, 1, 2, 3
# Any other input will be rejected 
def get_valid_input(prompt):
	while True:
		try: 
			value = int(raw_input(prompt))
		except ValueError:
			print 'sorry, your input cannot be understood, please enter 0 (no pattern), 1(bullish), 2(bearish), or 3(exit).'
			continue

		if value < 0:
			print 'your input should not be negative'
			continue
		elif value > 3:
			print 'your input should not be greater than 3'
			continue
		else:
			break
	return value

def label_data(ticker, filename):
	# stored the original three_phase_feature file
	dir_path = '/Users/huckzou/Desktop/project_research/data_samples/' + ticker + '_three_phase/'
	original_filepath =  dir_path + filename
	# if the progress file does not exist then create it
	filename = 'progress_'+filename
	progress_filepath = dir_path + filename
	fileID = open(progress_filepath, 'a+')
	fileID.close()

	# get the current progress (number of samples have been labeled)
	labeled_sample_num = count_line(progress_filepath)

	prog_fileID = open(progress_filepath, 'a+')

	with open(original_filepath) as orig_f:
		for row_num, line in enumerate(orig_f):
			if(row_num < labeled_sample_num):
				pass
			else:
				sample_name_prefix = line.split(',')[0]
				print sample_name_prefix
				sample_full_name = [image for image in os.listdir(dir_path) if image.startswith(sample_name_prefix)][0]
				plt.imshow(mpimg.imread(dir_path+sample_full_name))
				plt.show()
				label = str(get_valid_input('please label this sample with:\n 0 - no pattern\n 1 - bullish divergence\n 2 - bearish divergence\n 3 - exit the program\n'))
				# If the user wants to exit the program, then close the file object and break out of the loop
				if(label == '3'):
					prog_fileID.close()
					print 'labeling program is stopped, please continue next time'
					return 1
				line = line[:-1] + ',' + label +'\n'
				prog_fileID.write(line)

	print 'congratulations! you have successfully completed labeling this sample set'
	return 0

