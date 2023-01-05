# Asinus Cars
## Launch files

### Core
```
roslaunch asinus_car core.launch car_id:=*<car_id>* [heart_rate:=25]
```
- Nodes
	- [asinus_car node](#Asinus_Car)

### DonkieNet
```
roslaunch ros_deep_learning donkienet.ros1.launch [debug:=False]
```
- Nodes
	- [detectnet node](#Detectnet)
	- [video_source node](#Video_Source)

### Obstacle_Localization
```
roslaunch asinus_car obstacle_localization.launch car_id:=*<car_id>* [debug:=False]
```
- Launch files
	- [donkienet](#DonkieNet)
	- road_context/obstacle_localization

### Prime
```
roslaunch asinus_car prime.launch car_id:=*<car_id>* [heart_rate:=25]
```
- Launch files
	- [core](#Core)
	- [obstacle_localization](#Obstacle_Localization)

## Nodes
### Asinus_Car

|Topic	|	Type|Msg type|
| ---	|	---	|	---	|
|/asinus_cars/*<car_id>*/camera/pose|Publisher|geometry_msgs/PoseStamped|
|/asinus_cars/*<car_id>*/camera/camera_info|Publisher|sensor_msgs/CameraInfo|
|/asinus_cars/*<car_id>*/motors_raw_data|Publisher|donkietown_msgs/MotorsState|
|/asinus_cars/*<car_id>*/filtered_pose|Publisher|geometry_msgs/PoseWithCovarinceStamped|
|/asinus_cars/*<car_id>*/motors_driver|Subscriber|donkietown_msgs/MotorsSpeed|
|/fake_gps/ego_pose_raw/*<car_id>*|Subscriber|geometry_msgs/PoseWithCovarinceStamped|

### Detectnet
|Topic	|	Type|Msg type|
| ---	|	---	|	---	|
|/asinus_cars/*<car_id>*/camera/pose|Publisher|geometry_msgs/PoseStamped|
|/asinus_cars/*<car_id>*/camera/camera_info|Publisher|sensor_msgs/CameraInfo|
|/asinus_cars/*<car_id>*/motors_raw_data|Publisher|donkietown_msgs/MotorsState|
|/asinus_cars/*<car_id>*/filtered_pose|Publisher|geometry_msgs/PoseWithCovarinceStamped|
|/asinus_cars/*<car_id>*/motors_driver|Subscriber|donkietown_msgs/MotorsSpeed|
|/fake_gps/ego_pose_raw/*<car_id>*|Subscriber|geometry_msgs/PoseWithCovarinceStamped|

### Video_Source
|Topic	|	Type|Msg type|
| ---	|	---	|	---	|
|/asinus_cars/*<car_id>*/video_source/raw|Publisher|sensor_msgs/Image|