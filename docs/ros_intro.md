# Introducción a ROS

En esta paǵina encontrarás un resumen de los nodos creados en la clase introductoria. Puedes acceder a las diapositivas empleadas en el siguiente [enlace](https://docs.google.com/presentation/d/11rba075v5t-SfsgQmFG1QgTjC17kRaaJnMfp66Bpsvo/edit?usp=sharing). El paquete creado en esta clase lo puedes encontrar en [catkin_ws/src/hola_ros](../catkin_ws/src/hola_ros)



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
### Nodo hola
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

4. Editar CMakeLists.txt
```
cd ~/catkin_ws/src/hola_ros/
gedit CMakeLists.txt
```
Para poder compilar hola.cpp, el archivo CMakeLists debe quedar como sigue
```
cmake_minimum_required(VERSION 3.0.2)
project(hola_ros)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  std_msgs
  geometry_msgs # Twist msg usado en publicador.cpp y subscriptor.cpp
)

catkin_package()

include_directories(${catkin_INCLUDE_DIRS})

# Sólamente el código de abajo es específico para el nodo "hola"
add_executable(hola src/hola.cpp)
target_link_libraries(hola
  ${catkin_LIBRARIES}
)
```

5. Editar package.xml
Este paso no es necesario en este punto si realizaste el paso 2.

### Nodo publicador
6. Crear el archivo de código fuente
```
cd ~/catkin_ws/src/hola_ros/src
gedit publicador.cpp
```
Incluye el siguiente código
```cpp
// Este programa publica mensajes de velocidad aleatoriamente generados para turtlesim
#include<ros/ros.h>
#include<geometry_msgs/Twist.h>	//Para geometry_msgs::Twist
#include<stdlib.h>			//Para rand() y RAND_MAX

int main(int argc, char **argv){
// Inicializa el sistema de ROS.
ros::init(argc, argv, "publish_velocity");
ros::NodeHandle nh;

// Crea un objeto tipo publisher
ros::Publisher pub = nh.advertise<geometry_msgs::Twist>("turtle1/cmd_vel", 1000);

// Agrega una semilla a la generación de números aleatorios.
srand(time(0));

//Repite a 2Hz hasta que el nodo se apague
ros::Rate rate(2);

while(ros::ok()){
	// Crea y llena el mensaje de tipo velocidad. 
	// Por defecto todos los campos valen 0 al construir el objeto.
	geometry_msgs::Twist msg;
	msg.linear.x = double(rand())/double(RAND_MAX);
	msg.angular.z = 2*double(rand())/double(RAND_MAX) - 1;
		// Publica el mensaje:
	pub.publish(msg);

	// Envía un mensaje a rosout con los detalles
	ROS_INFO_STREAM("Sending random velocity command:"
		<< " linear="<<msg.linear.x << " angular=" << msg.angular.z);

	// Espera hasta que sea el tiempo para la próxima iteración.
	rate.sleep();
	}
}
```

7. Editar CMakeLists para añadir publicador.cpp al flujo de compilación
```
cd ~/catkin_ws/src/hola_ros/
gedit CMakeLists.txt
```
Al final del archivo añade lo siguiente:
```
add_executable(publicador src/publicador.cpp)
target_link_libraries(publicador
  ${catkin_LIBRARIES}
)
```

### Nodo subscriptor
De forma muy similar al nodo publicador:

8. Crear archivo con código fuente.
```
cd ~/catkin_ws/src/hola_ros/src
gedit subscriptor.cpp
```
Código:
```cpp
#include<ros/ros.h>
#include<geometry_msgs/Twist.h>

// Funcion callback que es llamada siempre que se recibe un mensaje en el tópic al que se subscribe
void callback(const geometry_msgs::Twist& msg){
	ROS_INFO("Recibi componente lineal [%f, %f, %f]", msg.linear.x, msg.linear.y, msg.linear.z);
	ROS_INFO("Recibi componente angular [%f, %f, %f]", msg.angular.x, msg.angular.y, msg.angular.z);
}

int main(int argc, char **argv){
	ros::init(argc, argv, "subscibre_velocity");
	ros::NodeHandle nh;
	// Objeto de subscriptor al tópico /turtle1/cmd_vel
	ros::Subscriber sub = nh.subscribe("/turtle1/cmd_vel",1000,callback);

	ros::spin();
	return 0;
}
```

## Observaciones
- El paso 1. es necesario solo para crear un nuevo workspace
- En el paso 2 se crea un nuevo paquete. Puedes definir más de un nodo en un paquete, así que podrías usar un paquete anteriormente creado.