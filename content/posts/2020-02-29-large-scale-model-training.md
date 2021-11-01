+++
date = "2020-02-29T17:31:29+08:00"
title = "大规模模型训练"
tags = ["AI","架构"]
keywords = ["模型训练","AI"]
+++

大规模模型训练涉及多GPU时的并行、通讯以及模型过大等问题。

# 并行方式

对于n个GPU

- 数据并行：不同的GPU输入不同的数据，运行相同的完整的模型。
- 模型并行：不同的GPU运行模型的不同部分，比如多层网络的不同层；

![数据并行与模型并行](/images/2020-02-29-large-scale-model-training/model_and_data_parallelism.png)

如果模型能够放进单个GPU的显存中，可以使用数据并行加速。

如果模型不能够放进单个GPU的显存中，但可以放进多个GPU显存，可以考虑模型并行。

**模型并行加速：pipeline**

对于模型并行，如果只是简单将模型不同部分放在不同GPU上，对GPU利用率很低。如下图所示。

![串行执行](/images/2020-02-29-large-scale-model-training/sequent.png)

此时可以采用流水线技术，将一个batch数据切分为多个mini-batch，每个GPU运行完一个mini-batch就将数据传输到下一阶段GPU，然后继续运行下一个mini-batch，可成倍提高GPU利用效率。如下图所示：

![流水线执行](/images/2020-02-29-large-scale-model-training/pipeline.png)

GPipe提供了一种模型并行流水线的实现 [https://arxiv.org/abs/1811.06965](https://arxiv.org/abs/1811.06965)

# 通讯算法

对于n个GPU

- Parameter Server：GPU 0将数据分成n份分到各个卡上，每张卡负责自己的那一份batch的训练，得到grad后，返回给GPU 0上做累积，得到更新的权重参数后，再分发给各个卡。


![参数服务器](/images/2020-02-29-large-scale-model-training/parameter_server.png)

- Ring AllReduce：n张以环形相连，每张卡都有左手卡和右手卡，一个负责接收，一个负责发送，循环n-1次完成梯度累积，再循环n-1次做参数同步。分为Scatter Reduce和All Gather两个环节。

![环形传播](/images/2020-02-29-large-scale-model-training/ring_allreduce.png)

Parameter Server是一种更通用的通讯算法，对于很多分布式机器学习算法都适用。但是在deep learning这一通讯量巨大的特定场景中，负责汇总的parameter server容易成为通讯瓶颈。

假设有N个GPU，通信一次完整的参数所需时间为K，那么使用PS架构，其通信成本为 `T=2(N−1)*K`。

因此Ring AllReduce被提出来，分为Scatter Reduce和All Gather两个环节。

Scatter Reduce过程：首先，我们将参数分为N份，相邻的GPU传递不同的参数，在传递N-1次之后，可以得到每一份参数的累积（在不同的GPU上）

All Gather：得到每一份参数的累积之后，再做一次传递，同步到所有的GPU上。

其通信成本仅为 `T=2(N−1)/N*K` 。

**参考**

[https://fyubang.com/2019/07/08/distributed-training/](https://fyubang.com/2019/07/08/distributed-training/)

# PyTorch实现

- DataParallel：基于Parameter server算法，通讯消耗较大，对于master节点会有额外显存消耗，但是改动小实现简单。
- DistributedDataParallel：官方推荐，基于Ring AllReduce算法，不过需要改造启动方式和dataloader。

**参考**

[https://fyubang.com/2019/07/23/distributed-training3/](https://fyubang.com/2019/07/23/distributed-training3/)

# 模型过大显存不足

- 梯度累积：适用于模型可以放进显存，但是想增大batch
- 梯度检查点：适用于模型无法放进显存。前馈时只存储部分结果，反向传播时重新计算
- 模型并行：使用于模型无法放进单个GPU，但可分段放入多个GPU中

**参考**

[https://zhuanlan.zhihu.com/p/48035735](https://zhuanlan.zhihu.com/p/48035735)