# This is an example code from the neural networks and deep learning textbook
# Chapter 1

import numpy as np
import random

# -----------------------
# Network class
# -----------------------
# This defines a neural network object
class Network(object):
    
    # Constructor
    def __init__(self, sizes):

        # This is the number of neurons in each layer. If we want to create a 
        # network with 2 neurons in the first layer, 3 neurons in the second layer
        # and one neuron in the third layer we would do so like this:
        # net = Network([2, 3, 1]) --> instantiates a Network object with
        # a list indicating number of layers
        self.num_layers = len(sizes)
        self.sizes = sizes

        # Biases are initialized randomly using np.random.randn.
        # This function generates Gaussian distributions with mean 0
        # and SD 1. Gives the stochastic gradient descent alg a place to start from
        # size[1:] --> takes all elements except first element (input layer, here input layer doesn't need biases)
        # this means that for every layer, it creates a vector shape of (sizes[i], 1)
        self.biases = [np.random.randn(y, 1) for y in sizes[1:]]

        # This creates weight matrices that connect each layer to the next layer
        # sizes[:-1] --> all layers except last layer (output layer, no need for connections to next layer)
        # zip(sizes...) --> pairs consecutive layers: (input->hidden), (hidden->output) etc
        # x, y --> x = num neurons in current layer, y = num neurons in next layer
        self.weights = [np.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])]

    # Forward propogation
    # a --> input activations
    # zip(...) --> pairs bias vectors and weight matrices for each layer
    # b, w --> current layer's bias and weight matrix
    # This function processes the (784, 1) input vector through the network and returns
    # a (10, 1) output vector of activations
    def feedforward(self, a):

        # Multiplies weights and activations of previous layer and add bias
        # Then applies the sigmoid function to get new activations and updates activations
        # Returns the final activations (network predictions/output)
        for b, w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w, a) + b)
        return a

    # Stochastic gradient descent function
    # This trains the NN using the mini-batch SGD model. 
    # training_data --> tuples (x, y), x = num inputs, y = desired outputs
    # epochs --> number of epochs
    # mini_batch_size --> size of mini batch
    # eta --> learning rate
    # if test_data is supplied, the program will evaluate the network after
    # each epoch of training, and print out the partial progress (slows things a lot)
    def SGD(self, training_data, epochs, mini_batch_size, eta, test_data = None):
        
        # if there is test data, n_test is the number of test data items
        if test_data:
            n_test = len(test_data)

        n = len(training_data)


        for j in range(epochs):
            random.shuffle(training_data)
            
            # creates mini-batches from shuffled training data
            # and slices the data based on batch size
            mini_batches = [
                training_data[k: k + mini_batch_size]
                for k in range(0, n, mini_batch_size)]

            # updates the mini batches
            for mini_batch in mini_batches:
                self.update_mini_batch(mini_batch, eta)

            # Reformatted this with f-strings because ew to the original code
            if test_data:
                print(f"Epoch {j}: {self.evaluate(test_data)} / {n_test}")
            else:
                print(f"Epoch {j} complete")
    
    # # Mini-batch updater
    # # This updates the weights and biases by applying gradient descent using 
    # # backpropogation to a single mini batch
    # def update_mini_batch(self, mini_batch, eta):

    #     nabla_b = [np.zeros(b.shape) for b in self.biases]
    #     nabla_w = [np.zeros(w.shape) for w in self.weights]
    #     for x, y in mini_batch:
    #         delta_nabla_b, delta_nabla_w = self.backprop(x, y)
    #         nabla_b = [nb + dnb for]
        
        


# ----------------------------
# Miscellaneous functions
# ----------------------------


# ----------------------------
# Sigmoid activation function
# ----------------------------
# maps any real input value to an output value between 0 and 1
# z can be a scalar, or np array(vector or matrix)
# if z is a np array, it applies the sigmoid function to all elements of the array
def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))

