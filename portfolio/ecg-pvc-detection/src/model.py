'''
 # @ Author: Lex Albrandt
 # @ Create Time: 2026-02-17 09:49:39
 # @ Description: This is the code for the 1D CNN model 
 '''

# Imports
import numpy as np
import torch
import torchvision.transforms as transforms
from torch.utils.data import DataLoader, TensorDataset
import torch.nn as nn
import torch.nn.functional as F

# --------------------------------------------------
# Constansts and hyperparameters
# --------------------------------------------------

batch_size = 64

# --------------------------------------------------
# Load numpy arrays from data processing pipeline
# --------------------------------------------------

def load_train_test_data():
    X_train = np.load('../data/processed/X_train.npy')
    X_test = np.load('../data/processed/X_test.npy')
    y_train = np.load('../data/processed/y_train.npy')
    y_test = np.load('../data/processed/y_test.npy')
 
    return X_train, X_test, y_train, y_test

# -------------------------------------------------
# Normalize training/test data
# -------------------------------------------------

def z_score_normalize(train_array, test_array):
    train_mean = train_array.mean()
    train_std = train_array.std()

    X_train_norm = (train_array - train_mean) / train_std
    X_test_norm = (test_array - train_mean) / train_std

    X_train_norm = X_train_norm.astype(np.float32)
    X_test_norm = X_test_norm.astype(np.float32)

    assert train_std > 0, "Cannot divide by zero"

    # save normalization stats
    np.save("../data/stats/mean.npy", train_mean)
    np.save("../data/stats/std.npy", train_std)

    return X_train_norm, X_test_norm

# ----------------------------------------------
# Create Datasets + Dataloaders
# ----------------------------------------------

def create_dataloaders(X_train, y_train, X_test, y_test):

    # Convert to tensors
    X_train = torch.tensor(X_train, dtype = torch.float32)
    y_train = torch.tensor(y_train, dtype = torch.float32)
    X_test = torch.tensor(X_test, dtype = torch.float32)
    y_test = torch.tensor(y_test, dtype = torch.float32)

    # Add channel dimension for 1D CNN
    # From (N, 200) -> (N, 1, 200)
    X_train = X_train.unsqueeze(1)
    X_test = X_test.unsqueeze(1)

    # Reshape labels for BCE
    # From (N, ) -> (N, 1)
    y_train = y_train.unsqueeze(1)
    y_test = y_test.unsqueeze(1)

    train_dataset = TensorDataset(X_train, y_train)
    test_dataset = TensorDataset(X_test, y_test)


    train_loader = torch.utils.data.DataLoader(
        train_dataset,
        batch_size = batch_size,
        shuffle = True,
    )

    test_loader = torch.utils.data.DataLoader(
        test_dataset,
        batch_size = batch_size,
        shuffle = False,
    )

    return train_loader, test_loader

# ------------------------------------------
# Define 1D CNN
# ------------------------------------------

class Model(nn.Module):

    def __init__(self, kernel_sizes = [15, 7, 3]):
        super().__init__()
        
        self.kernel_size = kernel_sizes

        self.conv1 = nn.Conv1d(in_channels = 1,
                               out_channels = 16, 
                               kernel_size = kernel_sizes[0],
                               padding = kernel_sizes[0] // 2)

        self.pool1 = nn.MaxPool1d(kernel_size = 2)

        self.conv2 = nn.Conv1d(in_channels = 16,
                               out_channels = 32, 
                               kernel_size = kernel_sizes[1],
                               padding = kernel_sizes[1] // 2)
                            
        self.pool2 = nn.MaxPool1d(kernel_size = 2)

        self.conv3 = nn.Conv1d(in_channels = 32,
                               out_channels = 64, 
                               kernel_size = kernel_sizes[2],
                               padding = kernel_sizes[2] // 2)
                            
        
        self.pool3 = nn.MaxPool1d(kernel_size = 2)

        dummy = torch.zeros(1, 1, 200)  # 1 sample, 1 channel, length 200
        dummy = self.pool1(F.relu(self.conv1(dummy)))
        dummy = self.pool2(F.relu(self.conv2(dummy)))
        dummy = self.pool3(F.relu(self.conv3(dummy)))
        fc_input = dummy.numel() // dummy.shape[0]

        self.fc = nn.Linear(fc_input, 1)

    def forward(self, x):
        
        x = self.pool1(F.relu((self.conv1(x))))
        x = self.pool2(F.relu((self.conv2(x))))
        x = self.pool3(F.relu((self.conv3(x))))

        x = torch.flatten(x, 1)

        x = self.fc(x)

        return x

