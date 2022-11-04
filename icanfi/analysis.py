import matplotlib.pyplot as plt

from icanfi.parameter import SUBCARRIER

SUBCARRIER

def analysis_time(data,Lsub = 0,Usub = SUBCARRIER,Sframe = 0,Eframe = None):
    s = ('Lsub = {}, Usub = {}, Sframe = {},Eframe = {}').format(Lsub,Usub,Sframe,Eframe)
    plt.title(s,fontsize = 10)
    if not Eframe:
        Eframe = len(data['time'])
    for i in range(Lsub,Usub):
        plt.plot(data['time'][Sframe:Eframe],data[i][Sframe:Eframe])
    plt.xlabel('second')
    plt.ylabel('amplitude')
    plt.show()

def analysis_sub(data,Lsub = 0,Usub = SUBCARRIER,Sframe = 0,Eframe = None):
    s = ('Lsub = {}, Usub = {}, Sframe = {},Eframe = {}').format(Lsub,Usub,Sframe,Eframe)
    plt.title(s,fontsize = 10)
    if not Eframe:
        Eframe = len(data['time'])
    for frame in range(Sframe,Eframe):
        hold = []
        for sub in range(Lsub,Usub):
            hold.append(data[sub][frame])
        plt.plot(list(range(Lsub,Usub)),hold)
        hold.clear()
    plt.xlabel('second')
    plt.ylabel('amplitude')
    plt.show()

def frame_distance(data):
    track = {}
    for frame in range(1,len(data['time'])):
        hold = data['time'][frame] - data['time'][frame-1]
        if hold not in track:
            track[hold] = 1
        else:
            track[hold] +=1
    for k,v in track.items():
        print(k,':',v)