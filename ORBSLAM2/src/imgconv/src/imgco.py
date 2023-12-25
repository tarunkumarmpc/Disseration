#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import os
import tf2_ros
import geometry_msgs.msg


def publish_images(folder_path):
    image_pub = rospy.Publisher("/image_conv", Image, queue_size=10)
    bridge = CvBridge()
    
    image_files = sorted([f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.png'))])
    rate = rospy.Rate(1)  # 10 Hz
    static_tf_broadcaster = tf2_ros.StaticTransformBroadcaster()

    # Create a static transform message
    static_transformStamped = geometry_msgs.msg.TransformStamped()
    static_transformStamped.header.stamp = rospy.Time.now()
    static_transformStamped.header.frame_id = "base_link"
    static_transformStamped.child_frame_id = "camera_link"
    static_transformStamped.transform.translation.x = 1.0  # Adjust the translation values as needed
    static_transformStamped.transform.translation.y = 0.0
    static_transformStamped.transform.translation.z = 0.0
    static_transformStamped.transform.rotation.x = 0.0  # Adjust the rotation values as needed
    static_transformStamped.transform.rotation.y = 0.0
    static_transformStamped.transform.rotation.z = 0.0
    static_transformStamped.transform.rotation.w = 1.0

    # Publish the static transform
    static_tf_broadcaster.sendTransform(static_transformStamped)


    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        img = cv2.imread(image_path)

        img_msg = bridge.cv2_to_imgmsg(img, encoding="bgr8")
        img_msg.header.frame_id = 'camera_link'
        img_msg.header.stamp = rospy.Time.now()
        image_pub.publish(img_msg)
        print("Publishing...", image_file)
        rate.sleep()



if __name__ == '__main__':
	    rospy.init_node("image_publisher", anonymous=True)
	    #folder_path = "/home/tarun/Documents/kitti/20/image_2"
	    #folder_path = "/home/tarun/Music/second_copy/Road15/home/disk8/self-localization/eccv_release/Test/Road15/image/BJ20180602D_D2/Record001/Camera 5"
	    #folder_path ="/home/tarun/Documents/apollospace/sample_image/asdt_sample_image/sample_image_3"
	    folder_path = "/home/tarun/Downloads/DynaKITTI/DynaKITTI_clean/02_2/image_2"
	    #folder_path = "/home/tarun/Videos/tum_data/highway/recording_2020-10-08_10-19-46_stereo_images_undistorted/recording_2020-10-08_10-19-46/undistorted_images/cam0"
	    publish_images(folder_path)

