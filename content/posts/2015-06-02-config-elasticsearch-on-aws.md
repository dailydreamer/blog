+++
date = "2015-06-02T20:00:00+08:00"
title = "在AWS上配置ElasticSearch"
tags = ["编程"]
keywords = ["AWS", "ElasticSearch"]
+++

最近在AWS EC2上部署了ElasticSearch，感觉AWS的文档详细但稍显凌乱，在这里总结一下步骤。

首先注册AWS。注意你需要一张支持外币支付的信用卡。

然后创建IAM用户，并配置其权限和密钥对。
可按照[文档](http://docs.aws.amazon.com/zh_cn/AWSEC2/latest/UserGuide/get-set-up-for-amazon-ec2.html)中的步骤来。
注意为了使elasticsearch节点启动后能够自动发现别的节点，你可能需要在这一步为该用户而外设置read-only权限。

之后有两种方案，可以直接部署在[EC2](http://aws.amazon.com/cn/ec2/)上，价格便宜量又足。
也可以部署在[EMR](http://aws.amazon.com/cn/elasticmapreduce/)上，获得Haddop的集群管理能力，方便扩展以及将来部署其它基于Haddop的程序。但是注意使用EMR除了支付EMR的计费还要支付其使用的EC2及S3等的计费。

## 部署在EC2上

进入EC2控制面板启动实例。
如果你希望数据在EC2实例关闭后不丢失需要为其配置挂载EBS卷并将其存储至EBS中，详细见[文档](http://docs.aws.amazon.com/zh_cn/AWSEC2/latest/UserGuide/ebs-using-volumes.html)。

注意EBS卷最好在home/ec2-user/下新建目录挂载，上次我挂载在home/ec2-user/下结果不知道.ssh是存在那里的，然后就连接不上了。。。
挂载完EBS卷后需要更改其权限使得普通用户可以读写文件。
`sudo chmod 777 ./ -R`

之后为其配置EIP来避免每次重启实例后IP地址改变。
EIP是一个固定的共有IP，将其和一个EC2实例的私有IP绑定即可。
这样也方便切换实例而IP不变。

最后即可ssh连接到EC2上然后安装ElasticSearch了。

安装好ElasticSearch之后还需安装[elasticsearch-cloud-aws插件](https://github.com/elastic/elasticsearch-cloud-aws)并配置才能实现自动Discovery。
大致的配置如

```yml
# AWS discovery
cloud.aws.access_key: KEY
cloud.aws.secret_key: KEY

plugin.mandatory: cloud-aws
discovery.type: ec2
discovery.zen.ping.multicast.enabled: false
discovery.ec2.groups: "elasticsearch"

discovery.ec2.availability_zones: "ap-northeast-1a"
cloud.aws.region: "ap-northeast-1"

discovery.ec2.host_type: "public_ip"
network.publish_host: [PUBLIC_IP]

discovery.ec2.ping_timeout: "30s"
```

discovery.ec2.groups是你的EC2集群所在的安全组，注意用这种方式的设置会将必须该安全组中所有节点都启动ElasticSearch服务才行，否则会一直等待。
如果不想这样可以使用Tag设置。

discovery.ec2.availability_zones一定要写对，否则节点会无法互相发现，不知道可以看EC2控制面版中有写。

network.publish_host是该节点的公网IP，可使用绑定的弹性IP。

更加详细的设置可以看[这里](http://www.markbetz.net/2014/03/18/elasticsearch-discovery-in-ec2/)。

有关部署的更加详细的步骤可以参考[这里](http://pavelpolyakov.com/2014/08/13/elasticsearch-cluster-on-aws-part-1-preparing-environment/)。

注意如果弹性IP更换了绑定的实例之后要ssh之前需要将原来保存在本地的host_key删除，使用命令`ssh-keygen -R hostname`,否则会报Host key verification failed。

## 部署在EMR上

安装AWS CLI。
可按照[文档](http://docs.aws.amazon.com/zh_cn/cli/latest/userguide/cli-chap-welcome.html)安装并配置。

然后直接使用Amazon EMR的[bootstrp action脚本](https://github.com/awslabs/emr-bootstrap-actions/tree/master/elasticsearch)即可。
这个仓库中还有其它基于Hadooop的软件的启动脚本，如spark，cascading等。

输入命令(相关参数可自行配置)

```sh
aws emr create-cluster \
--ec2-attributes KeyName="<YOUR_EC2_KEYNAME>" \
--log-uri="<YOUR_LOGGING_BUCKET>" \
--bootstrap-action \
  Name="Install ElasticSearch",Path="s3://support.elasticmapreduce/bootstrap-actions/other/elasticsearch_install.rb" \
  Name="Installkibanaginx",Path="s3://support.elasticmapreduce/bootstrap-actions/other/kibananginx_install.rb" \
  Name="Installlogstash",Path="s3://support.elasticmapreduce/bootstrap-actions/other/logstash_install.rb" \
--ami-version=3.5.0 \
--instance-count=3 \
--instance-type=m1.medium \
--name="TestElasticSearch"
```

即可启动一个3节点的elasticsearch集群，并安装kibana和logstash。

至此，ElasticSearch集群便部署完成了。Enjoy your search~
