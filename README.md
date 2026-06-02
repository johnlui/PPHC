<p align="center">
  <a href="https://github.com/Pinatra/Pinatra"><img src="./assets/banner.jpg"></a>
</p>

<h3 align="center">《高并发的哲学原理 Philosophical Principles of High Concurrency》</h3>
<h3 align="center">简称 <code>PPHC</code></h3>
<hr>

<p align="center">
<a href="https://trendshift.io/repositories/4395" target="_blank"><img src="https://trendshift.io/api/badge/repositories/4395" alt="johnlui%2FPPHC | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>
</p>

<style>
.book-publication {
    --book-surface: #fbfcfd;
    --book-panel: #ffffff;
    --book-border: rgba(30, 45, 55, 0.12);
    --book-border-soft: rgba(30, 45, 55, 0.08);
    --book-text: #1f2d33;
    --book-muted: #65747b;
    --book-faint: #7c8a91;
    --book-accent: #2f6f83;
    --book-warm: #a65f00;

    margin: 26px 0 64px;
    max-width: 910px;
    padding: 24px;
    border: 1px solid var(--book-border);
    border-radius: 8px;
    background: var(--book-surface);
}

.book-publication-head {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 16px;
    margin-bottom: 22px;
}

.book-publication h3 {
    margin: 0;
    color: var(--book-text);
    font-size: calc(1.35rem - 3px);
    font-weight: 700;
    line-height: 1.35;
}

.book-publication-subtitle {
    margin: 6px 0 0;
    color: var(--book-muted);
    font-size: calc(0.95rem - 3px);
    line-height: 1.7;
}

.book-publication-badge {
    flex: 0 0 auto;
    padding: 4px 10px;
    border: 1px solid var(--book-border-soft);
    border-radius: 999px;
    background: var(--book-panel);
    color: var(--book-accent);
    font-size: calc(0.82rem - 3px);
    font-weight: 700;
    line-height: 1.5;
}

.book-publication-grid {
    display: grid;
    grid-template-columns: minmax(180px, 230px) minmax(280px, 420px) minmax(0, 1fr) minmax(230px, 270px) minmax(0, 1fr);
    align-items: stretch;
    gap: 20px;
}

.book-cover {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100%;
}

.book-cover img {
    width: 100%;
    max-width: 230px;
    border: 1px solid var(--book-border-soft);
    border-radius: 6px;
}

.book-copy {
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 4px 0;
}

.book-copy-title {
    margin: 0 0 12px;
    color: var(--book-text);
    font-size: calc(1rem - 3px);
    font-weight: 700;
    line-height: 1.5;
}

.book-copy ul {
    display: grid;
    gap: 10px;
    margin: 0;
    padding: 0;
    list-style: none;
}

.book-copy li {
    position: relative;
    padding-left: 18px;
    color: #34464d;
    font-size: calc(0.95rem - 3px);
    line-height: 1.65;
}

.book-copy li::before {
    content: "";
    position: absolute;
    top: 0.78em;
    left: 0;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--book-accent);
}

.book-copy b {
    color: var(--book-text);
}

.book-purchase-panel {
    grid-column: 4;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 14px;
    padding: 16px;
    border: 1px solid var(--book-border-soft);
    border-radius: 8px;
    background: var(--book-panel);
}

.book-purchase-qr {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 8px;
    border: 1px solid var(--book-border-soft);
    border-radius: 6px;
    background: var(--book-panel);
}

.book-purchase-qr img {
    width: 100%;
    max-width: 176px;
    aspect-ratio: 1;
    display: block;
}

.book-purchase-content {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 12px;
    height: 100%;
}

.book-purchase-kicker {
    margin-bottom: 5px;
    color: var(--book-faint);
    font-size: calc(0.82rem - 3px);
    font-weight: 700;
    line-height: 1.5;
}

.book-purchase-title {
    color: var(--book-text);
    font-size: calc(1.08rem - 3px);
    font-weight: 700;
    line-height: 1.4;
}

.book-purchase-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin: 10px 0 12px;
}

.book-purchase-tags span {
    padding: 3px 8px;
    border: 1px solid rgba(166, 95, 0, 0.18);
    border-radius: 999px;
    background: #fff8e9;
    color: var(--book-warm);
    font-size: calc(0.78rem - 3px);
    font-weight: 700;
    line-height: 1.45;
}

.book-purchase-price {
    color: var(--book-warm);
    font-size: calc(1.1rem - 3px);
    font-weight: 700;
    line-height: 1.35;
}

.book-purchase-note {
    margin: 7px 0 0;
    color: var(--book-muted);
    font-size: calc(0.9rem - 3px);
    line-height: 1.65;
}

.book-trust-link {
    margin: 0;
    padding-top: 12px;
    border-top: 1px solid var(--book-border-soft);
    color: var(--book-faint);
    font-size: calc(0.88rem - 3px);
    line-height: 1.65;
}

.book-trust-link a {
    color: var(--book-accent);
    text-decoration: underline;
    text-underline-offset: 3px;
}

.book-trust-link a:hover {
    color: var(--book-text);
}

@media (max-width: 980px) {
    .book-publication-grid {
        grid-template-columns: minmax(180px, 220px) 1fr;
    }

    .book-purchase-panel {
        grid-column: 1 / -1;
        display: grid;
        grid-template-columns: minmax(160px, 190px) 1fr;
        align-items: center;
    }
}

