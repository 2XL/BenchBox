# BenchBox/manager [http://dillinger.io/]

definition: this module manages the dummy hosts for the simulation

## Pre Requisites:
### Testing:
Pre: define the syncservers, and the dummy hosts at [config.template.py], run:
```sh
>python config.template.py
```
this step generates the configuration files defined at the [config.template.py]

    * ./config.hosts.ini
    * ./config.all.ini


before running the tests having the pc-syncservers running and testing client account generated for each dummy
client, for each personal cloud:
 * owncloud: with prefix such as demo#:demo#, as logging and password [user and pass has to match]
 * stacksync: generate a list of demo# users with random credentials



### Use:


```sh
python init.py -o start [args...]
```

    - start     # setup each dummy hosts with appropriate tools to run the simulator
    - stop      # pause all the dummy virtual machines
    - status    # TODO
    - restart   # pause & start
    - clean     # TODO, clear repo at each dummy host and also remove vms
    - init      # greeting :D
    - scan      # scan subnet with nmap lookup for dummy hosts with port 22 open
    - monitor   # tell each dummy hosts to realtime render its loggs at dummy_ip:5000
 
### Version
0.0.1

### Tech

BenchBox/manager uses a number of open source projects to work properly:

* [Python]


* [Vagrant]
* [VirtualBox]
* [Hadoop]


 
 
### Plugins

BenchBox/manager is currently extended with the following plugins (personal cloud)

* Owncloud
* StackSync

Readmes, how to use them in your own application can be found here:

* [monitor/README.md](https://github.com/2XL/BenchBox/tree/master/monitor/README.md)
* [simulator/README.md](https://github.com/2XL/BenchBox/tree/master/simulator/README.md)
* [vagrant/README.md](https://github.com/2XL/BenchBox/tree/master/vagrant/README.md)
* [manager/README.md](https://github.com/2XL/BenchBox/tree/master/manager/README.md)

### Development

Want to contribute? Great!

BenchBox uses GitHub!!!


### Todos
- handle different kind of dummy hosts
	* aws
	* deim
	* others
- Write Tests
- Rethink Github Save 
  
 
License
----

MIT


**Free Software, Hell Yeah!**

- [john gruber](http://daringfireball.net)
- [@thomasfuchs](http://twitter.com/thomasfuchs) 
- [marked](https://github.com/chjj/marked)
- [Ace Editor](http://ace.ajax.org)
- [node.js](http://nodejs.org)
- [Twitter Bootstrap](http://twitter.github.com/bootstrap/)
- [keymaster.js](https://github.com/madrobby/keymaster)
- [jQuery](http://jquery.com)
- [@tjholowaychuk](http://twitter.com/tjholowaychuk)
- [express](http://expressjs.com)
- [AngularJS](http://angularjs.org)
- [Gulp](http://gulpjs.com)
