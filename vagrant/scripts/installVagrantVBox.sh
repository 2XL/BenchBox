#!/usr/bin/env bash

#
# Install Vagrant & VirtualBox
#

echo "Inicializar instalación de Vagrant and Virtualbox"

MACHINE_TYPE=`uname -m`
if which virtualbox; then
    echo 'vbox/OK';
 else
    echo 'vbox/no';

    if [ ${MACHINE_TYPE} == 'x86_64' ]; then

        echo '64'
        if [ ! -f virtualbox-4.2_4.2.2-81494~Debian~wheezy_amd64.deb ]
		 then
		 # 		 wget http://download.virtualbox.org/virtualbox/4.1.40/virtualbox-4.1_4.1.40-101594~Debian~squeeze_amd64.deb
	      wget http://download.virtualbox.org/virtualbox/4.2.2/virtualbox-4.2_4.2.2-81494~Debian~wheezy_amd64.deb
	     fi
	    sudo dpkg -i virtualbox-4.2_4.2.2-81494~Debian~wheezy_amd64.deb;
    else

        echo '32'
		#sudo apt-get purge virtualbox;
		if [ ! -f virtualbox-4.2_4.2.2-81494~Debian~wheezy_i386.deb ]
		 then
	      wget http://download.virtualbox.org/virtualbox/4.2.2/virtualbox-4.2_4.2.2-81494~Debian~wheezy_i386.deb;
	     fi
	    sudo dpkg -i virtualbox-4.2_4.2.2-81494~Debian~wheezy_i386.deb;
    fi
fi


if which vagrant; then
    echo 'vagrant/OK';
 else
	echo 'vagrant/no';
	#sudo apt-get purge virtualbox;
	if [ ${MACHINE_TYPE} == 'x86_64' ]; then
		# 64-bit stuff here
		if [ ! -f vagrant_1.7.3_x86_64.deb ]
		then
	    wget https://dl.bintray.com/mitchellh/vagrant/vagrant_1.7.3_x86_64.deb;
	    fi
		sudo dpkg -i vagrant_1.7.3_x86_64.deb
	else
		# 32-bit stuff here
		if [ ! -f vagrant_1.7.3_i686.deb ]
		then
	    wget https://dl.bintray.com/mitchellh/vagrant/vagrant_1.7.3_i686.deb;
	    fi
		sudo dpkg -i vagrant_1.7.3_i686.deb;
	fi

fi





# have to install sshpass at each dummyhost

if which sshpass; then
    echo 'sshpass/OK';
 else
	echo 'sshpass/no';
	sudo apt-get install sshpass
fi



