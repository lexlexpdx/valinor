# %%
'''
 # @ Author: Lex Albrandt
 # @ Class: CS440
 # @ Assignment: Assignment 4
 # @ Description: This is the code for assignment 4
 '''

# %% [markdown]
# # Question 1

# %%
import numpy as np
import torch
import torchvision
import torchvision.transforms as transforms
from torchvision import datasets
from sklearn.cluster import KMeans
import torch.nn as nn
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader, Subset

# %%
#-------------------------------------
# 1. Load CIFAR-10
# ------------------------------------

transform = transforms.Compose([transforms.ToTensor()])

dataset = torchvision.datasets.CIFAR10(
    root = './data',
    train = True,
    download = True,
    transform = transform
)

# shape (50000, 32, 32, 3)
images = dataset.data
labels = np.array(dataset.targets)

# %%
# --------------------------------------
# 2. Select 100 images per class
# --------------------------------------
samples_per_class = 100
class_counts = [0] * 10

selected_images = []
selected_labels = []

for img, label in zip(images, labels):
    if class_counts[label] < samples_per_class:
        selected_images.append(img)
        selected_labels.append(label)
        class_counts[label] += 1
        
    if len(selected_images) == 1000:
        break

X = np.array(selected_images)
y = np.array(selected_labels)

# %%
# -----------------------------------
# 3. Flatten images for KMeans
# -----------------------------------

X_flat = X.reshape(1000, -1)

# %%
# -----------------------------------
# 4. Run KMeans (k = 10)
# -----------------------------------

kmeans = KMeans(n_clusters = 10, random_state = 0, n_init = 10)
clusters = kmeans.fit_predict(X_flat)

# %%
# -----------------------------------
# 5. Build 10 x 10 table
# rows = true class
# columns = cluster
# -----------------------------------
table = np.zeros((10, 10), dtype = int)

for true_label, cluster in zip(y, clusters):
    table[true_label][cluster] += 1
    
print("10x10 Clustering table:")
print(table)

# %%
# -----------------------------------
# 6. Compute clusering accuracy
# -----------------------------------
correct = 0
for j in range(10):
    correct += np.max(table[:, j])

accuracy = correct / 1000

print(f"\nClustering Accuracy: {accuracy}")

# %% [markdown]
# The accuracy for the kclustering is much lower than the accuracy for the first  
# assignement because kclustering is an unsupervised learning method, which means  
# the alogrithm does not use true class labels during training. In contrast, the  
# first assignment used a fully connected neural network which is a supervised  
# approach, so the model is trained directly using labeled examples. In that  
# assignment the accuracy was around 85-90%.  
#   

# %% [markdown]
# # Question 2

# %%
X = np.array(selected_images)
y = np.array(selected_labels)

X = torch.tensor(X).float() / 255
X = X.permute(0, 3, 1, 2)

# %%
# ---------------------------------
# Build autoencoder
# ---------------------------------

class Autoencoder(nn.Module):
    
    def __init__(self):
        super().__init__()
        
        self.encoder = nn.Sequential(
            nn.Flatten(),
            nn.Linear(3072, 512),
            nn.ReLU(),
            nn.Linear(512, 128),
            nn.ReLU()
        )

        self.decoder = nn.Sequential(
            nn.Linear(128, 512),
            nn.ReLU(),
            nn.Linear(512, 3072),
            nn.Sigmoid()
        )

    def forward(self, x):
        z = self.encoder(x)
        x_hat = self.decoder(z)
        return x_hat

# %%
# ------------------------------
# Train the autoencoder
# ------------------------------

model = Autoencoder()

criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr = 0.001)

X_flat = X.reshape(1000, -1)

for epoch in range(30):
    
    optimizer.zero_grad()

    output = model(X_flat)

    loss = criterion(output, X_flat)

    loss.backward()
    optimizer.step()
    
    print(f"Epoch {epoch + 1}, Loss: {loss.item()}")

# %%
# -----------------------------
# Extract feature vectors
# -----------------------------
with torch.no_grad():
    features = model.encoder(X_flat)

features = features.numpy()

# %%
# ------------------------------
# Run K-means on feature vectors
# ------------------------------

