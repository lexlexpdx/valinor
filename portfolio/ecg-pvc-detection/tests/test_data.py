'''
 # @ Author: Lex Albrandt
 # @ Create Time: 2026-02-24 16:36:00
 # @ Modified by: Lex Albrandt
 # @ Modified time: 2026-02-24 16:36:16
 # @ Description: This is a pytest module for data prepartation pipeline to ensure robust loading,
                  cleaning, and test/train splitting for data set.
 '''

# Config
import sys
from pathlib import Path
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

# Imports
import data_prep
import numpy as np
import model

def test_load_records():
    records, annotations = data_prep.load_records()

    # Test number of records loaded == number of original records
    assert len(records) == len(data_prep.RECORD_IDS)

    # Test number of annotations loaded == number of original records
    assert len(annotations) == len(data_prep.RECORD_IDS)

    # Test each record/annotation is the correct instance type
    for r in records:
        assert isinstance(r, data_prep.wfdb.Record)
    for a in annotations:
        assert isinstance(a, data_prep.wfdb.Annotation)
        

def test_beat_window_length():
    records, annotations = data_prep.load_records()
    cleaned_ecgs, fs_list = data_prep.clean_ecgs(records)
    X_beats, y_labels, patients = data_prep.extract_beats(cleaned_ecgs, annotations, fs_list)

    # Test window length is correct
    assert X_beats.shape[1] == data_prep.WINDOW_BEFORE + data_prep.WINDOW_AFTER
    
def test_ecg_cleaning():
    records, _ = data_prep.load_records()
    cleaned_ecgs, fs_list = data_prep.clean_ecgs(records)

    # Test number of cleaned ecg records == number of loaded records
    assert len(cleaned_ecgs) == len(records)

    # Test for correct type for cleaned records and sampling rate
    for ecg in cleaned_ecgs:
        assert isinstance(ecg, np.ndarray)
    for sig in fs_list:
        assert isinstance(sig, (int, float))

    # Test length of cleaned signal matches original signal
    for i, ecg in enumerate(cleaned_ecgs):
        original = records[i].p_signal[:,0]
        assert len(ecg) == len(original)
    
def test_beat_extraction():
    records, annotations = data_prep.load_records()
    cleaned_ecgs, fs_list = data_prep.clean_ecgs(records)
    X_beats, y_labels, patients = data_prep.extract_beats(cleaned_ecgs, annotations, fs_list)
    
    # Test number of beats, labels, and patients match original values
    assert X_beats.shape[0] == len(y_labels)
    assert X_beats.shape[0] == len(patients)
    assert X_beats.shape[1] == data_prep.WINDOW_BEFORE + data_prep.WINDOW_AFTER
    
    # Test labels are only in label_set
    label_set = {1, 0, -1}
    for label in y_labels:
        assert label in label_set
    
def test_train_test_split():
    records, annotations = data_prep.load_records()
    cleaned_ecgs, fs_list = data_prep.clean_ecgs(records)
    X_beats, y_labels, patients = data_prep.extract_beats(cleaned_ecgs, annotations, fs_list)

    test_size = 0.3
    seed = 42
    X_train, X_test, y_train, y_test, train_patients, test_patients = data_prep.split_by_patient(X_beats, y_labels,
                                                                                                 patients, test_size,
                                                                                                 seed)
    # Test patients only occur in training OR test, not both
    for patient in train_patients:
        assert patient not in test_patients
    for patient in test_patients:
        assert patient not in train_patients

    # Test number of samps in X matches labels for both train and test
    assert X_train.shape[0] == len(y_train)
    assert X_test.shape[0] == len(y_test)
    
