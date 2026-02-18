
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
output_neurons = 10
epochs = 50
batch_size = 64
learning_rate = 0.001
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# -------------------------------
# Load MNIST and transform
# -------------------------------

class ModifiedMNISTTransform:
    def __call__(self, img):

        # Flip across y-axis
        img = func.hflip(img)
        
        # Rotate 90 degrees
        img = func.rotate(img, 90)

        # Shift right 5 pixels
        img = func.affine(img, 0, (5, 0), 1, 0)

        return func.to_tensor(img)

modified_transforms = ModifiedMNISTTransform()
original_transform = transforms.ToTensor()

mnist_original = torchvision.datasets.MNIST(root = "data",
                                            train = True,
                                            download = True,
                                            transform = original_transform)

mnist_modified = torchvision.datasets.MNIST(root = "data",
                                            train = True,
                                            download = True,
                                            transform = modified_transforms)

# -------------------------------
# Diplay original and modified
# -------------------------------

x_orig, _ = mnist_original[0]
x_mod, _ = mnist_modified[0]

plt.figure(figsize = (6, 3))
plt.subplot(1, 2, 1)
plt.imshow(x_orig.squeeze(), cmap="grey")
plt.title("Original")

plt.subplot(1, 2, 2)
plt.imshow(x_mod.squeeze(), cmap="grey")
plt.title("Modified")
plt.show()

# -------------------------------
# Transform for ResNet
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

# Reload modified resnet
mnist_modified_resnet = torchvision.datasets.MNIST(root = "data",
                                                   train = True, 
                                                   download = True,
                                                   transform = resnet_transform)

mnist_modified_test = torchvision.datasets.MNIST(root = "data",
                                                 train = False,
                                                 download = True,
                                                 transform = resnet_transform)

# ----------------------------------------------
# Subsample Training Sets
# ----------------------------------------------

def create_subset(dataset, num_per_class):
     
    indices = []
    class_counts = {i: 0 for i in range(10)}

    for idx, (_, label) in enumerate(dataset):
        if class_counts[label] < num_per_class:
            indices.append(idx)
            class_counts[label] += 1
        if all(count == num_per_class for count in class_counts.values()):
            break

    return Subset(dataset, indices)

# Number of images per class
train_sizes = [1, 5, 10, 50, 100]
train_loaders= {}

for size in train_sizes:
    subset = create_subset(mnist_modified_resnet, size)
    loader = DataLoader(subset, batch_size = 16, shuffle = True)
    train_loaders[size] = loader
    
test_loader = DataLoader(mnist_modified_test, batch_size = batch_size, shuffle = False)

# ----------------------------------------------
# Load pre-trained ResNet50 and freeze weights
# ----------------------------------------------

res_model = models.resnet50(weights = ResNet50_Weights)

# Replace output layer with 10 neurons
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

# ------------------------------------
# Training setup
# ------------------------------------
loss_function = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(res_model.fc.parameters(), lr = learning_rate)

def train_resnet(model, train_loader, test_loader, epochs):
    best_acc = 0
    best_epoch = 0
    
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
        correct = 0
        total = 0
        
        with torch.no_grad():
            for inputs, labels in test_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                _, predicted = torch.max(outputs, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
        acc = correct / total 
        if acc > best_acc:
            best_acc = acc
            best_epoch = epoch + 1
            
        print(f"Epoch {epoch + 1}, Test Accuracy: {acc:.4f}")

    return best_acc, best_epoch

# --------------------------
# Run and record results
# --------------------------

results = {}

for size, loader in train_loaders.items():
    print(f"\nTraining with {size * 10} images")
    best_acc, best_epoch = train_resnet(res_model, loader, test_loader, epochs)
    results[size * 10] = (best_acc, best_epoch)

# -------------------------
# Plot results
# -------------------------

sizes = list(results.keys())
errors = [1 - results[s][0] for s in sizes]
epochs_needed = [results[s][1] for s in sizes]

plt.figure(figsize = (8, 5))
plt.plot(sizes, errors, marker = 'o')
for i, txt in enumerate(epochs_needed):
    plt.annotate(f"{txt} epochs", (sizes[i], errors[i]))
plt.xlabel("Training test size")
plt.ylabel("Test error")
plt.title("Test error vs training set size")
plt.grid(True)
plt.show()