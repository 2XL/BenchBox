# BenchBox/monitor [http://dillinger.io/]

Definition: this module contains 3 main features:
	1. runs a socket server at each sandBox Machine, this server calls psutil utilities to gather the cpu, ram... sats
	2. contains a node app that manitorize in real time the sandBox personal cloud client process
	3. TODO: redirect the monitor output to an datastore backend, such as Impala

# Pre Requisites:
### Testing:

Pre: have nodejs installed at the dummyHost, there is a install node-install.sh script if its not installed
```sh
./node-install.sh
```

### Use:

```sh
npm start
```






### Version
0.0.1

### Tech

BenchBox/monitor uses a number of open source projects to work properly:

* [node.js] - evented I/O for the backend
* [Express] - fast node.js network app framework [@tjholowaychuk]
* [AngularJS] - HTML enhanced for web apps!
* [Jade]
* [Impala]
* [jQuery] - duh
* [Python]




### Plugins

BenchBox/monitor is currently storing monitor output to the following datastore

 * TODO, Impala


### Development

Want to contribute? Great!

BenchBox uses GitHub!!!



 ### Todos
 - redirect SocketLister results on simulator stop
 	* impala
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
