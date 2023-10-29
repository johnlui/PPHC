---
title: 分层的网络
taxonomy:
    category: docs
---

读到这里可能有读者会疑惑，既然单机的 Nginx 都顶不住五万 QPS 带来的 TCP 资源开销，那负载均衡器如何顶住呢？因为负载均衡器承载的是比 Nginx 所承载的 TCP 更下面一层的协议：IP 协议。

至此，我们正式进入了网络拆分之路，这条路很难走，但收益也会很大，最终我们将在下一章得到一个 200Gbps 带宽的“软件定义的负载均衡集群”，让我们正式开始。

### 网络是分层的

![](https://qn.lvwenhan.com/2023-01-04-16728298756611.jpg)

<center>图 5-5 经典 TCP/IP 四层网络协议的首部（header）</center>

经典 TCP/IP 四层网络协议的首部（header）会层层累加，最后再统一在网络中传输的，其结构如图 5-5 所示。

如果读者查看过网页的源代码，肯定知道网页背后是一段 HTML 代码文本，这段文本是被层层包裹之后，再在网络中传输的，这段文本就是图 5-5 中的应用数据的一部分（包含在 HTTP 协议之中）。以太网之所以拥有如此之强的扩展性和兼容能力，就是因为它的“分层特性”：每一层都有专门的硬件设备来对网络进行扩展，最终组成了这个容纳全球数十亿台网络设备的“互联网”。最近，这些传统硬件设备的工作越来越多地被软件所定义，即软件定义网络（SDN）。

### 什么是软件定义网络

软件定义网络（Software-Defined Networking，SDN）是一种将网络资源抽象到虚拟系统中的 IT 基础架构方法。 SDN 让 IT 运维团队通过软件抽象出的控制平面来控制复杂网络拓扑中的网络流量，无需手动处理每个网络设备。SDN 的核心思想是将网络控制与网络转发解耦，从而实现网络结构的随时更改，以适应瞬息万变的业务需求。

### 应用数据是什么

应用数据是指网页背后的 HTTP 协议所包含的全部信息。

我们使用 Charles 反向代理软件可以轻松获取 HTTP 协议的详细信息。下面是一个普通的 GET 请求示例。请使用浏览器访问 http://httpbin.org（在尝试时，不要选择 HTTPS 网站）：

#### 请求内容

当你的浏览器发起一个网页请求时，在 TCP 数据流的内部传输的内容就是遵循 HTTP 协议规范的字符串，如代码清单 5-1 所示。

<center>代码清单 5-1 一个 HTTP 请求的字符串内容</center>

```yaml
GET / HTTP/1.1
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/Webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
Cache-Control: max-age=0
Connection: keep-alive
Host: httpbin.org
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54
```

数据解释：

1. 第一行包含三个元素：HTTP 方法、URI（请求路径）、HTTP 版本
2. 之后的每一行以冒号`:`作为分隔符，左边是键，右边是值
3. HTTP 协议中，换行采用的不是 Linux 系统的`\n`，而是与 Windows 相同的`\r\n`

#### 响应内容

而浏览器接收到的服务器返回的内容，依然是在 TCP 数据流内部传输的、遵循 HTTP 协议规范的字符串，如代码清单 5-2 所示。

<center>代码清单 5-2 一个 HTTP 响应的字符串内容</center>

```html
HTTP/1.1 200 OK
Date: Wed, 04 Jan 2023 12:07:36 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 9593
Connection: keep-alive
Server: gunicorn/19.9.0
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>httpbin.org</title>
    <link href="https://fonts.googleapis.com/css?family=Open+Sans:400,700|Source+Code+Pro:300,600|Titillium+Web:400,600,700"
        rel="stylesheet">
    <link rel="stylesheet" type="text/css" href="/flasgger_static/swagger-ui.css">
    <link rel="icon" type="image/png" href="/static/favicon.ico" sizes="64x64 32x32 16x16" />
</head>

<body>
    <a href="https://github.com/requests/httpbin" class="github-corner" aria-label="View source on Github">
    </a>
    ... ... 此处省略一万个字
</div>
</body>

</html>
```

HTTP 响应的基本规则与 HTTP 请求相同，第一行的三个元素分别是协议版本、状态码和状态码的简短解释。唯一的区别在于，返回值中还包含 HTTP body。

1. 在两个换行 `\r\n\r\n` 之前的内容为 HTTP header
2. 在两个换行之后的内容为 HTTP body
3. HTTP body 就是你在浏览器中执行“查看网页源代码”操作时所看到的内容

### HTTP 层之下是 TCP 层

在 HTTP 数据流的外部，包裹着 TCP 首部的数据，其中包含的字段如图 5-6 所示。

![](https://qn.lvwenhan.com/15168101528869.jpg)

<center>图 5-6 TCP 首部包含的字段</center>

#### TCP 首部重要数据描述

1. TCP 首部中最重要的数据是`源端口`和`目的端口`
2. 它们各由 16 位二进制数组成，2^16 = 65536，所以网络端口的范围是 0~65535
3. 我们可以注意到，目的端口号这个重要数据是放在 TCP 首部的，与更下层的 IP 首部、以太网帧首部无关

### TCP 层之下是 IP 层

全球所有公网 IPv4 组成了一个大型网络，这个 IP 网络实际上就是互联网的本体。IPv6 更加复杂，为了便于读者们理解，本节中的示例均采用 IPv4 协议。

在 IP 层中，每台设备都有一个 IP 地址，形如`100.100.100.100`：

1. IPv4 地址范围为 0.0.0.0 - 255.255.255.255
2. 255 为 2 的 8 次方减一，所以我们用八位二进制数表示 0-255
3. 四个八位即为 32 位，4 个字节

### IP 首部包含哪些信息

从上图可以看出，IP 首部有固定长度的 20 字节用于存储 IP 数据包的基本信息：

1. 源地址 32 位（4 个字节）：100.100.100.100
2. 目的地址 32 位（4 个字节）：110.242.68.3
3. 协议 8 位（1 个字节）：内部数据包使用的协议，如 TCP、UDP 或 ICMP（Ping 命令使用的协议）
4. "首部检验和" 16 位（2 个字节）：对 IP 首部的数据进行加工后得到的一串字符串，类似于 MD5，用于验证 IP 首部的数据完整性

**IP 首部最重要的数据是“源 IP 地址”和“目的 IP 地址”。**

### IP 层之下是 MAC 层(物理层)

![](https://qn.lvwenhan.com/15168148429411.jpg)
<center>图 5-7 MAC 帧的数据结构</center>

在物理层中，二进制数据以图 5-7 中所示的格式进行组织，其基本单位被称为“MAC 帧”。MAC 层是交换机工作的地方。

不同的网络设备的 MAC 帧长度可能不同，默认为 1500 字节，即 IP 层的数据会按照这个长度进行分包。当局域网速度无法达到协商速率时，需要进行性能优化（例如 iSCSI 网络磁盘），可以使用“巨型帧”技术，将该数字增加到 10000 字节，以提高网络传输性能。然而，根据笔者的实际优化经验，大多数情况下，巨型帧对网络性能的提升小于 5%，属于一种聊胜于无的优化手段。

前两段目的地址和源地址都是 MAC 地址，形式如 AA:BB:CC:DD:EE:FF，共有六段，每段是一个两位的十六进制数。两位十六进制数转换为二进制就是 8 位，因此 MAC 地址的长度为 8*6 = 48 位，六个字节。

第三段类型字段使用 16 位二进制表示上一层（IP层）的网络层数据包的类型：IPv4、IPv6、ARP、iSCSI、RoCE 等等。
