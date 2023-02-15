#need to install git first.
sudo apt-get update
sudo apt-get install net-tools

echo "Adding universe,multiverse,.."
sudo apt-add-repository universe
sudo apt-add-repository multiverse
sudo apt-add-repository restricted

echo "sourcing ros keys"
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
sudo apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654

echo "installing ros"
sudo apt-get update
sudo apt-get install ros-melodic-desktop

echo "installing ros dependencies"
sudo apt install python-rosdep python-rosinstall python-rosinstall-generator python-wstool build-essential
rosdep init
sudo rosdep fix-permissions
rosdep update

# make home directory
mkdir -p /home/ubuntu/
sudo chown -R 999.999 /home/ubuntu/
sudo cp /etc/skel/.??* /home/ubuntu
sudo chown -R 999.999 /home/ubuntu/.??*

sudo sh -c "echo 'source /opt/ros/melodic/setup.bash' >> /home/ubuntu/.bashrc"

HOME=/home/ubuntu rosdep update
sudo chown -R 999.999 /home/ubuntu/.ros