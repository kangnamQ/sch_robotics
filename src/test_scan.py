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
        scan_data = []
        for n in range(360):
            scan_data.append(scan.ranges[n])
            print(f"{n}_th angle : ", scan.ranges[n])
        for i in range(len(scan_data)):
            if scan_data[i] < 0.3

        #초기 함수 설정, 3부분으로 나누어서 진행하려고 하기 떄문에 줄이 늘어났습니다.
        scan_front = []  # -20~20
        scan_fleft = []  # 20~75
        scan_left = []  # 75~105
        scan_fright = []  # -75~-20
        scan_right = []  # -105~-75

        #각 범위마다 각각에 리스트에 스캔값을 받습니다.
        for f in range(-20, 20):
            scan_front.append(scan.ranges[f])
        front = sum(scan_front) / len(scan_front)
        for fl in range(20, 75):
            scan_fleft.append(scan.ranges[fl])
        fleft = sum(scan_fleft) / len(scan_fleft)
        for l in range(75, 105):
            scan_left.append(scan.ranges[l])
        left = sum(scan_left) / len(scan_left)
        for fr in range(-75, -20):
            scan_fright.append(scan.ranges[fr])
        fright = sum(scan_fright) / len(scan_fright)
        for r in range(-105, -75):
            scan_right.append(scan.ranges[r])
        right = sum(scan_right) / len(scan_right)

        #주로 어디부분이 닿았는지 확인할 수 있는 print 문입니다. 확인을 위해 넣었습니다.
        if front < 0.2:
            print("front < 0.2 !!")
        if fleft < 0.2:
            print("fleft < 0.2 !!")
        if left < 0.2:
            print("left < 0.2 !!")
        if fright < 0.2:
            print("fright < 0.2 !!")
        if right < 0.2:
            print("right < 0.2 !!")

        if front < 0.3:
            print("front < 0.3 !!")
        if fleft < 0.3:
            print("fleft < 0.3 !!")
        if left < 0.3:
            print("left < 0.3 !!")
        if fright < 0.3:
            print("fright < 0.3 !!")
        if right < 0.3:
            print("right < 0.3 !!")

        if front < 0.4:
            print("front < 0.4 !!")
        if fleft < 0.4:
            print("fleft < 0.4 !!")
        if left < 0.4:
            print("left < 0.4 !!")
        if fright < 0.4:
            print("fright < 0.4 !!")
        if right < 0.4:
            print("right < 0.4 !!")

        if front < 0.5:
            print("front < 0.5 !!")
        if fleft < 0.5:
            print("fleft < 0.5 !!")
        if left < 0.5
            print("left < 0.5 !!")
        if fright < 0.5:
            print("fright < 0.5 !!")
        if right < 0.5:
            print("right < 0.5 !!")

        turtle_vel = Twist()
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
