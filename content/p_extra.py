# -*- coding: utf-8 -*-
"""第 11–13 章：对标对比 / FAQ 排错 / 资源与下一步"""


def build(code, term, exercise):
    B = {}

    # ------------------------------------------------------------------ 第 11 章
    B["pages/11-comparison.html"] = """
<span class="eyebrow">第 11 章 · 进阶 · 拓展</span>
<h1>对标对比与选型</h1>
<p class="lead">Paimon 最常和 Iceberg、Hudi、Delta Lake 放在一起比较。这一章帮你看清四者的差别，并给出按场景的选型建议。</p>

<div class="callout warn">
<span class="tag">视角说明</span>
<p>下面的对比综合了官方定位与<strong>社区 / 市场视角</strong>，并非任何一家的官方结论。各项目都在快速演进，技术选型请结合自己团队的实际栈与最新版本再判断。</p>
</div>

<h2>四种开源表格式速览</h2>
<div class="table-wrap">
<table>
<thead><tr><th>格式</th><th>出身</th><th>主要设计目标</th></tr></thead>
<tbody>
<tr><td><strong>Apache Iceberg</strong></td><td>Netflix（2017）</td><td>多引擎互操作、开放标准</td></tr>
<tr><td><strong>Delta Lake</strong></td><td>Databricks（2019）</td><td>Spark 上可靠的数据湖</td></tr>
<tr><td><strong>Apache Hudi</strong></td><td>Uber（2016）</td><td>流式 upsert 与增量处理</td></tr>
<tr><td><strong>Apache Paimon</strong></td><td>源自 Flink 社区（2022）</td><td>实时湖仓（LSM 结构）</td></tr>
</tbody>
</table>
</div>

<h2>关键维度对比</h2>
<div class="table-wrap">
<table>
<thead><tr><th>维度</th><th>Iceberg</th><th>Delta Lake</th><th>Hudi</th><th>Paimon</th></tr></thead>
<tbody>
<tr><td>多引擎支持</td><td>最广</td><td>Spark 最佳</td><td>Spark+Flink 强</td><td>Flink 原生最强</td></tr>
<tr><td>流式 / 实时</td><td>较好（靠 Flink）</td><td>CDC（CDF）</td><td>原生强</td><td>原生强</td></tr>
<tr><td>主键 upsert</td><td>支持</td><td>支持（merge）</td><td>原生（索引）</td><td>LSM 原生</td></tr>
<tr><td>高频更新性能</td><td>一般</td><td>一般</td><td>强</td><td>强（LSM）</td></tr>
<tr><td>开放生态 / 标准</td><td>最成熟</td><td>偏 Databricks</td><td>中等</td><td>成长中</td></tr>
</tbody>
</table>
</div>

<h2>逐个对比</h2>
<h3>Paimon vs Iceberg</h3>
<p><strong>Iceberg</strong> 是「跨引擎开放标准」的代表：多引擎兼容最成熟、云厂商支持最广、通用性强。<strong>Paimon</strong> 的优势在 Flink 原生实时链路、高频主键更新、changelog/CDC 这类实时语义。</p>
<blockquote>重跨引擎开放生态 → Iceberg；重 Flink 实时更新链路 → Paimon。</blockquote>

<h3>Paimon vs Hudi</h3>
<p><strong>Hudi</strong> 是流式 upsert 的老牌强项，进入市场早、能力成熟。<strong>Paimon</strong> 在 Flink 体系下更「原生」，设计上更偏实时湖仓一体化，LSM 结构在高频更新上表现突出。两者经常被放在一起比较。</p>

<h3>Paimon vs Delta Lake</h3>
<p><strong>Delta Lake</strong> 与 Spark/Databricks 生态绑定最紧。如果团队栈是 Databricks/Spark 主导，Delta 往往更顺手；如果是 Flink / 实时 CDC / 流式查询为主，Paimon 更合适。</p>

<h2>按场景选型</h2>
<div class="cards">
<div class="card"><div class="ttl">重 Flink 实时链路</div><div class="desc">CDC 入湖、实时更新、流式查询 → 优先看 <strong>Paimon</strong>。</div></div>
<div class="card"><div class="ttl">重跨引擎开放生态</div><div class="desc">想要最大互操作性、云厂商支持广 → 优先看 <strong>Iceberg</strong>。</div></div>
<div class="card"><div class="ttl">重 Spark / Databricks</div><div class="desc">团队栈以 Databricks 为主 → 优先看 <strong>Delta Lake</strong>。</div></div>
<div class="card"><div class="ttl">传统流式 upsert</div><div class="desc">老牌强项、已有经验 → 也常比较 <strong>Hudi</strong>。</div></div>
</div>

<h2>一句话记忆</h2>
<ul>
<li><strong>Paimon：</strong>Flink-native、实时更新、CDC、主键表（LSM）。</li>
<li><strong>Iceberg：</strong>开放标准、多引擎、生态最广。</li>
<li><strong>Hudi：</strong>流式 upsert 的老牌强项。</li>
<li><strong>Delta Lake：</strong>Databricks / Spark 体系强。</li>
</ul>

<div class="callout note">
<span class="tag">给零基础的建议</span>
<p>如果你做实时数仓 / Flink，Paimon 很值得学；做传统离线数仓，可以先学 Iceberg 再补 Paimon；团队是 Databricks/Spark 主导，则同时关注 Delta Lake。但无论选哪个，本教程学到的底层概念（表格式、snapshot、upsert、compaction）都是相通的。</p>
</div>
"""

    # ------------------------------------------------------------------ 第 12 章
    B["pages/12-faq.html"] = """
<span class="eyebrow">第 12 章 · 进阶 · 拓展</span>
<h1>常见问题与排错</h1>
<p class="lead">把前面各章踩坑点集中到一起，按「环境 / 写入 / 查询 / 存储」分类，方便你遇到问题时快速定位。</p>

<h2>环境与启动</h2>
<div class="table-wrap">
<table>
<thead><tr><th>问题</th><th>原因</th><th>解决</th></tr></thead>
<tbody>
<tr><td>启动报 <code>JAVA_HOME not set</code></td><td>没设 Java 环境变量</td><td>设置 <code>JAVA_HOME</code> 并加进 <code>PATH</code>（第 1/7 章）</td></tr>
<tr><td>建 catalog 报 <code>ClassNotFound</code> / 找不到 paimon</td><td>jar 没放进 lib 或版本不匹配</td><td>把对应 Flink 版本的 paimon jar 放进 <code>$FLINK_HOME/lib</code>，<strong>重启集群</strong></td></tr>
<tr><td>8081 Dashboard 打不开</td><td>集群没起 / 端口被占</td><td>查 <code>$FLINK_HOME/log</code>；释放端口或换端口</td></tr>
</tbody>
</table>
</div>

<h2>写入相关</h2>
<div class="table-wrap">
<table>
<thead><tr><th>问题</th><th>原因</th><th>解决</th></tr></thead>
<tbody>
<tr><td>写了数据，查不到</td><td>流模式没开 checkpoint，数据未提交</td><td>设 <code>execution.checkpointing.interval</code></td></tr>
<tr><td>更新没生效 / 出现重复行</td><td>表没建主键</td><td>建表声明 <code>PRIMARY KEY ... NOT ENFORCED</code></td></tr>
<tr><td>写入越来越慢</td><td>小文件堆积、compaction 跟不上</td><td>调大 checkpoint 间隔、加强/独立 compaction、合理 bucket（第 10 章）</td></tr>
<tr><td>CDC 同步起不来</td><td>MySQL 没开 binlog / 格式非 ROW / 权限不足</td><td>开 binlog、设 <code>binlog_format=ROW</code>、授权（第 9 章）</td></tr>
</tbody>
</table>
</div>

<h2>查询相关</h2>
<div class="table-wrap">
<table>
<thead><tr><th>问题</th><th>原因</th><th>解决</th></tr></thead>
<tbody>
<tr><td>批查只看到部分数据</td><td>查的是某个旧 snapshot / 流作业还没提交</td><td>等 checkpoint 提交后再查；确认没误用时间旅行参数</td></tr>
<tr><td>查询慢</td><td>小文件多、没做分区/列裁剪</td><td>确保 compaction 跟得上；查询带上分区条件</td></tr>
<tr><td>流查没有持续输出</td><td>没切到 streaming 模式</td><td><code>SET 'execution.runtime-mode' = 'streaming';</code></td></tr>
</tbody>
</table>
</div>

<h2>存储与运维</h2>
<div class="table-wrap">
<table>
<thead><tr><th>问题</th><th>原因</th><th>解决</th></tr></thead>
<tbody>
<tr><td>删了数据，磁盘没降</td><td>逻辑删除，文件等 snapshot 过期才清</td><td>正常现象；按需缩短 snapshot 保留（第 10 章）</td></tr>
<tr><td>存储增长过快</td><td>快照保留太久 / 小文件多</td><td>配置 <code>snapshot.num-retained</code> / <code>time-retained</code></td></tr>
</tbody>
</table>
</div>

<div class="callout tip">
<span class="tag">排错通用思路</span>
<p>① 先看 Flink Dashboard（8081）作业是否在跑、有没有报错；② 再看 <code>$FLINK_HOME/log</code> 里的日志；③ 90% 的「查不到数据」都是 checkpoint 没设；④ 90% 的「更新无效」都是没建主键。记住这两条能省很多时间。</p>
</div>
"""

    # ------------------------------------------------------------------ 第 13 章
    B["pages/13-resources.html"] = """
<span class="eyebrow">第 13 章 · 进阶 · 拓展</span>
<h1>学习资源与下一步</h1>
<p class="lead">本教程已经覆盖了从 0 到能用的全部内容。这一章给你官方资料导读、术语速查表，以及继续提升的方向——当你想深入时，知道去哪找。</p>

<h2>术语速查表</h2>
<div class="table-wrap">
<table>
<thead><tr><th>术语</th><th>一句话</th><th>详见</th></tr></thead>
<tbody>
<tr><td>表格式</td><td>数据湖文件之上的元数据管理层，Paimon 属于此类</td><td>第 4 章</td></tr>
<tr><td>CDC</td><td>把数据库的增删改实时捕获出来</td><td>第 4/9 章</td></tr>
<tr><td>流批一体</td><td>同一份数据既能流式消费也能批量分析</td><td>第 5/8 章</td></tr>
<tr><td>snapshot</td><td>表的一个版本，读表入口</td><td>第 6 章</td></tr>
<tr><td>LSM</td><td>先内存、再有序落盘、后台合并，让更新高效</td><td>第 6 章</td></tr>
<tr><td>upsert</td><td>主键在就更新、不在就插入</td><td>第 6 章</td></tr>
<tr><td>compaction</td><td>合并小文件、收拢同主键数据</td><td>第 6/10 章</td></tr>
<tr><td>bucket</td><td>按主键分桶，写入/合并的并行单元</td><td>第 10 章</td></tr>
<tr><td>merge engine</td><td>主键相同的记录怎么合并</td><td>第 10 章</td></tr>
</tbody>
</table>
</div>

<h2>官方资料导读（想深入时再看）</h2>
<p>本教程已自成闭环，下面这些是「想钻得更深」时的权威来源——把官方当「定义来源」，把博客当「案例补充」。</p>
<ul>
<li><a href="https://paimon.apache.org/" target="_blank" rel="noopener">Paimon 官网首页</a> —— 定位、核心能力、最新动态。</li>
<li><a href="https://paimon.apache.org/docs/master/" target="_blank" rel="noopener">官方文档总览</a> —— 系统化入口。</li>
<li><a href="https://paimon.apache.org/docs/master/concepts/" target="_blank" rel="noopener">Concepts 概念文档</a> —— 对照本教程第 6 章深入。</li>
<li><a href="https://paimon.apache.org/docs/master/flink/quick-start/" target="_blank" rel="noopener">Flink Quick Start</a> —— 对照本教程第 8 章核对版本。</li>
<li><a href="https://github.com/apache/paimon" target="_blank" rel="noopener">GitHub: apache/paimon</a> —— 源码、版本演进、引擎集成。</li>
</ul>

<h2>预备知识的延伸（如仍想补强）</h2>
<div class="table-wrap">
<table>
<thead><tr><th>方向</th><th>建议</th></tr></thead>
<tbody>
<tr><td>SQL</td><td>找一个交互式 SQL 练习平台，多写多练 join 和聚合</td></tr>
<tr><td>Linux</td><td>熟悉管道、重定向、简单 shell 脚本</td></tr>
<tr><td>Flink</td><td><a href="https://flink.apache.org/" target="_blank" rel="noopener">Flink 官网</a> + 中文社区，理解状态、checkpoint、窗口</td></tr>
<tr><td>湖仓</td><td>读各表格式官方文档，体会不同设计取舍</td></tr>
</tbody>
</table>
</div>

<h2>继续提升的方向</h2>
<div class="cards">
<div class="card"><div class="ttl">深入原理</div><div class="desc">读 Paimon 的 file layout、index、changelog producer 等文档，理解内部实现。</div></div>
<div class="card"><div class="ttl">多引擎查询</div><div class="desc">试着用 Spark / Trino / StarRocks 查 Paimon 表，体会「一份存储多处查」。</div></div>
<div class="card"><div class="ttl">生产化</div><div class="desc">监控、作业稳定性、资源调优、与调度平台集成。</div></div>
<div class="card"><div class="ttl">参与社区</div><div class="desc">看 issue、提问、读 PR，跟上版本演进。</div></div>
</div>

<div class="callout key">
<span class="tag">恭喜你走到这里</span>
<p>从终端命令、SQL，到 Flink、CDC、湖仓，再到 Paimon 的概念、上手、实战与调优——你已经走完了一条完整的零基础学习路径。接下来最好的提升方式只有一个：<strong>找一个真实场景，自己动手搭一遍。</strong></p>
</div>

<div class="callout tip">
<span class="tag">最后的建议</span>
<p>知识会忘，但动手做过的会留下。建议你现在就回到第 7、8 章，把环境搭起来、Quick Start 跑通；再用第 9 章的实战做一条 CDC 入湖链路。做完这两件事，你就真正「从 0 学会了 Paimon」。</p>
</div>
"""

    return B
