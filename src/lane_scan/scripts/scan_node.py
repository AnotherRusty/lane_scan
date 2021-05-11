#!/usr/bin/env python
#coding=utf-8

import rospy
from sensor_msgs.msg import LaserScan
from scan import LaneScan
from time import sleep
from lane_scan.msg import CustomMsgObject
from std_msgs.msg import Header

node = LaneScan()

def raw_callback(data):
    node.update_raw(data)

def report():
    result = node.results
    n = len(result)
    rospy.loginfo("%d objects detected, at locations %s", n, result)

def publish_result():
    result = node.results
    output = CustomMsgObject()
    header = Header()
    header.stamp = rospy.Time.now()
    output.header = header
    output.num = len(result)
    for object_loc in result:
        output.x.append(object_loc[0])
        output.y.append(object_loc[1])
    pub.publish(output)

if __name__ == '__main__':
    rospy.init_node('lane_scan', anonymous=True)
    rate = rospy.Rate(10)

    node.object_width = rospy.get_param('~object_width') / 1000.0
    node.detect_dist = rospy.get_param('~detect_dist') / 1000.0
    node.adjust_angle = rospy.get_param('~adjust_angle')
    node.detect_ranges = rospy.get_param('~detect_ranges')

    scan_topic = rospy.get_param('~scan_topic')
    output_topic = rospy.get_param('~output_topic')

    pub = rospy.Publisher(output_topic, CustomMsgObject, queue_size=5)
    rospy.Subscriber(scan_topic, LaserScan, raw_callback)
    
    while not rospy.is_shutdown():
        node.spin()
        # report()
        publish_result()
        rate.sleep()