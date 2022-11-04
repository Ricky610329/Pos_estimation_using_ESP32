import numpy as np

from icanfi.parameter import BIAS, DOWNSAMPLING_S, SUBCARRIER,WINDOWSIZE,HOP,DROP



def convert2np(data):
    for i in range(SUBCARRIER):
        data[i] = np.array(data[i])
    data['time'] = np.array(data['time'])


'''
output:

dic{
    time:[,,,......,]
    0:[,,,......,]
}

'''
#this is for csv file
def windowing(data_raw,windowsize = WINDOWSIZE,hop = HOP,drop = DROP):
    data = data_raw.data
    start = 0
    last_w = 0
    window = []
    for i in range(len(data['time'])):
        start = i
        if data['time'][start] >= data['time'][last_w] + hop:
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
    return window

            
            

        

def downsampling(data01,Srate = DOWNSAMPLING_S,bias = BIAS,extand = False):
    if type(data01)!=dict:
        data = data01.data
    else:
        data = data01
    track = {}
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
    if type(data01)!=dict:
        data01.data =  hold
    else:
        data01 = hold

def remove_DC(data):
    for i in range(SUBCARRIER):
        mean = np.mean(data[i])
        data[i] = data[i] - mean

