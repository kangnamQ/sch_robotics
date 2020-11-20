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
    response = ServtypeResponse(risk_per = request.risk, stop1 = request.danger1, stop2 = request.danger2, stop3 = request.danger3)

    if response.stop1 == True:
        print "Risk is high!"
    if response.stop2 == True:
        print "Low battery!"
    if response.stop3 == True:
        print "Overheating!"
    if response.stop1 == True and response.stop2 == True and response.stop3 == True:
	print "Risk :", response.risk_per, "Danger! You should better Stop!!"

    return response



rospy.init_node('Algorithm')
sub = rospy.Subscriber('Msgs_msg', Mesgtype, callback)
service = rospy.Service('Status', Servtype, service_callback)
rospy.spin()
