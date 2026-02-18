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
    '111','112','113','114','115','116','117','118','119',
    '121','122','123','124','200','201','202','203','205','207','208','209',
    '210','212','213','214','215','217','219','220','221','222','223','228','230','231','232','233','234'
]

all_records = []
all_annotations = []

for record_id in record_ids:
    try:
        record = wfdb.rdrecord(f'../data/{record_id}')
        annotation = wfdb.rdann(f'../data/{record_id}', 'atr')
        all_records.append(record)
        all_annotations.append(annotation)
        print(f"Loaded record {record_id}")
    except Exception as e:
        print(f"Error loading record {record_id}: {e}")

# -------------------------------------
# Clean ECG records
# -------------------------------------

cleaned_ecgs = []

for ecg_record in all_records:
    ecg_signal = ecg_record.p_signal[:,0]
    fs = ecg_record.fs

    ecg_cleaned = nk.ecg_clean(ecg_signal, sampling_rate = fs, method = "nuerokit")
    cleaned_ecgs.append(ecg_cleaned)