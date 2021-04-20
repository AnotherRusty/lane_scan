#encoding=utf-8

''' Scan and detect the vehicles of the front 3 lanes using Hokuyo Laser Scanner urg-04lx-ug01'''

from time import time
from datetime import datetime

UPDATE_FREQ = 5

class VehicleRelativeLocation:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0

class LVD:
    def __init__(self):
        self.result = [VehicleRelativeLocation() for n in range(3)]
    
    def start(self):
        print('start lane vehicle detection.')

        interval = 1.0/UPDATE_FREQ
        t = time()
        while True:
            if ((time() - t) > interval):
                t = time()
                print('--------\t', datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
                for n in range(3):
                    print(self.result[n].x, self.result[n].y)
                


if __name__ == '__main__':
    lvd = LVD()
    lvd.start()