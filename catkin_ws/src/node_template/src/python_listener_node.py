#!/usr/bin/python2
import rospy
import rospkg
from std_msgs.msg import String

class Node:
	def __init__(self):
		self.pub = rospy.Publisher("/dummy_test/status",String,queue_size=1,latch=True)
		self.sub = rospy.Subscriber("/dummy_test/string_topic",String,self.on_listen,queue_size=1)
	def on_listen(self,msg):
		rospy.loginfo(msg.data)
		st_msg = String()
		st_msg.data = "Estoy vivo!"
		self.pub.publish(st_msg)

def main():
	rospy.init_node("python_listener_node", anonymous=True)
	node = Node()
	rospy.spin()

if __name__ == '__main__':
	main()	