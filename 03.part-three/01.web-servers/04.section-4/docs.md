---
menu: 三种进程模型的技术特点
title: 测试三种 Apache 进程模型的技术特点
taxonomy:
    category: docs
---

在掌握了上述知识的基础上，我们将以 Apache 作为实验对象，探究它的三种运行方式在高并发场景下的差异，从而推导出 Web Server 领域高并发优化的内功心法。

### Apache 的原始并发模型

Apache 支持三种进程模型：`prefork`、`worker` 和 `event`。在此，我们简要分析这三种模式的优缺点。

1. prefork 进程模式，内存消耗较大。每当接收到新的数据时，需要使用 `select` 模型遍历 `TCP连接数 x 进程数` 次才能找到匹配的进程。在单机数千个 TCP 连接数的场景中，仅寻找进程操作就消耗了一颗 CPU 核心 100% 的时间片，导致单机性能达到极限，无法充分利用更多的 CPU 资源。
2. worker 线程模式，同样使用 `select` 模型来遍历 TCP 请求和线程。其性能上限与 prefork 相同，但内存消耗有所降低，初始 TCP 承载能力略好。然而，在请求数突然增加的场景下，worker 模式开启新线程的速度反而比 prefork 更慢，且基础延迟也比 prefork 模式高，在大部分场景下不如 prefork。
3. event 模式采用与 Nginx 相同的 `epoll` 模型承载，理论上性能与 Nginx 相当。但由于 Apache 通常与 mod_php（插件）模式的 PHP 一起部署，再加上 PHP 阻塞运行的特性，其性能与前两种模式并无显著差异。因此，即使在 event 模式下运行的 Apache，其性能仍然远低于 Nginx 和 php-fpm 的组合。

接下来，我们将使用 jmeter 对 prefork、worker、event 三种模式进行性能测试，并额外验证几个关于 Nginx 和 php-fpm 的悬而未决的问题。

### 测试环境

#### 客户端
  
  * i5-10400 6 核 12 线程
  * 32GB 内存
  * 千兆有线网络
  * 软件环境
    * macOS
    * Java 19.0.1

#### 服务端
  
  * 物理服务器 E5-2682V4 2.5GHz 16 核 32 线程 * 2 （阿里云 5 代 ECS 同款 CPU）256GB RAM
  * 虚拟机 64 vCPU （将物理机全部的 CPU 资源都赋予了虚拟机）
  * 虚拟机内存 32GB
  * 软件环境
    * CentOS Stream release 9
    * kernel 5.14.0-200.el9.x86_64  
    * Apache/2.4.53
    * Nginx/1.20.1
    * PHP 8.0.26
  * PHP 环境：
    * Laravel 9.19
    * 给默认路由增加 sleep 500ms 的代码，模拟数据库、Redis、RPC、cURL微服务等场景
    * 执行 `php artisan optimize` 后测试

#### 相关代码及配置

测试代码如代码清单 4-1 所示。

<center>代码清单 4-1 测试用的 PHP 代码</center>

```php
Route::get('/', function () {
usleep(500000);
return view('welcome');
});
```

Apache prefork 模式的配置文件如代码清单 4-2 所示。

<center>代码清单 4-2 prefork 模式下的 Apache 配置文件</center>

```apache
<IfModule mpm_prefork_module>
    StartServers         100
    MinSpareServers      5
    MaxSpareServers      100
    MaxRequestWorkers    500
    MaxRequestsPerChild  100000
</IfModule>
```

php-fpm 的配置文件如代码清单 4-3 所示。

<center>代码清单 4-3 prefork 模式下的 php-fpm 配置文件</center>

```tcl
pm = static
pm.max_children = 500
```

### 实验设计

我们将测试三种配置下的性能表现差异：

1. Apache 标准模式：prefork + mod_php 插件式运行 PHP
2. Nginx + php-fpm 专用解释器
3. Nginx 作为 HTTP 反向代理服务器，将 HTTP 请求转发给 Apache（采用 prefork 模式 + mod_php 插件式运行 PHP）

