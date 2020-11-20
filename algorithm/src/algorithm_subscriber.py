#!/usr/bin/env python
import rospy
from common_msgs.msg import Mesgtype
from common_msgs.srv import Servtype, ServtypeResponse

def callback(msg):
    print "Time :", msg.Runtime.data, "s"
    print "Speed | x :", msg.Speed.x, "| y :", msg.Speed.y, "| z :", msg.Speed.z
    print "Distance :", msg.Distance.data, "m"
    print ""

def service_callback(request):
    response = ServtypeResponse(risk = request.heating/10 + (100-request.battery), stop1 = request.danger1 == True and request.danger2 == True)

    if response.stop1 == True:
        print "Danger! You should better Stop!! | risk :", response.risk, "battery :", request.battery, "heat :", request.heating

    elif response.risk >= 60:
        print "Warning! Be careful! | risk :", response.risk, "battery :", request.battery, "heat :", request.heating 

    return response


rospy.init_node('Algorithm')
sub = rospy.Subscriber('Msgs_msg', Mesgtype, callback)
service = rospy.Service('Status', Servtype, service_callback)
rospy.spin()