kmeans = KMeans(n_clusters = 10, random_state = 0)
clusters = kmeans.fit_predict(features)

# ------------------------------
# Create table
# ------------------------------
table = np.zeros((10, 10), dtype = int)

for true_label, cluster in zip(y, clusters):
    table[true_label][cluster] += 1

print(table)

# %%
# -------------------------------
# Compute clustering accuracy
# -------------------------------
correct = 0
for j in range(10):
    correct += np.max(table[:, j])

accuracy = correct / 1000

print(f"Clustering accuracy: {accuracy}")

# %%
# -----------------------------------------------
# Apply PCA to feature vectors and run K-means
# -----------------------------------------------

pca = PCA(n_components = 20)
features_pca = pca.fit_transform(features)

kmeans = KMeans(n_clusters = 10, random_state = 0)

clusters_pca = kmeans.fit_predict(features_pca)

table_pca = np.zeros((10, 10), dtype = int)

for true_label, cluster in zip(y, clusters_pca):
    table_pca[true_label][cluster] += 1

print("PCA clustering table")
print(table_pca)

# %%
# -----------------------------------
# Table accuracy
# -----------------------------------

correct = 0
for j in range(10):
    correct += np.max(table_pca[:, j])

accuracy = correct / 1000

print(f"Accuracy: {accuracy}")

# %% [markdown]
# Clustering on autoencoder features followed by PCA-reduced features did not  
# improve accuracy compared to clustering raw pixels. This is likely because the  
# fully connected Autoencoder used does not discriminate enough features during  
# learning for CIFAR10.  

# %% [markdown]
# # Question 3

# %%
num_train = 5000
idx = np.random.choice(len(images), num_train, replace = False)
X_train = images[idx] / 255.0
X_train = torch.tensor(X_train).float()

# ------------------------------
# Add salt and pepper noise
# --------------------------------

def add_salt_pepper_noise(images, noise_ratio = 0.1):
    noisy_images = images.clone()
    n_samples, h, w, c = noisy_images.shape
    num_pixels = int(h * w * noise_ratio)

    for i in range(n_samples):
        for _ in range(num_pixels):
            x = np.random.randint(0, h)
            y = np.random.randint(0, w)
            ch = np.random.randint(0, c)
            noisy_images[i, x, y, ch] = 0 if np.random.rand() < 0.5 else 1
    return noisy_images

noise_ratio = 0.1
X_train_noisy = add_salt_pepper_noise(X_train, noise_ratio)

# %%
# ------------------------------
# Build denoising autoencoder
# ------------------------------

class DenoisingAutoencoder(nn.Module):
    
    def __init__(self):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Flatten(),
            nn.Linear(32 * 32 * 3, 512),
            nn.ReLU(),
            nn.Linear(512, 128),
            nn.ReLU()
        )
        self.decoder = nn.Sequential(
            nn.Linear(128, 512),
            nn.ReLU(),
            nn.Linear(512, 32 * 32 * 3),
            nn.Sigmoid()
        )

    def forward(self, x):
        z = self.encoder(x)
        x_hat = self.decoder(z)
        return x_hat

# -----------------------------------
# Train the DAE
# -----------------------------------
model = DenoisingAutoencoder()
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr = 0.001)

# flatten images
X_train_flat = X_train_noisy.reshape(num_train, -1)
X_target_flat = X_train.reshape(num_train, -1)

epochs = 30
for epoch in range(epochs):
    optimizer.zero_grad()
    output = model(X_train_flat)
    loss = criterion(output, X_target_flat)
    loss.backward()
    optimizer.step()
    print(f"Epoch {epoch + 1}, Loss: {loss.item()}")

# %%
# ---------------------------
# Test on 10 images
# ---------------------------

num_test = 10
test_idx = np.random.choice(len(dataset.data), num_test, replace = False)
X_test = torch.tensor(dataset.data[test_idx] / 255.0).float()


# Select 10 test images
test_indices = np.random.choice(len(X_test), 10, replace=False)
X_samples = X_test[test_indices]

# ----------------------------
# Noise Level 1: 5%
# ----------------------------
noise_ratio = 0.05
X_noisy = add_salt_pepper_noise(X_samples, noise_ratio)
X_noisy_flat = X_noisy.reshape(10, -1)
with torch.no_grad():
    X_denoised_flat = model(X_noisy_flat)
