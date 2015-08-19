#!/usr/bin/env bash




if [ "$#" -ne 0 ]; then
    echo "Illegal number of parameters"
    echo "use default root directory"
	DIR=$1
else
	echo '../'
	DIR='..'
fi


if [ ! -f "$DIR/ss.stacksync.ip" ];
then
echo "File: not found!"
sync_server_ip='192.168.1.240' # stacksync server_ip,
exit;
else
echo "File: $2 exists!"
fi
line=($(<"$DIR/ss.stacksync.ip"))
sync_server_ip=`echo $line | awk -F ' ' '{ print $2}' | awk -F ':' '{print $1}'`


if [ ! -f "$DIR/ss.stacksync.key" ];
then
echo "File: not found!"
exit;
else
echo "File: $1 exists!"
fi

line=($(<"$DIR/ss.stacksync.key"))


mystring="466d654e-31a7-47ba-9085-65f08d8ae863,demo17,AUTH_5e446d39e4294b57831da7ce3dd0d2c2,stacksync_e373c1fd_demo17,demo17@ast.cat"
mystring=$line


IFS=',' read -a myarray <<< "$mystring"

ID=${myarray[0]}
USER=${myarray[1]}

SWIFT_AUTH=${myarray[2]}
SWIFT_USER=${myarray[3]}

EMAIL=${myarray[4]}




swift_group='stacksync'
swift_user=$SWIFT_USER
username='vagrant'
id=$ID
email=$EMAIL
password=$USER
FILE='config.xml'

cat > $FILE <<- EOM

<stacksync>
    <!--
    <username>$username</username>
    <queuename>$hostname</queuename>
    <autostart>true</autostart>
    <notifications>true</notifications>
    -->
    <!--
    <apiLogUrl>http://localhost/stack/apiput</apiLogUrl>
    <apiLogUrl>URL_LOG_SERVER_API</apiLogUrl>
    -->
    <remoteLogs>false</remoteLogs>

    <rabbitMQ>
        <host>$sync_server_ip</host>

        <port>5672</port>
        <enableSSL>false</enableSSL>

        <username>guest</username>
        <password>guest</password>
        <rpc_exchange>rpc_global_exchange</rpc_exchange>
    </rabbitMQ>

    <cache>
        <size>1024</size>
        <folder>/home/$username/.stacksync/cache</folder>
    </cache>

<device>
        <name>Jo</name>
    </device>
    <profile>
        <enabled>true</enabled>
        <name>(unknown)</name>
        <repository>
            <chunksize>512</chunksize>
            <connection type="swift_comercial">
                <username>$swift_group:$swift_user</username>
                <apikey>$password</apikey>
                <authurl>http://$sync_server_ip:5000/v2.0/tokens</authurl>
            </connection>
        </repository>
        <folder>
            <active>true</active>
            <local>/home/$username/stacksync_folder</local>
        </folder>
        <account>
            <id>$id</id>
            <email>$email</email>
            <password>$password</password>
        </account>
    </profile>
</stacksync>

EOM


if [[ -s $FILE ]] ; then
echo "$FILE has data."
else
echo "$FILE is empty."
fi ;
ls -l $FILE
echo 'New credentials generated successfully!!'
cat $FILE
mv $FILE ../$FILE


