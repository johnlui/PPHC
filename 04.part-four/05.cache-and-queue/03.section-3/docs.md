---
menu: 队列
title: 秒杀系统的核心——队列
taxonomy:
    category: docs
---

有了前面几章数据库部分的铺垫，相信读者现在都认识到了，在库存需要一单一单地减掉的情况下，这个减库存的过程在宏观上必然有一个单点——这个单点需要把所有的需求排成队，一个一个地执行完成。

在一个没有经过任何复杂架构设计的电商系统中，扣库存需要基于 MySQL 中`update`语句自带的事务性来实现的排队：每一句`update`在执行的时候，MySQL 都会给它自动包裹成一个事务来执行。MySQL 的事务确实非常的严谨，执行不会出错，但是性能实在是不行，而且如果瞬间并发大量有冲突的事务，还会引发死锁，导致连接数暴涨，数据库服务挂掉。

怎么解决这个问题呢？很简单，用单独设计的队列把这个“单点”的工作接管过来，让 MySQL 能够舒服又高效地运行。

### 队列解决下单性能问题

在团购秒杀活动刚开始的几分钟，下单压力确实很大，但是几分钟后压力就降到了比日常平峰期高不了多少的水平。所以，我们可以用队列来把短期内暴增的数据库压力稍微地均匀分摊一下，让库存的扣减和订单的生成稍微等待一下，我们的数据库就不会挂，秒杀活动就能够正常地进行下去。

### 队列解决超售问题

超售问题的本质是计算机经典的“多线程”问题——在宏观上，同一个时刻有两个线程需要对同一个变量分别执行“减去 1”这个运算，如果我们不对这种并发行为做处理，最终可能两个线程都执行成功了，但是这个变量一共也只被减去了 1，而不是预期的 2。

这个问题用队列也能解决，而且有两种解决方案：

1. 利用队列来降低争抢烈度：用户做秒杀可能一千个人一起抢，但是后端只开了 3 个队列处理器进程，这就变成了 3 个人一起抢，即便还用 MySQL 事务来做原子化操作，死锁的概率就低多了，代价就是大部分用户需要等待前面的任务都处理完才能拿到自己没抢到的结果。
2. 直接利用 Redis 的原子性：将库存值直接存入 Redis，只要 Redis 还是单体架构，那对同一个 key 的操作就是原子化的。这么做的好处是完全不依赖数据库了，理论性能会更高，坏处是 Redis 会承担更大的压力，需要设计更复杂的锁机制来减少对 Redis 的压力，此外 MySQL 和 Redis 之间的数据同步也是一个无法被忽略的大问题。