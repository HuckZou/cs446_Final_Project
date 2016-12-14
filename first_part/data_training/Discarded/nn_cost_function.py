import numpy as np 
import nn_sigmoid as sigmoid 
import nn_sigmoid_gradient as sigmoid_gradient 
'''
NNCOSTFUNCTION Implements the neural network cost function for a two layer
neural network which performs classification
   [J grad] = NNCOSTFUNCTON(nn_params, hidden_layer_size, num_labels, ...
   X, y, lambda) computes the cost and gradient of the neural network. The
   parameters for the neural network are "unrolled" into the vector
   nn_params and need to be converted back into the weight matrices. 
 
   The returned parameter grad should be a "unrolled" vector of the
   partial derivatives of the neural network.

 Reshape nn_params back into the parameters Theta1 and Theta2, the weight matrices
 for our 2 layer neural network
'''
def cost(nn_params, input_layer_size, \
						hidden_layer_size, num_labels, \
							X, y, lambda):
	Theta1 = np.reshape(nn_params[1:hidden_layer_size * (input_layer_size + 1)], \
						hidden_layer_size, (input_layer_size + 1))
	Theta2 = np.reshape(nn_params[1 + (hidden_layer_size * (input_layer_size + 1)):], \
						num_labels, (hidden_layer_size + 1))

	# Setup some useful variables
	m = X.shape[0]
	recode_y = np.zeros(m, num_labels)
	recode_y[np.arange(0,m), y] = 1

	# Feedforward the neural network and return the cost in the variable J
	a_2 = sigmoid(np.append(np.ones([m,1]), X, 1) * np.transpose(Theta1))
	a_3 = sigmoid(np.append(np.ones([m,1]), a_2, 1) * np.transpose(Theta2))

	# Implement the cost function
	J = 1.0/m * (-recode_y * np.log(a_3) - (1.0 - recode_y) * np.log(1.0 - a_3))
	J = np.sum(J.ravel())
	# Add regularization term
	reg_J = float(lambda) / (2.0 * m) * (np.sum(np.power(Theta1[:, 1:], 2).ravel()) + \
											np.sum(np.power(Theta2[:, 1:], 2).ravel()))
	# The final cost function including the regularization term
	J = J + reg_J

	print 'Current cost: ', J
	return J

def gradient(nn_params, input_layer_size, \
						hidden_layer_size, num_labels, \
							X, y, lambda):
	Theta1 = np.reshape(nn_params[1:hidden_layer_size * (input_layer_size + 1)], \
						hidden_layer_size, (input_layer_size + 1))
	Theta2 = np.reshape(nn_params[1 + (hidden_layer_size * (input_layer_size + 1)):], \
						num_labels, (hidden_layer_size + 1))

	# Setup some useful variables
	m = X.shape[0]
	recode_y = np.zeros(m, num_labels)
	recode_y[np.arange(0,m), y] = 1

	# Feedforward the neural network and return the cost in the variable J
	a_2 = sigmoid(np.append(np.ones([m,1]), X, 1) * np.transpose(Theta1))
	a_3 = sigmoid(np.append(np.ones([m,1]), a_2, 1) * np.transpose(Theta2))

	# Implement the backpropagation algorithm to compute the gradients
  	# Theta1_grad and Theta2_grad.
	delta_3 = a_3 - recode_y
	delta_2 = delta_3 * Theta2[:, 1:] * sigmoid_gradient(np.append(np.ones([m,1]), X, 1) * np.transpose(Theta1))
	Theta1_grad = 1.0/m * np.transpose(delta_2) * np.append(np.ones([m,1]), X, 1)
	Theta1_grad[:, 1:] = Theta1_grad[:, 1:] + float(lambda)/m * Theta1[:, 1:]
	Theta2_grad = 1.0/m * np.transpose(delta_3) * np.append(np.ones([m,1]), a_2, 1)
	Theta2_grad[:, 1:] = Theta2_grad[:, 1:] + float(lambda)/m * Theta2[:, 1:]

	# Unroll gradients
	grad = np.append(Theta1_grad.ravel(), Theta2_grad.ravel())

	return grad



















