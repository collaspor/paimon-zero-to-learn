# -*- coding: utf-8 -*-
"""Generator for the 'Learn Apache Paimon from zero' static site.

Shared shell + sidebar + in-page TOC + reading progress bar.
Per-page content lives in content/*.py (one module per page group),
imported as a single BODIES dict. Run once to emit index.html and pages/*.html.
"""
import os
import html as _html

ROOT = os.path.dirname(os.path.abspath(__file__))

# (filename, idx_label, nav_title, is_index)
PAGES = [
    ("index.html",                  "",  "首页 · 学习总览", True),
    ("pages/00-roadmap.html",       "0", "零基础学习路线", False),
    ("pages/01-linux.html",         "1", "Linux 与终端", False),
    ("pages/02-sql.html",           "2", "SQL 与数据建模", False),
    ("pages/03-bigdata.html",       "3", "大数据与计算引擎", False),
    ("pages/04-cdc-lakehouse.html", "4", "CDC 与湖仓", False),
    ("pages/05-what-is-paimon.html","5", "Paimon 是什么", False),
    ("pages/06-concepts.html",      "6", "核心概念与原理", False),
    ("pages/07-env-setup.html",     "7", "环境搭建", False),
    ("pages/08-quickstart.html",    "8", "Quick Start 上手", False),
    ("pages/09-cdc-practice.html",  "9", "实战：CDC 入湖", False),
    ("pages/10-advanced.html",      "10","进阶：表类型与调优", False),
    ("pages/11-comparison.html",    "11","对标对比与选型", False),
    ("pages/12-faq.html",           "12","常见问题与排错", False),
    ("pages/13-resources.html",     "13","学习资源与下一步", False),
]

NAV_GROUPS = [
    ("开始", [0, 1]),
    ("打基础", [2, 3, 4, 5]),
    ("学 Paimon", [6, 7]),
    ("动手实践", [8, 9, 10]),
    ("进阶 · 拓展", [11, 12, 13, 14]),
]


def rel(from_is_index, target):
    if from_is_index:
        return target
    if target == "index.html":
        return "../index.html"
    return target.split("/", 1)[1]


def asset(from_is_index, path):
    return ("assets/" + path) if from_is_index else ("../assets/" + path)


def build_sidebar(cur_is_index):
    out = ['<aside class="sidebar" id="sidebar">']
    home = rel(cur_is_index, "index.html")
    out.append(f'<a href="{home}" class="brand" style="text-decoration:none">'
               '<span class="logo">P</span>'
               '<span><span class="name" style="display:block;color:var(--text)">Paimon 学习站</span>'
               '<span class="sub">从 0 到入门 · 完整自学</span></span></a>')
    for gtitle, idxs in NAV_GROUPS:
        out.append('<div class="nav-group"><div class="nav-group-title">'
                   f'{gtitle}</div><nav class="nav">')
        for i in idxs:
            fn, idx, title, is_index = PAGES[i]
            href = rel(cur_is_index, fn)
            label = idx if idx else "•"
            out.append(f'<a href="{href}"><span class="idx">{label}</span>{title}</a>')
        out.append('</nav></div>')
    out.append('</aside>')
    return "\n".join(out)


def build_pager(cur_index):
    prev_html = '<a class="disabled"></a>'
    next_html = '<a class="disabled"></a>'
    cur_is_index = PAGES[cur_index][3]
    if cur_index > 0:
        fn, idx, title, _ = PAGES[cur_index - 1]
        href = rel(cur_is_index, fn)
        prev_html = (f'<a class="prev" href="{href}"><span class="dir">← 上一页</span>'
                     f'<span class="pttl">{title}</span></a>')
    if cur_index < len(PAGES) - 1:
        fn, idx, title, _ = PAGES[cur_index + 1]
        href = rel(cur_is_index, fn)
        next_html = (f'<a class="next" href="{href}"><span class="dir">下一页 →</span>'
                     f'<span class="pttl">{title}</span></a>')
    return f'<div class="pager">{prev_html}{next_html}</div>'


def page_shell(cur_index, title, body):
    fn, idx, nav_title, is_index = PAGES[cur_index]
    css = asset(is_index, "style.css")
    js = asset(is_index, "main.js")
    sidebar = build_sidebar(is_index)
    pager = build_pager(cur_index)
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} · 从 0 学习 Apache Paimon</title>
<meta name="description" content="面向零基础的 Apache Paimon 中文完整自学教程：Linux、SQL、大数据、CDC、湖仓、Paimon 核心概念、环境搭建、Quick Start、实战与排错。">
<link rel="stylesheet" href="{css}">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-dark.min.css">
</head>
<body>
<div class="progress-bar" id="progress"></div>
<div class="topbar">
  <button class="menu-btn" aria-label="打开菜单">☰</button>
  <span class="logo">P</span>
  <strong style="font-size:15px">Paimon 学习站</strong>
</div>
<div class="overlay" id="overlay"></div>
<div class="layout">
{sidebar}
<main class="main"><div class="content">
{body}
{pager}
</div></main>
<nav class="toc" id="toc"></nav>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<script src="{js}"></script>
</body>
</html>
"""


def code(lang, label, text):
    esc = _html.escape(text)
    return (f'<div class="codeblock"><div class="bar"><span>{label}</span>'
            f'<button class="copy-btn">复制</button></div>'
            f'<pre><code class="language-{lang}">{esc}</code></pre></div>')


def term(word, en, desc):
    en_html = f'<span class="en">{en}</span>' if en else ''
    return (f'<div class="term"><div class="word">{word}{en_html}</div>'
            f'<p>{desc}</p></div>')


def exercise(title, prompt, answer):
    return (f'<div class="exercise"><div class="ex-h">{title}</div>'
            f'<div>{prompt}</div>'
            f'<details class="answer"><summary>查看参考答案</summary>{answer}</details></div>')


# expose helpers to content modules via builtins-like injection
import content  # noqa: E402  (content package builds BODIES using helpers)

BODIES = content.build_bodies(code=code, term=term, exercise=exercise)


def main():
    missing = [fn for (fn, *_rest) in PAGES if fn not in BODIES]
    if missing:
        raise SystemExit("Missing bodies for: " + ", ".join(missing))
    for i, (fn, idx, title, is_index) in enumerate(PAGES):
        body = BODIES[fn]
        html_out = page_shell(i, title, body)
        out_path = os.path.join(ROOT, fn.replace("/", os.sep))
        os.makedirs(os.path.dirname(out_path) or ROOT, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html_out)
        print("written:", fn)


if __name__ == "__main__":
    main()
