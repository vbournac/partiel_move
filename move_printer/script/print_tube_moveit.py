#! /usr/bin/env python

import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import math
from move_printer.srv import *

class print_tube_moveit:
  waypoints= []
  def __init__(self):
    print "============ Starting tutorial setup"
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('print_tube_moveit', anonymous=True)


    self.group = moveit_commander.MoveGroupCommander("printer_group")
    self.group.set_pose_reference_frame("base_link")

    self.group.set_named_target('init_pose')
    self.group.go(wait=True)

    #self.pose_A = geometry_msgs.msg.Pose()
    #self.pose_A .position.x = 0.05
    #self.pose_A.position.y = 0.0
    #self.pose_A.position.z = -0.2

    #self.pose_B = geometry_msgs.msg.Pose()
    #self.pose_B .position.x = 0.0
    #self.pose_B.position.y = 0.05
    #self.pose_B.position.z = -0.2

    #self.pose_C = geometry_msgs.msg.Pose()
    #self.pose_C .position.x = -0.05
    #self.pose_C.position.y = 0.0
    #self.pose_C.position.z = -0.2

    #self.pose_D = geometry_msgs.msg.Pose()
    #self.pose_D .position.x = 0.0
    #self.pose_D.position.y = -0.05
    #self.pose_D.position.z = -0.2

    rospy.sleep(3)

  def move_to_position(self):

	# self.waypoints.append(self.pose_A)
	# self.waypoints.append(self.pose_B)
	# self.waypoints.append(self.pose_C)
	# self.waypoints.append(self.pose_D)
	num_point =10
	diameter = 0.1
	height = 0.15
	
	self.current_pose= self.group.get_current_pose().pose
	self.current_pose.position.z = -0.2
	self.waypoints.append(self.group.get_current_pose().pose)
	
	for i in range(1, num_point):
        	for j in range(1, num_point):
			self.next_pose = geometry_msgs.msg.Pose()
			self.next_pose.position.x = diameter/2*math.cos(2*3.14*j/num_point)
			self.next_pose.position.y = diameter/2*math.sin(2*3.14*j/num_point)
			self.next_pose.position.z = -0.2+i*height/num_point
			self.waypoints.append(self.next_pose)



	(self.plan,self.fraction)=self.group.compute_cartesian_path(self.waypoints,0.01,1000)
	rospy.sleep(3)
	self.group.execute(self.plan)
	#print self.waypoints

	rospy.sleep(3)


if __name__ == '__main__':
    try:
	moveit=print_tube_moveit()
	moveit.move_to_position()
	rospy.spin()
    except rospy.ROSInterruptException:
        pass
