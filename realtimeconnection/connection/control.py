'''
OSX/Linux: ifconfig
Windows: ipconfig /all
'''

from graptocsi import realtime_Data
from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
import sys
import time
import threading




PORT_NUMBER = 5000
RASP_port = 5001
Ras_num = 1 #the number of raspberry has to be specify
SIZE = 1024
hostName = gethostbyname( '0.0.0.0' )
#the order of the ip address is the order of the raspberry pi connection
RASP_IP = [
    '192.168.0.109',
    '192.168.0.112',
    '127.0.0.1',
    '127.0.0.1'
]
flag = [False,False,False,False]
SOCKETsned = []
for i in range(Ras_num):
    SOCKETsned.append(socket( AF_INET, SOCK_DGRAM ))

for i in range(Ras_num):
    SOCKETsned[i].connect((RASP_IP[i],RASP_port))


grab_event = realtime_Data()


LSocket = socket( AF_INET, SOCK_DGRAM )
LSocket.bind( (hostName, PORT_NUMBER) )
LSocket.setblocking(False)

data = 0
addr = [' ',' ']
check = False
while True:
    for i in range(Ras_num):
        check = True
        if not flag[i]:
            check = False
            SOCKETsned[i].send(b'hi')
            break
    try:
        (data,addr) = LSocket.recvfrom(SIZE)
    except BlockingIOError:
        pass
    #print(addr)
    for i in range(Ras_num):
        if addr[0] == RASP_IP[i]:
            flag[i] = True
    time.sleep(0.01)
    if check:
        break

if check:
    print('ready...')

    print("\nInput file name, the system will save files on raspberry pi as csv file")

    filename = input("Input File name:\n>>")
    grab_event.setfilename(filename)

    for i in range(100):
        for j in range(Ras_num):
            link = "link"+(str(j+1))
            SOCKETsned[j].send((link).encode('utf-8'))
    
    print("enter 'stop' to end data collection process")
    sig = ' '
    grab_thread = threading.Thread(target = grab_event.grab_event, args =(LSocket,))
    grab_thread.start()
    
    while sig != 'stop':
        sig = input(">>>")
    grab_event.terminate()
    for i in range(100):
        for j in range(Ras_num):
            SOCKETsned[j].send(b'stop')


sys.exit()