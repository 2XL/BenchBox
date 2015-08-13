#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
__author__ = 'anna'

from ConfigParser import SafeConfigParser

from argparse import ArgumentParser
import shlex
from subprocess import Popen, PIPE
import traceback, time, sys, os
import random, numpy

#  sys.path.append('general') # hard-code :D


def process_opt():
    parser = ArgumentParser()

    parser.add_argument("-o", dest="option", default=None, help="Option: start|status|stop|restart|clear"
                                                                "example: ./init.py -o start")

    parser.add_argument("--out", dest="output", default='output', help="Folder for output files")

    parser.add_argument("--hosts", dest="hosts", default="config.hosts.ini", help="File containing all the hosts "
                                                                                  "available and their login "
                                                                                  "credentials")

    parser.add_argument("--config", dest="config", default="config.all.ini", help="File containing the localtion of "
                                                                                  "the sync servers, log server, "
                                                                                  "simulator "
                                                                                  "profiling distribution")

    parser.add_argument("--seed", dest="seed", default=int(time.time()), type=int, help="Random seed "
                                                                                        "(default unix_time)")

    parser.add_argument("--keygen", dest='keygen', default=None, help="Generate syncserver credentials for each hosts")

    parser.add_argument("--keepalive", dest='keepalive', default=None, help="Prevent hosts from self-destroy")

    parser.add_argument("--shutdown", dest='shutdown', default=None, help="Shutdown hosts")



    opt = parser.parse_args()

    if not opt.option:
        parser.print_help()
        sys.exit(1)

    opt = parser.parse_args()

    return opt


def loadConfiguration(path):
    print 'load configuration files settings'
    configAll = SafeConfigParser()
    configAll.read(path)
    profile = dict(configAll.items('profile'))
    owncloud = dict(configAll.items('owncloud'))
    stacksync = dict(configAll.items('stacksync'))
    log_server = dict(configAll.items('log_server'))
    return {'profile': profile,
            'ss': {'owncloud': owncloud, 'stacksync': stacksync},
            'ls': log_server}

def loadHosts(path):
    print 'load hosts candidates config file'
    configHosts = SafeConfigParser()
    configHosts.read(path)

    listOfHosts = configHosts.sections()
    hosts = {}
    for h in listOfHosts:
        hosts[h] = dict(configHosts.items(h))
    return hosts


def greet(who):
    print "Hello %s" % who


# --------------------------------------------------------------------------------
# Commands
# --------------------------------------------------------------------------------

def start():
    # customized lambda functions :D
    greed_command = lambda: greet('owncloud')
    greed_command()
    greed_command = lambda: greet('stacksync')
    greed_command()


def stop():
    print 'stop'


def restart():
    print 'restart'


def status():
    print 'status'


def clean():
    print 'clean'


# -------------------------------------------------------------------------------
# Main
# -------------------------------------------------------------------------------
# available commands
COMMANDS = {'start': start, 'stop': stop, 'status': status, 'restart': restart, 'clean': clean }

if __name__ == '__main__':

    opt = process_opt()

    # Root permissions are needed, and some checks to save existing files
    if not os.geteuid()!=0:
        exit("Only none-root can run this script")
    elif not (os.path.exists(opt.output) and os.path.isdir(opt.output)):
        exit("ERROR: This is not a folder: " + opt.output)
    elif len(os.listdir(opt.output)):
        exit("ERROR: This folder is not empty: " + opt.output)

    print opt

    config = loadConfiguration(opt.config)
    hosts = loadHosts(opt.hosts)

    print config
    print hosts

    # Popen(['command to run', 'some arguments'], stdout=PIPE, stderr=PIPE)
    args = ['/bin/echo',  "Hello World"]
    p = Popen(args)
    print 'Popen running...'
    p.communicate()
    print 'Popen wait finish.'

    COMMANDS[opt.option]()  # command pattern
