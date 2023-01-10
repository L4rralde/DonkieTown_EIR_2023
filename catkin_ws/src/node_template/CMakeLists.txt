cmake_minimum_required(VERSION 3.0.2)
project(node_template)

find_package(catkin REQUIRED COMPONENTS
  geometry_msgs
  roscpp
  rospy
  std_msgs
)

catkin_package()

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

add_executable(cpp_talker_node src/cpp_talker_node.cpp)
add_executable(cpp_listener_node src/cpp_listener_node.cpp)

target_link_libraries(cpp_talker_node
  ${catkin_LIBRARIES}
)
target_link_libraries(cpp_listener_node
  ${catkin_LIBRARIES}
)

catkin_install_python(PROGRAMS
  src/python_talker_node.py
  src/python_listener_node.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)