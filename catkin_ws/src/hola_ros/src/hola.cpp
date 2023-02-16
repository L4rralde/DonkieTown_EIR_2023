// Primer programa "hola ROS"
#include <ros/ros.h>

int main (int argc, char **argv) {
	// Inicializar el sistema de ROS
	ros::init(argc , argv, "hello_ros");

	// Establecer este programa como un nodo de ROS
	ros::NodeHandle nh;

	// Enviar una salida como mensaje al log
	ROS_INFO_STREAM("Hola, ROS!") ;
}