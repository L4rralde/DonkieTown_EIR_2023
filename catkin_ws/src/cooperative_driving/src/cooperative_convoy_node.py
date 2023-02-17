#!/usr/bin/env python2
import rospy
from cooperative_driving_node import CooperativeDrivingNode
from fub_controller import PID
from auto_model import pcs2pose2d
import v2x

roles = {	'Unknown': 0,
			'Leader': 1,
			'Follower': 2}

class CooperativeConvoyNode(CooperativeDrivingNode):
	def __init__(self,car_id,map_name,lane,look_ahead,speed_value,distance):
		super(CooperativeConvoyNode,self).__init__(car_id,map_name,lane,look_ahead,speed_value)
		self.distance = distance
		self.dist_ctrler = PID(0.4,0.0,0.05) #PD
		self.role = roles['Unknown']
		while self.role==roles['Unknown'] and not rospy.is_shutdown():
			self.role,self.leading = self.getRole()
			#print(self.role,self.leading)
			rospy.sleep(1)

	def getRole(self):
		leading = None
		pcs = self.car.getPCS()
		if pcs is None:
			return (roles['Unknown'],leading)
		myPose2d = pcs2pose2d(pcs)
		min_dist = 3.0
		CAMs = self.getCAMs()
		while not rospy.is_shutdown(): #[FIXME]: Find a smarter way
			self.myCAM.publish()
			CAMs = self.getCAMs()
			if len(CAMs)==3: #==1, ==2. #vehicles-1
				break
			rospy.sleep(0.1)
		for CAM in CAMs:
			pose2D = CAMs[CAM].reference_pose
			dist = self.vectorField.getPathDistance([myPose2d.x,myPose2d.y],[pose2D.x,pose2D.y])
			print(dist)
			if dist<=min_dist and dist>0:
				min_dist = dist
				leading = CAM
		if leading is None:
			return (roles['Leader'],leading)
		return (roles['Follower'],leading)

	def run(self):
		super(CooperativeConvoyNode,self).run()
		#rospy.logwarn(self.driving_state)
		#FSM propagation
		CAMs = self.getCAMs()
		if self.role == roles['Follower']:
			leadingCAM = CAMs[self.leading]
			self.driving_state = leadingCAM.driving_state
			#Distance control
			myPose2d = pcs2pose2d(self.car.getPCS())
			leadingPose = leadingCAM.reference_pose
			distance = self.vectorField.getPathDistance([myPose2d.x,myPose2d.y],
														[leadingPose.x,leadingPose.y])
			print(self.distance,distance)
			#self.speed_value = ... #PID?
			self.speed_value = max(0,min(0.25,0.1-self.dist_ctrler.control(self.distance,distance)))
			print(self.speed_value)
			return
		#FSM Handling (Just for Leader)
		print(self.speed_value)
		if self.driving_state==v2x.driving_states['LaneChangeReq']:
			if self.vectorField.lane_change_req():
				self.driving_state = v2x.driving_states['LaneChangeGrant']
				return
		if not self.lanes_blocked[0]:
			self.driving_state = v2x.driving_states['Drive']
			return
		if not self.lanes_blocked[1]:
			self.driving_state = v2x.driving_states['LaneChangeReq']
			return
		self.driving_state = v2x.driving_states['Stop']

	def talker(self,rate):
		rate = rospy.Rate(rate)
		self.driving_state = v2x.driving_states['Drive']
		while not rospy.is_shutdown():
  			self.run()
  			rate.sleep()

def main():
	rospy.init_node("cooperative_driving")
	car_id = rospy.get_param("~car_id")
	map_name = rospy.get_param("~map_name","cimat_reduced")
	lane = rospy.get_param("~lane",1)
	look_ahead = rospy.get_param("~look_ahead","30cm")
	speed = rospy.get_param("~speed",0.1)
	rate = rospy.get_param("~rate",10)
	distance = rospy.get_param("~distance",0.5)
	
	node = CooperativeConvoyNode(car_id,map_name,lane,look_ahead,speed,distance)
	try:
		node.talker(rate)
	except rospy.ROSInterruptException:
		pass
if __name__=='__main__':
	main()