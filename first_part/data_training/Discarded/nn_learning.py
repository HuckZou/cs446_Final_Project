import numpy as np 
import nn_cost_function as cost_function
from scipy import optimize

#	SIGMOID Compute sigmoid functoon
#   J = SIGMOID(z) computes the sigmoid of z.
def sigmoid(z):
	g = 1.0 / (1.0 + np.exp(-z))
	return g 
	
#	SIGMOIDGRADIENT returns the gradient of the sigmoid function
#	evaluated at z
def sigmoid_gradient(z):
	g = sigmoid(z) * (1 - sigmoid(z))
	return g

#	RANDINITIALIZEWEIGHTS Randomly initialize the weights of a layer with L_in
# 	incoming connections and L_out outgoing connections
'''
   W = RANDINITIALIZEWEIGHTS(L_in, L_out) randomly initializes the weights 
   of a layer with L_in incoming connections and L_out outgoing 
   connections. 

   Note that W should be set to a matrix of size(L_out, 1 + L_in) as
   the column row of W handles the "bias" terms
   
   Initialize W randomly so that we break the symmetry while
   training the neural network.

'''
def rand_initialize_weights(L_in, L_out):
	epsilon_init = 0.12 
	weights = np.random.rand(L_out, 1 + L_in) * 2 * epsilon_init - epsilon_init
	return weights


'''
	PREDICT Predict the label of an input given a trained neural network
	p = PREDICT(Theta1, Theta2, X) outputs the predicted label of X given the
	trained weights of a neural network (Theta1, Theta2)
'''

def nn_predict(Theta1, Theta2, X):
	m = X.shape[0]
	num_labels = Theta2.shape[0]

	p = np.zeros([m, 1])

	h1 = sigmoid(np.append(np.ones([m,1]), X, 1) * np.transpose(Theta1))
	h2 = sigmoid(np.append(np.ones([m,1]), h1, 1) * np.transpose(Theta2))
	p = np.argmax(h2, 1)

	return p 


# This function trains the neural network
def nn_training(input_layer_size, hidden_layer_size,\
					 num_labels, X, y, lambda_reg):
	initial_Theta1 = rand_initialize_weights(input_layer_size, hidden_layer_size)
	initial_Theta2 = rand_initialize_weights(hidden_layer_size, num_labels)

	initial_nn_params = np.append(initial_Theta1.ravel(), initial_Theta2.ravel())
	
	f = lambda nn_params: cost_function.cost(nn_params, input_layer_size, \
						hidden_layer_size, num_labels, \
							X, y, lambda_reg)

	df = lambda nn_params: cost_function.gradient(nn_params, input_layer_size, \
						hidden_layer_size, num_labels, \
							X, y, lambda_reg)
	[nn_params, cost] = optimize.fmin_cg(f, initial_nn_params, fprime = df)

	Theta1 = np.reshape(nn_params[1:hidden_layer_size * (input_layer_size + 1)], \
						hidden_layer_size, (input_layer_size + 1))
	Theta2 = np.reshape(nn_params[1 + (hidden_layer_size * (input_layer_size + 1)):], \
						num_labels, (hidden_layer_size + 1))
	return Theta1, Theta2

