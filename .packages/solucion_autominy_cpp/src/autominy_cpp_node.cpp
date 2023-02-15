#include "ros/ros.h"
#include "autominy_msgs/NormalizedSpeedCommand.h"
#include "autominy_msgs/NormalizedSteeringCommand.h"


class Node{
	ros::Publisher vel_pub;
	ros::Publisher giro_pub;
public:
	Node(ros::NodeHandle *nh){
		vel_pub = nh->advertise<autominy_msgs::NormalizedSpeedCommand>("/actuators/speed_normalized",1);
		giro_pub = nh->advertise<autominy_msgs::NormalizedSteeringCommand>("/actuators/steering_normalized",1);
	}
	void publish(float vel, float giro){
		autominy_msgs::NormalizedSpeedCommand vel_msg;
		autominy_msgs::NormalizedSteeringCommand giro_msg;

		vel_msg.value = vel;
		giro_msg.value = giro;

		ROS_INFO("Publicando mensaje");
		vel_pub.publish(vel_msg);
		giro_pub.publish(giro_msg);
	}
	void talk(){
		publish(0.2,-0.5);
		ros::Duration(2).sleep();
		publish(0.2,0.0);
		ros::Duration(2).sleep();
		publish(0.2,0.5);
		ros::Duration(2).sleep();
		publish(0.0,0.0);
		ROS_WARN("Terminando secuencia");
		ros::spinOnce();
	}
};

int main(int argc, char **argv){
	ros::init(argc,argv,"autominy_driver");
	ros::NodeHandle nh;
	Node node = Node(&nh);
	node.talk();
	return 0;
}