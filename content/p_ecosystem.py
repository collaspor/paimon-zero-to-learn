# -*- coding: utf-8 -*-
"""第 14–17 章：生态全景 / Flink / Spark / Hive（大白话版）"""


def build(code, term, exercise):
    B = {}

    # ------------------------------------------------------------------ 第 14 章
    B["pages/14-ecosystem.html"] = """
<span class="eyebrow">第 14 章 · 生态与引擎</span>
<h1>生态全景：Paimon 身边都有谁</h1>
<p class="lead">学到这儿，你已经能用 Flink + Paimon 把数据实时写进湖里了。但你可能也犯嘀咕：网上一会儿说 Flink，一会儿说 Spark、Hive、StarRocks，还冒出来个 Iceberg、WeData——<strong>这些东西到底跟 Paimon 是啥关系？哪个能替代哪个？我都得学吗？</strong>这一章就把这团乱麻一次性理清楚，用大白话，不堆术语。</p>

<div class="callout key">
<span class="tag">先打个比方，记住这个就够了</span>
<p>把整套大数据系统想象成<strong>一家餐厅</strong>：</p>
<ul>
<li><strong>Paimon = 冰箱 / 仓库</strong>。负责把食材（数据）<em>存好、放整齐、随时能取</em>。它不做菜，只管存。</li>
<li><strong>Flink / Spark / Hive = 厨师</strong>。负责<em>从仓库取料、加工、再放回去</em>。它们是干活的人，但东西不是它们存的。</li>
<li><strong>StarRocks = 前台传菜的飞毛腿</strong>。客人（报表、看板）一点单，它<em>飞快地从仓库取好端出去</em>，主打一个"快"。</li>
<li><strong>WeData = 整个餐厅的"店长 + 中央厨房系统"</strong>。帮你把上面这些人和设备<em>统一管起来</em>，你不用自己招厨师、修冰箱。</li>
<li><strong>Iceberg = 另一个牌子的冰箱</strong>。和 Paimon 干一样的活（存料），所以你<em>二选一</em>就行，不会两个冰箱一起买。</li>
</ul>
<p>所以核心就一句话：<strong>Paimon 管存，引擎管算，StarRocks 管快查，WeData 管托管，Iceberg 是 Paimon 的同行竞品。</strong>它们大多是"搭伙干活"，不是"你死我活"。</p>
</div>

<h2>为什么会有这么多东西？</h2>
<p>因为一件事被拆成了好几个专业岗位。你想想：数据从产生到被人看到报表，中间要经过——</p>
<ol>
<li><strong>有人把数据搬进来</strong>（比如把 MySQL 里的订单实时同步过来）；</li>
<li><strong>有个地方把数据存住</strong>（存得整齐、能更新、能查历史）；</li>
<li><strong>有人对数据做加工</strong>（算汇总、做宽表、清洗）；</li>
<li><strong>有人负责让老板秒查到结果</strong>（点开看板唰一下就出来）。</li>
</ol>
<p>一个工具想把这四件事全干好，太难了。所以大数据世界选择了<strong>分工</strong>：每个工具专精一件事，再拼到一起。Paimon 专精第 2 件（存），其它工具专精别的。理解了"分工"，你就理解了整个生态。</p>

<h2>分层看：数据是怎么流动的</h2>
<p>下面这张图，从上往下就是数据流动的方向。你不用记名字，先感受"料 → 存 → 算/查"这个走向：</p>
<div class="flow">
<div class="node"><div class="nt">① 数据源（原料产地）</div><div class="nd">MySQL 数据库、Kafka 消息、各种日志</div></div>
<div class="arrow">↓ 厨师（Flink / Spark）把料搬进仓库</div>
<div class="node brand"><div class="nt">② Apache Paimon（仓库 / 冰箱）</div><div class="nd">数据真正存放的地方：表、主键、快照、文件，落在 HDFS 或对象存储上</div></div>
<div class="arrow">↑↓ 谁要用数据，都来这个仓库取，存的只有一份</div>
<div class="node"><div class="nt">③ 计算 / 查询引擎（厨师 + 传菜员）</div><div class="nd">Flink 管实时 · Spark 管批量 · Hive 管老数仓 · StarRocks 管秒级快查</div></div>
</div>
<p>这里有个特别重要、新手常常想不到的点：<strong>同一份数据，可以被好几个工具同时用，不用拷来拷去。</strong>Flink 在往里写，Spark 同时在读它跑报表，StarRocks 同时在对外提供查询——大家围着<em>同一个冰箱</em>转。这就是大家常说的"湖仓一体"，省钱省事的关键就在这"一份数据多人用"上。</p>

<h2>一张表认清所有人</h2>
<p>把上面的话浓缩成一张速查表，以后忘了回来看这张就行：</p>
<div class="table-wrap">
<table>
<thead><tr><th>组件</th><th>大白话角色</th><th>和 Paimon 啥关系</th><th>啥时候用它</th></tr></thead>
<tbody>
<tr><td><strong>Flink</strong></td><td>实时干活的厨师</td><td>最佳拍档：实时往里写、能订阅变化</td><td>数据要"实时"进湖、做流处理</td></tr>
<tr><td><strong>Spark</strong></td><td>批量干活的厨师</td><td>一起干活：批量读写 Paimon</td><td>跑大批量加工、算历史、做机器学习</td></tr>
<tr><td><strong>Hive</strong></td><td>老资格的数仓厨师</td><td>一起干活：能查 Paimon 表</td><td>公司有老的 Hive 数仓，想平滑接上</td></tr>
<tr><td><strong>StarRocks</strong></td><td>飞毛腿传菜员</td><td>一起干活：直接快查 Paimon</td><td>要对外做秒级报表、即席查询</td></tr>
<tr><td><strong>Iceberg</strong></td><td>另一个牌子的冰箱（<em>竞品</em>）</td><td>二选一，不是搭伙</td><td>选型时拿来和 Paimon 比一比</td></tr>
<tr><td><strong>WeData</strong></td><td>店长 + 中央厨房系统</td><td>把上面整套托管起来</td><td>不想自己搭运维、想云上一站式搞定</td></tr>
</tbody>
</table>
</div>

<div class="callout warn">
<span class="tag">最容易踩的认知坑</span>
<p>很多新手第一反应是问"<strong>Paimon 和 Flink 是不是二选一？</strong>"——<strong>不是！</strong>这就好比问"冰箱和厨师二选一吗"，显然两个都得有，它们是搭配的。真正和 Paimon 二选一的，是 <strong>Iceberg、Hudi</strong> 这种"同样负责存"的另一个冰箱。把这一点想通，后面四章你就不会再绕晕。</p>
</div>

""" + exercise("练习 14-1", "<p>用刚才“餐厅”的比方，说说下面每个组件相当于餐厅里的什么角色，并指出谁和谁是“二选一”：Paimon、Flink、StarRocks、WeData、Spark、Iceberg。</p>",
        "<p>Paimon = 冰箱/仓库（管存）；Flink = 实时厨师、Spark = 批量厨师、Hive = 老数仓厨师（都管算）；StarRocks = 飞毛腿传菜员（管快查）；WeData = 店长/中央厨房（管托管）；Iceberg = 另一个牌子的冰箱。<strong>二选一的只有 Paimon 和 Iceberg</strong>（都是冰箱，买一个就行），其余都是搭伙干活的关系。</p>") + """

<div class="callout tip">
<span class="tag">这一章你要带走的</span>
<p>不用记任何命令。只要能用"餐厅分工"讲清楚：谁负责<strong>存</strong>、谁负责<strong>算</strong>、谁负责<strong>快查</strong>、谁负责<strong>托管</strong>，以及谁和谁是<strong>竞品</strong>。记住了，咱们下一章就请第一位厨师 Flink 上场，实际动手。</p>
</div>
"""

    # ------------------------------------------------------------------ 第 15 章
    B["pages/15-flink.html"] = """
<span class="eyebrow">第 15 章 · 生态与引擎</span>
<h1>Flink + Paimon：天生一对的"实时厨师"</h1>
<p class="lead">为什么把 Flink 放第一个讲？因为 <strong>Paimon 的"前身"就是 Flink 团队做的</strong>（以前叫 Flink Table Store），可以说 Paimon 是 Flink 亲手带大的孩子，俩人配合最默契。其实你在第 8、9 章已经用 Flink 写过 Paimon 了，这一章咱们把它俩的配合"系统地"再走一遍，并解锁两个 Flink 才有的拿手好戏：<strong>"订阅数据变化"</strong>和<strong>"穿越回看历史"</strong>。</p>

<div class="callout note">
<span class="tag">动手前提</span>
<p>这一章接着用第 7 章搭好的 Flink + Paimon 环境（也就是 <code>$FLINK_HOME/lib/</code> 里已经放了 paimon-flink 的 jar 包）。下面的命令都在 <strong>Flink SQL Client</strong> 里敲——就是那个能写 SQL 的交互窗口。</p>
</div>

<h2>第一步：先告诉 Flink "仓库在哪"</h2>
<p>厨师上岗第一件事，是知道"冰箱在哪个房间"。在 Flink 里，这一步叫"建 Catalog"——你可以把 Catalog 理解成<strong>一张写着仓库地址的门牌</strong>。建好之后，Flink 就知道去哪儿找 Paimon 的表了。</p>
""" + code("sql", "在 Flink SQL Client 里执行", """CREATE CATALOG paimon WITH (
    'type' = 'paimon',
    'warehouse' = 'file:/tmp/paimon'   -- 仓库地址，这里用本地目录演示
);

USE CATALOG paimon;   -- 切进这个仓库，之后建表查表都在这里面""") + """
<p>执行完，Flink 就"认门"了。后面所有的建表、写入、查询，都是在这个 Paimon 仓库里进行。</p>

<h2>第二步：往里写数据，有"批"和"流"两种姿势</h2>
<p>同样是往冰箱里放东西，有两种节奏：</p>
<ul>
<li><strong>批量写（batch）</strong>：像<em>一次性把一周的菜买回来塞满冰箱</em>。数据是固定的一批，写完就结束。</li>
<li><strong>流式写（streaming）</strong>：像<em>家里装了个自动补货机，源源不断地往里送</em>。数据持续不停地流进来，作业一直运行。</li>
</ul>
<p>在 Flink 里切换这两种姿势，只差一个开关 <code>runtime-mode</code>：</p>
""" + code("sql", "姿势一：批量写（一次性灌一批数据）", """SET 'execution.runtime-mode' = 'batch';

CREATE TABLE IF NOT EXISTS dim_city (
    city_id INT PRIMARY KEY NOT ENFORCED,
    name    STRING
);
INSERT INTO dim_city VALUES (1,'北京'),(2,'上海'),(3,'深圳');""") + code("sql", "姿势二：流式写（持续不停地往里送）", """SET 'execution.runtime-mode' = 'streaming';
SET 'execution.checkpointing.interval' = '10 s';   -- 流式写必须开这个，原因下面解释

INSERT INTO dim_city
SELECT city_id, name FROM some_streaming_source;   -- 数据从上游源源不断地来""") + """

<h3>插一句：checkpoint 是啥？为啥流式写非开不可？</h3>
<p>打个比方：你在写一篇很长的文档，<strong>checkpoint 就是"自动保存"</strong>。Flink 每隔一段时间（比如 10 秒）就把当前进度存一次档。</p>
<p>关键在于：<strong>Paimon 是在每次"自动保存"的那一刻，才真正把数据提交、生成一个新快照的。</strong>如果你不开自动保存（不设 checkpoint），数据就一直飘在内存里"没落地"，结果就是——<em>你流式写了半天，去查却什么都查不到</em>。这是新手最常见的坑之一，记牢：<strong>流式写，必开 checkpoint。</strong></p>
""" + term("checkpoint", "检查点 / 自动存档", "Flink 周期性地给作业进度做的“存档”。Paimon 在每个 checkpoint 提交一次写入、生成一个 snapshot（快照）。所以流式写不开 checkpoint，数据就提交不了、也就查不到。") + """

<h2>第三步：Flink 的拿手好戏——"订阅"数据的变化</h2>
<p>这是 Flink 读 Paimon 最酷的能力，叫<strong>流式读取</strong>。普通读取是"拍张照看现在长啥样"；流式读取是<strong>"盯着这张表，谁一改我立刻知道"</strong>——新增、修改、删除，它都能持续地读出来。</p>
<p>打个最贴切的比方：你可以把一张 Paimon 表当成<strong>能回放历史的"群聊"</strong>。你不仅能看到当前的聊天记录，还能"潜水盯着"，谁发新消息你马上收到。</p>
""" + code("sql", "流式订阅一张表的所有变化", """SET 'execution.runtime-mode' = 'streaming';

-- 从最新快照开始，之后这张表谁一变，这里就持续吐出来
SELECT * FROM dim_city /*+ OPTIONS('scan.mode'='latest') */;""") + """
<div class="callout key">
<span class="tag">为什么这事很了不起</span>
<p>因为它意味着 <strong>Paimon 表能当"消息队列"用，省掉一个 Kafka</strong>。传统做法是：数据先进 Kafka 给下游订阅，再落一份到湖里存储——同一份数据存了两遍。有了 Paimon 流式读，<em>数据只在 Paimon 存一份，既能当仓库批量查，又能被下游像订阅消息一样实时消费</em>。这就是实时数仓里 ODS→DWD→DWS 一层层往下加工的底气，架构更简单、更省钱。</p>
</div>

<h2>第四步：另一个好戏——"穿越"回看历史版本</h2>
<p>这叫<strong>时间旅行</strong>。因为 Paimon 每次提交都会留一个"快照"（就像游戏存档），所以你能随时<em>读回某个历史时刻的数据长啥样</em>。误删了？算错了想对比？穿越回去看一眼就行。</p>
""" + code("sql", "回看历史：按快照编号 或 按时间点", """SET 'execution.runtime-mode' = 'batch';

-- 先看看这张表有哪些存档（快照）
SELECT snapshot_id, commit_time FROM dim_city$snapshots;

-- 读"第 3 个存档"那一刻的数据
SELECT * FROM dim_city /*+ OPTIONS('scan.snapshot-id'='3') */;

-- 或者按某个时间点读（填毫秒时间戳）
SELECT * FROM dim_city /*+ OPTIONS('scan.timestamp-millis'='1718000000000') */;""") + """
<p>是不是很像给数据装了个"后悔药 + 监控录像"？这在排查问题、做数据审计时特别有用。</p>

<h2>遇到问题别慌：常见报错对照</h2>
<p>动手时八成会撞上下面几个，提前知道就不慌：</p>
<div class="table-wrap">
<table>
<thead><tr><th>你看到的现象</th><th>大白话原因</th><th>怎么解决</th></tr></thead>
<tbody>
<tr><td>建 Catalog 报 ClassNotFound</td><td>厨师没带工具——jar 包没放对</td><td>把对应 Flink 版本的 paimon-flink-*.jar 放进 <code>$FLINK_HOME/lib/</code>，<strong>重启集群</strong></td></tr>
<tr><td>流式写了半天，查不到数据</td><td>没开"自动存档"，数据没落地</td><td>加上 <code>SET 'execution.checkpointing.interval'='10 s'</code></td></tr>
<tr><td>流式读没反应、不吐数据</td><td>表压根没新变化，或读取模式不对</td><td>确认上游真的在写；或改用 <code>scan.mode='latest-full'</code> 先读全量再追增量</td></tr>
</tbody>
</table>
</div>

""" + exercise("练习 15-1", "<p>你想让下游一个 Flink 作业“盯着”一张 Paimon 主键表，只处理新发生的增删改。① 该用哪种读取方式？② 比起“在 Paimon 旁边再架一个 Kafka 让大家订阅”，这么做好在哪？</p>",
        "<p>① 用流式读取（streaming 模式 + <code>scan.mode='latest'</code> 之类），把表当消息流“订阅”。② 好处：省掉中间那个 Kafka，数据只在 Paimon 存一份，既能批量查又能被实时订阅，架构更简单、存储成本更低、也少了一处可能出故障的环节。</p>") + """

<div class="callout tip">
<span class="tag">这一章你要带走的</span>
<p>会用 Flink 对 Paimon 做批写/流写、会"订阅变化"（流式读）、会"穿越看历史"（时间旅行），并且记住<strong>流式写必开 checkpoint</strong>。下一章换批量厨师 Spark 上场，你会亲眼看到——<em>同一个冰箱，换个厨师照样能用</em>。</p>
</div>
"""

    # ------------------------------------------------------------------ 第 16 章
    B["pages/16-spark.html"] = """
<span class="eyebrow">第 16 章 · 生态与引擎</span>
<h1>Spark + Paimon：批量干活的厨师</h1>
<p class="lead">上一章的 Flink 擅长"实时"，像个手脚麻利、随叫随到的快手厨师。这一章的 <strong>Spark 擅长"批量"</strong>，像个一次处理一大锅的大厨：跑历史数据回算、做大批量加工、训练机器学习模型，都是它的活。重点来了——<strong>它俩用的是同一个冰箱（同一张 Paimon 表）</strong>。Flink 实时往里写，Spark 随时来批量读、加工，这是真实项目里超常见的搭配。</p>

<h2>第一步：把 Spark 和 Paimon "接上头"</h2>
<p>Spark 默认不认识 Paimon，得给它"装个插件"。最省事的办法是启动时用 <code>--packages</code> 让它自动联网下载 Paimon 的包，并顺手配好"仓库门牌"（catalog）：</p>
""" + code("bash", "启动 spark-sql（把版本号换成你自己的 Spark 版本）", """spark-sql \\
  --packages org.apache.paimon:paimon-spark-3.5:1.0.0 \\
  --conf spark.sql.catalog.paimon=org.apache.paimon.spark.SparkCatalog \\
  --conf spark.sql.catalog.paimon.warehouse=file:/tmp/paimon \\
  --conf spark.sql.extensions=org.apache.paimon.spark.extensions.PaimonSparkSessionExtensions""") + """
<div class="callout warn">
<span class="tag">最常见的翻车点：版本要对上</span>
<p>命令里的 <code>paimon-spark-3.5</code>，那个 <code>3.5</code> 必须和你的 Spark 大版本一模一样（你用 Spark 3.3 就写 3.3，用 3.4 就写 3.4）。<strong>版本对不上是启动失败最常见的原因</strong>，报错往往看着吓人，其实就是号没对上。先检查这个。</p>
</div>

<h2>第二步：进仓库、建张表</h2>
<p>接上头之后，先"走进"刚才配好的 paimon 仓库，再建一张带主键的表：</p>
""" + code("sql", "在 spark-sql 提示符里执行", """-- 走进上面配好的 paimon 仓库
USE paimon;

CREATE TABLE IF NOT EXISTS sales (
    id     BIGINT,
    item   STRING,
    amount DOUBLE
) TBLPROPERTIES (
    'primary-key' = 'id'    -- 指定主键，写同一个 id 会自动"更新"而不是堆两条
);""") + """
<p>注意那个 <code>TBLPROPERTIES</code>，它就是 Spark 给 Paimon 表"设参数"的地方。在 Flink 里你是写在 <code>WITH(...)</code> 里，在 Spark 里换成了 <code>TBLPROPERTIES(...)</code>，<strong>名字不同、干的是同一件事</strong>——告诉 Paimon 这张表的主键、桶数、合并方式等。</p>
""" + term("TBLPROPERTIES", "表属性", "Spark 建表时设置 Paimon 表属性的地方，比如主键 primary-key、桶数 bucket、合并引擎 merge-engine。作用等同于 Flink 建表里的 WITH(...)，只是换了个写法。") + """

<h2>第三步：写数据，亲眼看"主键更新"是咋回事</h2>
<p>下面这段最值得你亲手跑一遍——它能让你直观感受 Paimon 的"主键 upsert"：<strong>同一个 id 写两次，不会变成两条，而是后面的把前面的覆盖掉。</strong></p>
""" + code("sql", "写入 → 再写同一个 id → 查询看结果", """-- 先插两条
INSERT INTO sales VALUES (1,'apple',9.9),(2,'banana',3.5);

-- 再插一条 id=1 的，注意金额变了
INSERT INTO sales VALUES (1,'apple',12.0);

-- 查一下：id=1 的 amount 不是 9.9，而是被更新成了 12.0
SELECT * FROM sales ORDER BY id;""") + """
<p>看到没？id=1 只剩一条、金额是最新的 12.0。这就是"主键自动更新"。<strong>更妙的是</strong>：这个"同 id 自动更新"的规则，无论你用 Flink 写还是 Spark 写，效果完全一样——因为<em>这套规则是冰箱（Paimon）自己定的，跟哪个厨师来操作没关系</em>。</p>

<h2>第四步：Spark 也能"穿越看历史"</h2>
<p>时间旅行 Flink 有、Spark 也有，只是 SQL 写法是 Spark 自己的味道：</p>
""" + code("sql", "回看历史版本", """-- 按存档编号看
SELECT * FROM sales VERSION AS OF 1;

-- 按时间点看
SELECT * FROM sales TIMESTAMP AS OF '2026-06-23 10:00:00';""") + """

<h2>第五步：用 Spark 帮冰箱"整理整理"（compaction）</h2>
<p>数据写多了，冰箱里会攒一堆零碎小文件，查起来变慢。Paimon 提供了让 Spark 来"整理合并"的小工具（叫存储过程 procedure），一行命令就能触发：</p>
""" + code("sql", "手动触发小文件合并", """CALL paimon.sys.compact(table => 'paimon.default.sales');""") + """
<p>这相当于让大厨顺手把冰箱里散落的小盒子归并成大盒子，下次取用更利索。（compaction 的来龙去脉在第 10 章讲过，忘了可以翻回去。）</p>

<div class="callout key">
<span class="tag">这一章最想让你"体会"到的</span>
<p>同一张 <code>sales</code> 表——Flink 能写，Spark 也能写、能查，时间旅行两边都支持。<strong>为什么这么神奇？因为"主键怎么合并、快照怎么存、文件怎么布局"这些规矩，全是冰箱 Paimon 自己管的，厨师（引擎）只是来取放东西的"访客"。</strong>这正是"表格式"这种东西存在的最大意义：让不同引擎和平共处、共享一份数据。</p>
</div>

""" + exercise("练习 16-1", "<p>Flink 已经把 MySQL 的 orders 实时写进了 Paimon。现在数据团队想用 Spark 跑一个“最近 30 天按城市汇总”的离线报表。问：他们需要先让 Flink 停止写入吗？为什么？</p>",
        "<p>不需要停。Paimon 支持多个引擎同时读写：Spark 读到的是它发起查询那一刻的某个一致快照，而 Flink 可以继续往里实时写新数据，两边互不打架。这正是“一份数据多人用”的好处。</p>") + """

<div class="callout tip">
<span class="tag">这一章你要带走的</span>
<p>会给 Spark 接上 Paimon、读写主键表、亲眼验证"同 id 自动更新"、做时间旅行和小文件合并，并真切体会到"<strong>流批两种厨师共享同一个冰箱</strong>"。下一章请出公司里最常见的"老资格"——Hive，看它怎么跟 Paimon 接轨。</p>
</div>
"""

    # ------------------------------------------------------------------ 第 17 章
    B["pages/17-hive.html"] = """
<span class="eyebrow">第 17 章 · 生态与引擎</span>
<h1>Hive + Paimon：让老数仓平滑接上新表</h1>
<p class="lead">现实情况是：很多公司已经用 Hive 搭了好多年的数据仓库，里面有成百上千张老表，大家都习惯了。这时候你引入 Paimon，老板肯定会问：<strong>"能不能别推倒重来？让老工具也能查到新表？"</strong>这一章就解决这个问题——靠的是一个叫 <strong>Hive Metastore</strong> 的关键角色。</p>

<h2>先搞懂一个角色：Hive Metastore 到底是干嘛的</h2>
<p>这个名字听着唬人，其实特别好懂。打个比方：</p>
<div class="callout key">
<span class="tag">把它想成公司的"通讯录 / 资产登记册"</span>
<p><strong>Hive Metastore（简称 HMS）就是一本登记册</strong>，上面记着："公司有哪些表、每张表叫啥名、有哪些字段、数据存在哪个位置"。它<em>本身不存数据、也不算数据</em>，只负责<strong>记账</strong>——告诉大家"有哪些表、表在哪儿"。</p>
<p>妙的地方在于：<strong>好多工具都认这本登记册</strong>（Hive、Spark、Flink、Trino、StarRocks……）。只要你把一张表登记进去，所有认这本册子的工具，翻开就能查到它。</p>
</div>
""" + term("Hive Metastore（HMS）", "Hive 元数据服务 / 登记册", "一个集中记录“有哪些库、哪些表、什么字段、数据在哪”的服务。它不存数据本身，只管登记。很多引擎（Hive/Spark/Flink/Trino/StarRocks）都靠查它来发现表。") + term(
        "Hive Catalog（Paimon 的一种）", "登记到 Hive 册子的方式", "Paimon 的一种 catalog 类型。选了它，Paimon 建表时就顺手把这张表登记进 HMS 那本册子，于是老的 Hive 体系立刻就能“看见”这张新表。") + """

<h2>第一步：建表时，告诉 Paimon "顺便登记进册子"</h2>
<p>方法很简单：在 Flink（或 Spark）里建 catalog 时，加一句 <code>metastore = 'hive'</code>，再填上登记册的地址。这样以后建的 Paimon 表，都会自动在 HMS 那本册子上"挂个名"：</p>
""" + code("sql", "Flink SQL：建一个“会自动登记到 HMS”的 Paimon catalog", """CREATE CATALOG paimon_hive WITH (
    'type' = 'paimon',
    'metastore' = 'hive',                       -- 关键：登记到 Hive 的册子
    'uri' = 'thrift://localhost:9083',          -- 登记册（HMS）的地址
    'warehouse' = 'hdfs:///warehouse/paimon'    -- 数据实际存放的仓库
);
USE CATALOG paimon_hive;

CREATE TABLE user_log (
    id   BIGINT PRIMARY KEY NOT ENFORCED,
    name STRING
);""") + """
<p>建完这张 <code>user_log</code>，它有两个身份：① 它是一张实打实的 Paimon 表（数据按 Paimon 的方式存）；② 它的"名字和地址"已经登记进了 HMS。<strong>于是 Hive 那边，翻开册子就能看见它了。</strong></p>

<h2>第二步：在 Hive 里直接查这张 Paimon 表</h2>
<p>Hive 端要查 Paimon 表，得先给 Hive "装个能读 Paimon 的小工具"（一个 jar 包），之后就能像查普通老表一样查：</p>
""" + code("sql", "在 Hive CLI 或 Beeline 里执行", """-- 先加载 Paimon 的 Hive 连接器（路径换成你机器上的 jar 位置）
ADD JAR /opt/paimon/paimon-hive-connector.jar;

-- 然后就能直接查上一步建的表了
SELECT * FROM user_log LIMIT 10;""") + """
<div class="callout warn">
<span class="tag">老规矩：注意版本和 jar</span>
<p>Hive 这块对版本比较挑：要用<strong>和你 Hive 版本匹配</strong>的 paimon-hive-connector jar，还要保证能连上 HMS。版本不匹配时，常见报错是"找不到 SerDe / InputFormat"之类——看到这种错，先怀疑 jar 版本不对。</p>
</div>

<h2>第三步：理解这么做"值在哪"</h2>
<p>一张图说清楚：表只登记一次，所有认册子的工具都能用——</p>
<div class="flow">
<div class="node brand"><div class="nt">一张 Paimon 表</div><div class="nd">登记进 HMS 这本册子</div></div>
<div class="arrow">↓ 大家共查这一本册子</div>
<div class="node"><div class="nt">Hive · Spark · Trino · StarRocks</div><div class="nd">翻开册子都能发现、都能查同一张表</div></div>
</div>
<p>对有老数仓的团队来说，这事的价值就一句话：<strong>不用推倒重来。</strong>新建的实时表用 Paimon，登记进大家熟悉的那本老册子（HMS），原来的查询工具、报表、脚本照样能跑，迁移成本压到最低。这也是为什么 Paimon 能"挤进"已经很成熟的公司体系里。</p>

""" + exercise("练习 17-1", "<p>用一句大白话解释：为什么把 Paimon 表登记进 Hive Metastore，连“根本不是 Hive 的工具”（比如 Spark、StarRocks）也能查到这张表？</p>",
        "<p>因为 Spark、StarRocks 这些工具也认 Hive Metastore 这本“登记册”。HMS 是一本被大家公用的“表目录”，只要表登记在里面，所有翻这本册子的工具都能发现并查询它——不是只有 Hive 自己能看。</p>") + """

<div class="callout tip">
<span class="tag">这一章你要带走的</span>
<p>搞懂 Hive Metastore 就是一本"大家公用的表登记册"，会用 <code>metastore='hive'</code> 把 Paimon 表登记进去，并在 Hive 端查到它，明白这对融合老数仓有多省事。下一章请出"飞毛腿传菜员" StarRocks，体验对 Paimon 的秒级快查。</p>
</div>
"""

    return B
