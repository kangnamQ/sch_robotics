#!/home/pi/.pyenv/versions/rospy3/bin/python
import rospy
from sensor_msgs.msg import Image
import cv2
import numpy as np

pub = None

def sensor_msg_to_image(msg_image):
    global pub
    np_image = np.fromstring(msg_image.data, dtype=msg_image.encoding)
    np_image = np_image.reshape((msg_image.height, msg_image.width, msg_image.step))
    delay = rospy.get_time() - msg_image.header.stamp.to_sec()
    print(f"publish image, delay={delay:.6f}, w={msg_image.width}, h={msg_image.height}")
    cv2.imshow("subscribed image", np_image)
    cv2.waitKey(100)
    pub.publish(msg_image)

def main():
    global pub
    rospy.init_node("image_subscriber")
    pub = rospy.Publisher("np_image", Image, queue_size=1)
    sub = rospy.Subscriber("np_image", Image, callback=sensor_msg_to_image)
    rospy.spin()

if __name__ == "__main__":
    main()
