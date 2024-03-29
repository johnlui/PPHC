---
title: 缓存的读写策略
taxonomy:
    category: docs
---

在我们设计缓存的技术方案时，最重要的无疑就是缓存的读写策略，而缓存读写策略的核心是两个问题和一个设计。在展开读写策略之前，我们先复习一下大家最常用的缓存使用方法，笔者称之为“原始缓存架构”。

### 原始缓存架构

![](/media/RrQN3a.png)
<center>图 11-1 原始缓存架构</center>

如图 11-1 所示，使用 Redis 实现的原始缓存流程如下：

1. 尝试读缓存
2. 若读到，则返回
2. 若没有读到，则去数据库里查询到结果，将结果存入缓存，并返回数据

看完了原始缓存架构，接下来我们展开讨论一下缓存读写策略的两个问题和一个设计。

### 缓存击穿问题

![](/media/IZJvu2.png)
<center>图 11-2 缓存击穿示意图</center>

在秒杀活动期间，对热门商品的读取是非常高频的，这些高频数据称为“热点数据”。而如果在活动的高峰期，缓存失效了的话，瞬间会有多个请求发现读取不到缓存内容，就会选择直接从数据库中读取，进而数据库被瞬间高压击垮。这个过程就称为“缓存击穿”，如图 11-2 所示。

目前我们主要采用两种方法来应对缓存击穿：

1. 互斥锁/分布式锁：保证同一时间只有一个业务线程更新缓存，如果某个请求未能获取互斥锁，则等待或者直接返回空值/默认值。
2. 缓存不过期：可以使用后台进程定期异步更新缓存，也可以定期检查缓存过期时间，在过期前对数据进行刷新，并设置新的过期时间。

#### 缓存不过期引发的逻辑悖论

缓存不过期并不意味着永远不做数据淘汰，我们依然需要动态地管理缓存里的数据，因为内存空间不是无限大的。这样就引发了一个逻辑悖论：

如果缓存不过期，那在上游调用者看来，缓存就一定要能够在任何时候查询到任何数据，哪怕部分数据慢一点也不要紧，但是不能查询不到。但是，一旦我们对某些数据进行了淘汰，那它们在上游调用者看来就变得不存在了，这可以视为缓存系统的失效。如果我们再引入一个不存在时候的数据库直连机制，那这个架构不又成了原始缓存架构了。

因为有这个悖论的存在，所以缓存不过期必须和其它能够自动过期的缓存配合使用。

### 缓存雪崩问题

缓存雪崩是指在某个时间点，缓存中大量的数据同时失效，导致请求被集中大量发送给了后端的数据库，导致数据库因为瞬间的高负载而崩溃的问题。相比于前面的缓存击穿问题，缓存雪崩的问题更容易发生：因为各种流量都是在秒杀活动开始时同时开始进入高并发状态的，如果缓存超时时间一致，那就很容易出现雪崩问题。

应对这个常见的问题，我们一般按照如下顺序尝试解决。

#### ① 错开过期时间

根据资源类型甚至是资源本身的差异将缓存失效时间错开，例如根据商品的主键 ID 设置它们的过期时间。

#### ② 缓存不过期

和缓存击穿问题一样，我们也可以使用后台进程定期异步更新缓存来彻底解决这个问题。

#### ③ 双 Key 设计

我们对每一条缓存都用两个 key 存两份，一个是主 key，会设置过期时间，一个是备 key，不设置过期时间，它们的 key 不一样，value 值一样。当上游调用者访问不到主 key 时，就直接返回备 key 中的数据，之后只需要等待后台进程生成新的缓存数据即可，在调用者看来，数据没有丢失，甚至连性能都没有下降。

这本质上是空间换时间，用多一倍的内存空间解决缓存失效的问题，虽然确实解决了问题，但是浪费了宝贵的内存空间，只有在小规模的系统或者极其土豪的公司才应该采用。

#### 缓存服务器宕机引发的缓存雪崩

笔者不赞成使用所谓的高可用集群来规避缓存服务器宕机，因为缓存服务在绝大多数情况下并不会因为自己的软硬件故障而宕机，而是因为内存爆了，或者被超大读写压力给打挂了。所以，笔者建议，如果缓存服务器宕机，应该直接返回错误，然后让运维来修。

笔者为什么连挣扎都不想挣扎一下？因为笔者看到此时缓存服务器的单点性：当我们的数据读取流程依赖了缓存服务器时，那他对系统的重要性就和背后的数据库一样了，数据库宕机了你还要对外提供服务吗？完全没有必要，出现了数据丢失反而更麻烦。

### 缓存后台更新设计

前面我们说过了缓存不过期的设计方法，也讨论了缓存不过期引发的逻辑悖论，那么，有没有一种比较好的方法规避问题呢？有，虽然不完美，但是可用——使用消息队列对缓存的更新流程进行解耦。

前面的缓存更新中，我们的查询过程和更新过程是必须在同一个线程内先后进行的，这才是最大的束缚。一旦我们能用消息队列对缓存的工作进行解耦以后，缓存的更新过程一下子就变得自洽了。

