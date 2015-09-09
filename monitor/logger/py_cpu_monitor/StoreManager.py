
from Monitor import Monitor
from threading import Thread
import socket
import sys
import asyncore
import time
import SocketServer, subprocess



HOST = '192.168.56.101'
PORT = 11000


def worker():
    print 'This is a thread job'



# http://code.activestate.com/recipes/408859-socketrecv-three-ways-to-turn-it-into-recvall/, THIS IS TO BE DONE TOMMOROW

class StoreManager():

    def __init__(self, hostname, port, login, passwd):
        print 'Instance log storage manager'
        self.hostname = hostname
        self.port = port
        self.login = login
        self.passwd = passwd


    def connector(self):






if __name__ == '__main__':

    sm = StoreManager('http://ast12.recerca.intranet.urv.es', '8888', 'lab144', 'lab144')








