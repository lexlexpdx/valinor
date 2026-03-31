
# Lex Albrandt
# CS440
# Assignment 3
# Part 2

# sources

# Imports
import torch
from torch.utils.data import DataLoader, Subset
import torchvision.models as models
from torchvision.models import ResNet50_Weights
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
import torchvision.transforms.functional as func
import torch.optim as optim
import matplotlib.pyplot as plt
import numpy as np

# ----------------------------
# Hyperparameters
# ----------------------------
output_neurons = 2
epochs = 30
train_batch_size = 4
test_batch_size = 128
learning_rate = 1e-4
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# Random seeds
np.random.seed(0)
torch.manual_seed(0)

# -------------------------------
# Load MNIST and FashionMNIST and Transform for ResNet
# -------------------------------

resnet_transform = transforms.Compose([

    # Resize to 224 pixels
    transforms.Resize(224),

    # Convert graycale to RGB
    transforms.Grayscale(num_output_channels = 3),
    transforms.ToTensor(),

    # Normalize to ImageNet standards
    transforms.Normalize(mean = [0.485, 0.456, 0.406], std = [0.229, 0.224, 0.225])
])

mnist_train = torchvision.datasets.MNIST(root = "data",
                                        train = True, 
                                        download = True,
                                        transform = resnet_transform)

mnist_test = torchvision.datasets.MNIST(root = "data",
                                        train = False,
                                        download = True,
                                        transform = resnet_transform)

fashion_train = torchvision.datasets.FashionMNIST(root = "data",
                                                  train = True,
                                                  download = True,
                                                  transform = resnet_transform)

fashion_test = torchvision.datasets.FashionMNIST(root = "data",
                                                 train = False,
                                                 download = True,
                                                 transform = resnet_transform)
                                            

# ----------------------------------------------
# Load pre-trained ResNet50 and freeze weights
# ----------------------------------------------

res_model = models.resnet50(weights = ResNet50_Weights)

# Replace output layer with 2 neurons
num_ftrs = res_model.fc.in_features
res_model.fc = nn.Linear(num_ftrs, output_neurons)

# Freeze all layers
for param in res_model.parameters():
    param.requires_grad = False

# Unfreeze last layer
# FC here is the last layer
for param in res_model.fc.parameters():
    param.requires_grad = True

res_model.to(device)

# --------------------------------------------
# Create subsets for MNIST and FashionMNIST
# --------------------------------------------

mnist_train_indices = np.random.choice(len(mnist_train), 10, replace = False)
fashion_train_indices = np.random.choice(len(fashion_train), 10, replace = False)
mnist_test_indices = np.random.choice(len(mnist_test), 10, replace = False)
fashion_test_indices = np.random.choice(len(fashion_test), 10, replace = False)

mnist_train_small = Subset(mnist_train, mnist_train_indices)
fashion_train_small = Subset(fashion_train, fashion_train_indices)
mnist_test_small = Subset(mnist_test, mnist_test_indices)
fashion_test_small = Subset(fashion_test, fashion_test_indices)


# -------------------------------------
# Binarize labels
# -------------------------------------

class BinaryDataset(torch.utils.data.Dataset):
    def __init__(self, dataset, label):
        self.dataset = dataset
        self.label = label

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        x, _ = self.dataset[idx]
        return x, self.label

mnist_train_bin = BinaryDataset(mnist_train_small, 0)
fashion_train_bin = BinaryDataset(fashion_train_small, 1)
combined_train = torch.utils.data.ConcatDataset([mnist_train_bin, fashion_train_bin])
combined_trainloader = DataLoader(combined_train, batch_size = train_batch_size, shuffle = True, num_workers = 2)

mnist_test_bin = BinaryDataset(mnist_test, 0)
fashion_test_bin = BinaryDataset(fashion_test, 1)

combined_test = torch.utils.data.ConcatDataset([mnist_test_bin, fashion_test_bin])
combined_testloader = DataLoader(combined_test, batch_size = test_batch_size, shuffle = False, num_workers = 2)

# ------------------------------------
# Training setup
# ------------------------------------
loss_function = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(res_model.fc.parameters(), lr = learning_rate)

def train_resnet(model, train_loader, test_loader, epochs):

    accuracy_list = []
    
    for epoch in range(epochs):
        model.train()
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = loss_function(outputs, labels)
            loss.backward()
            optimizer.step()

        model.eval()
        correct, total = 0, 0
        with torch.no_grad():
            for inputs, labels in test_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                preds = torch.argmax(outputs, dim = 1)
                correct += (preds == labels).sum().item()
                total += labels.size(0)

        accuracy = correct / total
        accuracy_list.append(accuracy)
        print(f"Epoch {epoch + 1}, Test Accuracy: {accuracy:.4f}")

    return accuracy_list

accuracy_list = train_resnet(res_model, combined_trainloader, combined_testloader, epochs)

# ----------------------------------
# Plot results
# ----------------------------------

plt.figure(figsize = (8, 5))
plt.plot(range(1, epochs + 1), accuracy_list)
plt.xlabel("Epochs")
plt.ylabel(("Accuracy"))
plt.title("Accuracy vs Epochs")
plt.grid(True)
plt.show()

