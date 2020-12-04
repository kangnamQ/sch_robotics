#!/home/pi/.pyenv/versions/rospy3/bin/python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class SelfDrive:
    def __init__(self, publisher):
        self.publisher = publisher
        self.count = 30

    def lds_callback(self, scan):
        # scan 분석 후 속도 결정
        # ...
        left_scan_30 = 0
        for i in range(30):
            # print(f"{i}_th angle : ", scan.ranges[i])
            left_scan_30 += scan.ranges[i]
        mean_left_scan_30 = left_scan_30 / 30
        print("sum of left scan : ", left_scan_30)
        print("mean of left scan : ", mean_left_scan_30)
        turtle_vel = Twist()

        if mean_left_scan_30 < 0.4:
            turtle_vel.angular.z = -2.0
            turtle_vel.linear.x = 0.0
            self.publisher.publish(turtle_vel)

        else:
            turtle_vel.linear.x = 0.15
            self.publisher.publish(turtle_vel)
            # turtle_vel.angular.z = 1
        # 속도 출력


def main():
    rospy.init_node('self_drive')
    publisher = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    driver = SelfDrive(publisher)
    subscriber = rospy.Subscriber('scan', LaserScan,
                                  lambda scan: driver.lds_callback(scan))
    rospy.spin()

if __name__ == "__main__":
    main()
