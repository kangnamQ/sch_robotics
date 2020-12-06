#!/home/pi/.pyenv/versions/rospy3/bin/python

import rospy
from geometry_msgs.msg import Twist  # move wheel
from sensor_msgs.msg import LaserScan  # sacn
# laserscan data -> Twist -> robot move

class SelfDrive:
    def __init__(self, publisher):
        self.publisher = publisher

    def lds_callback(self, scan):
        # 0.3 이하인 부분을 탐지하여 터미널에 띄워줍니다.
        scan_data = []
        for n in range(-105,106):
            scan_data.append(scan.ranges[n])
            if scan.ranges[n] < 0.3
                print(f"{n}_th angle < 0.3 : ", scan.ranges[n])

        #초기 함수 설정, 3부분으로 나누어서 진행하려고 하기 떄문에 줄이 늘어났습니다.
        scan_front = []  # -20~20
        scan_fleft = []  # 20~75
        scan_left = []  # 75~105
        scan_fright = []  # -75~-20
        scan_right = []  # -105~-75

        #각 범위마다 각각에 리스트에 스캔값을 받고 평균을 구합니다.
        for f in range(-20, 20):
            scan_front.append(scan.ranges[f])
        front = sum(scan_front) / len(scan_front)
        for fl in range(20, 75):
            scan_fleft.append(scan.ranges[fl])
        fleft = sum(scan_fleft) / len(scan_fleft)
        for l in range(75, 106):
            scan_left.append(scan.ranges[l])
        left = sum(scan_left) / len(scan_left)
        for fr in range(-75, -20):
            scan_fright.append(scan.ranges[fr])
        fright = sum(scan_fright) / len(scan_fright)
        for r in range(-105, -75):
            scan_right.append(scan.ranges[r])
        right = sum(scan_right) / len(scan_right)

        turtle_vel = Twist()
        #모두 막혔을 경우 그냥 나갈 수 있는 구멍을 탐지할 때까지 왼쪽으로 돈다.
        if front < 0.2 and left < 0.2 and right < 0.2:
            turtle_vel.linear.x = 0.0
            turtle_vel.angular.z = 2.0  # + => turn left / - => turn right
            self.publisher.publish(turtle_vel)
            print("left will have wall! turn right!")
        #만약 앞과 왼쪽에 뭔가 있을 경우 오른쪽으로 돈다. 이경우 왼쪽에는 아무것도 없어야 한다.
        elif front < 0.2 and left < 0.3 and right > 0.3:
            turtle_vel.linear.x = 0.0
            turtle_vel.angular.z = -2.0  # + => turn left / - => turn right
            self.publisher.publish(turtle_vel)
            print("left will have wall! turn right!")
        #만약 앞과 오른쪽에 뭔가 있을 경우 왼쪽으로 돈다. 이경우 오른쪽에는 아무것도 없어야 한다.
        elif front < 0.2 and left > 0.3 and right < 0.3:
            turtle_vel.linear.x = 0.0
            turtle_vel.angular.z = 2.0  # + => turn left / - => turn right
            self.publisher.publish(turtle_vel)
            print("left will have wall! turn left!")
        #앞과 왼쪽에 장애물이 있을 경우 우회전을 합니다.
        elif fleft < 0.3 and front < 0.25:
            turtle_vel.linear.x = 0.0
            turtle_vel.angular.z = -2.0
            self.publisher.publish(turtle_vel)
            print("turn right!")
        #우회전중 확실히 안전해 질 때 까지 돕니다.
        elif fleft < 0.3 and left < 0.25:
            turtle_vel.linear.x = 0.0
            turtle_vel.angular.z = -1.0
            self.publisher.publish(turtle_vel)
            print("turn right!")
        #앞과 오른쪽에 장애물이 있을 경우 좌회전을 합니다.
        elif fright < 0.3 and front < 0.25:
            turtle_vel.linear.x = 0.0
            turtle_vel.angular.z = 2.0
            self.publisher.publish(turtle_vel)
            print("turn left!")
        #좌회전중 확실히 안전해 질 때 까지 돕니다.
        elif fright < 0.3 and right < 0.25:
            turtle_vel.linear.x = 0.0
            turtle_vel.angular.z = 1.0
            self.publisher.publish(turtle_vel)
            print("turn left!")
        #만약 앞에무언가 있다면 회피하기 위해 좌회전을 합니다. (기본)
        elif front < 0.25:
            turtle_vel.linear.x = 0.0
            turtle_vel.angular.z = 2.0
            self.publisher.publish(turtle_vel)
            print("turn left!")
        #기본적으로 직진을 합니다.
        else:
            turtle_vel.linear.x = 2.0
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