# Introducción a ROS

En esta paǵina encontrarás un resumen de los nodos creados en la clase introductoria. Puedes acceder a las diapositivas empleadas en el siguiente [enlace](https://docs.google.com/presentation/d/11rba075v5t-SfsgQmFG1QgTjC17kRaaJnMfp66Bpsvo/edit?usp=sharing).

1. Crear espacio de trabajo o workspace
```
cd ~
mkdir -p catkin_ws/src
cd ~/catkin_ws
catkin_make
```

2. Crear paquete o package
```
cd ~catkin_ws/src
catkin_create_pkg hola_ros roscpp std_msgs geometry_msgs
```

3. Crear archivo de código fuente (hola.cpp por ejemplo)
```
mkdir ~/catkin_ws/src/hola_ros/src
cd ~/catkin_ws/src/hola_ros/src
gedit hola.cpp
```
Este nodo incluye el siguiente código

```cpp
#include <ros/ros.h>

int main (int argc, char **argv) {
	// Inicializar el sistema de ROS
	ros::init(argc , argv, "hello_ros");

	// Establecer este programa como un nodo de ROS
	ros::NodeHandle nh;

	// Enviar una salida como mensaje al log
	ROS_INFO_STREAM("Hola, ROS!") ;
}
```