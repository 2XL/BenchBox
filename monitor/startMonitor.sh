#!/usr/bin/env bash


echo 'kill socketListener.sh'
echo 'vagrant' | sudo kill -9 $(pidof python)
echo 'start socketListener';  
if [ -d ~/monitor ]; then  
cd ~/monitor/logger/py_cpu_monitor
echo 'vagrant' | sudo -S python SocketListener.py;
echo 'stacksync client and monitor started';  
else  
echo 'stacksync client monitoring not available';  
fi
