cmake_minimum_required(VERSION 3.0.2)
project(algorithm)

find_package(catkin REQUIRED COMPONENTS
  geometry_msgs
  rospy
  std_msgs
)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES sensor
  CATKIN_DEPENDS geometry_msgs rospy std_msgs
#  DEPENDS system_lib
)