#### 请求计划

1. 客户端新线程开启后，每隔 5 秒发送一个请求
2. jmeter 用 50 秒开 5000 个线程，持续压测 100 秒，最大请求 QPS 为 1000

### 为什么这么设计？

单独对比 Nginx 和 Apache 性能的文章很多，数据结果也大同小异，无非是 Nginx 的 QPS 更高，但是 **“为什么 QPS 更高？”** 却没人回答，本次的实验设计就是要回答这个问题。

#### 标准模式：prefork + mod_php

prefork + mod_php 模式下的测试结果如图 4-4 和 图 4-5 所示。

![](https://qn.lvwenhan.com/2022-12-26-16720510490728.jpg)
<center>图 4-4 prefork + mod_php 模式下的 QPS 分布</center>

![](https://qn.lvwenhan.com/2022-12-26-16720510753399.jpg)
<center>图 4-5 prefork + mod_php 模式下的统计信息</center>


#### 高性能模式：Nginx + php-fpm

Nginx + php-fpm 模式下的测试结果如图 4-6 和 图 4-7 所示。

![](https://qn.lvwenhan.com/2022-12-26-16720511122515.jpg)
<center>图 4-6 Nginx + php-fpm 模式下的 QPS 分布</center>

![](https://qn.lvwenhan.com/2022-12-26-16720511252218.jpg)
<center>图 4-7 Nginx + php-fpm 模式下的统计信息</center>


#### Nginx 反向代理 Apache 模式

Nginx 反向代理 Apache 模式下的测试结果如图 4-8 和 图 4-9 所示。

![](https://qn.lvwenhan.com/2022-12-26-16720511439117.jpg)
<center>图 4-8 Nginx 反向代理 Apache 模式下的 QPS 分布</center>

![](https://qn.lvwenhan.com/2022-12-26-16720511638290.jpg)
<center>图 4-9 Nginx 反向代理 Apache 模式下的统计信息</center>


### 结果分析

我们可以很明显地看出，Apache + prefork 的问题在于它对数千个 TCP 连接的处理能力不足。

1. Nginx + fpm 一共发出了 59146 个请求，成功了五万个
2. Nginx + Apache 一共发出了 56464 个请求，成功了五万两千个，比 fpm 还多一些
3. fpm 模式最大 QPS 为 800 但比较稳定，Nginx + Apache 最大 QPS 1000 但不够稳定
4. 至于 Apache 标准模式，显然它的技术架构不足以处理 5000 个 TCP 连接下 1000 QPS 的状况，QPS 低且不稳定，错误率高达 43%

### 结论

1. Nginx 处理海量用户的海量 TCP 连接的能力超群
2. 提升 Apache 性能只需要在前面加一个 Nginx 作为 HTTP 反向代理即可，因为此时 Apache 只需要处理好和 Nginx 之间的少量 TCP 连接，性能损耗较小
3. php-fpm 和 mod_php 在执行 PHP 的时候没有任何性能差异

### epoll 和 prefork 的优劣势对比

#### 优势

1. Nginx 每个 worker 进程可以高效地处理上千个 TCP 连接，同时消耗较少的内存和 CPU 资源。这使得单台服务器能够承载比 Apache 多两个数量级的用户量，相较于 Apache 单机 5K 的 TCP 连接数上限（对应于 2000 个在线用户），这是一个巨大的进步。

2. Nginx 对 TCP 的复用使其非常擅长应对海量客户端的直接连接。根据实际测试，在 HTTP 高并发环境下，Nginx 的活跃 TCP 连接数仅为 Apache 的五分之一，并且随着用户量的增加，复用效果更加显著。

3. 在架构上，基于 FastCGI 网络协议进行架构扩展，可以更轻松地利用多台物理服务器的并行计算能力，从而提升整个系统的性能上限。

#### 劣势

1. 在低负载下，Nginx 的事件驱动特性导致每个请求的响应时长略长于 Apache prefork 模式（14ms vs 9ms）。
