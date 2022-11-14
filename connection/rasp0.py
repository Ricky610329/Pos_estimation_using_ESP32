'''
OSX/Linux: ifconfig
Windows: ipconfig /all
'''


import sys
from socket import socket,gethostbyname, AF_INET, SOCK_DGRAM
import time



CONTROL_IP   = '127.0.0.1'
PORT_NUMBER = 5000
LISTEN_PORT = 5001
SIZE = 1024
hostName = gethostbyname( '0.0.0.0' )
print ("Test client sending packets to IP {0}, via port {1}\n".format(CONTROL_IP, PORT_NUMBER))
LSocket = socket( AF_INET, SOCK_DGRAM )
LSocket.bind( (hostName, PORT_NUMBER) )
LSocket.setblocking(False)

mySocket = socket( AF_INET, SOCK_DGRAM )
mySocket.connect((CONTROL_IP,PORT_NUMBER))
while True:
    (data,addr) = LSocket.recvfrom(SIZE)
sys.exit()