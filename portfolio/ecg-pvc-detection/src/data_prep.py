'''
 # @ Author: Lex Albrandt
 # @ Create Time: 2026-02-17 09:49:19
 # @ Modified by: Lex Albrandt
 # @ Modified time: 2026-02-17 11:02:53
 # @ Description: This source code handles the data prep for the ECG/PVC detection
                  project. 
 '''

# Imports
import wfdb
import numpy as np
import neurokit2 as nk
from collections import Counter

# -------------------------------------
# Download MIT-BIH Database with wfdb
# -------------------------------------

# wfdb.dl_database('mitdb', dl_dir = '../data')


# -------------------------------------
# Extract data from patients
# -------------------------------------

# 48 total patients
record_ids = [
    '100','101','102','103','104','105','106','107','108','109',
    '111','112','113','114','115','116','117','118','119','121',
    '122','123','124','200','201','202','203','205','207','208',
    '209','210','212','213','214','215','217','219','220','221',
    '222','223','228','230','231','232','233','234'
]

all_records = []
all_annotations = []

for record_id in record_ids:
    try:
        record = wfdb.rdrecord(f'../data/{record_id}')
        annotation = wfdb.rdann(f'../data/{record_id}', 'atr')
        all_records.append(record)
        all_annotations.append(annotation)
        # n_samples is not used, but is required for return from X.shape
        print(f"Loaded record {record_id}")
    except Exception as e:
        print(f"Error loading record {record_id}: {e}")


# -------------------------------------
# Clean ECG records
# -------------------------------------

cleaned_ecgs = []
sampling_rates = []

for ecg_record in all_records:
    ecg_signal = ecg_record.p_signal[:,0]
    fs = ecg_record.fs
    sampling_rates.append(fs)

    ecg_cleaned = nk.ecg_clean(ecg_signal, sampling_rate = fs, method = "neurokit")
    cleaned_ecgs.append(ecg_cleaned)

# -------------------------------------
# Beat Extraction + Labeling
# -------------------------------------

# Window constants
WINDOW_BEFORE = 100
WINDOW_AFTER = 100

# Labels
PVC_SYMBOLS = ['V', 'E']
NORMAL_SYMBOLS = ['N', 'L', 'R']

all_beats = []
all_labels = []
all_patient_ids = []

for i, record_id in enumerate(record_ids):
    
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
    
# Conver to Numpy array
X_beats = np.array(all_beats)
y_labels = np.array(all_labels)
patient = np.array(all_patient_ids)

print(X_beats.shape, y_labels.shape)

print(f"PVCs: {np.sum(y_labels == 1)}")
print(f"Normal: {np.sum(y_labels == 0)}")
print(f"Other: {np.sum(y_labels == -1)}")