# Lex Albrandt
# CS440
# Homework 2
# RNN

import yfinance as yf
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, TensorDataset
import torch.optim as optim
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# --------------------------------
# Sources
# --------------------------------
# https://medium.com/thedeephub/rnns-in-action-predicting-stock-prices-with-recurrent-neural-networks-9155a33c4c3b

# --------------------------------
# Model size definitions
# --------------------------------
input_size = 1
hidden_size = 50
output_size = 1
num_layers = 1

# --------------------------------
# Hyperparameters/epochs
# --------------------------------
epochs = 50
learning_rate = 0.001
batch_size = 10

# --------------------------------
# Load data from yfinance
# --------------------------------

# # Download DJI average
# dow_jones_index = yf.download('^DJI', start = "2000-01-01", end = "2024-01-01")

# # Save to CSV
# dow_jones_index.to_csv("dow_jones.csv")


df = pd.read_csv("dow_jones.csv", header = [0, 1], index_col = 0)

# print(df["High"].head(10))
# print(df["High"].dtypes)

df_high_prices = df["High"]["^DJI"].values

# Normalize data
scaler = MinMaxScaler()
high_prices = scaler.fit_transform(df_high_prices.reshape(-1, 1))

# Split data into training and test data
train_size = int(len(high_prices) * 0.8)
train_data, test_data = high_prices[:train_size], high_prices[train_size:]

# Create sequences
# Default: 100 days
def create_dataset(dataset, look_back = 100):
    X, Y = [], []

    # Loop over dataset so each sequence has look_back elements
    for i in range(len(dataset) - look_back -1):
        X.append(dataset[i : i + look_back])
        Y.append(dataset[i + look_back])

    return np.array(X), np.array(Y)

# Number of days in a sequence
look_back = 100
X_train, Y_train = create_dataset(train_data, look_back)
X_test, Y_test = create_dataset(test_data, look_back)

# Convert numpy datasets to tensors
X_train_tensor = torch.from_numpy(X_train).float()
Y_train_tensor = torch.from_numpy(Y_train).float()

X_test_tensor = torch.from_numpy(X_test).float()
Y_test_tensor = torch.from_numpy(Y_test).float()

# Wrap tensors in dataloader for batching
train_dataset = TensorDataset(X_train_tensor, Y_train_tensor)
test_dataset = TensorDataset(X_test_tensor, Y_test_tensor)

train_loader = DataLoader(train_dataset, batch_size = batch_size, shuffle = True)
test_loader = DataLoader(test_dataset, batch_size = batch_size, shuffle = False)

# ---------------------------------
# Define LSTM RNN
# ---------------------------------

class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, num_layers):
        super().__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        
        # LSTM layer
        # input_size = num features per time step (1)
        # hidden_size = LSTM memory size
        # output_size = prediction size (1)
        # num_layers = stacked LSTM layers
        # Input shape = (batch_size, sequence length, input_size)
        #               (batch_size, 100, 1)
        self.lstm = nn.LSTM(input_size = input_size,
                            hidden_size = hidden_size,
                            num_layers = num_layers,
                            batch_first = True)
        
        # Output layer
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        """ Forward pass function

        Args:
            x (batch of sequences): input of shape (batch_size, seq_length, input_size)
        """

        # LSTM returns (output, (num final hidden states, num final cell states))
        # h_n and c_n are tensors
        lstm_output, (h_n, c_n) = self.lstm(x)

        # Output from last time step
        # From the 100 day sequence only keep what model knows is at day 100
        # Shape: (batch_size, hidden_size)
        last_output = lstm_output[:, -1, :]

        # Pass to output layer
        # Fully connected
        # Shape: (batch_size, 1)
        output = self.fc(last_output)

        return output


# Instantiate the model
model = LSTMModel(input_size, hidden_size, output_size, num_layers)

# Move to GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Define Loss function and optimizer
loss_function = nn.MSELoss()

# Using SGD and LR of 0.001
optimizer = optim.Adam(model.parameters(), lr = learning_rate)

# ------------------------------
# Training loop
# ------------------------------

training_loss = []
testing_loss = []

for epoch in range(epochs):

    # Set model to training mode
    model.train()
    running_loss = 0.0
    epoch_loss = 0.0

    for i, (X_batch, Y_batch) in enumerate(train_loader, 0):

        X_batch, Y_batch = X_batch.to(device), Y_batch.to(device)

        optimizer.zero_grad()
        outputs = model(X_batch)
        loss = loss_function(outputs, Y_batch)
        loss.backward()
        optimizer.step()

        epoch_loss += loss.item()
        running_loss += loss.item()
        
        if i % 2000 == 1999:
            print(f"[{epoch + 1}, {i + 1:5d}], loss: {running_loss / 2000:.4f}")
            running_loss = 0.0

    avg_training_loss = epoch_loss / len(train_loader)    
    training_loss.append(avg_training_loss)

    print(f"Epoch {epoch + 1}: Avg Training Loss: = {avg_training_loss:.4f}")

    # ------------------
    # Testing the model
    # ------------------

    model.eval()
    test_loss = 0.0
        
    with torch.no_grad():
        
        for X_batch, Y_batch in test_loader:
            X_batch, Y_batch = X_batch.to(device), Y_batch.to(device)
            outputs = model(X_batch)
            loss = loss_function(outputs, Y_batch)
            test_loss += loss.item()
            
    avg_test_loss = test_loss / len(test_loader)
    testing_loss.append(avg_test_loss)

    print(f"Epoch {epoch + 1}, Test Loss: {avg_test_loss:.4f}")


# ---------------------------
# Plot training vs test loss
# ---------------------------

epochs_range = range(1, epochs + 1)

plt.figure()
plt.plot(epochs_range, training_loss, label = "Training Loss")
plt.plot(epochs_range, testing_loss, label = "Testing Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title(f"Loss vs Epoch: LR = {learning_rate}, Loss = MSE")
plt.legend()
plt.grid(True)
plt.show()

