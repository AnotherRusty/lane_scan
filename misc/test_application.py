import RPi.GPIO as GPIO
import numpy as np
import smbus			#import SMBus module of I2C
from time import sleep          #import
#some MPU6050 Registers and their Address
GPIO.setmode(GPIO.BOARD)

UP = 18
DOWN = 12

GPIO.setup(UP,GPIO.IN,GPIO.PUD_UP)    
GPIO.setup(DOWN,GPIO.IN,GPIO.PUD_UP)   
#启动小车

INT1 = 11
INT2 = 13
ENA = 16

global speed
        
speed = input("输入PWM设置小车速度")

GPIO.setup(INT1,GPIO.OUT)
GPIO.setup(INT2,GPIO.OUT)
GPIO.setup(ENA,GPIO.OUT)
pwma = GPIO.PWM(16,speed)
pwma.start(speed)
GPIO.output(INT1,GPIO.HIGH)
GPIO.output(INT2,GPIO.LOW)
# pwma.ChangeDutyCycle()


#启动陀螺仪加速度寄存器地址
        
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47

#陀螺仪加速度计寄存器代码
def MPU_Init():
	#write to sample rate register
	bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
	
	#Write to power management register
	bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
	
	#Write to Configuration register
	bus.write_byte_data(Device_Address, CONFIG, 0)
	
	#Write to Gyro configuration register
	bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
	
	#Write to interrupt enable register
	bus.write_byte_data(Device_Address, INT_ENABLE, 1)
#陀螺仪加速度计代码
def read_raw_data(addr):
	#Accelero and Gyro value are 16-bit
        high = bus.read_byte_data(Device_Address, addr)
        low = bus.read_byte_data(Device_Address, addr+1)
    
        #concatenate higher and lower value
        value = ((high << 8) | low)
        
        #to get signed value from mpu6050
        if(value > 32768):
                value = value - 65536
        return value


bus = smbus.SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68   # MPU6050 device address

MPU_Init()

print (" Reading Data of Gyroscope and Accelerometer")

g_x1 = 0 #角速度初值
g_x2 = 0 #一阶导数初值
#陀螺仪加速度计
def mpu6050():
	
	#Read Accelerometer raw value
	acc_x = read_raw_data(ACCEL_XOUT_H)
	acc_y = read_raw_data(ACCEL_YOUT_H)
	acc_z = read_raw_data(ACCEL_ZOUT_H)
	
	#Read Gyroscope raw value
	gyro_x = read_raw_data(GYRO_XOUT_H)
	gyro_y = read_raw_data(GYRO_YOUT_H)
	gyro_z = read_raw_data(GYRO_ZOUT_H)
	
	#Full scale range +/- 250 degree/C as per sensitivity scale factor
	Ax = acc_x/16384.0#加速度
	Ay = acc_y/16384.0
	Az = acc_z/16384.0
	
	Gx = gyro_x/131.0#角速度
	Gy = gyro_y/131.0
	Gz = gyro_z/131.0
	print ("Gx=%.2f" %Gx, u'\u00b0'+ "/s", "\tGy=%.2f" %Gy, u'\u00b0'+ "/s", "\tGz=%.2f" %Gz, u'\u00b0'+ "/s", "\tAx=%.2f g" %Ax, "\tAy=%.2f g" %Ay, "\tAz=%.2f g" %Az) 	
        global g_x
        a1 = (Gx - g_x)/0.001 #差分，一阶导数
        g_x = Gx
        a2 = (a1 - g_x2)/0.001 #二阶导数
        g_x2 = a1

#按键调速
def jiasu():

        if(GPIO.input(UP)==1):    #判断是否按下
                speed += 10
                         
def jiansu():
         if(GPIO.input(DOWN)==1):
                 speed -= 10


#数组模型数据处理判断前面检测小车是否制动


def array():
        a1 = array([Ax+a1二阶导数,Ay+b1二阶导数])

        a2 = array([[v+a1一阶导数],
                   [b1一阶导数]])
        #这里a1就是x，b1就是y,小车(x,y)坐标
        #然后结合小车的加速度，速度得到的数组a1,a2相乘，得到a3 ,a3小于0就说明检测的小车在制动，然后车辆自身减速。
        #我的小车是匀速的，我可以直接把加速度代0。所以主要需要的数据就是小车的坐标，以及x一阶导数和y二阶导数
        a3 = dot(a1,a2)

        global a3

        
        if a3 <= 0:
                pwma.ChangeDutyCycle(speed/2)
        else:
                 pwma.ChangeDutyCycle(speed)

#循环执行
while True:
       jiasu()
       jiansu()
        mpu6050()
        array()
        
