# Author: Lex Albrandt
# ECG analysis with Pan-Thomspon


# Python library imports
import numpy as np                           
import random as rd                            
import wave                                      
import sys                                           
import matplotlib.pyplot as plt                         
from scipy import signal                               
from statistics import stdev                              
import wfdb                                                
import neurokit2 as nk                                      


# Constants
FIGURE_DPI = 150
LABEL_SIZE = 16
TITLE_SIZE = 18
NUMBER_SIZE = 14
FIG_LINE_WIDTH = 1.4
BP_HIGH_FREQ = 15
BP_LOW_FREQ = 5
BUTTERWORTH_ORDER = 4
FIG_SIZE_LEN = 18
FIG_SIZE_WID = 6
MAJ_X_TICK = 0.2
MIN_X_TICK = 0.04
MAJ_Y_TICK = 0.5
MIN_Y_TICK = 0.1
LOW_Y_TICK = -1.5
HIGH_Y_TICK = 1.5


# ---------------------------------------------------------
# STYLING PARAMETERS
# ---------------------------------------------------------

# This section sets the parameters for labels/titles
# for all images in the script. This can also be done
# temporarily: https://matplotlib.org/stable/users/explain/customizing.html
# All of these parameters are set at runtime and take
# precendent over style sheets in matplotlib

plt.rcParams['figure.dpi'] = FIGURE_DPI                         # Sets all MPL figures to 150 dpi
plt.rcParams['axes.labelsize'] = LABEL_SIZE                     # Font size for figure labes
plt.rcParams['axes.titlesize'] = TITLE_SIZE                     # Font size for figure titles
plt.rcParams['font.size'] = NUMBER_SIZE                         # Font size for figure numbers
plt.rcParams['lines.linewidth'] = FIG_LINE_WIDTH                # Line weight for plots


# ---------------------------------------------------------
# DATA EXTRACTION FUNCTIONS
# ---------------------------------------------------------

