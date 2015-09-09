
from Monitor import Monitor
from threading import Thread
import socket
import sys
import asyncore
import time
import SocketServer, subprocess
from impala.dbapi import connect
import dbms



HOST = '192.168.56.101'
PORT = 11000


def worker():
    print 'This is a thread job'



# http://code.activestate.com/recipes/408859-socketrecv-three-ways-to-turn-it-into-recvall/, THIS IS TO BE DONE TOMMOROW

class StoreManager():

    conn = None
    curr = None
    def __init__(self, hostname, port, login, passwd):
        print 'Instance log storage manager'
        self.hostname = hostname
        self.port = port
        self.login = login
        self.passwd = passwd



    def connect(self):
        # Get a handle to the API client
        self.conn = connect(
            host=self.hostname,
            port=self.port,
            ldap_user=self.login,
            ldap_password = self.passwd)
        self.curr = self.conn.cursor()

    def execute(self, query):
        if self.curr is not None:
            self.curr.execute(query)
            '''
            try:
                return self.curr.description, self.curr.fetchall()
            except Exception as e:
                print 'No results xD {}'.format(e)
            '''








if __name__ == '__main__':

    sm = StoreManager('ast12.recerca.intranet.urv.es',
                      21050,
                      'lab144',
                      'lab144')
    sm.connect()
    sm.execute('use default')
    print sm.execute('select * from download limit 10')
    print sm.curr.fetchall()



# references:
'''
http://cloudera.github.io/cm_api/docs/python-client/

http://gethue.com/tutorial-executing-hive-or-impala-queries-with-python/

$HUE_HOME: whereis hue :: /etc/hue && /usr/lib/hue

https://github.com/cloudera/impyla/tree/master/examples/logr

'''



