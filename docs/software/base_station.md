# Base Station
## Launch files
### Fake_GPS
```
roslaunch fake_gps fake_gps.launch [upcam_id:=0] [cam_port:=0] [resolution:=720p] [debug_lvl:=0] [calib_file=calibration.yaml]
```

- Nodes
	- [multicam_fake_gps](#Multicam_Fake_GPS)

### Map_Publisher
```
roslaunch map_publisher robotics_lab.launch
```

### Network
```
roslaunch vehicular_communication network.launch debug:=True [latency=0.1] [cluster_time_window:=2.0] [cluster_eps:=0.1] [cluster_min:=5] [cluster_rate:=2.0]
```
- Launch files
	- [map_publisher](#Map_Publisher)
- Nodes
	- [vehicular_network](#Vehicular_Network)
	- [sensor_sharing](#Sensor_Sharing)

## Nodes
### Multicam_Fake_GPS

|Topic	|	Type|Msg type|
| ---	|	---	|	---	|
|/fake_gps/ego_pose_raw/*<car_id>*|Publisher|geometry_msgs/PoseWithCovarinceStamped|
|/sensors/global_camera_*<upcam_id>*/marks_corners|Publisher|donkietown_msgs/MarkerEdgeArray|

### Vehicular_Network

|Topic	|	Type|Msg type|
| ---	|	---	|	---	|
|/v2x/CAM/*<car_id>*/rx|Publisher|donkietown_msgs/CooperativeAwarenessMessage|
|/v2x/CAM/pool|Subscriber|donkietown_msgs/CooperativeAwarenessMessage|

### Sensor_Sharing
|Topic	|	Type|Msg type|
| ---	|	---	|	---	|
|/v2x/sensors/obstacles/filtered|Publisher|sensor_msgs/PointCloud|
|/v2x/sensors/obstacles/pool|Publisher|sensor_msgs/PointCloud|
|/v2x/sensors/obstacles/raw|Subscriber|sensor_msgs/PointCloud|