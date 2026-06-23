# 从 0 学习 Apache Paimon

一个面向**零基础**的 Apache Paimon 中文学习网站。纯静态（HTML/CSS/JS），零构建依赖，开箱即可部署到 GitHub Pages。

## 内容结构

| 章节 | 页面 | 内容 |
|------|------|------|
| 首页 | `index.html` | 学习总览与路线入口 |
| 第 0 章 | `pages/00-roadmap.html` | 零基础学习路线（四层地基 → Paimon） |
| 第 1 章 | `pages/01-prerequisites.html` | 预备知识：Linux / SQL / 表·主键·分区·ETL·数仓 |
| 第 2 章 | `pages/02-stream-batch.html` | 计算基础：批 vs 流 / Spark / Flink / CDC |
| 第 3 章 | `pages/03-what-is-paimon.html` | Paimon 是什么：定位、特性、场景 |
| 第 4 章 | `pages/04-concepts.html` | 核心概念：snapshot / LSM / compaction 等 |
| 第 5 章 | `pages/05-quickstart.html` | Flink Quick Start 上手 |
| 第 6 章 | `pages/06-comparison.html` | 对标对比：Iceberg / Hudi / Delta Lake |
| 第 7 章 | `pages/07-resources.html` | 学习资源汇总 |

## 本地预览

任选一种方式，在项目根目录执行：

```bash
# Python
python -m http.server 8000
# 然后浏览器打开 http://localhost:8000
```

```bash
# Node（已装 npx）
npx serve .
```

## 部署到 GitHub Pages

1. 在 GitHub 新建一个仓库（如 `paimon-zero-to-learn`，需 Public 才能免费用 Pages）。
2. 把本目录所有文件推送上去：

```bash
git init
git add .
git commit -m "init: 从 0 学习 Apache Paimon 学习网站"
git branch -M main
git remote add origin https://github.com/<你的用户名>/<仓库名>.git
git push -u origin main
```

3. 打开仓库 **Settings → Pages**，Source 选择 `Deploy from a branch`，分支选 `main`、目录选 `/ (root)`，保存。
4. 等几分钟，访问 `https://<你的用户名>.github.io/<仓库名>/` 即可。

> 仓库已包含 `.nojekyll`，避免 GitHub Pages 的 Jekyll 处理忽略静态资源。

## 技术说明

- 纯静态页面，无后端、无打包工具。
- 代码高亮使用 highlight.js（CDN 加载，无本地依赖）。
- 页面由 `build_site.py` 统一生成，保证侧边栏与外壳一致；修改内容后重新运行该脚本即可。

## 内容来源

正文为本教程原创编排，技术事实参考 [Apache Paimon 官方文档](https://paimon.apache.org/)。对标对比部分综合官方定位与社区/市场视角，非任一厂商官方结论。
