#!/usr/bin/env python
import rospy
from common_msgs.msg import Mesgtype

def callback(msg):
    print "Sensor:", msg.timestamp.secs%100, "  주행 속도 | x:",msg.Speed.x," y:" msg.Speed.y," 각도:" msg.Speed.theta, "    주행 거리: ", msg.Distance

rospy.init_node('Algorithm')
sub = rospy.Subscriber('Algorithm_msg', Mesgtype, callback)
rospy.spin()
