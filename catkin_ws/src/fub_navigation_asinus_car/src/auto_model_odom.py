#!/usr/bin/env python
from gazebo_msgs.srv import GetLinkState
from gazebo_msgs.srv import GetLinkStateRequest
from nav_msgs.msg import Odometry
import rospy
import sys

class OdomPublisher:
	def __init__(self,model): 
		self.get_link_state = rospy.ServiceProxy('/gazebo/get_link_state', GetLinkState)
		self.get_link_req   = GetLinkStateRequest()
		self.get_link_req.link_name = model+'::base_link'
		self.msg = Odometry()
		self.msg.header.frame_id = 'map'
		self.odom_pub = rospy.Publisher('/'+model+'/Odometry', Odometry, queue_size=1, tcp_nodelay=True)


	def run(self,rate): 
		loop = rospy.Rate(rate)
		while not rospy.is_shutdown():
			link_state = self.get_link_state(self.get_link_req)
			self.msg.header.stamp = rospy.Time.now()
			self.msg.pose.pose = link_state.link_state.pose
			self.odom_pub.publish(self.msg)
			loop.sleep()

def main(args): 
	rospy.init_node('AutoModelMiniOdom', anonymous=True)
	model = rospy.get_param("~model","AutoModelMini")
	node = OdomPublisher(model)
	try: 
		node.run(10)
	except rospy.ROSInterruptException:
		pass

if __name__=='__main__': 
	main(sys.argv)