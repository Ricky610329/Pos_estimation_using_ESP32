#our CSI model can only detect 20HZ max because the serial speed
#butterworth filter


BUTTER_N = 3
BUTTER_WN = 1 #critical frequency
BUTTER_OUTPUT = 'sos'
BUTTER_ANALOG = False
BANDPASS_WN = [0.05,1]
#downsampling rate
DOWNSAMPLING_S = 0.1
DOWNSAMPLING_RATE = 1/DOWNSAMPLING_S
BIAS = 0.01

#list the subcarriers that has no informationn about respiratory
NO_USE_SUB = [0 ,1 ,2 ,3 ,4 ,5 ,32 ,59 ,60 ,61 ,62 ,63 ,64 ,65 ,123 ,124 ,125 ,126 ,127 ,128 ,129 ,130 ,131 ,132 ,133 ,191]

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