import serial
import csv
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
        return ' '

def stack_full(ser):
    for i in range(1000):
        dataraw = read(ser)
        start = dataraw.find('[')
        if start != -1:
            s = dataraw[start:]
            j = 0
            flag = False
            while j < 1000:
                j+=1
                dataraw = read(ser)
                e = dataraw.find('[')
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
    def Serial_save(self,f_name,index,com = COM_PORT,baud = BAUD_RATES):
        ser = serial.Serial(com, baud)
        start = time.time()

        with open(f_name, 'w', newline='') as csvfile:
            fieldnames = ['time','CSI']
            #writer = csv.writer(csvfile)
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            while True:
                if not self.Stop:
                    s = stack_full(ser)
                    if s:
                        s = {'time':time.time()-start,'CSI':s}
                        print(index,s["time"],len(s['CSI'].split(" ")))
                        writer.writerow(s)
                else:
                    print("KeyboardInterrupt")
                    break
        ser.close()

