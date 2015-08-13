#!/usr/bin/env bash

#
# Add Vagrant Box
#

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


echo "Instalation fin"


echo "now Vagrant ready to Start! --> vagrant up"