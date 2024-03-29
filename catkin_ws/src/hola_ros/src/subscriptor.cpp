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