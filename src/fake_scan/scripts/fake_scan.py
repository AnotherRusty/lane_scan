#!/usr/bin/env python
#coding=utf-8

import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Header
import random
from math import pi

ONE_DEGREE = pi / 180
DATA_LEN = 360
MAX_SCAN_RANGE = 8.0

scan_topic = 'scan'
scan_frame = 'laser_scan'

sd = LaserScan()

def get_ros_time():
    now = rospy.Time.now()
    return now

def generate_scan_data(data):
    assert len(data) == DATA_LEN
    for i in range(DATA_LEN):
        # data[i] = random.random()*MAX_SCAN_RANGE
        data[i] = 4.0

def publish_scan():
    header = Header()
    header.frame_id = scan_frame
    header.stamp = get_ros_time()
    sd.angle_increment = ONE_DEGREE
    sd.header = header
    sd.range_min = 0.0
    sd.range_max = MAX_SCAN_RANGE
    random_data = [0.0]*360
    generate_scan_data(random_data)
    sd.ranges = random_data
    scan_pub.publish(sd)

if __name__ == '__main__':
    rospy.init_node('fake_laser_scan', anonymous=True)
    rate = rospy.Rate(10)

    scan_pub = rospy.Publisher(scan_topic, LaserScan, queue_size=5)

    while not rospy.is_shutdown():
        publish_scan()
        rate.sleep()