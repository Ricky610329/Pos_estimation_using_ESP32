import numpy as np
from scipy import signal
from scipy import fft
import pywt

from icanfi.parameter import DOWNSAMPLING_S, SUBCARRIER, BUTTER_N, BUTTER_WN, BUTTER_OUTPUT,BUTTER_ANALOG,DOWNSAMPLING_RATE,LEVEL,WAVELET,BANDPASS_WN

Lowpass_filter = signal.butter(BUTTER_N,BUTTER_WN,btype = 'lowpass',analog = BUTTER_ANALOG,output = BUTTER_OUTPUT,fs = DOWNSAMPLING_RATE)
Bandpass_filter = signal.butter(BUTTER_N,BANDPASS_WN,btype = 'bandpass',analog = BUTTER_ANALOG,output = BUTTER_OUTPUT,fs = DOWNSAMPLING_RATE)
def lowpass(data):
    data[0] = signal.sosfilt(Lowpass_filter,data[0])

def bandpass(data):
    data[0] = signal.sosfilt(Bandpass_filter,data[0])

#will return a dic
def data_fft(data):
    hold = {}
    hold["frequency"] = fft.fftfreq(len(data['time']),DOWNSAMPLING_S)
    hold[0] = fft.fft(data[0])

    return hold


#input the data that is needed to to transform
def wavelet(data,l = LEVEL,wave_f = WAVELET):
    
    output = pywt.wavedec(data[0],wave_f,level=l)
    
    return output