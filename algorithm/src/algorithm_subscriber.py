#!/usr/bin/env python
import rospy
from common_msgs.msg import Mesgtype

def callback(msg):
    print(msg.Speed)
    print(msg.Distance)

rospy.init_node('Algorithm')
sub = rospy.Subscriber('Algorithm_msg', Mesgtype, callback)
rospy.spin()
