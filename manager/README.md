
###


Pre Requisites:

# setup:
pre:
define the syncservers, and the dummy hosts at [config.template.py]
run
>python config.template.py
this step generates the configuration files defined at the [config.template.py]

# use:
python init.py [args...]
    'start': start,     # setup each dummy hosts with appropriate tools to run the simulator
    'stop': stop,       # pause all the dummy virtual machines
    'status': status,   # TODO
    'restart': restart, # pause & start
    'clean': clean,     # TODO, clear repo at each dummy host and also remove vms
    'init': init,       # greeting :D
    'scan': scan,       # scan subnet with nmap lookup for dummy hosts with port 22 open
    'monitor': monitor  # tell each dummy hosts to realtime render its loggs at dummy_ip:5000







# TODO

handle different kind of dummy hosts
		-- aws
		-- deim
		-- others