X_denoised = X_denoised_flat.reshape(10,32,32,3)

# Plot all 10 images (Original, Noisy, Denoised)
fig, axs = plt.subplots(10, 3, figsize=(10, 30))
for i in range(10):
    axs[i,0].imshow(X_samples[i].numpy())
    axs[i,0].set_title("Original")
    axs[i,0].axis('off')
    
    axs[i,1].imshow(X_noisy[i].numpy())
    axs[i,1].set_title("Noisy 5%")
    axs[i,1].axis('off')
    
    axs[i,2].imshow(X_denoised[i].numpy())
    axs[i,2].set_title("Denoised")
    axs[i,2].axis('off')
plt.tight_layout()
plt.show()

# %%
# ----------------------------
# Noise Level 2: 10%
# ----------------------------
noise_ratio = 0.10
X_noisy = add_salt_pepper_noise(X_samples, noise_ratio)
X_noisy_flat = X_noisy.reshape(10, -1)
with torch.no_grad():
    X_denoised_flat = model(X_noisy_flat)
X_denoised = X_denoised_flat.reshape(10,32,32,3)

fig, axs = plt.subplots(10, 3, figsize=(10, 30))
for i in range(10):
    axs[i,0].imshow(X_samples[i].numpy())
    axs[i,0].set_title("Original")
    axs[i,0].axis('off')
    
    axs[i,1].imshow(X_noisy[i].numpy())
    axs[i,1].set_title("Noisy 10%")
    axs[i,1].axis('off')
    
    axs[i,2].imshow(X_denoised[i].numpy())
    axs[i,2].set_title("Denoised")
    axs[i,2].axis('off')
plt.tight_layout()
plt.show()

# %%
# ----------------------------
# Noise Level 3: 20%
# ----------------------------
noise_ratio = 0.20
X_noisy = add_salt_pepper_noise(X_samples, noise_ratio)
X_noisy_flat = X_noisy.reshape(10, -1)
with torch.no_grad():
    X_denoised_flat = model(X_noisy_flat)
X_denoised = X_denoised_flat.reshape(10,32,32,3)

fig, axs = plt.subplots(10, 3, figsize=(10, 30))
for i in range(10):
    axs[i,0].imshow(X_samples[i].numpy())
    axs[i,0].set_title("Original")
    axs[i,0].axis('off')
    
    axs[i,1].imshow(X_noisy[i].numpy())
    axs[i,1].set_title("Noisy 20%")
    axs[i,1].axis('off')
    
    axs[i,2].imshow(X_denoised[i].numpy())
    axs[i,2].set_title("Denoised")
    axs[i,2].axis('off')
plt.tight_layout()
plt.show()

# %%
# ----------------------------
# Noise Level 4: 30%
# ----------------------------
noise_ratio = 0.30
X_noisy = add_salt_pepper_noise(X_samples, noise_ratio)
X_noisy_flat = X_noisy.reshape(10, -1)
with torch.no_grad():
    X_denoised_flat = model(X_noisy_flat)
X_denoised = X_denoised_flat.reshape(10,32,32,3)

fig, axs = plt.subplots(10, 3, figsize=(10, 30))
for i in range(10):
    axs[i,0].imshow(X_samples[i].numpy())
    axs[i,0].set_title("Original")
    axs[i,0].axis('off')
    
    axs[i,1].imshow(X_noisy[i].numpy())
    axs[i,1].set_title("Noisy 30%")
    axs[i,1].axis('off')
    
    axs[i,2].imshow(X_denoised[i].numpy())
    axs[i,2].set_title("Denoised")
    axs[i,2].axis('off')
plt.tight_layout()
plt.show()

# %%
# ----------------------------
# Noise Level 5: 50%
# ----------------------------
noise_ratio = 0.50
X_noisy = add_salt_pepper_noise(X_samples, noise_ratio)
X_noisy_flat = X_noisy.reshape(10, -1)
with torch.no_grad():
    X_denoised_flat = model(X_noisy_flat)
X_denoised = X_denoised_flat.reshape(10,32,32,3)

