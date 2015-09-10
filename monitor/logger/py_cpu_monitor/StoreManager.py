

from impala.dbapi import connect


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
        try:
            self.conn = connect(
                host=self.hostname,
                port=self.port)
                # ldap_user=self.login,
                # ldap_password = self.passwd)
            self.curr = self.conn.cursor()
        except Exception as e:
            print "Could not connect!!!, {}".format(e)

    def execute(self, query):
        if self.curr is not None:
            self.curr.execute(query)
        else:
            print 'No connection'
            '''
            try:
                return self.curr.description, self.curr.fetchall()
            except Exception as e:
                print 'No results xD {}'.format(e)
            '''

    def quit(self):
        if self.conn is None:
            self.conn.close()
            print 'Client connection closed Successfully!'
            if self.curr is None:
                self.curr.close()
                print 'Client cursor closed Successfully!'
        else:
            print 'No Connection to close!'






if __name__ == '__main__':

    sm = StoreManager('ast12.recerca.intranet.urv.es',
                      21050,
                      'lab144',
                      'lab144')
    sm.connect()
    # asume that there is a benchbox database in impala
    sm.execute('use benchbox')
    # create table if not exists



    create_logger = "create table if not exists logger ( time TIMESTAMP ,type string, key string, value bigint  ) stored as parquet"

    fetch_logger = "select * from logger limit 10"

    print sm.execute(create_logger)
    print sm.execute(fetch_logger)
    print sm.curr.fetchall()


'''

create table logger (
time TIMESTAMP ,
type string,
key string, # process name, disk path, nic...
value bigint,
) stored as parquet;



'''

# references:
'''
http://cloudera.github.io/cm_api/docs/python-client/

http://gethue.com/tutorial-executing-hive-or-impala-queries-with-python/

$HUE_HOME: whereis hue :: /etc/hue && /usr/lib/hue

https://github.com/cloudera/impyla/tree/master/examples/logr

http://blog.cloudera.com/blog/2014/04/a-new-python-client-for-impala/

'''



