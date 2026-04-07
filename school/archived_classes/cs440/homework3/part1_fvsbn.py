# Lex Albrandt
# CS440
# Assignment 3
# Part 1 - FVSBN

# sources
# https://www.haraldvohringer.com/posts/fsbvn

# Imports
import torch
from torch.utils.data import DataLoader
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
import torch.optim as optim
import matplotlib.pyplot as plt
import numpy as np

# ----------------------------
# Hyperparameters
# ----------------------------
input_dim = 32 * 32 * 3
hidden_dim = 512
batch_size = 128
epochs = 250
learning_rate = 0.001
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ----------------------------
# Load and transform CIFAR-10
# ----------------------------

# We must binarize the data from CIFAR-10 because our FVSBN expects binary data
# The lambda function goes element by element in the tensor and produces true where
# the pixel value is > 0.5, and false where the value is < 0.5, which is then converted
# to a float, so true -> 1.0, and false -> 0.0, which binarizes the image at a threshold
# of 0.5
transform = transforms.Compose([transforms.ToTensor(),
                                transforms.Lambda(lambda x: (x > 0.5).float())])

training_data = torchvision.datasets.CIFAR10(
    root = "data",
    train = True,
    download = True,
    transform = transform
)

trainloader = torch.utils.data.DataLoader(
    training_data,
    batch_size = batch_size,
    shuffle = True,
    num_workers = 2
)

# Class Constants
classes = ('plane', 'car', 'bird', 'cat', 'deer',
           'dog', 'frog', 'horse', 'ship', 'truck')

# ---------------------------------------
# Define Masked Linear Layer
# ---------------------------------------

# This is a linear layer where some connections are forced to be zero so the
# network obes autoregressive probability rules
# Pixel i is allowed to depend only on pixels 1 ... i - 1, never on future pixels
# We enforce this using a mask on the weights
class MaskedLinear(nn.Linear):
    def __init__(self, in_features, out_features, mask):
        # weight shape = (out_features, in_features)
        super().__init__(in_features, out_features)

        # Buffer: tensor that moves to GPU, but is not a parameter, and is therefore
        # not trainable, remains fixed during training
        self.register_buffer("mask", mask)

    def forward(self, x):

        # Multiplies W (trainable weights) and M (binary mask) elementwise
        # if mask = 0, weight is forced to 0, if mask = 1, weight is trainable
        return nn.functional.linear(x, self.weight * self.mask, self.bias)

# decides which neurons are allowed to connect to which inputs (obeys rules of autoregression)
def create_masks(input_dim, hidden_dim):

    # Input order 1..D
    # Makes a generation order [0, 1, 2, ... , 3071]
    input_order = torch.arange(input_dim)

    # hidden ordering randomly sampled from output order
    # Each hidden neuron is assigned a random int between 0 and dim - 1
    hidden_order = torch.randint(0, input_dim, (hidden_dim,))

    # Mask input -> hidden
    # shape: (hidden_dim, input_dim)
    # Hidden neuron j can see input only if i < hidden_order[j]
    mask1 = (hidden_order[:, None] > input_order[None, :]).float()

    # Mask Hidden -> output
    # shape: (hidden_dim, input_dim)
    # Output pixel i can only see hidden neuron j if hidden_order[j] <= i
    mask2 = (input_order[:, None] >= hidden_order[None, :]).float()

    return mask1, mask2



# ---------------------------------------
# Define FVSBN
# ---------------------------------------

class FVSBN(nn.Module):

    # 32 x 32 x 3 = 3072 dim
    def __init__(self, input_dim = 3072, hidden_dim = 512):
        super().__init__()

        mask1, mask2 = create_masks(input_dim, hidden_dim)

        self.fc1 = MaskedLinear(input_dim, hidden_dim, mask1)
        self.fc2 = MaskedLinear(hidden_dim, input_dim, mask2)
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        h = self.relu(self.fc1(x))
        out = self.sigmoid(self.fc2(h))
        return out

model = FVSBN(input_dim, hidden_dim).to(device)
optimizer = optim.Adam(model.parameters(), lr = learning_rate)
loss_function = nn.BCELoss()

# ----------------------------------------
# Train the FVSBN
# ----------------------------------------

for epoch in range(epochs):
    model.train()

    total_loss = 0
    
    for inputs, _ in trainloader:
        inputs = inputs.view(inputs.size(0), -1).to(device)

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = loss_function(outputs, inputs)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    avg_loss = total_loss / len(trainloader)
    print(f"Epoch {epoch + 1}/{epochs}, Loss: {avg_loss:.4f}")


# ------------------------------
# Generate samples
# ------------------------------

# Generates images pixel-by-pixel using the autoregressive model
def sample_fvsbn(model, n_samples = 20):
    model.eval()

    # Initialize empty images
    samples = torch.zeros(n_samples, input_dim).to(device)

    # with disabled gradients
    with torch.no_grad():

        # Iterate over every pixel
        for i in range(input_dim):

            # compute probabilities for all pixels
            probs = model(samples)

            # probs[:, 1] = probability between 0 and 1
            # bernoulli returns a 1 with probability p and 0 for everything else
            samples[:, i] = torch.bernoulli(probs[:, i])

    return samples

samples = sample_fvsbn(model)
samples = samples.view(-1, 3, 32, 32).cpu()


# ------------------------------
# Plot samples
# ------------------------------
def show_images(imgs, nrow = 5):
    fig, axes = plt.subplots(len(imgs) // nrow, 
                             nrow, 
                             figsize = (nrow * 2, (len(imgs) // nrow *2)))
    for i, ax in enumerate(axes.flatten()):
        ax.imshow(np.transpose(imgs[i].numpy(), (1, 2, 0)))
        ax.axis("off")
    plt.show()

show_images(samples, nrow = 5)

