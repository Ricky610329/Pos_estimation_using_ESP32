import serial
import numpy as np
import time


COM_PORT = '/dev/ttyUSB0'
BAUD_RATES = 115200 


def read(ser):
    line = 0
    flag = False
    for i in range(10):
        try:
            line = ser.read(15).decode('utf-8')
            flag = True
        except UnicodeDecodeError:
            flag = False
            print("retry...")
        if flag:
            break
    if flag:
        return line
    else:
        print('error')

def stack_full(ser):
    for i in range(1000):
        dataraw = read(ser)
        print(2)
        start = dataraw.find('[')
        if start != -1:
            s = dataraw[start:]
            for j in range(1000):
                print(3)
                dataraw = read(ser)
                end = dataraw.find(']')
                if end == -1:
                    s = s+dataraw
                else:
                    s = s+dataraw[:end+1]
                    break
            return s
        



ser = serial.Serial(COM_PORT, BAUD_RATES)
start = time.time()
for i in range(1000):
    print(1)
    s = stack_full(ser)
    print(time.time()-start,s)
ser.close()