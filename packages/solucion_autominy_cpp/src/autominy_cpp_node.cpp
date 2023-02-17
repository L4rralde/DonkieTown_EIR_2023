#include "ros/ros.h"
#include "autominy_msgs/NormalizedSpeedCommand.h"
#include "autominy_msgs/NormalizedSteeringCommand.h"


class Node{
	ros::Publisher vel_pub;
	ros::Publisher giro_pub;
public:
	Node(ros::NodeHandle *nh){
		vel_pub = nh->advertise<_______>("_______",1);
		giro_pub = nh->advertise<_______>("_______",1);
		ros::Duration(1).sleep();
	}
	void publish(float vel, float giro){
		autominy_msgs::_______ vel_msg;
		_______::NormalizedSteeringCommand giro_msg;

		vel_msg.value = vel;
		giro_msg.value = giro;

		ROS_INFO("Publicando mensaje");
		vel_pub._______(vel_msg);
		giro_pub._______(giro_msg);
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
	_______(argc,argv,"_______");
	_______ nh;
	Node node = Node(&nh);
	node.talk();
	return 0;
}