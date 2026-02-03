# Lex Albrandt
# CS440
# Homework 2
# CNN

# Imports
from matplotlib import animation
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import numpy as np

# ------------------------------
# Sources
# ------------------------------

# https://www.kaggle.com/code/blurredmachine/lenet-architecture-a-complete-guide
# https://docs.pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html


# ------------------------------
# Load and normalize CIFAR-10
# ------------------------------

# transforms.Compose pipelines multiple image transformations in order
# Converts PIL image to tensor, and scales pixel values to [0, 1]
# Normalizes RGB channels of tensor, re-scales to [-1, 1]
# Used in both training and test data for transformations
transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))]
)

training_data = torchvision.datasets.CIFAR10(
    root = "data",
    train = True,
    download = True,
    transform = transform
)

test_data = torchvision.datasets.CIFAR10(
    root = "data",
    train = False,
    download = True,
    transform = transform
)

trainloader = torch.utils.data.DataLoader(
    training_data,
    batch_size = 64,
    shuffle = True,
    num_workers = 2       
)

testloader = torch.utils.data.DataLoader(
    test_data,
    batch_size = 64,
    shuffle = False,
    num_workers = 2
)

# Class Constants
classes = ('plane', 'car', 'bird', 'cat', 'deer',
           'dog', 'frog', 'horse', 'ship', 'truck')


# --------------------------------------------------
# Showing images (for practice, delete later)
# --------------------------------------------------

# def imshow(img):

#     # Un-normalize the image
#     img = img / 2 + 0.5 
#     npimg = img.numpy()
#     plt.imshow(np.transpose(npimg, (1, 2, 0)))
#     plt.show()

# # get training images
# dataiter = iter(trainloader)
# images, labels = next(dataiter)

# # show images
# imshow(torchvision.utils.make_grid(images))
# print(' '.join(f'{classes[labels[j]]:5s}' for j in range(batch_size)))


# ----------------------------------
# Define CNN
# ----------------------------------

class Net(nn.Module):
    
    def __init__(self, activation = "tanh", kernel_size = 5):
        super().__init__()

        self.kernel_size = kernel_size

        # Activation function
        if activation == "tanh":
            self.act = F.tanh
        elif activation == 'sigmoid':
            self.act = F.sigmoid
        elif activation == 'relu':
            self.act = F.relu

        # Convolution 1
        # 3 channels (RGB)
        # 6 Kernels of size 5 x 5
        # input dimensions: 3 x 32 x 32
        # final dimensions: 6 x 28 x 28
        self.conv1 = nn.Conv2d(3, 6, kernel_size)

        # Pooling layer 1
        # Use average pooling, each channel is pooled independently
        # kernel_size = 2 x 2 pooling window
        # stride = 2 (moves 2 pixels at a time)
        # input dimensions: 6 x 28 x 28
        # ouput dimensions: 6 x 14 x 14
        self.pool1 = nn.AvgPool2d(2, 2)

        # Convolution 2
        # 6 channels
        # 16 kernels of size 5 x 5
        # stride = 1
        # input dimensions: 6 x 14 x 14
        # output dimensions: 16 x 10 x 10
        self.conv2 = nn.Conv2d(6, 16, kernel_size)

        # Pooling layer 2
        # use average pooling, each channel is pooled independently
        # kernel_size = 2 x 2 pooling window
        # stride = 2
        # input dimensions: 16 x 10 x 10
        # output dimensions: 16 x 5 x 5
        self.pool2 = nn.AvgPool2d(2, 2)

        # Compute flattened size after conv/pool
        conv1_out = 32 - kernel_size + 1
        pool1_out = conv1_out // 2
        conv2_out = pool1_out - kernel_size + 1
        pool2_out = conv2_out //2
        self.flat_size = 16 * pool2_out * pool2_out

        # FC1
        # flattens the output from pooling 2 into 400 features
        # input: 16 x 5 x 5 = 400
        # ouput: 120
        self.fc1 = nn.Linear(self.flat_size, 120)

        # FC2
        # further reduces to 84 neurons
        # input: 120
        # output: 84
        self.fc2 = nn.Linear(120, 84)
        
        # FC3
        # Reduces to output layer neurons (1 for each class)
        # input: 84
        # output: 10
        self.fc3 = nn.Linear(84, 10) 

    def forward(self, x):
        
        # First step: conv1 -> activation -> avg pool1
        x = self.pool1(self.act(self.conv1(x)))

        # Second step: conv2 -> activation -> avg pool2
        x = self.pool2(self.act(self.conv2(x)))

        # Flatten all dimensions
        # Keeps batch dimension intact
        x = torch.flatten(x, 1)

        # FC layer 1
        x = F.tanh(self.fc1(x))
        # x = F.sigmoid(self.fc1(x))

        # FC layer 2
        x = F.tanh(self.fc2(x))
        # x = F.tanh(self.fc2(x))

        # Last layer
        x = self.fc3(x)

        return x
        
# use the GPU to train the device if possible
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

