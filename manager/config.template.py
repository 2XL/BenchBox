#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import ConfigParser

class Object(object):
    pass

# General Configuration Setup ##########################################################################################

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
configAll.add_section('log_server')

configAll.set('demo', 'url', 'https://wiki.python.org/moin/ConfigParserExamples')

configAll.set('profile', 'sync', '1')
configAll.set('profile', 'backup', '1')
configAll.set('profile', 'cdn', '1')
configAll.set('profile', 'regular', '1')
configAll.set('profile', 'idle', '1')

# configAll.set('owncloud', 'ip', '192.168.1.240')
configAll.set('owncloud', 'ip', '10.30.236.140')
configAll.set('owncloud', 'port', '80')
configAll.set('owncloud', 'user', 'user')
configAll.set('owncloud', 'passwd', 'bitnami')

configAll.set('stacksync', 'ip', '10.30.239.198')
configAll.set('stacksync', 'port', '80')
configAll.set('stacksync', 'admin', '10.30.239.198:8081/admin')
configAll.set('stacksync', 'user', 'swift')
configAll.set('stacksync', 'passwd', 'urv')

configAll.set('log_server', 'url', 'ds055822.mongolab.com:55822/benchbox')
configAll.set('log_server', 'user', 'test')
configAll.set('log_server', 'passwd', 'test')


# Writing our configuration file to 'example.cfg'
with open('config.all.ini', 'wb') as configfileAll:
    configAll.write(configfileAll)

# Hosts Specific Configuration Setup ###################################################################################

configHosts = ConfigParser.RawConfigParser()
'''
# CUSTOM SLAVE-HOSTS
'''
'''
ast13 = {'user': 'milax', 'passwd': 'milax', 'ip': '10.21.2.5',
         'owncloud_login': 'milax:milax',
         'stacksync_login': 'milax:milax'}
localhost = {'user': 'anna', 'passwd': 'joanna', 'ip': '10.30.236.141',
             'owncloud_login': 'anna:anna',
             'stacksync_login': 'anna:anna'}
'''
ast10 = {'user': 'user', 'passwd': 'lab144', 'ip': '10.30.102.186',
             'owncloud_login': 'anna:anna',
             'stacksync_login': 'anna:anna'}

ast03 = {'user': 'milax', 'passwd': 'milax', 'ip': '10.30.103.95',
         'owncloud_login': 'anna:anna',
         'stacksync_login': 'anna:anna'}

li = {'ast03': ast03, }


for hostname in li:
    configHosts.add_section(hostname)
    print li[hostname]
    for key in li[hostname].keys():
        configHosts.set(hostname, key, li[hostname][key])


'''
# python domain of hosts
offset_hostname = 200 # DEIM lab ip ranges 100:200:300
offset_ip = 5
hosts = 24 # num of hosts
hosts_available = 0 # probar... # total: 12
for i in range(hosts_available):
    hostname = 'd'+str(i+offset_hostname+offset_ip)+'.lab.deim'
    configHosts.add_section(hostname)
    configHosts.set(hostname,'user', 'milax')
    configHosts.set(hostname,'passwd', 'milax')
    configHosts.set(hostname,'ip', '10.21.2.'+str(offset_ip+i))

'''

# Writing our configuration file to 'example.cfg'
with open('config.hosts.ini', 'wb') as configfileHosts:
    configHosts.write(configfileHosts)

