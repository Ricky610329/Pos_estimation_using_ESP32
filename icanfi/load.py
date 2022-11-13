import csv
import numpy as np

from icanfi.parameter import SUBCARRIER

SUBCARRIER

# The idea is that use it as 
def amplitude(x,y):
    return np.sqrt(np.square(x)+np.square(y))

def phase(x,y):
    if x == 0:
        return np.arctan(99999999)
    return np.arctan(y/x)


def load(filename,mod = 'a'):
    if mod == 'a':
        opperation = amplitude
    else:
        opperation = phase
    file = open(filename)
    csvfile = csv.reader(file)
    CSI = []
    TIME = []
    
    for i in csvfile:
        try:
            TIME.append(i[26])#time data
            CSI.append(i[25])#CSI data
        except IndexError:
            pass
    
    TIME = np.array(TIME[1:])
    TIME = TIME.astype(np.float64)

    CSI = CSI[1:]
    datalen = len(CSI)
    for i in range(datalen):
        CSI[i] = CSI[i][1:-2].split(' ')

    total_data = len(CSI)

    output = {
        'time':[]
    }


    for sub in range(SUBCARRIER):
        output[sub] = []

    Start = TIME[0]
    for index in range(total_data):
        if len(CSI[index]) == SUBCARRIER*2:
            CSI[index] = np.array(CSI[index])
            CSI[index] = CSI[index].astype(np.float64)
            output['time'].append(TIME[index]-Start)
            for sub in range(SUBCARRIER):
                data = opperation(CSI[index][2*sub],CSI[index][2*sub+1])
                output[sub].append(data)
        
    for k in output.keys():
        output[k] = np.array(output[k])


    return output