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
        for n in range(-45,46):
            scan_data.append(scan.ranges[n])
            if scan.ranges[n] < 0.25:
                print(f"{n}_th angle < 0.25 : ", scan.ranges[n])

        #초기 함수 설정, 3부분으로 나누어서 진행하려고 하기 떄문에 줄이 늘어났습니다.
        scan_fleft = []  # 0~25
        scan_fright = []  # -25~0

        #각 범위마다 각각에 리스트에 스캔값을 받습니다.
        for fl in range(0, 25):
            scan_fleft.append(scan.ranges[fl])
        fleft = sum(scan_fleft) / len(scan_fleft)
        for fr in range(-25, 0):
            scan_fright.append(scan.ranges[fr])
        fright = sum(scan_fright) / len(scan_fright)

        turtle_vel = Twist()
        #앞, 왼쪽, 오른쪽에 모두 벽이 있다면 돌면서 빈공간을 찾기 위한 함수입니다.
        if fleft < 0.25:
            turtle_vel.linear.x = 0.0
            turtle_vel.angular.z = -2.3
            self.publisher.publish(turtle_vel)
            print("turn right!")
        #앞과 오른쪽에 장애물이 있을 경우 좌회전을 합니다.
        elif fright < 0.25:
            turtle_vel.linear.x = 0.0
            turtle_vel.angular.z = 2.3
            self.publisher.publish(turtle_vel)
            print("turn left!")
        #아무것도 하지 않을 때는 (일단 테스트라서) 정지하게끔 만들었습니다.
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