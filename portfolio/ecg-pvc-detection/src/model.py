'''
 # @ Author: Lex Albrandt
 # @ Create Time: 2026-02-17 09:49:39
 # @ Description: This is the code for the 1D CNN model 
 '''

# Imports
import numpy as np

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



