import numpy as np
import collections
from icanfi.parameter import BIAS, DOWNSAMPLING_S, SUBCARRIER,WINDOWSIZE,HOP,DROP,NO_USE_SUB


def into_energy(data):
    output = {
        'time' : data['time'],
        0 : np.zeros(len(data['time']))
    }
    for sub in range(SUBCARRIER):
        if sub not in NO_USE_SUB:
            output[0] = output[0] + np.square(data[sub])

    output[0] = output[0]/SUBCARRIER
    return output


def convert2np(data):
    for i in range(SUBCARRIER):
        data[i] = np.array(data[i])
    data['time'] = np.array(data['time'])

def delta_R(data_energy):
    out = {
        'time':[],
        'r':[]
    }
    for i in range(1,len(data_energy['time'])):
        out['time'].append(data_energy['time'][i])
        out['r'].append(data_energy[0][i]-data_energy[0][i-1])
    return out

'''
output:

dic{
    time:[,,,......,]
    0:[,,,......,]
}

'''
#this is for csv file
def windowing(data,windowsize = WINDOWSIZE,hop = HOP,drop = DROP,samplerate = DOWNSAMPLING_S):
    start = 0
    last_w = 0
    window = []
    hop_m=0
    for i in range(len(data['time'])):
        start = i
        if data['time'][start] >= data['time'][last_w] + hop_m:
            index = start
            check = False
            last_w = start
            while index < len(data['time']) and data['time'][index] <= data['time'][start] + windowsize:
                last = index
                index += 1
                if  index < len(data['time']) and data['time'][last] + drop < data['time'][index]:
                    check = True
                    break
            temp = {}
            for k ,v in data.items():
                temp[k] = v[start:index]
            if check:
                window.append(0)
            else:
                window.append(temp)
        hop_m=hop
    return window[:int(windowsize*DOWNSAMPLING_S)]

    

def downsampling(data,Srate = DOWNSAMPLING_S,bias = BIAS,extand = True):
    track = collections.OrderedDict()
    second = 0
    index = 0
    hold = {
        'time':[]
    }
    while index < len(data['time']):
        if data['time'][index] < second+(Srate*bias) and data['time'][index] > second-(Srate*bias):
            track[second] = index
            second += Srate
        elif data['time'][index] >= second+(Srate*bias):
            if extand:
                track[second] = index
            second += Srate
        elif data['time'][index] <= second-(Srate*bias):
            index +=1

        
    for i in range(SUBCARRIER):
        hold[i] = []
        for j in track.values():
            hold[i].append(data[i][j])
    
    for k in track.keys():
        hold['time'].append(k)

    convert2np(hold)

    return hold

def remove_DC(data):
    for i in range(SUBCARRIER):
        mean = np.mean(data[i])
        data[i] = data[i] - mean
