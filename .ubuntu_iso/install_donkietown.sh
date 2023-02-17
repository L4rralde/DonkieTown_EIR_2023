source /opt/ros/melodic/setup.sh
cd ~
git clone https://github.com/L4rralde/DonkieTown_EIR_2023.git
cd ~/DonkieTown_EIR_2023/catkin_ws
catkin_make
cd -
#sudo chown -R 999.999 /home/ubuntu/DonkieTown_EIR_2023/
sudo sh -c "echo 'source ~/DonkieTown_EIR_2023/catkin_ws/devel/setup.bash' >> ~/.bashrc"