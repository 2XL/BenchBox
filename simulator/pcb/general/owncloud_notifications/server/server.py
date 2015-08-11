'''
Created on 3 Jul 2014

@author: cotes
'''

import pika
from threading import Thread
from time import sleep
from subprocess import Popen, PIPE

class Server():
    
    def __init__(self, channel):
        self.channel = channel
        self.clients = {}
        
    def listen_general_queue(self):
        self.channel.queue_declare(queue='general_users')
        self.channel.basic_consume(self.newClient, queue='general_users', no_ack=True)

        self.channel.start_consuming()
        
    def new_client(self, ch, method, properties, body):
        print " [x] Received %r" % (body,)
        if body not in self.clients:
            self.clients[body] = 1
            self.channel.queue_declare(queue=body)
            
    def send_notification(self, client):
        self.channel.basic_publish(exchange='',
                          routing_key=client,
                          body='done')
        
    def watch_folder(self, base_path):
        while True:
            for client in self.clients.keys():
                pipe1 = Popen(["find", base_path + "/" + client + "/files", "-print"], stdout=PIPE)
                pipe2 = Popen(["wc", "-l"], stdin=pipe1.stdout, stdout=PIPE)
                pipe1.stdout.close()
                num_files = pipe2.communicate()[0]
                pipe2.stdout.close()
                
                if self.clients[client] != num_files:
                    self.send_notification(client)
                    self.clients[client] = num_files
                    
            sleep(2)
        

if __name__ == '__main__':

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='ast3-deim.urv.cat'))
    channel = connection.channel()
    
    server = Server(channel)
    thread = Thread(target=server.listen_general_queue)
    thread.daemon = True
    thread.start()
    
    server.watch_folder("/var/www/owncloud6/data")
