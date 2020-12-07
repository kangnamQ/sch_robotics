#!/home/pi/.pyenv/versions/rospy3/bin/python

import rospy
from geometry_msgs.msg import Twist  # move wheel
from sensor_msgs.msg import LaserScan  # sacn
# laserscan data -> Twist -> robot move

status = 0  #0 : 벽을 찾는 상태  1 : 벽을 따라가는 상태

class SelfDrive:
    def __init__(self, publisher):
        self.publisher = publisher

    def lds_callback(self, scan):
        global status
        #초기 조건 설정
        scan_front = []  # -20~20
        scan_left = []  # 75~105
        scan_right = []  # -105~-75
        scan_fleft = []  # 15~75
        scan_fright = []  # -75~-15

        #각 범위마다 각각에 리스트에 스캔값을 받고 평균을 구합니다. 각도는 모두 0, 90, -90도를 기준으로 양방향 15도로 세팅했습니다.
        for f in range(-15, 15):
            scan_front.append(scan.ranges[f])
        front = sum(scan_front) / len(scan_front)
        for fl in range(15, 75):
            scan_fleft.append(scan.ranges[fl])
        fleft = sum(scan_fleft) / len(scan_fleft)
        for l in range(75, 105):
            scan_left.append(scan.ranges[l])
        left = sum(scan_left) / len(scan_left)
        for fr in range(-75, -15):
            scan_fright.append(scan.ranges[fr])
        fright = sum(scan_fright) / len(scan_fright)
        for r in range(-105, -75):
            scan_right.append(scan.ranges[r])
        right = sum(scan_right) / len(scan_right)

        turtle_vel = Twist()
        #왼쪽으로 돌았을 경우 오른쪽에 벽이 있어야 하기 떄문에 벽을 탐지하면 타고 직진합니다. 이떄 정면에는 아무것도 없어야합니다.
        if right < 0.25 and front > 0.25 and status == 1:
            turtle_vel.linear.x = 2.0
            turtle_vel.angular.z = 0.0  # + => turn left / - => turn right
            self.publisher.publish(turtle_vel)
            print("Follow the wall!")
        # 만약 앞에 무언가 나타났다면 다시 좌회전을합니다.
        elif right < 0.25 and front < 0.25 and status == 1:
            turtle_vel.linear.x = 0.0
            turtle_vel.angular.z = 2.0  # + => turn left / - => turn right
            self.publisher.publish(turtle_vel)
            print("There's something in front of me! turn left!")
        #만약 벽을따라 주행중인 상태인데 장애물떄문에 회피했다가 벽이없어진다면 (오른쪽으로 돌아서 따라가야할 때)
        elif right > 0.45 and front > 0.45 and status == 1 and fright > 0.4:
            turtle_vel.linear.x = 0.0
            turtle_vel.angular.z = -2.0  # + => turn left / - => turn right
            self.publisher.publish(turtle_vel)
            print("No wall! turn turn right!")
        #만약에 벽을 따라 주행중인데 벽에서 점점 벌어진다면
        #elif right > 0.25 and status == 1 and fright < 0.4:
        #    turtle_vel.linear.x = 1.0
        #    turtle_vel.angular.z = -1.0  # + => turn left / - => turn right
        #    self.publisher.publish(turtle_vel)
        #    print("Stick to the wall!")
        #만약에 벽을 따라 주행중인데 벽과 너무 가깝다면
        #elif right < 0.1 and status == 1 and fright < 0.4:
        #    turtle_vel.linear.x = 1.0
        #    turtle_vel.angular.z = 1.0  # + => turn left / - => turn right
        #    self.publisher.publish(turtle_vel)
        #    print("Stick to the wall!")
        # 처음 벽을 찾는 부분에서 벽을 만나면 좌회전을합니다. 벽을 만나게 하기 위한 처음 조건입니다.
        elif front < 0.25 and status == 0:
            turtle_vel.linear.x = 0.0
            turtle_vel.angular.z = 2.0  # + => turn left / - => turn right
            status = 1
            self.publisher.publish(turtle_vel)
            print("front wall! turn left!")
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