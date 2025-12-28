# Import python libraries
import numpy as np                                          # Numpy for:
import random as rd                                         # Random for:
import wave                                                 # Wave for:
import sys                                                  # Sys for:
import matplotlib.pyplot as plt                             # MPL for:
from scipy.signal import butter, lfilter, filtfilt          # For data filtering
from statistics import stdev                                # For standard deviation
import wfdb                                                 # For PhysioNet plotting
sys.path.insert(1, r'./../functions')                       # Add to pythonpath

# ---------------------------------------------------------
# STYLING PARAMETERS
# ---------------------------------------------------------

# This section sets the parameters for labels/titles
# for all images in the script. This can also be done
# temporarily: https://matplotlib.org/stable/users/explain/customizing.html
# All of these parameters are set at runtime and take
# precendent over style sheets in matplotlib

plt.rcParams['figure.dpi'] = 150                                # Sets all MPL figures to 150 dpi
plt.rcParams['axes.labelsize'] = 16                             # Font size for figure labes
plt.rcParams['axes.titlesize'] = 18                             # Font size for figure titles
plt.rcParams['font.size'] = 14                                  # Font size for figure labels
plt.rcParams['lines.linewidth'] = 1.4                           # Line weight for plots



def extract_ecg_data(record):
    """
    Extracts ECG data using the wfdb libary

    Args:
        record_name (string): record name without file extension

    Returns:
        time_ECG (time array), wave_data (signal data in mV)
    """

    # I ended up using the wfdb library here because I was having trouble just extracting the
    # binary data. I don't think it was meant to be extracted that way, so the following code
    # uses the wfdb to extract the ecg data with that library. Worked on the first try. 

    # Loads the record from a subdirectory
    # Uses the wfdb function rdrecord. Note: files are read without file extension
    record_data = wfdb.rdrecord(f'mit_bih_data/{record}')

    # Extract signal data
    # p_signal is a 2D numpy array that contains physical signal data
    # Array shape: (number_samps, number_channels)
    # fs: sampling frequency of the record
    wave_data = record_data.p_signal[:, 0]
    sample_rate = record_data.fs

    # Create the time array
    # This gets the number of samples and creates an array of sample indices
    # Then each element is divided by the samply rate which creates a time point for each
    # sample
    time_ECG = np.arange(len(wave_data)) / sample_rate
    
    return time_ECG, wave_data

# List of binary files
normal_sinus_examples = ['100', '101', '102']

# just plotting the first 10 seconds
for i in range(0, len(normal_sinus_examples)):

    # Extracts the data for each file
    time_ECG, wave_data = extract_ecg_data(normal_sinus_examples[i])

    # This allows us to set the duration to however long we would like
    duration = 6                                # Duration in seconds
    sample_rate = 360                           # In Hz
    end_index = duration * sample_rate

    # set a subset for time and wave data
    time_ECG_subset = time_ECG[:end_index]
    wave_data_subset = wave_data[:end_index]

    # creates a figure that is 18 inches long and 6 inches wide
    plt.figure(figsize = (18, 6))

    # Sets x-axis label (default alignment is center)
    plt.xlabel("time (s)")

    # Set y-axis label
    plt.ylabel("Voltage (mV)")

    # Plot the data
    # plt.plot(x, y, color)
    # x-axis = time_ECG
    # y-axis = wave_data
    # color = b = blue
    plt.plot(time_ECG_subset, wave_data_subset, 'b')

    # Sets the title
    plt.title(normal_sinus_examples[i])

    # Shows each plot
    plt.show()



