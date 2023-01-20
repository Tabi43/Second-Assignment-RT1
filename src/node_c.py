#! /usr/bin/env python3

import rospy
import actionlib
import actionlib.msg
import Assignment_2.msg
import math
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Twist, PoseStamped
from Assignment_2.msg import Info
import assignment_2_2022.msg
from Assignment_2.srv import target,targetResponse

global avg_vx, avg_vy, n_samp


def clbk_info(msg):
	global rx,ry,avg_vx, avg_vy, n_samp, rate, distance
	
	distance = math.sqrt(pow((rx - msg.x),2)+pow((ry - msg.x),2))
	n_samp = n_samp + 1
	avg_vx = (avg_vx + msg.vel_x)/n_samp
	avg_vy = (avg_vy + msg.vel_y)/n_samp
	
	
def clbk_tgt(msg):
	global rx, ry

	rx = msg.x 
	ry = msg.y 

def main():
	global rx,ry, rate, n_samp ,avg_vx, avg_vy, distance
	
	n_samp = 0
	rx = 0
	ry = 0
	avg_vx = 0
	avg_vy = 0
	distance = 0
	
	#Init node
	rospy.init_node('node_c')
	
	#get value from the param
	freq = rospy.get_param("freq_c")	
	rate = rospy.Rate(freq)
	
	#Subscribe to /bot_info
	sub_info = rospy.Subscriber('/bot_info', Info, clbk_info)
	sub_tgt = rospy.Subscriber('/tgt', Point, clbk_tgt)
	
	while True:		
		print("Average Vx: ", float(f'{avg_vx:.4f}') ," Vy:", float(f'{avg_vy:.4f}'), "distance: ", float(f'{distance:.2f}'))	
		rate.sleep()

	
	rospy.spin()
	
if __name__ == "__main__":
    main()
