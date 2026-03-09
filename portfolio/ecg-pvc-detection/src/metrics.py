'''
 # @ Author: Lex Albrandt
 # @ Create Time: 2026-03-02 17:30:51
 # @ Class: CS440
 # @ Assignment: Final Project
 # @ Description: This file contains functions for all metrics computations 
 '''

# --------------------------------------
# Imports
# --------------------------------------

import numpy as np
from sklearn.metrics import confusion_matrix


def get_best_thresh(all_labels, all_probs):
    """
    

    Args:
        all_labels (_type_): _description_
        all_probs (_type_): _description_

    Returns:
        _type_: _description_
    """
    best_f1 = 0
    best_thresh = 0
    best_cm = None

    results = []

    for decision in np.linspace(0.05, 0.95, 50):

        preds = (all_probs >= decision).astype(int)
        conf_mat = confusion_matrix(all_labels, preds)
        precision, recall, f1 = compute_prec_rec_f1(conf_mat)

        results.append({
            "Threshold": decision,
            "Precision": precision,
            "Recall": recall,
            "F1": f1})

        if f1 > best_f1:
            best_f1 = f1
            best_thresh = decision
            best_cm = conf_mat

    return best_thresh, best_cm, results


def compute_prec_rec_f1(cm):
    
    TN = cm[0, 0]
    FP = cm[0, 1]
    FN = cm[1, 0]
    TP = cm[1, 1]

    # preven division by zero
    epsilon = 1e-8

    precision = TP / (TP + FP + epsilon)
    recall = TP / (TP + FN + epsilon)
    f1 = 2 * ((precision * recall) / (precision + recall + epsilon))

    return precision, recall, f1 

def get_conf_mat_indices(preds, all_labels):
    tp_idx = np.where((preds == 1) & (all_labels == 1))[0]
    tn_idx = np.where((preds == 0) & (all_labels == 0))[0]
    fp_idx = np.where((preds == 1) & (all_labels == 0))[0]
    fn_idx = np.where((preds == 0) & (all_labels == 1))[0]

    return tp_idx, tn_idx, fp_idx, fn_idx