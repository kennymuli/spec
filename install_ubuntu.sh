#!/bin/bash
apt-get install build-essential
gcc -v
make -v
apt-get install wget --yes
MYPATH=`pwd`
#wget https://s3.amazonaws.com/vdbenchbuckettest/cpu2006-1.2.iso
#mkdir -p /SPEC/CPU2006 /specisomount/cpu2006iso
#mount -t iso9660 -o ro,exec cpu2006-1.2.iso /specisomount/cpu2006iso
#cd /specisomount/cpu2006iso
#./install.sh -d /SPEC/CPU2006
cd /SPEC/CPU2006
source shrc
cd $MYPATH
#umount /specisomount/cpu2006iso
#rm -rf /specisomount

cpu_arch=`uname -p`
proc_model=`cat /proc/cpuinfo |grep "model name"|head -1`

echo ""
echo "Your Processor $proc_model and Architecture : $cpu_arch. Please copy and paste the relevant configuration file that matches your machine from the list shown below: "
echo ""
cd /SPEC/CPU2006/config/
ls Example*
echo ""
read -p "Enter the relevant configuration file: " spec_conf
echo ""
rm spec_test_config.cfg
cp $spec_conf spec_test_config.cfg
cd $MYPATH
./run_ubuntu.sh