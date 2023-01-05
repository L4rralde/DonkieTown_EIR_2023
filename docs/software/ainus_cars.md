# Asinus Cars
## Nodos
Nodo core
```
roslaunch asinus_car  car_id:=<aruco_id>
```

|Tópico	|	Tipo|Tipo de Mensaje|
| ---	|	---	|	---	|
|/asinus_cars/*<car_id>*/camera/pose|Publisher|geometry_msgs/PoseStamped|
|/asinus_cars/*<car_id>*/camera/camera_info|Publisher|sensor_msgs/CameraInfo|
|/asinus_cars/*<car_id>*/motors_raw_data|Publisher|donkietown_msgs/MotorsState|
|/asinus_cars/*<car_id>*/filtered_pose|Publisher|geometry_msgs/PoseWithCovarinceStamped|
|/asinus_cars/*<car_id>*/motors_driver|Subscriber|donkietown_msgs/MotorsSpeed|
|/fake_gps/ego_pose_raw/*<car_id>*|Subscriber|geometry_msgs/PoseWithCovarinceStamped|