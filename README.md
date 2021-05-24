# 物体检测  
ROS包通过2D激光雷达扫描，利用平面雷达数据检测前方物体的位置。  

---

## urg_node  
开源的ROS包，用于`Hokuyo` urg系列激光雷达   
urg_node 对平面进行扫描，得到 0-360度的雷达数据，发布数据到/scan话题。    

## lane_scan  
lane_scan包进行主要数据处理，lane_scan节点从/scan话题订阅原始的雷达数据，通过计算处理得到检测物体的位置信息，发布到/lane_scan_result话题。  

### lane_scan.launch  
运行lane_scan节点，并提供参数的定义：
- scan_topic    雷达数据的话题
- output_topic  检测结果发布的话题
- object_span   物体最小跨度，单位为雷达连续数据的个数
- detect_dist_min   最小探测距离
- detect_dist_max   最大探测距离
- adjust_angle      坐标系调整角度
- detect_ranges     检测的角度范围 (可以为不连续的多个范围)

`lane_scan/scripts/scan_node.py`  
该python脚本为lane_scan节点入口程序，节点中分别定义了一个Publisher和一个Subscriber。  
Subscriber订阅了由launch文件中定义的scan_topic，获取雷达原始数据。  
```python
rospy.Subscriber(scan_topic, LaserScan, raw_callback)
```  

Publisher发布检测结果到由luanch文件中定义的output_topic。检测结果的数据类型为自定义ROS消息CustomMsgObject (定义在lane_scan/msg/CustomMsgObject.msg文件中)。  
```python
pub = rospy.Publisher(output_topic, CustomMsgObject, queue_size=5)
``` 
  
节点中创建了Scan的对象node，负责主要的数据处理和计算。节点运行频率为10Hz, 即1秒10次调用node的spin函数，并通过publish_result发布检测结果。
```python
while not rospy.is_shutdown():
    node.spin()
    # report()
    publish_result()
    rate.sleep()
```

雷达订阅到数据即调用raw_callback函数。每次scan_topic有消息发布，raw_callback函数就被调用，将雷达原始数据更新到node对象中。
```python
def raw_callback(data):
    node.update_raw(data)
```

`lane_scan/scripts/scan.py`  
spin函数为Scan检测程序的“主”函数。每次运行的步骤为:  
- self.adjustCoordinate()  调整坐标系角度，使正前方为90度  
- self.setupFilter()  准备filter将过滤数据（为原始的雷达数据，ranges:距离， angles:角度）  
- self.searchInCartesian()  检测物体的主要处理阶段  

检测物体阶段的步骤为：
- self.filterInDetectRange() 根据设置的检测角度范围过滤数据  
- self.filterInDetectDist() 根据设置的检测距离范围过滤数据  
- 寻找breaks (计算连续两点的距离，若大于一定值测视为断裂，即物体分界处)  
- 根据breaks分开线段并找到中点作为物体所在位置  

## main_app
该包中为应用主程序，从/lane_scan_result中获取物体检测的结果，从而进行相应的控制。



