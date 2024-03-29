---
title: “2000W 行分表”问题
taxonomy:
    category: docs
---

经过上一小节的数据插入测试，我们可以来认真分析一下“2000W 行分表”的问题了。

### 真实世界数据长度及其四层极限

住范儿生产数据库中的电商业务常用大表“订单商品表”，实际单行数据长度为`0.9KB`，与测试结果的 1KB 相差不大，因此测试结果还是能比较符合现实世界的真实情况的。

我们取以下值来计算三层和四层的理论极限：

1. 单页可用数据容量为 14KB。
2. 单行数据为 0.9KB，因此每页最多可以存储 `14/0.9=15.5555`，取整为 15 行数据。
3. 主键类型采用 `int`，页指针长度为 12 字节，因此每页最多可以存储 `14*1024/12=1194.6666`，取整为 1194 个页指针。

则三层 B+ 树的理论极限为：`1194^2 * 15 = 21384540`，大约 2100 万行，与传说中的 2000W 行分表相符。

#### 那么四层到五层呢？

如果需要五层，则行数需要达到 `1194^3 * 15 = 25533140760`，即 255 亿行。这个数字已经超过了 `unsigned int` 的上限 42 亿多，需要使用 `bigint` 作为主键。感兴趣的读者可以自行计算 `bigint` 下五层索引甚至六层、七层、八层的行数极限，笔者在此不再赘述。

### 2100w 行以后真的会发生性能劣化吗？

并不会：**三层索引和四层索引的性能差异微乎其微，2000W 行分表已经过时了！**

实际上，每次 B+ 树增高只会增加两个索引页，修改一个索引页，总共只修改了三个 16KB 的数据页。无论是磁盘 I/O 还是 Buffer Pool 缓存失效，对性能的影响都非常微小：

索引从三层转换到四层，只增加了一次 I/O，绝对性能降低幅度的理论极限仅为 `1/3`。而且在有 Buffer Pool 存在的情况下，性能差异几乎可以忽略不计，只增加了 `1~2` 次比大小的计算成本。

### 那是否意味着不需要再分表了呢？

虽然三层索引和四层索引看起来性能差异不大，但是如果你的单行数据比较大，例如达到了 5KB，仍然建议进行横向分表，这是减少磁盘 I/O 次数的最直接有效的优化方法：

1. 当单行数据为 0.9KB 时，三层树的极限行数是 2100 万。但是当单行数据达到 5KB 时，这个极限将变为仅 285 万行，这可能就不太够了。
2. 数据页具有局部性：每次从磁盘读取都是一整页的数据，因此读取某一行数据后，它 id 附近的数据行也已经在内存缓存中了，读取这一行附近的其他行不会产生磁盘 I/O。减少一行数据的大小，可以提升局部性优势。
3. 在连续读取多行时（例如全表条件查询），巨大的单行数据将迅速丧失“局部性”优势，同时引发磁盘 I/O 次数数量级规模的上升，这就是单行数据较大的表读取速度较慢的原因。

### 何时进行分表？

2017 年的阿里巴巴 Java 开发手册上说，当单表行数超过 500 万行或单表容量超过 2GB 时，推荐进行分库分表。然而，很多技术博文错误地将其解读为：阿里巴巴建议超过 500 万行的表进行分表。

尽管经过实测，每行数据定长 1024 字节，Buffer Pool 配置为 22GB，在单表体积 24GB 的情况下，四层索引和三层索引之间没有性能差异。但现实世界中的数据表并非如此完美：

1. 为了节省空间和保持扩展性，大多数短字符串类型采用 varchar 而非定长的 char，导致最底层的每一页包含的数据行数不一致，使平衡多路查找树不平衡。
2. 生产表经常面临数据删除和更新：同层页之间的双向链表和不同层页之间的单向指针需要频繁变化，同样会导致树不平衡。
3. 使用时间越长的表，ibd 文件中的碎片越多，极端情况下（例如新增 10 行删除 9 行）会使数据页的缓存几乎失效。
4. 磁盘上单文件体积过大不仅在读取 IOPS 上不如多文件，还会引发文件系统的高负载：单个文件描述符也是一种“单点”，大文件的读写性能不佳，还容易浪费大量内存。

那么，如何回答 “何时进行分表” 这个问题呢？很遗憾并没有一个通用的答案，这取决于每个表的读取、新增、更新情况。

虽然在数据库技术层面无法给出具体答案，但从软件工程层面可以得出一个结论：

! 能不分就不分，不到万不得已不搞分表，如果能通过加索引或加内存解决就不考虑分表，分表会对业务代码产生根本性的影响，并带来长期的技术债务。

B+ 树和分表的问题就讨论到这里，下面我们简单了解一下 Buffer Pool 的设计思想和运行规律。
