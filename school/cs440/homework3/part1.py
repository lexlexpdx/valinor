# Lex Albrandt
# CS440
# Assignment 3
# Part 1

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
epochs = 50
learning_rate = 0.001
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ----------------------------
# Load and transform CIFAR-10
# ----------------------------

transform = transforms.Compose([transforms.ToTensor()])

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


# ---------------------------------------
# Define FVSBN
# ---------------------------------------

class FVSBN(nn.Module):

    # 32 x 32 x 3 = 3072 dim
    def __init__(self, input_dim = 3072, hidden_dim = 512):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, input_dim),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.net(x)

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
model.eval()

with torch.no_grad():

    # create a batch of 20 random input vectors, uniformly generated between 0 and 1
    z = torch.rand(20, input_dim).to(device)

    # Feeds vectors through network and is the predicted probability of
    # each pixel being 1
    probs = model(z)

    # Converts probabilities into actual pixel values
    samples = torch.bernoulli(probs)

    # reshape vectors to (20 imgs, 3 channels, 32 width, 32 height)
    # moves back to cpu for visualization
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