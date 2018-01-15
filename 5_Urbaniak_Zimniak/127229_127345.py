import sys
from scipy.io import wavfile
from scipy import *
import numpy as np
from scipy.signal import decimate
import glob

def is_male(filename):
    if filename[10] == 'M':
        return True
    return False

def filter_frequencies(signal, w, signal_len):
    retFrequency = []
    retSignal = []
    frequency = linspace(0,w,signal_len)
    for i in range(len(frequency)):
        if 85 <= frequency[i] <= 255:
            retFrequency.append(frequency[i])
            retSignal.append(signal[i])
    return (retFrequency, retSignal)

def average_frequency(frequency, signal):
    return frequency[signal.index(max(signal))]

def voice_gender_recognition(filename):
    w, signal = wavfile.read(filename)
    signal = [mean(s) for s in signal] #srednia z kanalow
    n = len(signal)
    signal = np.log(abs(fft(signal)))
    signal = signal[0:len(signal) // 2]
    
    freq, sig = filter_frequencies(signal,w, n)
    avg_freq = average_frequency(freq, sig)
    if avg_freq < 165:
        print('M')
        if is_male(filename):
            return 1
        return 0
    else:
        print('K')
        if not(is_male(filename)):
            return 1
        return 0

def process_files():
    filenames_list = glob.glob("train/*.wav") # usuniete pliki 001 (problem z headerem pliku WAV) oraz 072 i 073 (problem z Chunkami)
    valid = 0
    for i in range(len(filenames_list)):
        valid = valid + voice_gender_recognition(filenames_list[i])
    print(valid/len(filenames_list))


if __name__ == '__main__':
    #process_files() # do testow - skutecznosc algorytmu wynosi 73%
    voice_gender_recognition(sys.argv[1])
