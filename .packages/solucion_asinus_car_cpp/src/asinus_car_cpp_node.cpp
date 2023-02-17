#include "ros/ros.h"
#include "donkietown_msgs/MotorsSpeed.h"

class Node{
	ros::Publisher pub;
public:
	Node(ros::NodeHandle *nh){
		pub = nh->advertise<donkietown_msgs::MotorsSpeed>("/asinus_cars/9/motors_driver",1);
		ros::Duration(1).sleep();
	}
	void publish(float left, float right){
		donkietown_msgs::MotorsSpeed msg;
		msg.leftMotor = left;
		msg.rightMotor = right;
		ROS_INFO("Publicando mensaje");
		pub.publish(msg);
	}
	void talk(){
		publish(40,20);
		ros::Duration(2).sleep();
		publish(40,40);
		ros::Duration(2).sleep();
		publish(20,40);
		ros::Duration(2).sleep();
		publish(0,0);
		ROS_WARN("Terminando secuencia");
		ros::spinOnce();
	}
};

int main(int argc, char **argv){
	ros::init(argc,argv,"asinus_car_driver");
	ros::NodeHandle nh;
	Node node = Node(&nh);
	node.talk();
	return 0;
}