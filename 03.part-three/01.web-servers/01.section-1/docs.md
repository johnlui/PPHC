---
menu: Apache
title: Apache——最成功的开源软件之一
taxonomy:
    category: docs
---

Apache HTTP Server 是一个可以和 Kernel、MySQL 并列的最成功的开源软件之一，它的历史就是万维网的历史，就是互联网的历史。

### 互联网的第一声啼哭

1993 年，淮河以南长江以北的丘陵地带有一个名为梨树的生产小队，小队里有一片长条形的池塘，在池塘畔的土坯房里，笔者出生了。同一年，在太平洋的另一头，美国伊利诺伊大学香槟分校内，美国国家超级电脑应用中心（NCSA）相继发布了三个软件：Mosaic 浏览器、CGI 协议、HTTPd Web Server 软件，互联网出生了。

1991 年的 Tim Berners-Lee 创造的那个胚胎，在孕育了两年之后，互联网呱呱坠地了。

### CGI 和 HTTPd 的创造者是一个年仅 20 岁的年轻小伙

当时，Robert McCool 是 NCSA 实验室的一名本科生，他在大二到大三期间成为了 HTTPd 和 CGI 协议的主要作者之一。然而，当他大三结束后，他离开了 NCSA 实验室，导致 HTTPd 失去了维护者。随后，一个由八人组成的小组希望继续开发 NCSA HTTPd，以维护 Web Server 的发展，他们自称为 Apache 小组。随后，该小组发布了从 NCSA HTTPd 衍生而来的 Apache 开源 Web Server。

1995 年 8 月时，几乎所有的网站都使用着 NCSA HTTPd。然而，到了 1996 年 4 月，Apache 就超过了 NCSA HTTPd，成为市场占有率第一的 Web Server。这一地位保持了整整 20 年，直到 2016 年被 Nginx 超越。

那么，为什么 Robert McCool 要离开实验室呢？原来，他的学长、Mosaic 的主要作者之一 Marc Andreessen，于 1993 年 12 月本科毕业后创办了网景公司，并成功挖走了他。不仅如此，这位学长还挖走了 NCSA 互联网三件套几乎所有的核心开发者。

### Apache：驱动人类历史上大部分流量的开源软件

自浏览器诞生以来，Apache Web Server 与 Perl、PHP 两种主流编程语言紧密合作，传输了互联网上绝大多数的流量。即使在 Java 崭露头角的时代，Java 仍然与 Tomcat 和 Apache 配合多年，直到被 Nginx 超越。Apache 可以与几乎所有常见的后端编程语言配合使用，相较于 Nginx，它拥有更丰富的功能，并且稳定性极佳，远超过 Nginx + php-fpm 的组合。

这一切使得 Apache Web Server 成为了最成功的开源软件之一，为人类创造了巨大的价值。

然而，由于其陈旧的软件架构和对向前兼容性的需求，Apache 最终不得不因为性能较差而让出了第一名的位置。

### Apache 基金会——最成功的开源软件基金会

Apache 邮件小组在早期得到了 IBM 的大力支持，IBM 将 Apache HTTPd 内置到了自家的商用产品中，并为 Apache HTTPd 开源软件提供了资金和人力资源的支持。随后，在 2002 年，Apache Group 成立了一个专门用于孵化新的开源软件的项目 Apache Incubator。同年 11 月，该项目接收了第一个软件：Java 构建工具 ant。在接下来的几年里，Java 生态开源软件相继入驻，直到 2008 年 Hadoop 的到来，正式将 Apache 软件基金会推向了巅峰。

如今，Apache 已经孵化出了多个十分流行的开源软件，涵盖了从 Java 运行容器 Tomcat 到项目全生命周期管理工具 Maven，再到代码管理工具 Subversion（SVN），以及日志工具类库 Log4j、Web 框架 struts、开源搜索引擎 Lucene、消息中间件 ActiveMQ、RocketMQ、JVM 编程语言 Groovy、多语言软件开发 IDE NetBeans、磁盘大数据处理框架 Hadoop、内存大数据处理框架 Spark、事实大数据处理框架 Flink、分布式消息队列 Kafka、分布式数据库 Cassandra、超大规模磁盘存储引擎 HBase、分布式服务框架 Dubbo、分布式中间件 Zookeeper 等等各种技术领域。这些软件都是其所在领域的绝对领导者，为全球范围内的互联网和软件企业节约了大量的研发成本。
