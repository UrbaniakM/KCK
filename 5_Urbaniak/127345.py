import sys
from scipy.io import wavfile
from scipy import *
import numpy as np
from scipy.signal import decimate
import glob
import matplotlib.pyplot

def is_male(filename):
    if filename[10] == 'M':
        return True
    return False


def hps(sample_rate, signal):
    signal = [mean(s) for s in signal] #srednia z kanalow
    
    divider = 5 #co 5 probka
    N = 524288 # 2^k, liczba probek fft
    freq = np.arange(N) / N;

    val = np.fft.fft(signal, N)
    val = np.abs(val[:int(len(val) / 2)]) # pierwsza polowa probek
    freq = freq[:int(len(freq) / 2)] # pierwsza polowa

    return_length = int(np.ceil(freq.size / divider)) # 1/5 probek
    return_val = val[:return_length].copy()
    for i in range(2, divider+1):
        return_val *= val[::i][:return_length]

    freq = freq[:return_length] * sample_rate
    return (freq, return_val)

def voice_gender_recognition(filename):
    sample_rate, signal = wavfile.read(filename)
    signal = [mean(s) for s in signal] #srednia z kanalow
    
    freqs, values = hps(sample_rate, signal)
    max_val_index = values.argmax()
    avg_freq = freqs[max_val_index]

    male_voice_min = 50
    male_voice_max = 160
    female_voice_min = 161
    female_voice_max = 255

    if avg_freq >= 50 and avg_freq <= 255: # w przedziale
        if avg_freq <= 160:
            print('M')
            if is_male(filename):
                return 1
            return 0
        else:
            print('K')
            if not(is_male(filename)):
                return 1
            return 0
    else:
        male_freq_sum = 0.0
        female_freq_sum = 0.0
        
        for freq, value in zip(freqs,values):
            if freq >= 50 and freq <= 160:
                male_freq_sum += value
            if freq > 160 and freq <= 255:
                female_freq_sum += value
        
        if male_freq_sum > female_freq_sum:
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
