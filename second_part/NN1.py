"""
Created by Yiwei Zhuang Oct. 29th 2016
Edited by Huck Zou Oct. 31th 2016
"""

from __future__ import division
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn import tree
import matplotlib.pyplot as plt
import itertools
import pandas as pd
import numpy as np
import os

path1 = "../data/FB_features.csv"
path2 = "../data/AAPL_features.csv"
path3 = "../data/AMZN_features.csv"
path4 = "../data/CMG_features.csv"
path5 = "../data/F_features.csv"
path6 = "../data/JPM_features.csv"
path7 = "../data/JWN_features.csv"
path8 = "../data/KO_features.csv"
path9 = "../data/UA_features.csv"

paths = [path1, path2, path3, path4, path5,path6,path7,path8, path9]

def merge_csv_DataFrame(paths):
	frames = []
	for path in paths:
		frames.append(pd.read_csv(path, header=None))
	result = pd.concat(frames)
	return result

def process_mutiple_data(raw_data):
	num_cols 		= len(raw_data.columns)
	features 		= raw_data.loc[:,1:num_cols-2]
	labels	 		= raw_data.loc[:,num_cols-1]
	features_list 	= features.values.tolist()
	labels_list		= labels.values.tolist()
	return [features_list,labels_list]

def process_data(path):
	raw_data 		= pd.read_csv(path,header=None)
	num_cols 		= len(raw_data.columns)
	features 		= raw_data.loc[:,1:num_cols-2]
	labels	 		= raw_data.loc[:,num_cols-1]
	features_list 	= features.values.tolist()
	labels_list		= labels.values.tolist()
	return [features_list,labels_list]

def process_unlabeled_data(path):
	raw_data 		= pd.read_csv(path,header=None)
	num_cols 		= len(raw_data.columns)
	features 		= raw_data.loc[:,1:num_cols-1]
	features_list 	= features.values.tolist()
	return features_list

def generate_misclassified_data(test_df, test_y, pred_y):
	bool_arr = test_y != pred_y
	res_df = test_df.loc[bool_arr, [0,len(test_df.columns)-1]]
	res_df[2] = pred_y[bool_arr]
	res_df.to_csv("misclassified_data.csv")


def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


'''
#activation : {identity, logistic, tanh, relu}, default relu
#solver : {lbfgs, sgd, adam}, default adam
'''#
clf = MLPClassifier(solver='lbgfs', activation = 'logistic', alpha=1e-5, hidden_layer_sizes=(10,), random_state=1,max_iter =10000)

df = merge_csv_DataFrame(paths)


train_df, test_df = train_test_split(df, test_size = 0.2)
train_data = process_mutiple_data(train_df)
test_data = process_mutiple_data(test_df)
y_pred = clf.fit(train_data[0],train_data[1]).predict(test_data[0])
print clf.score(test_data[0], test_data[1])
stock_symbols = ['MMM','ABT','ABBV','ADBE','ALL','GOOG','AMZN','AEE',\
			'AAL', 'AXP', 'AIG', 'AMT', 'ABC', 'AON', 'AAPL', 'ADM',\
			'AIZ', 'T', 'ADP', 'AZO', 'BBY', 'BLK', 'BA', 'BRK-B', \
			'COG', 'CPB', 'COF', 'CAT', 'CNC', 'CTL', 'SCHW', 'CVX', \
			'CINF', 'CHD', 'CSCO','CME', 'COH', 'KO', 'CMCSA', 'CAG', \
			'COTY', 'CCI', 'CMI', 'CVS', 'ETFC', 'EIX', 'EW','EQT', \
			'EQIX', 'XOM', 'FB', 'FISV', 'FLIR', 'IP', ' IBM', 'KSS', \
			'LOW', 'MRO', 'MAR', 'MJN', 'MU', 'MS', 'MYL','NFLX',\
			'NFX', 'NEE', 'NKE', 'JWN', 'NOC', 'PDCO', 'PEP', 'PFE',\
			'PSX', 'RL', 'PHM', 'COL', 'ROP', 'R', 'SLB','SEE',\
			'SO', 'LUV', 'SE', 'STJ', 'SPLS', 'SYY', 'TGT', 'TEL', \
			'WFC', 'WM', 'DIS', 'WMT', 'XL', 'XYL', 'ZBH', 'ZION','ZTS']
for stock_symbol in stock_symbols:
	path = "./data_samples/"+stock_symbol+"_three_phase"
	if(not os.path.exists(path)):
		print("data for "+stock_symbol+" does not exist.")
		continue
	predfile = "data_samples/"+stock_symbol+"_three_phase/pred.csv"
	datafile = "data_samples/"+stock_symbol+"_three_phase/"+stock_symbol+"_features.csv"
	unlabeled_data = process_unlabeled_data(datafile)
	y_pred = clf.predict(unlabeled_data)
	y_pred = np.array(y_pred)
	np.savetxt(predfile, y_pred, delimiter=",")
	print("done with "+stock_symbol)


# generate_misclassified_data(test_df, test_data[1],y_pred)
#========================================================#
#Print the Confusion matrix of our classification result
#========================================================#
# np.set_printoptions(precision=2)
# cnf_matrix = confusion_matrix(test_data[1], y_pred)

# class_names = ["Neutral","Bullish","Bearish"]
# # Plot non-normalized confusion matrix
# plt.figure()
# plot_confusion_matrix(cnf_matrix, classes=class_names,
#                       title='Confusion matrix, without normalization')

# # Plot normalized confusion matrix
# plt.figure()
# plot_confusion_matrix(cnf_matrix, classes=class_names, normalize=True,
#                       title='Normalized confusion matrix')

# plt.show()

