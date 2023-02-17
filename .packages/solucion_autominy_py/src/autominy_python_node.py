#!/usr/bin/python2
import rospy
from autominy_msgs.msg import NormalizedSpeedCommand, NormalizedSteeringCommand

class Node:
	def __init__(self):
		self.vel_pub = rospy.Publisher("/actuators/speed_normalized",NormalizedSpeedCommand,queue_size=1)
		self.giro_pub = rospy.Publisher("/actuators/steering_normalized",NormalizedSteeringCommand,queue_size=1)
		rospy.sleep(1)
	def publish(self,velocidad,giro):
		vel_msg = NormalizedSpeedCommand()
		giro_msg = NormalizedSteeringCommand()
		vel_msg.value = velocidad
		giro_msg.value = giro

		rospy.loginfo("Publicando mensaje")
		self.vel_pub.publish(vel_msg)
		self.giro_pub.publish(giro_msg)
	def talk(self):
		self.publish(0.2,-0.5)
		rospy.sleep(2)
		self.publish(0.2,0.0)
		rospy.sleep(2)
		self.publish(0.2,0.5)
		rospy.sleep(2)
		self.publish(0.0,0.0)
		rospy.logwarn("Terminando secuencia")

def main():
	rospy.init_node("autominy_driver",anonymous=True)
	node = Node()
	node.talk()

if __name__=='__main__':
	main()		
		
