# -*- coding: utf-8 -*-
"""第 18–19 章：StarRocks / Iceberg 对比 + WeData"""


def build(code, term, exercise):
    B = {}

    # ------------------------------------------------------------------ 第 18 章
    B["pages/18-starrocks.html"] = """
<span class="eyebrow">第 18 章 · 生态与引擎</span>
<h1>StarRocks + Paimon：极速 OLAP 查询</h1>
<p class="lead">前面用 Flink/Spark 把数据写进了 Paimon。但要对外提供「秒级响应」的报表、即席查询，通常会再加一个 OLAP 引擎。<strong>StarRocks</strong> 就是其中最流行的一个，它能直接查询 Paimon 表，不用把数据再搬一份。</p>

<div class="callout note">
<span class="tag">关于「Setats」</span>
<p>你提到的 <strong>Setats</strong>，按目前生态最贴近的产品理解为 <strong>StarRocks</strong>（高性能 OLAP / MPP 查询引擎，常用于湖上加速）。本章按 StarRocks 讲解；若你指的是其它产品，告诉我即可替换。</p>
</div>

<h2>1. StarRocks 是什么、为什么需要它</h2>
""" + term("OLAP", "联机分析处理", "面向「分析查询」的处理方式：对大量数据做聚合、分组、多维分析，追求查询快。与之相对的 OLTP 面向「事务」（增删改单条记录）。报表、看板、即席分析都属于 OLAP。") + term(
        "MPP", "大规模并行处理", "把一个查询拆成很多份，在多台机器上并行算，再汇总结果。StarRocks 用 MPP 架构实现高并发、低延迟的查询。") + """
<p>定位很清楚：Flink/Spark 负责<strong>把数据写好、加工好</strong>放进 Paimon；StarRocks 负责<strong>对外快速查</strong>。三者各司其职。</p>

<h2>2. 在 StarRocks 里创建 Paimon External Catalog</h2>
<p>StarRocks 通过「外部 catalog」直接挂载 Paimon 仓库，不导入数据、查的是 Paimon 里的原始数据：</p>
""" + code("sql", "StarRocks（MySQL 协议客户端连上后执行）", """-- 创建一个指向 Paimon 的外部 catalog
CREATE EXTERNAL CATALOG paimon_catalog
PROPERTIES (
    'type' = 'paimon',
    'paimon.catalog.type' = 'filesystem',
    'paimon.catalog.warehouse' = 'hdfs:///warehouse/paimon'
);""") + """
<p>如果 Paimon 用的是 Hive Metastore（见第 17 章），把 <code>paimon.catalog.type</code> 改为 <code>hive</code> 并补上 metastore 地址即可。</p>

<h2>3. 像查本地表一样查 Paimon</h2>
""" + code("sql", "切换 catalog 并查询", """-- 查看 catalog 里的库
SHOW DATABASES FROM paimon_catalog;

-- 切换进去
SET CATALOG paimon_catalog;
USE default;

-- 直接查 Paimon 表，享受 StarRocks 的并行加速
SELECT city, COUNT(*) AS cnt, SUM(amount) AS total
FROM orders
GROUP BY city
ORDER BY total DESC;""") + """
<div class="callout key">
<span class="tag">关键价值：数据不搬家</span>
<p>StarRocks 查的就是 Paimon 里那一份数据，<strong>没有额外的导入和拷贝</strong>。Flink 实时写入 Paimon，StarRocks 立刻就能查到最新数据对外提供服务——这就是「湖上即席查询加速」。</p>
</div>

<h2>4. 典型架构串起来</h2>
<div class="flow">
<div class="node"><div class="nt">MySQL / Kafka</div><div class="nd">数据源</div></div>
<div class="arrow">↓ Flink CDC 实时写</div>
<div class="node brand"><div class="nt">Paimon（湖上一份数据）</div><div class="nd">实时、可更新、带历史</div></div>
<div class="arrow">↓ 外部 catalog 直查</div>
<div class="node"><div class="nt">StarRocks</div><div class="nd">对外秒级报表 / BI / 即席查询</div></div>
</div>

<h2>5. 性能小贴士</h2>
<ul>
<li>保证 Paimon 端 <strong>compaction 跟得上</strong>，小文件少，StarRocks 扫描才快（见第 10 章）。</li>
<li>查询多用<strong>分区裁剪</strong>（带上分区过滤条件）和<strong>列裁剪</strong>（只 SELECT 需要的列）。</li>
<li>对超高并发的固定报表，可在 StarRocks 端建<strong>物化视图</strong>进一步加速。</li>
</ul>

""" + exercise("练习 18-1", "<p>有人问：「已经有 Paimon 了，为什么还要 StarRocks？直接用 Spark 查不行吗？」请从『定位』角度回答。</p>",
        "<p>Spark 擅长批处理/加工，查询延迟偏高、并发有限，不适合直接面向大量用户的秒级报表。StarRocks 是 MPP OLAP 引擎，专为高并发、低延迟查询设计。分工：Flink/Spark 写入加工，StarRocks 对外快速查。用 StarRocks 直查 Paimon，数据不用搬，又能拿到查询性能。</p>") + """

<div class="callout tip">
<span class="tag">本章目标</span>
<p>理解 OLAP/MPP 概念与 StarRocks 的定位，会用外部 catalog 让 StarRocks 直查 Paimon，并能画出「源→Flink→Paimon→StarRocks」的实时分析链路。最后一章对比 Iceberg 并认识 WeData 平台。</p>
</div>
"""

    # ------------------------------------------------------------------ 第 19 章
    B["pages/19-iceberg-wedata.html"] = """
<span class="eyebrow">第 19 章 · 生态与引擎</span>
<h1>Iceberg 对比 &amp; WeData 平台</h1>
<p class="lead">这一章做两件事：① 把 Paimon 和它最常被拿来比较的竞品 <strong>Apache Iceberg</strong> 讲清楚，帮你做选型；② 认识 <strong>WeData</strong>——腾讯云上把这一整套湖仓栈托管起来的数据开发平台。</p>

<h2>一、Paimon vs Iceberg：同层竞品</h2>
<p>回顾第 14 章：Iceberg 和 Paimon 一样，都是「湖表格式」，是<strong>二选一</strong>的关系（不是协作）。它们都能让你在数据湖上拥有「像数据库表一样」的能力：ACID、schema 演进、时间旅行。区别在侧重点。</p>
""" + term("Apache Iceberg", "冰山", "由 Netflix 发起、现为 Apache 顶级项目的开放表格式。生态成熟、被各大引擎和云厂商广泛支持，尤其擅长大规模「批分析」和缓慢变化的大表。") + """

<div class="table-wrap">
<table>
<thead><tr><th>维度</th><th>Apache Paimon</th><th>Apache Iceberg</th></tr></thead>
<tbody>
<tr><td>底层结构</td><td>LSM 树</td><td>基于不可变数据文件 + 清单（manifest）</td></tr>
<tr><td>最擅长</td><td><strong>实时更新 / CDC 入湖 / 主键 upsert</strong></td><td><strong>大规模批分析、缓慢变化大表</strong></td></tr>
<tr><td>流式能力</td><td>原生强（前身即 Flink Table Store）</td><td>有，但实时更新不是强项</td></tr>
<tr><td>主键 upsert</td><td>一等公民，开箱即用</td><td>有 MOR，但更偏批式合并</td></tr>
<tr><td>生态成熟度</td><td>较新，增长快</td><td>非常成熟，引擎/云厂商支持广</td></tr>
<tr><td>典型选择</td><td>实时数仓、需要频繁更新</td><td>离线数仓、海量历史、以读为主</td></tr>
</tbody>
</table>
</div>

<div class="callout key">
<span class="tag">一句话选型</span>
<p>数据<strong>频繁变更、要实时、要主键 upsert（如 CDC 入湖）→ 选 Paimon</strong>；以<strong>海量历史、批量分析、更新少 → Iceberg 很成熟稳妥</strong>。很多团队也会两者并存，按场景分别使用。</p>
</div>

<h2>二、WeData：腾讯云的数据开发平台</h2>
<p>前面所有动手都是你自己装 Flink、配 jar、起集群——这在学习阶段很有价值（你理解了每一层）。但到了生产，自己运维这一整套很重。<strong>WeData</strong> 就是把它们托管起来的云平台。</p>
""" + term("WeData", "腾讯云数据开发治理平台", "腾讯云提供的一站式大数据开发平台，整合数据集成、开发（SQL/任务编排）、调度、治理、运维等能力，底层可对接 Flink、Spark、湖格式（含 Paimon/Iceberg）等，让团队不必自己搭运维这套栈。") + """

<h3>它帮你省掉什么</h3>
<div class="table-wrap">
<table>
<thead><tr><th>你在前面章节手动做的</th><th>WeData 上的形态</th></tr></thead>
<tbody>
<tr><td>装 Flink、放 jar、起集群</td><td>平台托管的计算资源，开箱即用</td></tr>
<tr><td>手写 CDC 同步命令</td><td>可视化配置数据集成任务</td></tr>
<tr><td>命令行提交、自己盯作业</td><td>任务编排 + 调度 + 监控告警</td></tr>
<tr><td>自己管元数据、权限</td><td>统一的元数据管理与数据治理</td></tr>
</tbody>
</table>
</div>

<div class="callout note">
<span class="tag">学习顺序建议</span>
<p>先用前面的章节<strong>把原理和手动流程跑通</strong>（理解发生了什么），再上 WeData 这类平台<strong>提效</strong>。反过来「只会点平台、不懂底层」，遇到问题会很难排查。你现在已经具备了看懂平台背后在做什么的能力。</p>
</div>

<h3>在 WeData 上用 Paimon 的大致流程</h3>
<div class="flow">
<div class="node"><div class="nt">① 接入数据源</div><div class="nd">在数据集成里配置 MySQL/Kafka 等</div></div>
<div class="arrow">↓</div>
<div class="node brand"><div class="nt">② 实时写入 Paimon</div><div class="nd">用托管 Flink，配置 CDC 同步到 Paimon 表</div></div>
<div class="arrow">↓</div>
<div class="node"><div class="nt">③ 开发与调度</div><div class="nd">写 SQL 任务做加工，配置周期调度</div></div>
<div class="arrow">↓</div>
<div class="node"><div class="nt">④ 查询与服务</div><div class="nd">对接 StarRocks 等对外提供查询</div></div>
</div>
<p class="muted">具体菜单和名称以腾讯云 WeData 控制台最新版本为准；这里给的是「概念流程」，对应的正是你前面亲手做过的每一步。</p>

""" + exercise("练习 19-1", "<p>两道选型题：① 业务要把 MySQL 订单实时入湖、且要随时反映增删改，选 Paimon 还是 Iceberg？② 团队不想自己运维 Flink 集群、希望可视化配置实时同步任务，应该考虑什么？</p>",
        "<p>① 选 Paimon——实时 + 主键 upsert 是它的强项。② 考虑用 WeData 这类托管数据开发平台，用托管计算资源 + 可视化数据集成替代自建运维。</p>") + """

<div class="callout tip">
<span class="tag">恭喜你学完生态篇</span>
<p>到这里，你不仅会用 Paimon，还理解了它与 Flink、Spark、Hive、StarRocks、Iceberg、WeData 的关系与协作方式，具备了在真实项目里做技术选型和搭建链路的基础。回首页可重温整张学习地图，或去「学习资源与下一步」继续深入。</p>
</div>
"""

    return B
