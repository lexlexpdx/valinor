'''
 # @ Author: Lex Albrandt
 # @ Create Time: 2026-02-17 09:49:53
 # @ Class: CS440
 # @ Assignment: Final Project
 # @ Description: This file contains code for model training, evaluation, and
                  predictions. 
 '''

# ---------------------------------------------
# Imports
# ---------------------------------------------

import torch
import torch.nn as nn
import torch.optim as optim
import model
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import metrics
import visuals


# ---------------------------------------------
# Hyperparameters
# ---------------------------------------------

learning_rate = 1e-5
epochs = 10
kernel_sizes = [15, 7, 3]
dec_thresh = 0.3

# ---------------------------------------------
# Reproducibility
# ---------------------------------------------

SEED = 42

torch.manual_seed(SEED)
np.random.seed(SEED)

if torch.cuda.is_available():
    torch.cuda.manual_seed(SEED)
    torch.cuda.manual_seed_all(SEED)


# ---------------------------------------------
# Train/test loop
# ---------------------------------------------

# Configure device to run on CUDA if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def run_experiment(train_loader, test_loader, dec_thresh, learning_rate = 0.001, 
                   epochs = 15, kernel_sizes = [15, 7, 3]):
    """
    Train and evaluate a 1D CNN model on the provided dataset

    This function handles the full training loop including forward pass, 
    loss computation, backpropogation, and optimizer step. It also evaluates the 
    model on the test set after each epoch. Binary predictions are computed using
    the provided decision threshold.

    Args:
        train_loader (torch.utils.data.DataLoader): DataLoader for the training 
            dataset.
        test_loader (torch.utils.data.DataLoader): DataLoader for the test
            dataset.
        dec_thresh (float): Decision threshold for convertin model outputs
            to binary predictions
        learning_rate (float, optional): Learning rate for the optimizer. 
            Defaults to 0.001.
        epochs (int, optional): Number of training epochs. Defaults to 15.
        kernel_sizes (list, optional): List of kernel sizes for each convolutional
            layer in the model. Defaults to [15, 7, 3].

    Returns:
        training_loss (list of floats): Average training loss per epoch
        testing_loss (List of floats): Average testing loss per epoch
        test_acc (List of floats): Test set accuracy for each epoch
        training_acc (List of foats): Training set accuracy for each epoch
        net (torch.nn.Module): Trained CNN model
    """

    net = model.Model(kernel_sizes).to(device)
    optimizer = optim.Adam(net.parameters(), lr = learning_rate)
    loss_function = nn.BCEWithLogitsLoss()

    training_loss = []
    testing_loss = []
    training_acc = []
    test_acc = []
    
    for epoch in range(epochs):
        
        net.train()
        
        epoch_loss = 0.0
        correct_train = 0.0
        total_train = 0

        for inputs, labels in train_loader:

            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = net(inputs)
            loss = loss_function(outputs, labels)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()

            preds = torch.sigmoid(outputs) >= dec_thresh 
            correct_train += (preds.float() == labels).sum().item()
            total_train += labels.size(0)
            
        avg_training_loss = epoch_loss / len(train_loader)
        training_loss.append(avg_training_loss)
        train_accuracy = correct_train / total_train
        training_acc.append(train_accuracy)

        print(f"""Epoch {epoch + 1}: Avg Training Loss: = {avg_training_loss:.4f}, 
              Training Acc: {train_accuracy:.4f}""")

        # -----------------------
        # Testing the model
        # -----------------------
        net.eval()
        test_loss = 0.0
        correct_test = 0.0
        total_test = 0
        
        with torch.no_grad():
            
            for inputs, labels in test_loader:

                inputs,labels = inputs.to(device), labels.to(device)
                outputs = net(inputs)
                loss = loss_function(outputs, labels)
                test_loss += loss.item()

                preds = torch.sigmoid(outputs) >= dec_thresh 
                correct_test += (preds.float() == labels).sum().item()
                total_test += labels.size(0)
                
        avg_test_loss = test_loss / len(test_loader)
        testing_loss.append(avg_test_loss)
        test_accuracy = correct_test / total_test
        test_acc.append(test_accuracy)

        print(f"""Epoch {epoch + 1}, Test loss: {avg_test_loss:.4f}, Test acc: 
              {test_accuracy:.4f}""")

    return training_loss, testing_loss, test_acc, training_acc, net


def get_all_probs(net, test_loader):
    """
    Get all probabilities and related labels from the trained 1D CNN

    This function extracts all labels and probabilities from the trained model
    and returns them as numpy arrays for further determination of metrics.

    Args:
        net (torch.nn.Module): Trained CNN model
        test_loader (torch.utils.data.DataLoader): DataLoader for the test
            dataset.

    Returns:
        all_probs (np.ndarray): 1D numpy array of predicted probabilities 
        all_labels (np.ndarray): 1D numpy array of true labels associated with
                                 predicted probabilities
    """

    net.eval()
    all_probs = []
    all_labels = []
    
    with torch.no_grad():
        for inputs, labels in test_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = net(inputs)

            probs = torch.sigmoid(outputs)

            all_probs.extend(probs.cpu().numpy().flatten())
            all_labels.extend(labels.cpu().numpy().flatten())

    
    return np.array(all_probs), np.array(all_labels)

    
def main():
    
    # Load and normalize data
    X_train, X_test, y_train, y_test = model.load_train_test_data()
    X_train_norm, X_test_norm = model.z_score_normalize(X_train, X_test)
    train_loader, test_loader = model.create_dataloaders(X_train_norm, y_train, 
                                                        X_test_norm, y_test)
    # Training
    training_loss, testing_loss, test_acc, training_acc, net = run_experiment(
                                                                train_loader, 
                                                                test_loader,
                                                                dec_thresh, 
                                                                learning_rate, 
                                                                epochs, 
                                                                kernel_sizes)

    # Get all probabilities and labels
    all_probs, all_labels = get_all_probs(net, test_loader)

    # Gather metrics
    best_thresh, best_cm, results = metrics.get_best_thresh(all_labels, all_probs)
    df_results = pd.DataFrame(results).round(3)

    # Normalize by true clas (row-wise) to obtain per-class percentages
    best_conf_mat_norm = best_cm.astype("float") / best_cm.sum(axis = 1)[:, np.newaxis]

    # Plot visuals
    visuals.plot_results_table(df_results)
    visuals.plot_prec_rec_f1_thresh(best_thresh, df_results)
    visuals.plot_confusion_matrix(best_cm, "raw")
    visuals.plot_confusion_matrix(best_conf_mat_norm, "norm")
    visuals.plot_roc_curve(all_labels, all_probs)
    visuals.print_results(training_loss, 
                          testing_loss, 
                          test_acc, 
                          training_acc, 
                          epochs, 
                          learning_rate)
    
if __name__ == "__main__":
    main()
