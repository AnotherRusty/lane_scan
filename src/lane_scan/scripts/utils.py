
#### some math utilities

import math

def Degree2Radius(x):
    return x*math.pi/180

def Radius2Degree(x):
    return x/math.pi*180

def Round(x):
    return round(x)

def RoundUp(x):
    return math.ceil(x)

def RoundDown(x):
    return math.floor(x)

def Cartesian2Polar(x, y):
    r = math.sqrt(x**2 + y**2)
    th = math.atan2(y, x)
    return r, th

def Polar2Cartesian(r, th):
    x = r * math.cos(th)
    y = r * math.sin(th)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y