def extract_ecg_data(record: str) -> tuple[np.ndarray, np.ndarray, int]:
    """
    Extracts ECG data using the wfdb libary

    Args:
        record_name (string): record name without file extension
        clean (bool): allows for raw vs clean data

    Returns:
        tuple: time_ECG (time array), wave_data (signal data in mV), sample_rate (int)
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
    # Then each element is divided by the sample rate which creates a time point for each
    # sample
    time_ECG = np.arange(len(wave_data)) / sample_rate
    
    return time_ECG, wave_data, sample_rate


# --------------------------------------------------------
# PAN-THOMKINS ALGORITHM STEPS
# --------------------------------------------------------

def band_pass_ECG(ecg_signal: np.ndarray, sample_rate: int, low_freq: int = BP_LOW_FREQ, high_freq: int = BP_HIGH_FREQ) -> np.ndarray:
    """
    Step 1: Bandpass filter (5-15 Hz) to maximize QRS energy
    
    This function takes ecg signal data and applies a bandpass filter
    The reason for using a bandpass filter here is to maximize QRS energy, supress baseline wander
    and muscle noise, and make other steps in the Pan-Thomkins algorithm more reliable

    Args:
        ecg_signal (array): ECG sginal data
        sample_rate (int): sampling frequency
        low_freq (float): high-pass cutoff frequency (default: 5 Hz)
        high_freq (float): low-pass cutoff frequency (default: 15 Hz)

    Returns:
        ECG_BP_filt (array): bandpass filtered ECG signal
    """

    # We want to normalize the high and low frequencies to a Nyquist frequency
    # Nyquist = sample_rate / 2 = 360 / 2 = 180 Hz
    # Normalized = 5 Hz / 180 Hz = 0.0278
    # The Nyquist frequency essentially sets the ceiling for the the filter,
    # in this case, both the low and high frequencies
    nyquist = sample_rate / 2
    W1 = low_freq / nyquist                 # Normalized low cutoff (high-pass)
    W2 = high_freq / nyquist                # Normalized high cutoff (low-pass)

    # Create the b and a coefficients that will be passed to the singal.filtfilt() function
    # later. We do this using a 4th order butterworth filter, which is commonly used in 
    # ECG analysis. The 4th order butterworth filter supresses the out-of-band noise more strongly
    # while simultaneously preservin the QRS frequency for reliable detection
    b, a = signal.butter(BUTTERWORTH_ORDER, [W1, W2], 'bandpass')

    # Apply zero-phase filtering with filtfilt to compensate for delay
    # if we had used signal.lfilter() it would introduce a delay, which shifts the time
    # relative to the original, which we don't want
    ECG_BP_filt = signal.filtfilt(b, a, ecg_signal)

    return ECG_BP_filt

    
def differentiate(ecg_signal: np.ndarray) -> np.ndarray:
    """
    Step 2: Derivative filter to emphasize QRS slope

    Compute a single point difference of the signal of the ECG and square it
    This emphasizes the high-frequency components (QRS complexes)

    Args:
        ecg_signal (np.ndarray): Bandpass filtered ECG signal

    Returns:
        diff_ecg (np.ndarray): Differentiated and squared ECG signal
    """

    # Differentiates the ECG signal
    ECG_diff = np.diff(ecg_signal)

    # Squares the differentiated signal
    ECG_sq = np.power(ECG_diff, 2)

    # Insert the first value of the ECG_sq at index 0 to maintain original length
    # this is because np.diff() reduces the length by 1, so we add the element back
    diff_ecg = np.insert(ECG_sq, 0, ECG_sq[0])

    return diff_ecg

def MovingAverage(ECG, N = 30):
    """ This function computes the moving average of signal ECG with a rectangular
        window of N

    Args:
        ECG (np.ndarray): Differentiated and squared ECG signal
        N (int): average window size, defaults to 30
    """

    window = np.ones((1, N)) / N
    move_avg_ecg = np.convolve(np.squeeze(ECG), np.squeeze(window))
    
    return move_avg_ecg

def QRSpeaks(ECG, Fs):
    
    peaks, _ = signal.find_peaks(ECG, height = np.mean(ECG), distance = round(Fs * 0.200))
    return peaks



# List of sample files
normal_sinus_examples = ['101']

# just plotting the first 10 seconds
for i in range(0, len(normal_sinus_examples)):

    # Extracts the data for each file
    time_ECG, wave_data, sample_rate = extract_ecg_data(normal_sinus_examples[i])

    # Apply bandpass filter
    bandpass_filtered = band_pass_ECG(wave_data, sample_rate)

    # Apply differentiation
    differentiated_result = differentiate(bandpass_filtered)

    # Apply moving average
    move_avg_result = MovingAverage(differentiated_result)

    # Peaks result
    peaks_result =  QRSpeaks(move_avg_result, sample_rate)
        

    # This allows us to set the duration to however long we would like (in seconds)
    duration = 6     
    end_index = int(duration * sample_rate)

    # set a subset for time and wave data
    time_ECG_subset = time_ECG[:end_index]
    wave_data_subset = wave_data[:end_index]
    bandpass_subset = bandpass_filtered[:end_index]
    differentiated_subset = differentiated_result[:end_index]
    move_avg_subset = move_avg_result[:end_index]

    # Calculate scaling factors for visualization
    scale_factor = np.max(np.abs(wave_data_subset)) / np.max(np.abs(differentiated_subset))
    differentiated_plot = differentiated_subset * scale_factor

    scale_factor_ma = np.max(np.abs(wave_data_subset)) / np.max(np.abs(move_avg_subset))
    move_avg_plot = move_avg_subset * scale_factor_ma

    # find peaks within plotting window
    peaks_in_window = peaks_result[peaks_result < end_index]
    peak_times = time_ECG[peaks_in_window]
    peak_values = move_avg_plot[peaks_in_window]

    # creates a figure with len x width dimensions
    plt.figure(figsize = (FIG_SIZE_LEN, FIG_SIZE_WID))

    # Sets x-axis label (default alignment is center)
    plt.xlabel("Time (s)")

    # Set y-axis label
    plt.ylabel("Voltage (mV)")

    # Plot the data
    # plt.plot(x, y, color)
    plt.plot(time_ECG_subset, wave_data_subset, 'k', label = "Raw ECG", alpha = 1)
    plt.plot(time_ECG_subset, bandpass_subset, 'b', label = "bandpass filtered", alpha = 0.7)
    plt.plot(time_ECG_subset, differentiated_plot, 'g', label = "differentiated", alpha = 0.7)
    plt.plot(time_ECG_subset, move_avg_plot, 'y', label = "moving average", alpha = 0.9)
    plt.plot(peak_times, peak_values, 'o', label = "peaks", alpha = 1)

    # Declares an axes object
    axis = plt.gca()

    # Set tick marks for ECG grid
    # syntax for np.arange(start, stop, step)
    axis.set_xticks(np.arange(0, duration + MAJ_X_TICK, MAJ_X_TICK))
    axis.set_xticks(np.arange(0, duration + MIN_Y_TICK, MIN_Y_TICK), minor = True)
    axis.set_yticks(np.arange(LOW_Y_TICK, HIGH_Y_TICK, MAJ_Y_TICK))
    axis.set_yticks(np.arange(LOW_Y_TICK, HIGH_Y_TICK, MIN_Y_TICK), minor = True)

    # Adds grid with colors
    # Alpha sets opacity (ex: 0.6 = 60% opaque, 40% transparent)
    axis.grid(True, which = 'major', color = 'red', alpha = 0.6, linewidth = 1.0)
    axis.grid(True, which = 'minor', color = 'red', alpha = 0.3, linewidth = 0.5)

    # Shows title and plots
    plt.title(f"ECG Record: {normal_sinus_examples[i]} - Lead II")
    plt.show()



