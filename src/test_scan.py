#!/home/pi/.pyenv/versions/rospy3/bin/python

import rospy
from geometry_msgs.msg import Twist  # move wheel
from sensor_msgs.msg import LaserScan  # sacn
import numpy as np

# laserscan data -> Twist -> robot move

class SelfDrive:
    def __init__(self, publisher):
        self.publisher = publisher
        self.count = 30

    def lds_callback(self, scan):
        # scan 분석 후 속도 결정
        # ...
        left_scan_30 = 0
        scan_data = np.array([])
        for n in range(360):
            scan_data = np.append(scan_data, np.array(scan.ranges[n]))
            print(f"{n}_th angle : ", scan.ranges[n])

        scan_fleft = []     #0~30
        scan_fright = []    #-30~0
        scan_left = []      #30~60
        scan_right = []     #-60~-30
        scan_front = []     #-15~15

        for fl in range(0,30):
            scan_fleft = np.append(scan_fleft, np.array(scan.ranges[fl]))
        for l in range(30,60):
            scan_left = np.append(scan_left, np.array(scan.ranges[l]))
        for fr in range(-30,0):
            scan_fright = np.append(scan_fright, np.array(scan.ranges[fr]))
        for r in range(-60,-30):
            scan_right = np.append(scan_right, np.array(scan.ranges[r]))
        for f in range(-15,15):
            scan_front = np.append(scan_front, np.array(scan.ranges[r]))

        if np.min(scan_front) < 2:
            print("scan_front < 2 !!")
        if np.min(scan_fleft) < 2:
            print("scan_fleft < 2 !!")
        if np.min(scan_left) < 2:
            print("scan_left < 2 !!")
        if np.min(scan_fright) < 2:
            print("scan_fright < 2 !!")
        if np.min(scan_right) < 2:
            print("scan_right < 2 !!")

        turtle_vel = Twist()

	turtle_vel.linear.x=0.0
	turtle_vel.angular.z=0.0
	self.publisher.publish(turtle_vel)
	

        # 속도 출력


def main():
    rospy.init_node('Final_Project')
    publisher = rospy.Publisher('cmd_vel', Twist, queue_size=1)  # It's already fixed.
    driver = SelfDrive(publisher)
    subscriber = rospy.Subscriber('scan', LaserScan,
                                  lambda scan: driver.lds_callback(scan))
    rospy.spin()


if __name__ == "__main__":
    main()
