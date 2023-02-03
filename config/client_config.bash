cd $(dirname $(readlink -f "${BASH_SOURCE:-$0}"))
export COURSE_PATH=$(git rev-parse --show-toplevel)
cd - > /dev/null
source $COURSE_PATH/catkin_ws/devel/setup.bash
export ROS_MASTER_URI=192.168.100.$1
export ROS_IP=$(ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep 192.168.100.)