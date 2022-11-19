# **Pos estimation using ESP32**

This program is build for estimate Position using ESP32.

## **icanfi**
-------------------
Under module icanfi, it cantain the function to **load csv file** of capture CSI data, **preprocess** it and some **filter utility**.

### **load.py and new_load.py**

To load csv file that is capture from ```idf monitor``` you can use ```icanfi.load``` to do the trick. If you use the utility provide in ```connection``` -> ```serial_load.py``` please rember to use ```icanfi.new_load``` to help you througt the work.

|utility|description|
|----|----|
|**icanfi.load(filename,mod = 'a')**|use it to load ```idf monitor``` file ```mod``` stands for capture data type: 'a' amplitude, 'p' phase|
|**icanfi.new_load(filename,mod = 'a')**|use it to load ```erial_load.py``` file ```mod``` stands for capture data type: 'a' amplitude, 'p' phase|

After you load the csv file, the data will be store in format below:

```python
#dict(np.array)

CSI_data = {
    "time" : np.array([*time sequence*]),
    0 : np.array([*CSI data sequence*]), #subcarrier index - 1
    1 : np.array([*CSI data sequence*]),
    2 : np.array([*CSI data sequence*]),
    ...
    63 : np.array([*CSI data sequence*])
}
```

### **analysis.py**

After load in the data set, you can use utilities in ```analysis.py``` to check the data. (note: It only provides minimum support. If there is an error, the quickest way to fix it is to write you own analysis system using ```matplotlib.pyplot```)

|utility|description|
|----|----|
|**icanfi.analysis_time(data,Lsub = 0,Usub = SUBCARRIER,Sframe = 0,Eframe = None)**|```analysis_time``` can help us to understand how subcarrier behave in time domain. <br>**Lsub**: lower subcarrier, <br>**Usub**: upper subcarrier, <br>**Sframe**: starting frame, <br>**Eframe**: ending frame|
|**icanfi.analysis_sub(data,Lsub = 0,Usub = SUBCARRIER,Sframe = 0,Eframe = None)**|```analysis_sub``` demonstrate the data by subcarrier, by this we can observie the amplitude difference between each subcarrier in each frame.<br>**Lsub**: lower subcarrier, <br>**Usub**: upper subcarrier, <br>**Sframe**: starting frame, <br>**Eframe**: ending frame|


### **preprocess.py**

After load in the data set,  preprocess can help us to transfrom the dataset into desire form. you can use ```icanfi.downsampling``` to get uniform data distribution, ```icanfi.remove_DC``` to eliminate DC component... the uilities is explain below.

|utility|description|
|----|----|
|**icanfi.into_energy(data)**|Transform data into energy of the signal in channel, please do this opperation in your **LAST** step of preprocessing, otherwise you might have trobule in doing further work.<br> **return dict(np.array())**  *#check source code or test.py to get better undestanding*|
|**icanfi.delta_R(data_energy)**|compute the difference between frame, take input from into_energy.<br>**return dict(np.array)**|
|**icanfi.windowing(data,windowsize = WINDOWSIZE,hop = HOP,drop = DROP)**|Do windowing operation.<br>**windowsize**: how many second can be contain in a window defult is 20 second<br>**hop**: the starting second from the last previous one defult is 3 second.<br>**drop**: if the gap between frame is larger them drop the window is discard<br>**return list(dict(np.array()))**|
|**icanfi.downsampling(data,Srate = DOWNSAMPLING_S,bias = BIAS,extand = False)**|downsapling will modify the original data,i.e. no need to assign another parameter<br>**Srate**: sample rate<br>**bias**: tolerance for data bias, the data have to be in range of second +/- bais.<br>**extend**: acceptance of extending the data if there is a miss<br><br>**interact with windowing can help you filter out those window that has large miss*|

### **filters.py**

utilities in filters.py are design for data that process by ```into_energy```,so be ware of the format.

|utility|description|
|----|----|
|**icanfi.lowpass(data)**|to change low pass filter's cut of frequency, please change it in ```parameter.py```|
|**icanfi.bandpass(data)**|to change band pass filter's cut of frequency, please change it in ```parameter.py```|
|**icanfi.data_fft(data)**|do fourier transform and return result|
|**icanfi.wavelet**|do wavelet transform return the result|


### **algorithm.py**

contain some PCA utility, which is unrelated to this project ,but still helpful for building a new PCA utility.

### **parameter.py**

all parameter can be set up here.
```python
#our CSI model can only detect 20HZ max because the serial speed
#butterworth filter


BUTTER_N = 7
BUTTER_WN = 0.5 #cut off frequency
BUTTER_OUTPUT = 'sos'
BUTTER_ANALOG = False
BANDPASS_WN = [0.05,1]
#downsampling rate
DOWNSAMPLING_S = 0.04
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
```

## **connection system**
--------------------
To have better control over whole data collecting system, I use lan to connect the CSI capturing device. the system is being saparated into two programs, ```connection``` and ```ras_connection``` 

### **connection**
connection can be use in Windows os, ```control.py``` is all you need for you to connect to raspberry pi. two other can help you test ESP32 if there is something unexpected.

### **ras_connection**
ras_connection is designed for rapberry pi,```rasp.py``` can help you get the ESP32 data.
### system overview

            [Control Center]                  [Data Collector]
                    |                                 |
                    |---------check connection------>>|
                    |                                 |
                    |<<--------send connected---------|
                    |                                 |
              [check reply]                           |
                    |                                 |
                    |----------send filename-------->>|
                    |                                 |
                    |                     [start collecting process]
                    |                                 |
                    |-----------send stop----------->>|
                    |                                 |

Each file is saved in raspberry pi. you have to do some preset to make rapberry to collect multiple ESP32 data input. please see the source code before you using.