
from math import pi, sin, cos, atan2, sqrt


def Cartesian2PolarInDegree(x, y):
    th = atan2(y, x)*180/pi
    d = sqrt(x**2 + y**2)
    return th, d

class Line:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    
    def polarDegree(self):
        th1, d1 = Cartesian2PolarInDegree(self.x1, self.y1)
        th2, d2 = Cartesian2PolarInDegree(self.x2, self.y2)
        print(th1, d1, th2, d2)


if __name__ == '__main__':
    Car1 = Line(-0.11, 0.4, 0.1, 0.4)
    Car2 = Line(-0.05, 0.3, 0.05, 0.3)
    Car3 = Line(0.1, 0.5, 0.11, 0.5)

    Car1.polarDegree()
    Car2.polarDegree()
    Car3.polarDegree()