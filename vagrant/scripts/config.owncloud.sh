#!/usr/bin/env bash


[ -f owncloudsync.sh ] && rm owncloudsync.sh
[ -f ../owncloudsync.sh ] && rm ../owncloudsync.sh

if [ "$#" -ne 0 ]; then
    echo "Illegal number of parameters"
    echo "use default root directory"
	DIR=$1
else
	echo '../'
	DIR='..'
fi



if [ ! -f "$DIR/ss.owncloud.ip" ];
then
echo "File: not found!"
sync_server_ip='192.168.1.240' # owncloud server_ip,
exit;
else
echo "File: $2 exists!"
fi

#line=($(<"$DIR/ss.owncloud.ip"))
sync_server_ip=`more "$DIR/ss.owncloud.ip" | awk -F ' ' '{ print $4}' | awk -F ',' '{print $1}'`

if [ ! -f "$DIR/ss.owncloud.key" ];
then
echo "File: not found!"
exit;
else
echo "File: $1 exists!"
fi

line=($(<"$DIR/owncloud.key"))


mystring="demo0"
mystring=$line


IFS=',' read -a myarray <<< "$mystring"

user=${myarray[0]}
pass=${myarray[0]}



FILE='owncloudsync.sh'

cat > $FILE <<- EOM

#!/usr/bin/env bash
while true; do
    owncloudcmd --httpproxy http://$sync_server_ip -u $user -p $pass /home/vagrant/owncloud_folder/ http://$sync_server_ip
     sleep 30
    # ls -l
done

EOM


if [[ -s $FILE ]] ; then
echo "$FILE has data."
else
echo "$FILE is empty."
fi ;



ls -l $FILE
echo 'New credentials generated successfully!!'
chmod u+x $FILE
ls $FILE # assign run credentials
cat $FILE
mv $FILE ../$FILE

