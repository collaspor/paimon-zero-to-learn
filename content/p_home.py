# -*- coding: utf-8 -*-
"""首页 + 第 0 章 学习路线"""


def build(code, term, exercise):
    B = {}

    B["index.html"] = """
<span class="eyebrow">零基础 · 中文完整自学教程</span>
<h1>从 0 学习 Apache Paimon</h1>
<p class="lead">这是一个为<strong>完全没有大数据基础</strong>的人准备的教程。你不需要再去翻官方文档或其他资料——从终端命令、SQL，到 Flink、CDC、湖仓，再到 Paimon 的原理、上手与实战，全部在这个站里讲透。</p>

<div class="callout note">
<span class="tag">一句话先说清楚</span>
<p>Apache Paimon 是一个面向<strong>实时湖仓（Realtime Lakehouse）</strong>的开源<strong>数据湖表格式</strong>。它让<strong>流处理 + 批处理 + 数据湖存储</strong>统一起来，尤其擅长<strong>主键更新、CDC 入湖、近实时查询</strong>。看不懂这句话没关系，这正是本教程要带你弄明白的。</p>
</div>

<h2>这个教程的特点</h2>
<div class="cards">
<div class="card"><div class="ttl">真·零基础</div><div class="desc">从 <code>ls</code> / <code>cd</code> 和 <code>SELECT</code> 讲起，不预设任何前置知识。</div></div>
<div class="card"><div class="ttl">看完不用再查</div><div class="desc">预备知识、原理、上手、实战、排错全覆盖，自成闭环。</div></div>
<div class="card"><div class="ttl">能动手</div><div class="desc">每个关键点配可复制的命令/SQL，重要章节带练习题和参考答案。</div></div>
<div class="card"><div class="ttl">讲为什么</div><div class="desc">不只告诉你怎么做，更解释 Paimon 的设计动机和取舍。</div></div>
</div>

<h2>适合谁</h2>
<div class="taglist">
<span>大数据零基础</span><span>想转数据 / 数仓方向</span><span>做实时数仓 / Flink</span><span>想搞懂 Paimon vs Iceberg/Hudi/Delta</span><span>面试要用</span>
</div>

<h2>完整学习地图</h2>
<p>本教程分五个阶段、14 章。建议从第 0 章开始按顺序读；已有基础的同学可直接跳到第 5 章。</p>

<h3>① 开始</h3>
<div class="cards">
<a class="card" href="pages/00-roadmap.html"><span class="num">第 0 章</span><div class="ttl">零基础学习路线</div><div class="desc">先学什么、后学什么、各花多久，给你一张全局地图。</div></a>
<a class="card" href="pages/01-linux.html"><span class="num">第 1 章</span><div class="ttl">Linux 与终端</div><div class="desc">命令行、文件路径、环境变量、解压与运行脚本。</div></a>
</div>

<h3>② 打基础</h3>
<div class="cards">
<a class="card" href="pages/02-sql.html"><span class="num">第 2 章</span><div class="ttl">SQL 与数据建模</div><div class="desc">查询、聚合、关联，以及表/主键/分区/ETL/数仓概念。</div></a>
<a class="card" href="pages/03-bigdata.html"><span class="num">第 3 章</span><div class="ttl">大数据与计算引擎</div><div class="desc">批 vs 流、Hadoop/HDFS、Spark 与 Flink 各管什么。</div></a>
<a class="card" href="pages/04-cdc-lakehouse.html"><span class="num">第 4 章</span><div class="ttl">CDC 与湖仓</div><div class="desc">CDC 是什么、数据湖/数仓/湖仓的演进、表格式的由来。</div></a>
<a class="card" href="pages/05-what-is-paimon.html"><span class="num">第 5 章</span><div class="ttl">Paimon 是什么</div><div class="desc">用大白话讲定位、核心特性和典型使用场景。</div></a>
</div>

<h3>③ 学 Paimon</h3>
<div class="cards">
<a class="card" href="pages/06-concepts.html"><span class="num">第 6 章</span><div class="ttl">核心概念与原理</div><div class="desc">snapshot/manifest/LSM/compaction/changelog 配图详解。</div></a>
<a class="card" href="pages/07-env-setup.html"><span class="num">第 7 章</span><div class="ttl">环境搭建</div><div class="desc">Java、Flink、Paimon jar 一步步装好，含版本与排错。</div></a>
</div>

<h3>④ 动手实践</h3>
<div class="cards">
<a class="card" href="pages/08-quickstart.html"><span class="num">第 8 章</span><div class="ttl">Quick Start 上手</div><div class="desc">建 catalog、建表、流式写入、批查、流查，逐行讲解。</div></a>
<a class="card" href="pages/09-cdc-practice.html"><span class="num">第 9 章</span><div class="ttl">实战：CDC 入湖</div><div class="desc">把 MySQL 的变更实时同步进 Paimon 的完整链路。</div></a>
<a class="card" href="pages/10-advanced.html"><span class="num">第 10 章</span><div class="ttl">进阶：表类型与调优</div><div class="desc">主键表/Append 表、merge engine、bucket、compaction 调优。</div></a>
</div>

<h3>⑤ 进阶 · 拓展</h3>
<div class="cards">
<a class="card" href="pages/11-comparison.html"><span class="num">第 11 章</span><div class="ttl">对标对比与选型</div><div class="desc">Paimon vs Iceberg / Hudi / Delta Lake，按场景选型。</div></a>
<a class="card" href="pages/12-faq.html"><span class="num">第 12 章</span><div class="ttl">常见问题与排错</div><div class="desc">环境、写入、查询、小文件等高频问题与解决办法。</div></a>
<a class="card" href="pages/13-resources.html"><span class="num">第 13 章</span><div class="ttl">学习资源与下一步</div><div class="desc">官方文档导读、术语速查、继续提升的方向。</div></a>
</div>

<div class="callout tip">
<span class="tag">怎么用这个网站</span>
<p>从左侧导航第 0 章开始，按顺序往下读。每页右侧有「本页目录」可快速跳转，顶部有阅读进度条，页面底部有「下一页」。代码块右上角可一键复制。</p>
</div>
"""

    B["pages/00-roadmap.html"] = """
<span class="eyebrow">第 0 章 · 开始</span>
<h1>零基础学习路线</h1>
<p class="lead">Paimon 对零基础并不友好。最聪明的做法不是直接啃它，而是先补一层地基，再进入正题。这一章给你一张全局地图。</p>

<h2>为什么不能直接学 Paimon</h2>
<p>Paimon 的官方文档默认你已经懂 SQL、懂表、懂 Flink、懂数据湖。如果这些都不熟，你会卡在「这个词是什么意思」，而不是「这个设计为什么好」。结果就是看十分钟、放弃。</p>
<p>所以本教程的策略是：<strong>先用四章把地基打牢，再正式进入 Paimon 本体</strong>。地基不深，但缺了会处处卡壳。</p>

<div class="callout key">
<span class="tag">核心思路</span>
<p>不要以「学 Paimon」为起点，而要以「补齐学 Paimon 所需的基础」为起点。这样你会轻松很多，也更不容易放弃。</p>
</div>

<h2>知识依赖关系</h2>
<p>下面是各部分之间的依赖。箭头表示「先学上面，再学下面」：</p>
<div class="flow">
<div class="node"><div class="nt">Linux 与终端</div><div class="nd">能跑命令、懂路径</div></div>
<div class="arrow">↓</div>
<div class="node"><div class="nt">SQL 与数据建模</div><div class="nd">表 / 主键 / 分区 / 数仓</div></div>
<div class="arrow">↓</div>
<div class="node"><div class="nt">大数据与计算引擎</div><div class="nd">批 vs 流 / Spark / Flink</div></div>
<div class="arrow">↓</div>
<div class="node"><div class="nt">CDC 与湖仓</div><div class="nd">变更捕获 / 表格式由来</div></div>
<div class="arrow">↓</div>
<div class="node brand"><div class="nt">Apache Paimon</div><div class="nd">概念 → 上手 → 实战 → 调优</div></div>
</div>

<h2>建议时间安排</h2>
<div class="table-wrap">
<table>
<thead><tr><th>阶段</th><th>对应章节</th><th>学什么</th><th>建议时长</th><th>达标标志</th></tr></thead>
<tbody>
<tr><td>第一阶段</td><td>第 1–2 章</td><td>Linux 命令 + SQL + 数仓概念</td><td>约 1 周</td><td>能写简单查询、看懂表结构、会用终端</td></tr>
<tr><td>第二阶段</td><td>第 3–4 章</td><td>批/流区别 + Spark/Flink + CDC + 湖仓</td><td>约 1–2 周</td><td>能说清流批差异、CDC 与湖仓是什么</td></tr>
<tr><td>第三阶段</td><td>第 5–8 章</td><td>Paimon 概念 + 环境搭建 + Quick Start</td><td>约 1 周</td><td>能跑通最小示例、理解核心特性</td></tr>
<tr><td>第四阶段</td><td>第 9–10 章</td><td>CDC 入湖实战 + 表类型与调优</td><td>约 1 周</td><td>能搭一条实时入湖链路</td></tr>
<tr><td>第五阶段</td><td>第 11–13 章</td><td>选型对比 + 排错 + 继续提升</td><td>按需</td><td>能回答「为什么选 Paimon」</td></tr>
</tbody>
</table>
</div>

<h2>三种读法</h2>
<div class="cards">
<div class="card"><div class="ttl">完全零基础</div><div class="desc">从第 0 章一路读到第 13 章，别跳。每章练习都做一遍。</div></div>
<div class="card"><div class="ttl">有 SQL/Linux 基础</div><div class="desc">快速扫第 1–2 章，从第 3 章开始认真读。</div></div>
<div class="card"><div class="ttl">懂大数据，只想学 Paimon</div><div class="desc">直接从第 5 章开始，配合第 6–10 章动手。</div></div>
</div>

<div class="callout warn">
<span class="tag">现在先别碰</span>
<p>Paimon 源码、极复杂的 Flink 作业、LSM 底层论文级细节、四种表格式的深度选型辩论——这些现在学性价比太低，等你跑通 Quick Start、做完实战后再回头看。</p>
</div>

<h2>本周最小目标</h2>
<ol class="steps">
<li>学会基础 SQL 查询（<code>select</code> / <code>where</code> / <code>group by</code> / <code>join</code>）。</li>
<li>理解「表、主键、分区、ETL、数仓」这几个词。</li>
<li>知道 Spark、Flink、CDC 分别是干什么的。</li>
</ol>
<p>完成这三件事，再看 Paimon 就不会完全懵。下一章我们从最基础的 Linux 与终端开始。</p>
"""

    return B
