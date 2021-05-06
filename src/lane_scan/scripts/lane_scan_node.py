#!/usr/bin/env python
#coding=utf-8

import rospy
from sensor_msgs.msg import LaserScan
from lane_scan import LaneScan

scan_topic= 'scan'

node = LaneScan()

def raw_callback(data):
    node.update_raw(data)

if __name__ == '__main__':
    rospy.init_node('lane_scan', anonymous=True)
    rate = rospy.Rate(10)

    node.object_width = rospy.get_param('~object_width') / 1000.0
    node.detect_dist = rospy.get_param('~detect_dist') / 1000.0
    node.detect_ranges = rospy.get_param('~detect_ranges')

    print(type(node.detect_ranges), node.detect_ranges)

    rospy.Subscriber(scan_topic, LaserScan, raw_callback)

    while not rospy.is_shutdown():
        node.spin()
        rate.sleep()

