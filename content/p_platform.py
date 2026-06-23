# -*- coding: utf-8 -*-
"""第 18–19 章：StarRocks / Iceberg 对比 + WeData（大白话版）"""


def build(code, term, exercise):
    B = {}

    # ------------------------------------------------------------------ 第 18 章
    B["pages/18-starrocks.html"] = """
<span class="eyebrow">第 18 章 · 生态与引擎</span>
<h1>StarRocks + Paimon：让查询快到飞起</h1>
<p class="lead">到这儿，数据已经被 Flink/Spark 好好地写进了 Paimon 这个"冰箱"。但还差最后一步：<strong>怎么让老板、运营点开报表，唰一下、一两秒就出结果？</strong>这就需要请出"飞毛腿传菜员"——<strong>StarRocks</strong>。它的绝活是：<em>直接冲进 Paimon 这个冰箱里快速取数，不用先把菜搬到自己家</em>。</p>

<div class="callout note">
<span class="tag">关于你提到的"Setats"</span>
<p>你之前说的 <strong>Setats</strong>，在现在的大数据生态里没有完全同名的产品，最贴近的就是 <strong>StarRocks</strong>（一个主打"查得快"的引擎）。所以本章按 StarRocks 来讲。如果你心里想的是另一个产品，把名字告诉我，我立马替换成那个。</p>
</div>

<h2>先想清楚：都有 Paimon 了，为啥还要它？</h2>
<p>你可能会问：数据都在 Paimon 里了，Spark 也能查，干嘛还多请一个 StarRocks？打个比方就懂了：</p>
<div class="callout key">
<span class="tag">大厨 vs 传菜飞毛腿</span>
<p><strong>Spark/Flink 像大厨</strong>：擅长后厨里大批量加工、慢工出细活，但你让大厨"立刻给一桌客人上菜"，他忙不过来、也慢。<strong>StarRocks 像专职传菜的飞毛腿</strong>：不负责做菜，专门负责<em>客人一点单，几秒钟把菜端上桌</em>，而且能同时伺候很多桌。</p>
<p>所以分工是：<strong>Flink/Spark 负责把数据写好、加工好放进 Paimon；StarRocks 负责对外飞快地查。</strong>各干各擅长的，谁也别抢谁的活。</p>
</div>
<p>那"查得快"靠的什么本事？两个关键词，用大白话解释一下：</p>
""" + term("OLAP", "分析型查询", "就是“为了分析而做的查询”：动不动就对一大堆数据做汇总、分组、各种维度对比（比如“按城市按月统计销售额”）。报表、看板、即席分析全属于 OLAP。和它相对的 OLTP 是“管单条记录的增删改”，比如下个单、改个地址。") + term(
        "MPP", "多机并行", "干活的诀窍：把一个大查询<strong>拆成很多小份，分给好多台机器同时算</strong>，最后把结果拼起来。就像一道大题分给一个班同时做，当然比一个人做快。StarRocks 靠这招实现“高并发 + 低延迟”。") + """

<h2>第一步：让 StarRocks "认识" Paimon 这个冰箱</h2>
<p>StarRocks 用一个叫"外部 catalog"的东西，<strong>直接挂载到 Paimon 仓库上</strong>——注意，是"挂载"，不是"把数据搬过来"。它查的就是 Paimon 里那一份原始数据：</p>
""" + code("sql", "用 MySQL 协议客户端连上 StarRocks 后执行", """-- 创建一个指向 Paimon 的"外部 catalog"（相当于给冰箱配把钥匙）
CREATE EXTERNAL CATALOG paimon_catalog
PROPERTIES (
    'type' = 'paimon',
    'paimon.catalog.type' = 'filesystem',
    'paimon.catalog.warehouse' = 'hdfs:///warehouse/paimon'
);""") + """
<p>如果你的 Paimon 是登记在 Hive Metastore 里的（还记得第 17 章那本"登记册"吗），就把 <code>paimon.catalog.type</code> 改成 <code>hive</code>，再补上登记册地址即可。</p>

<h2>第二步：像查自家表一样，查 Paimon</h2>
<p>钥匙配好了，就能直接查，享受 StarRocks 的并行加速：</p>
""" + code("sql", "切进去，然后查", """-- 看看这把钥匙能打开哪些库
SHOW DATABASES FROM paimon_catalog;

-- 切进去
SET CATALOG paimon_catalog;
USE default;

-- 直接查 Paimon 表，StarRocks 会并行加速
SELECT city, COUNT(*) AS cnt, SUM(amount) AS total
FROM orders
GROUP BY city
ORDER BY total DESC;""") + """
<div class="callout key">
<span class="tag">最值钱的一句：数据压根不用搬</span>
<p>注意了——StarRocks 查的<strong>就是 Paimon 冰箱里那一份数据本尊，没有任何额外的导入和拷贝</strong>。这意味着：Flink 前一秒刚实时写进 Paimon，StarRocks 后一秒就能查到最新的，对外提供服务。数据不搬家、还能查得飞快，这就是大家说的"湖上查询加速"。</p>
</div>

<h2>第三步：把整条链路串起来看一眼</h2>
<p>到这里，一条完整的"实时数据从产生到被秒查"的链路就齐了：</p>
<div class="flow">
<div class="node"><div class="nt">MySQL / Kafka</div><div class="nd">数据源（原料）</div></div>
<div class="arrow">↓ Flink CDC 实时搬进来</div>
<div class="node brand"><div class="nt">Paimon（湖上唯一一份数据）</div><div class="nd">实时、可更新、带历史存档</div></div>
<div class="arrow">↓ StarRocks 配把钥匙直接查</div>
<div class="node"><div class="nt">StarRocks</div><div class="nd">对外秒级报表 / BI 看板 / 即席查询</div></div>
</div>
<p>这套链路你其实已经会搭前两段了（源 → Flink → Paimon），现在补上最后一段"对外快查"，整条就通了。</p>

<h2>想查得更快？三个小窍门</h2>
<ul>
<li><strong>让 Paimon 那头"勤整理"</strong>：保证 compaction 跟得上、小文件别太多，StarRocks 扫起来才快（回顾第 10 章）。</li>
<li><strong>查询时"只取需要的"</strong>：带上分区过滤条件（分区裁剪）、只 SELECT 用得到的列（列裁剪），别动不动 <code>SELECT *</code> 全捞。</li>
<li><strong>固定报表用"预先算好"</strong>：对那种天天看、并发又高的固定报表，可以在 StarRocks 里建"物化视图"提前算好，查的时候直接拿现成结果。</li>
</ul>

""" + exercise("练习 18-1", "<p>同事问你：“咱已经有 Paimon 了，为啥还要 StarRocks？直接用 Spark 查它不就完了？”请用“分工”的角度，用大白话回答他。</p>",
        "<p>因为分工不一样。Spark 是“大厨”，擅长后厨里慢工出细活的批量加工，但让它直接面对一大群用户做秒级查询，它慢、也撑不住高并发。StarRocks 是“飞毛腿传菜员”，天生就是为“查得快、同时伺候很多人”设计的（MPP 多机并行）。所以让 Flink/Spark 负责写和加工，StarRocks 负责对外快查；而且 StarRocks 直接查 Paimon，数据不用搬，又快又省。</p>") + """

<div class="callout tip">
<span class="tag">这一章你要带走的</span>
<p>用大白话讲清 OLAP/MPP 是啥、StarRocks 凭啥快，会用"外部 catalog"让它直查 Paimon，并能默画出"源 → Flink → Paimon → StarRocks"这条实时分析链路。最后一章咱们做个收尾：把 Paimon 和它的"同行对手" Iceberg 摆一起比比，再认识把这整套托管起来的云平台 WeData。</p>
</div>
"""

    # ------------------------------------------------------------------ 第 19 章
    B["pages/19-iceberg-wedata.html"] = """
<span class="eyebrow">第 19 章 · 生态与引擎</span>
<h1>Iceberg 对比 &amp; WeData 平台：选型与"省心方案"</h1>
<p class="lead">生态篇最后一章，做两件事：① 把 Paimon 和它最常被拿来比的"同行对手" <strong>Apache Iceberg</strong> 摆一块儿，帮你以后做选型时心里有数；② 认识 <strong>WeData</strong>——一个能把前面这一整套（Flink、Paimon、调度……）<em>托管起来、让你不用自己搭</em>的腾讯云平台。</p>

<h2>一、Paimon 和 Iceberg：两个牌子的"冰箱"，二选一</h2>
<p>还记得第 14 章的比方吗——Paimon 和 Iceberg 都是"冰箱"（表格式），干的是同一类活：让你在数据湖上拥有"像数据库表一样"的能力（能保证数据一致、能改表结构、能穿越看历史）。<strong>所以它俩是二选一，不会两个一起上。</strong>区别在于各自的"脾气"和擅长场景。</p>
""" + term("Apache Iceberg", "冰山", "由 Netflix 发起、现在是 Apache 顶级项目的开放表格式。出道早、生态特别成熟，几乎所有引擎和云厂商都支持它，尤其擅长“大规模批量分析”和“很少变动的超大表”。") + """

<p>下面这张表，左右一对照就清楚了。你不用背，理解"一个偏实时、一个偏批量"这条主线即可：</p>
<div class="table-wrap">
<table>
<thead><tr><th>比什么</th><th>Apache Paimon</th><th>Apache Iceberg</th></tr></thead>
<tbody>
<tr><td>骨子里的结构</td><td>LSM 树（天生适合频繁更新）</td><td>一堆不可变文件 + 清单账本</td></tr>
<tr><td><strong>最拿手的</strong></td><td><strong>实时更新 / CDC 入湖 / 主键 upsert</strong></td><td><strong>大规模批量分析、很少变的大表</strong></td></tr>
<tr><td>实时/流式能力</td><td>强（前身就是 Flink Table Store）</td><td>有，但"频繁更新"不是它强项</td></tr>
<tr><td>主键更新（upsert）</td><td>一等公民，开箱即用</td><td>能做，但更偏"批量合并"那种</td></tr>
<tr><td>生态成熟度</td><td>较新，但涨势很猛</td><td>非常成熟，支持的工具/云厂商极广</td></tr>
<tr><td>啥时候选它</td><td>实时数仓、数据要频繁改</td><td>离线数仓、海量历史、以读为主</td></tr>
</tbody>
</table>
</div>

<div class="callout key">
<span class="tag">一句话教你选</span>
<p>数据<strong>老在变、要实时、要按主键更新（典型就是 CDC 把数据库实时同步入湖）→ 闭眼选 Paimon</strong>；如果是<strong>海量历史数据、主要拿来批量分析、很少改 → Iceberg 又稳又成熟</strong>。不少大公司其实两个都用，按场景分开摆——这很正常，不冲突。</p>
</div>

<h2>二、WeData：不想自己搭这一摊，就交给它</h2>
<p>说句实在话：前面每一章你都是<em>自己装 Flink、自己配 jar、自己起集群、自己盯作业</em>。<strong>学习阶段这么干特别值</strong>——因为你彻底搞懂了每一层在干嘛。但真到了公司生产环境，自己运维这一整套，又累又容易出事。这时候就轮到 <strong>WeData</strong> 登场了。</p>
<div class="callout key">
<span class="tag">打个比方：自己开火做饭 vs 用中央厨房</span>
<p>前面你做的，相当于<strong>自己买灶、买锅、买菜、自己掌勺</strong>——啥都懂，但很累。<strong>WeData 相当于一个"中央厨房 + 店长"</strong>：灶台（计算资源）现成的、配菜（数据接入）点几下就配好、上菜节奏（调度）自动安排、出问题还有人盯着报警。你专心"想吃啥（业务逻辑）"，脏活累活平台包了。</p>
</div>
""" + term("WeData", "腾讯云数据开发治理平台", "腾讯云的一站式大数据开发平台，把数据集成、开发（写 SQL / 编排任务）、调度、治理、运维都整合到一起，底层能对接 Flink、Spark、湖格式（含 Paimon/Iceberg）等。说白了就是：让团队不用自己搭、自己运维这一整套栈。") + """

<h3>它具体帮你省掉了什么？</h3>
<p>把你前面"亲手做的累活"和"平台上的省心形态"对照一下，一目了然：</p>
<div class="table-wrap">
<table>
<thead><tr><th>前面章节你手动做的</th><th>在 WeData 上变成了</th></tr></thead>
<tbody>
<tr><td>自己装 Flink、放 jar、起集群</td><td>平台给你现成的计算资源，开箱即用</td></tr>
<tr><td>手敲 CDC 同步命令</td><td>在界面上点点点，可视化配好同步任务</td></tr>
<tr><td>命令行提交、自己熬夜盯作业</td><td>任务编排 + 自动调度 + 出错自动报警</td></tr>
<tr><td>自己管表、管谁能看谁不能看</td><td>统一的元数据管理和权限治理</td></tr>
</tbody>
</table>
</div>

<div class="callout warn">
<span class="tag">给你的真心建议：学习顺序别搞反</span>
<p>一定要<strong>先用前面的章节把原理和手动流程跑通</strong>（知道底层到底发生了啥），<strong>再</strong>上 WeData 这类平台去提效。反过来——"只会在平台上点按钮、根本不懂底下在干嘛"——一旦出问题你会两眼一抹黑、根本不会排查。好消息是：你已经走完了前面的硬核部分，现在完全有能力看懂平台背后到底在做什么了。</p>
</div>

<h3>在 WeData 上用 Paimon，大概是这么个流程</h3>
<div class="flow">
<div class="node"><div class="nt">① 接入数据源</div><div class="nd">在"数据集成"里点选 MySQL/Kafka 等</div></div>
<div class="arrow">↓</div>
<div class="node brand"><div class="nt">② 实时写入 Paimon</div><div class="nd">用平台托管的 Flink，配置 CDC 同步到 Paimon 表</div></div>
<div class="arrow">↓</div>
<div class="node"><div class="nt">③ 开发与调度</div><div class="nd">写 SQL 任务做加工，设个周期让它自动跑</div></div>
<div class="arrow">↓</div>
<div class="node"><div class="nt">④ 查询与服务</div><div class="nd">对接 StarRocks 等，对外提供查询</div></div>
</div>
<p class="muted">具体菜单名称以腾讯云 WeData 控制台最新版为准。这里给的是"概念流程"，而它对应的，正是你前面一章一章亲手做过的每一步——只不过现在是平台替你做了。</p>

""" + exercise("练习 19-1", "<p>两道选型题，用大白话答：① 业务要把 MySQL 订单实时入湖、还得随时反映增删改，选 Paimon 还是 Iceberg？② 团队不想自己运维 Flink 集群、想点点鼠标就配好实时同步，该考虑什么？</p>",
        "<p>① 选 Paimon——“实时 + 按主键更新”正是它的拿手好戏。② 考虑 WeData 这类托管的数据开发平台：用现成的托管计算资源 + 可视化配置，代替自己搭集群、自己运维。</p>") + """

<div class="callout tip">
<span class="tag">恭喜，你学完整个生态篇了 🎉</span>
<p>到这儿，你不光会用 Paimon，还彻底理清了它和 Flink、Spark、Hive、StarRocks、Iceberg、WeData 的关系——谁存、谁算、谁快查、谁托管、谁是竞品，全都门儿清。这已经足够你在真实项目里参与技术选型、看懂架构图了。想重温整张地图就回首页，想再往深里钻就去"学习资源与下一步"那一章。</p>
</div>
"""

    return B
