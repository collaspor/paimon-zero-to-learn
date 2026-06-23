# -*- coding: utf-8 -*-
"""第 6–7 章：核心概念与原理 / 环境搭建"""


def build(code, term, exercise):
    B = {}

    # ------------------------------------------------------------------ 第 6 章
    B["pages/06-concepts.html"] = """
<span class="eyebrow">第 6 章 · 学 Paimon</span>
<h1>核心概念与原理</h1>
<p class="lead">这一章把 Paimon 文档里最常出现的术语，用通俗的话 + 图示讲一遍，并讲清它处理更新的底层原理。看懂这章，后面的上手和文档都会顺很多。</p>

<h2>先建立一个核心直觉</h2>
<p>Paimon 处理「更新」的方式和你想的不一样。它<strong>不会去原地修改旧文件</strong>，而是：</p>
<ol>
<li>把新数据<strong>写成新文件</strong>；</li>
<li>记录一次<strong>元数据变化</strong>（这次新增了哪些文件、删了哪些）；</li>
<li>用「版本（snapshot）」来决定哪些数据对外可见；</li>
<li>后台<strong>异步合并</strong>，把同一主键的新旧数据收拢、清理过期文件。</li>
</ol>
<p>下面所有概念，都是围绕这个思路展开的。</p>

<h2>表的物理结构</h2>
<p>一张 Paimon 表在存储里大致是这样组织的（从上到下是「找数据」的路径）：</p>
<div class="flow">
<div class="node brand"><div class="nt">Snapshot（快照）</div><div class="nd">某个版本，读表的入口</div></div>
<div class="arrow">↓ 指向</div>
<div class="node"><div class="nt">Manifest（清单）</div><div class="nd">记录这个版本有哪些数据文件被加/删</div></div>
<div class="arrow">↓ 指向</div>
<div class="node"><div class="nt">Data File（数据文件）</div><div class="nd">真正存数据，列式（Parquet/ORC）</div></div>
</div>
<div class="callout note">
<span class="tag">读表靠元数据，不是扫目录</span>
<p>Paimon 读表是从 <code>snapshot → manifest → data file</code> 这棵元数据树出发的，而不是简单看目录里有哪些文件。这让它能做到事务一致和时间旅行。</p>
</div>

<h2>关键术语速查</h2>
<div class="table-wrap">
<table>
<thead><tr><th>术语</th><th>通俗解释</th></tr></thead>
<tbody>
<tr><td><code>snapshot</code></td><td>快照。某个时间点的「数据版本」，读表时从一个 snapshot 出发还原出完整视图。每次写入（提交）产生一个新 snapshot。</td></tr>
<tr><td><code>manifest</code></td><td>清单文件。记录某个版本里有哪些数据文件被「加」或「删」。</td></tr>
<tr><td><code>data file</code></td><td>真正存数据的文件，列式存储（如 Parquet/ORC），压缩比高、扫描快。</td></tr>
<tr><td><code>LSM tree</code></td><td>「先写内存、再落盘成有序块、后台再合并」的结构，让高频更新很高效。下面详解。</td></tr>
<tr><td><code>compaction</code></td><td>压缩合并。把零散的小文件 / 多层数据整理合并，提升查询性能、收拢同主键数据。</td></tr>
<tr><td><code>changelog</code></td><td>变更日志。把数据的增删改作为「变化流」输出，供下游做增量计算。</td></tr>
<tr><td><code>time travel</code></td><td>时间旅行。查询历史某个 snapshot 的数据，用于回溯、对账、排查。</td></tr>
<tr><td><code>schema evolution</code></td><td>表结构演进。加字段、改类型时不用重写历史数据。</td></tr>
<tr><td><code>bucket</code></td><td>桶。把数据按主键 hash 分到固定数量的桶里，每个桶是一个并行写入/合并单元。</td></tr>
<tr><td><code>merge engine</code></td><td>合并引擎。决定主键相同的多条记录怎么合并（去重保留最新、部分更新、聚合等）。</td></tr>
</tbody>
</table>
</div>

<h2>核心原理：LSM 与主键更新</h2>
<p>主键表为什么能扛住高频更新？因为它用了 <strong>LSM（Log-Structured Merge-Tree）</strong> 的思路：</p>
<div class="flow">
<div class="node"><div class="nt">① 写入内存缓冲</div><div class="nd">新数据先攒在内存（MemTable）</div></div>
<div class="arrow">↓ 满了 / checkpoint</div>
<div class="node"><div class="nt">② 落盘成有序块</div><div class="nd">刷成一个有序的数据文件（sorted run）</div></div>
<div class="arrow">↓ 后台异步</div>
<div class="node brand"><div class="nt">③ Compaction 合并</div><div class="nd">把多个块合并，按主键收拢、去重</div></div>
</div>
<p>这样做的好处：写入时<strong>不用每次都去翻整张表找旧记录改</strong>，而是先快速追加，后台再慢慢整理。代价是查询时可能要合并多个块的数据，所以需要 compaction 来控制块的数量。</p>

<div class="callout key">
<span class="tag">upsert 的本质</span>
<p><strong>upsert = update + insert</strong>：主键已存在就更新、不存在就插入。在 Paimon 里，写一条主键相同的新记录，并不会立刻删掉旧记录，而是「新数据盖在上面」，读取/合并时按规则（merge engine）保留正确的那条。这就是它处理 CDC 的核心机制。</p>
</div>

<h2>三件最容易踩坑的事</h2>
<div class="callout warn">
<span class="tag">① 删除不等于立刻删文件</span>
<p>删除往往先是「逻辑删除」——对用户不可见，但物理文件还在。真正的物理清理要等 <strong>snapshot 过期（expiration）</strong> 后才发生。所以刚删完，磁盘空间不会马上降。</p>
</div>
<div class="callout warn">
<span class="tag">② 小文件与 checkpoint 强相关</span>
<p>流式写入时，每个 Flink checkpoint 会提交一次、生成快照和文件。checkpoint 间隔越小，小文件越多。需要靠 compaction、合理的 bucket 数来治理（第 10 章详解）。</p>
</div>
<div class="callout warn">
<span class="tag">③ 主键表必须先想清楚 bucket</span>
<p>bucket 数决定了写入并行度和后续扩展性，建表时要根据数据量评估。改 bucket 数需要重组数据，成本不低。</p>
</div>

""" + exercise("练习 6-1", "<p>用自己的话回答：① 为什么说 Paimon 读表是「沿元数据树」而不是「扫目录」？② LSM 结构让主键更新高效的关键在哪？</p>",
        "<p>① 因为 Paimon 通过 snapshot→manifest→data file 这棵元数据树来确定一个版本由哪些文件组成，这样能保证读到一致的版本、支持时间旅行，而不是依赖目录里恰好有哪些文件。② 关键在于写入时只追加（先内存、再有序落盘），不原地改旧文件；同主键的新旧数据由后台 compaction 异步合并，避免每次写都重写整表。</p>") + """

<div class="callout tip">
<span class="tag">本章目标</span>
<p>不要求全吃透，能在看到这些词时「说得出大概意思、知道它们怎么协作」就达标。接下来两章我们动手：先搭环境，再跑 Quick Start。</p>
</div>
"""

    # ------------------------------------------------------------------ 第 7 章
    B["pages/07-env-setup.html"] = """
<span class="eyebrow">第 7 章 · 学 Paimon</span>
<h1>环境搭建</h1>
<p class="lead">动手前先把环境装好。这一章带你从零装好 Java、Flink，并放好 Paimon 的 jar，确保下一章能直接跑通。每步都给了验证命令和常见报错。</p>

<div class="callout warn">
<span class="tag">版本说明</span>
<p>下面用占位版本号示意（如 <code>flink-1.20.x</code>、<code>paimon-flink-1.20-x.x.x.jar</code>）。实际下载时，请到 <a href="https://flink.apache.org/downloads/" target="_blank" rel="noopener">Flink 下载页</a> 和 <a href="https://paimon.apache.org/docs/master/flink/quick-start/" target="_blank" rel="noopener">Paimon Quick Start</a> 确认<strong>互相匹配</strong>的版本——Paimon 的 jar 必须对应你装的 Flink 大版本。</p>
</div>

<h2>步骤总览</h2>
<ol class="steps">
<li>安装 Java（Flink 需要 JDK 11 或以上）。</li>
<li>下载并解压 Flink。</li>
<li>把 Paimon 的 bundled jar 放进 Flink 的 <code>lib/</code>。</li>
<li>启动 Flink 本地集群，打开 SQL Client 验证。</li>
</ol>

<h2>1. 安装并验证 Java</h2>
""" + code("bash", "检查是否已装 Java", """java -version
# 期望看到 11 或更高，例如：
# openjdk version "11.0.x"
""") + """
<p>如果没装：macOS 可用 <code>brew install openjdk@11</code>；Ubuntu 可用 <code>sudo apt install openjdk-11-jdk</code>。装好后设置环境变量（第 1 章讲过）：</p>
""" + code("bash", "设置 JAVA_HOME", """export JAVA_HOME=$(/usr/libexec/java_home -v 11 2>/dev/null || echo /usr/lib/jvm/java-11)
export PATH=$JAVA_HOME/bin:$PATH
java -version   # 再次确认""") + """

<h2>2. 下载并解压 Flink</h2>
""" + code("bash", "解压 Flink 到工作目录", """# 假设已下载 flink 安装包到当前目录
tar -xzf flink-1.20.0-bin-scala_2.12.tgz

# 设一个方便引用的变量，指向解压目录
export FLINK_HOME=$(pwd)/flink-1.20.0
echo $FLINK_HOME
ls $FLINK_HOME   # 应能看到 bin/ conf/ lib/ 等目录""") + """

<h2>3. 放入 Paimon jar</h2>
<p>Paimon 提供「bundled jar」，直接丢进 Flink 的 <code>lib/</code> 即可被加载：</p>
""" + code("bash", "拷贝 Paimon bundled jar", """# 把下载好的 paimon-flink jar 拷进 Flink lib
cp paimon-flink-1.20-*.jar $FLINK_HOME/lib/

# 确认进去了
ls $FLINK_HOME/lib/ | grep paimon""") + """
<div class="callout note">
<span class="tag">关于 Hadoop 依赖</span>
<p>若你把数据存本地（<code>file:/...</code>）做实验，通常无需额外 Hadoop 依赖。若要写 HDFS/对象存储，按官方说明补对应的 Hadoop / 文件系统依赖 jar。新手先用本地路径即可。</p>
</div>

<h2>4. 启动集群并打开 SQL Client</h2>
""" + code("bash", "启动 Flink 本地集群", """# 启动本地集群
$FLINK_HOME/bin/start-cluster.sh

# 打开浏览器访问 Dashboard 确认集群起来了
# http://localhost:8081

# 打开 Flink SQL 交互客户端
$FLINK_HOME/bin/sql-client.sh""") + """
<p>看到 SQL Client 的提示符（一只松鼠 ASCII 图 + <code>Flink SQL></code>），说明环境就绪。下一章就在这里敲 SQL。</p>

<h2>常见报错速查</h2>
<div class="table-wrap">
<table>
<thead><tr><th>现象</th><th>可能原因</th><th>解决</th></tr></thead>
<tbody>
<tr><td>启动报 <code>JAVA_HOME not set</code></td><td>没设 Java 环境变量</td><td>按上面设置 <code>JAVA_HOME</code> 并加进 <code>PATH</code></td></tr>
<tr><td>SQL Client 里建 catalog 报 <code>ClassNotFound: paimon</code></td><td>Paimon jar 没放进 lib 或版本不匹配</td><td>确认 jar 在 <code>$FLINK_HOME/lib</code>，且对应 Flink 版本，<strong>重启集群</strong></td></tr>
<tr><td>Dashboard 打不开 / 8081 无响应</td><td>集群没起来或端口被占</td><td>看 <code>$FLINK_HOME/log</code> 里日志；换端口或杀掉占用进程</td></tr>
<tr><td>写入卡住、无数据落盘</td><td>流模式没开 checkpoint</td><td>设 <code>execution.checkpointing.interval</code>（下一章会设）</td></tr>
</tbody>
</table>
</div>

<div class="callout tip">
<span class="tag">本章目标</span>
<p>Java 能 <code>java -version</code>、Flink 集群能在 8081 看到、SQL Client 能打开。三者就绪，就可以进入下一章动手跑第一个 Paimon 示例了。</p>
</div>
"""

    return B
