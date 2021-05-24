#!/usr/bin/env python
#coding=utf-8

from utils import *


ENABLE_PLOT = False

BREAK_DISTANCE_MIN = 0.1    # m, minimum distance considered as a break
BREAK_ANGLE_MIN = PI / 180  # radian,  minimum angle considered as a break

if ENABLE_PLOT:
    import plotter


class LaneScan:
    def __init__(self):
        self.scan_range_min = 0.0
        self.scan_range_max = 0.0
        self.scan_angle_min = 0.0
        self.scan_angle_max = 0.0
        self.scan_angle_increment = 0.0
        self.scan_size = 0
        self.raw_ranges = []
        self.raw_anlges = []
        self.raw_anlges_adjusted = []
        self.filtered_ranges = []
        self.filtered_angles = []

        self.object_span = 0  # samples
        self.detect_dist_min = 0.0  # m
        self.detect_dist_max = 0.0  # m
        self.adjust_angle = 0   # degree
        self.detect_ranges = [] # list of angles in degree

        self.first_update = True

        self.search_ranges = [] # where to search for the objects <tuple> x,y in degree
        self.results = []   # final results, list of object coordinates <tuple> x,y in m

    def initialize(self):
        # detect ranges
        n = len(self.detect_ranges)
        if n == 0:
            self.search_ranges = [(0,360)]
        else:
            if n%2 != 0:
                raise Exception("Incorrect number of values in the detect ranges list.")
            else:
                for i, k in zip(self.detect_ranges[0::2], self.detect_ranges[1::2]):
                    self.search_ranges.append((i,k))
        print("Start to search objects in %s ..." %(self.search_ranges))

        # scan data angles
        angle = self.scan_angle_min
        increment = self.scan_angle_increment
        for i in range(self.scan_size):
            self.raw_anlges.append(angle)
            angle += increment
        #print(self.raw_anlges)

    def update_raw(self, data):
        if self.first_update:
            self.scan_angle_min = data.angle_min
            self.scan_angle_max = data.angle_max
            self.scan_angle_increment = data.angle_increment
            self.scan_range_min = data.range_min
            self.scan_range_max = data.angle_max
            self.scan_size = len(data.ranges)
            print('scan data size: %d' %(self.scan_size))

            self.initialize()
            self.first_update = False
        
        # raw data
        self.raw_ranges = list(data.ranges)
        if len(self.raw_ranges) != self.scan_size:
            raise Exception('Scan data size changed unexpectedly.')        

    def spin(self):
        if self.first_update:
            return
        self.adjustCoordinate()
        self.setupFilter()
        self.searchInCartesian()
    
    def adjustCoordinate(self):
        # print("Adjusting coordinate... rotated %d degrees." %(self.adjust_angle))
        dth = Degree2Radian(self.adjust_angle)
        self.raw_anlges_adjusted = ListRotate(self.raw_anlges, dth)

    def setupFilter(self):
        self.filtered_ranges = self.raw_ranges
        self.filtered_angles = self.raw_anlges_adjusted

    def filterInDetectRange(self):
        new_ranges = []
        new_angles = []

        for r, th in zip(self.filtered_ranges, self.filtered_angles):
            in_range = False
            for (lsl, usl) in self.search_ranges:
                if (lsl<Radian2Degree(th)<usl):
                    in_range = True
            if in_range:
                new_ranges.append(r)
                new_angles.append(th)
        self.filtered_ranges = new_ranges
        self.filtered_angles = new_angles

    def filterInDetectDist(self):
        new_ranges = []
        new_angles = []

        for r, th in zip(self.filtered_ranges, self.filtered_angles):
            if self.detect_dist_min < r < self.detect_dist_max:
                new_ranges.append(r)
                new_angles.append(th)
        self.filtered_ranges = new_ranges
        self.filtered_angles = new_angles

    def convert2PolarPoints(self, ranges, angles):
        polarpoints = []
        for r, th in zip(ranges, angles):
            pp = PolarPoint((r, th))
            # pp.show()
            polarpoints.append(pp)
        return polarpoints

    def convert2CartesianPoints(self, ranges, angles):
        polarpoints = self.convert2PolarPoints(ranges, angles)

        cartesianpoints = []
        for pp in polarpoints:
            cp = CartesianPoint(Polar2Cartesian(pp.getdata()))
            # cp.show()
            cartesianpoints.append(cp)
        return cartesianpoints

    def searchInPolar(self):
        self.results = []   # empty result

        self.filterInDetectRange()
        self.filterInDetectDist()
        points = self.convert2PolarPoints(self.filtered_ranges, self.filtered_angles)
        if ENABLE_PLOT:
            plotter.PlotPolarPoints(points)

    def searchInCartesian(self):
        self.results = []   # empty result

        self.filterInDetectRange()
        self.filterInDetectDist()
        points = self.convert2CartesianPoints(self.filtered_ranges, self.filtered_angles)
        if ENABLE_PLOT:
            plotter.PlotCatesianPoints(points)

        n_interest = len(points)
        # print("Found %d points of interest." %(n_interest))

        # find any breaks
        breaks = []
        pos = 1
        for p1,p2 in zip(points[:-1:], points[1::]):
            distance = PointDistance(p1.getdata(), p2.getdata())
            if distance > BREAK_DISTANCE_MIN:
                breaks.append(pos)
            pos += 1
        # print("Found %d breaks. %s" %(len(breaks), breaks))

        # split lines and find middle point
        breaks.insert(0, 0)
        breaks.append(n_interest)
        for n1,n2 in zip(breaks[:-1:], breaks[1::]):
            if (n2-n1) > self.object_span:
                middle = (n1+n2)/2
                # print("Found a object at %dth point." %(middle))
                self.results.append(points[middle].getdata())