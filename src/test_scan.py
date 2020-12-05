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

        #초기 함수 설정, 3부분으로 나누어서 진행하려고 하기 떄문에 줄이 늘어났습니다.
        scan_front = []  # -20~20
        scan_fleft = []  # 20~75
        scan_left = []  # 75~105
        scan_fright = []  # -75~-20
        scan_right = []  # -105~-75

        #각 범위마다 각각에 리스트에 스캔값을 받습니다.
        for f in range(-20, 20):
            scan_front.append(scan.ranges[f])
        for fl in range(20, 75):
            scan_fleft.append(scan.ranges[fl])
        for l in range(75, 105):
            scan_left.append(scan.ranges[l])
        for fr in range(-75, -20):
            scan_fright.append(scan.ranges[fr])
        for r in range(-105, -75):
            scan_right.append(scan.ranges[r])

        #주로 어디부분이 닿았는지 확인할 수 있는 print 문입니다. 확인을 위해 넣었습니다.
        if min(scan_front) < 0.5:
            print("scan_front < 0.5 !!")
        if min(scan_fleft) < 0.5:
            print("scan_fleft < 0.5 !!")
        if min(scan_left) < 0.5:
            print("scan_left < 0.5 !!")
        if min(scan_fright) < 0.5:
            print("scan_fright < 0.5 !!")
        if min(scan_right) < 0.5:
            print("scan_right < 0.5 !!")

        turtle_vel = Twist()

        #앞, 왼쪽, 오른쪽에 모두 벽이 있다면 돌면서 빈공간을 찾기 위한 함수입니다.
        if min(scan_front) < 0.3 and min(scan_fleft) < 0.5 and min(scan_fright) < 0.5:
            turtle_vel.linear.x = 0.0
            turtle_vel.angular.z = 1.0
            self.publisher.publish(turtle_vel)
            print("all wall! turn")
        #앞과 왼쪽에 장애물이 있을 경우 우회전을 합니다.
        elif min(scan_front) < 0.3 and min(scan_fleft)  :
            turtle_vel.linear.x = 1.0
            turtle_vel.angular.z = -1.0
            self.publisher.publish(turtle_vel)
            print("turn right!")
        #앞과 오른쪽에 장애물이 있을 경우 좌회전을 합니다.
        elif min(scan_front) < 0.3 and min(scan_fright)  :
            turtle_vel.linear.x = 1.0
            turtle_vel.angular.z = 1.0
            self.publisher.publish(turtle_vel)
            print("turn left!")
        #아무것도 하지 않을 때는 (일단 테스트라서) 정지하게끔 만들었습니다.
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