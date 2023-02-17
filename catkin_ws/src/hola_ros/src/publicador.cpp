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