1. 每次读取缓存，都判断一下是否即将失效
2. 若即将失效，则通过消息队列向后台的缓存更新进程发送一条“某缓存 Key 需要更新”的消息
3. 在高并发下，短时间内后台进程可能会收到多条消息，但这不重要，因为在真的从数据库读取信息更新缓存之前，执行只需要判断一下过期时间就行了，由于队列的排队执行特性，更新数据操作肯定只会被执行一次

这个方法的巧妙之处就是把阻塞的需要立马处理的“数据已经过期”了的噩耗转化成了一条又一条的消息，而消息的处理是顺序的，只要我们的一个队列处理器能够处理得过来某一类的资源就行，哪怕执行不过来也没关系，理论上缓存 key 相互之前没有关系——极限情况下你可以为每个 key 单独设立一个队列处理器来更新它的缓存数据。

#### 缓存淘汰策略

在缓存服务器内存不足时，我们需要选择一种方法来淘汰旧数据。常见的替换策略有最近最少使用（LRU）、先进先出（FIFO）、最不经常使用（LFU）、最长时间未使用（LRU-TTL）、最少经常使用（MFU）、后进先出（LIFO）、基于成本的淘汰（CBA）、随机淘汰等，下面我们简单描述一下它们分别的适用场景。

1. 最少使用 (LRU)：LRU 策略认为最近被访问过的缓存数据是最有可能再次被访问的，因此优先保留最近被使用过的数据。适用于访问模式较为集中的场景，商品详情和商品库存适合使用此策略。
2. 先进先出 (FIFO)：FIFO 策略按照缓存数据进入缓存的顺序进行淘汰，最早进入缓存的数据最先被淘汰。适用于缓存数据没有特定的访问模式，并且对访问顺序没有特别要求的场景，用户的订单列表等完全个性化的数据适合使用此策略。
3. 最不经常使用 (LFU)：LFU 策略认为被访问次数最少的缓存数据在未来的一段时间内仍然可能不被频繁访问，因此优先淘汰访问次数最少的数据。适用于部分数据非常热门，大部分数据较冷门的场景，商品详情和商品库存也非常适合使用此策略。
4. 最长时间未使用 (LRU-TTL)：该策略基于最近最少使用 (LRU)，但还考虑了缓存数据的过期时间。当缓存数据既长时间未被访问又已经过期时，优先淘汰该数据。
5. 最少经常使用 (MFU)：该策略与最不经常使用 (LFU) 相反，优先保留访问次数最多的缓存数据。认为访问次数多的数据在未来仍然可能被频繁访问，适用于访问次数具有较大波动的场景。
6. 后进先出 (LIFO)：该策略与先进先出 (FIFO) 相反，最后进入缓存的数据最先被淘汰。这个策略有一个十分神奇的应用：在秒杀系统从流量高峰下落的过程中，可以应用此策略来缓存商品信息，可以最大限度地保证热门商品保留在缓存中。
7. 基于成本的淘汰 (CBA)：该策略根据缓存数据的成本信息进行淘汰。成本可以包括缓存数据的存储成本、计算成本、更新成本等，换句话说就是先淘汰数据量更大的 key。
8. 随机淘汰 (Random)：该策略在缓存空间不足时，随机选择一个缓存数据进行淘汰，这比较适用于数据离散的场景，电商秒杀业务应用较少。

### 缓存穿透问题

缓存穿透指的是调用者希望查询一个缓存和数据库中都不存在的数据。缓存穿透的原因有两种：

1. 业务误操作，缓存中的数据和数据库中的数据都被误删除了，所以导致缓存和数据库中都没有数据。
2. 黑客恶意攻击，故意大量访问不存在的数据。

一般情况下，我们需要对非法请求进行快速的判断，并返回空值。而这个判断可能会出问题——因为这个判断需要读取数据库，这就可能出现一种场景：短时间内海量的`select exist`语句被发往数据库，把数据库打崩。

为了应对这个风险，我们可以在业务代码中做限流，或者使用“布隆过滤器”。

#### 布隆过滤器的工作原理

布隆过滤器（Bloom Filter）是一种空间效率极高的概率型数据结构，用于判断一个元素是否在一个集合中。它是由一个很长的二进制向量和一组哈希函数组成。当一个元素插入到布隆过滤器中时，会通过多个哈希函数进行映射，将元素的位置标记为 1；当查询一个元素是否存在时，同样会通过多个哈希函数进行映射，如果所有位置都是 1，那么认为该元素可能存在于集合中，但实际上可能不存在。

布隆过滤器的工作原理如下：

1. 初始化：创建一个长度为 m 的位数组和一个哈希函数列表。
2. 添加元素：将元素通过哈希函数映射到位数组的 n 个位置上，将这些位置的值设置为 1。
3. 查询元素：将元素通过哈希函数映射到位数组的 n 个位置上，如果这些位置的值都为 1，那么认为该元素可能存在于集合中；如果存在某个位置的值为 0，那么认为该元素一定不存在于集合中。
4. 删除元素：由于布隆过滤器不支持删除操作，所以需要重新添加元素来覆盖已删除的元素。

