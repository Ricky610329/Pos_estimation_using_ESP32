'''
OSX/Linux: ifconfig
Windows: ipconfig /all
'''

from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
import sys
import time

PORT_NUMBER = 5000
RASP_port = 5001
Ras_num = 1
SIZE = 1024

hostName = gethostbyname( '0.0.0.0' )
RASP_IP = [
    '192.168.0.108',
    '127.0.0.1',
    '127.0.0.1',
    '127.0.0.1'
]
flag = [False,False,False,False]
SOCKETsned = []
for i in range(Ras_num):
    SOCKETsned.append(socket( AF_INET, SOCK_DGRAM ))

for i in range(Ras_num):
    SOCKETsned[i].connect((RASP_IP[i],RASP_port))


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
    except:
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
    for i in range(100):
        for j in range(Ras_num):
            SOCKETsned[j].send(filename.encode('utf-8'))
    
    print("enter 'stop' to end data collection process")
    sig = ' '
    while sig != 'stop':
        sig = input(">>>")
    for i in range(100):
        for j in range(Ras_num):
            SOCKETsned[j].send(b'stop')


sys.exit()