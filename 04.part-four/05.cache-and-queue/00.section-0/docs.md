---
title: 概述
taxonomy:
    category: docs
---

电商秒杀业务的特点是短时间内用户量和用户点击量都暴增，最高可能达到百倍之多。虽然电商秒杀业务的流量会在短时间内暴增，但是流量越大，这些请求的“局部性”就越强——被抢购的商品会越集中，这个商品就越适合用缓存技术来承载，缓存的作用就会越大。

### 电商秒杀业务的特点

电商秒杀业务最大的特点就是请求数会突然暴增，因为用户会停在界面上等待，一旦活动开始，就开始疯狂下单付款，晚了就售罄了。正因为秒杀的突然性，让它在技术上有了如下的特点：

1. 客户端数量会突然暴增，对应的就是 TCP 连接数和 API 请求数的突然暴增
2. 流量集中在少部分商品上
3. 下单压力会变得特别大，对库存管理和数据库写入能力造成了严重威胁

### 缓存技术的底层原理

缓存技术的底层原理依然是老套的“空间换时间”和“内存比磁盘快”。

宏观上，我们多使用了一些内存空间，提升了系统的响应速度，这就是空间换时间。此外，由于内存必然比磁盘的读写速度快、读写延迟低，所以我们只要把热门数据和计算结果存储在内存中，就可以提高数据的读取速度，进而提升系统总体性能。
