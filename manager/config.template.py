#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import ConfigParser

class Object(object):
    pass

# General Configuration Setup

configAll = ConfigParser.RawConfigParser()

# When adding sections or items, add them in the reverse order of
# how you want them to be displayed in the actual file.
# In addition, please note that using RawConfigParser's and the raw
# mode of ConfigParser's respective set functions, you can assign
# non-string values to keys internally, but will receive an error
# when attempting to write to a file or when you get it in non-raw
# mode. SafeConfigParser does not allow such assignments to take place.

configAll.add_section('demo')
configAll.add_section('profile')
configAll.add_section('owncloud')
configAll.add_section('stacksync')

configAll.set('demo', 'url', 'https://wiki.python.org/moin/ConfigParserExamples')

configAll.set('profile', 'sync', '3')
configAll.set('profile', 'backup', '5')
configAll.set('profile', 'cdn', '9')
configAll.set('profile', 'regular', '1')
configAll.set('profile', 'idle', '1')

configAll.set('owncloud', 'ip', '192.168.1.240')
configAll.set('owncloud', 'port', '80')
configAll.set('owncloud', 'user', 'user')
configAll.set('owncloud', 'passwd', 'bitnami')

configAll.set('stacksync', 'ip', '192.168.1.237')
configAll.set('stacksync', 'port', '80')
configAll.set('stacksync', 'admin', '192.168.1.237:8081/admin')
configAll.set('stacksync', 'user', 'swift')
configAll.set('stacksync', 'passwd', 'urv')

# Writing our configuration file to 'example.cfg'
with open('config.all.ini', 'wb') as configfileAll:
    configAll.write(configfileAll)

# Hosts Specific Configuration Setup

configHosts = ConfigParser.RawConfigParser()
'''
configHosts.add_section('localhost')
configHosts.set('localhost', 'user', 'anna')
configHosts.set('localhost', 'passwd', 'joanna')
configHosts.set('localhost', 'owncloud_credentials', 'user:pass')
configHosts.set('localhost', 'stacksync_credentials', 'user:pass')
'''
# python defined hosts
ast13 = {'user': 'milax', 'passwd': 'milax', 'ip': '192.168.1.227',
         'owncloud_login': 'milax:milax',
         'stacksync_login': 'milax:milax'}
localhost = {'user': 'anna', 'passwd': 'joanna', 'ip': '192.168.1.160',
             'owncloud_login': 'anna:anna',
             'stacksync_login': 'anna:anna'}

li = {'ast13': ast13, }


for hostname in li:
    configHosts.add_section(hostname)
    print li[hostname]
    for key in ast13.keys():
        configHosts.set(hostname, key, li[hostname][key])

'''
# python domain of hosts
offset = 100 # DEIM lab ip ranges 100:200:300
hosts = 24 # num of hosts
for i in range(5):
    hostname = 'd'+str(i+offset)+'.lab.deim'
    configHosts.add_section(hostname)
    configHosts.set(hostname,'user', 'milax')
    configHosts.set(hostname,'passwd', 'milax')
'''

# Writing our configuration file to 'example.cfg'
with open('config.hosts.ini', 'wb') as configfileHosts:
    configHosts.write(configfileHosts)



'''
[localhost]
name = anna
passwd = joanna
owncloud_user = test
owncloud_pass = test
stacksync_user = test
stacksync_pass = test

[d###.lab.deim]
name = d###@lab.deim
passwd = milax
ownlcoud_user = 'demo##'
owncloud_pass = 'demo##'
stacksync_user = 'demo##'
stacksync_pass = 'demo##'
'''