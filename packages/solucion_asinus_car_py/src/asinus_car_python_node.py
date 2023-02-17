#!/usr/bin/python2
import rospy
from donkietown_msgs.msg import MotorsSpeed

class Node:
	def __init__(self):
		self.pub = rospy._______("_______",_______,queue_size=1)
		rospy.sleep(1)
	def publish(self,left,right):
		msg = _______
		msg.leftMotor = left
		msg.rightMotor = right
		rospy.loginfo("Publicando mensaje")
		_______.publish(msg)
	def talk(self):
		self.publish(40,20)
		rospy.sleep(2)
		self.publish(40,40)
		rospy.sleep(2)
		self.publish(20,40)
		rospy.sleep(2)
		self.publish(0,0)
		rospy.logwarn("Terminando secuencia")

def main():
	rospy._______("_______",anonymous=True)
	node = Node()
	node.talk()

if __name__=='__main__':
	main()