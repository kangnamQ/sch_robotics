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


while not rospy.is_shutdown():
    count += 1 

    msg.Runtime.data = count
    msg.Speed.x += 1
    msg.Speed.y += 1.5
    msg.Speed.z += 2
    msg.Distance.data = msg.Distance.data + msg.Speed.x + msg.Speed.y
    pub.publish(msg)

    battery_ -= 1.5
    heating_ += 2
    
    if battery_ <= 0 or heating_ >= 100:
        req = ServtypeRequest(battery = battery_, heating = heating_, danger1 = True, danger2 = True)
        res = requester(req)
        print "Danger! Turn off! | risk :", res.risk, "battery :", req.battery, "heat :", req.heating
        break

    elif battery_ <= 5 or heating_ >= 95:
        req = ServtypeRequest(battery = battery_, heating = heating_, danger1 = True, danger2 = True)
        res = requester(req)
        print "Danger! You should better Stop!! | risk :", res.risk, "battery :", req.battery, "heat :", req.heating
        
    elif battery_ <= 15:
        req = ServtypeRequest(battery = battery_, heating = heating_, danger2 = True)
        res = requester(req)
        print "Warning! Be careful! Low battery!  | risk :", res.risk, "battery :", req.battery

    elif heating_ >= 75:
        req = ServtypeRequest(battery = battery_, heating = heating_, danger1 = True)
        res = requester(req)
        print "Warning! Be careful! Overheating!  |risk :", res.risk, "heat :", req.heating

    else:
        req = ServtypeRequest(battery = battery_, heating = heating_, danger1 = False, danger2 = False)
        res = requester(req)

    

    print "Time :", msg.Runtime.data, "s"
    print "Speed | x :", msg.Speed.x, "| y :", msg.Speed.y, "| z :", msg.Speed.z
    print "Distance :", msg.Distance.data, "m"
    print ""
    rate.sleep()



