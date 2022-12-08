#need to install git first.
apt-get update
apt-get curl
apt-get install net-tools

echo "Adding universe,multiverse,.."
apt-add-repository universe
apt-add-repository multiverse
apt-add-repository restricted

echo "sourcing ros keys"
sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654

echo "installing ros"
apt-get update
apt-get install ros-melodic-ros-desktop
sh -c 'echo "source /opt/ros/melodic/setup.bash" >> ~/.bashrc'
source ~/.bashrc

echo "installing ros dependencies"
apt install python-rosdep python-rosinstall python-rosinstall-generator python-wstool build-essential
apt install python-rosdep
rosdep init
rosdep update

# make home directory
mkdir -p /home/ubuntu/
chown -R 999.999 /home/ubuntu/
cp /etc/skel/.??* /home/ubuntu
chown -R 999.999 /home/ubuntu/.??*
echo "
# ROS setup
source /opt/ros/$ROSDISTRO/setup.bash

# This file is created on ${DATE}
" >> /home/ubuntu/.bashrc
HOME=/home/ubuntu rosdep update
chown -R 999.999 /home/ubuntu/.ros