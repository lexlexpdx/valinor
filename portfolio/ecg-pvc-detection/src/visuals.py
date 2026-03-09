'''
 # @ Author: Lex Albrandt
 # @ Create Time: 2026-03-02 17:31:28
 # @ Description: This code contains all functions for data visualizations
 '''

import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
import pandas as pd

def print_results(training_loss, testing_loss, test_acc, training_acc, epochs, learning_rate):
    
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

def plot_confusion_matrix(cm, plot_type):
   
    plt.figure()
    plt.imshow(cm)
    plt.colorbar()

    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            value = cm[i, j]
            if plot_type == "norm":
                display = f"{value * 100:.1f}%"
            elif plot_type == "raw":
                display = str(int(value))

            # TN/FP/FN/TP labels
            if i == 0 and j == 0:
                display += "\n(TN)"
            elif i == 0 and j == 1:
                display += "\n(FP)"
            elif i == 1 and j == 0:
                display += "\n(FN)"
            elif i == 1 and j == 1:
                display += "\n(TP)"
            plt.text(j, i, display, ha = "center", va = "center", color = "black", fontsize = 12)

    if plot_type == "raw":
        plt.title("Raw Confusion Matrix from Best Threshold")
    else:
        plt.title("Normalized Confusion Matrix from Best Threshold")
    plt.xlabel("Predicted Label")
    plt.ylabel("True label")
    plt.xticks([0, 1], ["Normal", "PVC"])
    plt.yticks([0, 1], ["Normal", "PVC"])
    plt.tight_layout()
    plt.show()

    
def plot_roc_curve(all_labels, all_probs):
    
    fpr, tpr, _ = roc_curve(all_labels, all_probs)
    roc_auc = auc(fpr, tpr)

    plt.figure()
    plt.plot(fpr, tpr, color="darkorange", lw = 2, label = f'ROC curve (AUC = {roc_auc:.4f})')
    plt.plot([0, 1], (0, 1), color = "navy", lw = 2, linestyle = "--")
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("Receiver Operating Characteristic (ROC)")
    plt.legend(loc = "lower right")
    plt.grid(True)
    plt.show()
    
def plot_prec_rec_f1_thresh(best_thresh, df_results):
    
    plt.figure(figsize=(8, 5))
    plt.plot(df_results["Threshold"], df_results["Precision"], label = "Precision", marker = 'o')
    plt.plot(df_results["Threshold"], df_results["Recall"], label = "Recall", marker = 'o')
    plt.plot(df_results["Threshold"], df_results["F1"], label = "F1 Score", marker = 'o')
    plt.axvline(best_thresh, color = 'red', linestyle = "--", label = f"Best F1 Threshold: {best_thresh:.2f}")
    plt.xlabel("Decision Threshold")
    plt.ylabel("Score")
    plt.title("Precision, Recall, F1 vs Decision Threshold")
    plt.grid(True)
    plt.legend()
    plt.show()

def plot_results_table(df):

    df_sorted = df.sort_values(by = "F1", ascending = False).head(5)

    fig, ax = plt.subplots(figsize = (5, 5 * 0.5 + 1))
    ax.axis("off")

    table = ax.table(cellText = df_sorted.values,
                     colLabels = df_sorted.columns,
                     cellLoc = "center",
                     loc = "center")

    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 1.5)

    for col in range(len(df_sorted.columns)):
        cell_text = table[(0, col)].get_text()
        cell_text.set_fontweight('bold')
        cell_text.set_fontsize('14')

    plt.title("Top Thresholds by F1 Score", fontsize = 16, pad = 3, fontweight = 'bold')
    plt.show()


def plot_grid(beats, indices, title, n=6):
    
    fig, axes = plt.subplots(2, 3, figsize = (10, 6))
    axes = axes.flatten()
    
    for i in range(n):
        
        idx = indices[i]
        axes[i].plot(beats[idx])
        axes[i].set_title(f"Beat {idx}")
        axes[i].set_xticks([])
        axes[i].set_yticks([])

    fig.suptitle(title)
    plt.tight_layout()
    plt.show()
