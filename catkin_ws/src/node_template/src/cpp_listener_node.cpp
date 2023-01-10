#include "ros/ros.h"
#include "std_msgs/String.h"

class Node{
	ros::Publisher pub;
	ros::Subscriber sub;
public:
	Node(ros::NodeHandle *nh){
		pub = nh->advertise<std_msgs::String>("/dummy_test/status",1);
		sub = nh->subscribe("/dummy_test/string_topic",1,&Node::callback,this);
	}
	void callback(const std_msgs::String& msg){
		ROS_INFO("%s", msg.data.c_str());
		std_msgs::String cb_msg;
		cb_msg.data = "Estoy vivo!";
		pub.publish(cb_msg);
	}
};

int main(int argc, char **argv){
	ros::init(argc,argv,"cpp_listener_node");
	ros::NodeHandle nh;
	Node node = Node(&nh);
	ros::spin();

	return 0;
}