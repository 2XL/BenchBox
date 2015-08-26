
__author__ = 'Anna'

import psutil # python system and process utilities

import os, sys




print "This line will be printed."

def main(argv=None):
    print "Main Function..."

    print "Current process ID: {}".format(os.getpid())

    f = os.open('/tmp/cpu_monitor.pid', os.O_RDWR|os.O_CREAT)
    os.write(f, str(os.getpid()))
    os.close(f)

    #################################### CPU
    print "#### CPU ####"
    print "\npsutil.cpu_times()"
    print psutil.cpu_times()
    print psutil.cpu_times()

    wait_time=1 # seconds
    loops=1
    print "\npsutil.cpu_percent(interval={time})".format(time=wait_time)
    for x in range(loops):
        print psutil.cpu_percent(interval=wait_time)

    print "\npsutil.cpu_percent(interval={time}, percpu=True)".format(time=wait_time)
    for x in range(loops):
        print psutil.cpu_percent(interval=wait_time, percpu=True)

    print "\npsutil.cpu_times_percent(interval={time}, percpu=True)".format(time=wait_time)
    for x in range(loops):
        print psutil.cpu_times_percent(interval=wait_time, percpu=False)

    print "\npsutil.cpu_count() & psutil.cpu_count(logical=False)"
    print psutil.cpu_count()
    print psutil.cpu_count(logical=False)
    print "#### CPU/END ####"
    #################################### MEMORY
    print "#### MEMORY ####"
    print "\npsutil.virtual_memory()"
    print psutil.virtual_memory()
    print "\npsutil.swap_memory()"
    print psutil.swap_memory()
    print "#### MEMORY/END ####"
    #################################### DISK
    print "#### DISK ####"
    print "\npsutil.disk_partitions()"
    print psutil.disk_partitions()
    print "\npsutil.disk_usage('/'))"
    print psutil.disk_usage('/')
    print "\npsutil.disk_io_counters(perdisk=False) & True"
    print psutil.disk_io_counters(perdisk=False)
    print psutil.disk_io_counters(perdisk=True)
    print "#### DISK/END ####"
    #################################### NETWORK
    print "#### NETWORK ####"
    print "\npsutil.net_io_counters(pernic=True)"
    print psutil.net_io_counters(pernic=True)
    print "\npsutil.net_connections()"
    print psutil.net_connections()
    #print "\npsutil.net_if_addrs()"
    #print psutil.net_if_addrs() # available but still not released
    #print "\npsutil.net_if_stats()"
    #print psutil.net_if_stats()
    print "#### NETWORK/END ####"
    #################################### MISC
    print "#### MISC ####"
    print "\npsutil.users()"
    print psutil.users()
    print "\npsutil.boot_time()"
    print psutil.boot_time()
    print "#### MISC/END ####"
    #################################### PROCESS MANAGEMENT
    print "#### PROCESS MANAGEMENT ####"
    print "\npsutil.pids()"
    print psutil.pids()

    # lookup for process called stacksync
    proc_watchdog = 0
    for x in psutil.pids():
        print x
        p = psutil.Process(x)
        if p.name() == 'python':
            print "OK -> {}".format(x)
            proc_watchdog = x
        #print p.name()
        '''
        p.exe()
        p.cwd()
        p.status()
        p.cmdline()
        p.status()
        p.username()
        p.create_time()
        p.terminal()
        p.uids()
        p.gids()
        p.cpu_times()
        p.cpu_percent(interval=1) # seconds
        p.cpu_affinity()
        p.memory_percent()
        p.memory_info()
        p.memory_info_ex()
        p.memory_maps()
        p.io_counters()
        p.open_files()
        p.connections()
        p.num_threads()
        p.num_fds()
        p.num_ctx_switches()
        p.nice() # this value gives a process more or less cpu [-20(highest priority -> 19(lowest)]
        # p.nice(10) # set the nice of a certain process p to 10
        # p.ionice() # set input output nice
        # p.rlimit() # resource limit

        # p.suspend()
        # p.resume()
        # p.terminate()
        # p.wait()

    '''
    print "\npsutil.test()"
    print psutil.test()
    print "#### PROCESS MANAGEMENT/END ####"
    ######################################### POST PROCESSS
    print "#### POST PROCESS ####"
    print "\npsutil.process_iter()"
    for p in psutil.process_iter():
        print(p)

    def on_proc_terminate(proc):
        print ("Do _{}_ post process procedure ".format(proc))

    # waits for multiple process to terminate
    wait_timeout = 3 # seconds
    gone, alive = psutil.wait_procs(psutil.process_iter(), wait_timeout, callback=on_proc_terminate)
    print "\n gone"
    print gone
    print "\n alive"
    print alive

    print "do it for a single process"

    p = psutil.Process(proc_watchdog)
    try:
        p.wait(timeout=wait_timeout)
    except psutil.TimeoutExpired:
        p.kill()
        try:
            p.wait(timeout=wait_time)
        except psutil.TimeoutExpired:
            sys.exit('giving up xD')



    print "#### POST PROCESS/END ####"






if __name__ == '__main__':
    print "Probar de obtener cpu & ram de mi portatil"
    main()