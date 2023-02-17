#!/usr/bin/env python2
import rospy
from auto_model import AsinusCar, pcs2pose2d
from sensor_msgs.msg import PointCloud
from fub_controller import VectorfieldController
import numpy as np
import v2x

class CooperativeDrivingNode(object):
	def __init__(self,car_id,map_name,lane,look_ahead,speed_value):
		self.car_id = car_id
		self.car = AsinusCar(car_id)
		self.car_s = 0.0
		self.car_w = 0.0 
		self.speed_value = speed_value

		self.vectorField = VectorfieldController(map_name,lane,look_ahead)
		self.lanes_blocked = [False,False]

		self.driving_state = v2x.driving_states['Stop'] 

		self.myCAM = v2x.CAMPublisher(car_id)
		self.extCAM = v2x.CAMSubscriber(car_id)
		self.initCAM()
		self.myCAM.publish()

		self.sub_obs = rospy.Subscriber("/sensors/obstacles",PointCloud,self.on_obstacle, queue_size=1) #Need to remap topic while using v2x

		rospy.on_shutdown(self.shutdown)
		self.shutdown_ = False
	def getCAMs(self):
		return self.extCAM.msg_cache
	def on_obstacle(self,msg):
		pts = msg.points
		blocked = [False,False] 
		for pt in pts: 
			pt_car = self.vectorField.get_coords_from_car(pt)
			pt_lanes = self.vectorField.get_coords_from_lanes(pt)
			#dist_car = np.linalg.norm(pt_car) #[FUTURE]  
			dist_car = self.vectorField.getPathDistance(ptB=[pt.x,pt.y])
			if dist_car > 0.5:
				continue
			dist_lane = np.linalg.norm(pt_lanes, axis=1)
			rospy.logwarn(dist_lane)
			rospy.logwarn(dist_car)
			rospy.logwarn(dist_lane)
			blocked = dist_lane<0.1
		rospy.logwarn(blocked)
		self.lanes_blocked = blocked
	def run(self): #Model car state variables estimation
		pcs = self.car.getPCS()
		twist = self.car.getTwist()
		if pcs is None or twist is None:
			return
		self.s = twist.linear.x
		self.w = twist.angular.z
		if self.driving_state==v2x.driving_states['LaneChangeGrant']:
			self.vectorField.lane_change()
			self.lanes_blocked = list(reversed(self.lanes_blocked))
			rospy.logwarn("LaneChange")
		ctrl_s,ctrl_w,heading = self.vectorField.pd_control(pcs,self.speed_value)
		if (ctrl_s is not None) and (not self.shutdown_) and (self.driving_state!=v2x.driving_states['Stop']):
			self.car.drive(ctrl_s,ctrl_w)
		elif self.driving_state==v2x.driving_states['Stop']:
			self.car.stop()
		pose2D = pcs2pose2d(pcs)
		self.myCAM.set(pose2D,self.s,self.vectorField.lane,True,heading,self.driving_state)
		self.myCAM.publish()
  	def talker(self,rate):
  		rate = rospy.Rate(rate)
  		self.driving_state = v2x.driving_states['Drive']
  		while not rospy.is_shutdown():
  			self.run()
  			rate.sleep()
  	def stop(self):
  		self.car.stop()
  	def shutdown(self):
  		print("shutdown!")
  		self.shutdown_ = True
  		self.car.stop()
  		rospy.sleep(1)
  	def initCAM(self):
  		pcs = None
  		while pcs is None and not rospy.is_shutdown():
  			pcs = self.car.getPCS()
		myPose2d = pcs2pose2d(pcs)
		self.myCAM.set(myPose2d,0.0,self.vectorField.lane,True,0.0,self.driving_state)

def main():
	rospy.init_node("cooperative_driving")
	car_id = rospy.get_param("~car_id")
	map_name = rospy.get_param("~map_name","cimat_reduced")
	lane = rospy.get_param("~lane",1)
	look_ahead = rospy.get_param("~look_ahead","30cm")
	speed = rospy.get_param("~speed",0.1)
	rate = rospy.get_param("~rate",10)
	
	node = CooperativeDrivingNode(car_id,map_name,lane,look_ahead,speed)
	try:
		node.talker(rate)
	except rospy.ROSInterruptException:
		pass
if __name__=='__main__':
	main()