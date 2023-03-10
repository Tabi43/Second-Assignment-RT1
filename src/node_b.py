#! /usr/bin/env python3

"""
.. module:: node_b
	:platform: Unix
	::synopsis: Python module for Second Assignment of RT1 course

.. moduleauthor:: Marco Tabita 4653859@studenti.unige.it

\details 

This node send a request to the service goal_info
then it print the response wich contains the number of 
target canceled and the number of target reached

Services:
	goal_info
"""

import rospy
import actionlib
import actionlib.msg
import Assignment_2.msg
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Twist, PoseStamped
from Assignment_2.msg import Info
import assignment_2_2022.msg
from Assignment_2.srv import target,targetResponse

def getInfoGoal():
	rospy.wait_for_service('goal_info')
	try:
		handle = rospy.ServiceProxy('goal_info', target)
		resp = handle()
		print("Target reached: ",resp.reached, "Target canceled: ", resp.canceled)
	except rospy.ServiceException as e:
		print("Service call failed: %s" % e)


if __name__ == "__main__":
    getInfoGoal()
