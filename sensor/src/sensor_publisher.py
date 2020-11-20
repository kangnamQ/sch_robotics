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
battery_ = 100
heating_ = 0
risk_ = 0

req = ServtypeRequest(battery = battery_, heating = heating_, risk = risk_, danger1 = False, danger2 = False, danger3 = False)
req = res = requester(req)
print "status | battery :", battery_, "heating_ :", heating_, "risk :", risk_


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
    risk_ = heating_/10 + (100-battery_)
    

    if risk_ >= 80 and battery_ <=20 and heating_ >= 80:
        req = ServtypeRequest(battery = battery_, heating = heating_, risk = risk_, danger1 = True, danger2 = True, danger3 = True)
	res = requester(req)
        print "Danger! You should better Stop!! | battery :", req.battery, "heat :", req.heating, "risk :", req.risk

    if battery_ <= 20:
        req = ServtypeRequest(battery = battery_, heating = heating_, risk = risk_, danger2 = True)
        res = requester(req)
        print "Low battery!  | battery :", req.battery
            
    if risk_ >= 80:
        req = ServtypeRequest(battery = battery_, heating = heating_, risk = risk_, danger1 = True)
        res = requester(req)
        print "Risk is high!  | risk :", req.risk
        

    if heating_ >= 80:
        req = ServtypeRequest(battery = battery_, heating = heating_, risk = risk_, danger3 = True)
        res = requester(req)
        print "Overheating!  | heat :", req.heating


    print "Time :", msg.Runtime.data, "s"
    print "Speed | x :", msg.Speed.x, "| y :", msg.Speed.y, "| z :", msg.Speed.z
    print "Distance :", msg.Distance.data, "m"
    print ""
    rate.sleep()



