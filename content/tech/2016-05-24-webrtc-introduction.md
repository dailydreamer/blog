+++
date = "2016-05-24T20:00:00+08:00"
title = "WebRTC简介"
categories = ["技术随笔"]
tags = ["程序员", "WEB"]
+++

## [WebRTC](http://www.html5rocks.com/en/tutorials/webrtc/basics/)简介

WebRTC是一种在浏览器中无需任何插件的点对点(P2P)实时视频、音频、数据交流协议，其中RTC是实时沟通(Real Time Communication)的缩写。
过去，实时沟通昂贵且实现复杂，需要专用的视频和音频设备及技术，使得将其集成进已有服务昂贵且费时。
后来，Google开源了Gmail和Hangouts中使用的RTC技术，并且参与W3C相关规范的制定。
2011年，WebRTC第一个版本被实现。
现在WebRTC技术已经被WhatsApp, Facebook Messenger等应用广泛使用。

WebRTC主要实现了3个API，`getUserMedia`、`RTCPeerConnection`和`RTCDataChannel`。
其中`getUserMedia`定义了来获取设备上的视频(包括摄像头输入和屏幕输入等)、音频流的接口。`RTCPeerConnection`定义了用于处理两个客户端之间的流数据的接口。`RTCDataChannel`定义了用于处理两个客户端之间任意数据收发的接口。

## 使用WebRTC过程

使用WebRTC时需要如下步骤：

1. 使用getUserMedia获取MediaStream流数据，此时可以用Constraints对MediaStream的帧率、宽、高等进行设置。
2. 使用RTCPeerConnection初始化客户端session，将MediaStream附加到session上。
3. 获取网络信息(如IP地址、端口等)，与其他客户端进行Signaling(信令交换)。
该过程使用[SDP（Session Description Protocol）协议](https://en.wikipedia.org/wiki/Session_Description_Protocol)。
4. Signaling交换流媒体数据信息(如编码、分辨率等)。
5. Signaling过程完成，直接点对点交换流媒体数据MediaStream。
6. (可选)建立RTCDataChannel进行数据交换。

实际应用中，会遇到客户端处于防火墙或NAT之后等复杂情况，这时需要用到[STUN协议](http://en.wikipedia.org/wiki/STUN)或[TURN协议](https://en.wikipedia.org/wiki/Traversal_Using_Relays_around_NAT)等来实现防火墙和NAT穿透，获取真实的网络信息。

由于WebRTC在建立session之后流媒体数据是点对点传输，这样虽然很快，但是如果遇到大量客户端的视频会议等场景，客户端之间需要两两连接，对于客户端带宽要求很高。
这时就需要[MCU(Multipoint Control Unit)](https://en.wikipedia.org/wiki/Multipoint_control_unit)来改变网络拓扑，节省带宽提高性能。

WebRTC在Signaling过程中需要使用其他双向数据协议进行信息交换，如WebSocket或XMPP等。

由于WebRTC标准实现还未最终完全确定，各个浏览器都需开启实验性功能才能使用，可以考虑Chrome插件或者使用Electron封装成桌面程序的形式提供更好的用户体验。
