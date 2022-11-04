import numpy as np
from scipy import fft

from icanfi.parameter import DOWNSAMPLING_S

#[frequency_index,frequency_amplitude]
def estimate_fft(denoise,mod = 's'):
    output = [fft.fftfreq(len(denoise),DOWNSAMPLING_S),np.abs(fft.fft(denoise))]
    if mod == 's': #return spectrum
        return output
    
    if mod == 'r':
        max_index = 0
        for i in range(len(output[1])):
            if output[1][i] > output[1][max_index]:
                max_index = i
        return output[0][max_index]