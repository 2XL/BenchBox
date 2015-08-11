#!/usr/bin/env bash


echo "Inicializar instalación de dependencias en los Hosts"



if [ -f PuppetEssential/debian-7.0-amd64.box ]; then
	echo 'box/OK';
else
	echo 'no..., check if other path';

	if [ -f debian-7.0-amd64.box ]; then
		echo 'box/OK';
		cp debian-7.0-amd64.box PuppetEssential/
	else
		cd PuppetEssential;
		wget https://www.dropbox.com/s/si19tbftilcuipz/debian-7.0-amd64.box;
		cp debian-7.0-amd64.box ../
		cd;
	fi
fi


# check if the machine has installed python dependecy libraries



# instalar owncloud i stacksync client
# https://github.com/stacksync/desktop/releases/download/v2.0-alpha2/stacksync_2.0_all.deb





#if [ -f "Debian-7.3.0-i386b.box" ]; then
#	echo 'box/OK';
#else
#echo 'no';
# wget https://dl.dropboxusercontent.com/s/60pv9an852jx9y0/Debian-7.3.0-i386b.box?dl=1;
# mv Debian-7.3.0-i386b.box?dl=1 Debian-7.3.0-i386b.box;
#fi

  # ls;   pwd;
  #sudo apt-get purge vagrant;
  #wget https://dl.bintray.com/mitchellh/vagrant/vagrant_1.7.3_i686.deb;
  #sudo dpkg -i vagrant_1.7.3_i686.deb;

  #wget http://download.virtualbox.org/virtualbox/5.0.0/virtualbox-5.0_5.0.0-101573~Debian~wheezy_i386.deb
  #sudo dpkg -i virtualbox-5.0_5.0.0-101573~Debian~wheezy_i386.deb

  #sudo apt-get purge virtualbox;
  #wget http://download.virtualbox.org/virtualbox/4.2.2/virtualbox-4.2_4.2.2-81494~Debian~wheezy_i386.deb;
  #sudo dpkg -i virtualbox-4.2_4.2.2-81494~Debian~wheezy_i386.deb;


  # todo -> inicializar els imatges del lab amb lo que hiha dalt instalats.





echo "Instalation fin"


echo "now Vagrant ready to Start! --> vagrant up"