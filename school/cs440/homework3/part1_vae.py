# Lex Albrandt
# CS440
# Assignment 3
# Part 1 - VAE

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
latent_dim = 30
batch_size = 128
num_images = 10
epochs = 300
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

test_data = torchvision.datasets.CIFAR10(
    root = "data",
    train = False,
    download = True,
    transform = transform
)

testloader = torch.utils.data.DataLoader(
    test_data,
    batch_size = batch_size,
    shuffle = False,
    num_workers = 2
)

# Class Constants
classes = ('plane', 'car', 'bird', 'cat', 'deer',
           'dog', 'frog', 'horse', 'ship', 'truck')


# -------------------------------
# Define VAE
# -------------------------------

# Enodes an image into a probability distribution in latent space
class AutoEncoder(nn.Module):
    def __init__(self):
        super().__init__()

        # Encoder
        # Encodes to a gaussian distribution
        # q_{\theta}(z \mid x) = \mathcal{N}(\mu, \sigma^{2})
        
        # 3072 -> 512
        self.fc1 = nn.Linear(input_dim, hidden_dim)

        # 512 -> mu mean vector
        self.fc_mu = nn.Linear(hidden_dim, latent_dim)

        # 512 -> log variance vector (log sigma^2)
        self.fc_logvar = nn.Linear(hidden_dim, latent_dim)

        # Decoder
        # maps latent vector to hidden to reconstructed image
        self.fc2 = nn.Linear(latent_dim, hidden_dim)
        self.fc3 = nn.Linear(hidden_dim, input_dim)

        # relu for hidden layers, sigmoid for output
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()

    # Converts image to hidden representation
    # Predict mean and log-variance of latent gaussian
    # \mu_\theta(x),\log \sigma_theta^2(x)
    def encode(self, x):
        h = self.relu(self.fc1(x))
        mu = self.fc_mu(h)
        logvar = self.fc_logvar(h)
        return mu, logvar

    # We cannot backpropogate through random sampling directly, so instead of
    # sampling z ~ N(mu, theta^2)
    # we rewrite z=\mu + \sigma \times \epsilon, \epsilon ~ \mathcal(N)(0,I)
    # Sets up randomness that is independent of the network
    def reparameterize(self, mu, logvar):
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return mu + eps * std

    # Takes latent vector and reconstructs the image
    # Sigmoid outputs pixel probabilities
    def decode(self, z):
        h = self.relu(self.fc2(z))
        return self.sigmoid(self.fc3(h))
    
    # x -> encoder -> (mu, logvar) -> sample z -> decoder -> reconstructed image
    def forward(self, x):
        mu, logvar = self.encode(x)
        z = self.reparameterize(mu, logvar)
        recon = self.decode(z)
        return recon, mu, logvar

# Loss = reconstruction loss + KL divergence
def vae_loss(recon_x, x, mu, logvar):

    # measures how close the output image is to the input image
    recon_loss = nn.functional.binary_cross_entropy(recon_x, x, reduction = "sum")

    # KL Divergence term, forces latent space to match p(z)=\mathcal(N)(0, 1)
    # enables interpolation
    kl = -0.5 * torch.sum(1 + logvar - mu ** 2 - logvar.exp())

    beta = min(1.0, epoch / 20)
    return recon_loss + beta * kl

# ---------------------------------
# Training loop for VAE
# ---------------------------------

model = AutoEncoder().to(device)
optimizer = optim.Adam(model.parameters(), lr = learning_rate)

for epoch in range(epochs):
    model.train()
    total_loss = 0.0
    
    for inputs, _ in trainloader:
        inputs = inputs.view(inputs.size(0), -1).float().to(device)
        optimizer.zero_grad()

        recon, mu, logvar = model(inputs)
        loss = vae_loss(recon, inputs, mu, logvar)

        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
        avg_loss = total_loss / len(trainloader)

    print(f"Epoch {epoch + 1}, Loss: {avg_loss:.4f}")

# ----------------------------------------
# Generate 10 images for each CIFAR class
# ----------------------------------------

latent_by_class = {i: [] for i in range(10)}

model.eval()
with torch.no_grad():
    for inputs, labels in trainloader:
        inputs = inputs.view(inputs.size(0), -1).to(device)
        mu, logvar = model.encode(inputs)
        z = model.reparameterize(mu, logvar)

        for zi, label in zip(z, labels):
            latent_by_class[label.item()].append(zi.cpu())

def generate_class_images(model, latent_by_class):
    model.eval()
    class_images = {}

    with torch.no_grad():
        for c in range(10):
            z = torch.stack(latent_by_class[c][:10]).to(device)
            samples = model.decode(z)
            samples = samples.view(-1, 3, 32, 32).cpu()
            class_images[c] = samples

    return class_images

def interpolate(model, z1, z2, steps = 10):
    model.eval()
    images = []
    
    with torch.no_grad():
        for alpha in torch.linspace(0, 1, steps):
            z = (1 - alpha) * z1 + alpha * z2
            img = model.decode(z.unsqueeze(0))
            img = img.view(-1, 3, 32, 32).cpu()
            images.append(img)

    return images


# ----------------------------------
# Generate class images
# ----------------------------------

class_images = generate_class_images(model, latent_by_class)

# ----------------------------------
# Generate interpolated images
# ----------------------------------

# cat, horse
classA, classB = 3 ,7

zA = latent_by_class[classA][0].to(device)
zB = latent_by_class[classB][0].to(device)

interp_imgs = interpolate(model, zA, zB)

# ----------------------------------
# Display images
# ----------------------------------

def show_class_images(imgs, class_name, nrow = 5):
    imgs = imgs.detach().cpu()
    N = len(imgs)
    ncol = nrow
    nrow = (N + ncol - 1) // ncol

    fig, axes = plt.subplots(nrow, ncol, figsize = (ncol * 2, nrow * 2))
    axes = np.array(axes).reshape(-1)
    
    for i in range(N):
        img = np.transpose(imgs[i].numpy(), (1, 2, 0))
        axes[i].imshow(img)
        axes[i].axis("off")

    for i in range(N, len(axes)):
        axes[i].axis("off")

    plt.suptitle(f"Generated images for class: {class_name}")
    plt.tight_layout()
    plt.show()

def show_interpolation(imgs, classA, classB):
    imgs = torch.cat(imgs, dim = 0).cpu()
    N = len(imgs)

    fig, axes = plt.subplots(1, N, figsize = (2 * N, 2))

    for i in range(N):
        img = np.transpose(imgs[i].numpy(), (1, 2, 0))
        axes[i].imshow(img)
        axes[i].axis("off")
        axes[i].set_title(f"{i / (N - 1):.2f}")
    
    plt.suptitle(f"Interpolation: {classes[classA]} -> {classes[classB]}")
    plt.show()

for c in range(10):
    show_class_images(class_images[c], classes[c], nrow = 5)

show_interpolation(interp_imgs, classA, classB)
