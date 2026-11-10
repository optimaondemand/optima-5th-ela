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
    if (nowPlaying) { nowPlaying.pause(); if (nowPlaying._btn) nowPlaying._btn.classList.remove('g5-playing'); if (nowPlaying._btn === btn) { nowPlaying = null; return; } }
    var a = new Audio(url); a._btn = btn; nowPlaying = a;
    btn && btn.classList.add('g5-playing');
    a.addEventListener('ended', function () { btn && btn.classList.remove('g5-playing'); nowPlaying = null; });
    a.play().catch(function () { btn && btn.classList.remove('g5-playing'); });
  }
  function clip(path) { return (window.__G5_CLIPS && window.__G5_CLIPS[path]) || path; }  // preview builds inline clips
  function audioUrl(slot) { return clip('assets/audio/guide/g5ela-' + L.week + '-' + L.day + '-' + slot + '.mp3'); }
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

  /* ── 3. Listen cards (plain narrator, no character) ───────── */
  function buildListen() {
    if (!D.listen) return;
    ['page', 'warmup', 'words', 'reading', 'assignment'].forEach(function (tab) {
      var c = D.listen[tab]; if (!c || !c.text) return;
      var slot = c.clip || ('listen-' + tab);
      var play_ = h('button', { 'class': 'g5-listen-play', type: 'button', hidden: 'hidden', 'aria-label': 'Play' }, ['▶ Listen']);
      var words_ = h('details', { 'class': 'g5-listen-words' }, [h('summary', { text: 'Read the words instead' }), h('p', { text: c.text })]);
      var card = h('div', { 'class': 'g5-listen', 'data-tab': tab }, [
        h('span', { 'class': 'g5-listen-ico', 'aria-hidden': 'true', html: '<svg viewBox="0 0 24 24" width="22" height="22"><path fill="currentColor" d="M12 3a9 9 0 0 0-9 9v6a3 3 0 0 0 3 3h1a1 1 0 0 0 1-1v-6a1 1 0 0 0-1-1H5v-1a7 7 0 0 1 14 0v1h-2a1 1 0 0 0-1 1v6a1 1 0 0 0 1 1h1a3 3 0 0 0 3-3v-6a9 9 0 0 0-9-9z"/></svg>' }),
        h('div', { 'class': 'g5-listen-main' }, [h('div', { 'class': 'g5-listen-t', text: 'Listen' }), play_, words_])
      ]);
      play_.addEventListener('click', function () { play(audioUrl(slot), play_); });
      fileExists(audioUrl(slot), function (ok) { if (ok) { play_.hidden = false; words_.querySelector('summary').textContent = 'Read the words'; } else { words_.open = true; } });
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
      var walker = document.createTreeWalker(scope, NodeFilter.SHOW_TEXT, {
        acceptNode: function (n) {
          var p = n.parentNode;
          if (!p || p.closest('button, textarea, input, script, style, .g5-gloss, .g5-do, .activity-title, summary')) return NodeFilter.FILTER_REJECT;
          return re.test(n.nodeValue) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_SKIP;
        }
      });
      var node = walker.nextNode(); if (!node) return;
      var m = re.exec(node.nodeValue);
      var after = node.splitText(m.index); after.nodeValue = after.nodeValue.slice(m[0].length);
      var btn = h('button', { type: 'button', 'class': 'g5-gloss', 'aria-expanded': 'false' }, [m[0]]);
      var tip = h('span', { 'class': 'g5-gloss-tip', role: 'note', hidden: 'hidden', text: G.meaning });
      btn.addEventListener('click', function (e) { e.stopPropagation(); var open = tip.hidden; tip.hidden = !open; btn.setAttribute('aria-expanded', open ? 'true' : 'false'); });
      node.parentNode.insertBefore(btn, after);
      node.parentNode.insertBefore(tip, after);
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
    k.innerHTML = '<span><b>👆</b> You can tap it.</span><span><b>🔊</b> You can listen.</span><span><b class="nav-dot">dotted word</b> Tap it to see what it means.</span>';
    afterNode(hdr, k);
    var src = window.NAV_HOWTO_SRC || 'assets/video/g5ela-howto.mp4';
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

  /* ── boot, in page order ──────────────────────────────────── */
  function boot() {
    guard('theme', buildTheme);
    guard('listen', buildListen);
    guard('hook', buildHook);
    guard('art', buildArt);
    guard('how', buildHow);
    guard('glossary', buildGlossary);
    guard('hints', buildHints);
    guard('miss', buildMiss);
    guard('stones', buildStones);
    guard('checks', buildChecks);
    guard('cards', buildCards);
    guard('book', buildBook);
    guard('ribbon', buildRibbon);
    guard('nav', buildNav);
    window.__g5SparkleAPI = {
      teardown: function () {
        document.querySelectorAll('.g5-listen, .g5-hook, .g5-check, .g5-do, .g5-plate, .g5-extra, .g5-game, .g5-page, .g5-ribbon, .g5-modal, .g5-marble, .g5-kicker, .g5-miss, .g5-hint-b, .g5-hint').forEach(function (n) { n.remove(); });
        document.querySelectorAll('.g5-gloss').forEach(function (b) { var t = b.nextSibling; b.replaceWith(document.createTextNode(b.textContent)); if (t && t.classList && t.classList.contains('g5-gloss-tip')) t.remove(); });
        document.documentElement.classList.remove('g5-on');
        return document.querySelectorAll('.g5-listen, .g5-hook, .g5-check, .g5-do, .g5-plate, .g5-extra, .g5-game, .g5-page, .g5-ribbon, .g5-modal, .g5-marble, .g5-kicker, .g5-miss, .g5-hint-b, .g5-gloss').length;
      }
    };
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
