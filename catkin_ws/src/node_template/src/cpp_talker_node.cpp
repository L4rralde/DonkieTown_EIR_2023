#include "ros/ros.h"
#include "std_msgs/String.h"

class Node{
	ros::Publisher pub;
public:
	Node(ros::NodeHandle *nh){
		pub = nh->advertise<std_msgs::String>("/dummy_test/string_topic",1);
	}
	void talk(int rate){
		ros::Rate loop_rate(rate);
		while(ros::ok()){
			std_msgs::String msg;
			msg.data = "Hola";
			ROS_INFO("Publicando mensaje");
			pub.publish(msg);
			ros::spinOnce();
			loop_rate.sleep();
		}
	}
};

int main(int argc, char **argv){
	ros::init(argc,argv,"cpp_talker_node");
	ros::NodeHandle nh;
	Node node = Node(&nh);
	node.talk(1);

	return 0;
}