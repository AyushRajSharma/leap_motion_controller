from leap_motion.msg import Human
from geometry_msgs.msg import Twist,PoseStamped
from mavros_msgs.srv import CommandBool, SetMode
from mavros_msgs.msg import State 
import rospy

rospy.init_node("scanner")
rospy.Rate(1)
pi=3.14

arming_client = rospy.ServiceProxy("mavros/cmd/arming", CommandBool)
set_mode_client = rospy.ServiceProxy('mavros/set_mode', SetMode) 
pub = rospy.Publisher('/mavros/setpoint_velocity/cmd_vel_unstamped', Twist, queue_size=10)
pub_pose = rospy.Publisher('/mavros/setpoint_position/local', PoseStamped, queue_size=10)

loc_pos = PoseStamped()
loc_pos.pose.position.x = 0
loc_pos.pose.position.y = 0
loc_pos.pose.position.z = 1

for i in range(0,100,1):
	pub_pose.publish(loc_pos)
# ABOVE -- GIVING LOCAL SETPOINTS TO DRONE
def state_cb(state):

	#print("state")
	arming_client(True)
	set_mode_client(base_mode=0, custom_mode="OFFBOARD")

def callback_leap(msg):

	print("callback")
	global fr_bk,lt_rt

	roll = msg.right_hand.roll*180/pi #LEFT_HAND DATA TYPE = HAND
	pitch = msg.right_hand.pitch*180/pi
	#yaw = msg.right_hand.yaw*180/pi

	roll_l = msg.left_hand.roll*180/pi #LEFT_HAND DATA TYPE = HAND
	pitch_l = msg.left_hand.pitch*180/pi
	#yaw_l = msg.left_hand.yaw*180/pi

	try:
		w =msg.left_hand.sphere_center[1]
	except:
		w=0.1
	#print(type(w))
	print(w)

	fr_bk = (abs(pitch)>20)*((pitch>0)*2-1)
	lt_rt = (abs(roll)>20)*((roll>0)*2-1)
	up_dn = (abs(pitch_l)>20)*((pitch_l>0)*2-1)
	#lt_rt = (abs(roll_l)>20)*((roll_l>0)*2-1)

	print(lt_rt,fr_bk,up_dn)#TEST IF RETURNED VARIABLE IS 1 OR TRUE
	move(lt_rt,fr_bk,up_dn)

def move(lt_rt,fr_bk,up_dn):
	vel = Twist()
	vel.linear.x = fr_bk
	vel.linear.y = lt_rt
	vel.linear.z = up_dn

	#print("Pub")
	pub.publish(vel)

rospy.Subscriber('/leap_motion/leap_filtered',Human,callback_leap)
rospy.Subscriber('/mavros/state', State, state_cb)

#arming_client(True)
#set_mode_client(base_mode=0, custom_mode="OFFBOARD")
print("start")
while (not rospy.is_shutdown()):

#	print("arm")	
	rospy.spin()