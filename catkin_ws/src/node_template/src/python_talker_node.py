#!/usr/bin/python2
import rospy
import rospkg
from std_msgs.msg import String

class Node:
	def __init__(self):
		self.pub = rospy.Publisher("/dummy_test/string_topic",String,queue_size=1)
 	def talk(self,rate):
		rate = rospy.Rate(rate)
		while(not rospy.is_shutdown()):
			rospy.loginfo("Publishing message")
			msg = String()
			msg.data = "Hola"
			self.pub.publish(msg)
			rate.sleep()

def main():
	rospy.init_node("python_node",anonymous=True)
	node = Node()
	node.talk(1)

if __name__=='__main__':
	main()