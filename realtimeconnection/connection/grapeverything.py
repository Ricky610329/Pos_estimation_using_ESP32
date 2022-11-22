"""
This class is where to design the algorithm

"""


import csv
from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM

SIZE = 1024

class realtime_Data:
    def __init__(self):
        self.stop = False
        self.data = []
    def grab_event(self,listenIP):
        last = ' '
        while True:
            try:
                (data,addr) = listenIP.recvfrom(SIZE)
                packet = data.decode('utf-8')
                if packet != last:
                    self.data.append(packet)
                    print(packet)
                last = packet
            except BlockingIOError:
                pass
            if self.stop:
                break
    def terminate(self):
        self.stop = True