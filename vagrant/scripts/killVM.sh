#!/bin/bash




echo 'Killing Virtual Machines'




VBoxManage list runningvms | awk '{print $2;}' | xargs -I vmid VBoxManage controlvm vmid poweroff;




echo "Finish Massacre"