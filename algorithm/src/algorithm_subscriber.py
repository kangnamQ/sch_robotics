#!/usr/bin/env python
import rospy
from common_msgs.msg import Mesgtype
from common_msgs.srv import Servtype, ServtypeResponse

def callback(msg):
    print "Time :", msg.timestamp.secs%100
    print "Speed | x :", msg.Speed.x, "| y :", msg.Speed.y, "| z :", msg.Speed.z
    print "Distance :", msg.Distance.data, "m"
    print ""

def service_callback(request)
    response = ServtypeResponse(risk_per = request.risk, stop1 = request.danger1, stop2 = request.danger2, stop3 = request.danger3)

    if response.stop1 == True:
        print "위험도가 너무 높습니다."
    elif response.stop2 == True:
        print "전력이 부족합니다."
    elif response.stop3 == True:
        print "과열되었습니다."
    elif response.stop1 == True and response.stop2 == True and response.stop3 == True
	print "위험정도 :" risk_per, "위험합니다. 작동을 중지하시는 것을 권장합니다!"

    return response



rospy.init_node('Algorithm')
sub = rospy.Subscriber('Msgs_msg', Mesgtype, callback)
service = rospy.Service('Status', Service, service_callback)
rospy.spin()
