---
menu: TiDB 和 OceanBase
title: 国产分布式数据库双雄 TiDB 和 OceanBase
taxonomy:
    category: docs
chapterNumber: 10
---

TiDB 和 OceanBase 是目前中国 NewSQL 数据库的绝代双骄，关于他们的争论一直不绝于耳。

TiDB 是承袭 Spanner 思想的 NewSQL，对 MySQL 的兼容性一般，基于`key+版本号`的事务控制也比较弱，据说性能比较好，特别是写入性能。

OceanBase 是基于 Shared-Nothing 思想原生开发的分区存储数据库，其每个节点都支持完整的 SQL 查询，相互之间无需频繁通信。OceanBase 还支持多租户隔离，这明显就是为了云服务准备的(无论是公有云还是私有云)，和中小企业无关。另外，OceanBase 对于 MySQL  的兼容性也几乎是 NewSQL 里面最高的，毕竟它需要支持支付宝的真实业务，兼容性是硬性要求，积累了那么多年的老旧业务代码是很难被完全重写的。

下面我们详细对比一下两者的设计思路差异。
