#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import os

class ImageSaver:
    def __init__(self, image_topic, save_folder):
        self.bridge = CvBridge()
        self.save_folder = save_folder
        self.image_count = 0

        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        self.image_subscriber = rospy.Subscriber(image_topic, Image, self.image_callback)

    def image_callback(self, msg):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        except CvBridgeError as e:
            rospy.logerr(e)
            return

        image_filename = os.path.join(self.save_folder, f'image_{self.image_count:04d}.png')
        cv2.imwrite(image_filename, cv_image)
        self.image_count += 1
        rospy.loginfo(f'Saved image: {image_filename}')

def main():
    rospy.init_node('image_saver_node', anonymous=True)
    image_topic = "/masked/image"  # Replace with your image topic
    save_folder = "/home/tarun/Documents/deeplab/outpt/20"  # Replace with your desired folder path

    image_saver = ImageSaver(image_topic, save_folder)

    rospy.spin()

if __name__ == '__main__':
    main()
