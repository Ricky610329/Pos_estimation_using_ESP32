import serial
import time
from socket import socket,gethostbyname, AF_INET, SOCK_DGRAM

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
        return ' '

def stack_full(ser):
    for i in range(1000):
        dataraw = read(ser)
        start = dataraw.find('C')
        if start != -1:
            s = dataraw[start:]
            j = 0
            flag = False
            while j < 1000:
                j+=1
                dataraw = read(ser)
                e = dataraw.find('C')
                if e != -1:
                    flag = True
                    break
                end = dataraw.find(']')
                if end == -1:
                    s = s+dataraw
                else:
                    s = s+dataraw[:end+1]
                    break
            if j == 1000 or flag:
                return 0
            else:
                return s


class Serial_monitor_event:
    def __init__(self):
        self.Stop = False
    def Serial_save(self,raspname,index,sendIP,com = COM_PORT,baud = BAUD_RATES):
        ser = serial.Serial(com, baud)
        start = time.time()
        while True:
            if not self.Stop:
                s = stack_full(ser)
                if s:
                    s = {'time':time.time()-start,'CSI':s}
                    s = raspname +" "+index+" "+str(s["time"])+" "+s['CSI']
                    print(s)
                    for j in range(4):
                        sendIP.send(s.encode('utf-8'))
            else:
                print("KeyboardInterrupt")
                break
        ser.close()