需要注意的是，布隆过滤器存在一定的误判率，即判断一个元素不存在时，实际上可能存在于集合中。我们可以通过调整位数组的长度和哈希函数的数量来降低误判率。

### 缓存预热

在系统规模大到一定程度，例如在活动开始的一瞬间，Redis 缓存的写入流量超过了 1Gbit/S，那么缓存预热将是一种投入小收益大的架构优化方式。通过提前把预期的热数据主动载入到缓存中，可以大大降低秒杀活动开始一瞬间的系统压力：如果业务进程需要等待数据载入缓存，那么就会在一瞬间引发“多级缓存雪崩”，系统在刚开始的 30 秒，压力会非常大。而如果我们提前把热数据载入了内存缓存的话，那活动开始时瞬间的突发流量就会被抹平，等于系统一步就进入了稳定运行状态，对秒杀流程中的所有机器和服务都是一种有效的保护。

### 缓存高可用

经过前面两章分布式数据库的洗礼，想必大家已经了解了“内存缓存同步”是分布式系统的万恶之源了。为什么内存缓存同步这么难搞呢？因为它的性能实在是太高了，内存的读写速度比网络高了两个数量级，延迟更是差了上千倍，所以如果我们需要通过又慢延迟又高的网络来同步内存中的数据，一定要小心翼翼，从架构设计到用户读写的策略，都要保持在分布式缓存系统的“舒适区”内，否则集群的性能和一致性一定会要你好看。

一旦某项数据被放入了缓存，那这项数据大概率首先追求的是高性能，其次是高可用，最后才是节点之间的一致性，所以 Redis 的各种集群方案都是以高性能、高可用为设计目标的。其实直到今天，Redis 集群的依然是遵循最常见的集群设计思路来演进的：主从同步-增量复制-主从切换哨兵-哨兵集群。

基本的设计方法我们在前面的分布式数据库的章节中已经都了解过，下面笔者以 Redis 集群为例，简单阐述一下缓存高可用目前依然没有被完美解决的一些问题。

1. 全量同步/增量同步悖论：全量同步可以获得最完善的一致性，但是需要消耗大量的资源；增量同步的性能更好，但需要提前规划环形缓冲区的内存空间大小，这就让增量同步在事实上只能用于“计划中”的运维事件，例如运维手动触发的主从切换，无法应用在真正的异常——节点宕机场景下。
2. 脑裂问题：缓存业务天然的高性能需求几乎让任何分布式缓存系统必然选择容忍脑裂问题。其实别说是脑裂了，就是基础的主从强一致性目前都没有一种集群架构能完全做到。
3. 故障切换：虽然哨兵集群在理论上解决了单节点宕机后主节点无法切换的大问题，但是哨兵集群也只是“看起来很美”。现实世界中，单节点宕机只是一个小概率事件，更容易出现的其实是网络故障和集群容量爆满问题，这两个问题哨兵集群都无能为力。

这里笔者想引申解释一下为什么 Kubernetes 集群的高可用看起来那么完美：因为 Kubernetes 只把可以做到集群化高可用的部分留在了自己的系统里，真正的单点——网关和流量洪峰都是无法被 Kubernetes 集群很好地处理的，这两个高可用系统中最关键的要素都需要我们在架构的其他部分自己想办法解决。

### Elasticsearch 的缓存设计方案

作为知名内存使用大户，Elasticsearch 的缓存功能十分丰富，我们以页缓存、分片级请求缓存和查询缓存为例，学习一下 Elasticsearch 优秀的缓存设计思想。

#### 页缓存

和 InnoDB 的 Buffer Pool 设计类似，Elasticsearch 会给磁盘上的数据页生成一个内存镜像。当查询数据时，Elasticsearch 首先会检查页缓存中是否已经存在所需的数据，如果存在，则直接返回结果，避免了磁盘 I/O 操作，提高了查询速度。同时，页缓存还可以对写入操作进行缓冲，以提高写入性能。

#### 分片级请求缓存

![](/media/blog-cache-deep-dive-3.png)
<center>图 11-3 Elasticsearch 分片级请求缓存的适用场景</center>

如图 11-3 所示就是分片级请求缓存的应用场景：在查看日志场景下，旧数据的查询条件是不变的，用户刷新页面只是为了获取新数据，那我们把旧数据的查询结果缓存起来，就可以避免每次都“扫描全盘”。这种缓存主要用于加速 Kibana 的运行速度。它会缓存聚合操作的结果，当相同的查询再次出现时，可以直接返回结果，而不需要重新进行搜索和聚合操作。

#### 查询缓存

查询缓存是针对整个查询结果进行缓存的机制。当一个查询请求到达 Elasticsearch 时，Elasticsearch 会先检查查询缓存中是否已经存在相应的结果，如果存在，则直接返回结果，避免了重复执行查询，其背后的哲学思想和上面的分片级请求缓存一致。

基于局部性原理，这个缓存生效的概率要远大于人们直观的想象。
