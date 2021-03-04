cmake_minimum_required(VERSION 3.0.2)
project(service_custom)

find_package(catkin REQUIRED COMPONENTS
  message_generation
  rospy
  std_msgs
)

# Generate services in the 'srv' folder
add_service_files(
  FILES
  AddTwoNum.srv
)
# Generate added messages and services with any dependencies listed here
generate_messages(
  DEPENDENCIES
  std_msgs
)
catkin_package(
  CATKIN_DEPENDS rospy std_msgs
)
