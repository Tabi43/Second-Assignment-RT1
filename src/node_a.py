#! /usr/bin/env python3

"""
.. module:: node_a
    :platform: Unix
    :synopsis: Python module for Second Assignment of RT1 course
    
.. moduleauthor:: Marco Tabita 4653859@studenti.unige.it

\details

This node implement an action client allowing an user to set a target(x,y) or to cancel it
at any time. This node also publish the robot position and velocity as a custom message by reling on 
the topic /odom.   

Subscribes to: 
	/odom

Publish to:
	/bot_info
	/tgt

Services:
	goal_info
"""

import sys
import rospy
import select
import actionlib
import time
import actionlib.msg
import Assignment_2.msg
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Twist, PoseStamped
from Assignment_2.msg import Info
from Assignment_2.srv import target,targetResponse
import assignment_2_2022.msg

#Global variables
pose_ = Pose()
twist_ = Twist()
	
def clbk_odom(msg):
	"""
		Callback function to publish the desired information 
		taken from /odom.

		Args:
		msg(Odometry): It contains the odometry of the robot
	"""
	global pub_info
	
	x_ = msg.pose.pose.position.x
	y_ = msg.pose.pose.position.y
	vx_ = msg.twist.twist.linear.x
	vy_ = msg.twist.twist.linear.y
	
	msg_info = Info()
	
	msg_info.x = x_
	msg_info.y = y_
	msg_info.vel_x = vx_
	msg_info.vel_y = vy_
	
	if not rospy.is_shutdown():
		pub_info.publish(msg_info)
		
	
def getCordinatesFromConsole():		
	"""
		Function that ask to the user a new 
		targhet. It check if the input given is valid.
	"""
	print("Set a new target:")
	while True:
		try:
			x = float(input("x = "))
		except:
			print("Please enter a valid number")			
		else:
			break
	while True:
		try:
			y = float(input("y = "))
		except:
			print("Please enter a valid number")			
		else:			
			break	
	return x,y
	
def ltk_tgt(x, y):
	"""
		Function to publish on /tgt the new target.

		Args:
		x(float) : x position of the new target
		y(float) : y position of the new target
	"""
	global pub_target
	
	target = Point()
	
	target.x = x
	target.y = y	
	target.z = 0
	
	pub_target.publish(target)

def get_info_goal(req):
	"""
		Callback function to return as response the number of 
		traget reached and the one of target canceled.

		Args:
		req(target): the service's request it does not contain nothing actually.
	"""
	global target_reached, target_canceled, service 
	
	return targetResponse(target_reached, target_canceled)
	

def main():
	global pub_info, target_reached, target_canceled, service, pub_target

	#Initialization of elements
	pose = PoseStamped()
	target_reached = 0
	target_canceled = 0
	
	#Init node
	rospy.init_node('node_a')
	
	#Create a new client
	client = actionlib.SimpleActionClient('/reaching_goal', assignment_2_2022.msg.PlanningAction)
	
	#Publish
	pub_info = rospy.Publisher('/bot_info', Info, queue_size=1)	
	pub_target = rospy.Publisher('/tgt', Point, queue_size=1)
	
	#Subscribe
	sub_odom = rospy.Subscriber('/odom', Odometry, clbk_odom)	
	service = rospy.Service('goal_info',target, get_info_goal)
	
	#Wait for the server ready
	client.wait_for_server()
		
	while True:
		p = getCordinatesFromConsole()
		
		ltk_tgt(p[0],p[1])
		pose.pose.position.x = p[0];
		pose.pose.position.y = p[1];
		pose.pose.position.z = 0;
		
		#Create the object PlanningGoal and assign the position goal
		goal = assignment_2_2022.msg.PlanningGoal(target_pose = pose)
			
		#Send the goal request
		client.send_goal(goal)
				
		finished = False
		print("Do you wanna cancel this target ? (Y/N)")
		while not finished:						
			input = select.select([sys.stdin], [], [], 1)[0]
			if input:
				res = sys.stdin.readline().rstrip()	
				if res == 'Y' or res == 'y' or res == 'yes':
					finished = True					
					client.cancel_goal()						
			else:
				#Check of the state 	
				time.sleep(1)		
				state = client.get_state()
				if(state != 1 and state != 0):
					print("Targhet reachedd!") 				
					finished = True 
		
		time.sleep(1)
		state = client.get_state()
		if(state == 2):
			#Preempted task
			target_canceled = target_canceled + 1
		elif(state == 3):
			#Task completed
			target_reached = target_reached + 1
		else:
			printf("Error...")
		
		print("Target R: ",target_reached," C: ",target_canceled)		
		
if __name__ == "__main__":
    main()
