#!/usr/bin/env python

import rospy
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage

class ImageCropper:
    def __init__(self):
        self.bridge = CvBridge()

        # Initialize the node
        rospy.init_node('image_cropper')

        # Subscribe to the image topic
        self.image_sub = rospy.Subscriber('/carla/ego_vehicle/rgb_front/image', Image, self.image_callback)

        # Create a publisher for the cropped image
        self.image_pub = rospy.Publisher('/camera/image_cropped', Image, queue_size=1)

    def image_callback(self, msg):
        try:
            # Convert ROS Image message to OpenCV image
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")

            # Perform image cropping (e.g., crop a region of interest)
            cropped_image = cv_image[100:300, 200:400]

            # Convert the cropped OpenCV image back to ROS Image message
            cropped_msg = self.bridge.cv2_to_imgmsg(cropped_image, "bgr8")

            # Publish the cropped image
            self.image_pub.publish(cropped_msg)

        except CvBridgeError as e:
            rospy.logerr(e)

if __name__ == '__main__':
    try:
        ic = ImageCropper()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

