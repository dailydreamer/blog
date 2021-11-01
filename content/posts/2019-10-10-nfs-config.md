+++
date = "2019-10-10T19:25:41+08:00"
title = "如何配置NFS"
tags = ["编程"]
keywords = ["NFS"]
+++

NFS 全称 Network File System 网络文件系统，用于像访问本地文件系统一样访问远程文件系统。本文介绍如何在服务器上配置 NFS，默认使用Ubuntu 16.04系统。

## Server端

安装nfs server

```bash
sudo apt install nfs-kernel-server
```

编辑 `/etc/exports`，参考 [https://linux.die.net/man/5/exports](https://linux.die.net/man/5/exports)

```bash
/data xxx.xxx.xxx.*(rw,sync,no_root_squash,all_squash,anonuid=1000,anongid=1000)
```

格式为：导出数据盘 客户端ip地址（配置项）

其中：

rw 代表读写权限

sync 表示同步读写

no_root_squash 表示client保留对server共享文件夹的root权限

all_squash 表示client其他用户被map到一个匿名用户

anonuid 和 anongid 指定了匿名用户的uid和gid

通过配置all_squash和指定匿名用户为nfs server上的常用用户，可以省去很多权限问题。

然后重启nfs server端

```bash
sudo systemctl restart nfs-kernel-server
```

## Client端

安装 nfs client

```bash
sudo apt install nfs-common
```

mount远程nfs

```bash
sudo mount xxx.xxx.xxx.xxx:/data /data
```

如果是老版本的nfs server可以使用如下选项

```bash
sudo mount -t nfs -o vers=3,timeo=600,nolock xxx.xxx.xxx.xxx:/data2 /data2
```

如果需要配置启动挂载可以编辑 `/etc/fstab`，

```bash
# nfs auto mount
xxx.xxx.xxx.xxx:/data /data nfs defaults 0 0
xxx.xxx.xxx.xxx:/data2 /data2 nfs vers=3,timeo=600,nolock 0 0
```

可以使用 `sudo mount -a`使改动立即生效

然后即可在客户端上访问nfs server数据了