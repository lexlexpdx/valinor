'''
 # @ Author: Lex Albrandt
 # @ Create Time: 2026-02-25 13:01:09
 # @ Class: CS440
 # @ Assignement: Final Project
 # @ Description: This file contains all functions related to the data preparation
                  pipeline for use with model.py and train.py
 '''

# --------------------------------------
# Imports
# --------------------------------------

import wfdb
import numpy as np
import neurokit2 as nk
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

# -------------------------------------
# Download MIT-BIH Database with wfdb
# -------------------------------------

wfdb.dl_database('mitdb', dl_dir = '../data')

# -------------------------------------
# Config
# -------------------------------------

# Beat window constants
WINDOW_BEFORE = 100
WINDOW_AFTER = 100

# Beat annotation constants
PVC_SYMBOLS = ['V', 'E']
NORMAL_SYMBOLS = ['N', 'L', 'R']

# Record ID constants
RECORD_IDS = [
    '100','101','102','103','104','105','106','107','108','109',
    '111','112','113','114','115','116','117','118','119','121',
    '122','123','124','200','201','202','203','205','207','208',
    '209','210','212','213','214','215','217','219','220','221',
    '222','223','228','230','231','232','233','234'
]

def load_records():
    """
    Load all MIT-BIH records.
    
    This function loads all 48 records from the MIT-BIH dataset and outputs 
    console data indicating success or failure in loading. Utilizes the WFDB 
    library to extract necessary records and annotations.

    Returns:
        all_records (list): List of all patient ECG records
        all_annotations (list): List of all annotations for associated patient
            ECG record
    """

    all_records = []
    all_annotations = []

    for record_id in RECORD_IDS:
        try:
            record = wfdb.rdrecord(f'../data/raw/{record_id}')
            annotation = wfdb.rdann(f'../data/raw/{record_id}', 'atr')
            all_records.append(record)
            all_annotations.append(annotation)
            print(f"Loaded record {record_id}")
        except Exception as e:
            print(f"Error loading record {record_id}: {e}")
    
    return all_records, all_annotations

    
def clean_ecgs(all_records):
    """
    Cleans all ecg samples for each patient.
    
    This function extracts the first lead (default: MLII) for each patient along
    with sampling rate, and preprocesses the data using the Neurokit library.
    The "neurokit" method performs a 5th order 0.5 Hz high-pass butterworth filter
    followed by 50 Hz powerline filter.

    Args:
        all_records (List): List of all patient ECG records

    Returns:
        _type_: _description_
    """
    cleaned_ecgs = []
    sampling_rates = []

    for ecg_record in all_records:
        ecg_signal = ecg_record.p_signal[:,0]
        fs = ecg_record.fs
        sampling_rates.append(fs)

        ecg_cleaned = nk.ecg_clean(ecg_signal, 
                                   sampling_rate = fs, 
                                   method = "neurokit")
        cleaned_ecgs.append(ecg_cleaned)

    return cleaned_ecgs, sampling_rates


def extract_beats(cleaned_ecgs, all_annotations, sampling_rates):

    all_beats = []
    all_labels = []
    all_patient_ids = []

    for i, record_id in enumerate(RECORD_IDS):
        
        ecg_cleaned = cleaned_ecgs[i]
        annotations = all_annotations[i]
        fs = sampling_rates[i]

        # Convert symbols -> Labels
        # PVC = 1, Normal = 0
        beat_labels = []
        for symbol in annotations.symbol:
            if symbol in PVC_SYMBOLS:
                beat_labels.append(1)
            elif symbol in NORMAL_SYMBOLS:
                beat_labels.append(0)
            else:
                beat_labels.append(-1)
            
        beat_labels = np.array(beat_labels)

        # Extract Beats
        for j, r_peak in enumerate(annotations.sample):
            
            # Skip beats we are not interested in
            if beat_labels[j] == -1:
                continue

            start = r_peak - WINDOW_BEFORE
            end = r_peak + WINDOW_AFTER

            # Skip beats too close to edges
            if start < 0 or end >= len(ecg_cleaned):
                continue
            
            segment = ecg_cleaned[start:end]

            if len(segment) == WINDOW_BEFORE + WINDOW_AFTER:
                all_beats.append(segment)
                all_labels.append(beat_labels[j])
                all_patient_ids.append(record_id)
        
    # Convert to Numpy array
    X_beats = np.array(all_beats)
    y_labels = np.array(all_labels)
    patients = np.array(all_patient_ids)

    # Distributions
    print(X_beats.shape, y_labels.shape)
    print(f"PVCs: {np.sum(y_labels == 1)}")
    print(f"Normal: {np.sum(y_labels == 0)}")
    print(f"Other: {np.sum(y_labels == -1)}")

    return X_beats, y_labels, patients


def split_by_patient(X_beats, y_labels, patients, test_size = 0.3 , seed = 42):

    # Get unique patient ids
    unique_patients = np.unique(patients)

    train_patients, test_patients = train_test_split(
        unique_patients,
        test_size = test_size,
        random_state = seed,
        shuffle = True
    )

    print(f"Train patients: {train_patients}")
    print(f"Test patients: {test_patients}")

    train_mask = np.isin(patients, train_patients)
    test_mask = np.isin(patients, test_patients)

    X_train, y_train = X_beats[train_mask], y_labels[train_mask]
    X_test, y_test = X_beats[test_mask], y_labels[test_mask]

    print(f"Train shape: {X_train.shape, y_train.shape}")
    print(f"Test shape: {X_test.shape, y_test.shape}")

    # Shuffle within train/test
    idx = np.random.permutation(len(X_train))
    X_train, y_train = X_train[idx], y_train[idx]

    idx = np.random.permutation(len(X_test))
    X_test, y_test = X_test[idx], y_test[idx]

    return X_train, X_test, y_train, y_test


def save_arrays(X_train, X_test, y_train, y_test):
    np.save('../data/processed/X_train.npy', X_train)
    np.save('../data/processed/y_train.npy', y_train)
    np.save('../data/processed/X_test.npy', X_test)
    np.save('../data/processed/y_test.npy', y_test)


def main():

    records, annotations = load_records()
    cleaned, fs_list = clean_ecgs(records)
    X_beats, y_labels, patients = extract_beats(cleaned, annotations, fs_list)
    X_train, X_test, y_train, y_test = split_by_patient(X_beats, y_labels, patients)
    save_arrays(X_train, X_test, y_train, y_test)
    

if __name__ == "__main__":
    main()