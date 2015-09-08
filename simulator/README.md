 # BenchBox/simulator [http://dillinger.io/]

 definition: this module contains the simulator that will be executed at each BenchBox virtual machine to generate
 workload for each sandBox pc-client.

 ## Pre Requisites:
 ### Testing:
 Pre: generate the interarrivals csv for simulation, demo-files are located at data/*.csv:
 .all.ini

 ### Use:

 ```sh
 python executor.py
 ```


 ### Version
 0.0.1

 ### Tech

 BenchBox/manager uses a number of open source projects to work properly:

 * [Python]
 * [scypi]
 * [numpy]
 * [SD-gen] : sintetic file system generation


 ### Plugins

 BenchBox/simulator is currently extended with the following plugins (personal cloud)


 Readme,showing how to use them in your own application can be found here:

 * [monitor/README.md](https://github.com/2XL/BenchBox/tree/master/monitor/README.md)
 * [simulator/README.md](https://github.com/2XL/BenchBox/tree/master/simulator/README.md)
 * [vagrant/README.md](https://github.com/2XL/BenchBox/tree/master/vagrant/README.md)
 * [manager/README.md](https://github.com/2XL/BenchBox/tree/master/manager/README.md)

 ### Development

 Want to contribute? Great!

 BenchBox uses GitHub!!!


 ### Todos
 - generating sintetic filesystem
 	* sdgen
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



