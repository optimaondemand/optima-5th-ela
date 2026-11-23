/* g5-sparkle.js — OAO Grade 5 ELA sparkle layer: The Commonplace Book.
 *
 * Holds NO lesson content. Everything a lesson shows comes from its own
 * <script type="application/json" id="oao-data"> block (written by
 * tools/g5sparkle/inject.py from data/g5ela-<week>-<day>.json). A missing key
 * turns off only its own feature. Every module runs inside guard(), so one
 * failure never blanks the page; failures are listed in window.OAO_SPARKLE_FAILED.
 *
 * Storage (all wrapped in try/catch):
 *   oao.g5ela.book            the year-long Commonplace Book, one entry per lesson
 *   oao.g5ela.profile         { name }
 *   oao.g5ela.<key>.<thing>   per-lesson state (hook, checks, game)
 *   oao.g5ela.stones.wk<NN>   the week's river crossing
 *
 * Built Nov 2026 for the g5-ela-sparkle-lesson skill. Never put lesson text here.
 */
(function () {
  'use strict';
  if (window.__g5Sparkle) return;
  window.__g5Sparkle = true;
  window.OAO_SPARKLE_FAILED = window.OAO_SPARKLE_FAILED || [];

  function readJSON(id) {
    var el = document.getElementById(id);
    if (!el) return null;
    try { return JSON.parse(el.textContent || '{}'); } catch (e) { return null; }
  }
  var L = readJSON('oao-lesson');
  var D = readJSON('oao-data') || {};
  if (!L) return;
  var KEY = 'g5ela-' + L.week + '-' + L.day;
  var REDUCED = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ── tiny helpers ─────────────────────────────────────────── */
  function store(k, v) {
    try {
      if (v === undefined) { var s = localStorage.getItem('oao.g5ela.' + k); return s ? JSON.parse(s) : null; }
      localStorage.setItem('oao.g5ela.' + k, JSON.stringify(v)); return true;
    } catch (e) { return v === undefined ? null : false; }
  }
  function h(tag, attrs, kids) {
    var el = document.createElement(tag);
    if (attrs) for (var a in attrs) {
      if (a === 'html') el.innerHTML = attrs[a];
      else if (a === 'text') el.textContent = attrs[a];
      else if (a.slice(0, 2) === 'on') el.addEventListener(a.slice(2), attrs[a]);
      else el.setAttribute(a, attrs[a]);
    }
    (kids || []).forEach(function (k) { if (k) el.appendChild(typeof k === 'string' ? document.createTextNode(k) : k); });
    return el;
  }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function words(s) { return (String(s || '').trim().match(/[A-Za-z0-9'’-]+/g) || []).length; }
  function sentences(s) { return (String(s || '').match(/[^.!?]+[.!?]+/g) || []).filter(function (x) { return words(x) >= 3; }).length; }
  function guard(name, fn) {
    try { fn(); } catch (e) { window.OAO_SPARKLE_FAILED.push(name + ': ' + (e && e.message)); if (window.console) console.error('[g5-sparkle] ' + name, e); }
  }
  function panel(tab) { return document.getElementById('tab-' + tab); }
  function nextWrap(tab) { var p = panel(tab); return p ? p.querySelector(':scope > .tab-next-wrap') : null; }
  function activityByTitle(sub, scope) {
    var titles = (scope || document).querySelectorAll('.activity-title');
    for (var i = 0; i < titles.length; i++) if (titles[i].textContent.indexOf(sub) >= 0) return titles[i].closest('.activity');
    return null;
  }
  function afterNode(ref, node) { ref.parentNode.insertBefore(node, ref.nextSibling); }
  function top(tab) {
    // first place inside a tab where layer cards go: after the tracker card on Reading, else the start
    var p = panel(tab); if (!p) return null;
    var tr = p.querySelector(':scope > .tracker-card');
    return { panel: p, after: tr };
  }
  function putTop(tab, node) {
    var t = top(tab); if (!t) return;
    if (t.after) afterNode(t.after, node);
    else t.panel.insertBefore(node, t.panel.firstChild);
  }
  function fileExists(url, cb) {
    var a = new Audio(); var done = false;
    a.preload = 'metadata';
    a.addEventListener('loadedmetadata', function () { if (!done) { done = true; cb(true, a); } });
    a.addEventListener('error', function () { if (!done) { done = true; cb(false); } });
    a.src = url;
  }

  /* one audio at a time; stop the page's own read-aloud first */
  var nowPlaying = null;
  function play(url, btn) {
    try { if (window.speechSynthesis) window.speechSynthesis.cancel(); } catch (e) {}
    document.querySelectorAll('.g5-film video').forEach(function (o) { try { o.pause(); } catch (e) {} });
    if (nowPlaying) { nowPlaying.pause(); if (nowPlaying._btn) nowPlaying._btn.classList.remove('g5-playing'); if (nowPlaying._btn === btn) { nowPlaying = null; return; } }
    var a = new Audio(url); a._btn = btn; nowPlaying = a;
    btn && btn.classList.add('g5-playing');
    a.addEventListener('ended', function () { btn && btn.classList.remove('g5-playing'); nowPlaying = null; });
    a.play().catch(function () { btn && btn.classList.remove('g5-playing'); });
  }
  function clip(path) { return (window.__G5_CLIPS && window.__G5_CLIPS[path]) || path; }  // preview builds inline clips
  function audioUrl(slot) { return clip('assets/audio/guide/g5ela-' + L.week + '-' + L.day + '-' + slot + '.mp3'); }
  function videoUrl(slot) { return clip('assets/video/guide/g5ela-' + L.week + '-' + L.day + '-' + slot + '.mp4'); }
  /* a film beside a Listen clip: H.264 High, yuv420p, AAC, +faststart (see tools/g5video). Poster = same name .jpg,
     captions = same name .vtt (off until CC is pressed). */
  function filmControl(src, label) {
    if (!src || /^data:audio/.test(src)) return null;
    var fig = document.createElement('figure'); fig.className = 'g5-film'; fig.hidden = true;
    var v = document.createElement('video');
    v.controls = true; v.playsInline = true; v.setAttribute('playsinline', ''); v.preload = 'metadata';
    v.setAttribute('aria-label', label);
    var se = document.createElement('source'); se.src = src; se.type = 'video/mp4'; v.appendChild(se);
    fig.appendChild(v);
    var okFns = [], badFns = [], settled = false;
    function bad() { if (settled) return; settled = true; fig.remove(); badFns.forEach(function (f) { f(); }); }
    v.addEventListener('loadedmetadata', function () {
      if (settled) return; settled = true; fig.hidden = false;
      if (/\.mp4(\?|$)/.test(src)) v.poster = src.replace(/\.mp4(\?|$)/, '.jpg$1');
      okFns.forEach(function (f) { f(); });
      var vtt = src.replace(/\.mp4(\?|$)/, '.vtt$1');
      if (vtt !== src && window.fetch) fetch(vtt, { method: 'HEAD', cache: 'no-cache' }).then(function (r) {
        if (!r.ok) return;
        var t = document.createElement('track'); t.kind = 'captions'; t.srclang = 'en'; t.label = 'English'; t.src = vtt;
        v.appendChild(t); if (t.track) t.track.mode = 'disabled';
      }).catch(function () {});
    });
    v.addEventListener('error', bad); se.addEventListener('error', bad);
    v.addEventListener('play', function () {
      try { if (window.speechSynthesis) window.speechSynthesis.cancel(); } catch (e) {}
      if (nowPlaying) { try { nowPlaying.pause(); if (nowPlaying._btn) nowPlaying._btn.classList.remove('g5-playing'); } catch (e) {} nowPlaying = null; }
      document.querySelectorAll('.g5-film video').forEach(function (o) { if (o !== v) o.pause(); });
    });
    return { fig: fig, ready: function (f) { okFns.push(f); }, fail: function (f) { badFns.push(f); } };
  }
  function howUrl(slug) { return clip('assets/audio/guide/how/g5ela-how-' + slug + '.mp3'); }

  /* ── 1. the paper: header strip, fonts, ribbon ────────────── */
  function buildTheme() {
    // The page's own banner (navy header, Optima logo, progress bar) is never restyled.
    document.documentElement.classList.add('g5-on');
    if (!document.getElementById('g5-fonts')) {
      document.head.appendChild(h('link', { id: 'g5-fonts', rel: 'stylesheet',
        href: 'https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&display=swap' }));
    }
  }

  /* ── 2. the ribbon bookmark: this week's pages ────────────── */
  function bookAll() { return store('book') || {}; }
  function pageDone(p) { return !!(p && p.own && words(p.own) >= 4 && sentences(p.why) >= 2 && words(p.sentence) >= 8); }
  function buildRibbon() {
    if (typeof L.day !== 'number' || !D.book) return;   // the ribbon belongs to the Commonplace Book
    var r = h('button', { 'class': 'g5-ribbon', type: 'button', 'aria-label': 'Open my Commonplace Book' });
    r.addEventListener('click', openBook);
    document.body.appendChild(r);
    paintRibbon();
  }
  function paintRibbon() {
    var r = document.querySelector('.g5-ribbon'); if (!r) return;
    var all = bookAll(), dots = '';
    for (var d = 1; d <= 4; d++) {
      var done = pageDone(all['g5ela-' + L.week + '-' + d]);
      dots += '<span class="g5-rdot' + (done ? ' on' : '') + (d === L.day ? ' here' : '') + '" title="Day ' + d + (done ? ': page written' : '') + '"></span>';
    }
    r.innerHTML = '<span class="g5-rib-ico" aria-hidden="true">📖</span><span class="g5-rib-t">My book</span><span class="g5-rib-dots">' + dots + '</span>';
  }

  /* ── 3. Listen cards: Mason, the G5 ELA guide (portrait assets/companions/mason-v2.jpg) ── */
  function buildListen() {
    if (!D.listen) return;
    ['page', 'warmup', 'words', 'reading', 'assignment'].forEach(function (tab) {
      var c = D.listen[tab]; if (!c || !c.text) return;
      var slot = c.clip || ('listen-' + tab);
      var play_ = h('button', { 'class': 'g5-listen-play', type: 'button', hidden: 'hidden', 'aria-label': 'Play' }, ['▶ Listen']);
      var words_ = h('details', { 'class': 'g5-listen-words' }, [h('summary', { text: 'Read the words instead' }), h('p', { text: c.text })]);
      var main_ = h('div', { 'class': 'g5-listen-main' }, [h('div', { 'class': 'g5-listen-t', text: 'Mason' }), play_, words_]);
      var card = h('div', { 'class': 'g5-listen', 'data-tab': tab }, [
        h('img', { 'class': 'g5-listen-av', src: 'assets/companions/mason-v2.jpg', alt: '' }), main_
      ]);
      play_.addEventListener('click', function () { play(audioUrl(slot), play_); });
      var filmOn = false, audioOk = false;
      fileExists(audioUrl(slot), function (ok) { audioOk = ok; if (ok) { if (!filmOn) play_.hidden = false; words_.querySelector('summary').textContent = 'Read the words'; } else if (!filmOn) { words_.open = true; } });
      /* Mason's film: the same name under assets/video/ (…/g5ela-21-1-listen-words.mp4 beside the .mp3).
         It carries the voice, so it replaces the Listen button. Hidden until it loads; if it fails, the audio stays. */
      var film = filmControl(videoUrl(slot), 'Mason: ' + tab);
      if (film) {
        main_.insertBefore(film.fig, words_);
        film.ready(function () { filmOn = true; play_.hidden = true; words_.open = false; words_.querySelector('summary').textContent = 'Read the words'; card.classList.add('g5-has-film'); });
        film.fail(function () { filmOn = false; card.classList.remove('g5-has-film'); if (audioOk) play_.hidden = false; });
      }
      if (tab === 'page') {   // one-page lessons (fluency): above the passage
        var fp = document.querySelector('.fluency-passage') || document.querySelector('.steps');
        if (fp) fp.parentNode.insertBefore(card, fp);
        return;
      }
      putTop(tab, card);
    });
  }

  /* ── 4. the hook (Warm-Up, day 1 usually) ─────────────────── */
  function buildHook() {
    var H = D.hook; if (!H) return;
    var saved = store(KEY + '.hook');
    var card = h('div', { 'class': 'g5-card g5-hook' });
    card.innerHTML = '<div class="g5-card-k">Before you begin</div><p class="g5-hook-q">' + esc(H.q) + '</p>';
    var opts = h('div', { 'class': 'g5-choices', role: 'group', 'aria-label': H.q });
    var out = h('div', { 'class': 'g5-hook-out', 'aria-live': 'polite' });
    function reveal(i) {
      opts.querySelectorAll('button').forEach(function (b, j) { b.setAttribute('aria-pressed', j === i ? 'true' : 'false'); });
      out.innerHTML = (H.options[i].reply ? '<p>' + esc(H.options[i].reply) + '</p>' : '') +
        '<blockquote class="g5-quote">“' + esc(H.reveal.line) + '”<cite>' + esc(H.reveal.cite) + '</cite></blockquote>' +
        (H.reveal.then ? '<p>' + esc(H.reveal.then) + '</p>' : '');
      store(KEY + '.hook', i);
    }
    H.options.forEach(function (o, i) { opts.appendChild(h('button', { type: 'button', 'class': 'g5-choice', 'aria-pressed': 'false', onclick: function () { reveal(i); } }, [o.t])); });
    card.appendChild(opts); card.appendChild(out);
    if (typeof saved === 'number' && H.options[saved]) reveal(saved);
    var t = top('warmup'); if (!t) return;
    var li = t.panel.querySelector(':scope > .g5-listen');
    if (li) afterNode(li, card); else t.panel.insertBefore(card, t.panel.firstChild);
  }

  /* ── 5. quick checks: meet the trip point, see it fail ────── */
  function buildChecks() {
    (D.checks || []).forEach(function (C, n) {
      var p = panel(C.tab); if (!p) return;
      var skey = KEY + '.check' + n, saved = store(skey);
      var card = h('div', { 'class': 'g5-card g5-check' });
      card.innerHTML = '<div class="g5-card-k">' + esc(C.kicker || 'Quick check') + '</div><p class="g5-check-q">' + esc(C.q) + '</p>';
      var opts = h('div', { 'class': 'g5-choices', role: 'group', 'aria-label': C.q });
      var out = h('div', { 'class': 'g5-check-out', 'aria-live': 'polite' });
      function pick(i) {
        var o = C.options[i];
        opts.querySelectorAll('button').forEach(function (b, j) {
          b.classList.toggle('g5-right', j === i && !!o.ok);
          b.classList.toggle('g5-notyet', j === i && !o.ok);
          b.setAttribute('aria-pressed', j === i ? 'true' : 'false');
        });
        out.innerHTML = '<p><b>' + (o.ok ? 'Yes.' : 'Not quite.') + '</b> ' + esc(o.why) + '</p>';
        store(skey, i);
      }
      C.options.forEach(function (o, i) { opts.appendChild(h('button', { type: 'button', 'class': 'g5-choice', 'aria-pressed': 'false', onclick: function () { pick(i); } }, [o.t])); });
      card.appendChild(opts); card.appendChild(out);
      if (typeof saved === 'number' && C.options[saved]) pick(saved);
      var ref = C.after ? activityByTitle(C.after, p) : null;
      if (ref) afterNode(ref, card);
      else { var nw = nextWrap(C.tab); if (nw) p.insertBefore(card, nw); else p.appendChild(card); }
    });
  }

  /* ── 6. "What to do" lines on every activity ──────────────── */
  function howLine(H) {
    var box = h('div', { 'class': 'g5-do' });
    var head = h('div', { 'class': 'g5-do-h' }, [h('b', { text: 'What to do' })]);
    if (H.say) {
      var b = h('button', { type: 'button', 'class': 'g5-do-say', hidden: 'hidden', 'aria-label': 'Hear the directions' }, ['🔊']);
      b.addEventListener('click', function () { play(howUrl(H.say), b); });
      fileExists(howUrl(H.say), function (ok) { if (ok) b.hidden = false; });
      head.appendChild(b);
    }
    box.appendChild(head);
    var ol = h('ol', { 'class': 'g5-do-steps' });
    (H['do'] || []).forEach(function (s) { ol.appendChild(h('li', { text: s })); });
    box.appendChild(ol);
    if (H.why || H.use) {
      var d = h('details', { 'class': 'g5-why' }, [h('summary', { text: 'Why are we doing this?' })]);
      if (H.why) d.appendChild(h('p', { text: H.why }));
      if (H.use) d.appendChild(h('p', { 'class': 'g5-use', text: H.use }));
      box.appendChild(d);
    }
    return box;
  }
  /* Pilot review (Nov 2026): "too much to read". On the Warm-Up and Word Study
     tabs, the lead-in paragraph under What to do mostly repeats it. Fold it into
     a closed "More help" so it is there for a student who wants it. */
  function foldIntro(act, box) {
    var tab = act.closest('.tab-panel');
    if (!tab || !/^tab-(warmup|words)$/.test(tab.id)) return;
    var nx = box.nextElementSibling;
    if (!nx || nx.tagName !== 'P' || nx.querySelector('input,textarea,button,select')) return;
    var more = h('details', { 'class': 'g5-why g5-more' }, [h('summary', { text: 'More help' })]);
    more.appendChild(nx);
    box.appendChild(more);
  }
  function buildHow() {
    (D.how || []).forEach(function (H) {
      var act = H.match ? activityByTitle(H.match) : null;
      if (!act) { if (H.match) window.OAO_SPARKLE_FAILED.push('how: no activity titled "' + H.match + '"'); return; }
      var body = act.querySelector(':scope > .activity-body') || act;
      if (body.querySelector(':scope > .g5-do')) return;
      var box = howLine(H);
      body.insertBefore(box, body.firstChild);
      foldIntro(act, box);
    });
  }

  /* ── 7. glossary: dotted words, tap to see the meaning ────── */
  function buildGlossary() {
    (D.glossary || []).forEach(function (G) {
      var scope = G['in'] ? activityByTitle(G['in']) : document.body;
      if (!scope) return;
      var re = new RegExp('\\b(' + G.word.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')\\b', 'i');
      /* first look in the page text students see; only if the word is not there,
         look in the folds under What to do ("Why are we doing this?", "More help").
         The What to do steps themselves stay clean. */
      function find(folds) {
        var w = document.createTreeWalker(scope, NodeFilter.SHOW_TEXT, {
          acceptNode: function (n) {
            var p = n.parentNode;
            if (!p || p.closest('button, textarea, input, script, style, .g5-gloss, .activity-title, summary')) return NodeFilter.FILTER_REJECT;
            if (p.closest('.g5-do') && !(folds && p.closest('.g5-why'))) return NodeFilter.FILTER_REJECT;
            return re.test(n.nodeValue) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_SKIP;
          }
        });
        return w.nextNode();
      }
      var node = find(false) || find(true); if (!node) return;
      var m = re.exec(node.nodeValue);
      var after = node.splitText(m.index); after.nodeValue = after.nodeValue.slice(m[0].length);
      /* hover (or focus, or tap on a tablet) shows the meaning in a box that floats
         over the page; nothing around the word moves */
      var btn = h('span', { 'class': 'g5-gloss', tabindex: '0', 'aria-label': m[0] + ': ' + G.meaning }, [m[0]]);
      var tip = h('span', { 'class': 'g5-gloss-tip', role: 'tooltip', 'aria-hidden': 'true', hidden: 'hidden' },
        [h('b', { text: G.word }), h('span', { text: G.meaning })]);
      document.body.appendChild(tip);
      function place() {
        tip.hidden = false; tip.classList.remove('below');
        var r = btn.getBoundingClientRect(), tw = tip.offsetWidth, th = tip.offsetHeight, vw = document.documentElement.clientWidth;
        var x = Math.max(8, Math.min(vw - tw - 8, r.left + r.width / 2 - tw / 2)), y = r.top - th - 10;
        if (y < 8) { y = r.bottom + 10; tip.classList.add('below'); }
        tip.style.left = x + 'px'; tip.style.top = y + 'px';
        tip.style.setProperty('--g5-arrow', Math.max(12, Math.min(tw - 12, r.left + r.width / 2 - x)) + 'px');
      }
      function hide() { tip.hidden = true; btn.classList.remove('open'); }
      btn.addEventListener('mouseenter', place);
      btn.addEventListener('mouseleave', function () { if (!btn.classList.contains('open')) hide(); });
      btn.addEventListener('focus', place);
      btn.addEventListener('blur', hide);
      btn.addEventListener('click', function (e) { e.stopPropagation(); if (btn.classList.toggle('open')) place(); else hide(); });
      btn.addEventListener('keydown', function (e) { if (e.key === 'Escape') hide(); });
      document.addEventListener('click', function (e) { if (!btn.contains(e.target)) hide(); });
      window.addEventListener('scroll', function () { if (!tip.hidden) hide(); }, { passive: true });
      node.parentNode.insertBefore(btn, after);
    });
  }

  /* ── 8. hint ladders on fill-ins (keyed by the answer) ────── */
  function buildHints() {
    if (!D.hints) return;
    document.querySelectorAll('input.fillin-input[data-answer]').forEach(function (inp) {
      var rungs = D.hints[(inp.getAttribute('data-answer') || '').toLowerCase()];
      if (!rungs || inp.nextElementSibling && inp.nextElementSibling.classList.contains('g5-hint-b')) return;
      var i = 0;
      var b = h('button', { type: 'button', 'class': 'g5-hint-b', 'aria-label': 'Get a hint' }, ['💡']);
      var tip = h('span', { 'class': 'g5-hint', 'aria-live': 'polite', hidden: 'hidden' });
      b.addEventListener('click', function () {
        tip.hidden = false; tip.textContent = rungs[Math.min(i, rungs.length - 1)];
        i++; if (i >= rungs.length) b.setAttribute('aria-label', 'Last hint shown');
      });
      afterNode(inp, b); afterNode(b, tip);
    });
  }

  /* ── 9. miss lines on the page's sort ─────────────────────── */
  function buildMiss() {
    if (!D.miss || typeof window.dropSortChip !== 'function') return;
    var orig = window.dropSortChip;
    var line = null;
    window.dropSortChip = function (col, name) {
      var chip = window.sortSelected;
      var word = chip ? chip.textContent.trim() : '';
      var right = chip ? chip.getAttribute('data-group') === name : true;
      var r = orig.apply(this, arguments);
      try {
        var sort = document.getElementById('spellSort') || (col && col.closest('.activity-body'));
        if (!line && sort) { line = h('p', { 'class': 'g5-miss', 'aria-live': 'polite' }); sort.parentNode.insertBefore(line, sort.nextSibling); }
        if (line) {
          if (!right && word && D.miss[word.toLowerCase()]) { line.textContent = D.miss[word.toLowerCase()]; line.hidden = false; }
          else if (right) line.hidden = true;
        }
      } catch (e) {}
      return r;
    };
  }

  /* ── 10. art plate ─────────────────────────────────────────── */
  function buildArt() {
    var A = D.art; if (!A || !A.file) return;
    var fig = h('figure', { 'class': 'g5-plate' });
    var img = h('img', { src: A.file, alt: A.alt || A.title, loading: 'lazy' });
    img.addEventListener('error', function () { fig.remove(); });
    fig.appendChild(h('div', { 'class': 'g5-plate-frame' }, [img]));
    var cap = h('figcaption');
    cap.innerHTML = '<div class="g5-plate-t">' + esc(A.title) + '</div>' +
      (A.look ? '<div class="g5-notice"><div class="g5-notice-h">👀 Look closely.</div><p class="g5-notice-q">What do you <b>notice</b>? What do you <b>wonder</b>?</p></div>' +
        '<details class="g5-look"><summary>' + esc(A.lookBtn || 'Tap to learn about this picture') + '</summary><p>' + esc(A.look) + '</p></details>' : '') +
      '<div class="g5-credit">' + esc([A.creator, A.date, A.license].filter(Boolean).join(' · ')) +
      (A.url ? ' · <a href="' + esc(A.url) + '" target="_blank" rel="noopener">source</a>' : '') + '</div>';
    fig.appendChild(cap);
    /* the plate is the lesson's frontispiece: right under the book quote, as in G3 and G4 */
    /* first thing on the Warm-Up tab, so it shows on Warm-Up only (Bethany, Nov 12 2026) */
    var wu = panel('warmup');
    if (wu) { fig.classList.add('g5-plate-top'); wu.insertBefore(fig, wu.firstChild); return; }
    var tab = A.tab || 'reading', p = panel(tab), li = p && p.querySelector(':scope > .g5-listen');
    if (li) afterNode(li, fig); else putTop(tab, fig);
  }

  /* ── 11. extra folded cards (e.g. Choctaw words in the book) ─ */
  function buildCards() {
    (D.cards || []).forEach(function (C) {
      var p = panel(C.tab || 'reading'); if (!p) return;
      var d = h('details', { 'class': 'g5-card g5-extra' });
      d.appendChild(h('summary', { html: esc(C.title) + ' <span class="g5-opt">optional · about ' + (C.min || 2) + ' min</span>' }));
      if (C.intro) d.appendChild(h('p', { text: C.intro }));
      var dl = h('dl', { 'class': 'g5-terms' });
      (C.items || []).forEach(function (it) {
        dl.appendChild(h('dt', { text: it.term }));
        var dd = h('dd');
        dd.innerHTML = esc(it.meaning) + (it.line ? '<span class="g5-terms-line">“' + esc(it.line) + '” <cite>' + esc(it.cite || '') + '</cite></span>' : '');
        dl.appendChild(dd);
      });
      d.appendChild(dl);
      if (C.note) d.appendChild(h('p', { 'class': 'g5-note', text: C.note }));
      var ref = C.after ? activityByTitle(C.after, p) : null;
      if (ref) afterNode(ref, d);
      else { var nw = nextWrap(C.tab || 'reading'); if (nw) p.insertBefore(d, nw); else p.appendChild(d); }
    });
  }

  /* ── 12. the week's word game: Stones in the River ────────── */
  function buildStones() {
    var G = D.game; if (!G || G.type !== 'stones' || !G.stones || !G.stones.length) return;
    var wkKey = 'stones.wk' + L.week;
    var st = store(wkKey) || {};
    var mine = st[L.day] || { done: [] };
    var stones = G.stones, idx = 0;
    while (idx < stones.length && mine.done.indexOf(idx) >= 0) idx++;

    var wrap = h('div', { 'class': 'activity g5-game' });
    wrap.innerHTML =
      '<div class="activity-head"><div class="activity-num g5-game-num" aria-hidden="true">🪨</div><div>' +
      '<div class="activity-title">' + esc(G.title || 'Stones in the River') + '</div>' +
      '<div class="activity-sub">' + esc(G.sub || 'Word game for this week') + '</div></div></div>';
    var body = h('div', { 'class': 'activity-body' });
    wrap.appendChild(body);

    var look = h('details', { 'class': 'g5-look' }, [h('summary', { text: '👀 What am I looking at?' }), h('p', { text: G.look })]);
    if (!mine.done.length) look.open = true;
    body.appendChild(look);
    if (G.how) body.appendChild(howLine(G.how));

    var scene = h('div', { 'class': 'g5-river', role: 'img', 'aria-label': 'A river with stepping stones. Each word you finish lights a stone.' });
    body.appendChild(scene);
    var stepBox = h('div', { 'class': 'g5-stone-step', 'aria-live': 'polite' });
    var wordBox = h('div', { 'class': 'g5-stone-word' });
    var ctrl = h('div', { 'class': 'g5-stone-ctrl' });
    var fb = h('p', { 'class': 'g5-stone-fb', 'aria-live': 'polite' });
    var tally = h('p', { 'class': 'g5-stone-tally' });
    [stepBox, wordBox, ctrl, fb, tally].forEach(function (n) { body.appendChild(n); });

    function drawRiver() {
      var n = stones.length, w = 900, hgt = 170, svg = '';
      svg += '<svg viewBox="0 0 ' + w + ' ' + hgt + '" preserveAspectRatio="xMidYMid meet" aria-hidden="true">' +
        '<defs><linearGradient id="g5w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5E7F86"/><stop offset="1" stop-color="#2F4E57"/></linearGradient>' +
        '<radialGradient id="g5s" cx=".4" cy=".35" r=".7"><stop offset="0" stop-color="#C9C2B4"/><stop offset=".7" stop-color="#8C8576"/><stop offset="1" stop-color="#5E5848"/></radialGradient>' +
        '<radialGradient id="g5g" cx=".4" cy=".35" r=".7"><stop offset="0" stop-color="#F6DE9A"/><stop offset=".7" stop-color="#C8A850"/><stop offset="1" stop-color="#8A6E25"/></radialGradient></defs>' +
        '<rect x="0" y="0" width="' + w + '" height="' + hgt + '" fill="url(#g5w)"/>' +
        '<path d="M0,0 L70,0 C60,40 85,90 62,' + hgt + ' L0,' + hgt + 'Z" fill="#6F6B3E"/><path d="M0,0 L55,0 C46,50 70,100 48,' + hgt + ' L0,' + hgt + 'Z" fill="#545A2E"/>' +
        '<path d="M' + w + ',0 L' + (w - 70) + ',0 C' + (w - 60) + ',40 ' + (w - 85) + ',90 ' + (w - 62) + ',' + hgt + ' L' + w + ',' + hgt + 'Z" fill="#6F6B3E"/><path d="M' + w + ',0 L' + (w - 55) + ',0 C' + (w - 46) + ',50 ' + (w - 70) + ',100 ' + (w - 48) + ',' + hgt + ' L' + w + ',' + hgt + 'Z" fill="#545A2E"/>';
      for (var r = 0; r < 7; r++) {
        var y = 18 + r * 22;
        svg += '<path class="g5-ripple" d="M90,' + y + ' C200,' + (y - 6) + ' 320,' + (y + 6) + ' 450,' + y + ' S700,' + (y - 6) + ' 810,' + y + '" stroke="rgba(255,255,255,.18)" stroke-width="2" fill="none"/>';
      }
      for (var i = 0; i < n; i++) {
        var x = 110 + i * ((w - 220) / Math.max(1, n - 1)), yy = 92 + (i % 2 ? -22 : 18);
        var lit = mine.done.indexOf(i) >= 0, cur = i === idx;
        svg += '<ellipse cx="' + x + '" cy="' + (yy + 10) + '" rx="40" ry="10" fill="rgba(0,0,0,.25)"/>' +
          '<ellipse class="g5-st' + (lit ? ' lit' : '') + (cur ? ' cur' : '') + '" cx="' + x + '" cy="' + yy + '" rx="38" ry="20" fill="url(#' + (lit ? 'g5g' : 'g5s') + ')" stroke="' + (cur ? '#FFF6D8' : 'rgba(0,0,0,.25)') + '" stroke-width="' + (cur ? 3 : 1) + '"/>';
      }
      svg += '</svg>';
      scene.innerHTML = svg;
      var total = 0, allDone = 0;
      Object.keys(st).forEach(function (k) { allDone += (st[k].done || []).length; });
      tally.textContent = 'Today: ' + mine.done.length + ' of ' + n + ' stones. This week: ' + allDone + ' stones crossed.';
    }

    function save() { st[L.day] = mine; store(wkKey, st); }

    function show() {
      drawRiver();
      fb.textContent = ''; ctrl.innerHTML = ''; wordBox.innerHTML = '';
      if (idx >= stones.length) {
        stepBox.innerHTML = '<b>You crossed the river.</b> ' + esc(G.doneLine || 'Every stone is lit.');
        var again = h('button', { type: 'button', 'class': 'g5-btn g5-btn-ghost' }, ['↺ Cross again']);
        again.addEventListener('click', function () { mine.done = []; idx = 0; save(); show(); });
        ctrl.appendChild(again);
        return;
      }
      var S = stones[idx];
      if (S.kind === 'root') rootStone(S); else syllableStone(S);
    }

    function lightStone() {
      if (mine.done.indexOf(idx) < 0) mine.done.push(idx);
      save();
      if (!REDUCED) chime();
      var next = h('button', { type: 'button', 'class': 'g5-btn' }, [idx + 1 < stones.length ? 'Next stone →' : 'Finish →']);
      next.addEventListener('click', function () { idx++; while (idx < stones.length && mine.done.indexOf(idx) >= 0) idx++; show(); setTimeout(function () { var f = ctrl.querySelector('button'); if (f) f.focus(); }, 30); });
      ctrl.innerHTML = ''; ctrl.appendChild(next);
      drawRiver();
    }

    function syllableStone(S) {
      var w = S.w, split = null;
      stepBox.innerHTML = '<span class="g5-stepn">Stone ' + (idx + 1) + ' of ' + stones.length + ' · Step 1 of 2</span> Say <b>' + esc(w) + '</b> slowly. Tap the gap where the first beat ends.';
      for (var i = 0; i < w.length; i++) {
        wordBox.appendChild(h('span', { 'class': 'g5-l', text: w[i] }));
        if (i < w.length - 1) {
          (function (cut) {
            var g = h('button', { type: 'button', 'class': 'g5-gap', 'aria-label': 'Split after ' + w.slice(0, cut) });
            g.addEventListener('click', function () {
              if (split !== null) return;
              if (cut === S.split) {
                split = cut;
                g.classList.add('g5-cut');
                wordBox.querySelectorAll('.g5-gap').forEach(function (x) { x.disabled = true; });
                fb.textContent = w.slice(0, cut) + ' · ' + w.slice(cut);
                stepTwo(S);
              } else {
                fb.textContent = S.gapHint || ('Not there. Say it slowly: ' + w.slice(0, S.split) + '... ' + w.slice(S.split) + '. Where did your voice stop?');
                g.classList.add('g5-shake'); setTimeout(function () { g.classList.remove('g5-shake'); }, 450);
              }
            });
            wordBox.appendChild(g);
          })(i + 1);
        }
      }
    }
    function stepTwo(S) {
      var first = S.w.slice(0, S.split);
      stepBox.innerHTML = '<span class="g5-stepn">Stone ' + (idx + 1) + ' of ' + stones.length + ' · Step 2 of 2</span> The first beat is <b>' + esc(first) + '</b>. What does it end on?';
      [['open', 'Open: ends on a vowel'], ['closed', 'Closed: ends on a consonant']].forEach(function (o) {
        var b = h('button', { type: 'button', 'class': 'g5-btn g5-btn-choice' }, [o[1]]);
        b.addEventListener('click', function () {
          if (o[0] === S.kind) {
            fb.textContent = S.why || ('Yes. ' + first + ' is ' + S.kind + '.');
            lightStone();
          } else {
            fb.textContent = S.miss || ('Look at the last letter of ' + first + '. Is it a vowel or a consonant? Then listen to the vowel sound.');
          }
        });
        ctrl.appendChild(b);
      });
    }

    function rootStone(S) {
      var w = S.w, sel = [];
      stepBox.innerHTML = '<span class="g5-stepn">Stone ' + (idx + 1) + ' of ' + stones.length + ' · Root stone</span> Tap the letters of the root hiding in <b>' + esc(w) + '</b>, then tap Check.';
      var letters = [];
      for (var i = 0; i < w.length; i++) {
        (function (k) {
          var b = h('button', { type: 'button', 'class': 'g5-lt', 'aria-pressed': 'false', 'aria-label': 'letter ' + w[k] }, [w[k]]);
          b.addEventListener('click', function () {
            var on = b.getAttribute('aria-pressed') !== 'true';
            b.setAttribute('aria-pressed', on ? 'true' : 'false');
          });
          letters.push(b); wordBox.appendChild(b);
        })(i);
      }
      var chk = h('button', { type: 'button', 'class': 'g5-btn' }, ['Check']);
      chk.addEventListener('click', function () {
        var picked = letters.map(function (b, i) { return b.getAttribute('aria-pressed') === 'true' ? i : -1; }).filter(function (i) { return i >= 0; });
        var ranges = [[S.at, S.root.length]].concat(S.alt || []);   // e.g. memory: mem or memor
        var ok = ranges.some(function (r) {
          return picked.length === r[1] && picked[0] === r[0] && picked.every(function (v, j) { return v === r[0] + j; });
        });
        if (ok) {
          letters.forEach(function (b) { b.disabled = true; });
          picked.forEach(function (i) { letters[i].classList.add('g5-rootlit'); });
          fb.textContent = S.why || ('Yes: ' + S.root + ' means ' + S.means + '.');
          lightStone();
        } else {
          fb.textContent = S.miss || ('Look for ' + S.family + '. Tap only those letters.');
        }
      });
      var clr = h('button', { type: 'button', 'class': 'g5-btn g5-btn-ghost' }, ['Clear']);
      clr.addEventListener('click', function () { letters.forEach(function (b) { b.setAttribute('aria-pressed', 'false'); }); fb.textContent = ''; });
      ctrl.appendChild(chk); ctrl.appendChild(clr);
    }

    var ctx;
    function chime() {
      try {
        ctx = ctx || new (window.AudioContext || window.webkitAudioContext)();
        [523.25, 659.25].forEach(function (f, i) {
          var o = ctx.createOscillator(), g = ctx.createGain();
          o.type = 'sine'; o.frequency.value = f;
          g.gain.setValueAtTime(0.0001, ctx.currentTime + i * 0.09);
          g.gain.exponentialRampToValueAtTime(0.12, ctx.currentTime + i * 0.09 + 0.02);
          g.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + i * 0.09 + 0.5);
          o.connect(g); g.connect(ctx.destination); o.start(ctx.currentTime + i * 0.09); o.stop(ctx.currentTime + i * 0.09 + 0.55);
        });
      } catch (e) {}
    }

    show();
    var ref = G.after ? activityByTitle(G.after, panel('words')) : null;
    if (ref) afterNode(ref, wrap);
    else { var nw = nextWrap('words'); if (nw) panel('words').insertBefore(wrap, nw); }
  }

  /* ── 12b. the week's word game: Footprints Forward (week 19) ──
     DATA.game = {type:'footprints', title, sub, after, look, how, doneLine,
                  steps:[{base, end:'ive'|'al'|'ic', word, why}]}.
     Each footprint holds a base word; pick the ending that builds the describing word.
     Storage oao.g5ela.steps.wk<NN> {day:{done:[i]}}. */
  function buildFootprints() {
    var G = D.game; if (!G || G.type !== 'footprints' || !G.steps || !G.steps.length) return;
    var wkKey = 'steps.wk' + L.week;
    var st = store(wkKey) || {};
    var mine = st[L.day] || { done: [] };
    var steps = G.steps, idx = 0;
    while (idx < steps.length && mine.done.indexOf(idx) >= 0) idx++;

    var wrap = h('div', { 'class': 'activity g5-game' });
    wrap.innerHTML =
      '<div class="activity-head"><div class="activity-num g5-game-num" aria-hidden="true">👣</div><div>' +
      '<div class="activity-title">' + esc(G.title || 'Footprints Forward') + '</div>' +
      '<div class="activity-sub">' + esc(G.sub || 'Word game for this week') + '</div></div></div>';
    var body = h('div', { 'class': 'activity-body' });
    wrap.appendChild(body);
    var look = h('details', { 'class': 'g5-look' }, [h('summary', { text: '👀 What am I looking at?' }), h('p', { text: G.look })]);
    if (!mine.done.length) look.open = true;
    body.appendChild(look);
    if (G.how) body.appendChild(howLine(G.how));
    var scene = h('div', { 'class': 'g5-river g5-snow', role: 'img', 'aria-label': 'A snowy road. Each word you build lights a footprint.' });
    body.appendChild(scene);
    var stepBox = h('div', { 'class': 'g5-stone-step', 'aria-live': 'polite' });
    var wordBox = h('div', { 'class': 'g5-stone-word g5-fp-word' });
    var ctrl = h('div', { 'class': 'g5-stone-ctrl' });
    var fb = h('p', { 'class': 'g5-stone-fb', 'aria-live': 'polite' });
    var tally = h('p', { 'class': 'g5-stone-tally' });
    [stepBox, wordBox, ctrl, fb, tally].forEach(function (n) { body.appendChild(n); });

    function foot(x, y, left, cls, fill, stroke) {   // a bare footprint: sole, then four toes
      var s = left ? -1 : 1, toes = '';
      [[-7, -27, 4.2], [0, -30, 4.6], [6, -28, 4], [10, -23, 3.3]].forEach(function (t) {
        toes += '<circle cx="' + (t[0] * s) + '" cy="' + t[1] + '" r="' + t[2] + '" fill="' + fill + '" stroke="' + stroke + '" stroke-width="1.5"/>';
      });
      return '<g class="' + cls + '" transform="translate(' + x + ',' + y + ') rotate(' + (s * 10) + ')">' +
        '<path d="M' + (-2 * s) + ',-22 C' + (10 * s) + ',-22 ' + (13 * s) + ',-8 ' + (10 * s) + ',4 C' + (8 * s) + ',14 ' + (8 * s) + ',22 ' + (1 * s) + ',24 C' + (-7 * s) + ',25 ' + (-9 * s) + ',16 ' + (-8 * s) + ',6 C' + (-7 * s) + ',-4 ' + (-12 * s) + ',-20 ' + (-2 * s) + ',-22Z" fill="' + fill + '" stroke="' + stroke + '" stroke-width="2"/>' + toes + '</g>';
    }
    function draw() {
      var n = steps.length, w = 900, hgt = 170, svg = '';
      svg += '<svg viewBox="0 0 ' + w + ' ' + hgt + '" preserveAspectRatio="xMidYMid meet" aria-hidden="true">' +
        '<defs><linearGradient id="g5sn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C9D3DC"/><stop offset="1" stop-color="#EEF2F5"/></linearGradient></defs>' +
        '<rect x="0" y="0" width="' + w + '" height="' + hgt + '" fill="url(#g5sn)"/>';
      for (var t = 0; t < 9; t++) {   // bare winter trees along the far edge
        var tx = 40 + t * 105, th = 46 + (t % 3) * 10;
        svg += '<path d="M' + tx + ',' + (th + 8) + ' L' + tx + ',8 M' + tx + ',24 L' + (tx - 14) + ',12 M' + tx + ',30 L' + (tx + 13) + ',16 M' + tx + ',40 L' + (tx - 10) + ',30" stroke="#6B6A62" stroke-width="3" fill="none" stroke-linecap="round"/>';
      }
      svg += '<path d="M0,128 C220,104 420,140 640,116 S860,112 900,120" stroke="rgba(120,135,150,.35)" stroke-width="34" fill="none"/>';
      for (var i = 0; i < n; i++) {
        var x = 90 + i * ((w - 180) / Math.max(1, n - 1)), y = 122 + (i % 2 ? -10 : 8);
        var lit = mine.done.indexOf(i) >= 0, cur = i === idx;
        svg += foot(x, y, i % 2 === 0, 'g5-fp' + (lit ? ' lit' : '') + (cur ? ' cur' : ''),
                    lit ? '#C8A850' : 'rgba(255,255,255,.65)', cur ? '#1A2D5A' : 'rgba(80,95,110,.55)');
      }
      svg += '</svg>';
      scene.innerHTML = svg;
      var allDone = 0;
      Object.keys(st).forEach(function (k) { allDone += (st[k].done || []).length; });
      tally.textContent = 'Today: ' + mine.done.length + ' of ' + n + ' footprints. This week: ' + allDone + (allDone === 1 ? ' step' : ' steps') + ' forward.';
    }
    function save() { st[L.day] = mine; store(wkKey, st); }
    function show() {
      draw(); fb.textContent = ''; ctrl.innerHTML = ''; wordBox.innerHTML = '';
      if (idx >= steps.length) {
        stepBox.innerHTML = '<b>Every footprint is lit.</b> ' + esc(G.doneLine || 'Come back tomorrow for more.');
        var again = h('button', { type: 'button', 'class': 'g5-btn g5-btn-ghost' }, ['↺ Walk it again']);
        again.addEventListener('click', function () { mine.done = []; idx = 0; save(); show(); });
        ctrl.appendChild(again); return;
      }
      var S = steps[idx], tries = 0;
      stepBox.innerHTML = '<span class="g5-stepn">Footprint ' + (idx + 1) + ' of ' + steps.length + '</span> Which ending turns <b>' + esc(S.base) + '</b> into a describing word?';
      wordBox.textContent = S.base + ' + ?';
      ['ive', 'al', 'ic'].forEach(function (e) {
        var b = h('button', { type: 'button', 'class': 'g5-btn g5-btn-choice' }, ['-' + e]);
        b.addEventListener('click', function () {
          if (e === S.end) {
            wordBox.textContent = S.word;
            fb.textContent = S.why || ('Yes: ' + S.base + ' + -' + e + ' = ' + S.word + '.');
            ctrl.querySelectorAll('button').forEach(function (x) { x.disabled = true; });
            if (mine.done.indexOf(idx) < 0) mine.done.push(idx);
            save(); if (!REDUCED) chime(); draw();
            var next = h('button', { type: 'button', 'class': 'g5-btn' }, [idx + 1 < steps.length ? 'Next footprint →' : 'Finish →']);
            next.addEventListener('click', function () { idx++; while (idx < steps.length && mine.done.indexOf(idx) >= 0) idx++; show(); setTimeout(function () { var f = ctrl.querySelector('button'); if (f) f.focus(); }, 30); });
            ctrl.appendChild(next);
          } else {
            tries++;
            b.disabled = true;
            fb.textContent = tries > 1 && S.miss ? S.miss : 'Say it: ' + S.base + e + '. Does that sound like a real word? Try another ending.';
          }
        });
        ctrl.appendChild(b);
      });
    }
    var ctx;
    function chime() {
      try {
        ctx = ctx || new (window.AudioContext || window.webkitAudioContext)();
        [392.0, 523.25].forEach(function (f, i) {
          var o = ctx.createOscillator(), g = ctx.createGain();
          o.type = 'sine'; o.frequency.value = f;
          g.gain.setValueAtTime(0.0001, ctx.currentTime + i * 0.09);
          g.gain.exponentialRampToValueAtTime(0.1, ctx.currentTime + i * 0.09 + 0.02);
          g.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + i * 0.09 + 0.45);
          o.connect(g); g.connect(ctx.destination); o.start(ctx.currentTime + i * 0.09); o.stop(ctx.currentTime + i * 0.09 + 0.5);
        });
      } catch (e) {}
    }
    show();
    var ref = G.after ? activityByTitle(G.after, panel('words')) : null;
    if (ref) afterNode(ref, wrap);
    else { var nw = nextWrap('words'); if (nw) panel('words').insertBefore(wrap, nw); }
  }

  /* ── 12c. the week's word game: Council Fire (week 20) ──────
     DATA.game = {type:'fire', title, sub, after, look, how, doneLine,
                  logs:[{a:'cour·age', sa:0, b:'cou·ra·geous', sb:1, why}]}  (sa/sb = index of the stressed beat)
     Tap the stressed beat in each word of a related pair; the log goes on the fire.
     Storage oao.g5ela.fire.wk<NN> {day:{done:[i]}}. */
  function buildFire() {
    var G = D.game; if (!G || G.type !== 'fire' || !G.logs || !G.logs.length) return;
    var wkKey = 'fire.wk' + L.week;
    var st = store(wkKey) || {};
    var mine = st[L.day] || { done: [] };
    var logs = G.logs, idx = 0;
    while (idx < logs.length && mine.done.indexOf(idx) >= 0) idx++;
    var wrap = h('div', { 'class': 'activity g5-game' });
    wrap.innerHTML =
      '<div class="activity-head"><div class="activity-num g5-game-num" aria-hidden="true">🔥</div><div>' +
      '<div class="activity-title">' + esc(G.title || 'Council Fire') + '</div>' +
      '<div class="activity-sub">' + esc(G.sub || 'Word game for this week') + '</div></div></div>';
    var body = h('div', { 'class': 'activity-body' });
    wrap.appendChild(body);
    var look = h('details', { 'class': 'g5-look' }, [h('summary', { text: '👀 What am I looking at?' }), h('p', { text: G.look })]);
    if (!mine.done.length) look.open = true;
    body.appendChild(look);
    if (G.how) body.appendChild(howLine(G.how));
    var scene = h('div', { 'class': 'g5-river g5-fire', role: 'img', 'aria-label': 'A campfire at night. Each pair of words you finish adds a log.' });
    body.appendChild(scene);
    var stepBox = h('div', { 'class': 'g5-stone-step', 'aria-live': 'polite' });
    var wordBox = h('div', { 'class': 'g5-fire-words' });
    var ctrl = h('div', { 'class': 'g5-stone-ctrl' });
    var fb = h('p', { 'class': 'g5-stone-fb', 'aria-live': 'polite' });
    var tally = h('p', { 'class': 'g5-stone-tally' });
    [stepBox, wordBox, ctrl, fb, tally].forEach(function (n) { body.appendChild(n); });

    function draw() {
      var allDone = 0;
      Object.keys(st).forEach(function (k) { allDone += (st[k].done || []).length; });
      var n = mine.done.length, w = 900, hgt = 170, cx = 450, svg = '';
      svg += '<svg viewBox="0 0 ' + w + ' ' + hgt + '" preserveAspectRatio="xMidYMid meet" aria-hidden="true">' +
        '<defs><radialGradient id="g5glow" cx=".5" cy=".75" r=".6"><stop offset="0" stop-color="rgba(255,170,60,' + (0.15 + 0.08 * n) + ')"/><stop offset="1" stop-color="rgba(255,170,60,0)"/></radialGradient>' +
        '<linearGradient id="g5night" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#16213A"/><stop offset="1" stop-color="#2B2A33"/></linearGradient></defs>' +
        '<rect width="' + w + '" height="' + hgt + '" fill="url(#g5night)"/><rect width="' + w + '" height="' + hgt + '" fill="url(#g5glow)"/>';
      for (var s = 0; s < 26; s++) svg += '<circle cx="' + ((s * 137) % w) + '" cy="' + (8 + (s * 53) % 60) + '" r="1.2" fill="rgba(255,255,255,.55)"/>';
      for (var t = 0; t < 8; t++) {   // pines on the far edge
        var tx = 40 + t * 120 + (t > 3 ? 60 : 0), th = 70 + (t % 3) * 14;
        if (Math.abs(tx - cx) < 120) continue;
        svg += '<path d="M' + tx + ',' + (150 - th) + ' L' + (tx - 22) + ',150 L' + (tx + 22) + ',150 Z" fill="#101826"/>';
      }
      svg += '<ellipse cx="' + cx + '" cy="152" rx="160" ry="10" fill="rgba(0,0,0,.35)"/>';
      for (var i = 0; i < logs.length; i++) {   // one log per pair; lit logs are on the fire
        var on = mine.done.indexOf(i) >= 0, ang = (i % 2 ? -1 : 1) * (8 + i * 4);
        var lx = on ? cx : 120 + i * 30, ly = on ? 146 - Math.floor(mine.done.indexOf(i) / 2) * 9 : 160;
        svg += '<g transform="translate(' + lx + ',' + ly + ') rotate(' + (on ? ang : 0) + ')"><rect x="-46" y="-6" width="92" height="12" rx="6" fill="' + (on ? '#6B4426' : '#4A3423') + '" stroke="#2C1D12"/><circle cx="46" cy="0" r="6" fill="#A87A4E"/></g>';
      }
      if (n) {   // flames grow with the logs
        var fh = 28 + n * 12;
        svg += '<path class="g5-flame" d="M' + (cx - 30) + ',140 C' + (cx - 34) + ',' + (140 - fh * .5) + ' ' + (cx - 6) + ',' + (140 - fh * .7) + ' ' + cx + ',' + (140 - fh) + ' C' + (cx + 8) + ',' + (140 - fh * .65) + ' ' + (cx + 36) + ',' + (140 - fh * .5) + ' ' + (cx + 30) + ',140 Z" fill="#F29A2E"/>' +
               '<path d="M' + (cx - 15) + ',140 C' + (cx - 16) + ',' + (140 - fh * .35) + ' ' + (cx - 2) + ',' + (140 - fh * .5) + ' ' + cx + ',' + (140 - fh * .7) + ' C' + (cx + 4) + ',' + (140 - fh * .45) + ' ' + (cx + 18) + ',' + (140 - fh * .35) + ' ' + (cx + 15) + ',140 Z" fill="#FFD36B"/>';
      }
      svg += '</svg>';
      scene.innerHTML = svg;
      tally.textContent = 'Today: ' + n + ' of ' + logs.length + ' logs. This week: ' + allDone + (allDone === 1 ? ' log' : ' logs') + ' on the fire.';
    }
    function save() { st[L.day] = mine; store(wkKey, st); }
    function beats(word, right, label, onDone) {
      var row = h('div', { 'class': 'g5-fire-row' }), parts = word.split('·'), done = false;
      row.appendChild(h('span', { 'class': 'g5-fire-label', text: label }));
      parts.forEach(function (p, k) {
        var b = h('button', { type: 'button', 'class': 'g5-beat', 'aria-label': 'Stress on ' + p }, [p]);
        b.addEventListener('click', function () {
          if (done) return;
          if (k === right) {
            done = true; b.classList.add('g5-beat-on');
            row.querySelectorAll('.g5-beat').forEach(function (x) { x.disabled = true; });
            onDone();
          } else {
            fb.textContent = 'Say it out loud and lean hard on ' + p.toUpperCase() + '. Does that sound like English? Try another beat.';
            b.classList.add('g5-shake'); setTimeout(function () { b.classList.remove('g5-shake'); }, 450);
          }
        });
        row.appendChild(b);
      });
      wordBox.appendChild(row);
    }
    function show() {
      draw(); fb.textContent = ''; ctrl.innerHTML = ''; wordBox.innerHTML = '';
      if (idx >= logs.length) {
        stepBox.innerHTML = '<b>Every log is on the fire.</b> ' + esc(G.doneLine || 'Come back tomorrow for more.');
        var again = h('button', { type: 'button', 'class': 'g5-btn g5-btn-ghost' }, ['↺ Build it again']);
        again.addEventListener('click', function () { mine.done = []; idx = 0; save(); show(); });
        ctrl.appendChild(again); return;
      }
      var S = logs[idx], got = 0;
      stepBox.innerHTML = '<span class="g5-stepn">Log ' + (idx + 1) + ' of ' + logs.length + '</span> Say each word. Tap the beat you say the strongest.';
      function both() {
        got++;
        if (got < 2) { fb.textContent = 'Good. Now the second word.'; return; }
        fb.textContent = S.why || 'Yes. The stress moved.';
        if (mine.done.indexOf(idx) < 0) mine.done.push(idx);
        save(); if (!REDUCED) chime(); draw();
        var next = h('button', { type: 'button', 'class': 'g5-btn' }, [idx + 1 < logs.length ? 'Next log →' : 'Finish →']);
        next.addEventListener('click', function () { idx++; while (idx < logs.length && mine.done.indexOf(idx) >= 0) idx++; show(); setTimeout(function () { var f = ctrl.querySelector('button'); if (f) f.focus(); }, 30); });
        ctrl.appendChild(next);
      }
      beats(S.a, S.sa, '1', both);
      beats(S.b, S.sb, '2', both);
    }
    var ctx;
    function chime() {
      try {
        ctx = ctx || new (window.AudioContext || window.webkitAudioContext)();
        [329.63, 440].forEach(function (f, i) {
          var o = ctx.createOscillator(), g = ctx.createGain();
          o.type = 'sine'; o.frequency.value = f;
          g.gain.setValueAtTime(0.0001, ctx.currentTime + i * 0.1);
          g.gain.exponentialRampToValueAtTime(0.1, ctx.currentTime + i * 0.1 + 0.02);
          g.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + i * 0.1 + 0.5);
          o.connect(g); g.connect(ctx.destination); o.start(ctx.currentTime + i * 0.1); o.stop(ctx.currentTime + i * 0.1 + 0.55);
        });
      } catch (e) {}
    }
    show();
    var ref = G.after ? activityByTitle(G.after, panel('words')) : null;
    if (ref) afterNode(ref, wrap);
    else { var nw = nextWrap('words'); if (nw) panel('words').insertBefore(wrap, nw); }
  }

  /* ── 12d. the week's word game: The Spyglass (week 21) ──────
     DATA.game = {type:'spy', title, sub, after, look, how, doneLine,
                  words:[{w:'visitor', root:'vis', part:'vis', opts:['…','…','…'], ok:1, why}]}
     root is 'vis' (vis/vid = see) or 'spect' (look); part = the letters to light up in the word.
     Step 1: tap the root the word carries. Step 2: tap its meaning. Each word found adds a star.
     Storage oao.g5ela.spy.wk<NN> {day:{done:[i]}}. */
  function buildSpyglass() {
    var G = D.game; if (!G || G.type !== 'spy' || !G.words || !G.words.length) return;
    var wkKey = 'spy.wk' + L.week;
    var st = store(wkKey) || {};
    var mine = st[L.day] || { done: [] };
    var W = G.words, idx = 0;
    while (idx < W.length && mine.done.indexOf(idx) >= 0) idx++;
    var wrap = h('div', { 'class': 'activity g5-game' });
    wrap.innerHTML =
      '<div class="activity-head"><div class="activity-num g5-game-num" aria-hidden="true">🔭</div><div>' +
      '<div class="activity-title">' + esc(G.title || 'The Spyglass') + '</div>' +
      '<div class="activity-sub">' + esc(G.sub || 'Word game for this week') + '</div></div></div>';
    var body = h('div', { 'class': 'activity-body' });
    wrap.appendChild(body);
    var look = h('details', { 'class': 'g5-look' }, [h('summary', { text: '👀 What am I looking at?' }), h('p', { text: G.look })]);
    if (!mine.done.length) look.open = true;
    body.appendChild(look);
    if (G.how) body.appendChild(howLine(G.how));
    var scene = h('div', { 'class': 'g5-river g5-spy', role: 'img', 'aria-label': 'A brass spyglass pointed at the night sky. Each word you find adds a star.' });
    body.appendChild(scene);
    var stepBox = h('div', { 'class': 'g5-stone-step', 'aria-live': 'polite' });
    var pick = h('div', { 'class': 'g5-spy-pick' });
    var ctrl = h('div', { 'class': 'g5-stone-ctrl' });
    var fb = h('p', { 'class': 'g5-stone-fb', 'aria-live': 'polite' });
    var tally = h('p', { 'class': 'g5-stone-tally' });
    [stepBox, pick, ctrl, fb, tally].forEach(function (n) { body.appendChild(n); });

    function lensWord(S, lit) {
      var w = S.w, at = lit ? w.indexOf(S.part) : -1;
      if (at < 0) return esc(w);
      return esc(w.slice(0, at)) + '<tspan class="g5-spy-lit">' + esc(S.part) + '</tspan>' + esc(w.slice(at + S.part.length));
    }
    function draw(S, lit) {
      var allDone = 0;
      Object.keys(st).forEach(function (k) { allDone += (st[k].done || []).length; });
      var n = mine.done.length, w = 900, hgt = 190, cx = 560, cy = 95, r = 78, svg = '';
      svg += '<svg viewBox="0 0 ' + w + ' ' + hgt + '" preserveAspectRatio="xMidYMid meet" aria-hidden="true">' +
        '<defs><linearGradient id="g5sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#121B33"/><stop offset="1" stop-color="#28324F"/></linearGradient>' +
        '<linearGradient id="g5brass" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E2C27A"/><stop offset=".5" stop-color="#B38A3E"/><stop offset="1" stop-color="#7D5E26"/></linearGradient>' +
        '<clipPath id="g5lens"><circle cx="' + cx + '" cy="' + cy + '" r="' + (r - 8) + '"/></clipPath></defs>' +
        '<rect width="' + w + '" height="' + hgt + '" fill="url(#g5sky)"/>';
      for (var s = 0; s < 22; s++) svg += '<circle cx="' + ((s * 151) % w) + '" cy="' + (10 + (s * 47) % 120) + '" r="1" fill="rgba(255,255,255,.35)"/>';
      svg += '<path d="M0,170 C140,150 260,160 380,168 L380,190 L0,190 Z" fill="#0D1426"/>';
      // the spyglass: three brass tubes from the lower left up to the lens
      svg += '<g transform="rotate(-12 ' + cx + ' ' + cy + ')">' +
        '<rect x="' + (cx - r - 300) + '" y="' + (cy - 16) + '" width="120" height="32" rx="5" fill="url(#g5brass)" stroke="#5C4419"/>' +
        '<rect x="' + (cx - r - 185) + '" y="' + (cy - 24) + '" width="110" height="48" rx="5" fill="url(#g5brass)" stroke="#5C4419"/>' +
        '<rect x="' + (cx - r - 80) + '" y="' + (cy - 34) + '" width="90" height="68" rx="6" fill="url(#g5brass)" stroke="#5C4419"/></g>';
      svg += '<circle cx="' + cx + '" cy="' + cy + '" r="' + r + '" fill="url(#g5brass)" stroke="#5C4419" stroke-width="2"/>' +
        '<circle cx="' + cx + '" cy="' + cy + '" r="' + (r - 8) + '" fill="#F6F1E3"/>';
      svg += '<g clip-path="url(#g5lens)">';
      for (var i = 0; i < W.length; i++) {   // a star in the lens for each word found today
        if (mine.done.indexOf(i) < 0) continue;
        var sx = cx - 50 + (i * 37) % 100, sy = cy - 50 + (i * 23) % 26;
        svg += '<path d="M' + sx + ',' + (sy - 6) + ' L' + (sx + 2) + ',' + (sy - 2) + ' L' + (sx + 6) + ',' + sy + ' L' + (sx + 2) + ',' + (sy + 2) + ' L' + sx + ',' + (sy + 6) + ' L' + (sx - 2) + ',' + (sy + 2) + ' L' + (sx - 6) + ',' + sy + ' L' + (sx - 2) + ',' + (sy - 2) + ' Z" fill="#D9A93E"/>';
      }
      if (S) svg += '<text x="' + cx + '" y="' + (cy + 12) + '" text-anchor="middle" class="g5-spy-word">' + lensWord(S, lit) + '</text>';
      else svg += '<text x="' + cx + '" y="' + (cy + 8) + '" text-anchor="middle" class="g5-spy-done">' + n + ' ★</text>';
      svg += '</g></svg>';
      scene.innerHTML = svg;
      tally.textContent = 'Today: ' + n + ' of ' + W.length + (W.length === 1 ? ' word' : ' words') + '. This week: ' + allDone + (allDone === 1 ? ' star' : ' stars') + ' in the spyglass.';
    }
    function save() { st[L.day] = mine; store(wkKey, st); }
    function shake(b) { b.classList.add('g5-shake'); setTimeout(function () { b.classList.remove('g5-shake'); }, 450); }
    function show() {
      fb.textContent = ''; ctrl.innerHTML = ''; pick.innerHTML = '';
      if (idx >= W.length) {
        draw(null);
        stepBox.innerHTML = '<b>Every word is in focus.</b> ' + esc(G.doneLine || 'Come back tomorrow for more.');
        var again = h('button', { type: 'button', 'class': 'g5-btn g5-btn-ghost' }, ['↺ Look again']);
        again.addEventListener('click', function () { mine.done = []; idx = 0; save(); show(); });
        ctrl.appendChild(again); return;
      }
      var S = W[idx];
      draw(S, false);
      stepBox.innerHTML = '<span class="g5-stepn">Word ' + (idx + 1) + ' of ' + W.length + '</span> Which root is inside this word?';
      [['vis', 'vis / vid · see'], ['spect', 'spect · look']].forEach(function (R) {
        var b = h('button', { type: 'button', 'class': 'g5-beat g5-spy-root' }, [R[1]]);
        b.addEventListener('click', function () {
          if (R[0] !== S.root) { fb.textContent = 'Look closely at the letters. Find ' + (S.root === 'vis' ? 'v-i-s or v-i-d' : 's-p-e-c-t') + ' hiding in the word.'; shake(b); return; }
          b.classList.add('g5-beat-on'); draw(S, true); meanings(S);
        });
        pick.appendChild(b);
      });
    }
    function meanings(S) {
      pick.innerHTML = ''; fb.textContent = '';
      stepBox.innerHTML = '<span class="g5-stepn">Word ' + (idx + 1) + ' of ' + W.length + '</span> The root is lit. Now tap what <b>' + esc(S.w) + '</b> means.';
      S.opts.forEach(function (o, k) {
        var b = h('button', { type: 'button', 'class': 'g5-spy-opt' }, [o]);
        b.addEventListener('click', function () {
          if (k !== S.ok) { fb.textContent = 'Not quite. The root means ' + (S.root === 'vis' ? 'see' : 'look') + '. Which meaning has seeing or looking in it?'; shake(b); return; }
          b.classList.add('g5-spy-on'); pick.querySelectorAll('button').forEach(function (x) { x.disabled = true; });
          fb.textContent = S.why || 'Yes.';
          if (mine.done.indexOf(idx) < 0) mine.done.push(idx);
          save(); draw(S, true);
          var next = h('button', { type: 'button', 'class': 'g5-btn' }, [idx + 1 < W.length ? 'Next word →' : 'Finish →']);
          next.addEventListener('click', function () { idx++; while (idx < W.length && mine.done.indexOf(idx) >= 0) idx++; show(); setTimeout(function () { var f = pick.querySelector('button') || ctrl.querySelector('button'); if (f) f.focus(); }, 30); });
          ctrl.appendChild(next);
        });
        pick.appendChild(b);
      });
    }
    show();
    var ref = G.after ? activityByTitle(G.after, panel('words')) : null;
    if (ref) afterNode(ref, wrap);
    else { var nw = nextWrap('words'); if (nw) panel('words').insertBefore(wrap, nw); }
  }

  /* ── 12e. the week's word game: Light the Lanterns (week 22) ──
     DATA.game = {type:'lantern', title, sub, after, look, how, doneLine,
                  words:[{w:'photocopy', parts:['photo','copy'], decoys:['graph'], means:'…', clue:'photo = light', why}]}
     Tap the word parts in order to build the word that matches the meaning; a finished word lights
     its lantern. A tile that does not come next shakes and says what to look for.
     Storage oao.g5ela.lantern.wk<NN> {day:{done:[i]}}. */
  function buildLanterns() {
    var G = D.game; if (!G || G.type !== 'lantern' || !G.words || !G.words.length) return;
    var wkKey = 'lantern.wk' + L.week;
    var st = store(wkKey) || {};
    var mine = st[L.day] || { done: [] };
    var W = G.words, idx = 0;
    while (idx < W.length && mine.done.indexOf(idx) >= 0) idx++;
    var wrap = h('div', { 'class': 'activity g5-game' });
    wrap.innerHTML =
      '<div class="activity-head"><div class="activity-num g5-game-num" aria-hidden="true">🏮</div><div>' +
      '<div class="activity-title">' + esc(G.title || 'Light the Lanterns') + '</div>' +
      '<div class="activity-sub">' + esc(G.sub || 'Word game for this week') + '</div></div></div>';
    var body = h('div', { 'class': 'activity-body' });
    wrap.appendChild(body);
    var look = h('details', { 'class': 'g5-look' }, [h('summary', { text: '👀 What am I looking at?' }), h('p', { text: G.look })]);
    if (!mine.done.length) look.open = true;
    body.appendChild(look);
    if (G.how) body.appendChild(howLine(G.how));
    var scene = h('div', { 'class': 'g5-river g5-lan', role: 'img', 'aria-label': 'Lanterns hang from a branch in the dark woods. Each word you build lights one.' });
    body.appendChild(scene);
    var stepBox = h('div', { 'class': 'g5-stone-step', 'aria-live': 'polite' });
    var slots = h('div', { 'class': 'g5-lan-slots', 'aria-live': 'polite' });
    var pick = h('div', { 'class': 'g5-lan-pick' });
    var ctrl = h('div', { 'class': 'g5-stone-ctrl' });
    var fb = h('p', { 'class': 'g5-stone-fb', 'aria-live': 'polite' });
    var tally = h('p', { 'class': 'g5-stone-tally' });
    [stepBox, slots, pick, ctrl, fb, tally].forEach(function (n) { body.appendChild(n); });

    function draw(cur) {
      var allDone = 0;
      Object.keys(st).forEach(function (k) { allDone += (st[k].done || []).length; });
      var n = mine.done.length, w = 900, hgt = 190, svg = '';
      svg += '<svg viewBox="0 0 ' + w + ' ' + hgt + '" preserveAspectRatio="xMidYMid meet" aria-hidden="true">' +
        '<defs><linearGradient id="g5lsky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#101829"/><stop offset="1" stop-color="#222C44"/></linearGradient>' +
        '<radialGradient id="g5glow"><stop offset="0" stop-color="#FFE3A0" stop-opacity=".9"/><stop offset=".45" stop-color="#E9B44C" stop-opacity=".45"/><stop offset="1" stop-color="#E9B44C" stop-opacity="0"/></radialGradient></defs>' +
        '<rect width="' + w + '" height="' + hgt + '" fill="url(#g5lsky)"/>';
      for (var s = 0; s < 26; s++) svg += '<circle cx="' + ((s * 173) % w) + '" cy="' + (8 + (s * 41) % 60) + '" r="1" fill="rgba(255,255,255,.3)"/>';
      for (var t = 0; t < 7; t++) { var tx = 30 + t * 140; svg += '<path d="M' + tx + ',190 L' + (tx + 22) + ',120 L' + (tx + 44) + ',190 Z" fill="#0B1220"/>'; }
      svg += '<path d="M40,34 C260,60 640,60 860,30" stroke="#3A2A18" stroke-width="7" fill="none" stroke-linecap="round"/>';
      var gap = 760 / (W.length + 1);
      for (var i = 0; i < W.length; i++) {
        var lx = 70 + gap * (i + 1), ly = 52 + Math.sin((i + 1) / (W.length + 1) * Math.PI) * 10, lit = mine.done.indexOf(i) >= 0, on = i === cur;
        svg += '<line x1="' + lx + '" y1="' + (ly - 8) + '" x2="' + lx + '" y2="' + (ly + 22) + '" stroke="#6B5530" stroke-width="2"/>';
        if (lit) svg += '<circle cx="' + lx + '" cy="' + (ly + 56) + '" r="62" fill="url(#g5glow)"/>';
        svg += '<rect x="' + (lx - 16) + '" y="' + (ly + 22) + '" width="32" height="8" rx="2" fill="#7D5E26"/>' +
          '<path d="M' + (lx - 20) + ',' + (ly + 30) + ' L' + (lx + 20) + ',' + (ly + 30) + ' L' + (lx + 16) + ',' + (ly + 82) + ' L' + (lx - 16) + ',' + (ly + 82) + ' Z" fill="' + (lit ? '#F4CF73' : '#2F3850') + '" stroke="' + (on ? '#E9B44C' : '#7D5E26') + '" stroke-width="' + (on ? 3 : 2) + '"/>' +
          '<rect x="' + (lx - 18) + '" y="' + (ly + 82) + '" width="36" height="7" rx="2" fill="#7D5E26"/>';
        if (lit) svg += '<ellipse cx="' + lx + '" cy="' + (ly + 62) + '" rx="5" ry="9" fill="#FFF4D2"/>';
      }
      svg += '</svg>';
      scene.innerHTML = svg;
      tally.textContent = 'Today: ' + n + ' of ' + W.length + (W.length === 1 ? ' lantern' : ' lanterns') + ' lit. This week: ' + allDone + '.';
    }
    function save() { st[L.day] = mine; store(wkKey, st); }
    function shake(b) { b.classList.add('g5-shake'); setTimeout(function () { b.classList.remove('g5-shake'); }, 450); }
    function shuffled(a) {   // fixed order per word so a reload looks the same
      var out = a.slice(), seed = 7;
      for (var i = out.length - 1; i > 0; i--) { seed = (seed * 31 + i * 17) % 101; var j = seed % (i + 1); var tmp = out[i]; out[i] = out[j]; out[j] = tmp; }
      if (out.length > 1 && out[0] === a[0]) out.push(out.shift());   // never start with the right first part
      return out;
    }
    function show() {
      fb.textContent = ''; ctrl.innerHTML = ''; pick.innerHTML = ''; slots.innerHTML = '';
      if (idx >= W.length) {
        draw(-1);
        stepBox.innerHTML = '<b>Every lantern is lit.</b> ' + esc(G.doneLine || 'Come back tomorrow for more.');
        var again = h('button', { type: 'button', 'class': 'g5-btn g5-btn-ghost' }, ['↺ Build them again']);
        again.addEventListener('click', function () { mine.done = []; idx = 0; save(); show(); });
        ctrl.appendChild(again); return;
      }
      var S = W[idx], got = 0;
      draw(idx);
      stepBox.innerHTML = '<span class="g5-stepn">Lantern ' + (idx + 1) + ' of ' + W.length + '</span> Build the word that means: <b>' + esc(S.means) + '</b>' +
        (S.clue ? '<br><span class="g5-lan-clue">Part you know: ' + esc(S.clue) + '</span>' : '');
      var boxes = S.parts.map(function () { var b = h('span', { 'class': 'g5-lan-slot' }, ['?']); slots.appendChild(b); return b; });
      shuffled(S.parts.concat(S.decoys || [])).forEach(function (p) {
        var b = h('button', { type: 'button', 'class': 'g5-beat g5-lan-tile' }, [p]);
        b.addEventListener('click', function () {
          if (p !== S.parts[got]) {
            fb.textContent = got === 0 ? 'Not the first part. Which part of the meaning comes first in the word?' : 'That part does not come next. Say what you have built so far, then listen for the next part.';
            shake(b); return;
          }
          boxes[got].textContent = p; boxes[got].classList.add('g5-lan-full'); b.disabled = true; b.classList.add('g5-beat-on'); got++; fb.textContent = '';
          if (got < S.parts.length) return;
          pick.querySelectorAll('button').forEach(function (x) { x.disabled = true; });
          if (mine.done.indexOf(idx) < 0) mine.done.push(idx);
          save(); draw(idx);
          fb.innerHTML = '<b>' + esc(S.w) + '</b>. ' + esc(S.why || 'The lantern is lit.');
          var next = h('button', { type: 'button', 'class': 'g5-btn' }, [idx + 1 < W.length ? 'Next lantern →' : 'Finish →']);
          next.addEventListener('click', function () { idx++; while (idx < W.length && mine.done.indexOf(idx) >= 0) idx++; show(); setTimeout(function () { var f = pick.querySelector('button') || ctrl.querySelector('button'); if (f) f.focus(); }, 30); });
          ctrl.appendChild(next);
        });
        pick.appendChild(b);
      });
    }
    show();
    var ref = G.after ? activityByTitle(G.after, panel('words')) : null;
    if (ref) afterNode(ref, wrap);
    else { var nw = nextWrap('words'); if (nw) panel('words').insertBefore(wrap, nw); }
  }

  /* ── 12f. the week's word game: Raise Your Voice (week 23) ──
     DATA.game = {type:'voice', title, sub, after, look, how, doneLine,
                  lines:[{who:'A council member', before:'…', after:'…', opts:['advocate','predict','revoke'], ok:0, hint:'…', why:'…'}]}
     A cloze: read a line someone in the book's world could say, tap the voc/voke or dict word that fits
     the blank; the line rings out and a gold voice ring rises over the camp. A wrong word shakes and says
     what to look for. Storage oao.g5ela.voice.wk<NN> {day:{done:[i]}}. */
  function buildVoice() {
    var G = D.game; if (!G || G.type !== 'voice' || !G.lines || !G.lines.length) return;
    var wkKey = 'voice.wk' + L.week;
    var st = store(wkKey) || {};
    var mine = st[L.day] || { done: [] };
    var W = G.lines, idx = 0;
    while (idx < W.length && mine.done.indexOf(idx) >= 0) idx++;
    var wrap = h('div', { 'class': 'activity g5-game' });
    wrap.innerHTML =
      '<div class="activity-head"><div class="activity-num g5-game-num" aria-hidden="true">📣</div><div>' +
      '<div class="activity-title">' + esc(G.title || 'Raise Your Voice') + '</div>' +
      '<div class="activity-sub">' + esc(G.sub || 'Word game for this week') + '</div></div></div>';
    var body = h('div', { 'class': 'activity-body' });
    wrap.appendChild(body);
    var look = h('details', { 'class': 'g5-look' }, [h('summary', { text: '👀 What am I looking at?' }), h('p', { text: G.look })]);
    if (!mine.done.length) look.open = true;
    body.appendChild(look);
    if (G.how) body.appendChild(howLine(G.how));
    var scene = h('div', { 'class': 'g5-river g5-voice', role: 'img', 'aria-label': 'A camp in the snowy woods at dusk. Each line you finish sends a gold voice ring into the sky.' });
    body.appendChild(scene);
    var stepBox = h('div', { 'class': 'g5-stone-step', 'aria-live': 'polite' });
    var card = h('p', { 'class': 'g5-voice-line', 'aria-live': 'polite' });
    var pick = h('div', { 'class': 'g5-voice-pick' });
    var ctrl = h('div', { 'class': 'g5-stone-ctrl' });
    var fb = h('p', { 'class': 'g5-stone-fb', 'aria-live': 'polite' });
    var tally = h('p', { 'class': 'g5-stone-tally' });
    [stepBox, card, pick, ctrl, fb, tally].forEach(function (n) { body.appendChild(n); });

    function draw() {
      var allDone = 0;
      Object.keys(st).forEach(function (k) { allDone += (st[k].done || []).length; });
      var n = mine.done.length, w = 900, hgt = 190, cx = 450, svg = '';
      svg += '<svg viewBox="0 0 ' + w + ' ' + hgt + '" preserveAspectRatio="xMidYMid meet" aria-hidden="true">' +
        '<defs><linearGradient id="g5vsky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1A2340"/><stop offset="1" stop-color="#4A4560"/></linearGradient></defs>' +
        '<rect width="' + w + '" height="' + hgt + '" fill="url(#g5vsky)"/>';
      for (var s = 0; s < 24; s++) svg += '<circle cx="' + ((s * 167) % w) + '" cy="' + (8 + (s * 37) % 70) + '" r="1" fill="rgba(255,255,255,.3)"/>';
      for (var r = 0; r < W.length; r++) {   // one ring per line, lit when that line is done today
        var on = mine.done.indexOf(r) >= 0, rr = 46 + r * 26;
        svg += '<path d="M' + (cx - rr) + ',150 A' + rr + ',' + (rr * 0.9) + ' 0 0 1 ' + (cx + rr) + ',150" fill="none" stroke="' + (on ? '#E9B44C' : 'rgba(255,255,255,.12)') + '" stroke-width="' + (on ? 4 : 2) + '" stroke-linecap="round"/>';
      }
      for (var t = 0; t < 9; t++) { var tx = t * 110 - 20; if (tx > cx - 160 && tx < cx + 120) continue; svg += '<path d="M' + tx + ',165 L' + (tx + 24) + ',92 L' + (tx + 48) + ',165 Z" fill="#141B2E"/>'; }
      svg += '<path d="M0,160 C200,148 700,148 900,160 L900,190 L0,190 Z" fill="#E8ECF2"/>';
      for (var p = -2; p <= 2; p++) {   // people sitting together around the circle
        var px = cx + p * 34, py = 158 - Math.abs(p) * 2;
        svg += '<circle cx="' + px + '" cy="' + (py - 20) + '" r="7" fill="#222A3D"/><path d="M' + (px - 11) + ',' + py + ' Q' + px + ',' + (py - 22) + ' ' + (px + 11) + ',' + py + ' Z" fill="#222A3D"/>';
      }
      svg += '</svg>';
      scene.innerHTML = svg;
      tally.textContent = 'Today: ' + n + ' of ' + W.length + (W.length === 1 ? ' voice' : ' voices') + ' raised. This week: ' + allDone + '.';
    }
    function save() { st[L.day] = mine; store(wkKey, st); }
    function shake(b) { b.classList.add('g5-shake'); setTimeout(function () { b.classList.remove('g5-shake'); }, 450); }
    function line(S, word) {
      return (S.who ? '<span class="g5-voice-who">' + esc(S.who) + ':</span> ' : '') + '&ldquo;' + esc(S.before) +
        (word ? '<b class="g5-voice-fill">' + esc(word) + '</b>' : '<span class="g5-voice-blank">______</span>') + esc(S.after) + '&rdquo;';
    }
    function show() {
      fb.textContent = ''; ctrl.innerHTML = ''; pick.innerHTML = ''; card.innerHTML = '';
      if (idx >= W.length) {
        draw();
        stepBox.innerHTML = '<b>Every voice is raised.</b> ' + esc(G.doneLine || 'Come back tomorrow for more.');
        var again = h('button', { type: 'button', 'class': 'g5-btn g5-btn-ghost' }, ['↺ Say them again']);
        again.addEventListener('click', function () { mine.done = []; idx = 0; save(); show(); });
        ctrl.appendChild(again); return;
      }
      var S = W[idx];
      draw();
      stepBox.innerHTML = '<span class="g5-stepn">Line ' + (idx + 1) + ' of ' + W.length + '</span> Read the whole line. Tap the word that fits the blank.';
      card.innerHTML = line(S, null);
      S.opts.forEach(function (o, k) {
        var b = h('button', { type: 'button', 'class': 'g5-beat g5-voice-opt' }, [o]);
        b.addEventListener('click', function () {
          if (k !== S.ok) { fb.textContent = S.hint || 'Read the line again. Does it need a word about voice and calling (voc, voke) or about saying (dict)?'; shake(b); return; }
          b.classList.add('g5-beat-on'); pick.querySelectorAll('button').forEach(function (x) { x.disabled = true; });
          card.innerHTML = line(S, o);
          if (mine.done.indexOf(idx) < 0) mine.done.push(idx);
          save(); draw();
          fb.innerHTML = '<b>' + esc(o) + '</b>. ' + esc(S.why || 'That word fits.');
          var next = h('button', { type: 'button', 'class': 'g5-btn' }, [idx + 1 < W.length ? 'Next line →' : 'Finish →']);
          next.addEventListener('click', function () { idx++; while (idx < W.length && mine.done.indexOf(idx) >= 0) idx++; show(); setTimeout(function () { var f = pick.querySelector('button') || ctrl.querySelector('button'); if (f) f.focus(); }, 30); });
          ctrl.appendChild(next);
        });
        pick.appendChild(b);
      });
    }
    show();
    var ref = G.after ? activityByTitle(G.after, panel('words')) : null;
    if (ref) afterNode(ref, wrap);
    else { var nw = nextWrap('words'); if (nw) panel('words').insertBefore(wrap, nw); }
  }

  /* ── 12g. the week's word game: Ears of Corn (week 24) ──
     DATA.game = {type:'corn', title, sub, after, look, how, doneLine,
                  ears:[{w:'mistreatment', parts:['mis','treat','ment'], base:1, means:'…', why:'…', hint:'…'}]}
     A take-apart: a long word is an ear of corn. Tap each husk (a part added to the front or the end) to peel
     it away; the base word is the ear inside. Tapping the base shakes and says what a husk is.
     Storage oao.g5ela.corn.wk<NN> {day:{done:[i]}}. */
  function buildCorn() {
    var G = D.game; if (!G || G.type !== 'corn' || !G.ears || !G.ears.length) return;
    var wkKey = 'corn.wk' + L.week;
    var st = store(wkKey) || {};
    var mine = st[L.day] || { done: [] };
    var W = G.ears, idx = 0, peeled = [];
    while (idx < W.length && mine.done.indexOf(idx) >= 0) idx++;
    var wrap = h('div', { 'class': 'activity g5-game' });
    wrap.innerHTML =
      '<div class="activity-head"><div class="activity-num g5-game-num" aria-hidden="true">🌽</div><div>' +
      '<div class="activity-title">' + esc(G.title || 'Ears of Corn') + '</div>' +
      '<div class="activity-sub">' + esc(G.sub || 'Word game for this week') + '</div></div></div>';
    var body = h('div', { 'class': 'activity-body' });
    wrap.appendChild(body);
    var look = h('details', { 'class': 'g5-look' }, [h('summary', { text: '👀 What am I looking at?' }), h('p', { text: G.look })]);
    if (!mine.done.length) look.open = true;
    body.appendChild(look);
    if (G.how) body.appendChild(howLine(G.how));
    var scene = h('div', { 'class': 'g5-river g5-corn', role: 'img', 'aria-label': 'A row of ears of corn on a blanket by a cooking fire. Each word you take apart opens one ear.' });
    body.appendChild(scene);
    var stepBox = h('div', { 'class': 'g5-stone-step', 'aria-live': 'polite' });
    var row = h('div', { 'class': 'g5-corn-word' });
    var ctrl = h('div', { 'class': 'g5-stone-ctrl' });
    var fb = h('p', { 'class': 'g5-stone-fb', 'aria-live': 'polite' });
    var tally = h('p', { 'class': 'g5-stone-tally' });
    [stepBox, row, ctrl, fb, tally].forEach(function (n) { body.appendChild(n); });

    function draw() {
      var allDone = 0;
      Object.keys(st).forEach(function (k) { allDone += (st[k].done || []).length; });
      var n = mine.done.length, w = 900, hgt = 170, svg = '';
      svg += '<svg viewBox="0 0 ' + w + ' ' + hgt + '" preserveAspectRatio="xMidYMid meet" aria-hidden="true">' +
        '<rect width="' + w + '" height="' + hgt + '" fill="#2B2A3A"/>' +
        '<path d="M0,120 C220,104 680,104 900,120 L900,170 L0,170 Z" fill="#E8ECF2"/>' +
        '<path d="M150,128 L750,128 L790,160 L110,160 Z" fill="#8B3A20"/><path d="M150,128 L750,128 L756,134 L144,134 Z" fill="#C8A850"/>';
      svg += '<circle cx="70" cy="118" r="26" fill="rgba(233,180,76,.25)"/><path d="M58,128 Q70,84 82,128 Z" fill="#E9B44C"/><path d="M64,128 Q70,104 76,128 Z" fill="#F6E27A"/><path d="M48,130 L92,130" stroke="#3A2A1A" stroke-width="6" stroke-linecap="round"/>';
      var gap = 600 / (W.length + 1);
      for (var r = 0; r < W.length; r++) {
        var on = mine.done.indexOf(r) >= 0, x = 150 + gap * (r + 1), y = 132;
        if (on) {
          svg += '<ellipse cx="' + x + '" cy="' + (y - 34) + '" rx="13" ry="38" fill="#E9B44C"/>';
          for (var k = 0; k < 6; k++) svg += '<path d="M' + (x - 11) + ',' + (y - 62 + k * 10) + ' L' + (x + 11) + ',' + (y - 62 + k * 10) + '" stroke="#C8922A" stroke-width="1.5"/>';
          svg += '<path d="M' + x + ',' + (y - 72) + ' L' + x + ',' + y + '" stroke="#C8922A" stroke-width="1.5"/>' +
            '<path d="M' + (x - 13) + ',' + (y - 20) + ' Q' + (x - 34) + ',' + (y - 4) + ' ' + (x - 30) + ',' + (y + 6) + ' Q' + (x - 12) + ',' + (y + 4) + ' ' + x + ',' + (y + 2) + ' Z" fill="#7FA05A"/>' +
            '<path d="M' + (x + 13) + ',' + (y - 20) + ' Q' + (x + 34) + ',' + (y - 4) + ' ' + (x + 30) + ',' + (y + 6) + ' Q' + (x + 12) + ',' + (y + 4) + ' ' + x + ',' + (y + 2) + ' Z" fill="#7FA05A"/>';
        } else {
          svg += '<path d="M' + x + ',' + (y - 76) + ' Q' + (x + 20) + ',' + (y - 36) + ' ' + x + ',' + (y + 4) + ' Q' + (x - 20) + ',' + (y - 36) + ' ' + x + ',' + (y - 76) + ' Z" fill="#6F8F4E"/>' +
            '<path d="M' + x + ',' + (y - 76) + ' L' + x + ',' + (y + 2) + '" stroke="#587A3C" stroke-width="2"/>';
        }
      }
      svg += '</svg>';
      scene.innerHTML = svg;
      tally.textContent = 'Today: ' + n + ' of ' + W.length + (W.length === 1 ? ' ear' : ' ears') + ' opened. This week: ' + allDone + '.';
    }
    function save() { st[L.day] = mine; store(wkKey, st); }
    function shake(b) { b.classList.add('g5-shake'); setTimeout(function () { b.classList.remove('g5-shake'); }, 450); }
    function show() {
      fb.textContent = ''; ctrl.innerHTML = ''; row.innerHTML = ''; peeled = [];
      if (idx >= W.length) {
        draw();
        stepBox.innerHTML = '<b>Every ear is open.</b> ' + esc(G.doneLine || 'Come back tomorrow for more.');
        var again = h('button', { type: 'button', 'class': 'g5-btn g5-btn-ghost' }, ['↺ Take them apart again']);
        again.addEventListener('click', function () { mine.done = []; idx = 0; save(); show(); });
        ctrl.appendChild(again); return;
      }
      var S = W[idx], husks = S.parts.length - 1;
      draw();
      stepBox.innerHTML = '<span class="g5-stepn">Word ' + (idx + 1) + ' of ' + W.length + '</span> <b>' + esc(S.w) + '</b>. Tap each husk: a part added to the front or the end. Leave the base word.';
      S.parts.forEach(function (p, k) {
        var b = h('button', { type: 'button', 'class': 'g5-beat g5-corn-part', 'aria-label': 'word part ' + p }, [p]);
        b.addEventListener('click', function () {
          if (k === S.base) { fb.textContent = S.hint || 'That part can stand alone as a word, so it is the base. Tap a part that was added to the front or the end.'; shake(b); return; }
          if (peeled.indexOf(k) >= 0) return;
          peeled.push(k); b.classList.add('g5-corn-husk'); b.disabled = true;
          if (peeled.length < husks) { fb.textContent = 'One husk off. Is there another?'; return; }
          row.querySelectorAll('button').forEach(function (x, j) { x.disabled = true; if (j === S.base) x.classList.add('g5-corn-base'); });
          if (mine.done.indexOf(idx) < 0) mine.done.push(idx);
          save(); draw();
          fb.innerHTML = 'The base word is <b>' + esc(S.parts[S.base]) + '</b>. ' + esc(S.why || '') + (S.means ? ' <b>' + esc(S.w) + '</b>: ' + esc(S.means) : '');
          var next = h('button', { type: 'button', 'class': 'g5-btn' }, [idx + 1 < W.length ? 'Next word →' : 'Finish →']);
          next.addEventListener('click', function () { idx++; while (idx < W.length && mine.done.indexOf(idx) >= 0) idx++; show(); setTimeout(function () { var f = row.querySelector('button') || ctrl.querySelector('button'); if (f) f.focus(); }, 30); });
          ctrl.appendChild(next);
        });
        row.appendChild(b);
      });
    }
    show();
    var ref = G.after ? activityByTitle(G.after, panel('words')) : null;
    if (ref) afterNode(ref, wrap);
    else { var nw = nextWrap('words'); if (nw) panel('words').insertBefore(wrap, nw); }
  }

  /* ── 12h. The Assayer's Scale (week 25): weigh each word on the HEAR pan (aud), the SPEAK pan (or),
     or the FOOL'S GOLD tray when it only looks like one. DATA game.type 'scale', game.nuggets[{w, pan, why, miss}] */
  function buildScale() {
    var G = D.game; if (!G || G.type !== 'scale' || !G.nuggets || !G.nuggets.length) return;
    var wkKey = 'scale.wk' + L.week;
    var st = store(wkKey) || {};
    var mine = st[L.day] || { done: [], hear: 0, speak: 0, fool: 0 };
    var W = G.nuggets, idx = 0;
    while (idx < W.length && mine.done.indexOf(idx) >= 0) idx++;
    var PANS = [['hear', '👂 HEAR pan', 'aud'], ['speak', '🗣️ SPEAK pan', 'or'], ['fool', '🪨 Fool’s gold', 'looks like it, but no']];
    var wrap = h('div', { 'class': 'activity g5-game' });
    wrap.innerHTML =
      '<div class="activity-head"><div class="activity-num g5-game-num" aria-hidden="true">⚖️</div><div>' +
      '<div class="activity-title">' + esc(G.title || 'The Assayer’s Scale') + '</div>' +
      '<div class="activity-sub">' + esc(G.sub || 'Word game for this week') + '</div></div></div>';
    var body = h('div', { 'class': 'activity-body' });
    wrap.appendChild(body);
    var look = h('details', { 'class': 'g5-look' }, [h('summary', { text: '👀 What am I looking at?' }), h('p', { text: G.look })]);
    if (!mine.done.length) look.open = true;
    body.appendChild(look);
    if (G.how) body.appendChild(howLine(G.how));
    var scene = h('div', { 'class': 'g5-river g5-scale', role: 'img', 'aria-label': 'An assayer’s brass scale with a HEAR pan and a SPEAK pan, and a tray for fool’s gold below. Each word you weigh adds gold.' });
    body.appendChild(scene);
    var stepBox = h('div', { 'class': 'g5-stone-step', 'aria-live': 'polite' });
    var nug = h('div', { 'class': 'g5-scale-word' });
    var row = h('div', { 'class': 'g5-scale-pans' });
    var ctrl = h('div', { 'class': 'g5-stone-ctrl' });
    var fb = h('p', { 'class': 'g5-stone-fb', 'aria-live': 'polite' });
    var tally = h('p', { 'class': 'g5-stone-tally' });
    [stepBox, nug, row, ctrl, fb, tally].forEach(function (n) { body.appendChild(n); });

    function flakes(cx, cy, n, col) {
      var s = '';
      for (var i = 0; i < n; i++) { var x = cx - 22 + (i % 5) * 11, y = cy - 4 - Math.floor(i / 5) * 7; s += '<ellipse cx="' + x + '" cy="' + y + '" rx="6" ry="3.6" fill="' + col + '" stroke="#8A6514" stroke-width=".8"/>'; }
      return s;
    }
    function draw() {
      var allDone = 0;
      Object.keys(st).forEach(function (k) { allDone += (st[k].done || []).length; });
      var tilt = Math.max(-10, Math.min(10, (mine.speak - mine.hear) * 4));
      var w = 900, hgt = 190, cx = 450, py = 46, arm = 190;
      var rad = tilt * Math.PI / 180, dx = Math.cos(rad) * arm, dy = Math.sin(rad) * arm;
      var lx = cx - dx, ly = py - dy, rx = cx + dx, ry = py + dy;
      var svg = '<svg viewBox="0 0 ' + w + ' ' + hgt + '" preserveAspectRatio="xMidYMid meet" aria-hidden="true">' +
        '<rect width="' + w + '" height="' + hgt + '" fill="#2B2A3A"/>' +
        '<rect x="0" y="160" width="' + w + '" height="30" fill="#5A3A1E"/><rect x="0" y="158" width="' + w + '" height="4" fill="#8B5E34"/>' +
        '<rect x="' + (cx - 6) + '" y="' + py + '" width="12" height="104" fill="#C8A850"/><path d="M' + (cx - 40) + ',160 L' + (cx + 40) + ',160 L' + (cx + 26) + ',146 L' + (cx - 26) + ',146 Z" fill="#B08A3A"/>' +
        '<line x1="' + lx + '" y1="' + ly + '" x2="' + rx + '" y2="' + ry + '" stroke="#E2C46A" stroke-width="6" stroke-linecap="round"/><circle cx="' + cx + '" cy="' + py + '" r="8" fill="#F5D77A"/>';
      [[lx, ly, mine.hear, 'aud · hear'], [rx, ry, mine.speak, 'or · speak']].forEach(function (p) {
        var x = p[0], y = p[1], bot = y + 62;
        svg += '<line x1="' + x + '" y1="' + y + '" x2="' + (x - 44) + '" y2="' + bot + '" stroke="#C8A850" stroke-width="1.5"/><line x1="' + x + '" y1="' + y + '" x2="' + (x + 44) + '" y2="' + bot + '" stroke="#C8A850" stroke-width="1.5"/>' +
          '<path d="M' + (x - 52) + ',' + bot + ' Q' + x + ',' + (bot + 22) + ' ' + (x + 52) + ',' + bot + ' Z" fill="#B08A3A" stroke="#E2C46A" stroke-width="1.5"/>' +
          flakes(x, bot, Math.min(p[2], 15), '#F5C842') +
          '<text x="' + x + '" y="' + (bot + 34) + '" fill="#F5E6C8" font-family="Georgia,serif" font-size="14" text-anchor="middle">' + p[3] + '</text>';
      });
      svg += '<rect x="700" y="132" width="150" height="24" rx="5" fill="#4A3A2A" stroke="#8B5E34"/>' + flakes(775, 140, Math.min(mine.fool, 10), '#9A9A8A') +
        '<text x="775" y="126" fill="#D8D0C0" font-family="Georgia,serif" font-size="13" text-anchor="middle">fool’s gold</text>';
      svg += '<path d="M90,150 Q70,120 96,104 L124,104 Q150,120 130,150 Z" fill="#8B5E34" stroke="#C8A850"/><path d="M98,104 L122,104" stroke="#3A2A1A" stroke-width="3"/>' +
        '<text x="110" y="134" fill="#F5E6C8" font-family="Georgia,serif" font-size="16" text-anchor="middle">' + (mine.hear + mine.speak) + '</text>' +
        '<text x="110" y="176" fill="#F5E6C8" font-family="Georgia,serif" font-size="13" text-anchor="middle">pouch</text></svg>';
      scene.innerHTML = svg;
      tally.textContent = 'Today: ' + mine.done.length + ' of ' + W.length + ' words weighed. This week: ' + allDone + '.';
    }
    function save() { st[L.day] = mine; store(wkKey, st); }
    function shake(b) { b.classList.add('g5-shake'); setTimeout(function () { b.classList.remove('g5-shake'); }, 450); }
    function show() {
      fb.textContent = ''; ctrl.innerHTML = ''; row.innerHTML = ''; nug.innerHTML = '';
      if (idx >= W.length) {
        draw();
        stepBox.innerHTML = '<b>Every word is weighed.</b> ' + esc(G.doneLine || 'Come back tomorrow for more.');
        var again = h('button', { type: 'button', 'class': 'g5-btn g5-btn-ghost' }, ['↺ Weigh them again']);
        again.addEventListener('click', function () { mine = { done: [], hear: 0, speak: 0, fool: 0 }; idx = 0; save(); show(); });
        ctrl.appendChild(again); return;
      }
      var S = W[idx];
      draw();
      stepBox.innerHTML = '<span class="g5-stepn">Word ' + (idx + 1) + ' of ' + W.length + '</span> Does this word really carry <b>aud</b> (hear) or <b>or</b> (speak)? Or is it fool’s gold?';
      nug.appendChild(h('span', { 'class': 'g5-scale-nugget' }, [S.w]));
      PANS.forEach(function (P) {
        var b = h('button', { type: 'button', 'class': 'g5-beat g5-scale-pan', 'aria-label': P[1] + ', ' + P[2] }, [P[1]]);
        b.appendChild(h('small', { text: P[2] }));
        b.addEventListener('click', function () {
          if (P[0] !== S.pan) { fb.textContent = S.miss || (P[0] === 'fool' ? 'Look again. This one really does carry a hear or speak root.' : 'Look again. Think about what the word means, not just how it looks.'); shake(b); return; }
          row.querySelectorAll('button').forEach(function (x) { x.disabled = true; });
          b.classList.add('g5-scale-right');
          if (mine.done.indexOf(idx) < 0) { mine.done.push(idx); mine[S.pan]++; }
          save(); draw();
          fb.innerHTML = '<b>' + esc(S.w) + '</b>: ' + esc(S.why || '');
          var next = h('button', { type: 'button', 'class': 'g5-btn' }, [idx + 1 < W.length ? 'Next word →' : 'Finish →']);
          next.addEventListener('click', function () { idx++; while (idx < W.length && mine.done.indexOf(idx) >= 0) idx++; show(); setTimeout(function () { var f = row.querySelector('button') || ctrl.querySelector('button'); if (f) f.focus(); }, 30); });
          ctrl.appendChild(next);
        });
        row.appendChild(b);
      });
    }
    show();
    var ref = G.after ? activityByTitle(G.after, panel('words')) : null;
    if (ref) afterNode(ref, wrap);
    else { var nw = nextWrap('words'); if (nw) panel('words').insertBefore(wrap, nw); }
  }

  /* ── 12i. Through the Strait (week 26): a route game ─────────
     The ship works west through the narrows of the Strait of Magellan. At each
     narrows a clue and two channels; the right word is the safe channel. A wrong
     channel bumps the rocks (try again). Each narrows passed lights a fire on the
     south shore; the last one opens the Pacific. DATA: game {type:'strait',
     narrows:[{clue, a, b, ok:'a'|'b', why, miss}]}. */
  function buildStrait() {
    var G = D.game; if (!G || G.type !== 'strait' || !G.narrows || !G.narrows.length) return;
    var wkKey = 'strait.wk' + L.week;
    var st = store(wkKey) || {};
    var mine = st[L.day] || { done: [] };
    var N = G.narrows, idx = 0;
    while (idx < N.length && mine.done.indexOf(idx) >= 0) idx++;
    var wrap = h('div', { 'class': 'activity g5-game' });
    wrap.innerHTML =
      '<div class="activity-head"><div class="activity-num g5-game-num" aria-hidden="true">🧭</div><div>' +
      '<div class="activity-title">' + esc(G.title || 'Through the Strait') + '</div>' +
      '<div class="activity-sub">' + esc(G.sub || 'Word game for this week') + '</div></div></div>';
    var body = h('div', { 'class': 'activity-body' });
    wrap.appendChild(body);
    var look = h('details', { 'class': 'g5-look' }, [h('summary', { text: '👀 What am I looking at?' }), h('p', { text: G.look })]);
    if (!mine.done.length) look.open = true;
    body.appendChild(look);
    if (G.how) body.appendChild(howLine(G.how));
    var scene = h('div', { 'class': 'g5-river g5-strait', role: 'img', 'aria-label': 'A map of a narrow, winding strait between Patagonia to the north and Tierra del Fuego to the south. The ship moves west from the Atlantic toward the Pacific as you pass each narrows.' });
    body.appendChild(scene);
    var stepBox = h('div', { 'class': 'g5-stone-step', 'aria-live': 'polite' });
    var row = h('div', { 'class': 'g5-strait-chan' });
    var ctrl = h('div', { 'class': 'g5-stone-ctrl' });
    var fb = h('p', { 'class': 'g5-stone-fb', 'aria-live': 'polite' });
    var tally = h('p', { 'class': 'g5-stone-tally' });
    [stepBox, row, ctrl, fb, tally].forEach(function (n) { body.appendChild(n); });

    function pt(i) { // points along the channel, east (right) to west (left)
      var n = N.length, t = n > 1 ? i / (n - 1) : 0;
      var x = 790 - t * 680, y = 100 + Math.sin(t * Math.PI * 2.2) * 26;
      return [x, y];
    }
    function draw() {
      var allDone = 0;
      Object.keys(st).forEach(function (k) { allDone += (st[k].done || []).length; });
      var passed = mine.done.length, finished = passed >= N.length;
      var path = 'M880,96';
      for (var i = 0; i < N.length; i++) { var p = pt(i); path += ' L' + p[0] + ',' + p[1]; }
      path += ' L20,98';
      var svg = '<svg viewBox="0 0 900 200" preserveAspectRatio="xMidYMid meet" aria-hidden="true">' +
        '<rect width="900" height="200" fill="#9CC3D5"/>' +
        '<rect x="0" y="0" width="120" height="200" fill="' + (finished ? '#6FB0D8' : '#7FA9BE') + '"/>' +
        '<path d="M120,0 L900,0 L900,70 Q780,58 700,80 Q600,104 500,72 Q400,40 300,78 Q220,108 120,74 Z" fill="#C9B98A" stroke="#8C7A4A"/>' +
        '<path d="M120,200 L900,200 L900,124 Q780,140 700,122 Q600,146 500,120 Q400,96 300,128 Q220,150 120,126 Z" fill="#B7A777" stroke="#8C7A4A"/>' +
        '<path d="' + path + '" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-dasharray="6 6" opacity=".8"/>' +
        '<text x="500" y="26" fill="#5A4A22" font-family="Georgia,serif" font-size="16" text-anchor="middle">Patagonia</text>' +
        '<text x="500" y="186" fill="#4A3A18" font-family="Georgia,serif" font-size="16" text-anchor="middle">Tierra del Fuego</text>' +
        '<text x="60" y="104" fill="' + (finished ? '#0E3A5C' : '#3A5A6C') + '" font-family="Georgia,serif" font-size="' + (finished ? 17 : 14) + '" text-anchor="middle" font-weight="' + (finished ? 700 : 400) + '">PACIFIC</text>' +
        '<text x="860" y="44" fill="#2A4A5C" font-family="Georgia,serif" font-size="13" text-anchor="middle">ATLANTIC</text>';
      for (var j = 0; j < N.length; j++) {
        var q = pt(j), on = mine.done.indexOf(j) >= 0;
        svg += '<circle cx="' + q[0] + '" cy="' + q[1] + '" r="7" fill="' + (on ? '#F5D77A' : '#FFFFFF') + '" stroke="#2A4A5C" stroke-width="1.5"/>';
        var fx = q[0], fy = 158 + (j % 2) * 10;
        svg += on ? '<path d="M' + fx + ',' + (fy - 16) + ' Q' + (fx + 8) + ',' + (fy - 6) + ' ' + fx + ',' + fy + ' Q' + (fx - 8) + ',' + (fy - 6) + ' ' + fx + ',' + (fy - 16) + ' Z" fill="#F08A24" stroke="#B5501A"/><circle cx="' + fx + '" cy="' + (fy - 5) + '" r="2.5" fill="#FFE07A"/>'
                  : '<circle cx="' + fx + '" cy="' + (fy - 4) + '" r="3" fill="#7A6A4A"/>';
      }
      var sp = finished ? [60, 130] : (idx < N.length ? pt(idx) : pt(N.length - 1));
      var sx = finished ? 70 : sp[0] + 22, sy = finished ? 140 : sp[1];
      svg += '<g transform="translate(' + sx + ',' + (sy - 4) + ')"><path d="M-18,0 L18,0 L12,9 L-12,9 Z" fill="#3A2A1A"/><rect x="-2" y="-22" width="3" height="22" fill="#3A2A1A"/><path d="M1,-21 L14,-6 L1,-6 Z" fill="#FFFFFF" stroke="#8C7A4A" stroke-width=".8"/><circle cx="-8" cy="4" r="5" fill="#8B3A20"/></g>';
      svg += '</svg>';
      scene.innerHTML = svg;
      tally.textContent = 'Today: ' + passed + ' of ' + N.length + ' narrows passed. This week: ' + allDone + '.';
    }
    function save() { st[L.day] = mine; store(wkKey, st); }
    function shake(b) { b.classList.add('g5-shake'); setTimeout(function () { b.classList.remove('g5-shake'); }, 450); }
    function show() {
      fb.textContent = ''; ctrl.innerHTML = ''; row.innerHTML = '';
      if (idx >= N.length) {
        draw();
        stepBox.innerHTML = '<b>Through the Strait!</b> ' + esc(G.doneLine || 'The Pacific is open.');
        var again = h('button', { type: 'button', 'class': 'g5-btn g5-btn-ghost' }, ['↺ Sail it again']);
        again.addEventListener('click', function () { mine = { done: [] }; idx = 0; save(); show(); });
        ctrl.appendChild(again); return;
      }
      var S = N[idx];
      draw();
      stepBox.innerHTML = '<span class="g5-stepn">Narrows ' + (idx + 1) + ' of ' + N.length + '</span> ' + esc(S.clue);
      [['a', '⬆ North channel'], ['b', '⬇ South channel']].forEach(function (C) {
        var b = h('button', { type: 'button', 'class': 'g5-beat g5-strait-btn', 'aria-label': C[1] + ': ' + S[C[0]] }, [h('small', { text: C[1] }), h('span', { text: S[C[0]] })]);
        b.addEventListener('click', function () {
          if (C[0] !== S.ok) { fb.textContent = '🪨 Rocks! ' + (S.miss || 'Look again at what the word means, not just how it looks.'); shake(b); return; }
          row.querySelectorAll('button').forEach(function (x) { x.disabled = true; });
          b.classList.add('g5-strait-right');
          if (mine.done.indexOf(idx) < 0) mine.done.push(idx);
          save(); draw();
          fb.innerHTML = '<b>' + esc(S[S.ok]) + '</b>: ' + esc(S.why || '');
          var next = h('button', { type: 'button', 'class': 'g5-btn' }, [idx + 1 < N.length ? 'Sail on →' : 'Into the Pacific →']);
          next.addEventListener('click', function () { idx++; while (idx < N.length && mine.done.indexOf(idx) >= 0) idx++; show(); setTimeout(function () { var f = row.querySelector('button') || ctrl.querySelector('button'); if (f) f.focus(); }, 30); });
          ctrl.appendChild(next);
        });
        row.appendChild(b);
      });
    }
    show();
    var ref = G.after ? activityByTitle(G.after, panel('words')) : null;
    if (ref) afterNode(ref, wrap);
    else { var nw = nextWrap('words'); if (nw) panel('words').insertBefore(wrap, nw); }
  }

  /* ── 13. the Commonplace Book page ─────────────────────────── */
  var NAME_BAD = /\b(ass|butt|poop|fart|stupid|dumb|idiot|hate|kill|sex|damn|hell|crap)\b/i;
  function profileName() { var p = store('profile'); return p && p.name ? p.name : ''; }

  function buildBook() {
    var B = D.book; if (!B) return;
    var all = bookAll();
    var page = all[KEY] || {};
    function persist() {
      page.book = L.bookTitle; page.chapters = L.chapters; page.week = L.week; page.day = L.day;
      page.lesson = L.week + '.' + L.day; page.when = new Date().toISOString().slice(0, 10);
      page.line = B.line && B.line.text; page.lineCite = B.line && B.line.cite;
      page.word = B.word && B.word.w; page.root = B.word && B.word.root; page.means = B.word && B.word.means;
      all = bookAll(); all[KEY] = page;
      var ok = store('book', all);
      status.textContent = ok ? 'Saved on this computer.' : 'Could not save on this computer. Copy your page before you leave.';
      paintRibbon(); paintDone();
    }

    var card = h('section', { 'class': 'g5-page', 'aria-labelledby': 'g5-page-h' });
    var nm = profileName();
    card.innerHTML =
      '<div class="g5-page-marble" aria-hidden="true"></div>' +
      '<div class="g5-page-head"><div class="g5-page-k">My Commonplace Book</div>' +
      '<h2 id="g5-page-h" class="g5-page-h">Page ' + esc(B.page || L.day) + ' · <em>' + esc(L.bookTitle) + '</em>, ' + esc(L.chapters) + '</h2></div>';

    var look = h('details', { 'class': 'g5-look' }, [h('summary', { text: '👀 What am I looking at?' }), h('p', { text: B.look || '' })]);
    if (!Object.keys(all).length) look.open = true;
    card.appendChild(look);

    // name, once
    var nameRow = h('div', { 'class': 'g5-name' });
    function paintName() {
      var n = profileName();
      nameRow.innerHTML = '';
      if (n) { nameRow.appendChild(h('p', { 'class': 'g5-owner', text: 'The Commonplace Book of ' + n })); return; }
      var inp = h('input', { type: 'text', maxlength: '24', id: 'g5-name-in', autocomplete: 'given-name' });
      var lab = h('label', { 'for': 'g5-name-in', text: 'Write your first name for the front of your book: ' });
      var go = h('button', { type: 'button', 'class': 'g5-btn g5-btn-small' }, ['Save name']);
      var msg = h('span', { 'class': 'g5-name-msg', 'aria-live': 'polite' });
      go.addEventListener('click', function () {
        var v = inp.value.trim().replace(/[^A-Za-z' -]/g, '');
        if (!v) { msg.textContent = 'Type your first name.'; return; }
        if (NAME_BAD.test(v)) { msg.textContent = 'Please use your real first name.'; return; }
        store('profile', { name: v }); paintName();
      });
      nameRow.appendChild(lab); nameRow.appendChild(inp); nameRow.appendChild(go); nameRow.appendChild(msg);
    }
    paintName(); card.appendChild(nameRow);

    // 1. lines worth keeping
    var s1 = h('div', { 'class': 'g5-pg-sec' });
    s1.innerHTML = '<h3 class="g5-pg-h">1 · Lines worth keeping</h3>';
    s1.appendChild(howLine(B.how1 || { 'do': ['Read the line copied for you.', 'Find a second line in your book.', 'Copy it exactly, with its page number.'] }));
    if (B.line) s1.appendChild(h('blockquote', { 'class': 'g5-quote g5-kept', html: '“' + esc(B.line.text) + '”<cite>' + esc(B.line.cite) + '</cite>' }));
    var ownL = h('label', { 'class': 'g5-lab', 'for': 'g5-own', text: 'A line I chose from ' + (L.chapters || 'today\'s chapters') + ' (copy it exactly):' });
    var own = h('textarea', { id: 'g5-own', 'class': 'g5-ta g5-ta-line', rows: '2' });
    own.value = page.own || '';
    var pgL = h('label', { 'class': 'g5-lab g5-lab-inline', 'for': 'g5-own-pg', text: 'Page number in my book: ' });
    var pg = h('input', { id: 'g5-own-pg', type: 'text', inputmode: 'numeric', maxlength: '4', 'class': 'g5-pg-in' });
    pg.value = page.ownPage || '';
    s1.appendChild(ownL); s1.appendChild(own); s1.appendChild(h('div', {}, [pgL, pg]));
    var whyL = h('label', { 'class': 'g5-lab', 'for': 'g5-why', text: B.prompt || 'Pick one of your two lines. Why does it matter?' });
    var why = h('textarea', { id: 'g5-why', 'class': 'g5-ta', rows: '4' });
    why.value = page.why || '';
    var whyN = h('span', { 'class': 'g5-count' });
    s1.appendChild(whyL); s1.appendChild(why); s1.appendChild(whyN);
    card.appendChild(s1);

    // 2. word of the day
    if (B.word) {
      var s2 = h('div', { 'class': 'g5-pg-sec' });
      s2.innerHTML = '<h3 class="g5-pg-h">2 · Word of the day</h3>' +
        '<p class="g5-wod"><b>' + esc(B.word.w) + '</b> <span class="g5-wod-root">root <i>' + esc(B.word.root) + '</i> = ' + esc(B.word.means) + '</span></p>' +
        (B.word.def ? '<p class="g5-wod-def">' + esc(B.word.def) + '</p>' : '');
      var senL = h('label', { 'class': 'g5-lab', 'for': 'g5-sen', text: 'Write your own sentence with ' + B.word.w + ' (8 or more words). Make it show what the word means.' });
      var sen = h('textarea', { id: 'g5-sen', 'class': 'g5-ta', rows: '2' });
      sen.value = page.sentence || '';
      var senN = h('span', { 'class': 'g5-count' });
      s2.appendChild(senL); s2.appendChild(sen); s2.appendChild(senN);
      card.appendChild(s2);
    }

    // 3. the author's move (RWM days only; carried forward, never asked twice)
    var mimicBox = document.getElementById('journal-rwm-mimic');
    if (B.move && mimicBox) {
      var s3 = h('div', { 'class': 'g5-pg-sec' });
      s3.innerHTML = '<h3 class="g5-pg-h">3 · The author’s move</h3><p class="g5-move">' + esc(B.move) + '</p>';
      var carry = h('blockquote', { 'class': 'g5-carry' });
      var carryNote = h('p', { 'class': 'g5-note', text: 'This is your sentence from the Read Like a Writer “Try It” box. Change it there and it changes here.' });
      function paintCarry() { carry.textContent = mimicBox.value.trim() || '(You have not written your Try It sentence yet. It is in Read Like a Writer, on the Reading tab.)'; page.mimic = mimicBox.value.trim(); }
      paintCarry();
      mimicBox.addEventListener('input', function () { paintCarry(); persist(); });
      s3.appendChild(carry); s3.appendChild(carryNote);
      card.appendChild(s3);
    }

    var foot = h('div', { 'class': 'g5-pg-foot' });
    var status = h('span', { 'class': 'g5-status', 'aria-live': 'polite' });
    var doneMark = h('span', { 'class': 'g5-done' });
    var openB = h('button', { type: 'button', 'class': 'g5-btn g5-btn-ghost' }, ['📖 Open my whole book']);
    openB.addEventListener('click', openBook);
    foot.appendChild(doneMark); foot.appendChild(status); foot.appendChild(openB);
    card.appendChild(foot);

    function paintCounts() {
      var n = sentences(why.value);
      whyN.textContent = n >= 2 ? '✓ ' + n + ' sentences' : n + ' of 2 sentences';
      whyN.classList.toggle('ok', n >= 2);
      var sn = card.querySelector('#g5-sen');
      if (sn) { var w = words(sn.value), c = sn.nextElementSibling; c.textContent = w >= 8 ? '✓ ' + w + ' words' : w + ' of 8 words'; c.classList.toggle('ok', w >= 8); }
    }
    function paintDone() {
      var left = [];
      if (words(page.own) < 4) left.push('copy a line you chose');
      if (sentences(page.why) < 2) left.push('write 2 sentences about why it matters');
      if (B.word && words(page.sentence) < 8) left.push('write your word sentence');
      doneMark.innerHTML = left.length ? 'Still to do: ' + esc(left.join('; ')) + '.' : '<b>✓ This page is written.</b>';
      doneMark.classList.toggle('ok', !left.length);
    }
    var t;
    function onType(field, el) { return function () { page[field] = el.value; paintCounts(); clearTimeout(t); t = setTimeout(persist, 350); }; }
    own.addEventListener('input', onType('own', own));
    pg.addEventListener('input', onType('ownPage', pg));
    why.addEventListener('input', onType('why', why));
    var senEl = card.querySelector('#g5-sen'); if (senEl) senEl.addEventListener('input', onType('sentence', senEl));
    paintCounts(); paintDone();

    var p = panel(B.tab || 'reading'), nw = nextWrap(B.tab || 'reading');
    if (nw) p.insertBefore(card, nw); else if (p) p.appendChild(card);
  }

  /* ── 14. the whole book: view, download, print ────────────── */
  function bookText() {
    var all = bookAll(), name = profileName();
    var keys = Object.keys(all).sort(function (a, b) {
      var x = all[a], y = all[b]; return (x.week - y.week) || (x.day - y.day);
    });
    var out = 'MY COMMONPLACE BOOK' + (name ? ' · ' + name : '') + '\n\n';
    var lastBook = '';
    keys.forEach(function (k) {
      var p = all[k];
      if (p.book !== lastBook) { out += '════ ' + p.book + ' ════\n\n'; lastBook = p.book; }
      out += 'Lesson ' + p.lesson + ' · ' + (p.chapters || '') + '\n';
      if (p.line) out += '  Line: “' + p.line + '” (' + (p.lineCite || '') + ')\n';
      if (p.own) out += '  My line: “' + p.own.trim() + '”' + (p.ownPage ? ' (page ' + p.ownPage + ')' : '') + '\n';
      if (p.why) out += '  Why it matters: ' + p.why.trim() + '\n';
      if (p.word) out += '  Word of the day: ' + p.word + ' (' + p.root + ' = ' + p.means + ')\n';
      if (p.sentence) out += '  My sentence: ' + p.sentence.trim() + '\n';
      if (p.mimic) out += '  Author’s move, my try: ' + p.mimic + '\n';
      out += '\n';
    });
    return out;
  }
  var lastFocus = null;
  function openBook() {
    var old = document.querySelector('.g5-modal'); if (old) old.remove();
    lastFocus = document.activeElement;
    var all = bookAll(), name = profileName();
    var keys = Object.keys(all).sort(function (a, b) { return (all[a].week - all[b].week) || (all[a].day - all[b].day); });
    var m = h('div', { 'class': 'g5-modal', role: 'dialog', 'aria-modal': 'true', 'aria-label': 'My Commonplace Book' });
    var inner = h('div', { 'class': 'g5-modal-in' });
    var html = '<div class="g5-page-marble" aria-hidden="true"></div><div class="g5-book-title"><div class="g5-page-k">My Commonplace Book</div><h2>' + (name ? 'The Commonplace Book of ' + esc(name) : 'My Commonplace Book') + '</h2>' +
      '<p class="g5-note">A reader’s book of lines worth keeping, one page for every lesson. You will use it again at the end of the year.</p></div>';
    var lastBook = '';
    if (!keys.length) html += '<p>No pages yet. Your first page is at the bottom of the Reading tab.</p>';
    keys.forEach(function (k) {
      var p = all[k];
      if (p.book !== lastBook) {
        var tp = (D.titlePages || {})[p.book] || {};
        html += '<div class="g5-tp"><h3><em>' + esc(p.book) + '</em></h3>' + (tp.author ? '<p>' + esc(tp.author) + '</p>' : '') + (tp.setting ? '<p class="g5-tp-set">' + esc(tp.setting) + '</p>' : '') + '</div>';
        lastBook = p.book;
      }
      html += '<article class="g5-bp"><h4>Lesson ' + esc(p.lesson) + ' · ' + esc(p.chapters || '') + '</h4>' +
        (p.line ? '<blockquote class="g5-quote">“' + esc(p.line) + '”<cite>' + esc(p.lineCite || '') + '</cite></blockquote>' : '') +
        (p.own ? '<blockquote class="g5-quote g5-mine">“' + esc(p.own.trim()) + '”<cite>' + (p.ownPage ? 'page ' + esc(p.ownPage) : 'my line') + '</cite></blockquote>' : '') +
        (p.why ? '<p>' + esc(p.why) + '</p>' : '') +
        (p.word ? '<p class="g5-wod"><b>' + esc(p.word) + '</b> <span class="g5-wod-root">' + esc(p.root) + ' = ' + esc(p.means) + '</span></p>' : '') +
        (p.sentence ? '<p>' + esc(p.sentence) + '</p>' : '') +
        (p.mimic ? '<p><i>My try at the author’s move:</i> ' + esc(p.mimic) + '</p>' : '') + '</article>';
    });
    inner.innerHTML = html;
    var bar = h('div', { 'class': 'g5-modal-bar' });
    var dl = h('button', { type: 'button', 'class': 'g5-btn' }, ['⬇ Download (.txt)']);
    dl.addEventListener('click', function () {
      var blob = new Blob([bookText()], { type: 'text/plain' });
      var a = h('a', { href: URL.createObjectURL(blob), download: 'my-commonplace-book.txt' }); document.body.appendChild(a); a.click(); a.remove();
    });
    var pr = h('button', { type: 'button', 'class': 'g5-btn g5-btn-ghost' }, ['🖨 Print or save as PDF']);
    pr.addEventListener('click', function () {
      var w = window.open('', '_blank'); if (!w) return;
      w.document.write('<!doctype html><meta charset="utf-8"><title>My Commonplace Book</title><style>body{font:16px/1.6 Georgia,serif;max-width:680px;margin:30px auto;padding:0 20px;color:#2B2118}blockquote{border-left:3px solid #C8A850;margin:10px 0;padding:4px 12px;font-style:italic}cite{display:block;font-size:13px;font-style:normal;color:#6B5E4E}.g5-tp{margin:24px 0 8px;border-top:2px solid #2B2118;padding-top:10px}.g5-bp{page-break-inside:avoid;border-bottom:1px solid #E5D8BD;padding:8px 0}.g5-page-marble,.g5-modal-bar{display:none}</style>' + inner.innerHTML);
      w.document.close(); w.focus(); w.print();
    });
    var cl = h('button', { type: 'button', 'class': 'g5-btn g5-btn-ghost g5-close', 'aria-label': 'Close my book' }, ['Close ✕']);
    function close() { m.remove(); document.removeEventListener('keydown', key); if (lastFocus) lastFocus.focus(); }
    function key(e) {
      if (e.key === 'Escape') close();
      if (e.key === 'Tab') {
        var f = m.querySelectorAll('button, a[href]'); if (!f.length) return;
        if (e.shiftKey && document.activeElement === f[0]) { e.preventDefault(); f[f.length - 1].focus(); }
        else if (!e.shiftKey && document.activeElement === f[f.length - 1]) { e.preventDefault(); f[0].focus(); }
      }
    }
    cl.addEventListener('click', close);
    m.addEventListener('click', function (e) { if (e.target === m) close(); });
    document.addEventListener('keydown', key);
    bar.appendChild(dl); bar.appendChild(pr); bar.appendChild(cl);
    inner.insertBefore(bar, inner.firstChild);
    m.appendChild(inner); document.body.appendChild(m);
    dl.focus();
  }
  window.openCommonplaceBook = openBook;


  /* ── 14. Pilot-review fixes (Nov 10 2026), from the G3 ELA review,
     applied ahead of G5's: a new tab starts at the top; 👆 on every
     button that does something (it taps now and then, so the eye goes
     there); a key line under the header; Opti's "How to use your
     lesson" video in a Start here drawer at the very top. ───────── */
  function navTabTop() {
    if (typeof window.switchTab !== 'function' || window.switchTab._navTop) return;
    var inner = window.switchTab;
    var f = function () {
      var r = inner.apply(this, arguments);
      var t = document.getElementById('pageTop');
      try { if (t) t.scrollIntoView({ block: 'start' }); else window.scrollTo(0, 0); } catch (e) { window.scrollTo(0, 0); }
      try {
        if (window.parent && window.parent !== window) {
          window.parent.postMessage(JSON.stringify({ subject: 'lti.scrollToTop' }), '*');
          window.parent.postMessage({ subject: 'lti.scrollToTop' }, '*');
        }
      } catch (e) {}
      return r;
    };
    f._navTop = true; window.switchTab = f;
  }
  var NAV_TAP = 'button.dol-check-btn, button.fillin-check-btn, button.tab-next-btn, button.g5-hint-b, button.g5-btn, button.gathered-btn';
  function navTaps() {
    document.querySelectorAll(NAV_TAP).forEach(function (b) {
      if (b.querySelector('.nav-hand')) return;
      var t = b.firstChild;
      if (t && t.nodeType === 3) t.nodeValue = t.nodeValue.replace(/^\s*(?:\p{Extended_Pictographic}️?\s*)+/u, '');
      var hd = document.createElement('span'); hd.className = 'nav-hand'; hd.setAttribute('aria-hidden', 'true'); hd.textContent = '👆';
      b.insertBefore(hd, b.firstChild);
    });
    // the book-words drawer keeps its ▸ arrow in ::before, so its hand is a real span
    document.querySelectorAll('.g5-extra > summary').forEach(function (sm) {
      if (sm.querySelector('.nav-hand')) return;
      var hd = document.createElement('span'); hd.className = 'nav-hand'; hd.setAttribute('aria-hidden', 'true'); hd.textContent = '👆 ';
      sm.insertBefore(hd, sm.firstChild);
    });
  }
  function navKeyAndStart() {
    var hdr = document.querySelector('.header'); if (!hdr || document.querySelector('.nav-key')) return;
    var k = h('div', { 'class': 'nav-key' });
    k.innerHTML = '<span><b>👆</b> You can tap it.</span><span><b>🔊</b> You can listen.</span><span><b class="nav-dot">dotted word</b> Point to it (or tap it) to see what it means.</span>';
    afterNode(hdr, k);
    var src = window.NAV_HOWTO_SRC || 'assets/video/g5ela-howto-v2.mp4';
    var poster = window.NAV_HOWTO_POSTER || 'assets/video/g5ela-howto.jpg';
    var owl = window.NAV_OWL || 'assets/companions/owl.png';
    var card = document.createElement('details'); card.className = 'nav-start';
    card.innerHTML = '<summary class="nav-start-bar"><span class="nav-start-play" aria-hidden="true">▶</span>' +
      '<span class="nav-start-txt"><span class="nav-start-k">Start here</span>' +
      '<span class="nav-start-t">Watch how to use your lesson · 1 minute</span></span>' +
      '<span class="nav-start-face" aria-hidden="true"><img src="' + owl + '" alt="" onerror="this.remove()"></span>' +
      '<span class="nav-start-chev" aria-hidden="true">▾</span></summary>' +
      '<div class="nav-howto"><video class="nav-howto-v" controls preload="metadata" playsinline></video></div>';
    var v = card.querySelector('video');
    v.poster = poster; v.src = src;
    v.addEventListener('play', function () { if (nowPlaying) { try { nowPlaying.pause(); } catch (e) {} } });
    card.addEventListener('toggle', function () { if (!card.open) { try { v.pause(); } catch (e) {} } });
    afterNode(k, card);
  }
  function buildNav() {
    document.documentElement.classList.add('nav-fixes');
    navTabTop(); navKeyAndStart(); navTaps();
    if (window.MutationObserver) {
      var t = null;
      new MutationObserver(function () { clearTimeout(t); t = setTimeout(navTaps, 60); }).observe(document.body, { childList: true, subtree: true });
    }
  }

  /* ── 15. Hear the word: 🔊 beside each vocabulary word (Nov 2026).
     One recording per word, course-wide: assets/audio/words/g5ela-word-<word>.mp3.
     A word with no recording (e.g. Choctaw words, on purpose) gets no button.
     Cards, word bank, match words and use-it lines only: not inside book
     sentences (clutter) and not on the fill-in (it would give the answer away). ── */
  function wordSlug(w) { return String(w).trim().toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, ''); }
  function wordUrl(w) { return clip('assets/audio/words/g5ela-word-' + wordSlug(w) + '.mp3'); }
  function sayBtn(word) {
    var b = h('button', { type: 'button', 'class': 'g5-say', hidden: 'hidden', 'aria-label': 'Hear the word ' + word, title: 'Hear the word' }, ['🔊']);
    b.addEventListener('click', function (e) { e.stopPropagation(); e.preventDefault(); play(wordUrl(word), b); });
    fileExists(wordUrl(word), function (ok) { if (ok) b.hidden = false; });
    return b;
  }
  function firstText(el) {
    for (var n = el.firstChild; n; n = n.nextSibling) if (n.nodeType === 3 && n.nodeValue.trim()) return n;
    return null;
  }
  function buildWordSay() {
    var act = activityByTitle('Vocabulary', panel('words')); if (!act) return;
    function add(el, word) {
      if (!el || !word || el.querySelector(':scope > .g5-say')) return;
      el.appendChild(sayBtn(word.trim()));
    }
    act.querySelectorAll('.fc-word').forEach(function (el) { add(el, el.textContent); });
    act.querySelectorAll('.vocab-bank strong').forEach(function (el) { add(el, el.textContent); });
    act.querySelectorAll('.match-item.is-word').forEach(function (el) { add(el, el.textContent); });
    act.querySelectorAll('.vocab-use-item > div:first-child').forEach(function (el) {
      var t = firstText(el); if (!t) return;
      if (el.querySelector('.g5-say')) return;
      var b = sayBtn(t.nodeValue.trim()); el.insertBefore(b, t.nextSibling);
    });
  }

  /* ── section icons: one hand-drawn set (assets/icons/*.png) in every activity circle ──
     Matched on the activity title; the emoji in front of the title goes (the icon replaces it).
     A missing file leaves the original circle exactly as it was. */
  var ICONS = [[/Good Readers/i, 'lens'], [/Daily Oral/i, 'dol'], [/Morpholog/i, 'morphology'], [/Vocabular/i, 'vocabulary'],
    [/Chapter Thinking/i, 'chapter'], [/Chapter Introduction|^\W*Reading/i, 'reading'], [/Poetry|By Heart/i, 'poetry'],
    [/Spelling/i, 'spelling'], [/Virtue/i, 'virtue'], [/Writer/i, 'writing'], [/Grammar/i, 'grammar']];
  function buildIcons() {
    document.querySelectorAll('.activity > .activity-head').forEach(function (hd) {
      var num = hd.querySelector('.activity-num'), t = hd.querySelector('.activity-title');
      if (!num || !t || num.querySelector('.g5-ico')) return;
      var name = 'compass';
      for (var i = 0; i < ICONS.length; i++) if (ICONS[i][0].test(t.textContent)) { name = ICONS[i][1]; break; }
      var img = new Image();
      img.className = 'g5-ico'; img.alt = ''; img.setAttribute('aria-hidden', 'true');
      img.onload = function () {
        num.setAttribute('data-g5-was', num.innerHTML);
        num.innerHTML = ''; num.appendChild(img); num.classList.add('g5-ico-num');
        var tn = t.firstChild;
        while (tn && tn.nodeType !== 3) tn = tn.nextSibling;
        if (tn && tn.nodeType === 3) {
          var stripped = tn.nodeValue.replace(/^[\s☀-➿️‍]*(?:[\uD83C-\uD83E][\uDC00-\uDFFF][️‍]*)*\s*/, '');
          if (stripped !== tn.nodeValue) { t.setAttribute('data-g5-was', tn.nodeValue); tn.nodeValue = stripped; }
        }
      };
      img.src = 'assets/icons/' + name + '.png';
    });
  }

  /* ── the reading lens: What Good Readers Do becomes a choice that follows the student ──
     The lenses ARE the page's own "How to Do It" steps (scope-and-sequence content untouched):
     <strong>name:</strong> tip. The student taps one; it shows as a bookmark on the later tabs and
     comes back as one short line at the end of Chapter Thinking (added to My Work). */
  function buildLens() {
    var act = activityByTitle('What Good Readers Do'); if (!act) return;
    var kc = null;
    act.querySelectorAll('.key-concept').forEach(function (k) { if (!kc && /How to Do It/i.test(k.textContent) && k.querySelector('ol li strong')) kc = k; });
    if (!kc) return;
    var lenses = [];
    kc.querySelectorAll('ol > li').forEach(function (li) {
      var st = li.querySelector('strong'); if (!st) return;
      var name = st.textContent.replace(/[:\s]+$/, '').trim();
      var tip = li.textContent.slice(li.textContent.indexOf(st.textContent) + st.textContent.length).trim();
      lenses.push({ name: name, tip: tip });
    });
    if (lenses.length < 2) return;
    kc.hidden = true; kc.classList.add('g5-lens-src');
    act.querySelectorAll('.thinking-stop').forEach(function (n) { n.hidden = true; n.style.display = 'none'; n.classList.add('g5-lens-src'); });

    var pick = store(KEY + '.lens');
    var box = h('div', { 'class': 'g5-lens' });
    box.innerHTML = '<div class="g5-lens-hero" aria-hidden="true"></div>' +
      '<div class="g5-lens-h">Choose your reading lens</div>' +
      '<p class="g5-lens-sub">Tap one. You will read today’s chapters through it.</p>';
    var hero = new Image(); hero.alt = '';
    hero.onload = function () { box.querySelector('.g5-lens-hero').appendChild(hero); box.classList.add('has-hero'); };
    hero.src = 'assets/icons/lens-hero.jpg';
    var row = h('div', { 'class': 'g5-lens-row', role: 'group', 'aria-label': 'Reading lenses' });
    var said = h('div', { 'class': 'g5-lens-said', 'aria-live': 'polite' });
    lenses.forEach(function (L2, i) {
      var b = h('button', { type: 'button', 'class': 'g5-lens-card', 'aria-pressed': 'false' });
      b.innerHTML = '<span class="g5-lens-n">' + (i + 1) + '</span><span class="g5-lens-name">' + esc(L2.name) + '</span><span class="g5-lens-tip">' + esc(L2.tip) + '</span>';
      b.addEventListener('click', function () { choose(i); });
      row.appendChild(b);
    });
    box.appendChild(row); box.appendChild(said);
    kc.parentNode.insertBefore(box, kc);

    /* the bookmark on every tab after the lens's own tab. Placed at paint time, not now:
       onestep.js moves What Good Readers Do to Warm-Up after this layer runs. */
    var marks = [];
    function placeMarks() {
      /* one bookmark only, at the top of the Chapter Introduction box (Bethany, Nov 12 2026) */
      marks.forEach(function (m) { m.remove(); }); marks = [];
      var ci = activityByTitle('Chapter Introduction'); if (!ci) return;
      var body = ci.querySelector(':scope > .activity-body') || ci;
      var m = h('div', { 'class': 'g5-lens-mark' });
      var first = body.querySelector(':scope > .os-todo') || body.querySelector(':scope > .g5-do');
      if (first) afterNode(first, m); else body.insertBefore(m, body.firstChild);
      marks.push(m);
    }
    /* one line at the end of Chapter Thinking */
    var ct = activityByTitle('Chapter Thinking'), use = null, ta = null;
    if (ct) {
      var body = ct.querySelector(':scope > .activity-body') || ct;
      use = h('div', { 'class': 'g5-lens-use' });
      use.innerHTML = '<div class="g5-lens-use-h">🔍 Through your lens</div><p class="g5-lens-use-q"></p>';
      ta = h('textarea', { 'class': 'journal-box g5-lens-ta', id: 'journal-lens', rows: '3',
        placeholder: 'Through my lens, I noticed…' });
      ta.value = store(KEY + '.lensNote') || '';
      ta.addEventListener('input', function () { store(KEY + '.lensNote', ta.value); if (typeof window.gatherAnswers === 'function') window.gatherAnswers(); });
      use.appendChild(ta);
      body.appendChild(use);
    }
    function goHome() {
      var home = box.closest('.tab-panel');
      if (home && typeof window.switchTab === 'function') window.switchTab(home.id.replace(/^tab-/, ''));
      setTimeout(function () { box.scrollIntoView({ behavior: REDUCED ? 'auto' : 'smooth', block: 'center' }); }, 60);
    }
    function paint() {
      var L2 = typeof pick === 'number' ? lenses[pick] : null;
      row.querySelectorAll('.g5-lens-card').forEach(function (b, j) { b.setAttribute('aria-pressed', j === pick ? 'true' : 'false'); });
      placeMarks();
      said.innerHTML = L2 ? '<b>Your lens today:</b> ' + esc(L2.name) + '. Keep it in mind as you read. You will use it at the end of the lesson.' : '';
      marks.forEach(function (m) {
        m.hidden = false;
        m.innerHTML = L2
          ? '<span class="g5-lens-mark-ico" aria-hidden="true"></span><span><b>Your lens:</b> ' + esc(L2.name) + '<span class="g5-lens-mark-tip">' + esc(L2.tip) + '</span></span><button type="button" class="g5-lens-change">Change</button>'
          : '<span class="g5-lens-mark-ico" aria-hidden="true"></span><span><b>Pick your reading lens first.</b></span><button type="button" class="g5-lens-change">Go pick</button>';
        m.querySelector('button').addEventListener('click', goHome);
      });
      if (use) {
        use.querySelector('.g5-lens-use-q').innerHTML = L2
          ? 'Your lens was <b>' + esc(L2.name) + '</b>. In 1 or 2 sentences, tell what it helped you notice in today’s chapters.'
          : 'First pick a reading lens in What Good Readers Do. Then tell what it helped you notice.';
      }
      if (typeof window.gatherAnswers === 'function') try { window.gatherAnswers(); } catch (e) {}
    }
    function choose(i) { pick = i; store(KEY + '.lens', i); paint(); }
    window.addEventListener('load', function () { setTimeout(paint, 900); });   /* after onestep.js (load + 400 ms) moves the activity */

    /* My Work: add the lens and the line to the gathered answers */
    var orig = window.gatherAnswers;
    if (typeof orig === 'function' && !orig.__g5lens) {
      var wrapped = function () {
        var r = orig.apply(this, arguments);
        var out = document.getElementById('gatheredOutput');
        if (out && typeof pick === 'number') {
          out.value += '\n🔍 MY READING LENS\n────────────────────────────────\nLens: ' + lenses[pick].name + '\n' +
            ((ta && ta.value.trim()) || '(no answer)') + '\n';
        }
        return r;
      };
      wrapped.__g5lens = true; window.gatherAnswers = wrapped;
    }
    paint();
  }

  /* ── the year board: one painted path, one space per week, Mason walks it ──
     Replaces the page's old chapter tracker on the Reading tab. The art is
     assets/maps/year-board.jpg; BOARD.spaces are measured off it in PATH order
     (tools/g5sparkle/measure_board.py), so a repaint means re-measuring.
     Weeks before this lesson's week count as travelled. Books not reached yet
     lie quiet: colour drained, paper veiled. */
  var BOARD = {
    src: 'assets/maps/year-board.jpg', w: 1536, h: 1024, r: 33,
    spaces: [[212,216],[312,214],[412,214],[508,212],[608,212],[1118,214],[1216,212],[1316,212],[1346,478],[1262,478],[1176,478],[1094,478],[1006,476],[920,476],[382,476],[294,478],[200,476],[206,702],[302,706],[402,706],[494,708],[588,708],[682,710],[778,710],[1366,956],[1276,954],[1186,956],[1090,956],[996,956],[902,956],[392,956],[300,958]],
    books: [
      { t: 'The Witch of Blackbird Pond', weeks: [1, 5],   ink: '#7F9A55', rect: [140, 40, 560, 170] },
      { t: 'Johnny Tremain',              weeks: [6, 8],   ink: '#B5573F', rect: [1030, 0, 506, 190] },
      { t: 'Carry On, Mr. Bowditch',      weeks: [9, 14],  ink: '#4C5F96', rect: [790, 280, 700, 180] },
      { t: 'Writer’s Workshop',      weeks: [15, 17], ink: '#C9962F', rect: [20, 280, 480, 180] },
      { t: 'How I Became a Ghost',        weeks: [18, 24], ink: '#4F8C7E', rect: [80, 510, 760, 170] },
      { t: 'By the Great Horn Spoon!',    weeks: [25, 30], ink: '#D07A2C', rect: [780, 770, 720, 170] },
      { t: 'Journey’s End',          weeks: [31, 32], ink: '#8C6FA6', rect: [120, 770, 420, 160] }
    ]
  };
  function bookOfWeek(w) { for (var i = 0; i < BOARD.books.length; i++) if (w >= BOARD.books[i].weeks[0] && w <= BOARD.books[i].weeks[1]) return BOARD.books[i]; return BOARD.books[0]; }
  function buildBoard() {
    if (typeof L.week !== 'number' || L.week < 1 || L.week > 32) return;
    var rp = panel('reading'); if (!rp) return;
    var old = rp.querySelector('.tracker-card');
    var B = BOARD, cur = L.week, here = B.spaces[cur - 1]; if (!here) return;
    var card = h('div', { 'class': 'g5-board' });
    card.innerHTML = '<div class="g5-board-head"><div class="g5-card-k">My reading journey</div>' +
      '<div class="g5-board-t">Week ' + cur + ' of 32 · <em>' + esc(bookOfWeek(cur).t) + '</em></div></div>';
    var NS = 'http://www.w3.org/2000/svg';
    var svg = document.createElementNS(NS, 'svg');
    svg.setAttribute('viewBox', '0 0 ' + B.w + ' ' + B.h); svg.setAttribute('class', 'g5-board-svg');
    svg.setAttribute('role', 'img');
    svg.setAttribute('aria-label', 'Year map. You are on week ' + cur + ' of 32, in ' + bookOfWeek(cur).t + '.');
    var s = '<defs><filter id="g5bUnread" color-interpolation-filters="sRGB"><feColorMatrix type="saturate" values="0.12"/></filter>' +
      '<filter id="g5bSoft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="16"/></filter>' +
      '<clipPath id="g5bFace"><circle cx="0" cy="0" r="52"/></clipPath>';
    B.books.forEach(function (b, i) {
      var r = b.rect;
      s += '<mask id="g5bM' + i + '" maskUnits="userSpaceOnUse" x="0" y="0" width="' + B.w + '" height="' + B.h + '">' +
        '<rect x="' + (r[0] + 6) + '" y="' + (r[1] + 6) + '" width="' + (r[2] - 12) + '" height="' + (r[3] - 12) + '" rx="26" fill="#fff" filter="url(#g5bSoft)"/></mask>';
    });
    s += '</defs><image id="g5bImg" href="' + B.src + '" x="0" y="0" width="' + B.w + '" height="' + B.h + '"/>';
    B.books.forEach(function (b, i) {
      if (cur >= b.weeks[0]) return;
      var r = b.rect;
      s += '<g mask="url(#g5bM' + i + ')"><use href="#g5bImg" filter="url(#g5bUnread)"/>' +
        '<rect x="' + r[0] + '" y="' + r[1] + '" width="' + r[2] + '" height="' + r[3] + '" fill="#FBF3DF" opacity=".42"/></g>';
    });
    /* book titles: a cream label under each book's own spaces */
    B.books.forEach(function (b) {
      var xs = [], ys = [];
      for (var w = b.weeks[0]; w <= b.weeks[1]; w++) { xs.push(B.spaces[w - 1][0]); ys.push(B.spaces[w - 1][1]); }
      var cx = (Math.min.apply(0, xs) + Math.max.apply(0, xs)) / 2, cy = Math.max.apply(0, ys) + 62;
      if (cy + 18 > B.h) cy = Math.min.apply(0, ys) - 56;   /* bottom row: label above the spaces */
      var reached = cur >= b.weeks[0], tw = 16 + b.t.length * 11.5;
      s += '<g opacity="' + (reached ? 1 : .6) + '"><rect x="' + (cx - tw / 2) + '" y="' + (cy - 20) + '" width="' + tw + '" height="34" rx="17" fill="#FFF8E9" stroke="' + b.ink + '" stroke-width="2"/>' +
        '<text x="' + cx + '" y="' + (cy + 4) + '" text-anchor="middle" font-family="Libre Baskerville,Georgia,serif" font-size="19" font-style="italic" fill="#3A2C1E">' + esc(b.t) + '</text></g>';
    });
    B.spaces.forEach(function (p, i) {
      var w = i + 1, ink = bookOfWeek(w).ink;
      if (w < cur) {
        s += '<g><title>Week ' + w + ' · done</title><circle cx="' + p[0] + '" cy="' + p[1] + '" r="' + B.r + '" fill="' + ink + '" opacity=".9"/>' +
          '<path d="M' + (p[0] - 12) + ' ' + p[1] + ' l8 9 16 -18" stroke="#FFF8E9" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>';
      } else if (w === cur) {
        s += '<circle cx="' + p[0] + '" cy="' + p[1] + '" r="' + (B.r + 7) + '" fill="none" stroke="#C7922C" stroke-width="6"/>';
      } else {
        s += '<g><title>Week ' + w + '</title><circle cx="' + p[0] + '" cy="' + p[1] + '" r="' + (B.r + 1) + '" fill="#FBF3DF" opacity=".55"/></g>';
      }
    });
    /* today's space: the gold ring and the lesson tag (no portrait on the map, Bethany Nov 12 2026) */
    var mx = here[0], my = here[1];
    var label = 'LESSON ' + L.week + '.' + (typeof L.day === 'number' ? L.day : 4), bw = 22 + label.length * 11;
    var bx = Math.max(8, Math.min(B.w - bw - 8, mx - bw / 2)); my = my - 66;   /* tag sits just above the ring */
    s += '<rect x="' + bx + '" y="' + (my - 19) + '" width="' + bw + '" height="38" rx="19" fill="#8B3A20"/>' +
      '<text x="' + (bx + bw / 2) + '" y="' + (my + 7) + '" text-anchor="middle" font-family="Nunito,sans-serif" font-weight="800" font-size="19" fill="#FFF8E9">' + label + '</text>';
    svg.innerHTML = s;
    card.appendChild(svg);
    card.appendChild(h('p', { 'class': 'g5-board-note', text: 'Every colored space is one week. The gold ring shows where you are, all the way to Finish.' }));
    if (old) { old.hidden = true; old.style.display = 'none'; old.classList.add('g5-board-old'); }
    rp.insertBefore(card, rp.firstChild);   /* back at the top of Reading (Bethany, Nov 12 2026) */
  }

  /* ── today's reading, said plainly at the top of the Reading tab, with the tab's order:
     the card lists the jobs in order and each job gets a matching "Step N" chip, so a student
     always knows what comes first (Bethany, Nov 12 2026: read first, or the courage activity first?) ── */
  function buildReadNow() {
    var rp = panel('reading'); if (!rp || !L.chapters || rp.querySelector('.g5-readnow')) return;
    var card = h('div', { 'class': 'g5-readnow' });
    card.innerHTML = '<div class="g5-readnow-ico" aria-hidden="true"></div><div class="g5-readnow-main"><div class="g5-readnow-k">Today’s reading</div>' +
      '<div class="g5-readnow-t">' + (D.readnow && D.readnow.text ? esc(D.readnow.text) : 'Read <b>' + esc(L.chapters) + '</b> of <em>' + esc(L.bookTitle) + '</em> in your book.') + '</div>' +
      '<div class="g5-readnow-s">On this tab, in order:</div><ol class="g5-readnow-steps"></ol></div>';
    var li = rp.querySelector(':scope > .g5-listen');
    if (li) afterNode(li, card); else rp.insertBefore(card, rp.firstChild);
    function paintSteps() {
      var ol = card.querySelector('.g5-readnow-steps'); ol.innerHTML = '';
      rp.querySelectorAll('[data-g5-step]').forEach(function (c) { c.removeAttribute('data-g5-step'); });
      var n = 0;
      Array.prototype.forEach.call(rp.children, function (el) {
        if (el.offsetParent === null && getComputedStyle(el).display === 'none') return;
        var label = null, host = null, t;
        if (el.classList.contains('activity')) {
          t = (el.querySelector('.activity-title') || el).textContent;
          host = el.querySelector('.activity-title');
          if (/Chapter Introduction/i.test(t)) label = D.readnow && D.readnow.step ? esc(D.readnow.step) : '<b>Read ' + esc(L.chapters) + '</b> in your book';
          else if (/Virtue/i.test(t)) label = 'Learn the virtue: <b>' + esc(t.replace(/^\W*Virtue Watch:?\s*/i, '').trim().toLowerCase()) + '</b> (before you read)';
          else label = esc(t.replace(/^[^A-Za-z]+/, '').trim());
        } else if (el.classList.contains('g5-virtue')) {
          host = el.querySelector('.g5-virtue-t'); label = 'Virtue Watch: <b>' + esc(host.textContent) + '</b> (after you read)';
        } else if (el.classList.contains('rwm-box')) {
          host = el.querySelector('.rwm-header'); label = 'The <b>Read Like a Writer</b> box';
        }
        if (!label || !host) return;
        n++;
        ol.insertAdjacentHTML('beforeend', '<li>' + label + '</li>');
        host.setAttribute('data-g5-step', n);   /* drawn by CSS, so it never becomes part of the title text */
      });
      card.querySelector('.g5-readnow-s').hidden = n < 2; ol.hidden = n < 2;
    }
    paintSteps();
    window.addEventListener('load', function () { setTimeout(paintSteps, 1000); });   /* after onestep.js has moved things */
  }

  /* ── Virtue Watch, active: the page's own Virtue Watch introduces the virtue; after the
     reading, one short job at the end of the Reading tab. The kind changes across the week
     (DATA.virtue.kind): sort (Courage or not?), log (tap the bravest moment + one line),
     meter (slide how brave, one line, then Mason's take), best (bravest of the week).
     The week's answers are kept together (oao.g5ela.virtue.wk<NN>) and go into My Work. */
  function buildVirtue() {
    var V = D.virtue; if (!V || !V.kind) return;
    var rp = panel(V.tab || 'reading'); if (!rp) return;
    var wkKey = 'virtue.wk' + L.week, all = store(wkKey) || {}, mine = all[L.day] || {};
    function save() { all[L.day] = mine; store(wkKey, all); if (typeof window.gatherAnswers === 'function') try { window.gatherAnswers(); } catch (e) {} }
    var Name = V.name.charAt(0).toUpperCase() + V.name.slice(1);
    var card = h('div', { 'class': 'g5-card g5-virtue' });
    card.innerHTML = '<div class="g5-virtue-head"><span class="g5-virtue-ico" aria-hidden="true"></span><div>' +
      '<div class="g5-card-k">Virtue Watch · after you read</div><div class="g5-virtue-t">' + esc(V.title) + '</div></div></div>' +
      (V.intro ? '<p class="g5-virtue-intro">' + esc(V.intro) + '</p>' : '');
    function lineBox(ph) {
      var ta = h('textarea', { 'class': 'journal-box g5-virtue-ta', rows: '2', placeholder: ph || 'It took ' + V.name + ' because…' });
      ta.value = mine.why || '';
      ta.addEventListener('input', function () { mine.why = ta.value; save(); });
      return ta;
    }
    function choiceList(opts, onPick) {
      var g = h('div', { 'class': 'g5-virtue-opts', role: 'group' });
      opts.forEach(function (o, i) {
        var b = h('button', { type: 'button', 'class': 'g5-virtue-opt', 'aria-pressed': mine.pick === i ? 'true' : 'false' }, [o.t]);
        b.addEventListener('click', function () {
          mine.pick = i; mine.pickText = o.t;
          g.querySelectorAll('.g5-virtue-opt').forEach(function (x, j) { x.setAttribute('aria-pressed', j === i ? 'true' : 'false'); });
          save(); onPick && onPick(i);
        });
        g.appendChild(b);
      });
      return g;
    }
    if (V.kind === 'sort') {
      mine.sort = mine.sort || {};
      V.items.forEach(function (it, i) {
        var row = h('div', { 'class': 'g5-virtue-row' });
        row.appendChild(h('p', { 'class': 'g5-virtue-moment', text: it.t }));
        var btns = h('div', { 'class': 'g5-virtue-btns' }), fb = h('p', { 'class': 'g5-virtue-fb', 'aria-live': 'polite' });
        [[true, Name], [false, 'Not ' + V.name]].forEach(function (pair) {
          var b = h('button', { type: 'button', 'class': 'g5-btn g5-virtue-sortbtn' }, [pair[1]]);
          b.addEventListener('click', function () { mine.sort[i] = pair[0]; paintRow(); save(); });
          btns.appendChild(b);
        });
        function paintRow() {
          var a = mine.sort[i]; if (a === undefined) return;
          var right = a === it.ok;
          btns.querySelectorAll('button').forEach(function (b, j) { b.setAttribute('aria-pressed', (j === 0) === a ? 'true' : 'false'); });
          fb.className = 'g5-virtue-fb ' + (right ? 'ok' : 'no');
          fb.textContent = (right ? '✓ Yes. ' : 'Look again. ') + it.why;
        }
        row.appendChild(btns); row.appendChild(fb); card.appendChild(row); paintRow();
      });
    } else if (V.kind === 'log' || V.kind === 'best') {
      if (V.kind === 'best') {
        var past = [];
        Object.keys(all).sort().forEach(function (d) { if (+d !== L.day && all[d] && (all[d].pickText || all[d].why)) past.push(all[d]); });
        if (past.length) {
          var lg = h('div', { 'class': 'g5-virtue-log' }, [h('div', { 'class': 'g5-virtue-log-h', text: 'Your Virtue log this week' })]);
          past.forEach(function (x) { lg.appendChild(h('p', { text: (x.pickText ? x.pickText + ' ' : '') + (x.why ? '“' + x.why.trim() + '”' : '') })); });
          card.appendChild(lg);
        }
      }
      card.appendChild(choiceList(V.options));
      card.appendChild(h('p', { 'class': 'g5-virtue-q', text: V.line || 'Finish the sentence.' }));
      card.appendChild(lineBox(V.placeholder));
    } else if (V.kind === 'meter') {
      card.appendChild(h('p', { 'class': 'g5-virtue-moment', text: V.moment }));
      card.appendChild(h('p', { 'class': 'g5-virtue-q', text: V.ask }));
      var lab = V.scale || ['Not brave', 'A little brave', 'Somewhat brave', 'Brave', 'Very brave'];
      var wrap = h('div', { 'class': 'g5-virtue-meter' });
      var sl = h('input', { type: 'range', min: '1', max: String(lab.length), step: '1', value: String(mine.score || 3), 'aria-label': V.ask });
      var out = h('div', { 'class': 'g5-virtue-meter-out', 'aria-live': 'polite' });
      var take = h('div', { 'class': 'g5-virtue-take', hidden: 'hidden' });
      take.innerHTML = '<img src="assets/companions/mason-v2.jpg" alt="" class="g5-virtue-take-av"><p></p>';
      take.querySelector('p').textContent = V.take;
      function paintM() { out.textContent = lab[(+sl.value) - 1]; }
      sl.addEventListener('input', function () { mine.score = +sl.value; mine.scoreLabel = lab[mine.score - 1]; paintM(); take.hidden = false; save(); });
      wrap.appendChild(sl); wrap.appendChild(out);
      var ends = h('div', { 'class': 'g5-virtue-ends' }, [h('span', { text: lab[0] }), h('span', { text: lab[lab.length - 1] })]);
      card.appendChild(wrap); card.appendChild(ends); paintM();
      card.appendChild(h('p', { 'class': 'g5-virtue-q', text: V.line }));
      card.appendChild(lineBox(V.placeholder));
      card.appendChild(take);
      if (mine.score) take.hidden = false;
    }
    /* after the Quick check if there is one, else after the reading activity */
    var checks = rp.querySelectorAll(':scope > .g5-check'), at = checks.length ? checks[checks.length - 1] : activityByTitle('Chapter Introduction', rp);
    if (at) afterNode(at, card); else { var nx = rp.querySelector(':scope > .tab-next-wrap'); rp.insertBefore(card, nx); }

    var orig = window.gatherAnswers;
    if (typeof orig === 'function' && !orig.__g5virtue) {
      var wrapped = function () {
        var r = orig.apply(this, arguments), o = document.getElementById('gatheredOutput');
        if (o) {
          var t = '';
          if (V.kind === 'sort') V.items.forEach(function (it, i) { if (mine.sort && mine.sort[i] !== undefined) t += (mine.sort[i] === it.ok ? '✅ ' : '⬜ ') + it.t + '\n'; });
          else {
            if (mine.pickText) t += 'Moment: ' + mine.pickText + '\n';
            if (mine.scoreLabel) t += 'Rating: ' + mine.scoreLabel + '\n';
            t += (mine.why && mine.why.trim()) || '(no answer)';
            t += '\n';
          }
          if (t) o.value += '\n🏮 VIRTUE WATCH: ' + Name.toUpperCase() + '\n────────────────────────────────\n' + t;
        }
        return r;
      };
      wrapped.__g5virtue = true; window.gatherAnswers = wrapped;
    }
  }

  /* ── the compact banner (Bethany, Nov 12 2026: "match the condensed version", as in G3/G4 buildTop) ──
     One navy row: the Optima logo, the title, a meta line (Lesson · Week), a 🔊 Read aloud pill that opens
     the page's own read-aloud player, and an ⓘ Lesson details pill holding the unit/week/reading/focus
     cells and the standards. Nothing is deleted: the original nodes are moved or hidden, so the lesson's
     own scripts keep working. Logo and navy color stay. */
  function buildTop() {
    var header = document.querySelector('.header'); if (!header || header.classList.contains('g5-hd')) return;
    var root = document.documentElement;
    root.classList.add('g5-top'); header.classList.add('g5-hd');
    var title = header.querySelector('.header-title'), badge = header.querySelector('.header-badge-text');
    var meta = h('div', { 'class': 'g5-hd-meta' }), bits = [];
    if (badge && badge.textContent.trim()) bits.push('<b>' + esc(badge.textContent.trim()) + '</b>');
    if (L.week) bits.push('Week ' + L.week);
    meta.innerHTML = bits.join(' · ');
    if (title) title.appendChild(meta);
    var tools = h('div', { 'class': 'g5-hd-tools' }); header.appendChild(tools);
    var after = header;
    var panels = [];
    function pnl() { var pn = h('div', { 'class': 'g5-hd-panel' }); afterNode(after, pn); after = pn; panels.push(pn); return pn; }
    /* the panels open right under the banner, above the key line and Start here (built later) */
    function placePanels() { var a = header; panels.forEach(function (pn) { afterNode(a, pn); a = pn; }); }
    setTimeout(placePanels, 0);
    window.addEventListener('load', function () { setTimeout(placePanels, 950); });
    function pill(label, pn) {
      var b = h('button', { type: 'button', 'class': 'g5-pill', 'aria-expanded': 'false', html: label });
      b.addEventListener('click', function () {
        var open = !pn.classList.contains('open');
        document.querySelectorAll('.g5-hd-panel.open').forEach(function (x) { x.classList.remove('open'); });
        document.querySelectorAll('.g5-pill[aria-expanded="true"]').forEach(function (x) { x.setAttribute('aria-expanded', 'false'); });
        if (open) { pn.classList.add('open'); b.setAttribute('aria-expanded', 'true'); }
      });
      tools.appendChild(b); return b;
    }
    var ra = document.getElementById('optima-read-aloud');
    if (ra) { var rp = pnl(); rp.classList.add('g5-hd-ra'); rp.appendChild(ra); pill('🔊 Read aloud', rp); }
    var dl = '';
    document.querySelectorAll('.info-strip .info-cell').forEach(function (c) {
      var l = c.querySelector('.info-label'), v = c.querySelector('.info-value'), d = c.querySelector('.info-detail');
      if (!l || !v) return;
      dl += '<dt>' + esc(l.textContent.trim()) + '</dt><dd><b>' + esc(v.textContent.trim()) + '</b>' +
        (d && d.textContent.trim() ? ' · ' + esc(d.textContent.replace(/\s+/g, ' ').trim()) : '') + '</dd>';
    });
    document.querySelectorAll('.standards-panel .standards-group').forEach(function (g) {
      var l = g.querySelector('.standards-group-label');
      var codes = Array.prototype.map.call(g.querySelectorAll('.standards-codes span, .fl-code, .tx-code'), function (x) { return x.textContent.trim(); })
        .filter(function (x, i, a) { return x && x !== '·' && a.indexOf(x) === i; });
      if (!l || !codes.length) return;
      dl += '<dt>' + esc(l.textContent.trim()) + '</dt><dd class="g5-std">' + codes.map(esc).join(' · ') + '</dd>';
    });
    if (dl) { var dp = pnl(); dp.innerHTML = '<dl>' + dl + '</dl>'; pill('ⓘ Lesson details', dp); }
    function mark(id) { root.setAttribute('data-g5-tab', id || 'warmup'); }
    var active = document.querySelector('.tab-panel.active');
    mark(active && active.id ? active.id.replace(/^tab-/, '') : 'warmup');
    var inner = window.switchTab;
    if (typeof inner === 'function') window.switchTab = function (id) { var r = inner.apply(this, arguments); mark(id); return r; };
  }

  /* ── spot ornaments: the same pen-and-ink set and the same places as G4 ELA ──
     A divider before every tab's Next button (two designs, alternating) and one
     under the opening card; ivy in the corner of the opening card and the book
     page; the quill on the Writer's Workshop; the blossom on Poetry Corner.
     All decorative: CSS backgrounds or aria-hidden, so a screen reader never meets them. */
  function buildOrnaments() {
    var O = { divider: 'divider.png', divider2: 'divider-books.png', corner: 'corner.png', quill: 'quill.png', blossom: 'blossom.png' };
    var root = document.documentElement;
    Object.keys(O).forEach(function (k) { root.style.setProperty('--g5-orn-' + k, 'url("assets/ornaments/' + O[k] + '")'); });
    function rule(alt) { return h('div', { 'class': 'g5-divider' + (alt ? ' g5-divider-b' : ''), 'aria-hidden': 'true' }); }
    var n = 0;
    document.querySelectorAll('.tab-panel > .tab-next-wrap').forEach(function (w) {
      if (w.previousElementSibling && w.previousElementSibling.classList.contains('g5-divider')) return;
      w.parentNode.insertBefore(rule(n++ % 2), w);
    });
    var hook = document.querySelector('.g5-hook');
    if (hook && !(hook.nextElementSibling && hook.nextElementSibling.classList.contains('g5-divider'))) afterNode(hook, rule(false));
    document.querySelectorAll('.activity > .activity-head').forEach(function (hd) {
      var t = (hd.querySelector('.activity-title') || hd).textContent;
      if (/Writer.s Workshop/i.test(t)) hd.classList.add('g5-orn-quill');
      else if (/Poetry/i.test(t)) hd.classList.add('g5-orn-blossom');
    });
  }

  /* ── boot, in page order ──────────────────────────────────── */
  function boot() {
    guard('theme', buildTheme);
    guard('top', buildTop);
    guard('listen', buildListen);
    guard('hook', buildHook);
    guard('art', buildArt);
    guard('board', buildBoard);
    guard('how', buildHow);
    guard('lens', buildLens);
    guard('icons', buildIcons);
    guard('glossary', buildGlossary);
    guard('wordsay', buildWordSay);
    guard('hints', buildHints);
    guard('miss', buildMiss);
    guard('stones', buildStones);
    guard('footprints', buildFootprints);
    guard('fire', buildFire);
    guard('spy', buildSpyglass);
    guard('lantern', buildLanterns);
    guard('voice', buildVoice);
    guard('corn', buildCorn);
    guard('scale', buildScale);
    guard('strait', buildStrait);
    guard('cards', buildCards);
    guard('checks', buildChecks);
    guard('virtue', buildVirtue);
    guard('readnow', buildReadNow);
    guard('book', buildBook);
    guard('ornaments', buildOrnaments);
    guard('ribbon', buildRibbon);
    guard('nav', buildNav);
    window.__g5SparkleAPI = {
      teardown: function () {
        document.querySelectorAll('.g5-say, .g5-board, .g5-readnow, .g5-virtue, .g5-divider, .g5-lens, .g5-lens-mark, .g5-lens-use, .g5-listen, .g5-hook, .g5-check, .g5-do, .g5-plate, .g5-extra, .g5-game, .g5-page, .g5-ribbon, .g5-modal, .g5-marble, .g5-kicker, .g5-miss, .g5-hint-b, .g5-hint').forEach(function (n) { n.remove(); });
        document.querySelectorAll('.g5-gloss').forEach(function (b) { b.replaceWith(document.createTextNode(b.textContent)); }); document.querySelectorAll('.g5-gloss-tip').forEach(function (t) { t.remove(); });
        document.documentElement.classList.remove('g5-on');
        return document.querySelectorAll('.g5-listen, .g5-hook, .g5-check, .g5-do, .g5-plate, .g5-extra, .g5-game, .g5-page, .g5-ribbon, .g5-modal, .g5-marble, .g5-kicker, .g5-miss, .g5-hint-b, .g5-gloss').length;
      }
    };
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();

/* One step at a time (onestep.js), on for every sparkled lesson since Nov 10 2026; ?steps=0 turns it off */
(function () { try { if (/[?&]steps=0/.test(location.search)) return;
  var l = document.createElement("link"); l.rel = "stylesheet"; l.href = "onestep.css"; document.head.appendChild(l);
  var s = document.createElement("script"); s.src = "onestep.js"; document.body.appendChild(s); } catch (e) {} })();
