

from impala.dbapi import connect


HOST = '192.168.56.101'
PORT = 11000


def worker():
    print 'This is a thread job'


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
            self.curr = self.conn.cursor()
        except Exception as e:
            print "Could not connect!!!, {}".format(e)
            self.conn = None
            self.curr = None

    def execute(self, query):
        if self.curr is not None:
            self.curr.execute(query)
        else:
            print 'No connection'

    def quit(self):
        if self.conn is not None:
            if self.curr is not None:
                self.curr.close()
                print 'Client cursor closed Successfully!'
            self.conn.close()
            print 'Client connection closed Successfully!'
        else:
            print 'No Connection to close!'

if __name__ == '__main__':

    IMPALA_DOMAIN = 'ast12.recerca.intranet.urv.es'
    sm = StoreManager(IMPALA_DOMAIN,
                      21050,
                      'lab144',
                      'lab144')
    sm.connect()
    sm.execute('use benchbox')

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




