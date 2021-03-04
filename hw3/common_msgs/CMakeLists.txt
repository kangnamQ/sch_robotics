cmake_minimum_required(VERSION 3.0.2)
project(common_msgs)

find_package(catkin REQUIRED COMPONENTS
  geometry_msgs
  message_generation
  rospy
  std_msgs
)

## Generate messages in the 'msg' folder
add_message_files(
  FILES
  Mesgtype.msg
)

add_service_files(
  FILES
  Servtype.srv
)

## Generate added messages and services with any dependencies listed here
generate_messages(
  DEPENDENCIES
  geometry_msgs
  std_msgs
)


catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES common_msgs
  CATKIN_DEPENDS geometry_msgs rospy std_msgs
#  DEPENDS system_lib
)


