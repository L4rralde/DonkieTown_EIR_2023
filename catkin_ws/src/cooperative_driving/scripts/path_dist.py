import numpy as np
from scipy.spatial import KDTree
import path_parser
import cv2
import sys
import rospkg
sys.path.append(rospkg.RosPack().get_path('cooperative_driving')+'/src/')
from fub_controller import VectorfieldController

class LaneLine:
	def __init__(self,map_name,lane,flip=False):
		path = rospkg.RosPack().get_path('cooperative_driving')+'/scripts/maps/'+map_name+'/'
		map_img = cv2.imread(path+'map.png')
		(h,w,l) = map_img.shape
		self.map_size_x = w  # cm
		self.map_size_y = h  # cm


		map_file = path+'new_map_loop'+str(lane)+'.txt'
		self.resolution = 1 #1px:1cm
		xy = np.array(list(path_parser.read_points(map_file)))-np.array([self.map_size_x/200.0, self.map_size_y/200.0])
		if flip:
			xy = np.flip(xy,axis=0)
		self.tree = KDTree(xy)
		self.len = len(xy)
	def findNearest(self,pt):
		i,d = self.findNearestIndex(pt)
		print(i)
		return(self.tree.data[i])
	def findNearestIndex(self,pt):
		pt = np.asarray(pt)
		dist,index = self.tree.query(pt)
		return (index, dist)
	def measureDistance(self,ptA,ptB):
		indexA,_ = self.findNearestIndex(ptA)
		indexB,_ = self.findNearestIndex(ptB)
		return ((indexB-indexA)%self.len)/100.0

def main():
	la = 0.5
	lane1 = LaneLine("cimat_reduced",1)
	vfc = VectorfieldController("cimat_reduced",1,str(int(100*la))+"cm")
	xs = []
	ys = []
	fails = 0
	for x_map in range(1,lane1.map_size_x,5):
		print(x_map)
		for y_map in range(1,lane1.map_size_y,5):
			x = x_map/100.0-lane1.map_size_x/200.0
			y = y_map/100.0-lane1.map_size_y/200.0
			_,i = lane1.tree.query([x,y])
			xs.append(lane1.tree.data[i,0])
			ys.append(lane1.tree.data[i,1])
			dx,dy = vfc.get_coords_from_vf(x,y)
			x2 = x+dx
			y2 = y+dy
			dist = lane1.measureDistance([x,y],[x2,y2])
			if abs(dist-la) > 0.1*la:
				print("------------")
				print(x,y)
				print(x2,y2)
				print(dist, la)
				print(lane1.measureDistance([x2,y2],[x,y]))
				print(i)	
				fails += 1	
	print(fails)
if __name__=='__main__':
	main()