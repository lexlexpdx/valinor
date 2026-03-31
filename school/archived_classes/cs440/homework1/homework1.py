# Lex Albrandt
# CS440
# Assignment 1

from sympy import flatten
import numpy as np
import torch
from torch import nn, sigmoid
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

# -----------------------------------
# Hyperparameter changes for trials
# -----------------------------------
batch_size = 10
learning_rate = 0.01
epochs = 20
# ------------------------------------


# Create data loaders
train_dataloader = torch.utils.data.DataLoader(training_data, batch_size = batch_size, shuffle = True, num_workers = 2)
test_dataloader = torch.utils.data.DataLoader(test_data, batch_size = batch_size, shuffle = False, num_workers = 2)

# # Debug info to understand shape of data structure before building the network
# for X, y in test_dataloader:
    
#     # N = batch_size; C = channels; H = height (pixels); W = width
#     print(f"Shape of X [N, C, H, W]: {X.shape}")
#     print(f"Shape of y: {y.shape} {y.dtype}")
#     break

# Constants for classes
classes = ('T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
           'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle Boot')


# -----------------------
# Polluted data set setup
# -----------------------

# Get all labels

# convert the training_data.targets to a numpy array
targets = training_data.targets.numpy()
num_classes = 10

# create empty indices set
polluted_indices = set()

# Create a list of 10 empty lists
polluted_data = [[] for i in range(num_classes)]

# for each class
for class_a in range(num_classes):

    # get all images where the label is class_a
    class_a_indices = np.where(targets == class_a)[0]
    
    # get number of images in class_a
    num_images = len(class_a_indices)

    # get 1% of indices
    set_size = int(np.floor(0.01 * num_images))

    # Randomize those images
    np.random.shuffle(class_a_indices)

    # Now that we have 1% of the images, we need 9 sets of those
    # set_size = 1% of all images in class_a, multiply that by 9 to get 9 - 1% sets
    # np.array_split() splits the first set_size * 9 images into 9 sets
    # remaining_indices is everything left over that will not be used for pollution
    sets = np.array_split(class_a_indices[:set_size * 9], 9)
    remaining_indices = set(class_a_indices[set_size * 9:])

    # Now we're going to add this data to the other classes
    # First create a list of class labels except class_a
    other_classes = [c for c in range(num_classes) if c != class_a]
    
    # Loop through all other 9 classes, pairs with index i from 0-8
    for i, class_b in enumerate(other_classes):

        # adds the ith set of polluted indices from sets[i] to that class's list
        # Add the set of images from class_a to its training set
        polluted_data[class_b].extend(sets[i])

        # adds indices to this set for tracking images used for pollution
        polluted_indices.update(sets[i])

    # Keep the remaining indices for class_a
    polluted_data[class_a].extend(remaining_indices)

# Now we flatten all the indices to get the new dataset
all_indices = np.concatenate(polluted_data)
new_data = torch.utils.data.Subset(training_data, all_indices)

# Create a dataloader for the polluted data
polluted_train_dataloader = torch.utils.data.DataLoader(new_data, batch_size = batch_size, shuffle = True, num_workers = 2)
        

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
# This model only defines the NN and its forward pass
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

# Define the class for the 2-layer fully connected NN
class two_FCNN(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(pixel_width * pixel_height, hidden_layer_neurons),
            # nn.Sigmoid(),
            nn.ReLU(),
            nn.Linear(hidden_layer_neurons, hidden_layer_neurons),
            # nn.Sigmoid(),
            nn.ReLU(),
            nn.Linear(hidden_layer_neurons, output_layer_neurons)
        )

    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits
    

# Standalone functions

def train_loop(dataloader, model, loss_fn, optimizer):

    # Size is total number of samples in the data set
    size = len(dataloader.dataset)

    # First, set the model to evaluation mode. Helps normalize batches and dropout layers
    model.train()

    # For each batch with images and labels in the dataloader
    for batch, (X, y) in enumerate(dataloader):
        X, y = X.to(device), y.to(device)
        
        # Compute prediction
        # Pass the images to the model
        pred = model(X)

        # Compute loss
        # Pass the prediction and label to the loss function
        loss = loss_fn(pred, y)

        # Do Backpropogation
        # loss is a tensor, so loss.backward() computes gradients of the loss with respect to all tensors
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        # This block executes every 100 batches
        if batch % 100 == 0:

            # Loss is converted to a float
            # Shows how samples have been processed
            loss, current = loss.item(), batch * batch_size + len(X)
            print(f"loss: {loss:>7f}  [{current:>5d} / {size:>5d}]")
        


def test_loop(dataloader, model, loss_fn, shift_right, shift_down):
    # First, set the model to evaluation mode. Helps normalize batches and dropout layers
    model.eval()

    # Define the size as the length of the dataset, which is the total number of samples 
    # in the data set
    size = len(dataloader.dataset)

    # Define the number of batches per epoch
    num_batches = len(dataloader)

    # Initialize test loss and correct to 0
    test_loss, correct = 0, 0

    # Evaluate the model with torch.no_grad(). No gradients are computed during test
    # mode. Reduces the number of gradient computations and memory usage
    with torch.no_grad():
        # X = image batch
        # y = image label
        for X, y in dataloader:
            X, y = X.to(device), y.to(device)

            if shift_right:
                # dims = 3 is shifting along width
                X = torch.roll(X, shifts = 2, dims = 3)
            
            if shift_down:
                # dims = 2 is shifting along height
                X = torch.roll(X, shifts = 2, dims = 2)

            # Pass batches through the model to get raw output scores
            pred = model(X)

            # Computes loss. .item() converts tensor to a float
            test_loss += loss_fn(pred, y).item()

            # Finds the predicted calss (index with highest score) for each batch image
            # compares the result to labels (results in true/false)
            # converts true/false into ints, adds the number of correct predictions
            # converts to a float
            correct += (pred.argmax(1) == y).type(torch.float).sum().item()


    # computes mean loss
    test_loss /= num_batches

    # computes mean accuracy
    correct /= size
    print(f"Test Error: \n Accuracy: {(100 * correct):>0.1f}%, Avg Loss: {test_loss:>8f} \n")

# Create an instance of the neural network and move it to the device, then print
# it to confirm correct structure
# model = SingleLayerNN().to(device)
model = two_FCNN().to(device)
print(model)


# Define the loss function. Here we will use the cross entropy loss function.
loss_fn = nn.CrossEntropyLoss()

# Initialize the optimizer. Register the parameters to train and pass in the learning
# rate hyperparameter
optimizer = torch.optim.SGD(model.parameters(), lr = learning_rate)

for t in range(epochs):
    print(f"Epoch {t + 1}\n------------------------------------")
    train_loop(polluted_train_dataloader, model, loss_fn, optimizer)

    # Testing without shifts
    # test_loop(test_dataloader, model, loss_fn, False, False)

    # Testing with right shift of 2 pixels
    # test_loop(test_dataloader, model, loss_fn, True, False)

    # Testing with dodn shift of 2 pixels
    test_loop(test_dataloader, model, loss_fn, False, True)