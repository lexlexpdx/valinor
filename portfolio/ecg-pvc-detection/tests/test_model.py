'''
 # @ Author: Lex Albrandt
 # @ Create Time: 2026-02-28 15:48:53
 # @ Description: Pytest modules for 1D CNN model
 '''

# Config
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore", category = DeprecationWarning)
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

import model
import numpy as np
import torch

def test_numpy_load():

    X_train, X_test, y_train, y_test = model.load_train_test_data()
    
    assert isinstance(X_train, np.ndarray)
    assert isinstance(X_test, np.ndarray)
    assert isinstance(y_train, np.ndarray)
    assert isinstance(y_test, np.ndarray)

def test_numpy_shapes():

    X_train, X_test, y_train, y_test = model.load_train_test_data()

    assert X_train.ndim == 2
    assert X_test.ndim == 2
    assert X_train.shape[1] == 200
    assert X_test.shape[1] == 200
    
    assert y_train.ndim == 1
    assert y_test.ndim == 1
    
def test_normalization():

    X_train, X_test, y_train, y_test = model.load_train_test_data()
    X_train_norm, X_test_norm = model.z_score_normalize(X_train, X_test)

    assert X_train_norm.shape == X_train.shape
    assert X_test_norm.shape == X_test.shape

    mean = np.mean(X_train_norm)
    std = np.std(X_train_norm)
    assert np.isclose(mean, 0, atol = 1e-6)
    assert np.isclose(std, 1, atol = 1e-6)

def test_dataloader_shapes():
    
    X_train, X_test, y_train, y_test = model.load_train_test_data()
    X_train_norm, X_test_norm = model.z_score_normalize(X_train, X_test)
    train_loader, test_loader = model.create_dataloaders(X_train_norm, y_train, X_test_norm, y_test)

    batch_X, batch_y = next(iter(train_loader))
    assert batch_X.shape[1:] == (1, 200)
    assert batch_y.shape[1:] == (1, )
    assert isinstance(batch_X, torch.Tensor)
    assert isinstance(batch_y, torch.Tensor)

def test_model_forward():

    X_train, X_test, y_train, y_test = model.load_train_test_data()
    X_train_norm, X_test_norm = model.z_score_normalize(X_train, X_test)

    dummy_input = torch.tensor(X_train_norm[:8]).unsqueeze(1)
    dummy_input = dummy_input.float()

    net = model.Model()
    out = net(dummy_input)

    assert out.shape == (8, 1)