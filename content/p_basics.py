# -*- coding: utf-8 -*-
"""第 1–5 章：Linux / SQL / 大数据 / CDC与湖仓 / Paimon是什么"""


def build(code, term, exercise):
    B = {}

    # ------------------------------------------------------------------ 第 1 章
    B["pages/01-linux.html"] = """
<span class="eyebrow">第 1 章 · 开始</span>
<h1>Linux 与终端</h1>
<p class="lead">大数据工具几乎都在命令行里跑。这一章带你掌握最少够用的终端操作：命令、路径、解压、环境变量、运行脚本。不难，但缺了会处处卡。</p>

<h2>什么是终端和命令行</h2>
<p><strong>终端（Terminal）</strong>是一个让你用「打字」而不是「点鼠标」来操作电脑的窗口。你输入一行<strong>命令</strong>，回车，电脑执行并返回结果。大数据工具（Flink、Spark、Paimon）大多通过命令行启动和操作，所以这是绕不开的第一关。</p>
<div class="callout note">
<span class="tag">在哪打开终端</span>
<p>macOS：打开「终端」App。Windows：推荐装 WSL2（Windows Subsystem for Linux）或 Git Bash，获得接近 Linux 的体验。Linux：自带。本教程的命令都以 Linux/macOS 为准。</p>
</div>

<h2>必会的基础命令</h2>
<div class="table-wrap">
<table>
<thead><tr><th>命令</th><th>作用</th><th>例子</th></tr></thead>
<tbody>
<tr><td><code>pwd</code></td><td>显示当前所在目录</td><td><code>pwd</code></td></tr>
<tr><td><code>ls</code></td><td>列出目录里的文件</td><td><code>ls -l</code>（详细）<code>ls -a</code>（含隐藏）</td></tr>
<tr><td><code>cd</code></td><td>进入某个目录</td><td><code>cd /tmp/paimon</code></td></tr>
<tr><td><code>mkdir</code></td><td>新建目录</td><td><code>mkdir data</code></td></tr>
<tr><td><code>cat</code></td><td>查看文件内容</td><td><code>cat conf.yaml</code></td></tr>
<tr><td><code>grep</code></td><td>在文件里搜关键词</td><td><code>grep ERROR log.txt</code></td></tr>
<tr><td><code>cp</code> / <code>mv</code> / <code>rm</code></td><td>复制 / 移动 / 删除</td><td><code>cp a.jar lib/</code></td></tr>
<tr><td><code>tar</code></td><td>解压安装包</td><td><code>tar -xzf flink.tgz</code></td></tr>
</tbody>
</table>
</div>
""" + code("bash", "示例：从零建目录、进入、查看", """# 看看我现在在哪
pwd

# 在 /tmp 下建一个工作目录并进去
mkdir -p /tmp/paimon-lab
cd /tmp/paimon-lab

# 建一个文件并写入内容（> 表示写入，>> 表示追加）
echo "hello paimon" > note.txt

# 查看文件
cat note.txt

# 列出当前目录（-l 显示详情）
ls -l""") + """

<h2>理解「路径」</h2>
<p>路径就是文件的地址。两种写法：</p>
<ul>
<li><strong>绝对路径</strong>：从根目录 <code>/</code> 开始，如 <code>/tmp/paimon-lab/note.txt</code>。在哪都能用。</li>
<li><strong>相对路径</strong>：相对「当前目录」，如 <code>./note.txt</code>（当前目录下）、<code>../</code>（上一级）。</li>
</ul>
<div class="callout tip">
<span class="tag">小技巧</span>
<p>打命令时按 <kbd>Tab</kbd> 键可自动补全文件名/路径，少打字少出错。按 <kbd>↑</kbd> 可调出上一条命令。</p>
</div>

<h2>环境变量与 PATH</h2>
<p><strong>环境变量</strong>是系统里的一些「全局设置」。装 Flink、Java 时经常要设两个：</p>
""" + code("bash", "设置 JAVA_HOME 和 PATH", """# 告诉系统 Java 装在哪
export JAVA_HOME=/usr/lib/jvm/java-11

# 把 Java 的 bin 加进 PATH，这样就能直接敲 java 命令
export PATH=$JAVA_HOME/bin:$PATH

# 验证
java -version""") + """
<p><code>PATH</code> 是一串目录，你敲命令时系统会去这些目录里找对应的程序。把要写进 <code>~/.bashrc</code> 或 <code>~/.zshrc</code> 里，重开终端才会永久生效。</p>

<h2>解压安装包</h2>
<p>大数据软件常以 <code>.tgz</code> / <code>.tar.gz</code> 形式发布，用 <code>tar</code> 解压：</p>
""" + code("bash", "解压并进入目录", """# x=解压 z=gzip f=指定文件
tar -xzf flink-1.20.0-bin-scala_2.12.tgz

# 解压后进去看看
cd flink-1.20.0
ls""") + """

""" + exercise("练习 1-1", "<p>请用命令完成：在 <code>/tmp</code> 下创建目录 <code>lab</code>，进入它，创建一个内容为 <code>test</code> 的文件 <code>a.txt</code>，然后查看它。</p>",
        code("bash", "参考答案", """mkdir -p /tmp/lab
cd /tmp/lab
echo "test" > a.txt
cat a.txt""")) + """

<div class="callout tip">
<span class="tag">本章目标</span>
<p>能打开终端、切换目录、查看文件、解压安装包、设置环境变量、照着教程执行命令。够用即可，不必深入 shell 编程。下一章进入数据世界的通用语言——SQL。</p>
</div>
"""

    # ------------------------------------------------------------------ 第 2 章
    B["pages/02-sql.html"] = """
<span class="eyebrow">第 2 章 · 打基础</span>
<h1>SQL 与数据建模</h1>
<p class="lead">SQL 是你和数据对话的语言，Paimon 的建表、写入、查询全靠它。这一章带你掌握够用的查询能力，并理解表、主键、分区、ETL、数仓这些核心概念。</p>

<h2>表是什么</h2>
<p>一张<strong>表（Table）</strong>就像 Excel 的一张工作表：</p>
<ul>
<li><strong>列 / 字段（Column）</strong>：表的每一项属性，如 <code>order_id</code>、<code>amount</code>。</li>
<li><strong>行 / 记录（Row）</strong>：一条具体数据，如「订单 1001，金额 200」。</li>
<li><strong>数据类型</strong>：每列有类型，如整数 <code>INT</code>、长整数 <code>BIGINT</code>、字符串 <code>STRING</code>、小数 <code>DECIMAL</code>。</li>
</ul>
""" + code("sql", "建一张订单表", """CREATE TABLE orders (
    order_id   BIGINT,
    user_id    BIGINT,
    city       STRING,
    amount     DECIMAL(10, 2),
    created_at TIMESTAMP
);""") + """

<h2>核心查询：SELECT</h2>
<p>查询是 SQL 用得最多的能力。先掌握这四件事：<strong>选列、过滤、聚合、排序</strong>。</p>
""" + code("sql", "查询：选列 + 过滤", """-- 从订单表取 user_id 和 amount
-- 只要北京、金额大于 100 的订单
SELECT user_id, amount
FROM orders
WHERE city = 'Beijing' AND amount > 100;""") + """
""" + code("sql", "聚合：分组统计", """-- 按城市统计：订单数、总金额、平均金额
SELECT
    city,
    COUNT(*)     AS order_cnt,
    SUM(amount)  AS total_amount,
    AVG(amount)  AS avg_amount
FROM orders
GROUP BY city
ORDER BY total_amount DESC;""") + """
<p>常用聚合函数：<code>COUNT</code>（计数）、<code>SUM</code>（求和）、<code>AVG</code>（平均）、<code>MAX</code>/<code>MIN</code>（最大/最小）。<code>GROUP BY</code> 决定「按什么分组」。</p>

<h2>关联：JOIN</h2>
<p>当信息分散在多张表，用 <code>JOIN</code> 把它们拼起来：</p>
""" + code("sql", "把订单表和用户表拼起来", """-- orders 里只有 user_id，想知道用户名要去 users 表取
SELECT o.order_id, u.name, o.amount
FROM orders o
JOIN users u ON o.user_id = u.user_id;""") + """
<div class="callout note">
<span class="tag">JOIN 直觉</span>
<p>JOIN 就是「按某个相同的字段（这里是 <code>user_id</code>）把两张表对齐拼接」。在实时数仓里，把多张表 JOIN 成一张「宽表」是非常常见的需求，也是 Paimon 的典型用途之一。</p>
</div>

<h2>必懂概念</h2>
""" + term("主键 PRIMARY KEY", "Primary Key", "能唯一标识一行的字段，比如订单号。主键相同就认为是同一条记录——这点在 Paimon 的「更新（upsert）」里至关重要：主键相同的新数据会覆盖旧数据。") + term(
        "分区 PARTITION", "Partition", "把一张大表按某字段（常见是日期）切成多块存放，比如按 dt=20260101 一天一块。查询时只扫需要的分区，速度更快、成本更低。") + term(
        "ETL", "Extract-Transform-Load", "抽取（从源头取数据）→ 转换（清洗、加工）→ 加载（写入目标表）。数据平台每天都在做这件事，CDC 入湖本质也是一种 ETL。") + term(
        "数据仓库 数仓", "Data Warehouse", "专门用于分析的「大表仓库」。和支撑业务的数据库不同，它面向报表、统计、离线分析。理解数仓是理解「湖仓（Lakehouse）」的前提，下一阶段会讲。") + """

<h2>分区表长什么样</h2>
""" + code("sql", "带分区的表", """-- 按日期 dt 分区，每天的数据单独一块
CREATE TABLE orders_partitioned (
    order_id BIGINT,
    amount   DECIMAL(10,2),
    dt       STRING       -- 分区字段，如 '20260101'
) PARTITIONED BY (dt);

-- 查询只扫某一天，速度快
SELECT SUM(amount) FROM orders_partitioned WHERE dt = '20260101';""") + """

""" + exercise("练习 2-1", "<p>有一张 <code>orders(order_id, city, amount)</code> 表。请写 SQL：统计每个城市金额大于 50 的订单数量，按数量从多到少排序。</p>",
        code("sql", "参考答案", """SELECT city, COUNT(*) AS cnt
FROM orders
WHERE amount > 50
GROUP BY city
ORDER BY cnt DESC;""")) + """

<div class="callout tip">
<span class="tag">本章目标</span>
<p>能看懂表结构、写简单查询（选列/过滤/聚合/排序/关联），并说清主键、分区、ETL、数仓是什么。尤其是<strong>主键</strong>和<strong>分区</strong>，直接关系到 Paimon 为什么擅长更新。下一章进入大数据计算引擎。</p>
</div>
"""

    # ------------------------------------------------------------------ 第 3 章
    B["pages/03-bigdata.html"] = """
<span class="eyebrow">第 3 章 · 打基础</span>
<h1>大数据与计算引擎</h1>
<p class="lead">这一章讲清 Paimon 所在的世界：什么是批处理和流处理，Hadoop/HDFS 是什么，Spark 和 Flink 各管什么、为什么 Flink 是 Paimon 的最佳搭档。</p>

<h2>为什么需要「大数据」技术</h2>
<p>当数据量大到一台机器存不下、算不动时，就要把数据和计算<strong>分散到很多台机器上并行处理</strong>。这就是大数据技术解决的核心问题：<strong>分布式存储 + 分布式计算</strong>。</p>

<h2>Hadoop 与 HDFS</h2>
""" + term("HDFS", "Hadoop Distributed File System", "Hadoop 的分布式文件系统，把一个大文件切块、分散存到多台机器，并保留多份副本防丢。很多数据湖（包括 Paimon）可以把数据存在 HDFS 上，也可以存在对象存储（如 S3、OSS）或本地。") + """
<p>你现阶段只需知道：HDFS / 对象存储是「数据放哪儿」的底层。Paimon 把表数据以文件形式存进去，自己管理这些文件的组织方式。</p>

<h2>批处理 vs 流处理</h2>
<p>这是最重要的一组概念。</p>
<div class="table-wrap">
<table>
<thead><tr><th></th><th>批处理（Batch）</th><th>流处理（Streaming）</th></tr></thead>
<tbody>
<tr><td>处理方式</td><td>攒一批数据，定时跑一次</td><td>数据来一条处理一条，持续运行</td></tr>
<tr><td>时效</td><td>一般 T+1（隔天出结果）</td><td>秒级 / 分钟级</td></tr>
<tr><td>典型场景</td><td>每日报表、离线统计</td><td>实时大屏、实时风控、实时入湖</td></tr>
<tr><td>代表引擎</td><td>Spark（也支持流）</td><td>Flink（流处理见长）</td></tr>
</tbody>
</table>
</div>
<blockquote>批处理像「每天结算一次」，流处理像「随时实时记账」。</blockquote>

<h2>Spark 和 Flink</h2>
<h3>Apache Spark</h3>
<p>大数据领域最流行的计算引擎之一，<strong>批处理和分析见长</strong>，生态成熟，常用于离线数仓、机器学习。也支持流处理（Structured Streaming），但本质偏「微批」。</p>
<h3>Apache Flink</h3>
<p><strong>流处理见长</strong>的引擎，强在低延迟、状态管理、Exactly-Once 语义。它是 Paimon 的「最佳搭档」——Paimon 最早就诞生在 Flink 社区，原名就叫 <strong>Flink Table Store</strong>。</p>

<div class="callout key">
<span class="tag">为什么 Paimon 和 Flink 绑得这么紧</span>
<p>Paimon 是为「实时」而生的，而实时的核心引擎就是 Flink。Flink 负责「算」（接入变更、做计算），Paimon 负责「存」（高效地存下不断变化的数据并支持快速查询）。两者配合，构成实时湖仓的核心。</p>
</div>

<h2>一张图看清角色分工</h2>
<div class="flow">
<div class="node"><div class="nt">数据源</div><div class="nd">MySQL / Kafka / 日志</div></div>
<div class="arrow">↓</div>
<div class="node"><div class="nt">计算引擎</div><div class="nd">Flink（流）/ Spark（批）</div></div>
<div class="arrow">↓ 写入</div>
<div class="node brand"><div class="nt">存储层</div><div class="nd">Paimon 表（在 HDFS / S3 / 本地）</div></div>
<div class="arrow">↓ 查询</div>
<div class="node"><div class="nt">查询引擎</div><div class="nd">Flink / Spark / Trino / StarRocks</div></div>
</div>
<p>记住这个分工：<strong>引擎负责算，Paimon 负责存，查询引擎负责取。</strong>Paimon 处在「存储层」，是连接「实时写入」和「快速查询」的枢纽。</p>

""" + exercise("练习 3-1", "<p>用自己的话说清楚：① 批处理和流处理最大的区别是什么？② 在「MySQL → Flink → Paimon → Spark 查询」这条链路里，Flink、Paimon、Spark 各自扮演什么角色？</p>",
        "<p>① 批处理是攒一批定时跑、时效 T+1；流处理是来一条算一条、持续运行、秒级时效。② Flink 负责实时接入与计算并写入；Paimon 负责存储这些不断变化的数据并支持快速查询；Spark 负责对 Paimon 里的数据做批量分析/查询。</p>") + """

<div class="callout tip">
<span class="tag">本章目标</span>
<p>能说清批/流区别，知道 HDFS、Spark、Flink 各是什么、在链路里的角色。下一章讲两个直接通往 Paimon 的概念：CDC 与湖仓。</p>
</div>
"""

    # ------------------------------------------------------------------ 第 4 章
    B["pages/04-cdc-lakehouse.html"] = """
<span class="eyebrow">第 4 章 · 打基础</span>
<h1>CDC 与湖仓</h1>
<p class="lead">这是地基的最后一章，也是离 Paimon 最近的一章。讲清 CDC 是什么、数据湖/数仓/湖仓怎么演进、以及「表格式（table format）」这个 Paimon 所属的品类为什么会出现。</p>

<h2>CDC：变更数据捕获</h2>
""" + term("CDC", "Change Data Capture", "把业务数据库（如 MySQL）里发生的「增、删、改」实时捕获出来，变成一条条变更记录，喂给下游系统。常见实现：读取数据库的 binlog（变更日志）。") + """
<p>举例：用户在 App 下了一单，MySQL 里 <code>orders</code> 表插入一行；用户取消订单，这行被更新或删除。CDC 能把这些「插入/更新/删除」实时同步出来。</p>
<div class="callout note">
<span class="tag">CDC 的典型链路</span>
<p>很多实时数仓的第一步就是：<strong>MySQL → CDC → Flink → Paimon</strong>。把线上数据库的变化实时灌进数据湖——这正是 Paimon 最擅长的场景之一，第 9 章会带你亲手做一遍。</p>
</div>

<h2>从数据库到数仓，再到数据湖</h2>
<div class="table-wrap">
<table>
<thead><tr><th>品类</th><th>是什么</th><th>擅长</th><th>短板</th></tr></thead>
<tbody>
<tr><td>业务数据库</td><td>支撑线上业务的库（MySQL 等）</td><td>高频增删改、事务</td><td>不适合大规模分析</td></tr>
<tr><td>数据仓库</td><td>面向分析的结构化大表仓库</td><td>复杂查询、报表</td><td>偏离线、扩展贵、不灵活</td></tr>
<tr><td>数据湖</td><td>用开放文件格式存海量原始数据</td><td>便宜、灵活、可存各种数据</td><td>早期缺事务/更新能力</td></tr>
<tr><td>湖仓一体</td><td>在数据湖上补齐数仓能力</td><td>兼顾便宜灵活与可靠分析</td><td>需要「表格式」来支撑</td></tr>
</tbody>
</table>
</div>

<h2>什么是「湖仓一体」</h2>
""" + term("湖仓一体", "Lakehouse", "把「数据湖的低成本、开放、灵活」和「数据仓库的事务、更新、高效查询」结合起来的架构。核心是在廉价的文件存储之上，加一层能管理事务、更新、版本的「表格式」。") + """

<h2>关键角色：表格式（Table Format）</h2>
<p>数据湖把数据存成一堆文件（如 Parquet）。但「一堆文件」不等于「一张能可靠读写的表」——谁记录有哪些文件？怎么支持更新和删除？怎么保证读到一致的数据？这就是<strong>表格式</strong>要解决的。</p>
""" + term("表格式", "Table Format", "在数据湖文件之上的一层「元数据管理协议」。它记录一张表由哪些文件组成、如何演进、如何支持事务/更新/时间旅行。Apache Paimon、Iceberg、Hudi、Delta Lake 都是表格式。") + """
<div class="callout key">
<span class="tag">关键认知</span>
<p><strong>Paimon 就是一种表格式。</strong>它的定位不是数据库，也不是计算引擎，而是「让数据湖里的文件，表现得像一张支持实时更新、可时间旅行的表」。而 Paimon 的差异化是：用 LSM 结构把<strong>实时更新</strong>做到极致。</p>
</div>

<h2>把四章串起来</h2>
<div class="flow">
<div class="node"><div class="nt">业务库变更</div><div class="nd">MySQL（第 2 章：表/主键）</div></div>
<div class="arrow">↓ <small>CDC 捕获（本章）</small></div>
<div class="node"><div class="nt">Flink 实时计算</div><div class="nd">（第 3 章：流处理）</div></div>
<div class="arrow">↓ 写入</div>
<div class="node brand"><div class="nt">Paimon 表格式</div><div class="nd">湖仓存储层（本章）</div></div>
<div class="arrow">↓ <small>SQL 查询（第 2 章）</small></div>
<div class="node"><div class="nt">分析 / 报表</div><div class="nd">Spark / Trino 等</div></div>
</div>

""" + exercise("练习 4-1", "<p>请回答：① CDC 解决了什么问题？② 「表格式」在数据湖里扮演什么角色，Paimon 属于哪一类？</p>",
        "<p>① CDC 把数据库的增删改实时捕获出来，让下游能实时拿到数据变化（而不用定时全量拉取）。② 表格式是数据湖文件之上的元数据管理层，让一堆文件表现得像一张支持事务/更新/版本的表；Paimon 就是一种表格式，特点是用 LSM 把实时更新做得很强。</p>") + """

<div class="callout tip">
<span class="tag">地基完成</span>
<p>恭喜，四层地基已经打完。你现在具备了理解 Paimon 所需的全部背景知识。下一章正式认识 Paimon。</p>
</div>
"""

    # ------------------------------------------------------------------ 第 5 章
    B["pages/05-what-is-paimon.html"] = """
<span class="eyebrow">第 5 章 · 打基础</span>
<h1>Paimon 是什么</h1>
<p class="lead">地基打好了，现在正式认识 Paimon。这一章用大白话讲清它的定位、核心特性和典型场景——读完你能对别人解释清楚「Paimon 是干嘛的」。</p>

<h2>一句话定位</h2>
<div class="callout note">
<span class="tag">官方定位</span>
<p>Apache Paimon 是一个<strong>数据湖表格式（lake format）</strong>，配合 Flink 和 Spark，支持<strong>流处理和批处理</strong>，用来构建<strong>实时湖仓架构（Realtime Lakehouse）</strong>。</p>
</div>
<p>它的前身是 <strong>Flink Table Store</strong>，2022 年从 Flink 中独立出来，现在是 Apache 顶级项目。</p>

<h2>用更通俗的话说</h2>
<blockquote>Paimon 是一个给大数据系统用的「数据底座」，专门处理「数据不断变化、还要实时查和分析」的场景。</blockquote>
<p>结合前几章：它既不是数据库，也不是消息队列，也不是计算引擎，而是<strong>数据湖里的一种表格式</strong>（第 4 章），让流 + 批 + 数据湖存储统一起来，并把<strong>实时更新</strong>做得特别强。</p>

<h2>核心特性</h2>
<div class="cards">
<div class="card"><div class="ttl">流批一体</div><div class="desc">同一份数据，既能流式消费，也能批量分析，不用维护两套存储。</div></div>
<div class="card"><div class="ttl">主键更新强</div><div class="desc">基于 LSM 结构处理更新，特别适合高频 upsert 和 CDC 入湖。</div></div>
<div class="card"><div class="ttl">Changelog</div><div class="desc">能产出数据变化记录，供下游做增量计算。</div></div>
<div class="card"><div class="ttl">Time Travel</div><div class="desc">可查询历史某个时间点 / 版本的数据，便于回溯和排查。</div></div>
<div class="card"><div class="ttl">Schema Evolution</div><div class="desc">表结构变了（加字段等）也不用重写历史数据。</div></div>
<div class="card"><div class="ttl">多引擎查询</div><div class="desc">Flink 集成最强，也支持 Spark、Trino、StarRocks、Doris 等。</div></div>
</div>

<h2>它最擅长的事：实时更新</h2>
<p>传统数据湖格式（早期）更擅长「只追加不修改」的数据。但现实里数据经常变——订单状态会改、用户信息会更新。Paimon 用 <strong>LSM 结构</strong>（第 6 章详解）把「高频更新」做得很高效：新数据先进内存、再有序落盘、后台再合并，不用每次都重写整张表。</p>
<div class="callout key">
<span class="tag">一句话记住</span>
<p>如果你的场景是「数据不断变化（尤其是带主键的更新/CDC），还要又快又便宜地查」，Paimon 往往是很合适的选择。</p>
</div>

<h2>典型使用场景</h2>
<ul>
<li><strong>CDC 实时入湖：</strong>MySQL/PostgreSQL 的变更实时同步进数据湖（第 9 章实战）。</li>
<li><strong>实时宽表 / 实时特征表：</strong>多张表实时 JOIN 成一张大宽表供查询。</li>
<li><strong>近实时明细查询：</strong>既要明细、又要响应快的 ad-hoc 查询。</li>
<li><strong>流批统一：</strong>用一套存储同时支撑实时和离线，降本增效。</li>
</ul>

<h2>什么时候不一定用它</h2>
<p>客观地说，Paimon 不是万能的：</p>
<ul>
<li>如果你的团队栈是 <strong>Databricks/Spark 主导</strong>、几乎不用 Flink，Delta Lake 可能更顺手。</li>
<li>如果你最看重<strong>跨引擎的开放标准和最广生态</strong>，Iceberg 更成熟。</li>
<li>如果数据基本「只追加、极少更新」，各家差异没那么大。</li>
</ul>
<p>第 11 章会做详细对比。</p>

<div class="callout tip">
<span class="tag">本章目标</span>
<p>能用一两句话向别人解释 Paimon 是什么、擅长什么、什么场景用它。下一章深入它的核心概念和原理——看懂了，文档就不再是天书。</p>
</div>
"""

    return B
