#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64
from geometry_msgs.msg import Vector3
from common_msgs.msg import Mesgtype
from common_msgs.srv import Servtype, ServtypeRequest


rospy.init_node('Sensor')
requester = rospy.ServiceProxy('Status', Servtype)

pub = rospy.Publisher('Msgs_msg', Mesgtype, queue_size=1)
msg = Mesgtype()
rate = rospy.Rate(1)
msg.Speed.x = 0
msg.Speed.y = 0
msg.Speed.z = 0
msg.Distance.data = 0

count = 0
battery_ = 100.0
heating_ = 0.0

req = ServtypeRequest(battery = battery_, heating = heating_, danger1 = False, danger2 = False)
req = res = requester(req)
print "status | battery :", battery_, "heating_ :", heating_


while not rospy.is_shutdown():
    count += 1 

    msg.Runtime.data = count
    msg.Speed.x += 1
    msg.Speed.y += 1.5
    msg.Speed.z += 2
    msg.Distance.data = msg.Distance.data + msg.Speed.x + msg.Speed.y
    pub.publish(msg)

    battery_ -= 2.5
    heating_ += 3
    
    if battery_ <= 20 and heating_ >= 80:
        req = ServtypeRequest(battery = battery_, heating = heating_, danger1 = True, danger2 = True)
        res = requester(req)
        print "Danger! You should better Stop!! | risk :", res.risk, "battery :", req.battery, "heat :", req.heating 

    if battery_ <= 20:
        req = ServtypeRequest(battery = battery_, heating = heating_, danger2 = True)
        res = requester(req)
        print "Low battery!  | risk :", res.risk, "battery :", req.battery
            
    if heating_ >= 80:
        req = ServtypeRequest(battery = battery_, heating = heating_, danger1 = True)
        res = requester(req)
        print "Overheating!  |risk :", res.risk, "heat :", req.heating


    print "Time :", msg.Runtime.data, "s"
    print "Speed | x :", msg.Speed.x, "| y :", msg.Speed.y, "| z :", msg.Speed.z
    print "Distance :", msg.Distance.data, "m"
    print ""
    rate.sleep()