@media (max-width: 640px) {
    .book-publication {
        margin: 22px 0 54px;
        padding: 18px;
    }

    .book-publication-head {
        display: block;
        margin-bottom: 18px;
    }

    .book-publication-badge {
        display: inline-block;
        margin-top: 10px;
    }

    .book-publication-grid,
    .book-purchase-panel {
        grid-template-columns: 1fr;
    }

    .book-cover {
        justify-content: flex-start;
    }

    .book-cover img {
        max-width: 230px;
    }

    .book-copy {
        padding: 0;
    }

    .book-purchase-qr img {
        max-width: 200px;
    }
}
</style>

<div class="book-publication">
    <div class="book-publication-head">
        <div>
            <h3>纸质书已经出版</h3>
            <p class="book-publication-subtitle">实体书版本新增了 AI 架构、高可用、分布式理论与工程化体系等内容。</p>
        </div>
        <div class="book-publication-badge">电子工业出版社</div>
    </div>
    <div class="book-publication-grid">
        <div class="book-cover">
            <img src="./assets/book.jpg" alt="《高并发的哲学原理》实体书" />
        </div>
        <div class="book-copy">
            <div class="book-copy-title">纸质书新增内容</div>
            <ul>
                <li>紧跟时代的 <b>"AI 架构"</b> 与前沿技术</li>
                <li>系统化的 <b>"高可用"</b> 与 <b>"分布式理论"</b></li>
                <li>完整阐述了 <b>"工程化体系"</b> 与 <b>"方法论"</b></li>
                <li>更加硬核的 <b>"底层原理"</b> 深挖</li>
                <li>实战项目 <b>"全栈式"</b> 落地</li>
            </ul>
        </div>
        <div class="book-purchase-panel" aria-label="纸质书主推购买渠道">
            <div class="book-purchase-qr">
                <img src="./assets/signature-purchase-qrcode.png" alt="作者直销作者签名版购买二维码" />
            </div>
            <div class="book-purchase-content">
                <div>
                    <div class="book-purchase-title">全新塑封 / 作者签名版</div>
                    <div class="book-purchase-tags">
                      <span>作者直销</span>
                    </div>
                    <div class="book-purchase-price">扫码购买 ¥55</div>
                    <p class="book-purchase-note"></p>
                </div>
                <p class="book-trust-link">
                    <a href="https://item.jd.com/14642937.html" target="_blank">🛒 京东购买 ¥67.6</a>
                </p>
            </div>
        </div>
    </div>
</div>

### 开源版本阅读地址：https://pphc.lvwenhan.com

**pdf 下载链接在网站右上角。**

### 写作目标

本书的目标是在作者有限的认知范围内，讨论一下高并发问题背后隐藏的一个哲学原理——找出单点，进行拆分。

### 内容梗概

我们将从动静分离讲起，一步步深入 Apache、Nginx、epoll、虚拟机、k8s、异步非阻塞、协程、应用网关、L4/L7 负载均衡器、路由器(网关)、交换机、LVS、软件定义网络(SDN)、Keepalived、DPDK、ECMP、全冗余架构、用户态网卡、集中式存储、分布式存储、PCIe 5.0、全村的希望 CXL、InnoDB 三级索引、内存缓存、KV 数据库、列存储、内存数据库、Shared-Nothing、计算存储分离、Paxos、微服务架构、削峰、基于地理位置拆分、高可用等等等等。并最终基于地球和人类社会的基本属性，设计出可以服务地球全体人类的高并发架构。

开源版本共有 12 章，83 篇文章，总计 167547 字。

### 读者评价

> 会上一谈到架构和 I/O，我都想到你的文章。主讲解答清楚和没解答清楚的，都没你的文章清楚。
>
> —— 秋收，于 RubyConf 2023

---

> 像看小说一样把文章都看完了，全程无尿点，作者的脑袋是在哪里开过光，知识储备竟如此扎实
>
> —— 观东山

---

> 非常棒的技术分享！深入浅出，娓娓道来，让我想起了那本 csapp。
>
> —— drhrchen

---

> 写得真好，膜拜！作者愿意出书吗，一定买！
>
> —— bean

---

> 拜读了！应该算是架构顶级总结！！
>
> —— 雨山前

---

> 看完了 博主好厉害 学习到了各种骚技巧 和知识 膜拜
>
> —— evanxian

---

> 写的太好了，不仅充满了理工科的严谨较真，也充满了文科的浪漫
>
> —— 一秒

---

> 写得很好，视角也是我喜欢的，站在地球表面，述事宏大，思维自信。
>
> —— 纳秒时光

---

> 全部看完，博主太强了，很受启发
>
> —— Bruce

---

> 棒
>
> —— JuniaWonter


### 作者信息：

1. 姓名：吕文翰
2. GitHub：[johnlui](https://github.com/johnlui)
3. 职位：住范儿创始成员，CTO，监事

![公众号](https://lvwenhan.com/content/uploadfile/202301/79c41673579170.jpg)

#### 高并发系统处理经验

1. 2017 年维护的单体 CMS 系统顶住了每日两百万 PV 的压力
2. 2020 年优化一个单机 PHP 商城顶住了 QPS 1000+ 的压力
3. 2021 年设计的分布式电商秒杀系统在实际业务中跑到了最高一分钟 GMV 500 万，QPS 10000+


### 目录

<img src="./assets/table.jpg">

### 精彩图片摘录

<img src="./assets/p0.jpg">

<img src="./assets/p1.jpg">

<img src="./assets/p2.jpg">

<img src="./assets/p3.jpg">

<img src="./assets/p4.jpg">

<img src="./assets/p5.jpg">


### 版权声明

本书版权归属于[吕文翰](https://github.com/johnlui)，采用 [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode.zh-Hans) 协议开源，供 GitHub 平台用户免费阅读。

<a rel="license" href="https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode.zh-Hans"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-nd/4.0/88x31.png" /></a>
