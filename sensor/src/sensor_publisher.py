#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64
from geometry_msgs.msg import Vector3
from common_msgs.msg import Mesgtype

rospy.init_node('Sensor')
pub = rospy.Publisher('Sensor_msg', Mesgtype, queue_size=1)
msg = Mesgtype()
rate = rospy.Rate(1)
while not rospy.is_shutdown():
    msg.timestamp = rospy.get_rostime()
    second = msg.timestamp.secs
    msg.Speed = Vector3(x=second/10, y=second/7, theta=second/5)
    msg.Distance = Float64(msg.Speed.x+msg.Speed.y)    
    pub.publish(msg)
    print "Sensor:", msg.timestamp.secs%100, "  주행 속도 | x:",msg.Speed.x," y:" msg.Speed.y," 각도:" msg.Speed.theta, "    주행 거리: ", msg.Distance
    rate.sleep()d
