---
title: 概述
taxonomy:
    category: docs
---

本节我们以静山平台为例讲述如何在基础设施并发层面增加系统总容量。

### 静山平台流量持续增大，我们该怎样扩容呢？

假设场景：经过了一段时间的运营，静山电商平台的用户持续增多，在高峰期，同时在线用户来到了 1000 人，每分钟新增订单数 20 个。假设每用户每秒发送 1 个网络请求，则此时后端压力来到了 1000 QPS。

在静山平台中，静态资源完全由云服务商提供，而且由于 CDN 传输的图片之间没有关系，属于纯离散数据，所以理论上一个 CDN 域名就可以拥有无穷大的带宽，这部分的压力我们完全不用担心。而动态 API 请求部分，我们拥有一台跑后端代码的云主机和一台云数据库，这台云主机的单机性能上限为 200 QPS。

### 为何单机只能处理 200 QPS

在一个传统的“Apache + mod_php”的后端服务器单机架构中，QPS（每秒查询率）很难达到非常高的水平。这是因为 Apache 是一个古老的 Web 服务器软件，而 PHP 也是一种阻塞语言。Apache 无法处理超过 5000 的 TCP 连接数，不论使用多少个核心都一样，一旦超过这个限制，客户端就需要等待其它客户端的 TCP 连接数释放后才能和服务器进行通信，在那之前只能等待。

而当 PHP 在执行比较费时的网络和磁盘 I/O 操作时，它会停下来等待操作完成，此时不消耗 CPU 资源，但内存会被持续占用，而且最重要的 TCP 连接数资源会被持续占用。

因此，在使用 Apache 直接对外提供 HTTP/HTTPS 服务的情况下，单机的极限 QPS 大约在 200 左右。

### 何为基础设施并发

像 Apache 一样，由于计算机体系结构的限制，很多软件无法利用多个 CPU 核心，像 Apache、Redis 甚至是 MySQL 都是无法很好地利用多核心硬件的：最新的 AMD EPYC™ 9654 服务器 CPU 已经来到了 192 核心 384 线程，最常见的双路服务器拥有 768 个超线程，这个核心数恐怕 Go 语言都得败下阵来。所以大部分时候，我们都需要将一台数百个核心的物理服务器拆分成多台虚拟机来使用，以提高计算资源利用率。

对静山平台来说，在面临 1000 QPS 的场景时，我们就需要引入负载均衡器了：一台机器跑 Nginx 充当负载均衡器在前面接收客户端 APP 的 HTTPS 请求，然后转身就把这些请求平均分给 5 台真正的 Apache 后端服务器来进行具体的 PHP 代码执行，之后等 Apache 服务器返回结果之后，再将返回值转发给客户端 APP。

使用负载均衡器将请求分发到多台机器上的处理方式就是基础设施并发，其对应的架构图如图 2-1 所示。

![](/media/16889131746258.jpg)
<center>图 2-1 含有负载均衡器的基础设施并发架构图</center>
