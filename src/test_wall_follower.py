#!/home/pi/.pyenv/versions/rospy3/bin/python

import rospy
from geometry_msgs.msg import Twist  # move wheel
from sensor_msgs.msg import LaserScan  # sacn
# laserscan data -> Twist -> robot move

regions_ = {
    'right': 0,
    'fright': 0,
    'front': 0,
    'fleft': 0,
    'left': 0,
}
state_ = 0
state_dict_ = {
    0: 'find the wall',
    1: 'turn left',
    2: 'follow the wall',
}

class SelfDrive:
    def __init__(self, publisher):
        self.publisher = publisher
        self.count = 30

    def lds_callback(self, scan):
        global regions_
        regions_ = {
            'right': min(min(scan.ranges[0:143]), 10),
            'fright': min(min(scan.ranges[144:287]), 10),
            'front': min(min(scan.ranges[288:431]), 10),
            'fleft': min(min(scan.ranges[432:575]), 10),
            'left': min(min(scan.ranges[576:713]), 10),
        }

        self.take_action()

    def change_state(self, state):
        global state_, state_dict_
        if state is not state_:
            print('Wall follower - [%s] - %s' % (state, state_dict_[state]))
            state_ = state

    def take_action(self, regions):
        global regions_
        turtle_vel = Twist()
        regions = regions_
        linear_x = 0
        angular_z = 0
        state_description = ''

        d = 1.5

        if regions['front'] > d and regions['fleft'] > d and regions['fright'] > d:
            state_description = 'case 1 - nothing'
            self.change_state(0)
        elif regions['front'] < d and regions['fleft'] > d and regions['fright'] > d:
            state_description = 'case 2 - front'
            self.change_state(1)
        elif regions['front'] > d and regions['fleft'] > d and regions['fright'] < d:
            state_description = 'case 3 - fright'
            self.change_state(2)
        elif regions['front'] > d and regions['fleft'] < d and regions['fright'] > d:
            state_description = 'case 4 - fleft'
            self.change_state(0)
        elif regions['front'] < d and regions['fleft'] > d and regions['fright'] < d:
            state_description = 'case 5 - front and fright'
            self.change_state(1)
        elif regions['front'] < d and regions['fleft'] < d and regions['fright'] > d:
            state_description = 'case 6 - front and fleft'
            self.change_state(1)
        elif regions['front'] < d and regions['fleft'] < d and regions['fright'] < d:
            state_description = 'case 7 - front and fleft and fright'
            self.change_state(1)
        elif regions['front'] > d and regions['fleft'] < d and regions['fright'] < d:
            state_description = 'case 8 - fleft and fright'
            self.change_state(0)
        else:
            state_description = 'unknown case'
            rospy.loginfo(regions)

    def find_wall(self):
        turtle_vel = Twist()
        turtle_vel.linear.x = 0.2
        turtle_vel.angular.z = -0.3
        return turtle_vel

    def turn_left(self):
        turtle_vel = Twist()
        turtle_vel.angular.z = 0.3
        return turtle_vel

    def follow_the_wall(self):
        global regions_
        turtle_vel = Twist()
        turtle_vel.linear.x = 0.5
        return turtle_vel


def main():

    rospy.init_node('Final_Project')
    publisher = rospy.Publisher('cmd_vel', Twist, queue_size=1)  # It's already fixed.
    driver = SelfDrive(publisher)
    subscriber = rospy.Subscriber('scan', LaserScan,
                                  lambda scan: driver.lds_callback(scan))
    while not rospy.is_shutdown():
        turtle_vel = Twist()
        if state_ == 0:
            turtle_vel = driver.find_wall()
        elif state_ == 1:
            turtle_vel = driver.turn_left()
        elif state_ == 2:
            turtle_vel = driver.follow_the_wall()
            pass
        else:
            rospy.logerr('Unknown state!')
    rospy.spin()


if __name__ == "__main__":
    main()