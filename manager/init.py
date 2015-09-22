#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
__author__ = 'anna'

from ConfigParser import SafeConfigParser

from argparse import ArgumentParser
import shlex
import psycopg2
import threading
from subprocess import Popen, PIPE
import traceback, time, sys, os
import random, numpy
from multiprocessing import Pool
import csv
import pxssh
import getpass

# sys.path.append('general') # hard-code by cristian :D
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

    parser.add_argument("-x", dest="xxx", default=None, help="Apply changes only at host x")

    opt = parser.parse_args()

    if not opt.option:

        parser.print_help()
        print 'Example: ./init.py -o start'
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
    graphite = dict(configAll.items('graphite'))
    return {'profile': profile,
            'ss': {'owncloud': owncloud, 'stacksync': stacksync},
            'ls': log_server,
            'graphite': graphite}

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
            options={"StrictHostKeyChecking": "no", "UserKnownHostsFile": "/dev/null", "timeout": "3600"}
            s = pxssh.pxssh()
            s.login(hostname, login, passwd)
            s.timeout = 3600 # set timeout to one hour
            s.sendline(cmd) # run a command
            s.prompt() # match the prompt
            #print s.before # print everyting before the prompt
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


def start(h, hostname, idx, cb):
    print 'start, hostname:{} :&&: idx:{} '.format(hostname, idx)
    preconfig(h, hostname)  # tell all the hosts to download BenchBox
    setup(h, hostname)    # tell all the hosts to install VirtualBox and Vagrant
    summon(h, hostname)   # tell the hosts to download Vagrant box to use
    config(h, hostname, idx, CONFIG)  # tell each hosts their profile
    if idx < 0: # onlye has to be done once
        keygen_stacksync(h, hostname, CONFIG) # only have to be run once
    credentials(h, hostname, idx)      # cal conectar desde la mateixa maquina virtual xk no dona accés a hosts externs
    sserver(h, hostname, idx, CONFIG)   # tell each host where the sync servers are located
    # split run test... how to tell each dummy to run a test???, have to open a socket a the simulator... or create a
    #  proxy at the dummy host
    #  test proxy
    run(h, hostname, idx) # make vagrant up
    print 'start/OK: {}:{}'.format(hostname, idx)
    cb(hostname)


def stop():
    print 'stop'
    pause(HOSTS)


def restart():
    print 'restart'
    stop()
    start()
    print 'restart/OK'


def status():
    print 'status: Retrieve for each hosts if they are Ready|Running|Stopped'


def monitor():
    print 'monitor: start dummy node server'
    start_node_server(HOSTS)
# Advance functions

def preconfig(h, hostname):
    #print 'preconfig: download BenchBox repo at the Slave hosts: {}'.format(hostname)

    str_cmd = "" \
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
    # print str_cmd
    print h
    rpc(h['ip'], h['user'], h['passwd'], str_cmd) # utilitzar un worker del pool

    '''
    versió pool
    '''
    print 'preconfig/OK: {}'.format(hostname)


def setup(h, hostname):
    #print 'setup: Setup vagrant and VirtualBox at the Slave hosts: {}'.format(hostname)

    str_cmd = "" \
              "if [ -d BenchBox ]; then " \
              "cd BenchBox;" \
              "git pull; " \
              "cd vagrant/scripts; " \
              "echo '%s' | sudo -S ./installVagrantVBox.sh; " \
              "fi;" \
              "" % h['passwd']
    # print str_cmd
    rpc(h['ip'], h['user'], h['passwd'], str_cmd)
    print 'setup/OK: {}'.format(hostname)


def summon(h, hostname):
    # print 'summon: Download vagrant box dependencies at the Slave hosts'

    str_cmd = "" \
              "if [ -d BenchBox ]; then " \
              "cd BenchBox;" \
              "git pull; " \
              "cd vagrant/scripts; " \
              "./installDependencies.sh; " \
              "fi;" \
              ""
    #print str_cmd
    rpc(h['ip'], h['user'], h['passwd'], str_cmd)
    print 'summon/OK: {}'.format(hostname)