fig, axs = plt.subplots(10, 3, figsize=(10, 30))
for i in range(10):
    axs[i,0].imshow(X_samples[i].numpy())
    axs[i,0].set_title("Original")
    axs[i,0].axis('off')
    
    axs[i,1].imshow(X_noisy[i].numpy())
    axs[i,1].set_title("Noisy 50%")
    axs[i,1].axis('off')
    
    axs[i,2].imshow(X_denoised[i].numpy())
    axs[i,2].set_title("Denoised")
    axs[i,2].axis('off')
plt.tight_layout()
plt.show()

# %% [markdown]
# Question 4
#
# I don't have a saved version of a model, so I wrote a new one

# %%
# -----------------------------
# 1. Prepare MNIST data
# -----------------------------
transform = transforms.ToTensor()

train_dataset = datasets.MNIST(root="./data", train=True, download=True, transform=transform)
test_dataset = datasets.MNIST(root="./data", train=False, download=True, transform=transform)

batch_size = 64
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

# -----------------------------
# 2. Define a small FCNN
# -----------------------------
class MNIST_FC(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.fc = nn.Sequential(
            nn.Linear(28*28, 256),  # input layer -> hidden
            nn.ReLU(),
            nn.Linear(256, 128),    # hidden -> hidden
            nn.ReLU(),
            nn.Linear(128, 10)      # hidden -> output
        )
    def forward(self, x):
        x = self.flatten(x)
        return self.fc(x)

# -----------------------------
# 3. Setup model, loss, optimizer
# -----------------------------
device = "cuda" if torch.cuda.is_available() else "cpu"
model = MNIST_FC().to(device)

loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# -----------------------------
# 4. Training loop
# -----------------------------
epochs = 5  # quick training for demonstration

for epoch in range(epochs):
    model.train()
    for X, y in train_loader:
        X, y = X.to(device), y.to(device)
        optimizer.zero_grad()
        output = model(X)
        loss = loss_fn(output, y)
        loss.backward()
        optimizer.step()
    print(f"Epoch {epoch+1}/{epochs}, Loss: {loss.item():.4f}")

# -----------------------------
# 5. Test accuracy
# -----------------------------
model.eval()
correct, total = 0, 0
with torch.no_grad():
    for X, y in test_loader:
        X, y = X.to(device), y.to(device)
        preds = model(X).argmax(dim=1)
        correct += (preds == y).sum().item()
        total += y.size(0)

print(f"Test Accuracy: {100*correct/total:.2f}%")

# %%
# ---------------------------------------
# Create skewed MNIST dataset
# ---------------------------------------
from torch.utils.data import DataLoader, Subset
from torchvision import datasets, transforms
import numpy as np

# Load MNIST test set
transform = transforms.ToTensor()
test_dataset = datasets.MNIST(root='./data', train=False, download=True, transform=transform)

# Target counts for the skewed dataset
target_counts = {0:1000, 1:1000, 2:1000, 3:640, 4:320, 5:160, 6:80, 7:40, 8:20, 9:10}

# Convert test labels to numpy array
targets_np = test_dataset.targets.numpy()

# Get all indices by label
indices_by_class = {i: np.where(targets_np == i)[0] for i in range(10)}

# Select indices for the skewed dataset
selected_indices = []
for digit, count in target_counts.items():
    idx = np.random.choice(indices_by_class[digit], count, replace=True)  # allow replacement if needed
    selected_indices.extend(idx)

# Create Subset and DataLoader
skewed_test_dataset = Subset(test_dataset, selected_indices)
batch_size = 64
skewed_test_loader = DataLoader(skewed_test_dataset, batch_size=batch_size, shuffle=False)

# %%
# --------------------------------
# Test on skewed data
# --------------------------------

model.eval()
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

correct, total = 0, 0
with torch.no_grad():
    for X, y in skewed_test_loader:
        X, y = X.to(device), y.to(device)
        preds = model(X).argmax(dim=1)
        correct += (preds == y).sum().item()
        total += y.size(0)

accuracy_skewed = correct / total
print(f"Accuracy on skewed test set: {accuracy_skewed*100:.2f}%")

# %% [markdown]
# As shown, the accuracy is different and slightly increased. This is because the
# model is seeing a different class distribution, and accuracy is dataset-dependent.  
