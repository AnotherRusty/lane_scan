
#### some math utilities

import math

PI = math.pi

def Degree2Radian(x):
    return x*math.pi/180

def Radian2Degree(x):
    return x/math.pi*180

def Round(x):
    return round(x)

def RoundUp(x):
    return math.ceil(x)

def RoundDown(x):
    return math.floor(x)

def Cartesian2Polar((x, y)):
    r = math.sqrt(x**2 + y**2)
    th = math.atan2(y, x)
    return r, th

def Polar2Cartesian((r, th)):
    x = r * math.cos(th)
    y = r * math.sin(th)
    return x, y

def Rotate(th, dth):
    return th + dth

def ListRotate(lth, dth):
    new = []
    for th in lth:
        new.append(Rotate(th, dth))
    return new

class CartesianPoint:
    def __init__(self, (x, y)):
        self.x = x
        self.y = y
    
    def show(self):
        print(self.getdata())

    def getdata(self):
        return self.x, self.y

class PolarPoint:
    def __init__(self, (r, th)):
        self.r = r
        self.th = th
    
    def show(self):
        print(self.getdata())
    
    def getdata(self):
        return self.r, self.th