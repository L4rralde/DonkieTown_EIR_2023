cmake_minimum_required(VERSION 3.0.2)
project(solucion_autominy_cpp)

find_package(catkin REQUIRED COMPONENTS
  autominy_msgs
  roscpp
  std_msgs
)

catkin_package()

include_directories(
  include
  ${catkin_INCLUDE_DIRS}
)

add_executable(autominy_cpp_node src/autominy_cpp_node.cpp)

target_link_libraries(autominy_cpp_node
  ${catkin_LIBRARIES}
)

add_dependencies(autominy_cpp_node
  ${catkin_EXPORTED_TARGETS}
)