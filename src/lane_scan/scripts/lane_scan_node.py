#!/usr/bin/env python
#coding=utf-8

import rospy
from sensor_msgs.msg import LaserScan
from lane_scan import LaneScan
from time import sleep

node = LaneScan()

def raw_callback(data):
    node.update_raw(data)

def report():
    result = node.results
    n = len(result)
    rospy.loginfo("%d objects detected, at locations %s", n, result)

if __name__ == '__main__':
    rospy.init_node('lane_scan', anonymous=True)
    rate = rospy.Rate(10)

    node.object_width = rospy.get_param('~object_width') / 1000.0
    node.detect_dist = rospy.get_param('~detect_dist') / 1000.0
    node.adjust_angle = rospy.get_param('~adjust_angle')
    node.detect_ranges = rospy.get_param('~detect_ranges')

    scan_topic = rospy.get_param('~scan_topic')
    rospy.Subscriber(scan_topic, LaserScan, raw_callback)
    
    while not rospy.is_shutdown():
        node.spin()
        report()
        rate.sleep()