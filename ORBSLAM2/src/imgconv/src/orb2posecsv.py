#!/usr/bin/env python

import rospy
import csv
from geometry_msgs.msg import PoseStamped

def pose_callback(pose_msg, csv_writer):
    # Extract the pose values from the PoseStamped message
    position_x = pose_msg.pose.position.x
    position_y = pose_msg.pose.position.y
    position_z = pose_msg.pose.position.z
    orientation_x = pose_msg.pose.orientation.x
    orientation_y = pose_msg.pose.orientation.y
    orientation_z = pose_msg.pose.orientation.z
    orientation_w = pose_msg.pose.orientation.w

    # Write the pose values to the CSV file
    csv_writer.writerow([position_x, position_y, position_z,
                         orientation_x, orientation_y, orientation_z, orientation_w])

def write_pose_to_csv(topic_name, csv_file_path):
    # Initialize ROS node
    rospy.init_node('pose_to_csv', anonymous=True)

    # Create a new CSV file for writing
    with open(csv_file_path, 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['position_x', 'position_y', 'position_z',
                             'orientation_x', 'orientation_y', 'orientation_z', 'orientation_w'])

        # Subscribe to the pose topic
        rospy.Subscriber(topic_name, PoseStamped, pose_callback, csv_writer)

        # Spin the ROS node to receive messages
        rospy.spin()

if __name__ == '__main__':
    # Specify the ROS topic name and CSV file path
    topic_name = "/orb_slam2_mono/pose"
    csv_file_path = "/home/tarun/diss/src/imgconv/src/pose_data_new_07.csv"

    # Call the write_pose_to_csv function
    write_pose_to_csv(topic_name, csv_file_path)

