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


def new_load(filename,mod = 'a'):
    if mod == 'a':
        opperation = amplitude
    else:
        opperation = phase

    with open(filename,newline="") as csvfile:
        
        rows = csv.DictReader(csvfile)

        temp = {
            'time':[],
            'CSI':[]
        }
        for row in rows:
            if len(row['CSI'].split(' ')) == 2*SUBCARRIER+1 and row['CSI'][-1] == ']':
                temp['time'].append(row['time'])
                temp['CSI'].append(row['CSI'])
        output = {
            'time': []
        }

        for i in range(SUBCARRIER):
            output[i] = []

        for i in range(len(temp['CSI'])):
            temp['time'][i] = int(temp['time'][i])
            if len(temp['CSI'][i]) == SUBCARRIER*2:
                temp['CSI'][i] = temp['CSI'][i][1:-2].split(' ')
                temp['CSI'][i] = np.array(temp['CSI'][i])
                temp['CSI'][i] = temp['CSI'][i].astype(np.float64)
            for sub in range(SUBCARRIER):
                data = opperation(temp['CSI'][i][2*sub],temp['CSI'][i][2*sub+1])
                output[sub].append(data)
        for k in output.keys():
            output[k] = np.array(output[k])
        
