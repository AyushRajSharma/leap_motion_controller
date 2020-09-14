# leap_motion_controller
Control a Drone with leap motion controller to detect gesture and control a drone

The software packages used were :
  Leap motion Ros (https://github.com/warp1337/rosleapmotion)
  ROS Python package (if not installed, type command: pip3 install rospy )
  Gazebo for simulation 
 
 Hardware Used:
  Pixhawk 4 flight controller
  Leap motion hand gesture detector
 
How to use it :
  roslaunch custom.launch
  python3 takeoff.py
  python3 leap.py
  
The controller was unstable in real world so it was mostly used in simulation.
