#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64
from geometry_msgs.msg import Vector3
from common_msgs.msg import Mesgtype

rospy.init_node('Sensor')
pub = rospy.Publisher('Sensor_msg', Mesgtype, queue_size=1)
msg = Mesgtype()
rate = rospy.Rate(1)
msg.topic_custom
msg.Speed.x = 0
msg.Speed.y = 0
msg.Speed.z = 0
msg.Distance = 0

while not rospy.is_shutdown():
    msg.timestamp = rospy.get_rostime()
    second = msg.timestamp.secs
    msg.Speed.x += 1
    msg.Speed.y += 1.5
    msg.Speed.z += 2
    msg.Distance = msg.Distance + msg.Speed.x + msg.Speed.y
    pub.publish(msg)

    print(msg.Speed)
    print(msg.Distance)
    rate.sleep()
