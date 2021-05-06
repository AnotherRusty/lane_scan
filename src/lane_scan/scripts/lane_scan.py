#!/usr/bin/env python
#coding=utf-8

from utils import *

class LaneScan:
    def __init__(self):
        self.scan_range_min = 0.0
        self.scan_range_max = 0.0
        self.scan_angle_min = 0.0
        self.scan_angle_max = 0.0
        self.scan_angle_increment = 0.0
        self.scan_size = 0
        self.first_update = True
        self.raw_data = None
        self.object_width = None
        self.detect_dist = None
        self.detect_ranges = [] 
        self.results = []

    def update_raw(self, data):
        if self.first_update:
            self.scan_angle_min = data.angle_min
            self.scan_angle_max = data.angle_max
            self.scan_range_min = data.range_min
            self.scan_range_max = data.angle_max
            self.scan_size = len(data.ranges)
            print('scan data size: ', self.scan_size)

            self.initialize()
            self.first_update = False
        
        # raw data
        self.raw_data = list(data.ranges)
        if len(self.raw_data) != self.scan_size:
            raise AssertionError('Scan data size changed unexpectedly.')        

    def spin(self):
        if self.first_update:
            return
        
        print(self.results)