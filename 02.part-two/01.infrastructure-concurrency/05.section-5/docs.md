---
menu: Spring Cloud
title: Spring Cloud 是微服务的中间态
taxonomy:
    category: docs
---

在后端部署架构从虚拟机向 Kubernetes 进化的过程中，Java 生态诞生了一款功能强大的微服务框架—— Spring Cloud。该框架在代码层面提供了微服务架构中最重要的注册与发现、负载均衡、容错处理、远程调用和链路追踪等工具和组件，使得在虚拟机时代，我们能够基于传统的虚拟机技术或者云计算虚拟机技术，利用普通的二层以太网，搭建出一套可用的微服务调用框架。

### Spring Cloud 并不是微服务架构的价值所在

需要注意的是，Spring Cloud 和 Kubernetes 所实现的这些价值，并不是微服务相比于单体应用的价值，微服务的价值是

1. 整体系统容量更大
2. 不同的微服务之间可以独立部署和快速迭代，这可以将大团队拆成小团队，提升宏观上的软件质量

Spring Cloud 其实是在弥补微服务架构的弱点。

### Spring Cloud 和 Kubernetes 关于微服务需求的对应关系

在架构上，微服务系统的需求是不会变的，所以 Spring Cloud 和 Kubernetes 有着几乎一一对应的解决方案，具体对应关系如表 2-1 所示。

<center>表 2-1 Spring Cloud 和 Kubernetes 不同组件的对应关系</center>

| 功能           | Kubernetes                | Spring Cloud         |
| -------------- | ------------------------- | -------------------- |
| 弹性伸缩       | Autoscaling               | N/A                  |
| 服务发现       | KubeDNS / CoreDNS         | Spring Cloud Eureka  |
| 配置中心       | ConfigMap / Secret        | Spring Cloud Config  |
| 服务网关       | Ingress Controller        | Spring Cloud Zuul    |
| 负载均衡       | Load Balancer             | Spring Cloud Ribbon  |
| 服务安全       | RBAC API                  | Spring Cloud Security|
| 跟踪监控       | Metrics API / Dashboard   | Spring Cloud Turbine |
| 降级熔断       | N/A                       | Spring Cloud Hystrix |