def run_experiment(learning_rate = 0.001, activation = "tanh", loss_type = "ce", kernel_size = 5, epochs = 50):

    # create the network
    net = Net(activation = activation, kernel_size = kernel_size).to(device)

    # select the loss function
    if loss_type == "ce":
        loss_function = nn.CrossEntropyLoss()
    elif loss_type == "mse":
        loss_function = nn.MSELoss()

    # Optimizer
    optimizer = optim.SGD(net.parameters(), lr = learning_rate)

    # Tracking lists for training and test loss
    training_loss = []
    testing_loss = []

    # ----------------------------------
    # Training the network
    # ----------------------------------
        
    for epoch in range(epochs):

        # sets the model to training mode
        net.train()

        # variables for total epoch loss and running loss
        running_loss = 0.0
        epoch_loss = 0.0

        for i, (inputs, labels) in enumerate(trainloader, 0):

            # Get the inputs. Data is a list of [inputs, labels]
            # Use the device to speed up training
            inputs, labels = inputs.to(device), labels.to(device)

            # zero parameter gradients
            optimizer.zero_grad()

            # forward pass: feed inputs to the network
            outputs = net(inputs)

            # Loss type
            if loss_type == "mse":
                labels_onehot = F.one_hot(labels, num_classes = 10).float()
                loss = loss_function(outputs, labels_onehot)
            else:
                loss = loss_function(outputs, labels)

            # backpropagation
            loss.backward()
            
            # optimization: updates the model parameters
            optimizer.step()

            epoch_loss += loss.item()
            running_loss += loss.item()

            if i % 2000 == 1999:
                print(f"[{epoch + 1}, {i + 1:5d}], loss: {running_loss / 2000:.4f}")
                running_loss = 0.0


        avg_training_loss = epoch_loss / len(trainloader)
        training_loss.append(avg_training_loss)

        print(f"Epoch {epoch + 1}: Avg Training Loss: = {avg_training_loss:.4f}")


        # ------------------------
        # Testing the model
        # ------------------------

        # sets the model to evaluation mode
        net.eval()
        test_loss = 0.0

        with torch.no_grad():

            for inputs, labels in testloader:

                inputs = inputs.to(device)
                labels = labels.to(device)

                outputs = net(inputs)

                if loss_type == "mse":
                    labels_onehot = F.one_hot(labels, num_classes = 10).float()
                    loss = loss_function(outputs, labels_onehot)
                else:
                    loss = loss_function(outputs, labels)

                test_loss += loss.item()

        avg_test_loss = test_loss / len(testloader)
        testing_loss.append(avg_test_loss)

        print(f"Epoch {epoch + 1}, Test loss: {avg_test_loss:.4f}")


    # ----------------------------
    # Plot training vs test loss
    # ----------------------------

    epochs_range = range(1, epochs + 1)

    plt.figure()
    plt.plot(epochs_range, training_loss, label = "Training loss")
    plt.plot(epochs_range, testing_loss, label = "Testing loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.title(f"Loss vs Epoch: LR = {learning_rate}, Activation = {activation}, Loss = {loss_type}")
    plt.legend()
    plt.grid(True)
    plt.show()

    return net, training_loss, testing_loss

def visualize_FM(net, images):

    # set mode to eval
    net.eval()
    
    # send images to device
    images = images.to(device)

    with torch.no_grad():
        x = net.pool1(net.act(net.conv1(images)))
        x = net.pool2(net.act(net.conv2(x)))

    batch_size, channels, H, W = x.shape
    print(f"Feature Maps Shape: {x.shape}")

    for i in range(min(10, batch_size)):
        plt.figure(figsize = (12, 3))
        for j in range(channels):
            plt.subplot(2, 8, j + 1)
            plt.imshow(x[i, j].cpu(), cmap = 'gray')
            plt.axis('off')
        plt.show()

# -------------------------------
# Run Experiments
# -------------------------------

# Test 1
# net, training_loss, testing_loss = run_experiment(0.1, "tanh", "ce", 5, 70)

# Test 2
# net, training_loss, testing_loss = run_experiment(0.01, "tanh", "ce", 5, 70)

# Test 3
# net, training_loss, testing_loss = run_experiment(0.001, "tanh", "ce", 5, 100)

# Test 4
# net, training_loss, testing_loss = run_experiment(0.1, "sigmoid", "ce", 5, 100)

# Test 5
# net, training_loss, testing_loss = run_experiment(0.01, "sigmoid", "ce", 5, 100)

# Test 6
# net, training_loss, testing_loss = run_experiment(0.001, "sigmoid", "ce", 5, 100)

# Test 7
# net, training_loss, testing_loss = run_experiment(0.1, "tanh", "mse", 5, 100)

# Test 8
# net, training_loss, testing_loss = run_experiment(0.01, "tanh", "mse", 5, 100)

# Test 9
# net, training_loss, testing_loss = run_experiment(0.001, "tanh", "mse", 5, 100)

# Test 10
# net, training_loss, testing_loss = run_experiment(0.1, "sigmoid", "mse", 5, 100)

# Test 11
# net, training_loss, testing_loss = run_experiment(0.01, "sigmoid", "mse", 5, 100)

# Test 12
# net, training_loss, testing_loss = run_experiment(0.001, "sigmoid", "mse", 5, 100)

# Output feature map
# dataiterator = iter(testloader)
# images, labels = next(dataiterator)
# visualize_FM(net, images[:10])

# ReLU test
net, training_loss, testing_loss = run_experiment(0.001, "relu", "ce", 3, 100)