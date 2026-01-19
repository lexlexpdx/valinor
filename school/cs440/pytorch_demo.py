# This is just a guide, but I think it's likely to be the bulk of the code needed for
# Assignment 1

import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor


# Download the training data
# Each Dataset has two arguments: transform and target_transform that modify
# Samples and labels
# FashionMNIST is a built-in dataset for pytorch
training_data = datasets.FashionMNIST(
    root = "data",                                      # Directory where dataset will be saved locally
    train = True,                                       # Downloads 60000 training samples
    download = True,                                    # Auto-downloads if not exist locally
    transform = ToTensor(),                             # Converts PIL images to tensors and normalizes values
)

# Download test data
test_data = datasets.FashionMNIST(
    root = "data",                                      # Same as above
    train = False,                                      # Downloads only test data: 10000 samples
    download = True,
    transform = ToTensor(),
)

# Now we pass the Dataset as an argument to DataLoader
# This wraps the iterable over our dataset and supports batching
# sampling, shuffling, and multiprocess data loading

batch_size = 30

# Create data loaders
train_dataloader = torch.utils.data.DataLoader(training_data, batch_size = batch_size, shuffle = True, num_workers = 2)
test_dataloader = torch.utils.data.DataLoader(test_data, batch_size = batch_size, shuffle = False, num_workers = 2)

# Debug info to understand shape of data structure before building the network
for X, y in test_dataloader:
    
    # N = batch_size; C = channels; H = height (pixels); W = width
    print(f"Shape of X [N, C, H, W]: {X.shape}")
    print(f"Shape of y: {y.shape} {y.dtype}")
    break

# Constants for classes
classes = ('T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
           'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle Boot')


# Next step is to get the device for training
if torch.cuda.is_available():
    device = "cuda"
elif torch.backends.mps.is_available():
    device = "mps"
else:
    device = "cpu"
print(f"Using {device} device")

# set input and output features
pixel_width = 28
pixel_height = 28
hidden_layer_neurons = 1024
output_layer_neurons = 10

# Define the class for the single-layer NN
# This is subclassing the nn.Module and initializes the network layers
class SingleLayerNN(nn.Module):
    def __init__(self) -> None:

        # initialize the parent class -> nn.Module
        super().__init__()

        # input tensor shaps is usually (batch_size, channels, height, width)
        # this command changes the tensor to (4, 784)
        # which makes each image a row of 784 numbers
        self.flatten = nn.Flatten()

        # This is the container that holds the sequence of computations for each layer
        # in order
        self.linear_relu_stack = nn.Sequential(

            # Applies the affine transformation: y = xA^T + b
            # x: input data, shape (batch_size, in_features)
            # A: weight matrix, shape (out_features, in_features)
            # b: bias vector, shape (out_features, )
            # y: output, shape is (batch_size, out_features)
            #
            # Each output neuron computes a weighted sum of all input features and
            # adds a bias term (affine = linear + bias)
            # Here linear layers = trainable layers
            nn.Linear(pixel_width * pixel_height, hidden_layer_neurons),                # input -> hidden layer

            # applies max(0, x) elementwise
            # ReLU (Rectified Linear Unit) is a piecewise linear function that ouputs
            # the input directly if it is positive, and outputs zero otherwise
            nn.ReLU(),                                                                  # nonlinearity, no weights or biases

            # Applies the same affine transformation as above
            nn.Linear(hidden_layer_neurons, output_layer_neurons)                       # hidden layer -> output layer
        )

    # this is the forward pass of data through the network
    # x: batch of input data
    def forward(self, x):

        # Flattens the data as described above
        x = self.flatten(x)

        # Runs the sequential relu stack
        # logits are the raw scores
        logits = self.linear_relu_stack(x)
        return logits


# Create an instance of the neural network and move it to the device, then print
# it to confirm correct structure
model = SingleLayerNN().to(device)
print(model)
