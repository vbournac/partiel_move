#! /usr/bin/env python

import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import math
from move_printer.srv import *
from std_msgs.msg import *

class print_tube_moveit:
  waypoints= []
  def __init__(self):
    print "============ Starting tutorial setup"
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('print_tube_moveit', anonymous=True)
    s=rospy.Service('print_tube', print_tube, self.move_to_position)
    self.extrusion_service = rospy.Publisher('/extrude', Bool, queue_size=100)

    self.group = moveit_commander.MoveGroupCommander("printer_group")
    self.group.set_pose_reference_frame("base_link")

    self.group.set_named_target('init_pose')
    self.group.go(wait=True)
    rospy.sleep(3)
#call service from terminal with rosservice call /print_tube ...

  def move_to_position(self, req):
	num_point =20
	# diameter = 0.1
	# height = 0.15
        diameter= req.diameter
        height = req.height
        extrusion = Bool()

        if((req.diameter > 0.245 or req.diameter<=0)  or (req.height>0.3 or req.height<=0)):
            return False

        extrusion.data= False
        self.extrusion_service.publish(extrusion)
	self.current_pose= self.group.get_current_pose().pose
	self.current_pose.position.z = 0.025
	self.waypoints.append(self.group.get_current_pose().pose)
        self.premiere_pose = geometry_msgs.msg.Pose()
        self.premiere_pose.position.x = diameter/2*math.cos(2*3.14/num_point)
        self.premiere_pose.position.y = diameter/2*math.sin(2*3.14/num_point)
        self.premiere_pose.position.z = 0.025+height/num_point
        self.waypoints.append(self.premiere_pose)

        (self.plan,self.fraction)=self.group.compute_cartesian_path(self.waypoints,0.01,1000)
    	self.group.execute(self.plan)
        self.waypoints=[]
        extrusion.data=True
        self.extrusion_service.publish(extrusion)

	for i in range(1, num_point):
        	for j in range(1, num_point):
			self.next_pose = geometry_msgs.msg.Pose()
			self.next_pose.position.x = diameter/2*math.cos(2*3.14*j/num_point)
			self.next_pose.position.y = diameter/2*math.sin(2*3.14*j/num_point)
			self.next_pose.position.z = 0.025+i*height/num_point
			self.waypoints.append(self.next_pose)



	(self.plan,self.fraction)=self.group.compute_cartesian_path(self.waypoints,0.01,1000)
	# rospy.sleep(3)
	self.group.execute(self.plan)
        extrusion.data = False
        self.extrusion_service.publish(extrusion)

	#print self.waypoints

	rospy.sleep(3)
        self.group.set_named_target('init_pose')
        self.group.go(wait=True)
        return(True)


if __name__ == '__main__':
    try:
	moveit=print_tube_moveit()

	# moveit.move_to_position()
	rospy.spin()
    except rospy.ROSInterruptException:
        pass
