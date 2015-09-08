# BenchBox/vagrant [http://dillinger.io/]

definition: this module contains the vagrant project that each dummyhost will need to invoice the sandBox and
benchBox vms for the simulations

## Pre Requisites:
### Testing:
Pre: each of the dummy hosts must ssh installed and running, if the machine doesn't have vagrant and virtualbox the
manager will install it.

Fix the puppet/manifests/default-stacksync.pp with the correct stacksync server ip and also at the puppet
modules/stacksync with the correct module
Fix the puppet/manifests/default-owncloud.pp with the correct owncloud server ip

AUTOFIX TODO!!!

* the virtual mahcines cannot be used locally as the pc-credentials has to be provided by the manager., but once its
provided you access each of the vms within the vagrant project with

* vagrant ssh sandBox
* vagrant ssh benchBox

### Version
0.0.1

### Tech

BenchBox/vagrant uses a number of open source projects to work properly:

* [Vagrant]
* [Puppet]
* [Librarian-puppet]
* [yierra] : TODO, AUTO, server ip assignment within configuration file
* [VirtualBox]

### Plugins

BenchBox/vagrant is currently extended with the following plugins (personal cloud)

* owncloud -> using the defualt-owncloud.pp manifest
* stacksync -> using the default-stacksync.pp manifest


Readme,showing how to use them in your own application can be found here:

* [monitor/README.md](https://github.com/2XL/BenchBox/tree/master/monitor/README.md)
* [simulator/README.md](https://github.com/2XL/BenchBox/tree/master/simulator/README.md)
* [vagrant/README.md](https://github.com/2XL/BenchBox/tree/master/vagrant/README.md)
* [manager/README.md](https://github.com/2XL/BenchBox/tree/master/manager/README.md)

### Development

Want to contribute? Great!

BenchBox uses GitHub!!!


### Todos
- SyncServer IP assignment with config file instead of modifying at different places with the editor replace command
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





