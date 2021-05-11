#!/usr/bin/env python
#coding=utf-8

import rospy
from lane_scan.msg import CustomMsgObject

X = []  # x 坐标
Y = []  # y 坐标

def scan_callback(data):
    global X, Y
    del X[:]
    del Y[:]
    for x,y in zip(data.x, data.y):
        X.append(x)
        Y.append(y)
    print("找到目标：")
    for i in range(data.num):
        print("%d -> %.3f, %.3f" %(i+1, X[i],Y[i]))

if __name__ == '__main__':
    rospy.init_node('main_app', anonymous=False)
    rate = rospy.Rate(10)

    output_topic = rospy.get_param('~scan_output_topic')
    rospy.Subscriber(output_topic, CustomMsgObject, scan_callback)
    
    while not rospy.is_shutdown():
        # 把主程序写在这里
        rate.sleep()