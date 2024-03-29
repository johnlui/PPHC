---
title: 面试题
taxonomy:
    category: docs
---

#### No.37：如何设计一个每秒一万单的秒杀系统？

使用队列可以实现一个每秒一万单的秒杀系统。

1. 用队列来把短期内暴增的数据库压力稍微地均匀分摊到一段时间中
2. 利用队列来降低争抢烈度：用户做秒杀可能一千个人一起抢，但是后端只开了 3 个队列处理器进程，这就变成了 3 个人一起抢，即便还用 MySQL 事务来做原子化操作，死锁的概率就低了很多，代价就是大部分用户需要等待前面的任务都处理完才能拿到自己没抢到的结果。
3. 直接利用 Redis 的原子性来减库存：将库存值直接存入 Redis，只要 Redis 还是单体架构，那对同一个 key 的操作就是原子化的。这么做的好处是完全不依赖数据库了，理论性能会更高，坏处是 Redis 会承担更大的压力，需要设计更复杂的锁机制来减少对 Redis 的压力，此外 MySQL 和 Redis 之间的数据同步也是一个无法忽略的大问题。

#### No.38：分布式缓存如何保证数据一致性？

在分布式缓存系统中，保证数据一致性是最重要的需求。下面是几种常见的保证数据一致性的方法：

1. 缓存失效策略：通过标记失效和重新获取最新数据来避免脏数据的读取。
2. 更新广播：通过消息队列通知变动，使缓存节点及时更新数据。
3. 读写锁：控制对共享资源的访问，读操作并发进行，写操作独占资源。
4. 基于版本号的处理：通过比较版本号来更新缓存。
5. 一致性哈希算法：将数据分散到不同节点，影响部分数据的迁移。
6. 分布式事务：确保操作的原子性和一致性。

#### No.39：如何解决商品超售问题？

商品超售问题可以使用以下策略解决：

1. 库存预留：在接收订单前，先将库存进行预留。如果库存不足无法预留，则不接受新订单。只有当库存足够时才接受订单，并及时更新库存。
2. 并发控制：使用锁机制或者队列等方式，控制对库存的并发访问。当有多个请求同时减少库存时，只允许一个请求成功，其他请求需要等待或者进行退款处理。
3. 保证检查库存操作和下单操作的原子性：在下单过程中，需要保证检查库存和生成订单的操作是原子执行的，避免并发操作导致超售问题。

#### No.40：如何保证消息仅被消费一次？

保证消息仅被消费一次，有以下几种方法：

1. 消费者确认机制（ACK）：消费者在处理完消息后向消息队列发送确认信号，告知队列消息已被正确消费。消息队列收到确认信号后将该消息标记为已处理并删除或移到已消费队列，确保每条消息只被一个消费者处理。
2. 消息去重：消费者通过唯一标识符或业务逻辑判断实现消息去重。记录已处理过的消息标识符，下次消费时先检查该标识符，若已存在则不再处理。
3. 幂等性处理：消费者实现幂等性处理，即使同一条消息被重复消费，也能保证最终结果一致。通过添加幂等性判断和处理机制，在多次处理同一条消息时不会产生错误。
4. 消费者分组：将多个消费者分组成一个消费者组。消息只会被组内某个消费者消费，其他消费者无法接收相同消息，确保同一条消息只被消费者组内处理。
5. 基于事务的消费：使用支持事务的消息队列，将消息的消费与业务逻辑放在一个事务中进行。如果事务提交成功，则消息被标记为已处理；否则回滚事务，确保消息不被重复消费。

#### No.41：如何降低分布式消息队列中消息的延迟？

要降低分布式消息队列中消息的延迟，可以尝试以下几种方法：

1. 异步处理：将操作异步化，提高处理吞吐量，减少等待时间。
2. 批量处理：批量拉取和写入，减少网络开销和调用次数，降低延迟。
3. 负载均衡：合理分配负载，避免过载导致延迟增加。
4. 预取机制：引入预取机制，提前拉取下一批消息，避免等待时间。
5. 消息索引和缓存：在内存中维护索引和缓存，减少访问时间开销。
6. 水平扩展：增加并行度，通过分区或增加消费者数量提升处理能力。
7. 性能监控和优化：定期监控性能指标，针对瓶颈问题进行优化，提高整体性能和效率。

#### No.42：Kafka、Hadoop 和 Clickhouse 背后有哪个相同的基本原理？

Kafka、Hadoop 和 Clickhouse 都是基于分布式系统的架构设计，能够处理大规模的数据。它们将数据分散存储在多个节点上，以实现高可用性和可扩展性。在它们背后有一个相同的基本原理：

**把数据之间的关系降到最低，让数据离散化，这样就可以尽可能地让数据的处理在多个 CPU 核心甚至是多台机器上并行起来。**
