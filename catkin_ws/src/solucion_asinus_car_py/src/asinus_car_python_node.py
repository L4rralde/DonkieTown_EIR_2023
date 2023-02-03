#!/usr/bin/python2
import rospy
from donkietown_msgs.msg import MotorsSpeed

class Node:
	def __init__(self):
		self.pub = rospy.Publisher("/asinus_cars/9/motors_driver",MotorsSpeed,queue_size=1)
	def publish(self,left,right):
		msg = MotorsSpeed()
		msg.leftMotor = left
		msg.rightMotor = right
		rospy.loginfo("Publicando mensaje")
		self.pub.publish(msg)
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
	rospy.init_node("asinus_car_driver",anonymous=True)
	node = Node()
	node.talk()

if __name__=='__main__':
	main()