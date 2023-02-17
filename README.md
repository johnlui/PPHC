<p align="center">
  <a href="https://github.com/Pinatra/Pinatra"><img src="./assets/banner.jpg"></a>
</p>

<h3 align="center">《高并发的哲学原理 Philosophical Principles of High Concurrency》</h3>
<h3 align="center">简称 <code>PPHC</code></h3>
<hr>

### 写作目标

本书的目标是在作者有限的认知范围内，讨论一下高并发问题背后隐藏的一个哲学原理——找出单点，进行拆分。

### 内容梗概

我们将从动静分离讲起，一步步深入 Apache、Nginx、epoll、虚拟机、k8s、异步非阻塞、协程、应用网关、L4/L7 负载均衡器、路由器(网关)、交换机、LVS、软件定义网络(SDN)、Keepalived、DPDK、ECMP、全冗余架构、用户态网卡、集中式存储、分布式存储、PCI-E 5.0、全村的希望 CXL、InnoDB 三级索引、内存缓存、KV 数据库、列存储、内存数据库、Shared-Nothing、计算存储分离、Paxos、微服务架构、削峰、基于地理位置拆分、高可用等等等等。并最终基于地球和人类社会的基本属性，设计出可以服务地球全体人类的高并发架构。

全书共八万多字。

### 目录

1. 找出单点，进行拆分
2. Apache 的性能瓶颈与 Nginx 的性能优势
3. 基础设施并发：虚拟机与 Kubernetes（k8s）
4. 隐藏在语言背后的魔鬼：运行架构为何会成为性能瓶颈
5. 拆分网络单点(上)：应用网关、负载均衡和路由器(网关)
6. 拆分网络单点(下)：SDN 如何替代百万人民币的负载均衡硬件(网关、LVS、交换机)
7. 最难以解决的单点：数据库以及它背后的存储
8. 将 InnoDB 剥的一丝不挂：B+ 树与 Buffer Pool
9. 细数四代分布式数据库并拆解 TiDB 和 OceanBase（主从、中间件、KV、计算与存储分离、列存储、CAP定理）
10. 理论无限容量：站在地球表面

### 作者信息：

1. 姓名：吕文翰
2. GitHub：[johnlui](https://github.com/johnlui)
3. 职位：住范儿 CTO

![公众号](https://lvwenhan.com/content/uploadfile/202301/79c41673579170.jpg)

### 在线浏览
streamlit apps: https://sherry0429-pphc-main-p0otkm.streamlit.app/
create by [sherry0429](https://github.com/sherry0429)

### 版权声明

本书版权归属于[吕文翰](https://github.com/johnlui)，供 GitHub 平台用户免费阅读。
