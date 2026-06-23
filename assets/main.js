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

  document.addEventListener('DOMContentLoaded', function () {
    bindMenu();
    highlightNav();
    bindCopy();
    if (window.hljs) { try { window.hljs.highlightAll(); } catch (e) {} }
  });
})();
