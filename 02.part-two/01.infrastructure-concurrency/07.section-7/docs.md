---
menu: 实战：Docker 部署静山平台
title: 实战：使用 Docker 部署静山平台
taxonomy:
    category: docs
---

多年以来，笔者一直认为，新技术是“学”不会的，新技术都是“用”会的，所以笔者在过去学习新技术的过程中，从来不专门规划所谓的学习时间，而是找几个入门的文字或者视频教程，直接开始做真实的可以赚钱的需求。读大学时，笔者会通过做外包的方式学习新技术，工作以后笔者会特意选择用新技术去开发一些非关键，但是需要在生产环境运行的软件。

所以，请大家跟着我一起，使用三种不同的容器组织形式，逐步演进，使用 Docker 和 K8s 部署我们的静山平台。

### 传统思维——打造全功能容器

前文我们说过一种[制作静山平台容器镜像](/part-two/infrastructure-concurrency/section-3#-4)的方法，它使用的就是打造全功能容器的思想。需求如下：

1. 基于 CentOS 8 基础系统镜像构建新镜像
2. 执行命令：yum 安装 Nginx
3. 执行命令：yum 安装 php-fpm 8
4. 执行命令：yum 安装 MySQL 8
5. 执行命令：复制 Nginx 和 php-fpm 的配置文件进入镜像
6. 设置启动命令：启动 php-fpm、Nginx 和 MySQL

#### Dockerfile

我们先新建一个文件夹，然后切换到该目录内：`mkdir -p jingshan && cd jingshan`，然后新建一个名为 Dockerfile 的文件，根据前面的需求写出所需的配置文本，填入其中。可以参考笔者写的代码清单 2-2。

<center>代码清单 2-2 jingshan:0.1 版本镜像的 Dockerfile</center>

```dockerfile
# 基于 CentOS 基础镜像
FROM centos:latest

# 进入yum.repos.d 目录下
RUN cd /etc/yum.repos.d/
# 修改源链接
RUN sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-*
# 要将之前的mirror.centos.org 改成 vault.centos.org
RUN sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*

# 安装 Nginx、PHP8 和 MySQL8
RUN yum -y install epel-release && \
    yum -y install wget && \
    yum -y install nginx && \
    yum -y install php php-fpm php-mysqlnd php-opcache php-mbstring php-json php-gd php-curl php-xml php-zip && \
    yum -y install mysql-server && \
    yum clean all && \
    rm -rf /var/cache/yum/*

# 配置 PHP-FPM
COPY php-fpm.conf /etc/php-fpm.conf

# 配置 Nginx
COPY nginx.conf /etc/nginx/nginx.conf

# 创建 fpm 需要的目录
RUN mkdir -p /run/php-fpm

# 暴露端口
EXPOSE 80

# 启动 PHP-FPM、Nginx 和 MySQL 服务
CMD ["sh", "-c", "php-fpm -F -R && nginx && /usr/sbin/mysqld"]
```

有了 Dockerfile 还不够，我们还需要准备 Nginx 和 PHP 的配置文件，分别如代码清单 2-3 和 2-4 所示。

<center>代码清单 2-3 jingshan:0.1 镜像所需的 Nginx 配置文件 nginx.conf</center>

```nginx
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;
events {
    worker_connections 1024;
}
http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';
    access_log  /var/log/nginx/access.log  main;
    sendfile        on;
    keepalive_timeout  65;
    server {
        listen       80;
        server_name  localhost;
        root         /usr/share/nginx/html;
        index        index.html index.htm index.php;
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   /usr/share/nginx/html;
        }
        location ~ \.php$ {
            fastcgi_pass   127.0.0.1:9000;
            fastcgi_index  index.php;
            fastcgi_param  SCRIPT_FILENAME  $document_root$fastcgi_script_name;
            include        fastcgi_params;
        }
        location ~ /\.ht {
            deny  all;
        }
    }
}
```

<center>代码清单 2-4 jingshan:0.1 镜像所需的 PHP 配置文件 php-fpm.conf</center>

```ini
[global]
pid = /run/php-fpm.pid
error_log = /var/log/php-fpm.log
daemonize = yes

[www]
user = www-data
group = www-data
listen = 127.0.0.1:9000
listen.owner = www-data
listen.group = www-data
listen.mode = 0660
pm = dynamic
pm.max_children = 5
pm.start_servers = 2
pm.min_spare_servers = 1
pm.max_spare_servers = 3
pm.process_idle_timeout = 10s
include = /etc/php-fpm.d/*.conf
```

#### 生成镜像

接下来就可以生成镜像了，执行 `docker build -t jingshan:0.1 .` 命令，稍等片刻，我们就得到了一个镜像，执行 `docker images` 可以看到，如代码清单 2-5 所示。

<center>代码清单 2-5 `docker images` 命令的执行结果</center>

```bash
REPOSITORY      TAG     IMAGE ID        CREATED         SIZE
jingshan        0.1     f2f0eb3801f1    2 minutes ago   566 MB
```

#### 基于镜像启动容器

可以看到镜像已经在我本地成功生成。接下来，基于这个镜像创建一个容器，服务就可以正式跑起来啦！执行以下命令：

`docker run -d -p 10086:80 --name first-jingshan jingshan:0.1`

然后，执行 `docker ps -a` 就可以看到正在运行的容器了，笔者的运行结果如代码清单 2-6 所示（此时该容器已经运行三个小时）。

<center>代码清单 2-6 `docker ps -a` 命令的执行结果</center>

```bash
CONTAINER ID  IMAGE         COMMAND         CREATED      STATUS PORTS           NAMES
33191d4736c9  jingshan:0.1  "sh -c 'ph..."  3 hours ago  Up     3 hours 0.0.0.0:10086->80/tcp   first-jingshan
```

#### 检查运行结果

此时，让我们访问服务器的 10086 端口，可以看到如图 2-8 所示的网页。

![](/media/1698129894.png)
<center>图 2-8 网页访问结果</center>

### 容器思维——多个容器部署在同一个 Pod 内

前面在一个容器内安装所有软件其实不是容器技术的正确使用方式，如果读者需要在生产环境使用 Docker，即便是单机，也推荐使用单台服务器部署 Kubernetes 编排工具，然后使用将多个容器部署在同一个 Pod 内的方式来组织这些容器。

![多个容器部署在同一个 Pod 内](/media/20230823-132220.png)
<center>图 2-7 多个容器部署在同一个 Pod 内</center>

在这种组织方式下，系统架构图如图 2-7 所示。

下面笔者陈述一下思路，复杂而枯燥的 Kubernetes 配置文件就不再列出，感兴趣的读者可以自己尝试。

1. 创建一个 pod，在里面添加 container
2. 添加一个基于官方 Nginx 镜像的 container，修改配置文件以配合 php-fpm，对本地（Pod 内）暴露 `TCP/80` 端口（如果你需要 HTTPS 还需要暴露 443 端口并写入你申请到的 HTTPS 证书和私钥）
3. 添加一个基于官方 php-fpm 镜像的 container，指定根目录到 Nginx 根目录，对本地（Pod 内）暴露 `TCP/9000` 端口
4. 添加一个基于官方 MySQL 镜像的 container，指定初始用户名与密码，对本地（Pod 内）暴露 `TCP/3306` 端口
5. 使用 Kubernetes 的 NodePort 服务对外部网络暴露本 pod 的 80 和 3306 端口

在编写完 Kubernetes 配置文件后，部署这个配置文件，Kubernetes 会自己下载镜像文件，按照你的配置搭建出一个 pod：你可以得到一个类似传统虚拟机一样的“模拟虚拟机”，里面运行了三个软件，分别是 Nginx、php-fpm 和 MySQL，这台模拟虚拟机有独立的 ip，并且它已经将自己的 80 和 3306 端口映射到了宿主机的 ip 上。

需要注意的是，在标准的 Docker 环境或者 Kubernetes 环境下，你无法使用宿主机低于 1024 的端口，这些端口只有使用 root 权限启动的进程才可以监听，所以我们还需要在 Kubernetes 集群之外搞一个公网流量入口，才能真正对公网提供服务，这个部分我们在后面的“负载均衡与网关”的章节再予以详细阐述。

### 平台思维——每个容器一个 Pod

前面是单机 Kubernetes 平台上的部署方法，而如果我们拥有一个多台机器组成的 Kubernetes 集群呢？那就需要按照最新的精细流量管理的方式来组织我们的静山平台了。精细流量管理的基本方法是“层层代理”：

1. 外部负载均衡集群将公网流量分发到 Kubernetes 集群中的某一台服务器上。这可以通过使用如 Nginx、HAProxy 等负载均衡器来实现，但是更推荐直接使用云服务商的负载均衡服务。
2. 随后，流量进入 Ingress Gateway（入口网关）组件，根据网关的配置，将 HTTPS 请求解包，再把 HTTP 请求发送到某个 Pod 的某个端口上。Ingress Gateway 是 Kubernetes 中的一个组件，用于处理外部流量并将其路由到适当的服务或端口。
3. 之后，流量进入该 Pod 内的边车（Sidecar）组件，又根据边车的配置，将流量发送到 Pod 本地的某个特定的端口上，在这个过程中，记录流量的关键信息。边车模式是一种微服务架构设计模式，其中每个主要服务的 Pod 都有一个额外的 Sidecar 容器，用于处理与主要服务相关的辅助功能，如日志记录、监控、流量控制等。

这是目前最流行的大规模 Kubernetes 集群中流量的管理方式，最后的 Sidecar 就是大名鼎鼎的“服务网格”。具体架构如图 2-8 所示。

![每个容器一个 Pod](/media/1698204307.png)
<center>图 2-8 每个容器一个 Pod</center>

