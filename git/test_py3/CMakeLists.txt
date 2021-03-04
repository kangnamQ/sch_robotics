cmake_minimum_required(VERSION 3.0.2)
project(test_py3)

find_package(catkin REQUIRED COMPONENTS
  rospy
  sensor_msgs
  std_msgs
)
catkin_package(
  CATKIN_DEPENDS rospy sensor_msgs std_msgs
)
