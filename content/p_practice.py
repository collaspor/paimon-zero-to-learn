# -*- coding: utf-8 -*-
"""第 8–10 章：Quick Start / CDC 实战 / 进阶调优"""


def build(code, term, exercise):
    B = {}

    # ------------------------------------------------------------------ 第 8 章
    B["pages/08-quickstart.html"] = """
<span class="eyebrow">第 8 章 · 动手实践</span>
<h1>Quick Start 上手</h1>
<p class="lead">环境就绪后，用 Flink SQL 跑一个最小示例：建 catalog、建主键表、流式写入、批量查、流式查。每段 SQL 都有逐行讲解，跟着敲一遍就能体会「流批一体」。</p>

<div class="callout note">
<span class="tag">在哪敲</span>
<p>下面所有 SQL 都在第 7 章打开的 <strong>Flink SQL Client</strong>（<code>Flink SQL></code> 提示符）里执行。第一次看可以先「读懂流程」，环境装好后再逐段实操。</p>
</div>

<h2>1. 创建 Catalog</h2>
""" + term("Catalog", "目录", "Paimon 用 catalog 来管理「仓库（warehouse）」里的库和表。建好 catalog 并 USE 它之后，建的表就会落到对应的 warehouse 目录下。") + code("sql", "建一个 Paimon catalog（数据存本地）", """-- 创建一个 Paimon catalog，数据存在本地目录 /tmp/paimon
CREATE CATALOG my_catalog WITH (
    'type' = 'paimon',
    'warehouse' = 'file:/tmp/paimon'
);

-- 切换到这个 catalog
USE CATALOG my_catalog;""") + """
<p>逐行看：<code>type=paimon</code> 表示这是 Paimon catalog；<code>warehouse</code> 是表数据落盘的根目录，本地实验用 <code>file:/</code> 前缀。</p>

<h2>2. 创建主键表</h2>
""" + code("sql", "建一张 word_count 表", """-- word 作为主键：相同 word 的写入会被合并（upsert）
CREATE TABLE word_count (
    word STRING PRIMARY KEY NOT ENFORCED,
    cnt  BIGINT
);""") + """
<p><code>PRIMARY KEY NOT ENFORCED</code>：声明 <code>word</code> 是主键（Paimon 据此做 upsert/合并），<code>NOT ENFORCED</code> 表示 Flink 不强制校验唯一性（由 Paimon 在合并时保证）。</p>

<h2>3. 流式写入数据</h2>
""" + code("sql", "用数据生成器持续写入", """-- 造一个不断产生单词的临时数据源
CREATE TEMPORARY TABLE word_table (
    word STRING
) WITH (
    'connector' = 'datagen',
    'fields.word.length' = '1'
);

-- 流模式下 Paimon 写入依赖 checkpoint 来提交（生成 snapshot）
SET 'execution.checkpointing.interval' = '10 s';

-- 持续把「单词计数」写进 word_count（这是一个一直运行的流作业）
INSERT INTO word_count
SELECT word, COUNT(*) FROM word_table GROUP BY word;""") + """
<div class="callout warn">
<span class="tag">为什么必须设 checkpoint</span>
<p>流式写入时，Paimon 在每个 checkpoint 提交一次数据（生成一个 snapshot）。<strong>不设 checkpoint，数据不会真正提交、查不到。</strong>这是新手最常踩的坑。10 秒只是示例，生产要按延迟/小文件权衡。</p>
</div>

<h2>4. 批量查询当前结果</h2>
<p>新开一个 SQL Client 会话（或停掉上面的流作业后），切到批模式查当前快照：</p>
""" + code("sql", "切到批模式查询", """-- 让结果以表格形式展示
SET 'sql-client.execution.result-mode' = 'tableau';

-- 切换到批模式
SET 'execution.runtime-mode' = 'batch';

-- 查询当前 word_count（可多次执行，观察数字在变）
SELECT * FROM word_count;""") + """

<h2>5. 流式查询变化</h2>
""" + code("sql", "切到流模式持续观察", """-- 切回流模式
SET 'execution.runtime-mode' = 'streaming';

-- 持续跟踪表的变化（会不断刷新输出）
SELECT * FROM word_count;""") + """

<div class="callout key">
<span class="tag">你刚刚做了什么</span>
<p>同一张 <code>word_count</code> 表，既能<strong>流式写入</strong>，又能<strong>批量查</strong>当前快照、还能<strong>流式查</strong>变化——这就是「流批一体」的直观体验，也是 Paimon 最核心的卖点。</p>
</div>

<h2>6. 体验时间旅行（可选）</h2>
""" + code("sql", "查询历史快照", """-- 先看有哪些 snapshot
SELECT snapshot_id, commit_time FROM word_count$snapshots;

-- 查询指定 snapshot 时的数据（把 1 换成实际 id）
SET 'execution.runtime-mode' = 'batch';
SELECT * FROM word_count /*+ OPTIONS('scan.snapshot-id'='1') */;""") + """
<p><code>word_count$snapshots</code> 是 Paimon 的「系统表」，能查到这张表的版本历史——这正是第 6 章讲的 snapshot 在起作用。</p>

<h2>7. 收尾</h2>
""" + code("bash", "停止集群", """# 在 http://localhost:8081 取消正在跑的流作业后，停止本地集群
$FLINK_HOME/bin/stop-cluster.sh""") + """

""" + exercise("练习 8-1", "<p>不看上文，回答：在流模式下写入 Paimon，为什么一定要设置 checkpoint？如果忘了设，会出现什么现象？</p>",
        "<p>因为 Paimon 在每个 checkpoint 提交一次写入并生成 snapshot。不设 checkpoint，数据一直停在未提交状态，不会生成 snapshot，查询时<strong>查不到刚写入的数据</strong>（看起来像「写了没反应」）。</p>") + """

<div class="callout tip">
<span class="tag">本章目标</span>
<p>能独立跑通建 catalog → 建表 → 流写 → 批查 → 流查，并理解 checkpoint 的作用。下一章做一件更接近真实工作的事：把 MySQL 的数据实时同步进 Paimon。</p>
</div>
"""

    # ------------------------------------------------------------------ 第 9 章
    B["pages/09-cdc-practice.html"] = """
<span class="eyebrow">第 9 章 · 动手实践</span>
<h1>实战：CDC 入湖</h1>
<p class="lead">这一章把前面学的串起来，做一件真实工作里最常见的事：把 MySQL 里的数据变化（增删改）<strong>实时同步</strong>进 Paimon 表。这就是「CDC 入湖」。</p>

<h2>我们要搭的链路</h2>
<div class="flow">
<div class="node"><div class="nt">MySQL</div><div class="nd">业务库，数据会增删改</div></div>
<div class="arrow">↓ <small>读 binlog 捕获变更</small></div>
<div class="node"><div class="nt">Flink CDC</div><div class="nd">实时同步</div></div>
<div class="arrow">↓ 写入</div>
<div class="node brand"><div class="nt">Paimon 主键表</div><div class="nd">实时反映 MySQL 的最新状态</div></div>
<div class="arrow">↓ 查询</div>
<div class="node"><div class="nt">Flink / Spark</div><div class="nd">实时分析</div></div>
</div>

<h2>前置准备</h2>
<ul>
<li>第 7 章的 Flink + Paimon 环境已就绪。</li>
<li>一个可访问的 MySQL，并<strong>开启 binlog</strong>（CDC 的基础）。</li>
<li>把 <strong>Flink CDC 的 MySQL connector jar</strong> 也放进 <code>$FLINK_HOME/lib/</code>（和 Paimon jar 一起）。</li>
</ul>
""" + code("sql", "MySQL 侧：确认 binlog 已开启", """-- 在 MySQL 里执行，确认 binlog 格式为 ROW
SHOW VARIABLES LIKE 'log_bin';        -- 期望 ON
SHOW VARIABLES LIKE 'binlog_format';  -- 期望 ROW""") + """
<div class="callout note">
<span class="tag">没有现成 MySQL？</span>
<p>可以用 Docker 快速起一个开了 binlog 的 MySQL 做实验。新手如果暂时没有环境，先把本章当「读懂流程」，理解每一步在做什么即可。</p>
</div>

<h2>方式 A：整库同步（最省事）</h2>
<p>Paimon 提供了 CDC 同步动作（action），一条命令把 MySQL 整个库实时同步到 Paimon，自动建表、自动跟随 schema 变化：</p>
""" + code("bash", "用 Paimon CDC action 同步整库", """$FLINK_HOME/bin/flink run \\
    paimon-flink-action-*.jar \\
    mysql_sync_database \\
    --warehouse file:/tmp/paimon \\
    --database app_db \\
    --mysql_conf hostname=localhost \\
    --mysql_conf port=3306 \\
    --mysql_conf username=root \\
    --mysql_conf password=123456 \\
    --mysql_conf database-name=app_db \\
    --table_conf bucket=4""") + """
<p>逐项看：<code>mysql_sync_database</code> 是「整库同步」动作；<code>--warehouse</code> 是 Paimon 落盘根目录；<code>--mysql_conf</code> 是 MySQL 连接信息；<code>--table_conf bucket=4</code> 给生成的 Paimon 表设 4 个桶。提交后这是个<strong>一直运行的流作业</strong>，MySQL 一变，Paimon 就跟着变。</p>

<h2>方式 B：用 Flink SQL 手动接 CDC 源</h2>
<p>想更可控，可以在 SQL Client 里手动定义 MySQL CDC 源表，再写进 Paimon 表：</p>
""" + code("sql", "定义 MySQL CDC 源 + 写入 Paimon", """-- 1) 定义一个读取 MySQL binlog 的源表（临时表）
CREATE TEMPORARY TABLE mysql_orders (
    order_id BIGINT,
    user_id  BIGINT,
    amount   DECIMAL(10,2),
    PRIMARY KEY (order_id) NOT ENFORCED
) WITH (
    'connector'     = 'mysql-cdc',
    'hostname'      = 'localhost',
    'port'          = '3306',
    'username'      = 'root',
    'password'      = '123456',
    'database-name' = 'app_db',
    'table-name'    = 'orders'
);

-- 2) 在 Paimon catalog 里建对应的主键表
USE CATALOG my_catalog;
CREATE TABLE orders (
    order_id BIGINT PRIMARY KEY NOT ENFORCED,
    user_id  BIGINT,
    amount   DECIMAL(10,2)
);

-- 3) 流式写入：MySQL 的增删改会实时反映到 Paimon
SET 'execution.checkpointing.interval' = '10 s';
INSERT INTO orders SELECT * FROM mysql_orders;""") + """

<h2>验证：改 MySQL，看 Paimon</h2>
<ol class="steps">
<li>在 MySQL 里 <code>INSERT</code> 一条订单。</li>
<li>等一个 checkpoint（约 10 秒）。</li>
<li>在另一个 SQL Client 里批模式查 Paimon 的 <code>orders</code>，能看到这条。</li>
<li>在 MySQL 里 <code>UPDATE</code> 这条的 <code>amount</code>，再查 Paimon——金额已更新（这就是 upsert）。</li>
<li>在 MySQL 里 <code>DELETE</code> 它，再查 Paimon——它没了。</li>
</ol>
<div class="callout key">
<span class="tag">你验证了什么</span>
<p>Paimon 主键表能<strong>实时跟随源库的增、删、改</strong>，始终反映最新状态。这就是 CDC 入湖的核心价值，也是第 6 章「upsert 机制」在真实场景里的体现。</p>
</div>

<h2>常见问题</h2>
<div class="table-wrap">
<table>
<thead><tr><th>现象</th><th>原因</th><th>解决</th></tr></thead>
<tbody>
<tr><td>同步作业起不来，报 binlog 相关错</td><td>MySQL 没开 binlog / 格式不是 ROW</td><td>开启 binlog 并设 <code>binlog_format=ROW</code>，给账号授予相应权限</td></tr>
<tr><td>Paimon 查不到数据</td><td>没设 checkpoint</td><td>设置 <code>execution.checkpointing.interval</code></td></tr>
<tr><td>更新没生效，出现重复</td><td>Paimon 表没建主键</td><td>建表时声明 <code>PRIMARY KEY ... NOT ENFORCED</code></td></tr>
</tbody>
</table>
</div>

<div class="callout tip">
<span class="tag">本章目标</span>
<p>能搭起一条「MySQL → Flink CDC → Paimon」的实时入湖链路，并验证增删改实时生效。做到这一步，你已经会用 Paimon 解决真实问题了。下一章学怎么把它用好、调优。</p>
</div>
"""

    # ------------------------------------------------------------------ 第 10 章
    B["pages/10-advanced.html"] = """
<span class="eyebrow">第 10 章 · 动手实践</span>
<h1>进阶：表类型与调优</h1>
<p class="lead">会跑之后，还要会「用好」。这一章讲 Paimon 的两类表、合并引擎、分桶（bucket）和压缩（compaction）调优——这些直接决定写入吞吐、查询速度和存储成本。</p>

<h2>两类表：主键表 vs Append 表</h2>
<div class="table-wrap">
<table>
<thead><tr><th></th><th>主键表（Primary Key Table）</th><th>Append 表（Append Table）</th></tr></thead>
<tbody>
<tr><td>是否有主键</td><td>有</td><td>无</td></tr>
<tr><td>支持更新/删除</td><td>支持（upsert）</td><td>只追加</td></tr>
<tr><td>底层结构</td><td>LSM</td><td>普通追加文件</td></tr>
<tr><td>典型场景</td><td>CDC 入湖、实时宽表、状态会变的数据</td><td>日志、埋点、只增不改的明细</td></tr>
</tbody>
</table>
</div>
<p>选型很简单：<strong>数据会更新 → 主键表；只追加 → Append 表</strong>。本教程前面用的都是主键表。</p>

<h2>Merge Engine：主键相同怎么合并</h2>
<p>主键表里，主键相同的多条记录如何合并，由 <code>merge-engine</code> 决定：</p>
""" + term("deduplicate（默认）", "去重", "保留同主键的最新一条。最常用，CDC 入湖默认就是它——始终反映最新状态。") + term(
        "partial-update", "部分更新", "同主键的多条记录，按列「拼起来」。适合「多个数据流各更新一张宽表的不同列」的场景。") + term(
        "aggregation", "聚合", "同主键按配置的聚合函数（sum/max 等）合并。适合实时累加类指标。") + code("sql", "建表时指定 merge engine", """-- 部分更新：不同来源补全同一行的不同列
CREATE TABLE user_wide (
    user_id   BIGINT PRIMARY KEY NOT ENFORCED,
    name      STRING,
    last_city STRING
) WITH (
    'merge-engine' = 'partial-update'
);""") + """

<h2>Bucket：写入并行的基本单元</h2>
""" + term("bucket", "桶", "Paimon 把数据按主键 hash 分到固定数量的桶，每个桶独立写入和 compaction。bucket 数 ≈ 写入/合并的并行度。") + """
<ul>
<li><strong>太少</strong>：写入并行度不够，吞吐上不去。</li>
<li><strong>太多</strong>：小文件变多，元数据和管理开销增大。</li>
<li><strong>经验</strong>：按单桶数据量（如几 GB）估算总桶数；数据量大就多设。也可用「动态 bucket」让 Paimon 自适应。</li>
</ul>
""" + code("sql", "建表时设置 bucket", """CREATE TABLE orders (
    order_id BIGINT PRIMARY KEY NOT ENFORCED,
    amount   DECIMAL(10,2)
) WITH (
    'bucket' = '4'
);""") + """
<div class="callout warn">
<span class="tag">注意</span>
<p>固定 bucket 数建表后再改，需要重组数据，成本较高。建表前先评估好数据规模。</p>
</div>

<h2>Compaction：治理小文件</h2>
<p>流式写入会产生很多小文件（第 6 章讲过）。compaction 把它们合并，提升查询、收拢同主键数据。两种方式：</p>
<ul>
<li><strong>自动 compaction</strong>：写入作业里后台自动触发（默认行为）。简单，但会占用写入作业的资源。</li>
<li><strong>独立 compaction</strong>：单独起一个作业专门做合并，把写入和合并解耦，适合高吞吐场景。</li>
</ul>
""" + code("bash", "起一个独立 compaction 作业", """$FLINK_HOME/bin/flink run \\
    paimon-flink-action-*.jar \\
    compact \\
    --warehouse file:/tmp/paimon \\
    --database default \\
    --table orders""") + """

<h2>快照过期与文件清理</h2>
<p>第 6 章说过：删除/更新不会立刻清文件，要等 snapshot 过期。可以配置保留多少个/多久的 snapshot：</p>
""" + code("sql", "配置快照保留", """ALTER TABLE orders SET (
    'snapshot.num-retained.min' = '10',
    'snapshot.num-retained.max' = '20',
    'snapshot.time-retained' = '1 h'
);""") + """
<p>保留太久占空间、太短则时间旅行可回溯的范围变小，按需权衡。</p>

<h2>调优速查</h2>
<div class="table-wrap">
<table>
<thead><tr><th>目标</th><th>关注项</th></tr></thead>
<tbody>
<tr><td>写入吞吐不够</td><td>增大 bucket、考虑独立 compaction、调大 checkpoint 间隔</td></tr>
<tr><td>小文件太多</td><td>增大 checkpoint 间隔、开/加强 compaction、合理 bucket 数</td></tr>
<tr><td>查询慢</td><td>确保 compaction 跟得上、用好分区裁剪、列裁剪</td></tr>
<tr><td>存储涨太快</td><td>缩短 snapshot 保留、及时清理过期快照</td></tr>
</tbody>
</table>
</div>

""" + exercise("练习 10-1", "<p>判断该用哪类表/哪种 merge engine：① 用户行为埋点日志，只增不改；② CDC 同步订单表，要始终反映最新状态；③ 三个流分别更新一张用户宽表的不同字段。</p>",
        "<p>① Append 表（只追加）。② 主键表 + deduplicate（默认，保留最新）。③ 主键表 + partial-update（不同来源补全不同列）。</p>") + """

<div class="callout tip">
<span class="tag">本章目标</span>
<p>能根据场景选对表类型和 merge engine，理解 bucket / compaction / 快照保留对性能和成本的影响。到这里，你已经能独立用 Paimon 做实时湖仓了。后面三章是拓展：选型对比、排错、继续提升。</p>
</div>
"""

    return B
