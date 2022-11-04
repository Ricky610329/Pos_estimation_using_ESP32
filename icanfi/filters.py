import numpy as np
from scipy import signal
from scipy import fft
import pywt

from icanfi.parameter import DOWNSAMPLING_S, SUBCARRIER, BUTTER_N, BUTTER_WN, BUTTER_OUTPUT,BUTTER_ANALOG,DOWNSAMPLING_RATE,LEVEL,WAVELET,BANDPASS_WN

Lowpass_filter = signal.butter(BUTTER_N,BUTTER_WN,btype = 'lowpass',analog = BUTTER_ANALOG,output = BUTTER_OUTPUT,fs = DOWNSAMPLING_RATE)
Bandpass_filter = signal.butter(BUTTER_N,BANDPASS_WN,btype = 'bandpass',analog = BUTTER_ANALOG,output = BUTTER_OUTPUT,fs = DOWNSAMPLING_RATE)
def lowpass(data):
    for i in range(SUBCARRIER):
        data[i] = signal.sosfilt(Lowpass_filter,data[i])

def bandpass(data):
    for i in range(SUBCARRIER):
        data[i] = signal.sosfilt(Bandpass_filter,data[i])

#will return a dic
def data_fft(data):
    hold = {}
    hold["frequency"] = fft.fftfreq(len(data['time']),DOWNSAMPLING_S)
    for i in range(SUBCARRIER):
        hold[i] = fft.fft(data[i])

    return hold


#input the data that is needed to to transform
def wavelet(data,selected,l = LEVEL,wave_f = WAVELET):
    
    output = []
    for i in selected:
        output.append(pywt.wavedec(data[i],wave_f,level=l))
    
    return output