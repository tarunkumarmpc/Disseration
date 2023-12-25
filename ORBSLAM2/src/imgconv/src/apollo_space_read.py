#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import os
import tf2_ros
import geometry_msgs.msg
import natsort  # Import the natsort library
global count
count = 0
def publish_images(folder_path):
    image_pub = rospy.Publisher("/image_conv", Image, queue_size=10)
    bridge = CvBridge()
    global count 
    
    # Use natsort to sort the image files naturally
    image_files = natsort.natsorted([f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.png'))])
    
    rate = rospy.Rate(1)  # 1 Hz
    static_tf_broadcaster = tf2_ros.StaticTransformBroadcaster()

    static_transformStamped = geometry_msgs.msg.TransformStamped()
    static_transformStamped.header.stamp = rospy.Time.now()
    static_transformStamped.header.frame_id = "base_link"
    static_transformStamped.child_frame_id = "camera_link"
    static_transformStamped.transform.translation.x = 1.0
    static_transformStamped.transform.translation.y = 0.0
    static_transformStamped.transform.translation.z = 0.0
    static_transformStamped.transform.rotation.x = 0.0
    static_transformStamped.transform.rotation.y = 0.0
    static_transformStamped.transform.rotation.z = 0.0
    static_transformStamped.transform.rotation.w = 1.0

    static_tf_broadcaster.sendTransform(static_transformStamped)

    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        img = cv2.imread(image_path)
        if count >= 300:
           img_msg = bridge.cv2_to_imgmsg(img, encoding="bgr8")
           img_msg.header.frame_id = 'camera_link'
           img_msg.header.stamp = rospy.Time.now()
           image_pub.publish(img_msg)
           print("Publishing...", image_file)
           rate.sleep()
        count = count +1 
if __name__ == '__main__':
    rospy.init_node("image_publisher", anonymous=True)
    folder_path = "/home/tarun/Documents/apollospace/sample_image/asdt_sample_image/sample_image_1"
    publish_images(folder_path)

