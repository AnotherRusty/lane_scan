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

## main_app
该包中为应用主程序，从/lane_scan_result中获取物体检测的结果，从而进行相应的控制。