def config(h, hostname, idx, cfg):
    # print 'config: Assign a Stereotype to each host'

    profiles = cfg['profile']
    p = []
    counter = 1
    for prof in profiles:
        for i in range(counter, counter+int(profiles[prof])):
            #print prof, idx
            p.append(prof)
        counter+=int(profiles[prof])


    str_cmd = "" \
              "if [ -d BenchBox ]; then " \
              "cd BenchBox;" \
              "git pull; " \
              "cd vagrant; " \
              "echo '%s' > profile; "  \
              "fi; " % p[idx]

    #print str_cmd
    rpc(h['ip'], h['user'], h['passwd'], str_cmd)

    print 'config/OK: {} :: {}'.format(hostname, p[idx])




def keygen_stacksync(h, hostname, conf):
    stacksync_ip = conf['ss']['stacksync']['ip']

    # print 'keygen: retrieve stacksync login credentials'
    conn = psycopg2.connect(database="stacksync_db",
                            user="stacksync_user",
                            password="stacksync_pass",
                            host=stacksync_ip,
                            port="5432")
    cur = conn.cursor()
    query = "select id, name, swift_account, swift_user, email from user1 where name  ~ 'demo' order by email asc";
    outputquery = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(query)
    with open('stacksync_credentials.csv', 'w') as f:
        cur.copy_expert(outputquery, f)
    conn.close()
    print 'keygen/OK {}'.format(hostname)
    # el allin one tiene este puerto bloqueado por ello no puedo acceder a esos datos.



def credentials(h, hostname, idx):
    # print 'credentials'

    #keygen_stacksync()  # stacksync

    # keygen() # owncloud
    # push the generated keys to each slave host
    cred = []
    with open("stacksync_credentials.csv", "rb") as infile:
        reader = csv.reader(infile)
        next(reader, None)  # skip the headers
        for row in reader:
            # process each row
            cred.append(row)

    key = ','.join(cred[idx])
    ownkey = cred[idx][1]
    str_cmd = "" \
              "if [ -d BenchBox ]; then " \
              "cd BenchBox; " \
              "git pull; " \
              "cd vagrant; " \
              "echo '%s' > ss.stacksync.key; " \
              "echo '%s' > ss.owncloud.key; " \
              "echo '%s' > hostname; " \
              "echo 'Run: clients configuration scripts: '; " \
              "cd scripts; " \
              "./config.owncloud.sh; " \
              "./config.stacksync.sh; " \
              "echo 'clients configuration files generated'; " \
              "fi; " % (key, ownkey, hostname)
    # print str_cmd
    rpc(h['ip'], h['user'], h['passwd'], str_cmd)
    print 'credentials/OK: {}:[{}] => {} / {}'.format(hostname, idx, ownkey, key)



def sserver(h, hostname, idx,  conf):
    # print 'sserver'
    # print config
    owncloud_ip = conf['ss']['owncloud']
    stacksync_ip = conf['ss']['stacksync']

    str_cmd = "" \
              "if [ -d BenchBox ]; then " \
              "cd BenchBox/vagrant; " \
              "echo '%s' > ss.stacksync.ip; " \
              "echo '%s' > ss.owncloud.ip; " \
              "fi; " % (stacksync_ip, owncloud_ip)

    # print str_cmd
    rpc(h['ip'], h['user'], h['passwd'], str_cmd)
    print 'sserver/OK {} : {}'.format(hostname, idx)

def credentials_owncloud(hosts):
    print 'pushOwnCloudCredentials'


def credentials_stacksync(hosts):
    print 'pushStackSyncCredentials'




def run(h, hostname, idx):
    print 'run: Call Vagrant init at each host: {}'.format(hostname)
    str_cmd = "" \
              "if [ -d BenchBox ]; then " \
              "cd BenchBox;" \
              "git pull; " \
              "cd vagrant; " \
              "echo '-------------------------------'; " \
              "ls -l *.box; " \
              "vagrant -v; " \
              "VBoxManage --version; " \
              "echo '-------------------------------'; " \
              "VBoxManage list runningvms | wc -l > running; " \
              "vagrant up sandBox; " \
              "vagrant provision sandBox; " \
              "vagrant up benchBox; " \
              "vagrant provision benchBox; " \
              "else " \
              "echo 'Vagrant Project not Found!??'; " \
              "fi;" \
              ""
    # print str_cmd
    rpc(h['ip'], h['user'], h['passwd'], str_cmd)
    print 'run/OK {}/{}'.format(hostname, idx)


