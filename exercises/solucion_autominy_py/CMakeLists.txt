cmake_minimum_required(VERSION 3.0.2)
project(solucion_autominy_py)

find_package(catkin REQUIRED COMPONENTS
  autominy_msgs
  rospy
  std_msgs
)

catkin_package()

include_directories(${catkin_INCLUDE_DIRS})

catkin_install_python(PROGRAMS
  src/autominy_python_node.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)