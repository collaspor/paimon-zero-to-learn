(function () {
  // Mobile sidebar toggle
  function bindMenu() {
    var btn = document.querySelector('.menu-btn');
    var sidebar = document.querySelector('.sidebar');
    var overlay = document.querySelector('.overlay');
    if (!btn || !sidebar) return;
    function open() { sidebar.classList.add('open'); if (overlay) overlay.classList.add('show'); }
    function close() { sidebar.classList.remove('open'); if (overlay) overlay.classList.remove('show'); }
    btn.addEventListener('click', function () {
      sidebar.classList.contains('open') ? close() : open();
    });
    if (overlay) overlay.addEventListener('click', close);
    sidebar.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', close);
    });
  }

  // Highlight active nav link by current filename
  function highlightNav() {
    var path = location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('.nav a').forEach(function (a) {
      var href = (a.getAttribute('href') || '').split('/').pop();
      if (href === path) a.classList.add('active');
    });
  }

  // Copy-to-clipboard for code blocks
  function bindCopy() {
    document.querySelectorAll('.codeblock').forEach(function (block) {
      var btn = block.querySelector('.copy-btn');
      var pre = block.querySelector('pre');
      if (!btn || !pre) return;
      btn.addEventListener('click', function () {
        var text = pre.innerText;
        navigator.clipboard.writeText(text).then(function () {
          var old = btn.textContent;
          btn.textContent = '已复制';
          btn.classList.add('copied');
          setTimeout(function () { btn.textContent = old; btn.classList.remove('copied'); }, 1600);
        });
      });
    });
  }

  // Build in-page TOC from h2/h3 inside .content
  function buildTOC() {
    var toc = document.getElementById('toc');
    var content = document.querySelector('.content');
    if (!toc || !content) return;
    var heads = content.querySelectorAll('h2, h3');
    if (heads.length < 2) { toc.style.display = 'none'; return; }
    var slugCount = {};
    function slug(t) {
      var s = t.trim().toLowerCase().replace(/[^\w\u4e00-\u9fa5]+/g, '-').replace(/^-+|-+$/g, '');
      if (!s) s = 'sec';
      if (slugCount[s] != null) { slugCount[s]++; s = s + '-' + slugCount[s]; }
      else { slugCount[s] = 0; }
      return s;
    }
    var html = '<div class="toc-title">本页目录</div>';
    heads.forEach(function (h) {
      if (!h.id) h.id = slug(h.textContent);
      var lvl = h.tagName === 'H3' ? ' lvl3' : '';
      html += '<a href="#' + h.id + '" class="toc-link' + lvl + '">' + h.textContent + '</a>';
    });
    toc.innerHTML = html;

    // Active highlight on scroll
    var links = toc.querySelectorAll('.toc-link');
    function onScroll() {
      var pos = window.scrollY + 120;
      var cur = null;
      heads.forEach(function (h) { if (h.offsetTop <= pos) cur = h.id; });
      links.forEach(function (a) {
        a.classList.toggle('active', a.getAttribute('href') === '#' + cur);
      });
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // Reading progress bar
  function bindProgress() {
    var bar = document.getElementById('progress');
    if (!bar) return;
    function update() {
      var h = document.documentElement;
      var max = (h.scrollHeight - h.clientHeight) || 1;
      var pct = Math.min(100, Math.max(0, (window.scrollY / max) * 100));
      bar.style.width = pct + '%';
    }
    window.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update);
    update();
  }

  document.addEventListener('DOMContentLoaded', function () {
    bindMenu();
    highlightNav();
    bindCopy();
    buildTOC();
    bindProgress();
    if (window.hljs) { try { window.hljs.highlightAll(); } catch (e) {} }
  });
})();
