---
menu: 基础设施并发
title: 基础设施并发：虚拟机与 Kubernetes（K8s）
taxonomy:
    category: docs
chapterNumber: 2
---

基础设施并发，全称为“基础设施并发管理”，指的是在计算机系统中同时有多个应用程序或任务在共享和访问计算机系统的各种资源（比如 CPU、内存、网络等）的情况下，保证这些资源的正确使用和公平分配的技术能力。笔者想用另一个技术概念来帮助大家理解基础设施并发：

**基础设施即服务**：IAAS（Infrastructure as a Service）是一种云计算服务模型，它提供了基础设施资源，如计算、存储和网络等。用户可以根据需要灵活地使用这些资源，而无需关心底层的硬件和软件实现细节。IAAS 通常由云服务提供商提供，用户只需通过互联网访问这些服务即可。

通俗来说，精确地管控每个进程所能使用的 CPU、内存、网络、磁盘等物理计算资源就是基础设施并发管理的目标，它可以让分布式系统更加均衡、更加稳定，减少资源浪费，提升系统的总容量。
