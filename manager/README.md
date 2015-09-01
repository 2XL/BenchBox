
TODO,

0th download
https://github.com/2XL/PuppetEssential.git


1st make ssh push to list of clients
https://github.com/2XL/PuppetEssential

###


Pre Requisites:

- setup: config.template.py & run it inorder to generate the config.all.ini and config.hosts.ini file

Use cases:


python init.py [args...]
	start
	stop
	status
	restart







## -> this has to be refactored to python...
# thread invocation unviable and unhandleble



-- Aquest modul s'encarrega de gestionar el rang de hosts a manipular
	-- els hosts poden provindre de diferents fonts
		-- aws
		-- deim
		-- altres

	-- fitxer de configuració
		-- ip's hosts
		-- ip log server (mongodb)
		-- ip owncloud server
		-- ip stacksync server

	-- operacions
		-- setup
		-- configure
		-- start
		-- finish
