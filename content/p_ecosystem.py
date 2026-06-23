# -*- coding: utf-8 -*-
"""第 14–17 章：生态全景 / Flink / Spark / Hive"""


def build(code, term, exercise):
    B = {}

    # ------------------------------------------------------------------ 第 14 章
    B["pages/14-ecosystem.html"] = """
<span class="eyebrow">第 14 章 · 生态与引擎</span>
<h1>生态全景：Paimon 在大数据栈里的位置</h1>
<p class="lead">学到这里，你已经会用 Flink + Paimon 做实时入湖了。但真实工作里，Paimon 从不孤军奋战——它和 Flink、Spark、Hive、StarRocks 等一起组成「湖仓栈」。这一章先用一张图把它们的分工讲清楚，后面几章再逐个动手。</p>

<div class="callout key">
<span class="tag">一句话先记住</span>
<p>Paimon 是<strong>存数据的「表格式」</strong>（管数据怎么存在湖上）；Flink/Spark/Hive 是<strong>算数据的「计算引擎」</strong>（读写、加工）；StarRocks 是<strong>查得快的「OLAP 引擎」</strong>（对外提供秒级查询）；WeData 是<strong>把这一切托管起来的「云平台」</strong>。它们是分层协作，不是互相替代。</p>
</div>

<h2>分层看：谁负责什么</h2>
<div class="flow">
<div class="node"><div class="nt">数据源</div><div class="nd">MySQL / Kafka / 日志</div></div>
<div class="arrow">↓ Flink CDC / Spark 写入</div>
<div class="node brand"><div class="nt">Apache Paimon（表格式 + 存储）</div><div class="nd">数据真正存放的地方：表、主键、快照、文件，落在 HDFS/对象存储上</div></div>
<div class="arrow">↑↓ 各引擎都来读写同一份数据</div>
<div class="node"><div class="nt">计算 / 查询引擎</div><div class="nd">Flink（流）· Spark（批）· Hive（数仓）· StarRocks（极速查询）</div></div>
</div>
<p>关键认知：<strong>同一张 Paimon 表，可以被多个引擎同时读写</strong>。Flink 实时写进去，Spark 跑批量加工，StarRocks 对外秒级查询，Hive 做兼容查询——大家共用一份数据，不用来回拷贝。这就是「湖仓一体」的价值。</p>

<h2>各组件定位速查</h2>
<div class="table-wrap">
<table>
<thead><tr><th>组件</th><th>它是什么</th><th>和 Paimon 的关系</th><th>典型用途</th></tr></thead>
<tbody>
<tr><td><strong>Flink</strong></td><td>流计算引擎</td><td>最佳拍档：实时写入 / 流式读取</td><td>CDC 入湖、实时宽表、流处理</td></tr>
<tr><td><strong>Spark</strong></td><td>批处理引擎</td><td>读写 Paimon 表</td><td>批量加工、历史回算、机器学习</td></tr>
<tr><td><strong>Hive</strong></td><td>老牌数仓 / SQL on Hadoop</td><td>通过 catalog 查询 Paimon 表</td><td>兼容存量数仓、离线查询</td></tr>
<tr><td><strong>StarRocks</strong></td><td>OLAP 极速查询引擎</td><td>外部 catalog 直查 Paimon</td><td>对外报表、即席查询、加速</td></tr>
<tr><td><strong>Iceberg</strong></td><td>另一种湖表格式（<em>竞品</em>）</td><td>同层替代关系，不是协作</td><td>对比选型时的参照物</td></tr>
<tr><td><strong>WeData</strong></td><td>腾讯云数据开发平台</td><td>托管运行上面这一整套</td><td>云上一站式开发、调度、运维</td></tr>
</tbody>
</table>
</div>

<div class="callout note">
<span class="tag">为什么要分清「层」</span>
<p>新手最容易混淆的是「Paimon 和 Flink 是不是二选一」。不是。Flink 是工具，Paimon 是工具加工/存放的「料」。真正和 Paimon 二选一的是 <strong>Iceberg / Hudi</strong> 这类同样是「表格式」的产品。把这点理清，后面就顺了。</p>
</div>

""" + exercise("练习 14-1", "<p>把下列组件归类到「表格式 / 计算引擎 / OLAP 查询 / 云平台」：Paimon、Flink、StarRocks、WeData、Spark、Iceberg。</p>",
        "<p>表格式：Paimon、Iceberg；计算引擎：Flink（流）、Spark（批）；OLAP 查询引擎：StarRocks；云平台：WeData。其中 Paimon 与 Iceberg 是同层竞品（二选一），其余是协作关系。</p>") + """

<div class="callout tip">
<span class="tag">本章目标</span>
<p>能说清 Paimon 与 Flink / Spark / Hive / StarRocks / Iceberg / WeData 各自的定位和关系，知道「谁和谁协作、谁和谁是竞品」。接下来四章逐个上手最常见的引擎集成。</p>
</div>
"""

    # ------------------------------------------------------------------ 第 15 章
    B["pages/15-flink.html"] = """
<span class="eyebrow">第 15 章 · 生态与引擎</span>
<h1>Flink + Paimon：最佳拍档</h1>
<p class="lead">Paimon 的前身就是 Flink Table Store，二者天生一对。前面第 8、9 章其实已经用 Flink 写过 Paimon 了，这一章系统梳理 Flink 怎么读写 Paimon，并补上「流式读取」「时间旅行」这些 Flink 专属玩法。</p>

<div class="callout note">
<span class="tag">前置</span>
<p>本章沿用第 7 章搭好的 Flink + Paimon 环境（<code>$FLINK_HOME/lib/</code> 里有 paimon-flink jar），命令都在 Flink SQL Client 里执行。</p>
</div>

<h2>1. 建 Catalog（回顾）</h2>
""" + code("sql", "Flink SQL Client", """CREATE CATALOG paimon WITH (
    'type' = 'paimon',
    'warehouse' = 'file:/tmp/paimon'
);
USE CATALOG paimon;""") + """

<h2>2. 批写 vs 流写</h2>
<p>Flink 对 Paimon 的写入分两种模式，区别只在 <code>runtime-mode</code>：</p>
""" + code("sql", "批量写入（一次性灌数据）", """SET 'execution.runtime-mode' = 'batch';

CREATE TABLE IF NOT EXISTS dim_city (
    city_id INT PRIMARY KEY NOT ENFORCED,
    name    STRING
);
INSERT INTO dim_city VALUES (1,'北京'),(2,'上海'),(3,'深圳');""") + code("sql", "流式写入（持续不断）", """SET 'execution.runtime-mode' = 'streaming';
SET 'execution.checkpointing.interval' = '10 s';   -- 流写必须设

INSERT INTO dim_city
SELECT city_id, name FROM some_streaming_source;""") + """
""" + term("checkpoint", "检查点", "Flink 周期性给作业状态做的「存档」。Paimon 在每个 checkpoint 提交一次写入并生成 snapshot——所以流写一定要设 checkpoint，否则数据提交不了、查不到。") + """

<h2>3. 流式读取：Paimon 当成「带历史的 Kafka」</h2>
<p>Flink 读 Paimon 最强大的能力是<strong>流式读取</strong>：不仅能读到当前快照，还能持续读出后续的<em>变更</em>（增删改）。</p>
""" + code("sql", "流式读取一张主键表的变化", """SET 'execution.runtime-mode' = 'streaming';

-- 从最新快照开始，持续输出后续变更
SELECT * FROM dim_city /*+ OPTIONS('scan.mode'='latest') */;""") + """
<div class="callout key">
<span class="tag">为什么这很重要</span>
<p>这意味着 Paimon 表可以像消息队列一样被「订阅」：上游实时写入 Paimon，下游 Flink 作业流式读取做二次加工，形成<strong>实时数仓的分层（ODS→DWD→DWS）</strong>，而中间不再需要额外的 Kafka。</p>
</div>

<h2>4. 时间旅行：读历史版本</h2>
""" + code("sql", "按快照 / 时间点查询", """SET 'execution.runtime-mode' = 'batch';

-- 看有哪些快照
SELECT snapshot_id, commit_time FROM dim_city$snapshots;

-- 读第 3 个快照时的数据
SELECT * FROM dim_city /*+ OPTIONS('scan.snapshot-id'='3') */;

-- 或按时间点读（毫秒时间戳）
SELECT * FROM dim_city /*+ OPTIONS('scan.timestamp-millis'='1718000000000') */;""") + """

<h2>5. 常见报错</h2>
<div class="table-wrap">
<table>
<thead><tr><th>报错 / 现象</th><th>原因</th><th>解决</th></tr></thead>
<tbody>
<tr><td>ClassNotFound / Catalog 创建失败</td><td>paimon-flink jar 没放进 lib</td><td>把对应 Flink 版本的 paimon-flink-*.jar 放入 <code>$FLINK_HOME/lib/</code> 并重启集群</td></tr>
<tr><td>流写后查不到数据</td><td>没设 checkpoint</td><td><code>SET 'execution.checkpointing.interval'='10 s'</code></td></tr>
<tr><td>流读没有输出</td><td>表没有新变更 / scan.mode 不对</td><td>确认上游在写入，或用 <code>scan.mode='latest-full'</code> 先读全量再读增量</td></tr>
</tbody>
</table>
</div>

""" + exercise("练习 15-1", "<p>你想让下游 Flink 作业「订阅」一张 Paimon 主键表，只处理新发生的增删改，应该用什么读取方式？这相比传统「Paimon 之上再接一个 Kafka」有什么好处？</p>",
        "<p>用流式读取（streaming 模式 + <code>scan.mode='latest'</code> 之类）订阅变更。好处：省掉了中间的 Kafka，数据只存一份在 Paimon 里，既能批查又能被流式订阅，降低了架构复杂度和存储成本。</p>") + """

<div class="callout tip">
<span class="tag">本章目标</span>
<p>掌握 Flink 对 Paimon 的批写/流写、流式读取、时间旅行，理解「Paimon 可被流式订阅」对实时数仓分层的意义。下一章换 Spark，体会同一份数据被批引擎读写。</p>
</div>
"""

    # ------------------------------------------------------------------ 第 16 章
    B["pages/16-spark.html"] = """
<span class="eyebrow">第 16 章 · 生态与引擎</span>
<h1>Spark + Paimon：批处理读写</h1>
<p class="lead">Flink 擅长「流」，Spark 擅长「批」。同一张 Paimon 表，Flink 实时写、Spark 批量读来做加工/回算/训练，是非常常见的搭配。这一章用 Spark SQL 读写 Paimon。</p>

<h2>1. 启动带 Paimon 的 Spark SQL</h2>
<p>用 <code>--packages</code> 自动拉取 Paimon 的 Spark 包，并配好 catalog：</p>
""" + code("bash", "启动 spark-sql（注意换成你的 Spark 版本对应的包）", """spark-sql \\
  --packages org.apache.paimon:paimon-spark-3.5:1.0.0 \\
  --conf spark.sql.catalog.paimon=org.apache.paimon.spark.SparkCatalog \\
  --conf spark.sql.catalog.paimon.warehouse=file:/tmp/paimon \\
  --conf spark.sql.extensions=org.apache.paimon.spark.extensions.PaimonSparkSessionExtensions""") + """
<div class="callout warn">
<span class="tag">版本要对应</span>
<p>包名里的 <code>paimon-spark-3.5</code> 要和你的 Spark 大版本一致（Spark 3.3/3.4/3.5 各有对应包），版本错配是最常见的启动失败原因。</p>
</div>

<h2>2. 切换 catalog 并建表</h2>
""" + code("sql", "spark-sql>", """-- 使用上面配置的 paimon catalog
USE paimon;

CREATE TABLE IF NOT EXISTS sales (
    id     BIGINT,
    item   STRING,
    amount DOUBLE
) TBLPROPERTIES (
    'primary-key' = 'id'
);""") + """
""" + term("TBLPROPERTIES", "表属性", "Spark 建表时通过它设置 Paimon 表的属性，比如主键 primary-key、桶数 bucket、合并引擎 merge-engine 等，作用等价于 Flink 建表里的 WITH(...)。") + """

<h2>3. 批量写入与查询</h2>
""" + code("sql", "写入 + 查询", """-- 批量插入
INSERT INTO sales VALUES (1,'apple',9.9),(2,'banana',3.5);

-- 同主键再插一条，会 upsert（更新）
INSERT INTO sales VALUES (1,'apple',12.0);

-- 查询：id=1 的 amount 已变成 12.0
SELECT * FROM sales ORDER BY id;""") + """
<p>注意：因为建表时设了 <code>primary-key='id'</code>，Spark 写入同主键时也会触发 Paimon 的 upsert 合并——和 Flink 写入时的语义一致，因为合并逻辑在 Paimon 这一层，与引擎无关。</p>

<h2>4. 时间旅行（Spark 语法）</h2>
""" + code("sql", "按版本 / 时间查历史", """-- 按快照版本号
SELECT * FROM sales VERSION AS OF 1;

-- 按时间点
SELECT * FROM sales TIMESTAMP AS OF '2026-06-23 10:00:00';""") + """

<h2>5. 用 Spark 做 compaction / 维护</h2>
<p>Paimon 也提供了 Spark 端的存储过程（procedure）来做小文件合并等维护：</p>
""" + code("sql", "调用 compact 存储过程", """CALL paimon.sys.compact(table => 'paimon.default.sales');""") + """

<div class="callout key">
<span class="tag">体会一下</span>
<p>同一张 <code>sales</code> 表，Flink 能写、Spark 也能写和查，时间旅行两边都支持——因为「主键合并、快照、文件布局」这些规则都由 Paimon 统一管理，<strong>引擎只是访问者</strong>。这正是表格式存在的意义。</p>
</div>

""" + exercise("练习 16-1", "<p>Flink 已经把 MySQL 的 orders 实时写进了 Paimon。现在数据团队想用 Spark 跑一个「最近 30 天按城市汇总」的离线报表。他们需要 Flink 停止写入吗？为什么？</p>",
        "<p>不需要。Paimon 表支持多引擎并发读写，Spark 读取的是某个一致的快照，Flink 可以继续实时写入。Spark 读到的是它发起查询那一刻的快照数据，互不影响。</p>") + """

<div class="callout tip">
<span class="tag">本章目标</span>
<p>能用 Spark SQL 配好 Paimon catalog、读写主键表、做时间旅行和 compaction，并理解「同一份数据流批引擎共享」。下一章看老牌的 Hive 怎么查 Paimon。</p>
</div>
"""

    # ------------------------------------------------------------------ 第 17 章
    B["pages/17-hive.html"] = """
<span class="eyebrow">第 17 章 · 生态与引擎</span>
<h1>Hive + Paimon：对接存量数仓</h1>
<p class="lead">很多公司有大量存量的 Hive 数仓和 Hive Metastore（HMS）。Paimon 可以把表注册进 Hive Metastore，让 Hive、以及所有「认 HMS」的引擎都能查到这些表，平滑融入既有体系。</p>

<h2>两件事别混淆</h2>
""" + term("Hive Metastore（HMS）", "Hive 元数据服务", "一个集中存放「库、表、字段、分区」等元数据的服务。它本身不算数，只记录「有哪些表、表在哪、什么结构」。很多引擎（Hive/Spark/Flink/Trino）都靠它来发现表。") + term(
        "Hive Catalog（Paimon 的）", "Hive 目录", "Paimon 的一种 catalog 类型，把 Paimon 表的元数据登记到 HMS。这样不需要单独维护 Paimon 的元数据，存量体系就能发现这些表。") + """

<h2>1. 用 Hive Metastore 作为 Paimon Catalog</h2>
<p>在 Flink（或 Spark）里建 catalog 时，指定 <code>metastore=hive</code>，Paimon 就会把表登记到 HMS：</p>
""" + code("sql", "Flink SQL：基于 HMS 的 Paimon catalog", """CREATE CATALOG paimon_hive WITH (
    'type' = 'paimon',
    'metastore' = 'hive',
    'uri' = 'thrift://localhost:9083',     -- Hive Metastore 地址
    'warehouse' = 'hdfs:///warehouse/paimon'
);
USE CATALOG paimon_hive;

CREATE TABLE user_log (
    id   BIGINT PRIMARY KEY NOT ENFORCED,
    name STRING
);""") + """
<p>建完后，这张 <code>user_log</code> 不仅是 Paimon 表，元数据也进了 HMS——Hive 端能「看见」它。</p>

<h2>2. 在 Hive 里查询 Paimon 表</h2>
<p>Hive 端需要加载 Paimon 的 Hive 连接 jar，然后就能像查普通表一样查：</p>
""" + code("sql", "Hive CLI / Beeline", """-- 加载 Paimon 的 Hive connector（路径换成你的 jar）
ADD JAR /opt/paimon/paimon-hive-connector.jar;

-- 直接查询上一步建的表
SELECT * FROM user_log LIMIT 10;""") + """
<div class="callout warn">
<span class="tag">版本与 jar</span>
<p>Hive 集成对版本较敏感：要用与你的 Hive 版本匹配的 paimon-hive-connector jar，并确保 HMS 可访问。版本不匹配会出现找不到 SerDe / InputFormat 之类的错误。</p>
</div>

<h2>3. 这样做的价值</h2>
<div class="flow">
<div class="node brand"><div class="nt">Paimon 表</div><div class="nd">登记到 HMS</div></div>
<div class="arrow">↓ 共享同一份元数据</div>
<div class="node"><div class="nt">Hive · Spark · Trino · StarRocks</div><div class="nd">都能发现并查询同一张表</div></div>
</div>
<p>对存量数仓团队来说，意义是：<strong>不用推倒重来</strong>。新建的实时表用 Paimon，登记进熟悉的 HMS，老的查询工具链照样能用，迁移成本最低。</p>

""" + exercise("练习 17-1", "<p>用一句话解释：为什么把 Paimon 表登记到 Hive Metastore，能让「不是 Hive 的引擎」（比如 Spark、StarRocks）也查到这张表？</p>",
        "<p>因为 Spark、StarRocks 等引擎也支持把 Hive Metastore 作为元数据来源。HMS 是一个被广泛共享的「表目录」，只要表登记在里面，所有认 HMS 的引擎都能发现并查询它，而不只是 Hive 自己。</p>") + """

<div class="callout tip">
<span class="tag">本章目标</span>
<p>理解 Hive Metastore 的角色，会用 <code>metastore=hive</code> 把 Paimon 表登记进 HMS，并在 Hive 端查询，明白这对融合存量数仓的价值。下一章上 StarRocks，体验对 Paimon 的极速查询。</p>
</div>
"""

    return B
