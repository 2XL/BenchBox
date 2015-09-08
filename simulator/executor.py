#!/usr/bin/python
'''
Created on 30/6/2015

@author: Raul
'''
from ConfigParser import SafeConfigParser
import os
import subprocess
import random
import time

from markov_chain import SimpleMarkovChain
from inter_arrivals_manager import InterArrivalsManager
from data_generator import DataGenerator

from pcb.general.ftp_sender import ftp_sender
from pcb.general.logger import logger
from pcb.actions import get_action, MakeResponse, PutContentResponse, Unlink, MoveResponse, GetContentResponse

from cpu_monitor import CPUMonitor

class StereotypeExecutor(object):

    def __init__(self):
        self.markov_chain = SimpleMarkovChain()
        self.markov_current_state = 'MakeResponse' # there should be an initial state @ can be random
        self.inter_arrivals_manager = InterArrivalsManager()
        self.data_generator = DataGenerator()
        # self.data_generator.initialize_file_system()
        # self.sender


    def initialize_from_stereotype_recipe(self, stereotype_recipe):
        '''Initialize the Markov Chain states'''
        self.markov_chain.initialize_from_recipe(stereotype_recipe)
        self.markov_chain.calculate_chain_relative_probabilities()
        '''Initialize the inter-arrival times'''
        self.inter_arrivals_manager.initialize_from_recipe(stereotype_recipe)
        '''Initialize the file system'''
        self.data_generator.initialize_file_system()

    def get_waiting_time(self):
        return self.inter_arrivals_manager.get_waiting_time(self.markov_chain.previous_state,
                                                            self.markov_chain.current_state)

    def next_operation(self):
        '''Get the next operation to be done'''
        self.markov_chain.next_step_in_random_navigation()


    '''Do an execution step as a client'''
    def execute(self):
        raise NotImplemented

class StereotypeExecutorU1(StereotypeExecutor):

    def __init__(self, ftp_client, ftp_files):
        StereotypeExecutor.__init__(self)
        self.ftp_client = ftp_client
        self.ftp_files = ftp_files

    '''Do an execution step as a client'''
    def execute(self):
        '''Get the next operation to be done'''
        self.markov_chain.next_step_in_random_navigation()
        self.randomWait(1,5)
        to_execute = getattr(self, 'do' + self.markov_chain.current_state)
        # to_execute = getattr(self, 'doGetContentResponse')
        to_execute()

    '''Operations that should connect to the Cristian's Benchmarking Framework'''
    def doMakeResponse(self):
        print "do create"
        '''Get the time to wait for this transition in millis'''
        #to_wait = self.inter_arrivals_manager.get_waiting_time(self.markov_current_state, 'MakeResponse')
        self.markov_current_state = 'MakeResponse'
        synthetic_file_name = self.data_generator.create_file()
        action = get_action(["MakeResponse", 'sampleMake.txt', 10], ftp_files)
        action.perform_action(ftp_client)

    def doPutContentResponse(self):
        print "do update"
        '''Get the time to wait for this transition in millis'''
        #to_wait = self.inter_arrivals_manager.get_waiting_time(self.markov_current_state, 'PutContentResponse')
        self.markov_current_state = 'PutContentResponse'
        action = get_action(["PutContentResponse", 'sampleMake.txt', [0, 57, 1100, 1206, -1, 227]], ftp_files)
        action.perform_action(ftp_client)

    def doSync(self ):
        self.doPutContentResponse()

    def doUnlink(self ):
        print "do delete"
        '''Get the time to wait for this transition in millis'''
        #to_wait = self.inter_arrivals_manager.get_waiting_time(self.markov_current_state, 'Unlink')
        self.markov_current_state = 'Unlink'
        action = get_action(["Unlink", 'sampleMake.txt'], ftp_files)
        action.perform_action(ftp_client)

    def doMoveResponse(self):
        print "do move"
        '''Get the time to wait for this transition in millis'''
        #to_wait = self.inter_arrivals_manager.get_waiting_time(self.markov_current_state, 'MoveResponse')
        self.markov_current_state = 'MoveResponse'
        action = get_action(["MoveResponse", 'files', 'ReSampleMake.txt'], ftp_files)
        action.perform_action(ftp_client)

    def doGetContentResponse(self):
        print "do download"
        '''Get the time to wait for this transition in millis'''
        #to_wait = self.inter_arrivals_manager.get_waiting_time(self.markov_current_state, 'GetContentResponse')
        self.markov_current_state = 'GetContentResponse'
        action = get_action(["GetContentResponse", 'sampleMake.txt', 'files/get/'], ftp_files)
        action.perform_action(ftp_client)

    def randomWait(self, min, max):
        print 'wait, between [{} - {}] seconds'.format(min, max)
        wait = random.randint(min, max)
        print '{}s'.format(wait)
        while wait > 0:
            time.sleep(1)
            wait = wait-1
            print '{}s'.format(wait)

if __name__ == '__main__':

    # Root permissions are needed, and some checks to save existing files
    # if not os.geteuid() == 0:
    #     print "Only root can run this script"  # exit()
    # else:
    #     print 'Config/OK'

    parser = SafeConfigParser()
    parser.read('config.ini')
    print parser.get('executor', 'interface')   # eth0
    print parser.get('executor', 'ftp')         # 192.168.56.2
    print parser.get('executor', 'port')        # 21
    print parser.get('executor', 'user')        # cotes -> vagrant
    print parser.get('executor', 'passwd')      # lab144 -> vagrant

    print 'Logger/OK'
    # log experiment metadata

    # print parser.options('executor')
    log = logger(parser.get('executor', 'output') + os.sep + "metadata.log", dict(parser._sections['executor']) )
    ftp_client = ftp_sender(parser.get('executor','ftp'),
                        parser.get('executor','port'),
                        parser.get('executor','user'),
                        parser.get('executor','passwd'),
                        parser.get('executor','folder')) # root path ftp_client directory :: ~/stacksync_folder
    ftp_files = parser.get('executor','files_folder') # relative path to local files :: ./files/demoFiles.txt
    print 'Markov/OK'
    stereotype_executor = StereotypeExecutorU1(ftp_client, ftp_files)
    stereotype_executor.markov_chain.initialize_from_recipe("./data/xl_markov_sync_all_ms.csv")
    stereotype_executor.markov_chain.calculate_chain_relative_probabilities()

    print 'IPTables/OK'
    # os.system('sudo ./pcb/scripts/firewall start')
    # os.system('sudo iptables -L')

    print 'FTP/OK'
    worker = None
    print "Start executing/****************************"
    # start monitoring
    #sandBoxSocketIpPort = '192.168.56.101',11000
    monitor = CPUMonitor('192.168.56.101',11000)
    interval = 1
    log_filename = 'local.csv'
    proc_name = 'StackSync' # if its stacksync
    monitor.start_monitor(interval, log_filename, proc_name)
    operations = 100
    operations = 30
    for i in range(operations):
        # stereotype_executor.execute(sender, parser.get('executor','files_folder'))
        stereotype_executor.execute()
    # stop monitoring
    monitor.stop_monitor()
    print "Finish executing/****************************"

    print "ClearingProcess/..."

    if ftp_client:
        print "close sender"
        ftp_client.close()
    #os.system('sudo ./pcb/scripts/firewall stop')

    print "ClearingProcess/OK"
