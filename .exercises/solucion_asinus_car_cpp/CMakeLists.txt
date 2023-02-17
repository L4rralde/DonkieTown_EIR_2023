cmake_minimum_required(VERSION 3.0.2)
project(solucion_asinus_car_cpp)

find_package(catkin REQUIRED COMPONENTS
  donkietown_msgs
  roscpp
  std_msgs
)

catkin_package()

include_directories(
  include
  ${catkin_INCLUDE_DIRS}
)

add_executable(asinus_car_cpp_node src/asinus_car_cpp_node.cpp)

target_link_libraries(asinus_car_cpp_node
  ${catkin_LIBRARIES}
)

add_dependencies(asinus_car_cpp_node
  ${catkin_EXPORTED_TARGETS}
)