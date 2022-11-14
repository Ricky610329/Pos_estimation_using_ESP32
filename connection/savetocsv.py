import serial
import csv
import time


COM_PORT = 'COM5'
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
            while j < 1000:
                j+=1
                dataraw = read(ser)
                e = dataraw.find('[')
                if e != -1:
                    break
                end = dataraw.find(']')
                if end == -1:
                    s = s+dataraw
                else:
                    s = s+dataraw[:end+1]
                    break
            if j == 1000:
                return 0
            else:
                return s
        

ser = serial.Serial(COM_PORT, BAUD_RATES)
start = time.time()
f_name = input("InputFileName:")
f_name = f_name + '.csv'

with open(f_name, 'w', newline='') as csvfile:
    fieldnames = ['time','CSI']
    #writer = csv.writer(csvfile)
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    while True:
        try:
            s = stack_full(ser)
            s = {'time':time.time()-start,'CSI':s}
            print(s["time"],len(s['CSI'].split(" ")))
            writer.writerow(s)
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            break
ser.close()