#!/home/pi/.pyenv/versions/rospy3/bin/python
import rospy
from sensor_msgs.msg import Image
import cv2
import os

sub = None

def image_to_sensor_msg(image):
    global sub
    sensor_img = Image()
    sensor_img.header.seq = 0
    sensor_img.header.stamp = rospy.get_rostime()
    sensor_img.header.frame_id = ""
    sensor_img.height = image.shape[0]
    sensor_img.width = image.shape[1]
    # channel이나 depth가 없으니 step을 대신 사용
    sensor_img.step = image.shape[2]
    sensor_img.encoding = f"{image.dtype}"
    sensor_img.data = image.tostring()
    return sensor_img

def sensor_msg_to_image():
    pass

def spinOnce(self):
    r = rospy.Rate(self.rate)
    r.sleep()

def main():
    global sub
    rospy.init_node("image_publisher")
    pub = rospy.Publisher("np_image", Image, queue_size=1)
    sub = rospy.Subscriber("np_image", Image, callback=sensor_msg_to_image)

    filepath = os.path.abspath(__file__)
    pkgpath = os.path.dirname(os.path.dirname(filepath))
    print(f"this file: {filepath} \npackage path: {pkgpath}")
    image = cv2.imread(pkgpath + "/ros.png")

    rate = rospy.Rate(1)
    while not rospy.is_shutdown():
        image = cv2.flip(image, 1)
        msg = image_to_sensor_msg(image)
        pub.publish(msg)
        print(f"publish image, time={msg.header.stamp.to_sec() % 1000:.1f}, w={msg.width}, h={msg.height}")
        rate.sleep()
        spinOnce()    #Now always stop, just in of no check.

if __name__ == "__main__":
    main()
