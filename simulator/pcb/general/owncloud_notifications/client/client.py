'''
Created on 3 Jul 2014

@author: cotes
'''

import pika
import time
import threading

'''
connection = pika.BlockingConnection(pika.ConnectionParameters(host='ast3-deim.urv.cat'))
channel = connection.channel()

channel.queue_declare(queue='general_users')

channel.basic_publish(exchange='',
                      routing_key='general_users',
                      body='lab144')

def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)

'''

class Notifier(threading.Thread):
    
    def __init__(self, channel, username, callback_class):
        threading.Thread.__init__(self)
        self.channel = channel
        self.username = username
        self.callback_class = callback_class
        
    def run(self):
        self.channel.basic_consume(self.callback_class.callback, queue=self.username, no_ack=True)
        self.channel.start_consuming()


class Watcher():
    
    def __init__(self, username):
        # Create queue
        self.uploaded = False
        self.connection = None
        self.channel = None
        self.create_queue(username)
        
    def create_queue(self, username):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='ast3-deim.urv.cat'))
        self.channel = self.connection.channel()
        
        self.channel.queue_declare(queue='general_users')
        
        self.channel.basic_publish(exchange='',
                              routing_key='general_users',
                              body=username)
        
        self.notifier = Notifier(self.channel, username, self)
        self.notifier.start()
        
        
    def callback(self, ch, method, properties, body):
        print 'callback'
        self.uploaded = True
    
    def is_file_uploaded(self):
        while not self.uploaded:
            time.sleep(1)
        
        return
    
    def reset(self):
        self.uploaded = False
    
watcher = Watcher('lab144')
watcher.reset()
print 'waiting...'
watcher.is_file_uploaded()
print 'done...'