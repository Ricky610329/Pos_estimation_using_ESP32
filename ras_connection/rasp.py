'''
OSX/Linux: ifconfig
Windows: ipconfig /all
'''

from savetocsv import Serial_monitor_event as mevent
import sys
from socket import socket,gethostbyname, AF_INET, SOCK_DGRAM
import time
import threading





CONTROL_IP   = '192.168.0.115'
PORT_NUMBER = 5000
LISTEN_PORT = 5001
SIZE = 1024
ESPNUM = 1

serial_thread = []
monitor = []
for i in range(ESPNUM):
    monitor.append(mevent())

hostName = gethostbyname( '0.0.0.0' )
#print ("Test client sending packets to IP {0}, via port {1}\n".format(CONTROL_IP, PORT_NUMBER))
LSocket = socket( AF_INET, SOCK_DGRAM )
LSocket.bind( (hostName, LISTEN_PORT) )
#LSocket.setblocking(False)

mySocket = socket( AF_INET, SOCK_DGRAM )
mySocket.connect((CONTROL_IP,PORT_NUMBER))
while True:
    (data,addr) = LSocket.recvfrom(SIZE)
    if data == b'hi':
        break
for i in range(100):
    mySocket.send(b'hello')
data = ' '
while True:
    (data,addr) = LSocket.recvfrom(SIZE)
    print(data)
    if data != b'hi':
        break

filename = data.decode('utf-8')+'_1'+'.csv'
for i in range(ESPNUM):
    serial_thread.append(threading.Thread(target = monitor[i].Serial_save,args=(filename,)))
    serial_thread[i].start()

while True:
    (data,addr) = LSocket.recvfrom(SIZE)
    print(data)
    if data == b'stop':
        for i in range(ESPNUM):
            monitor[i].Stop = True
        break

sys.exit()

