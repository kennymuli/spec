#!/bin/bash

apt-get install build-essential
apt-get install wget python-pip mysql-server libmysqlclient-dev libaio1 python-dev python-lxml --yes
pip install mysql-python
pip install sqlalchemy

##--------------Spec Installation---------------------------

wget https://s3.amazonaws.com/vdbenchbuckettest/cpu2006-1.2.iso
mkdir -p /SPEC/CPU2006 /specisomount/cpu2006iso
mount -t iso9660 -o ro,exec cpu2006-1.2.iso /specisomount/cpu2006iso
cd /specisomount/cpu2006iso
./install.sh -d /SPEC/CPU2006
umount /specisomount/cpu2006iso
rm -rf /specisomount

##------------- Spec Installation end------------------------