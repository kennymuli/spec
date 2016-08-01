yum group install "Development tools"
yum install wget python-pip libaio-devel python-devel python-lxml -y
pip install mysql-python
pip install sqlalchemy


wget http://dl.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-7.noarch.rpm
rpm -ivh epel-release-7-7.noarch.rpm
wget http://dev.mysql.com/get/mysql57-community-release-el7-8.noarch.rpm
rpm -ivh mysql57-community-release-el7-8.noarch.rpm
yum install mysql-community-server -y
yum install mysql-community-devel -y


##--------------Spec Installation---------------------------

wget https://s3.amazonaws.com/vdbenchbuckettest/cpu2006-1.2.iso
mkdir -p /SPEC/CPU2006 /specisomount/cpu2006iso
mount -t iso9660 -o ro,exec cpu2006-1.2.iso /specisomount/cpu2006iso
cd /specisomount/cpu2006iso
./install.sh -d /SPEC/CPU2006
umount /specisomount/cpu2006iso
rm -rf /specisomount

##------------- Spec Installation end------------------------