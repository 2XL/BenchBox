#!/usr/bin/env bash


echo 'start socketListener';  
if [ -d ~/monitor ]; then  
cd ~/monitor/logger/py_cpu_monitor && python SocketListener.py;  
echo 'stacksync client and monitor started';  
else  
echo 'stacksync client monitoring not available';  
fi
