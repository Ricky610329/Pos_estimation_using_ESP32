import serial
import cv2
import numpy as np
import icanfi
import time


COM_PORT = 'COM5'
BAUD_RATES = 115200 


def read(ser):
    try:
        line = ser.read(15).decode('utf-8')
    except UnicodeDecodeError:
        line = ser.read(15).decode('utf-8')

    return line

def stack_full(ser):
    for i in range(10000):
        dataraw = read(ser)
        start = dataraw.find('[')
        if start != -1:
            s = dataraw[start:]
            for j in range(10000):
                dataraw = read(ser)
                end = dataraw.find(']')
                if end == -1:
                    s = s+dataraw
                else:
                    s = s+dataraw[:end+1]
                    break
            return s
        else:
            return 0




ser = serial.Serial(COM_PORT, BAUD_RATES)
guide_base = np.zeros((2000,2000,3), dtype=np.uint8)
start = time.time()
for i in range(1000):

    s = stack_full(ser)
    if s:
        print(time.time()-start,len(icanfi.load_r(s)))
    if cv2.waitKey(1) == ord('q'):
        break
ser.close()