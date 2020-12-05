#!/home/pi/.pyenv/versions/rospy3/bin/python

import rospy
from geometry_msgs.msg import Twist  # move wheel
from sensor_msgs.msg import LaserScan  # sacn


# laserscan data -> Twist -> robot move

class SelfDrive:
    def __init__(self, publisher):
        self.publisher = publisher
        self.count = 30

    def lds_callback(self, scan):
        # scan 분석 후 속도 결정
        # ...
        left_scan_30 = 0
        scan_data = []
        for n in range(360):
            scan_data.append(scan.ranges[n])
            print(f"{n}_th angle : ", scan.ranges[n])

        scan_fleft = []  # 0~30
        scan_fright = []  # -30~0
        scan_left = []  # 30~60
        scan_right = []  # -60~-30
        scan_front = []  # -15~15

        for fl in range(0, 30):
            scan_fleft.append(scan.ranges[fl])
        for l in range(30, 60):
            scan_left.append(scan.ranges[l])
        for fr in range(-30, 0):
            scan_fright.append(scan.ranges[fr])
        for r in range(-60, -30):
            scan_right.append(scan.ranges[r])
        for f in range(-15, 15):
            scan_front.append(scan.ranges[f])

        if min(scan_front) < 2:
            print("scan_front < 2 !!")
        if min(scan_fleft) < 2:
            print("scan_fleft < 2 !!")
        if min(scan_left) < 2:
            print("scan_left < 2 !!")
        if min(scan_fright) < 2:
            print("scan_fright < 2 !!")
        if min(scan_right) < 2:
            print("scan_right < 2 !!")

        turtle_vel = Twist()

        if min(scan_front) < 2:
            turtle_vel.linear.x = 2.0
            turtle_vel.angular.z = 0.0
            self.publisher.publish(turtle_vel)

        else:
            turtle_vel.linear.x = 0.0
            turtle_vel.angular.z = 0.0
            self.publisher.publish(turtle_vel)


def main():
    rospy.init_node('Final_Project')
    publisher = rospy.Publisher('cmd_vel', Twist, queue_size=1)  # It's already fixed.
    driver = SelfDrive(publisher)
    subscriber = rospy.Subscriber('scan', LaserScan,
                                  lambda scan: driver.lds_callback(scan))
    rospy.spin()


if __name__ == "__main__":
    main()
