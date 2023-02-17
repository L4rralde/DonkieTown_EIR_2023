cmake_minimum_required(VERSION 3.0.2)
project(solucion_asinus_car_py)

find_package(catkin REQUIRED COMPONENTS
  donkietown_msgs
  rospy
  std_msgs
)

catkin_package()

include_directories(${catkin_INCLUDE_DIRS})

catkin_install_python(PROGRAMS
  src/asinus_car_python_node.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)