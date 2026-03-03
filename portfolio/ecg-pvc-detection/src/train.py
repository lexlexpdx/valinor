'''
 # @ Author: Lex Albrandt
 # @ Create Time: 2026-02-17 09:49:53
 # @ Description: This file contains code for the training and evaluation loops for model.py
 '''

# Imports
import torch
import torch.nn as nn
import torch.optim as optim
import model
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve, auc
import numpy as np

# ----------------------------------------------
# Load data, normalize, and create dataloaders
# ----------------------------------------------

X_train, X_test, y_train, y_test = model.load_train_test_data()
X_train_norm, X_test_norm = model.z_score_normalize(X_train, X_test)
train_loader, test_loader = model.create_dataloaders(X_train_norm, y_train, X_test_norm, y_test)

# ---------------------------------------------
# Hyperparameters
# ---------------------------------------------

learning_rate = 1e-5
epochs = 10
kernel_sizes = [15, 7, 3]
dec_thresh = 0.3

# ---------------------------------------------
# Train/test loop
# ---------------------------------------------

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def run_experiment(train_loader, test_loader, dec_thresh, learning_rate = 0.001, epochs = 15, kernel_sizes = [15, 7, 3]):

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

        print(f"Epoch {epoch + 1}: Avg Training Loss: = {avg_training_loss:.4f}, Training Acc: {train_accuracy:.4f}")

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

        print(f"Epoch {epoch + 1}, Test loss: {avg_test_loss:.4f}, Test acc: {test_accuracy:.4f}")

    return training_loss, testing_loss, test_acc, training_acc, net


def print_results(training_loss, testing_loss, test_acc, training_acc):
    
    epochs_range = range(1, epochs + 1)

    plt.figure()
    plt.plot(epochs_range, training_loss, label = "Training Loss")
    plt.plot(epochs_range, testing_loss, label = "Testing Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.title(f"Loss vs Epoch: LR = {learning_rate}, ")
    plt.legend()
    plt.grid(True)
    plt.show()
    
    plt.figure()
    plt.plot(epochs_range, training_acc, label = "Training Accuracy")
    plt.plot(epochs_range, test_acc, label = "Testing Accuracy")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.title(f"Accuracy vs Epoch: LR = {learning_rate}, ")
    plt.legend()
    plt.grid(True)
    plt.show()

def calculate_confusion_matrix(net, test_loader, dec_thresh):
    
    net.eval()
    all_preds = []
    all_labels = []
    
    with torch.no_grad():
        for inputs, labels in test_loader:
            inputs = inputs.to(device)
            outputs = net(inputs)
            preds = (torch.sigmoid(outputs) >= dec_thresh).float()

            all_preds.extend(preds.cpu().numpy().flatten())
            all_labels.extend(labels.numpy().flatten())

    cm = confusion_matrix(all_labels, all_preds)
    
    return cm
    

def plot_confusion_matrix(cm, plot_type):
   
    if plot_type == "raw":
        plt.figure()
        plt.imshow(cm)
        plt.title("Raw Confusion Matrix")
        plt.xlabel("Predicted Label")
        plt.ylabel("True label")
        plt.xticks([0, 1], ["Normal", "PVC"])
        plt.yticks([0, 1], ["Normal", "PVC"])

        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                plt.text(j, i, cm[i, j], ha = "center", va = "center")
    
    if plot_type == "norm":
        plt.figure()
        plt.imshow(cm)
        plt.title("Normalized Confusion Matrix")
        plt.xlabel("Predicted Label")
        plt.ylabel("True label")
        plt.xticks([0, 1], ["Normal", "PVC"])
        plt.yticks([0, 1], ["Normal", "PVC"])

        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                value = cm[i, j] * 100
                plt.text(j, i, f"{value:.1f}%")

    plt.colorbar()
    plt.tight_layout()
    plt.show()

def compute_prec_rec_f1(cm, dec_thresh):
    
    TN = cm[0, 0]
    FP = cm[0, 1]
    FN = cm[1, 0]
    TP = cm[1, 1]

    precision = TP / (TP + FP)
    recall = TP / (TP + FN)
    f1 = 2 * ((precision * recall) / (precision + recall))

    print(f"Precision: {precision:.4f}, Decision Threshold: {dec_thresh}")
    print(f"Recall: {recall:.4f}, Decision Threshold: {dec_thresh}")
    print(f"F1 score: {f1:.4f}, Decision Threshold {dec_thresh}")

    return precision, recall, f1
    
    
def compute_roc_auc(net, test_loader):

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

    roc_auc = roc_auc_score(all_labels, all_probs)
    
    return roc_auc

def plot_roc_curve(net, test_loader):
    
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

    fpr, tpr, _ = roc_curve(all_labels, all_probs)
    roc_auc = auc(fpr, tpr)

    plt.figure()
    plt.plot(fpr, tpr, color="darkorange", lw = 2, label = f'ROC curve (AUC = {roc_auc:.4f})')
    plt.plot([0, 1], (0, 1), color = "navy", lw = 2, linestyle = "--")
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("Receiver Operating Characteristic")
    plt.legend(loc = "lower right")
    plt.grid(True)
    plt.show()

def main():
    
    # Initial training using BCE with logits loss
    training_loss, testing_loss, test_acc, training_acc, net = run_experiment(train_loader, 
                                                                              test_loader,
                                                                              dec_thresh, 
                                                                              learning_rate, 
                                                                              epochs, 
                                                                              kernel_sizes)
    print_results(training_loss, testing_loss, test_acc, training_acc)

    all_precision = [{}]
    all_recall = [{}]
    all_f1 = [{}]
    
    conf_mat = calculate_confusion_matrix(net, test_loader, decision)

    for decision in np.arange(0.1, 1, 0.1):
        precision, recall, f1 = compute_prec_rec_f1(conf_mat, decision)

        all_precision.append(decision, precision)
        all_recall.append(decision, recall)
        all_f1.append(decision, f1)

    print(all_precision)
    print(all_recall)
    print(all_f1)

    conf_mat_norm = conf_mat.astype("float") / conf_mat.sum(axis = 1)[:, np.newaxis]
    plot_confusion_matrix(conf_mat, "raw")
    plot_confusion_matrix(conf_mat_norm, "norm")
    auc = compute_roc_auc(net, test_loader)
    print(f"ROC-AUC Score: {auc:.4f}")
    plot_roc_curve(net, test_loader)

    
if __name__ == "__main__":
    main()
