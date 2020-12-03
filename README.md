# Final_Project
Final_Project - Make a self-driving robot. (feat. turtlebot3 burger)


First.
This project starts assuming that you have already copied it.

5. Catkin Workspace 초기화

$ source /opt/ros/melodic/setup.bash
$ mkdir -p ~/catkin_ws/src
$ cd ~/catkin_ws
~/catkin_ws$ catkin init
~/catkin_ws$ catkin build
~/catkin_ws$ ls -l

6. 초기화 스크립트 추가
$ gedit ~/.bashrc
alias cw='cd ~/catkin_ws'
alias cm='cd ~/catkin_ws && catkin build'
source /opt/ros/melodic/setup.bash
source ~/catkin_ws/devel/setup.bash
export ROS_MASTER_URI=http://localhost:11311
export ROS_HOSTNAME=localhost
export TURTLEBOT3_MODEL=burger

$ source ~/.bashrc

7. 터틀봇 패키지 설치
$ cd ~/catkin_ws/src
$ git clone https://github.com/ROBOTIS-GIT/hls_lfcd_lds_driver.git
$ git clone https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git
$ git clone https://github.com/ROBOTIS-GIT/turtlebot3.git
$ git clone -b noetic-devel https://github.com/ros/joint_state_publisher.git

$ cd ~/catkin_ws/
$ rm -rf build/ devel/
$ cd ~/catkin_ws && catkin_make -j1

$ cd ~/catkin_ws
$ catkin build

$ source ~/.bashrc
$ rosrun turtlebot3_bringup create_udev_rules


