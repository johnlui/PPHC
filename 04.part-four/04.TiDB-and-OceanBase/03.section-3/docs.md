---
menu: 如何抉择
title: 分布式数据库，应该怎么选？
taxonomy:
    category: docs
---

其实，分布式数据库根本就轮不到你来选：应用准备好了吗？有足够的研发资源吗？性能问题已经大到压倒其他需求了吗？

如果你有一个正在成长的业务，影响最小、成本最低的方案就是选择 Aurora/PolarDB 这种高兼容性数据库，等到这类云数据库的主节点达到性能上限了，再对应用做逐步改造，滚动式地替换每个部分的数据库依赖。

如果压力大到必须换分布式数据库技术方案了，再看看你能获得什么样的分布式数据库呢？无非是在哪个云平台就用哪家呗。

! **没得选，在哪个云平台就只能用哪家。**

### 还记得我们的目标吗？五百万数据库 QPS

在中国，我们现在有下面两种方案可以选择：

1. OceanBase 已经蝉联 TPC-C 数年的全球冠军了，每分钟可以处理 7.07 亿个订单，每秒订单数都已经过千万了，更不要说 QPS 500 万了，所以，如果你用 OceanBase，你的百万 QPS 的高并发系统已经搭建完成了！
2. 如果你用阿里云，那 1 主 4 从，88 vCore 710 GB * 5 个节点的 PolarDB 集群 [可以跑到大约 200 万 QPS](https://cloud.tencent.com/developer/article/2066823)。那离 500 万还有不小的距离呢，不要着急，我们最后一章解决这个问题。
