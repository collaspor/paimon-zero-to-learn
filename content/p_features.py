# -*- coding: utf-8 -*-
"""第 5b 章：核心特性详解（流批一体 / 主键更新 / Changelog / Time Travel / Schema Evolution / 多引擎）"""


def build(code, term, exercise):
    B = {}

    B["pages/05b-features.html"] = """
<span class="eyebrow">第 5+ 章 · 学 Paimon</span>
<h1>核心特性详解</h1>
<p class="lead">第 5 章用 6 张卡片快速过了一遍 Paimon 的卖点。但「卖点」和「真懂」之间隔着一句话：<strong>它到底解决了什么痛点？底层凭什么做到？我该怎么用？</strong>这一章就把这 6 大特性逐个掰开揉碎，每个都讲清「痛点 → 原理 → 怎么配 → 怎么用」，并配可运行的 SQL/配置。读完这章，你才算真正「认识」了 Paimon。</p>

<div class="callout note">
<span class="tag">怎么读这一章</span>
<p>不用死记配置参数。重点是建立「<strong>每个特性是为了解决什么麻烦</strong>」的直觉。具体参数用到时回来查即可。每节末尾都有一句「一句话记住」。</p>
</div>

<h2 id="feat-stream-batch">特性一 · 流批一体（Unified Streaming &amp; Batch）</h2>

<h3>先说痛点：为什么传统架构要存两份数据</h3>
<p>在 Paimon 之前，很多公司被「<strong>Lambda 架构</strong>」折磨：实时和离线是两套完全独立的链路——</p>
<div class="flow">
<div class="node"><div class="nt">实时链路</div><div class="nd">Kafka + Flink，秒级，给实时大屏</div></div>
<div class="node"><div class="nt">离线链路</div><div class="nd">Hive/数仓，T+1，给报表</div></div>
<div class="arrow">↓ 两套各干各的</div>
<div class="node brand"><div class="nt">麻烦来了</div><div class="nd">同一份业务数据存两份、算两遍、口径还经常对不上</div></div>
</div>
<p>打个比方：这就像一家店为了「现做现卖」和「批量备货」<strong>各开了一个厨房</strong>，食材买两份、菜谱维护两套，最后两个厨房做出来的同一道菜味道还不一样——既贵又容易出错。</p>

<h3>Paimon 怎么解决：一份数据，两种读法</h3>
<p>Paimon 的「流批一体」意思是：<strong>数据只存一份（一张 Paimon 表），既能像 Kafka 那样被流式订阅，也能像 Hive 表那样被批量扫描。</strong>到底是「流」还是「批」，由你查询时的模式决定，而不是由存储决定。</p>
<div class="table-wrap">
<table>
<thead><tr><th>同一张 Paimon 表</th><th>批读（Batch）</th><th>流读（Streaming）</th></tr></thead>
<tbody>
<tr><td>读到什么</td><td>当前这一刻的全量快照</td><td>从某个点开始，持续吐出后续的新变化</td></tr>
<tr><td>像什么</td><td>像查一张普通的表</td><td>像订阅一个消息队列</td></tr>
<tr><td>典型用途</td><td>跑报表、离线分析、补数</td><td>实时大屏、下游实时加工</td></tr>
</tbody>
</table>
</div>
""" + code("sql", "同一张表：批读 vs 流读（Flink SQL）", """-- ① 批读：拿当前全量（默认就是批，适合跑报表）
SET 'execution.runtime-mode' = 'batch';
SELECT city, SUM(amount) FROM orders GROUP BY city;

-- ② 流读：把这张表当成「带历史的消息流」持续订阅
SET 'execution.runtime-mode' = 'streaming';
SELECT * FROM orders /*+ OPTIONS('scan.mode'='latest') */;
-- 这个查询不会结束，新数据写进来就会被持续读到""") + """
<div class="callout key">
<span class="tag">一句话记住</span>
<p>流批一体 = <strong>存一份、两种读</strong>。省掉了「实时一套、离线一套」的双倍存储和双倍维护，口径天然统一。</p>
</div>

<h2 id="feat-pk-update">特性二 · 主键更新强（这是 Paimon 的看家本领）</h2>

<h3>先说痛点：数据湖天生「怕改」</h3>
<p>早期数据湖（一堆 Parquet 文件）擅长「<strong>只追加</strong>」——日志、埋点这种写了就不动的数据。但现实业务里数据天天变：订单状态从「待付款」改成「已发货」、用户改了手机号。要在「一堆不可变文件」上原地改一行，几乎做不到，传统做法只能<strong>把整个分区的文件全部读出来、改完再整个重写</strong>，又慢又费。</p>

<h3>Paimon 怎么解决：用 LSM 把「改」变成「追加 + 后台合并」</h3>
<p>Paimon 的主键表借用了数据库（如 RocksDB/HBase）里的 <strong>LSM-Tree</strong> 思路。核心一句话：<strong>不原地改，先把新值追加进去，读的时候按主键取最新的那条，后台再慢慢把新旧合并干净。</strong></p>
""" + term("upsert", "update + insert", "写一条数据时：主键已存在就当成「更新」，不存在就当成「插入」。你不用关心这条到底是新增还是修改，直接写就行，Paimon 自己判断。CDC 入湖几乎全靠它。") + term(
        "LSM-Tree", "Log-Structured Merge-Tree", "一种「先写内存、攒够了有序刷盘、后台再分层合并」的存储结构。它把随机更新转化成顺序追加，所以高频写/改特别快。Paimon 主键表的底座就是它。") + """
<div class="flow">
<div class="node"><div class="nt">① 写入</div><div class="nd">新值先进内存，再有序刷成小文件</div></div>
<div class="arrow">↓ 同主键的新值「盖」在旧值上</div>
<div class="node"><div class="nt">② 读取</div><div class="nd">按主键合并多个文件，只返回最新的那条</div></div>
<div class="arrow">↓ 后台异步</div>
<div class="node brand"><div class="nt">③ Compaction</div><div class="nd">把零散小文件合并、清掉被覆盖的旧值</div></div>
</div>

<h3>关键配置：merge-engine（同主键的多条怎么合）</h3>
<p>主键相同的记录来了好几条，到底怎么合成一条？这由 <strong>merge-engine（合并引擎）</strong> 决定。这是主键表最重要的一个选项，必须搞懂：</p>
<div class="table-wrap">
<table>
<thead><tr><th>merge-engine</th><th>怎么合并</th><th>适用场景</th></tr></thead>
<tbody>
<tr><td><code>deduplicate</code>（默认）</td><td>只保留最新的那条，旧的丢弃</td><td>最常见：CDC 同步，要表里永远是最新状态</td></tr>
<tr><td><code>partial-update</code></td><td>多条按列「拼起来」：这条更新了 A 列、那条更新了 B 列，合并后两列都更新</td><td>多个数据源各写宽表的一部分列（实时宽表）</td></tr>
<tr><td><code>aggregation</code></td><td>同主键按聚合函数累加/求和/取最大等</td><td>实时累计指标，如累计金额、累计点击数</td></tr>
<tr><td><code>first-row</code></td><td>只保留第一条，后来的忽略</td><td>去重、只要首次出现的记录</td></tr>
</tbody>
</table>
</div>
""" + code("sql", "建主键表 + 指定 merge-engine", """-- 主键表：PRIMARY KEY ... NOT ENFORCED
-- merge-engine = deduplicate：表里始终是每个 order_id 的最新状态
CREATE TABLE orders (
    order_id   BIGINT,
    status     STRING,
    amount     DECIMAL(10,2),
    updated_at TIMESTAMP,
    PRIMARY KEY (order_id) NOT ENFORCED
) WITH (
    'merge-engine' = 'deduplicate',
    'bucket' = '4'
);

-- 写第一次：插入
INSERT INTO orders VALUES (1001, 'PAID', 200.0, TIMESTAMP '2026-06-24 10:00:00');
-- 同一个 order_id 再写：自动变成更新（upsert），表里只会有一条最新的
INSERT INTO orders VALUES (1001, 'SHIPPED', 200.0, TIMESTAMP '2026-06-24 11:00:00');
-- 查询结果：order_id=1001 只有一行，status='SHIPPED'""") + """
""" + code("sql", "partial-update：多源拼一张宽表", """-- 用户基础信息和用户行为分别由两条流写入，各更新各的列
CREATE TABLE user_wide (
    user_id  BIGINT,
    name     STRING,      -- 来源 A：用户表
    city     STRING,      -- 来源 A
    last_buy TIMESTAMP,   -- 来源 B：行为流
    PRIMARY KEY (user_id) NOT ENFORCED
) WITH ('merge-engine' = 'partial-update');

-- A 流写：只填 name/city，last_buy 给 NULL
-- B 流写：只填 last_buy，name/city 给 NULL
-- Paimon 自动把两边非空的列「拼」到同一行 —— 不会互相覆盖成 NULL""") + """
<div class="callout warn">
<span class="tag">必须想清楚 bucket</span>
<p>主键表写入前要定 <code>bucket</code>（桶数）——它决定写入并行度和后续扩展性。建表时按数据量评估，事后改 bucket 要重组数据、成本不低。这点第 10 章会专门调优。</p>
</div>
<div class="callout key">
<span class="tag">一句话记住</span>
<p>主键更新强 = <strong>LSM 把「改」变成「追加 + 后台合并」</strong>，再用 merge-engine 决定同主键怎么合。这就是 Paimon 吃下 CDC、做实时宽表的根本原因。</p>
</div>

<h2 id="feat-changelog">特性三 · Changelog（变更日志，让下游能「增量」消费）</h2>

<h3>先说痛点：下游怎么知道「这次改了啥」</h3>
<p>假设你有一张实时汇总表，下游还想基于它再做一层加工（比如再汇总一次）。如果下游每次都把整张表重新读一遍重算，数据一大就扛不住。它真正需要的是：<strong>只告诉我「相比上次，哪些行新增了、哪些被改了、改成了什么」</strong>——这就是 changelog。</p>
""" + term("changelog", "变更日志", "把表的变化表达成一条条带「操作类型」的记录流：+I（插入）、-U（更新前的旧值）、+U（更新后的新值）、-D（删除）。下游拿到它，就能只处理「增量」，而不用全量重算。") + """
<h3>Paimon 怎么解决：changelog-producer</h3>
<p>Paimon 能在写入时顺便产出 changelog，怎么产由 <strong>changelog-producer</strong> 控制：</p>
<div class="table-wrap">
<table>
<thead><tr><th>changelog-producer</th><th>含义</th><th>代价 / 场景</th></tr></thead>
<tbody>
<tr><td><code>none</code>（默认）</td><td>不额外产出完整 changelog</td><td>最省，下游不需要精确增量时用</td></tr>
<tr><td><code>input</code></td><td>直接把输入的变更流当 changelog 透传</td><td>输入本身就是干净的 CDC 流时最划算</td></tr>
<tr><td><code>lookup</code></td><td>写入时通过查询补全变更前后的完整记录</td><td>能产出准确 changelog，有额外开销</td></tr>
<tr><td><code>full-compaction</code></td><td>在全量合并时产出 changelog</td><td>延迟较高但代价低，对时效要求不高时用</td></tr>
</tbody>
</table>
</div>
""" + code("sql", "建表时开启 changelog，供下游流式增量消费", """CREATE TABLE dwd_orders (
    order_id BIGINT,
    status   STRING,
    amount   DECIMAL(10,2),
    PRIMARY KEY (order_id) NOT ENFORCED
) WITH (
    'changelog-producer' = 'lookup'   -- 产出准确的变更前后值
);

-- 下游：流式读这张表的 changelog，只处理增量
SET 'execution.runtime-mode' = 'streaming';
SELECT * FROM dwd_orders;
-- 读到的就是 +I/-U/+U/-D 这样的变更流，可以接着往下游再加工""") + """
<div class="callout key">
<span class="tag">一句话记住</span>
<p>Changelog = <strong>把「表的变化」做成一条可订阅的变更流</strong>，让下游只算增量、不全量重跑。是搭实时数仓「层层加工（ODS→DWD→DWS）」的关键。</p>
</div>

<h2 id="feat-time-travel">特性四 · Time Travel（时间旅行，回到过去某个版本）</h2>

<h3>先说痛点：数据被改错了，怎么对账 / 回滚</h3>
<p>数据天天在变。突然有人问你「<strong>昨天下午 3 点这张表是什么样</strong>」，或者一个错误的写入把数据搞乱了想回退——传统文件堆做不到，因为旧文件可能已经被覆盖。</p>

<h3>Paimon 怎么解决：snapshot + 按版本/时间查询</h3>
<p>还记得第 6 章会讲的 snapshot 吗？Paimon <strong>每次提交写入都会生成一个新的 snapshot（版本号 + 时间戳）</strong>，旧版本在过期之前都还在。于是你可以指定「读哪个版本」或「读哪个时间点」。</p>
""" + term("snapshot", "快照 / 版本", "某次提交后表的完整状态的一个「存档点」，有递增的版本号和时间戳。读表其实就是「读某个 snapshot」，默认读最新的那个；指定旧的就实现了时间旅行。") + """
""" + code("sql", "时间旅行：按版本号 / 按时间查历史", """-- 按 snapshot 版本号查（查第 5 个版本时的样子）
SELECT * FROM orders /*+ OPTIONS('scan.snapshot-id'='5') */;

-- 按时间点查（查那个毫秒时间戳之前最近的版本）
SELECT * FROM orders /*+ OPTIONS('scan.timestamp-millis'='1750000000000') */;

-- 看这张表有哪些历史版本（系统表）
SELECT snapshot_id, commit_time FROM `orders$snapshots`;""") + """
<div class="callout note">
<span class="tag">还能用来「增量取一段」</span>
<p>除了查某一个历史点，还能查「<strong>版本 3 到版本 7 之间发生了哪些变化</strong>」（<code>incremental-between</code>），常用于补数和对账。</p>
</div>
<div class="callout warn">
<span class="tag">历史不是永久保留</span>
<p>snapshot 会按保留策略过期（如默认保留最近 N 个 / 一段时间），过期后旧版本的数据文件会被物理清理，就回不去了。需要长期可回溯的，要调大保留配置。</p>
</div>
<div class="callout key">
<span class="tag">一句话记住</span>
<p>Time Travel = <strong>每次写入存一个版本</strong>，于是能按「版本号」或「时间点」读历史，用于对账、排查、回滚。代价是历史版本会按策略过期。</p>
</div>

<h2 id="feat-schema-evolution">特性五 · Schema Evolution（表结构演进，加字段不用重写历史）</h2>

<h3>先说痛点：业务要加个字段，难道要重刷几个 T 的历史数据？</h3>
<p>业务永远在变。今天产品说「订单表加一个『优惠券 ID』字段」。如果表很大、历史数据几个 TB，传统方式可能要把所有历史文件读出来、加上新列、再全部重写——既慢又危险。</p>

<h3>Paimon 怎么解决：只改元数据，老数据照常读</h3>
<p>Paimon 把「表结构（schema）」也当成<strong>带版本的元数据</strong>来管理。加列、改列名、改兼容类型时，它<strong>只是登记一个新的 schema 版本，完全不动历史数据文件</strong>。读老数据时，缺的新列自动按 NULL/默认值补齐。</p>
""" + term("schema evolution", "表结构演进", "在不重写历史数据的前提下，安全地变更表结构：加列、删列、改列名、做兼容的类型放宽（如 INT→BIGINT）。靠的是把 schema 也做成带版本的元数据。") + """
""" + code("sql", "在线加字段 / 改名 / 放宽类型", """-- 加一列：历史数据这列自动为 NULL，无需重写
ALTER TABLE orders ADD coupon_id BIGINT;

-- 改列名
ALTER TABLE orders RENAME amount TO total_amount;

-- 兼容地放宽类型（INT -> BIGINT 安全）
ALTER TABLE orders MODIFY order_id BIGINT;""") + """
<div class="callout warn">
<span class="tag">不是什么改动都安全</span>
<p>「加列、改名、放宽类型」一般安全；但「<strong>缩窄类型</strong>」（如 BIGINT→INT 可能溢出）、删主键列这类有风险或不被允许。生产改结构前先在测试表验证。</p>
</div>
<div class="callout key">
<span class="tag">一句话记住</span>
<p>Schema Evolution = <strong>结构变更只改元数据、不重写历史</strong>。业务加字段这种高频需求，从「重刷全表的大工程」变成「一条 ALTER 秒级完成」。</p>
</div>

<h2 id="feat-multi-engine">特性六 · 多引擎查询（一份数据，多个引擎都能读）</h2>

<h3>先说痛点：换个工具就要搬一次数据</h3>
<p>实时用 Flink、离线用 Spark、对外快查用 StarRocks……如果每个工具都要把数据导一份到自己的格式里，就会出现「<strong>同一份数据在系统里躺了好几份</strong>」：存储翻倍、同步链路一堆、还容易不一致。</p>

<h3>Paimon 怎么解决：开放格式 + 共享元数据</h3>
<p>Paimon 用的是<strong>开放的存储格式</strong>（数据是 Parquet/ORC，元数据是公开协议），并且能把表登记到共享的元数据服务（如 Hive Metastore）。于是多个引擎都能<strong>直接读同一份 Paimon 表，数据不用搬</strong>。</p>
<div class="flow">
<div class="node brand"><div class="nt">一份 Paimon 表</div><div class="nd">数据只存一份</div></div>
<div class="arrow">↓ 多个引擎各取所需</div>
<div class="node"><div class="nt">Flink</div><div class="nd">实时写 / 流读</div></div>
<div class="node"><div class="nt">Spark</div><div class="nd">批量分析</div></div>
<div class="node"><div class="nt">StarRocks / Trino</div><div class="nd">OLAP 极速查</div></div>
</div>
<div class="table-wrap">
<table>
<thead><tr><th>引擎</th><th>对 Paimon 的支持</th><th>典型角色</th></tr></thead>
<tbody>
<tr><td>Flink</td><td>最完整（流写、流读、批读、CDC）</td><td>实时写入与加工（最佳拍档）</td></tr>
<tr><td>Spark</td><td>读写都支持，SQL 友好</td><td>批处理、离线分析</td></tr>
<tr><td>Hive</td><td>通过 Hive Catalog 查询</td><td>对接存量数仓</td></tr>
<tr><td>StarRocks / Doris / Trino</td><td>外部 catalog 直接查</td><td>对外 OLAP 极速查询</td></tr>
</tbody>
</table>
</div>
<p>这一块每个引擎怎么接，<strong>第 14~19 章「生态与引擎」篇</strong>有逐个的大白话实操，这里只需建立「一份数据多引擎共享」的认知。</p>
<div class="callout key">
<span class="tag">一句话记住</span>
<p>多引擎查询 = <strong>开放格式 + 共享元数据，数据不搬家</strong>。各引擎各司其职（实时写、批分析、快查），都读同一份，省存储、避免不一致。</p>
</div>

<h2 id="feat-recap">把六大特性串起来</h2>
<p>这六个特性不是孤立的卖点，而是围绕「<strong>实时湖仓</strong>」这一个目标互相咬合的：</p>
<div class="table-wrap">
<table>
<thead><tr><th>特性</th><th>解决的核心痛点</th><th>底层靠什么</th></tr></thead>
<tbody>
<tr><td>流批一体</td><td>不想存两份、维护两套</td><td>同一份数据 + 批/流两种读模式</td></tr>
<tr><td>主键更新强</td><td>数据湖天生怕「改」</td><td>LSM + merge-engine</td></tr>
<tr><td>Changelog</td><td>下游想只算增量</td><td>changelog-producer 产出变更流</td></tr>
<tr><td>Time Travel</td><td>要对账 / 回滚到历史</td><td>每次提交存一个 snapshot</td></tr>
<tr><td>Schema Evolution</td><td>加字段不想重刷历史</td><td>schema 也做成带版本的元数据</td></tr>
<tr><td>多引擎查询</td><td>换工具不想搬数据</td><td>开放格式 + 共享元数据</td></tr>
</tbody>
</table>
</div>

""" + exercise("练习 5b-1", "<p>用自己的话回答三个问题：① 「流批一体」省掉了传统 Lambda 架构的什么麻烦？② 主键表里 <code>merge-engine='partial-update'</code> 适合什么场景？③ Time Travel 为什么不能无限回溯历史？</p>",
        "<p>① 省掉了「实时一套链路 + 离线一套链路」带来的双倍存储、双倍维护和口径不一致——改成一份数据、批流两种读。② 适合多个数据源各写一张宽表的不同列（比如 A 源写 name/city、B 源写最近购买时间），Paimon 会把各自非空的列拼到同一行而不互相覆盖。③ 因为历史 snapshot 会按保留策略过期，过期后对应的旧数据文件会被物理清理，所以只能回溯到尚未过期的版本；要长期可回溯需调大保留配置。</p>") + """

<div class="callout tip">
<span class="tag">本章目标</span>
<p>能对每个特性说清「解决什么痛点 + 大概怎么做到」，并知道关键开关（merge-engine、changelog-producer、snapshot、bucket）大致管什么。下一章（第 6 章）进入这些特性背后的存储结构与原理细节。</p>
</div>
"""

    return B
