# Lex Albrandt
# CS440
# Homework 2
# RNN - Weather Data

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
batch_size = 1

# --------------------------------
# Load data from csv
# --------------------------------

df = pd.read_csv("seattle-weather.csv")

# --------------------------------
# DFT testing
# --------------------------------

# Extract one year and three years of data
one_year_data = df["temp_max"].values[10:375]
three_year_data = df["temp_max"].values[:1095]


# Perform DFT
# fft_vals = np.fft.fft(one_year_data)
# fft_freqs = np.fft.fftfreq(len(one_year_data), d = 1)

fft_vals = np.fft.fft(three_year_data)
fft_freqs = np.fft.fftfreq(len(three_year_data), d = 1)

# Compute magnitude spectrum
magnitude = np.abs(fft_vals)

skip = 1

# Plot data
plt.figure(figsize = (10, 4))
plt.stem(fft_freqs[skip:len(fft_freqs) // 2], magnitude[skip:len(magnitude) // 2])
plt.xlabel("Frequency (cycles per day)")
plt.ylabel('Magnitude')
plt.title("DFT of Seattle Max Temp (1 year)")
plt.show()

fft_list = list(zip(fft_freqs, magnitude))
fft_list_sorted = sorted(fft_list, key = lambda x: x[1], reverse = True)
for f, mag in fft_list_sorted[:10]:
    period_days = 1 / f if f != 0 else np.inf
    print(f"Frequency: {f:.4f} cycles/day, Magnitude: {mag:.2f}, period: {period_days:.1f} days")

# ------------------------------
# RNN
# ------------------------------

# Reshape too
df_temp_max = df["temp_max"].values.reshape(-1, 1)

days_per_year = 365

# Split data into training and test data
train_raw = df_temp_max[:2 * days_per_year]
test_raw = df_temp_max[2 * days_per_year : 3 * days_per_year]

# Normalize Data

# Create a scalar object
scaler = MinMaxScaler()

# calculates min-max and maps values to [0, 1]
train_data = scaler.fit_transform(train_raw)

# Does not calculate min-max from test, same scale
test_data = scaler.transform(test_raw)

# Create sequences
# Default = 160 days
def create_dataset(dataset, look_back = 160):
    X, Y = [], []

    for i in range(len(dataset) - look_back - 1):
        X.append(dataset[i : i + look_back])

        # value immediately after input sequence
        Y.append(dataset[i + look_back])

    return np.array(X), np.array(Y)

look_back = 10
X_train, Y_train = create_dataset(train_data, look_back)
X_test, Y_test = create_dataset(test_data, look_back)

X_train_tensor = torch.from_numpy(X_train).float()
Y_train_tensor = torch.from_numpy(Y_train).float()

X_test_tensor = torch.from_numpy(X_test).float()
Y_test_tensor = torch.from_numpy(Y_test).float()

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

    predictions = []

    # gets last look_back days from training data
    window = train_data[-look_back:]
    
    # convert numpy array to tensor and casts it to float32, adds batch dimension at axis 0
    # Shape expected by LSTM: (batch_size, sequence_length, input_size)
    window_tensor = torch.from_numpy(window).float().unsqueeze(0).to(device)

    model.eval()
        
    with torch.no_grad():
        for i in range(days_per_year):
            
            # send to model
            next_pred = model(window_tensor)

            # add result to predictions list
            predictions.append(next_pred.item())

            # uses the true temp from test data as the next input and reshapes to single
            # timestep
            true_next = test_data[i].reshape(1, 1)

            # drops oldes value, and appends the true next
            # Stacks vertically to remain shape
            window = np.vstack((window[1:], true_next))

            # Reshapes as before
            window_tensor = torch.from_numpy(window).float().unsqueeze(0).to(device)



# Inverse scaling
# converts to np array and reshapes to (n_samples, 1)
predictions = np.array(predictions).reshape(-1, 1)

# convert scaling back into degrees celcius (because we re-scaled our data earlier)
predictions = scaler.inverse_transform(predictions)

actual = test_raw[:days_per_year]

print("Day | Actual (°C) | Predicted (°C)")
print("-" * 35)

for i in range(10):
    print(f"{i+1:3d} | {actual[i][0]:10.2f} | {predictions[i][0]:14.2f}")

# ----------------------------
# Plot predicted vs actual
# ----------------------------

plt.figure(figsize = (12, 5))
plt.plot(actual, label = "Actual Max Temp")
plt.plot(predictions, label = "Predicted Max Temp")
plt.xlabel("Day of Year 3")
plt.ylabel("Temperature (Degrees Celcius)")
plt.title("Year 3 Temperature Prediction")
plt.legend()
plt.grid(True)
plt.show()