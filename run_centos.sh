MYPATH=`pwd`
cd /SPEC/CPU2006
source shrc
cd $MYPATH
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

python base.py