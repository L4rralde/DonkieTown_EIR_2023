cmake_minimum_required(VERSION 3.0.2)
project(hola_ros)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  std_msgs
  geometry_msgs # Twist msg usado en publicador.cpp y subscriptor.cpp
)

catkin_package()

include_directories(${catkin_INCLUDE_DIRS})

#Para cada nodo:
add_executable(hola src/hola.cpp)
target_link_libraries(hola
  ${catkin_LIBRARIES}
)

add_executable(publicador src/publicador.cpp)
target_link_libraries(publicador
  ${catkin_LIBRARIES}
)

add_executable(subscriptor src/subscriptor.cpp)
target_link_libraries(subscriptor
  ${catkin_LIBRARIES}
)