def keepalive(hosts):
    print 'keepalive: Prevent the hosts from auto-shutdown'
    for host in hosts:
        h = hosts[host]
        str_cmd = "" \
                  "if [ -f /usr/lib/milax-labdeim/autoapaguin.sh ]; then " \
                  "echo '%s' | sudo -S rm /usr/lib/milax-labdeim/autoapaguin.sh; " \
                  "else" \
                  "echo 'File not found!'; " \
                  "fi; " % h['passwd']
        # print str_cmd
        rpc(h['ip'], h['user'], h['passwd'], str_cmd)
    print 'keepalive/OK'


def scan(subnet = '192.168.1.0-255', port = 22, output = 'hosts'):
    print 'scan: Scan hosts at a specific subnet'
    cmd_args = "nmap %s -p %s | grep 'Nmap scan' | awk '{print $5}' > %s" % (subnet, port, output)
    print cmd_args
    p = Popen('/bin/bash', stdin=PIPE, stdout=PIPE)
    out, err = p.communicate(cmd_args)
    print out
    if err:
        print err
    print 'scan/OK...'


def clean(hosts):
    print 'clean: Remove the repository files'
    for host in hosts:
        h = hosts[host]
        str_cmd = "" \
                  "if [ -d BenchBox ]; then" \
                  "rm -rf BenchBox; " \
                  "else " \
                  "echo 'Repo already clean'; " \
                  "fi; "
        print str_cmd
        rpc(h['ip'], h['user'], h['passwd'], str_cmd)
    print 'clean/OK'


def destroy(hosts):
    print 'destroy: Remove the repository files'
    for host in hosts:
        h = hosts[host]
        str_cmd = "" \
                  "if [ -d BenchBox ]; then" \
                  "cd BenchBox; " \
                  "vagrant destroy -f; " \
                  "else " \
                  "echo 'Repo already clean'; " \
                  "fi; "
        print str_cmd
        rpc(h['ip'], h['user'], h['passwd'], str_cmd)
    print 'destroy/OK'


def pause(hosts):
    print 'pause: Pause the running vagrant machines'
    for host in hosts:
        h = hosts[host]
        str_cmd = "" \
                  "if [ -d BenchBox ]; then" \
                  "cd BenchBox; " \
                  "vagrant halt; " \
                  "else " \
                  "echo 'Repo does not exist!'; " \
                  "fi; "
        print str_cmd
        rpc(h['ip'], h['user'], h['passwd'], str_cmd)
    print 'destroy/OK'


def shutdown(hosts):
    print 'shutdown: Power off the remote Hosts'
    for host in hosts:
        h = hosts[host]
        str_cmd = "" \
                  "echo 'Shutdown!!!';" \
                  "echo '%s' | sudo -S shutdown -h 0 " \
                  "" % h['passwd']
        print str_cmd
        rpc(h['ip'], h['user'], h['passwd'], str_cmd)
    print 'shutdown/OK'

def start_node_server(h):
    print 'run the nodejs monitor server at each Dummy Host'

    str_cmd = "cd BenchBox/monitor; " \
              "nohup /usr/local/bin/npm start & "
    rpc(h['ip'], h['user'], h['passwd'], str_cmd)
    print 'nodeserver running at {}:{}'.format(h['ip'], '5000')
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
    'init': init,
    'scan': scan,
    'monitor': monitor
}


def cb_func(hostname):
    "The callback function."
    print 'Callback, in thread {} => {}'.format(threading.current_thread().name, hostname)

def th_func(callback):
    "The threaded function."
    # ...
    callback()

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
    for idx, host in enumerate(HOSTS):
        # COMMANDS['init']()
        print '...'
        # COMMANDS[opt.option](HOSTS[host], host)  # command pattern
        if opt.xxx == None:
            thr = threading.Thread(target=COMMANDS[opt.option], args=(HOSTS[host], host, idx, cb_func,)).start()
        elif int(opt.xxx) != idx:
            print 'Do nothing, {} != {}'.format(opt.xxx, idx)
        else:
            thr = threading.Thread(target=COMMANDS[opt.option], args=(HOSTS[host], host, idx, cb_func,)).start()

    ''' paralelize this part '''



