---
title: 从业务分库到微服务
taxonomy:
    category: docs
---

前面我们说过，微服务的拆分方式，反映的是其背后技术团队的组织方式。

那，技术团队的组织方式是什么决定的呢？

是由系统内各部分天然的内聚性决定的：用户相关的业务和商品相关的业务都有很强的内聚性，它们之间不会主动发生关联，但它们会分别和订单发生关联。

### 数据库调用推演

我们用商品下单处理流程来推演一个电商订单的生命周期内对用户、商品、订单三个部分数据库的读写情况。

1. 搜索：商品数据库-读
2. 点进详情：商品数据库-读，用户数据库-读（地址、会员）
3. 立即购买：商品数据库-读，用户数据库-读，订单数据库-写
4. 支付：订单数据库-读写，用户数据库-读
5. 商家后台查看并处理订单：订单数据库-读写，用户数据库-读，商品数据库-读

我们可以看出，大部分情况下，每一步都只有一个主要的微服务被需要，其它微服务都处于辅助地位：只读，且大部分都是单点读取。这就为我们降低了数据库单点的负载——只要把这三个微服务部署到三个独立的数据库上，就可以通过 API 调用的形式降低单个数据库的极限 QPS。

### 微服务背后的哲学

既然我们不能把拼多多和淘宝的系统称作一个系统，那么，在拼多多和淘宝系统内，肯定还可以基于类似的逻辑继续拆分：

1. 在大量调用的 API 中，一次携带了数据写入的请求一定只会对单个微服务进行写入，但会对多个微服务进行数据读取
2. 如果某个头部 API 请求会对两个微服务系统进行写入，那说明微服务的划分出了问题，需要调整系统结构划分

把几乎不相互写入的数据拆到两个数据库上，这种组织形态在人类社会随处可见：两个国家的人分别在自己国家申请护照，他们有时也可以到对方国家内的本国领事馆申领本国护照；两个村的人各自在本村的井里打水，有时也可以不怕麻烦地去隔壁村的水井里打水；你每天早上都用滴滴打车上班，万一滴滴打不到车你还可以用高德来补救...

### 微服务照进现实

微服务的拆分思想相信大家都理解了，下面我们来解决现实问题。

如果你真的成为了“设计百万 QPS 系统”的架构师，相信我，你第一个想到的，一定是“削峰”。
