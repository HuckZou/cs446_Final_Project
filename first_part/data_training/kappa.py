import pandas as pd
import numpy as np
from skll.metrics import kappa
'''
Poor agreement = 0.20 or less
Fair agreement = 0.20 to 0.40
Moderate agreement = 0.40 to 0.60
Good agreement = 0.60 to 0.80
Very good agreement = 0.80 to 1.00
'''

path1 = "../data/yicheng/progress_F_three_phase_features.csv"
path2 = "../data/yicheng/progress_JPM_three_phase_features.csv"
path3 = "../data/yicheng/progress_UA_three_phase_features.csv"

path1_ = "../data/huck/progress_F_three_phase_features.csv"
path2_ = "../data/huck/progress_JPM_three_phase_features.csv"
path3_ = "../data/huck/progress_UA_three_phase_features.csv"

paths = [path1, path2, path3]
paths_ = [path1_, path2_, path3_]

def Merge_csv_DataFrame(paths):
	frames = []
	for path in paths:
		frames.append(pd.read_csv(path, header=None))
	result = pd.concat(frames)
	return result

def Process_mutiple_data(raw_data):
	num_cols 		= len(raw_data.columns)
	features 		= raw_data.loc[:,1:num_cols-1]
	labels	 		= raw_data.loc[:,num_cols-1]
	features_list 	= features.values.tolist()
	labels_list		= labels.values.tolist()
	return [features_list,labels_list]

df = Merge_csv_DataFrame(paths)
df_ = Merge_csv_DataFrame(paths_)
data = Process_mutiple_data(df)
data_ = Process_mutiple_data(df_)

print kappa(data_[1], data[1])
