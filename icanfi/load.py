import csv
import numpy as np
import re

from icanfi.parameter import SUBCARRIER

SUBCARRIER

# The idea is that use it as 
def amplitude(x,y):
    return np.sqrt(np.square(x)+np.square(y))

def phase(x,y):
    if x == 0:
        return np.arctan(99999999)
    return np.arctan(y/x)

def convert(s):
    output = []
    for i in s[1:len(s)-2:1].split(" "):
        output.append(float(i))
    return output

#this is for analysis not for real time process
class dataset:
    
    def __init__(self):
        self.data = {
            'time':[]
        }
    
    def setfile(self,filename,mod = 'a'):
        if mod == 'a':
            opperation = amplitude
        else:
            opperation = phase
        file = open(filename)
        csvfile = csv.reader(file)
        dataset = []
        for i in csvfile:
            dataset.append(i)

        Preprocessed = []

        for i in range(1,len(dataset)):
            Preprocessed.append([])
            Preprocessed[i-1].append(float(dataset[i][-1]))
            Preprocessed[i-1].append(convert(dataset[i][-2]))
        
        for j in range(SUBCARRIER):
            self.data[j] = []

        for i in range(len(Preprocessed)):
            self.data['time'].append(Preprocessed[i][0])
            for j in range(SUBCARRIER):
                self.data[j].append(opperation(Preprocessed[i][1][2*j],Preprocessed[i][1][2*j+1]))

        length = len(self.data['time'])
        
        hold = self.data['time'][0]
        for i in range(length):
            self.data['time'][i] = self.data['time'][i] - hold
        
        for k,v in self.data.items():
            self.data[k] = np.array(v)

def load_r(s):
    temp=  np.array(re.split('\s+',s[1:-2]))
    return temp.astype(int)



