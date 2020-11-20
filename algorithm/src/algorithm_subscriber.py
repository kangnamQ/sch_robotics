#!/usr/bin/env python
import rospy
from common_msgs.msg import Mesgtype

def callback(msg):
    print "Time :", msg.timestamp.secs%100
    print "Speed | x :", msg.Speed.x, "| y :", msg.Speed.y, "| z :", msg.Speed.z
    print "Distance :", msg.Distance.data, "m"

rospy.init_node('Algorithm')
sub = rospy.Subscriber('Msgs_msg', Mesgtype, callback)
rospy.spin()
