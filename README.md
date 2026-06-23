# 从 0 学习 Apache Paimon

一个面向**零基础**的 Apache Paimon 中文**完整自学**教程。纯静态（HTML/CSS/JS），零构建依赖，开箱即可部署到 GitHub Pages。

目标：**只看这一个站，就能从 0 学会 Paimon**——从终端命令、SQL，到 Flink、CDC、湖仓，再到 Paimon 的原理、上手、实战与调优，自成闭环，无需再查其他资料。

## 在线访问

https://collaspor.github.io/paimon-zero-to-learn/

## 内容结构（首页 + 14 章，五个阶段）

| 阶段 | 章节 | 页面 | 内容 |
|------|------|------|------|
| 开始 | 第 0 章 | `pages/00-roadmap.html` | 零基础学习路线与全局地图 |
| 开始 | 第 1 章 | `pages/01-linux.html` | Linux 与终端：命令、路径、环境变量、解压 |
| 打基础 | 第 2 章 | `pages/02-sql.html` | SQL 与数据建模：查询/聚合/JOIN、表/主键/分区/数仓 |
| 打基础 | 第 3 章 | `pages/03-bigdata.html` | 大数据与计算引擎：批 vs 流、HDFS、Spark/Flink |
| 打基础 | 第 4 章 | `pages/04-cdc-lakehouse.html` | CDC 与湖仓：变更捕获、湖仓演进、表格式由来 |
| 打基础 | 第 5 章 | `pages/05-what-is-paimon.html` | Paimon 是什么：定位、特性、场景 |
| 学 Paimon | 第 6 章 | `pages/06-concepts.html` | 核心概念与原理：snapshot/LSM/compaction 配图详解 |
| 学 Paimon | 第 7 章 | `pages/07-env-setup.html` | 环境搭建：Java/Flink/Paimon jar + 排错 |
| 动手实践 | 第 8 章 | `pages/08-quickstart.html` | Quick Start：建表、流写、批查、流查（逐行讲解） |
| 动手实践 | 第 9 章 | `pages/09-cdc-practice.html` | 实战：MySQL → Flink CDC → Paimon 入湖 |
| 动手实践 | 第 10 章 | `pages/10-advanced.html` | 进阶：表类型、merge engine、bucket、compaction 调优 |
| 进阶·拓展 | 第 11 章 | `pages/11-comparison.html` | 对标对比：Iceberg / Hudi / Delta Lake 与选型 |
| 进阶·拓展 | 第 12 章 | `pages/12-faq.html` | 常见问题与排错（环境/写入/查询/存储） |
| 进阶·拓展 | 第 13 章 | `pages/13-resources.html` | 术语速查、官方资料导读、继续提升的方向 |

## 站点特性

- 左侧分组导航 + 右侧「本页目录」(TOC) 锚点，顶部阅读进度条。
- 代码块语法高亮 + 一键复制；重要章节含练习题与可折叠参考答案。
- 术语卡、流程图示、对比表、Callout 提示等多种排版组件。
- 响应式：窄屏自动折叠侧边栏、隐藏 TOC。

## 本地预览

在项目根目录执行：

```bash
python -m http.server 8000
# 浏览器打开 http://localhost:8000
```

## 部署到 GitHub Pages

1. 仓库需为 Public（免费 Pages）。
2. 打开仓库 **Settings → Pages**，Source 选择 `Deploy from a branch`，分支选 `main`、目录选 `/ (root)`，保存。
3. 等几分钟，访问 `https://collaspor.github.io/paimon-zero-to-learn/` 即可。

> 仓库已包含 `.nojekyll`，避免 GitHub Pages 的 Jekyll 处理忽略静态资源。

## 技术说明

- 纯静态页面，无后端、无打包工具。
- 代码高亮使用 highlight.js（CDN 加载）。
- 页面由 `build_site.py` + `content/*.py` 生成：外壳/导航/TOC 在 `build_site.py`，各章正文在 `content/` 下分模块维护。修改内容后重新运行 `python build_site.py` 即可。

## 内容来源

正文为本教程原创编排，技术事实参考 [Apache Paimon 官方文档](https://paimon.apache.org/)。版本号、API 细节请以官方文档为准。对标对比部分综合官方定位与社区/市场视角，非任一厂商官方结论。
