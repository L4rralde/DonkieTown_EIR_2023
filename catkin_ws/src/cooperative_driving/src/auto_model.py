import rospy
from tf.transformations import euler_from_quaternion
from donkietown_msgs.msg import MotorsSpeed, MotorsState
from geometry_msgs.msg import PoseWithCovarianceStamped as PCS
from geometry_msgs.msg import Twist,Pose2D

def pcs2pose2d(pcs):
    pose2D = Pose2D()
    pose2D.x = pcs.pose.pose.position.x
    pose2D.y = pcs.pose.pose.position.y
    orientation_q = pcs.pose.pose.orientation
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    (roll, pitch, yaw) = euler_from_quaternion(orientation_list)
    pose2D.theta = yaw
    return pose2D

class AsinusCar():
    def __init__(self,car_id):
        #DDR control inputs
        self.w = 0
        self.s = 0
        #DDR dimensions
        self.R = 0.03 #wheel radius
        self.L = 0.125 #axis length

        topic_bn = "/asinus_cars/"+str(car_id)
        self.pub_speed = rospy.Publisher(topic_bn+'/motors_driver', MotorsSpeed,
                                         queue_size=1, tcp_nodelay=True)
        self.pose_msg = None
        self.twist_msg = None
        self.pose_sub = rospy.Subscriber(topic_bn+'/filtered_pose',PCS,self.on_pose,queue_size=1)
        self.twist_sub = rospy.Subscriber(topic_bn+'/motors_raw_data',MotorsState,self.on_twist,queue_size=1)
    def on_pose(self, pose_msg):
        self.pose_msg = pose_msg
    def getPCS(self):
        return self.pose_msg
    def getPose2D(self):
        return pcs2pose2d(self.pose_msg)
    def on_twist(self,msg):
        twist_msg = Twist()
        twist_msg.linear.x = 0.5*self.R*(msg.speed.leftMotor+msg.speed.rightMotor)/9.549296
        twist_msg.angular.z = self.R*(msg.speed.rightMotor-msg.speed.leftMotor)/(self.L*9.549296)
        self.twist_msg = twist_msg
    def getTwist(self):
        return self.twist_msg
    def drive(self,speed,steering):
        self.publish_steer(steering)
        self.publish_speed(speed)
    def publish_steer(self,steering): #DDR angular speed.
        self.w = steering
    def publish_speed(self,speed): #DDR longitudinal speed.
    	if(speed==0):
    	    self.stop()
    	    return
        #convert (w,s) -> (ul,ur) [rpm]
        self.s = speed
        ur = 9.549296*(2*self.s+self.L*self.w)/(2*self.R) #9.5492 from rad/s to rpm
        ul = 9.549296*(2*self.s-self.L*self.w)/(2*self.R)
        speed_msg = MotorsSpeed()
        speed_msg.leftMotor = ul
        speed_msg.rightMotor = ur
        self.pub_speed.publish(speed_msg)
    def stop(self):
        self.s = 0
        self.w = 0
    	speed_msg = MotorsSpeed()
    	speed_msg.leftMotor = 0
    	speed_msg.rightMotor = 0
    	self.pub_speed.publish(speed_msg)

#FUTURE:
#   AUTOMINY
#   AUTONOMOUS