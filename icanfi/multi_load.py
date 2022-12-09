import copy
import csv
import numpy as np

from icanfi.parameter import SUBCARRIER
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


def multi_load(filename,mod = 'a'):
    if mod == 'a':
        opperation = amplitude
    else:
        opperation = phase

    all_link = dict()

    link_struct = {
        "time":[]
    }
    for i in range(SUBCARRIER):
        link_struct[i] = []

    with open(filename,newline="") as csvfile:
        
        rows = csv.reader(csvfile)

        for row in rows:
            raw_data = row[0]
            if raw_data[0:4] == 'link':
                link_index = int(raw_data[4])*2 + int(raw_data[6])-1
                if link_index in all_link:
                    CSIstart = raw_data.find('[')
                    all_link[link_index]['time'].append(float(raw_data[8:CSIstart].strip()))
                    real_img_csi = raw_data[CSIstart+1:-2].split(' ')
                    real_img_csi = np.array(real_img_csi)
                    real_img_csi = real_img_csi.astype(np.float64)
                    for sub in range(SUBCARRIER):
                        value = opperation(real_img_csi[2*sub],real_img_csi[2*sub+1])
                        all_link[link_index][sub].append(value)
                else:
                    all_link[link_index] = copy.deepcopy(link_struct)
        for k in all_link.keys():
            for m in all_link[k].keys():
                all_link[k][m] = np.array(all_link[k][m])

        return all_link
