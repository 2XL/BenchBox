# py_cpu_monitor is based on:
[https://github.com/Cotes/CPUMonitor] 

definition:  this python module gathers the cpu, ram, network and disk resource usage

### Refactor Status:

[SandBox code]
* Diagnostics.py : psutil command interface
* Monitor.py : resource manager
* MonitorResource.py  : resource interface
    * CPUMonitor.py
    * DiskMonitor.py
    * MemoryMonitor.py
    * NetworkMonitor.py
* SocketListener.py : socket server

[BenchBox code]
* cpu_monitor.py --> socket client

[Misc code]
* resolveDNS.py
