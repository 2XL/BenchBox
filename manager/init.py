#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
__author__ = 'anna'

from ConfigParser import SafeConfigParser

from argparse import ArgumentParser
import shlex
from subprocess import Popen, PIPE
import traceback, time, sys, os
import random, numpy
from multiprocessing import Pool
import pxssh
import getpass

# sys.path.append('general') # hard-code :D
# global variables
CONFIG = {}
HOSTS = {}

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

# ------------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------------

def loadConfiguration(path):
    print 'Load configuration files settings'
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
    print 'Load hosts candidates config file'
    configHosts = SafeConfigParser()
    configHosts.read(path)

    listOfHosts = configHosts.sections()
    hosts = {}
    for h in listOfHosts:
        hosts[h] = dict(configHosts.items(h))
    return hosts


def power(x):
    return x*x


def greet(who):
    print "BenchBox: %s" % who


def rpc(hostname, login, passwd, cmd, callback=None):
    while True:
        try:
            options={"StrictHostKeyChecking": "no", "UserKnownHostsFile": "/dev/null"}
            s = pxssh.pxssh()
            s.login(hostname, login, passwd)
            s.sendline(cmd) # run a command
            s.prompt() # match the prompt
            print s.before # print everyting before the prompt
            # s.sendline ('uptime;df -h') # running multiple lines
            s.logout()
        except pxssh.ExceptionPxssh, e:
            print "pxssh failed on login."
            print str(e)
            continue
        break

    if callback:
        return callback()

# --------------------------------------------------------------------------------
# Commands
# --------------------------------------------------------------------------------


def init():
    # customized lambda functions :D
    greed_command = lambda: greet('owncloud')
    greed_command()
    greed_command = lambda: greet('stacksync')
    greed_command()


def start():
    print 'start'
    preconfig(HOSTS)


def stop():
    print 'stop'


def restart():
    print 'restart'


def status():
    print 'status'


def clean():
    print 'clean'


# Advance functions

def preconfig(hosts):
    print 'preconfig: Setup vagrant and Virtualbox at the Slave hosts'
    for host in hosts:
        h = hosts[host]
        str = "" \
              "echo 'check if Git is installed...'; " \
              "echo '%s' | sudo -S apt-get install git; " \
              "echo 'check if BenchBox is installed...'; " \
              "if [ -d BenchBox ]; then " \
              "cd BenchBox;" \
              "git pull; " \
              "else " \
              "git clone --recursive https://github.com/2XL/BenchBox.git; " \
              "fi;" \
              "" % h['passwd']
        print str
        rpc(h['ip'], h['user'], h['passwd'], str)
    print 'preconfig/OK'

def summon():
    print 'summon'


def config():
    print 'config'


def run():
    print 'run'


def keepalive():
    print 'keepalive'


def scan():
    print 'scan'


def destroy():
    print 'destroy'


def shutdown():
    print 'shutdown'


def keygen():
    print 'keygen'


def credentials():
    print 'credentials'


# -------------------------------------------------------------------------------
# Main
# -------------------------------------------------------------------------------
# available commands
COMMANDS = {
    'start': start,
    'stop': stop,
    'status': status,
    'restart': restart,
    'clean': clean,
    'init': init
}

if __name__ == '__main__':

    opt = process_opt()

    # Root permissions are needed, and some checks to save existing files
    if not os.geteuid()!=0:
        exit("Only none-root can run this script")
    elif not (os.path.exists(opt.output) and os.path.isdir(opt.output)):
        exit("ERROR: This is not a folder: " + opt.output)
    elif len(os.listdir(opt.output)):
        exit("ERROR: This folder is not empty: " + opt.output)

    # print opt

    CONFIG = loadConfiguration(opt.config)
    HOSTS = loadHosts(opt.hosts)

    # Popen(['command to run', 'some arguments'], stdout=PIPE, stderr=PIPE)
    hw = ['/bin/echo',  "Popen/OK"]
    p = Popen(hw)
    print 'Popen installed...'
    p.communicate()
    print '...'
    COMMANDS['init']()
    print '...'
    COMMANDS[opt.option]()  # command pattern

