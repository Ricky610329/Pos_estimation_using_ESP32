


#our CSI model can only detect 20HZ max because the serial speed
#butterworth filter
from tkinter.tix import WINDOW


BUTTER_N = 7
BUTTER_WN = 1 #critical frequency
BUTTER_OUTPUT = 'sos'
BUTTER_ANALOG = False
BANDPASS_WN = [0.05,1]
#downsampling rate
DOWNSAMPLING_S = 0.04
DOWNSAMPLING_RATE = 1/DOWNSAMPLING_S
BIAS = 0.5

#list the subcarriers that has no informationn about respiratory
NO_USE_SUB = [0,1,2,3,4,5,32,59,60,61,62,63]

#threshold for SNR subcarrier that is been selected
SNR_SUB_THRESHOLD = 5000000
CHOOSE_SUB = 5
THRESHOLD_DECLINE = 0.95


#the amount of subcarrier in one channel

SUBCARRIER = 64

#wavelet transform

LEVEL = 6
WAVELET = 'db6'

#windowing
WINDOWSIZE = 20
HOP = 3
DROP = 100