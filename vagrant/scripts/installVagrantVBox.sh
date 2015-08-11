#!/usr/bin/env bash



echo "Inicializar instalación de vagrant and virtualbox"


if which virtualbox; then
    echo 'vbox/OK';
 else
    echo 'no';
	#sudo apt-get purge virtualbox;
	if [ ! -f virtualbox-4.2_4.2.2-81494~Debian~wheezy_i386.deb ]
	 then
      wget http://download.virtualbox.org/virtualbox/4.2.2/virtualbox-4.2_4.2.2-81494~Debian~wheezy_i386.deb;
     fi
    sudo dpkg -i virtualbox-4.2_4.2.2-81494~Debian~wheezy_i386.deb;
fi


if which vagrant; then
    echo 'vagrant/OK';
 else
    echo 'no';
	#sudo apt-get purge virtualbox;
	if [ ! -f vagrant_1.7.3_i686.deb ]
	 then
      wget https://dl.bintray.com/mitchellh/vagrant/vagrant_1.7.3_i686.deb;
     fi
    sudo dpkg -i vagrant_1.7.3_i686.deb;
fi
