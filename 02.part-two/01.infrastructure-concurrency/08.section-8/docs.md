---
title: 面试题
taxonomy:
    category: docs
---

#### No.05：大型项目架构分层的原因是什么？

由于软件开发的特殊性，导致在一个团队内只有少量的开发可以彻底了解某一个系统，在人数增加以后，沟通复杂度会呈指数型上升。所以，在系统越来越复杂的时候，就需要拆分团队，每个小团队负责某个或者某些服务，服务之间以 API 的形式互相调用，减少沟通损耗，提升研发效率。

亚马逊的创始人贝佐斯有一个披萨定律：如果两张全尺寸的披萨无法喂饱团队，说明团队应该拆分了。

软件架构本质上是软件维护团队的组织架构，组织上是分小组的，那软件架构上自然就是分层的。

#### No.06：系统如何横向扩张？

一个单体系统进行分布式架构演进的第一步一般就是横向扩张：增加数据库的硬件资源，并将后端代码分散到多台服务器上运行，用一个负载均衡软件对用户流量进行分发。横向扩张通常包括以下步骤：

1. **增加硬件资源**：首先需要增加更多的服务器资源，这可能包括CPU、内存、存储等硬件设备。
2. **代码分散运行**：然后，需要将后端的代码分散到这些新增的服务器上运行。这样，每个服务器都可以独立地处理一部分工作负载。
3. **引入负载均衡器**：为了使用户请求能够均匀地分配到所有的服务器上，需要引入一个负载均衡器。这个负载均衡器可以根据服务器的负载情况，动态地将新的请求分发到空闲的服务器上。

普通的横向扩展使用 Nginx 加上固定数量的后端服务器就可以实现，如果后端压力不定，为了省钱，可以使用 Consul 服务发现，让负载均衡器自己发现并适应不同数量的后端服务器，这样既可以满足业务高峰期的计算资源需求，也可以省钱。

如果业务规模再大，就需要更复杂的 K8s 软件来进行更大规模的计算资源调整了，需要引入外部负载均衡器，设计更大的更复杂的后端集群。而数据库由于拥有单点性，是很难横向扩张的，此时可能需要对后端系统进行拆分，分散数据库的压力，并对高性能需求的模块进行缓存改造，努力顶住压力。

#### No.07：K8s 技术比虚拟机技术先进在哪里？

K8s比虚拟机技术先进的地方主要有：

1. 弹性更强：K8s 能快速启动海量容器，实现更迅速的资源扩展和收缩，摆脱了时间和人工操作的限制，提升了部署速度。
2. 资源利用率更高：K8s 更轻量，能部署更多应用在同一物理服务器上，更精细地控制每个应用的资源占用，节约成本。
3. 管理更方便：K8s 提供全功能 API，可完全自动化运维过程，避免人工错误，适应大规模应用和跨时区数据中心的发展，确保系统稳定性。
