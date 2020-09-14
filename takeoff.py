import numpy as np
from geometry_msgs.msg import PoseStamped,TwistStamped,PositionTarget
from mavros_msgs.srv import CommandBool, SetMode
from mavros_msgs.msg import State 
from std_msgs.msg import Int32MultiArray,MultiArrayDimension
import rospy

pi=3.14
	
def state_cb(state):
	global current_state
	current_state = state
	print("state")
	arming_client(True)
	set_mode_client(base_mode=0, custom_mode="OFFBOARD")
def move_cb(msg):
	pos = TwistStamped()	#MESSEGE FOR CURRENT SETPOINT

	pos.twist.linear.x =msg.data[0]	
	pos.twist.linear.y =msg.data[1]
	pos.twist.linear.z =msg.data[2]
	publis.publish(pos)

def setOffboardMode(self):

		rospy.wait_for_service('mavros/set_mode')
		try:
			flightModeService = rospy.ServiceProxy('mavros/set_mode', mavros_msgs.srv.SetMode)
			flightModeService(custom_mode='OFFBOARD')
			print("ENTERING OFFBOARD MODE")

		except (rospy.ServiceException, e):
			
			print ("service set_mode call failed: %s. Offboard Mode could not be set."%e)

def setArm(self):

		rospy.wait_for_service('mavros/cmd/arming')
		try:
			armService = rospy.ServiceProxy('mavros/cmd/arming', mavros_msgs.srv.CommandBool)
			armService(True)
		except (rospy.ServiceException, e):
			print ("Service arming call failed: %s"%e)

rospy.init_node("scanner")
#rospy.Rate(20)

rospy.Subscriber('/mavros/state', State, state_cb)

arming_client = rospy.ServiceProxy('/mavros/cmd/arming', CommandBool)
set_mode_client = rospy.ServiceProxy('/mavros/set_mode', SetMode) 

rospy.Subscriber('/mavros/state', State, move_cb)
publis = rospy.Publisher('/mavros/setpoint_velocity/cmd_vel', TwistStamped, queue_size=10)
current_state = State() #DECLARE VARIABLE FOR CURRENT STATE


rospy.wait_for_message('/mavros/state', State)

if not current_state.armed:
	print("CURRENTLY NOT ARMED")
	arming_client(True)
	print("NOW ARMED")

if current_state.mode != "OFFBOARD":
	print("MODE IS NOT OFFBOARD")
	set_mode_client(base_mode=0, custom_mode="OFFBOARD")
	print("MODE CHANGED TO OFFBOARD")

while not rospy.is_shutdown():
	#print("Pub")
	#publis.publish(pos)
	rospy.wait_for_message('/mavros/state', State)
	if not current_state.armed:
		#print("CURRENTLY NOT ARMED")
		arming_client(True)
		#print("NOW ARMED")

	if current_state.mode != "OFFBOARD":
		#print("MODE IS NOT OFFBOARD")
		set_mode_client(base_mode=0, custom_mode="OFFBOARD")
		#print("MODE CHANGED TO OFFBOARD")
	rospy.spin()