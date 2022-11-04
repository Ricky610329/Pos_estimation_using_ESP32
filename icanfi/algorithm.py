import numpy as np
from scipy import fft
from sklearn.decomposition import PCA
from icanfi.filters import wavelet

from icanfi.parameter import SNR_SUB_THRESHOLD,SUBCARRIER,NO_USE_SUB,THRESHOLD_DECLINE,CHOOSE_SUB,DOWNSAMPLING_S

def SNR_sub(data,num_sub = CHOOSE_SUB,threshold = SNR_SUB_THRESHOLD):
    selected = []
    while len(selected)< num_sub:
        for i in range(SUBCARRIER):
            if i not in NO_USE_SUB:
                mean = np.mean(data[i])
                SNR = np.divide(data[i],mean)
                for j in SNR:
                    if len(selected) >= num_sub:
                        break
                    elif j > threshold and i not in selected:
                        selected.append(i)
        threshold *= THRESHOLD_DECLINE
    return selected

# input have to be the selected frequency
# have to be the subcarrier that is been choosen
# FFTdata
# 0: frequency
# 1: [1,1,1],[2,2,3],......
#
# Wavelet data
# app: []
# detail: [0]:[1,1,1],[2,3,5]


def do_PCA(data,selected,mod ='t'):
    output = []
    pca = PCA(n_components=1)
    for j in range(len(data[0])):
        output.append([])
        for i in selected:
            output[j].append(data[i][j])
    output = np.array(output)
    output = pca.fit_transform(output)
    if mod == 't':
        output ={
            'time': data['time'],
            'pca':output.flatten()
        }
        return output
    if mod == 'f':
        output ={
            'frequency': data['frequency'],
            'pca':output.flatten()
        }
        return output
    if mod == 'n':
        return output.flatten()

def fast_slow_classify(data,selected):
    pcawave = do_PCA(data,selected,'n')
    frequencyspec = {}
    frequencyspec["frequency"] = fft.fftfreq(len(data['time']),DOWNSAMPLING_S)
    frequencyspec["pca"] = fft.fft(pcawave)
    max = 0

    for i in range(len(frequencyspec["pca"])):
        if frequencyspec["pca"][i]> frequencyspec["pca"][max]:
            max = i

    return np.abs(frequencyspec["frequency"][max])

#def wavelet():

def PCA_fast_slow(FFTdata,Waveletdata):
    pca = PCA(n_components=1)# fit wave find common
    FFT_PCA = pca.fit_transform(np.abs(FFTdata['data']))
    max_index = np.argmax(FFT_PCA)
    hold = []
    for i in range(len(Waveletdata)):
        hold.append([])
        for j in range(len(Waveletdata[i])):
            hold[i].append(0)
    if FFT_PCA[max_index] > 0.3:#frequency is higher than 0.3Hz
        temp = pca.fit_transform(Waveletdata[2])
        hold[2] = []
        for i in range(len(temp)):
            hold[2].append(temp[i][0])
    else:#frequency is lower than 0.3Hz
        hold[1] = pca.fit_transform(Waveletdata[1])
        temp = pca.fit_transform(Waveletdata[1])
        hold[1] = []
        for i in range(len(temp)):
            hold[1].append(temp[i][0])
    for i in range(len(hold)):
        hold[i] = np.array(hold[i])

    return hold




