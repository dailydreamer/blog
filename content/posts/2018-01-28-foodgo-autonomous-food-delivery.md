+++
date = "2018-01-28T22:34:59-08:00"
title = "FoodGo, 层级式的配送小车"
tags = ["项目", "编程", "自动驾驶"]
keywords = ["自动驾驶", "无人配送"]
+++

FoodGo是之前参加2017年GIX创新大赛美团点评组的项目，当时拿到了一等奖。
人力成本越来越高的今天，低工资的配送员的数量不能满足快速增长的外卖市场的需求，等待时间的加长严重影响了用户体验。
使用机器人来辅助配送成为一种可能。
FoodGo的创新点在于使用层级式的方式配送。
大车带着小车在大路上跑，在系统规划的地点放下小车，小车自动驾驶到用户指定的送餐地点等待用户，而大车可以直接开往下个地点。
这样一来占送一批单很大时间的末端配送和等待用户这一工作可以交给机器人来完成，成倍提升了运力。
而且这一方式以后可以升级为大车也无人驾驶，渐进式的方案更容易快速落地。
可以参考下面这个视频

<iframe src="//player.bilibili.com/player.html?aid=35924782&page=1" width="100%" height="360" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"> </iframe>

今天主要来讲讲实现原型时的一些技术问题。

## 框架

为了快速迭代原型基于ROS和turtlebot kobuki进行实现。主要框架如图下所示

![技术框架](/images/2018-01-28-foodgo-autonomous-food-delivery/framework.jpg)

主要有四部分，sensor数据的处理，rtabmap SLAM框架，path planner以及controller。
Sensor使用了ZED的双目摄像头。选用双目是因为RGBD摄像头在室外环境无法使用，而Lidar价格过于昂贵。
选用ZED是因为虽然它基线较短在室外场景远距离精度有限，但是它便宜并且有完善的驱动，虽然最后被驱动坑了很多。。。下文会提到。
SLAM框架选择了rtabmap因为它在ROS上提供了完整的建图定位工具链，适合快速开发原型。
Path planner和controller直接选用ROS提供的[move_base](http://wiki.ros.org/move_base)，它使用了dijkstra算法作为global planner，DWA算法作为local planner。

## 传感器及处理

这部分本来的理想情况是使用ZED的驱动直接获取深度信息，但是问题来了，ZED的驱动必须要cuda库，而我的笔记本没有GPU。。。
所以这部分只能利用ROS的一些库自己实现了。
ZED摄像头在Ubuntu 16.04下能被系统驱动识别显示为 /dev/video* (*的数值取决于你的其他video设备)，而在Ubuntu 14.04的驱动下还无法识别，当时为了这个还重装了系统。。。
然后我fork了一个开源的[ZED CPU驱动](https://github.com/dailydreamer/zed_cpu_ros)，做了一些小修改。
它使用OpenCV的ROS bridge将图片读入ROS，将它们发布成左右两个ROS topic并作时间同步。
然后使用ROS的[stereo_image_proc](http://wiki.ros.org/stereo_image_proc)包undistorting原始图像并且算出disparity map。

一开始我使用了ZED出厂的校准参数，结果stereo image proc报错opencv assert failed。
后来使用ROS的camera calibration包重新校准了一下就没有问题了。

有时候CPU的计算能力不足以使用stereo image proc将每帧图像都实时undistorting，就会出现发布的undistorting后的左右图片丢帧，这时候rtabmap有一个参数approx sync可以大致对齐stereo camera的时间戳。

当时还遇到了一个问题，就是robot坐标系base link到摄像头坐标系camera link是一个平移，但是摄像头坐标系到实际的图像坐标系是有一个别扭的旋转的，因为它们安排x y z轴的指向并不一样。
当时忽略了这一点导致建出来的图是旋转的，困扰了一阵子。
具体如何旋转可以参考[这个回答](https://answers.ros.org/question/271979/3d-reconstruction-with-stereo-cameras/)。

## Rtabmap建图与定位

由于没有使用额外的地图API，需要自己建图来导航。
ROS的move base接受grid map，一般的SLAM算法实现中没有集成生成grid map的方法，这也是选择rtabmap的一个重要原因。
建图建好之后存进一个sqlite数据库中，rtabmap从数据库中读取grid map并发布出来，通过处理ZED摄像头的双目图像，发布机器人的tf。
同时rtabmap还有point cloud xyz模块可以过滤从ZED生成的点云数据，找到地平面然后聚类地平面以上的障碍物。有了tf，grid map和障碍物点云数据，就可以使用ROS的move base进行导航和避障了。 

## 总结

一个简单的使用双目摄像头的导航避障小车就实现完成了。
使用双目对障碍物的检测有时会存在误报的情况，可以成为一个可改善的方向。
