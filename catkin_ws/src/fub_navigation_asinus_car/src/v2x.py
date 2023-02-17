import rospy
from donkietown_msgs.msg import CooperativeAwarenessMessage as CAM

class CAMPublisher:
	def __init__(self, car_id):
		cam = CAM()
		cam.header.frame_id = str(car_id)
		self.cam = cam
		self.cam_pub = rospy.Publisher('/v2x/CAM/pool', CAM, queue_size=1)
	def set(self,pose,speed,lane,drive_direction,heading,lane_change):
		self.cam.reference_pose.x = pose[0]
		self.cam.reference_pose.y = pose[1]
		self.cam.reference_pose.theta = pose[2]
		self.cam.speed = speed
		self.cam.lane = lane
		self.cam.drive_direction = drive_direction
		self.cam.heading = heading
		self.cam.lane_change = lane_change
	def publish(self):
		self.cam.header.stamp = rospy.Time.now()
		self.cam_pub.publish(self.cam)

class CAMSubscriber(object):
	def __init__(self, car_id, queue_size=2):
		self.car_id = int(car_id)
		self.msg_cache = {}
		self.cam_sub = rospy.Subscriber('/v2x/CAM/'+str(car_id)+'/rx', CAM, self.onCAM, queue_size=queue_size)
	def onCAM(self,cam):
		car_id = int(cam.header.frame_id)
		if car_id == self.car_id:
			return
		self.msg_cache[car_id] = cam
	def clean(self, time_th=2.0):
		last_time = rospy.Time.now()
		for key in self.msg_cache.keys():
			if abs((last_time-self.msg_cache[key].header.stamp).to_sec()) > time_th:
				del self.msg_cache[key]