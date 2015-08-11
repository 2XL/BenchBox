#!/usr/bin/python
'''
Created on 30/6/2015

@author: Raul
'''
from ConfigParser import SafeConfigParser
import os
import subprocess

from markov_chain import SimpleMarkovChain
from inter_arrivals_manager import InterArrivalsManager
from data_generator import DataGenerator

from pcb.general.ftp_sender import ftp_sender
from pcb.general.logger import logger
from pcb.actions import get_action, MakeResponse, PutContentResponse, Unlink, MoveResponse, GetContentResponse

class StereotypeExecutor(object):

    def __init__(self):
        self.markov_chain = SimpleMarkovChain()
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

    '''Do an execution step as a client'''
    def execute(self, sender, files_folder):
        '''Get the next operation to be done'''
        self.markov_chain.nextStepInRandomNavigation()
        to_execute = getattr(self, 'do' + self.markov_chain.current_state)
        # to_execute = getattr(self, 'doGetContentResponse')
        to_execute(sender, files_folder)

    '''Operations that should connect to the Cristian's Benchmarking Framework'''
    def doMakeResponse(self, sender, files_folder):
        print "do create"
        '''Get the time to wait for this transition in millis'''
        to_wait = self.inter_arrivals_manager.get_waiting_time()
        synthetic_file_name = self.data_generator.create_file()
        action = get_action(["MakeResponse", 'sampleMake.txt', 10], files_folder)
        action.perform_action(sender)

    def doPutContentResponse(self, sender, files_folder):
        print "do update"
        '''Get the time to wait for this transition in millis'''
        to_wait = self.inter_arrivals_manager.get_waiting_time()
        action = get_action(["PutContentResponse", 'sampleMake.txt', [0, 57, 1100, 1206, -1, 227]], files_folder)
        action.perform_action(sender)

    def doSync(self, sender, files_folder):
        self.doPutContentResponse()

    def doUnlink(self, sender, files_folder):
        print "do delete"
        '''Get the time to wait for this transition in millis'''
        to_wait = self.inter_arrivals_manager.get_waiting_time()
        action = get_action(["Unlink", 'sampleMake.txt'], files_folder)
        action.perform_action(sender)

    def doMoveResponse(self, sender, files_folder):
        print "do move"
        '''Get the time to wait for this transition in millis'''
        to_wait = self.inter_arrivals_manager.get_waiting_time()
        action = get_action(["MoveResponse", 'files', 'ReSampleMake.txt'], files_folder)
        action.perform_action(sender)

    def doGetContentResponse(self, sender, files_folder):
        print "do download"
        '''Get the time to wait for this transition in millis'''
        to_wait = self.inter_arrivals_manager.get_waiting_time()
        action = get_action(["GetContentResponse", 'sampleMake.txt', 'files/get/'], files_folder)
        action.perform_action(sender)

if __name__ == '__main__':

    # Root permissions are needed, and some checks to save existing files
    if not os.geteuid() == 0:
        print "Only root can run this script"  # exit()
    else:
        print 'Config/OK'

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

    print 'Markov/OK'
    stereotype_executor = StereotypeExecutorU1()
    stereotype_executor.markov_chain.initializeFromFile("./data/xl_markov_sync_all_ms.csv")
    stereotype_executor.markov_chain.calculateChainRelativeProbabilities()

    print 'IPTables/OK'
    # os.system('sudo ./pcb/scripts/firewall start')
    # os.system('sudo iptables -L')

    print 'FTP/OK'
    worker = None
    sender = ftp_sender(parser.get('executor','ftp'),
                        parser.get('executor','port'),
                        parser.get('executor','user'),
                        parser.get('executor','passwd'),
                        parser.get('executor','folder'))
    print "Start eexecuting/****************************"
    for i in range(100):
        # stereotype_executor.execute(sender, parser.get('executor','files_folder'))
        stereotype_executor.execute(sender, parser.get('executor','files_folder'))
    print "Finish executing/****************************"

    print "ClearingProcess/..."

    if sender:
        print "close sender"
        sender.close()
    os.system('sudo ./pcb/scripts/firewall stop')

    print "ClearingProcess/OK"
