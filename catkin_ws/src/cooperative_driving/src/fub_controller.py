import sys
import rospy
import rospkg
import cv2
import math
import numpy as np
from tf.transformations import euler_from_quaternion
sys.path.append(rospkg.RosPack().get_path('fub_navigation_asinus_car')+'/scripts/')
from path_parser import read_points
from scipy.spatial import KDTree

class PID:
    def __init__(self,Kp,Ki,Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.last_time = rospy.Time.now()
        self.integral_error = 0.0
        self.last_e = 0.0
    def control(self,star,current):
        now = rospy.Time.now()
        dt = (now-self.last_time).to_sec()
        self.last_time = now

        e = star-current
        self.integral_error += e*dt
        u = self.Kp*e+self.Ki*self.integral_error+self.Kd*(e-self.last_e)/dt
        self.last_e = e
        return u
class MapConfig(object):
    def __init__(self,map_name,look_ahead='50cm'): 
        rospack = rospkg.RosPack()
        path = rospack.get_path('fub_navigation_asinus_car')+'/scripts/maps/'+map_name+'/'
        map_img = cv2.imread(path+'map.png')
        (h,w,l) = map_img.shape
        self.map_size_x = w  # cm
        self.map_size_y = h  # cm
        self.resolution = 1  #More than an argument, it's a parameter to meet. 
        #self.matrix_lane_1 = np.load(path + 'matrix'+look_ahead+'_lane1.npy')
        self.matrix_lane_1 = np.load(path + 'matrix-'+look_ahead+'_lane1.npy') #[FUTURE][FIXME]: Redraw svg files to avoid 
                                                                                #having different directions.
        #self.matrix_rlane_1 = np.load(path + 'matrix-'+look_ahead+'_lane1.npy')
        self.matrix_lane_2 = np.load(path + 'matrix'+look_ahead+'_lane2.npy')
        #self.matrix_rlane_2 = np.load(path + 'matrix-'+look_ahead+'_lane2.npy')

        self.distance_lane_1 = np.load(path + 'matrix0cm_lane1.npy')
        self.distance_lane_2 = np.load(path + 'matrix0cm_lane2.npy')

        xy = np.array(list(read_points(path+'new_map_loop1.txt'))) \
                -np.array([self.map_size_x,self.map_size_y])*self.resolution/200.0
        xy = np.flip(xy,axis=0) #[FUTURE][FIXME]: Redraw svg files to avoid having different directions.
        self.tree_lane1 = KDTree(xy)
        xy = np.array(list(read_points(path+'new_map_loop2.txt'))) \
                -np.array([self.map_size_x,self.map_size_y])*self.resolution/200.0
        self.tree_lane2 = KDTree(xy)
        self.path_len = len(xy)

class VectorfieldController(MapConfig):
    def __init__(self,map_name,lane,look_ahead):
        print(map_name,lane,look_ahead)
        super(VectorfieldController,self).__init__(map_name,look_ahead)
        
        self.lane = lane
        
        self.x = 0.0
        self.y = 0.0 

        self.last_lane_change = rospy.Time.now()
        
        self.Ks = [4.0,0.0,1.0]
        self.last_var = [0.0,0.0]
        self.last_time = rospy.Time.now()
        self.integral_error = 0.0

        if self.lane == 1:
            self.matrix = self.matrix_lane_1
            self.tree = self.tree_lane1
        else:
            self.matrix = self.matrix_lane_2 #Please, fix this by renaming the file
            self.tree = self.tree_lane2

    def get_coords_from_vf(self,raw_x, raw_y, matrix=None):
        if matrix is None:
            matrix = self.matrix
        #To match vector field
        x = raw_x+self.map_size_x/200.0
        y = raw_y+self.map_size_y/200.0
        x_index_floor = int(math.floor(x * (100.0 / self.resolution))) #Converting to cm
        y_index_floor = int(math.floor(y * (100.0 / self.resolution)))

        x_index_ceil = x_index_floor + 1
        y_index_ceil = y_index_floor + 1

        ceil_ratio_x = x * (100.0 / self.resolution) - x_index_floor #To check how much interpolate between floor and ceil.
        ceil_ratio_y = y * (100.0 / self.resolution) - y_index_floor

        if x_index_floor < 0:
            x_index_floor = 0
        if x_index_floor > self.map_size_x / self.resolution - 1:
            x_index_floor = self.map_size_x / self.resolution - 1

        if y_index_floor < 0:
            y_index_floor = 0
        if y_index_floor > self.map_size_y / self.resolution - 1:
            y_index_floor = self.map_size_y / self.resolution - 1

        if x_index_ceil < 0:
            x_index_ceil = 0
        if x_index_ceil > self.map_size_x / self.resolution - 1:
            x_index_ceil = self.map_size_x / self.resolution - 1

        if y_index_ceil < 0:
            y_index_ceil = 0
        if y_index_ceil > self.map_size_y / self.resolution - 1:
            y_index_ceil = self.map_size_y / self.resolution - 1

        vx_floor, vy_floor = matrix[x_index_floor, y_index_floor, :]
        vx_ceil, vy_ceil = matrix[x_index_ceil, y_index_ceil, :]

        vx = vx_floor * (1.0 - ceil_ratio_x) + vx_ceil * ceil_ratio_x
        vy = vy_floor * (1.0 - ceil_ratio_y) + vy_ceil * ceil_ratio_y
        return (vx,vy)

    def ddr_control(self,pose_msg,speed_value=None):
        dt = (pose_msg.header.stamp - self.last_time).to_sec()
        # 25hz
        if dt < 0.04:
            return (None, None,None)
        self.last_time = pose_msg.header.stamp
        self.x = pose_msg.pose.pose.position.x #Actual coord-x
        self.y = pose_msg.pose.pose.position.y #Actual coord-y
        orientation_q = pose_msg.pose.pose.orientation
        orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
        (roll, pitch, yaw) = euler_from_quaternion(orientation_list) #Actual yaw
        delta_xd,delta_yd = self.get_coords_from_vf(self.x,self.y,self.matrix)
        #eccentric point ddr controller
        ps = delta_xd+self.x
        qs = delta_yd+self.y
        dps = (ps-self.last_var[0])/dt
        dqs = (qs-self.last_var[1])/dt
        self.last_var[0] = ps
        self.last_var[1] = qs
        nu1 = dps+self.Ks[0]*(delta_xd)
        nu2 = dqs+self.Ks[1]*(delta_yd)
        speed = np.cos(yaw)*nu1+np.sin(yaw)*nu2
        steering = 14.2857*(-np.sin(yaw)*nu1+np.cos(yaw)*nu2) #where 14.2857 = 1/mu, mu:eccentrecity. Taking mu=0.07
        return(speed,steering,None)

    def pd_control(self, pose_msg, speed_value):
        dt = (pose_msg.header.stamp - self.last_time).to_sec()
        # 25hz
        if dt < 0.04:
            return (None,None,None)
        self.last_time = pose_msg.header.stamp
        self.x = pose_msg.pose.pose.position.x
        self.y = pose_msg.pose.pose.position.y
        orientation_q = pose_msg.pose.pose.orientation
        orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
        (roll, pitch, yaw) = euler_from_quaternion(orientation_list)

        x3,y3 = self.get_coords_from_vf(self.x,self.y,self.matrix)
        f_x = np.cos(yaw) * x3 + np.sin(yaw) * y3
        f_y = -np.sin(yaw) * x3 + np.cos(yaw) * y3

        angle = np.arctan2(f_y, f_x)

        self.integral_error = self.integral_error + angle * dt
        steering = self.Ks[0] * angle + self.Ks[2] * ((angle - self.last_var[0]) / dt) + self.Ks[1] * self.integral_error
        self.last_var[0] = angle

        if f_x > 0:
            speed = speed_value
        else:
            speed = speed_value

        gain = 1.0#+1.0*np.exp(-10.0*abs(steering))
        if f_x > 0:
            speed = max(speed_value*gain, gain*(speed* ((np.pi / 3) / (abs(steering) + 1))))
        return (speed,steering,angle)
    def fuzzy_control(self, pose_msg, speed_value):
        #FUTURE
        pass
    def lane_change(self):
        if not self.lane_change_req():
            return
        if self.lane == 1:
            self.matrix = self.matrix_lane_2
            self.tree = self.tree_lane2
            self.lane = 2
        else:
            self.matrix = self.matrix_lane_1
            self.tree = self.tree_lane1
            self.lane = 1
        self.last_lane_change = rospy.Time.now()
        print("lane change")
    def lane_change_req(self):
        return (rospy.Time.now()-self.last_lane_change).to_sec()>5.0
    def get_coords_from_car(self, pt):
        return [pt.x-self.x, pt.y-self.y]
    def get_coords_from_lanes(self, pt):
        xm = pt.x+self.map_size_x/200.0
        ym = pt.y+self.map_size_y/200.0
        (xi, yi) = int(xm*(100/self.resolution)), int(ym*(100/self.resolution))
        (xd1, yd1) = self.distance_lane_1[xi, yi, :]
        (xd2, yd2) = self.distance_lane_2[xi, yi, :]
        if self.lane == 1:
            return([[xd1,yd1],[xd2,yd2]])
        else:
            return([[xd2,yd2],[xd1,yd1]])
    def findNearestIndex(self,pt):
        dist,index = self.tree.query(np.asarray(pt))
        return index
    def findNearest(self,pt):
        i,d = self.findNearestIndex(pt)
        return(self.tree.data[i])
    def getPathDistance(self,ptA=None,ptB=None):
        if ptA is None:
            ptA = [self.x,self.y]
        indexA = self.findNearestIndex(ptA)
        indexB = self.findNearestIndex(ptB)
        return ((indexB-indexA)%self.path_len)*self.resolution/100.0