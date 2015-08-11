# Aquest modul s'encarrega de preparar els hosts, cada host
	- es un projecte vagrant
		- invocaran les maquines virtuals seguents: [Vagrantfile]
			* sandBox
					-> es on s'allotja els clients dels personal cloud
					-> també tindra installats uns dimonis que registren la cpu, ram, etc
			* benchBox
					-> es on hihaura el generador de tasques per els clients
					-> aquest envia peticions ftp al sandBox

		- en els moduls de manifests project: [Puppetfile]
			- benchbox
			* benchbox
				-> git
				-> python
					-> numpy, *
					-> simpy, 2.3
			- sandbox
			* owncloud
				-> vsftpd
				->
			* stacksync
				-> java
					-> jdk
				-> maven

