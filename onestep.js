/* One step at a time (prototype, Nov 2026, G4 + G5 ELA pilot review).
   Bethany: "too many words ... show one thing at a time, step by step,
   guide them, think like we are holding their hand."

   Per tab:
   - one activity open at a time; the others are short rows (title + ✓)
   - inside the open activity, one step at a time with Back / Next
   - the "Day 1: Notice ..." line, the Level badge and the What to do box
     are hidden (the step itself says what to do)
   Nothing is removed from the page: hidden parts keep their answers, so
   saving, the My Work download and progress still work. */
(function () {
  if (window.__oneStep) return; window.__oneStep = true;

  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }
  function shown(n) { return n.nodeType === 1 && getComputedStyle(n).display !== 'none'; }
  function titleOf(act) { var t = act.querySelector('.activity-title, .spk-card-title, .oao-bh-title, [class*="-title"]'); return t ? t.textContent.replace(/\s+/g, ' ').trim() : ''; }
  function isWhole(act) { return act.classList.contains('g5-game') || act.querySelector('.g5-river, .spk-wg, .wordgame, [class*="spk-wg"]'); }


  /* ══ PILOT IMPROVEMENTS (Nov 11 2026) ══════════════════════════════
     1 a box for the Daily Oral Language fix   3 long steps split, How to Do It folded
     5 "Step 3 of 27"                          6 finish = copy, then paste in Canvas
     8 activity numbers hidden                 9 a shorter top (G5)
     10 What Good Readers Do always on Warm-Up; later-chapter word tags say so */

  /* ── ROUND 3 (Nov 11 2026): the words match the copy-and-paste finish; no direction is lost or left pointing at nothing ── */
  function swap(root, rx, to) {
    if (!root) return; var w = document.createTreeWalker(root, 4, null), nd, hit = [];
    while ((nd = w.nextNode())) if (rx.test(nd.nodeValue)) hit.push(nd);
    hit.forEach(function (x) { x.nodeValue = x.nodeValue.replace(rx, to); });
  }
  function finishWords() {
    var acts = document.querySelector('.gathered-actions'); if (!acts) return;
    var panel = acts.closest('.tab-panel') || document.body;
    swap(panel, /Review, Copy,? or Download/i, 'Copy Your Work');
    swap(panel, /Copy to paste into Canvas, or download[^.]*\./i, 'Copy it, then paste it in Canvas.');
    swap(panel, /copy or download( your work)? at the bottom/i, 'copy your work at the bottom and paste it in Canvas');
    swap(panel, /I copied or downloaded my work and submitted it to Canvas/i, 'I copied my work, pasted it in Canvas, and submitted it');
    if (!titled(/Read Like a Writer/i).length && !document.querySelector('.rwm-step-label'))
      swap(panel, /\s*[—-]+\s*including your three RWM responses from the Reading tab/i, '');
    /* the questions are on the step before, not "above" */
    swap(document.body, /The Pause & Think prompts are above — look them over first, then stop at each one as you read\./, 'Stop at each Pause & Think question as you read. Tap ◂ Back to see the questions again.');
  }
  /* G5: one-step hides the What to do box, but on Reading and What Good Readers Do it held the only directions ("Open your book and read Chapters 3-4") */
  function g5Todo() {
    if (!document.body.classList.contains('os-g5')) return;
    titled(/Reading\b|What Good Readers Do/i).forEach(function (a) {
      var body = a.querySelector(':scope > .activity-body'), d = body && body.querySelector(':scope > .g5-do'), lis = d && d.querySelectorAll('ol > li');
      if (!lis || !lis.length || body.querySelector('.os-todo')) return;
      var box = el('div', 'callout os-todo'), ol = el('ol'); box.appendChild(el('b', '', 'What to do'));
      [].forEach.call(lis, function (li) { ol.appendChild(el('li', '', li.textContent.replace(/\s+/g, ' ').trim())); });
      box.appendChild(ol); body.insertBefore(box, d.nextSibling);
    });
  }
  var ALL = [];
  function words(n) { return ((n.textContent || '').replace(/\s+/g, ' ').trim().match(/\S+/g) || []).length; }
  function titled(rx) {
    return [].filter.call(document.querySelectorAll('.tab-panel .activity'), function (a) {
      var t = a.querySelector('.activity-title'); return t && rx.test(t.textContent);
    });
  }
  function moveWgrd() {
    var first = document.querySelector('.tab-panel'); if (!first) return;
    titled(/What Good Readers Do/i).forEach(function (a) {
      if (a.parentNode === first) return;
      first.insertBefore(a, first.querySelector(':scope > .activity, :scope > .spk-copia-card, :scope > .tab-next-wrap'));
    });
  }
  function foldHowTo() {
    titled(/What Good Readers Do/i).forEach(function (a) {
      var body = a.querySelector(':scope > .activity-body'); if (!body) return;
      [].forEach.call(body.querySelectorAll(':scope > .callout'), function (c) {
        if (!/^\W*How to Do It/i.test((c.textContent || '').trim()) || words(c) < 45) return;
        var d = el('details', 'nav-fold os-howto'); d.appendChild(el('summary', '', '💡 How to do it, step by step'));
        body.insertBefore(d, c); d.appendChild(c);
      });
    });
  }
  function dolBox() {
    titled(/Daily Oral Language/i).forEach(function (a) {
      var box = a.querySelector('.task-box'); if (!box || a.querySelector('textarea')) return;
      var ta = el('textarea', 'journal-box spk-onpage os-dolbox'); ta.id = 'dol-fix-box'; ta.rows = 2;
      ta.setAttribute('data-label', 'Daily Oral Language: my fixed sentence');
      ta.placeholder = 'Type the sentence here, with every fix made…';
      var key = (window._lessonKey || document.title) + '-dol-fix-box';
      try { var v = localStorage.getItem(key); if (v) ta.value = v; } catch (e) {}
      ta.addEventListener('input', function () {
        try { localStorage.setItem(key, ta.value); } catch (e) {}
        if (window.gatherAnswers) try { window.gatherAnswers(); } catch (e) {}
      });
      var btn = box.querySelector('.dol-check-btn');
      if (btn && btn.parentNode === box) box.insertBefore(ta, btn); else box.appendChild(ta);
    });
    /* the fix goes into the gathered work too (pages whose own gather does not know this box) */
    var g0 = window.gatherAnswers;
    if (typeof g0 === 'function' && !g0._os) {
      var g1 = function () {
        var r = g0.apply(this, arguments), out = document.querySelector('.gathered-output, #gatheredOutput'), ta = document.getElementById('dol-fix-box');
        if (out && ta && ta.value.trim() && out.value.indexOf(ta.value.trim()) < 0) out.value += '\n\n\u270f\ufe0f DAILY ORAL LANGUAGE\nMy fixed sentence: ' + ta.value.trim() + '\n';
        return r;
      };
      g1._os = true; window.gatherAnswers = g1; try { g1(); } catch (e) {}
    }
  }
  function finishOrder() {
    var acts = document.querySelector('.gathered-actions'), copy = acts && acts.querySelector('.gathered-btn-copy');
    if (!copy || acts.getAttribute('data-os')) return; acts.setAttribute('data-os', '1');
    var ol = el('ol', 'os-finish');
    ['Tap <b>Copy my work</b>.', 'Go back to this lesson’s assignment in Canvas.', '<b>Paste</b> your work in the box. Then tap <b>Submit</b>.']
      .forEach(function (h) { var li = el('li'); li.innerHTML = h; ol.appendChild(li); });
    acts.parentNode.insertBefore(ol, acts);
    [].slice.call(copy.childNodes).forEach(function (c) { if (c.nodeType === 3) copy.removeChild(c); });
    copy.appendChild(document.createTextNode(' Copy my work'));
    var more = el('details', 'os-more'); more.appendChild(el('summary', '', 'More ways to save your work'));
    var row = el('div', 'gathered-actions os-more-row');
    [].slice.call(acts.children).forEach(function (b) { if (b !== copy) row.appendChild(b); });
    if (row.children.length) { more.appendChild(row); acts.parentNode.insertBefore(more, acts.nextSibling); }
  }
  function shortTop() {
    if (!document.querySelector('link[href*="g5-sparkle"], script[src*="g5-sparkle"]')) return;
    document.body.classList.add('os-g5');
    var intro = document.querySelector('.page-wrap > .intro-section');
    if (intro && !intro.closest('details')) {
      var d = el('details', 'os-intro'); d.appendChild(el('summary', '', '🎯 Today’s Wonder and what you will learn'));
      intro.parentNode.insertBefore(d, intro); d.appendChild(intro);
    }
    var m = /Ch\.\s*(\d+)(?:\s*[–-]\s*(\d+))?/.exec(document.title), last = m ? +(m[2] || m[1]) : 0;
    if (last) [].forEach.call(document.querySelectorAll('.vocab-ch'), function (t) {
      var k = /Ch\.\s*(\d+)/.exec(t.textContent); if (k && +k[1] > last) t.textContent = 'coming up in Ch. ' + k[1];
    });
  }
  function paint(empty) {
    var tot = 0, at = [];
    ALL.forEach(function (st) { st.forEach(function (s) {
      for (var j = 0; j < s.steps.length; j++) { if (s.steps.length > 1 && empty(s, j)) continue; tot++; if (j <= s.at) at[ALL_ID(s)] = tot; }
    }); });
    ALL.forEach(function (st) { st.forEach(function (s) { if (s.count) s.count.textContent = 'Step ' + (at[ALL_ID(s)] || 1) + ' of ' + tot; }); });
  }
  var _ids = []; function ALL_ID(s) { var i = _ids.indexOf(s); if (i < 0) { _ids.push(s); i = _ids.length - 1; } return i; }

  /* split an activity body into steps */
  function chunks(body) {
    var out = [], cur = null, glue = false, prev = null;
    [].slice.call(body.children).forEach(function (k) {
      if (k.matches('.g5-do, .nav-do')) { k.classList.add('os-off'); return; }
      var media = k.matches('.spk-guide-wrap, .spk-guide');
      var afterEx = prev && prev.matches('.task-box, .key-concept') && k.tagName === 'P';   // the line that explains an example stays with it
      var attach = !cur || media ? false :
        glue || afterEx || k.tagName === 'BUTTON' || !shown(k) ||
        k.matches('.thinking-stop, .spk-write-tools, .dol-answer, .task-box, .match-game, .sort-game, .fillin-game, .spotter-game, .vocab-grid, .decode-steps, .textbox-prompt, textarea, .journal-label, .spk-wc, .spk-coach, .spk-notes-use, .saved-dot');   // a question and its answer box are one step
      if (attach && cur && k.matches('.key-concept, .callout') && !k.matches('.os-off') && shown(k) && !(prev && prev.tagName === 'P') &&
          cur.reduce(function (t, x) { return t + words(x); }, 0) > 70 && !cur.some(function (x) { return x.matches('textarea') || x.querySelector('textarea, input'); }) === true) attach = false;
      if (k.matches('.chapter-section-title')) attach = false;   // a chapter heading starts its own step and leads it
      if (cur && !media && k.id && /count|progress|score/i.test(k.id)) attach = true;   // a game's "0 of 6" counter stays with the game
      if (!attach) { cur = []; out.push(cur); }
      cur.push(k); prev = k;
      // an instruction line or a "notice" heading belongs with what follows it
      var decor = k.matches('.spk-arc-head, .spk-ornament');   // a picture-only ornament is not a step
      glue = decor || k.matches('.chapter-section-title') || (k.matches('.open-book-wrap, .oao-bh-head, .spk-goal, .callout, .g3-model-h, .key-concept, .spk-copia-seed') || (k.tagName === 'P' && !k.querySelector('textarea,input'))) && !k.matches('.swyk');
    });
    return out.filter(function (c) { return c.length; });
  }

  function setup(panel) {
    var acts = [].slice.call(panel.querySelectorAll(':scope > .activity, :scope > .spk-copia-card')).filter(function (a) {
      return !a.hasAttribute('data-oao-retired') && !a.hidden && a.style.display !== 'none' && getComputedStyle(a).display !== 'none';   // audit Nov 10: a retired Poetry Corner was still a stop, so Next led to a blank
    });
    if (!acts.length) return;
    var state = acts.map(function (act, i) {
      act.classList.add('os-act');
      var num = act.querySelector('.activity-num'); if (num && /^[0-9A-Z]{1,2}$/.test(num.textContent.trim())) num.classList.add('os-off');
      act.querySelectorAll('.activity-sub, .spk-card-sub, .rung-chip').forEach(function (n) { n.classList.add('os-off'); });
      act.querySelectorAll('.activity-head span, .activity-head div').forEach(function (n) {
        if (/level:/i.test(n.textContent) && n.children.length === 0) (n.closest('div[style*="margin-top"]') || n).classList.add('os-off');
      });
      var body = act.querySelector(':scope > .activity-body, :scope > .spk-card-body') || act;
      // a listen/watch clip that sits above the body becomes the activity's first step
      [].slice.call(act.querySelectorAll(':scope > .spk-guide-wrap, :scope > .spk-guide')).reverse().forEach(function (g) {
        if (body !== act) body.insertBefore(g, body.firstChild);
      });
      var steps = isWhole(act) ? [[].slice.call(body.children)] : chunks(body);
      steps.forEach(function (c, j) { c.forEach(function (n) { n.classList.add('os-part'); n.dataset.osStep = j; }); });
      steps.forEach(function (c) {
        var vis = c.filter(function (n) { return !n.classList.contains('os-off'); });
        if (steps.length > 1 && vis.length && vis.every(function (n) { return n.matches('.spk-guide-wrap, .spk-guide'); }) && !vis[vis.length - 1].querySelector('.os-hint'))
          vis[vis.length - 1].appendChild(el('p', 'os-hint', 'Listen. Then tap Next.'));
      });

      var bar = el('div', 'os-bar');
      var dots = el('div', 'os-dots');
      steps.forEach(function () { dots.appendChild(el('span', 'os-dot')); });
      var back = el('button', 'os-back', '◂ Back'); back.type = 'button';
      var next = el('button', 'os-next dol-check-btn', 'Next'); next.type = 'button';
      var count = el('span', 'os-count');
      bar.appendChild(back); bar.appendChild(dots); bar.appendChild(count); bar.appendChild(next);
      body.appendChild(bar);
      if (steps.length < 2) dots.style.visibility = 'hidden';

      var head = act.querySelector(':scope > .activity-head, :scope > .spk-card-head');
      var check = el('span', 'os-check', '✓');
      if (head) head.appendChild(check);
      return { act: act, body: body, steps: steps, at: 0, back: back, next: next, dots: dots, head: head, count: count };
    });

    function empty(s, j) {
      return !(s.steps[j] || []).some(function (n) {
        if (n.hidden) return false;
        if (n.matches('.spk-guide-wrap, .spk-guide')) return !!n.querySelector('.spk-audio:not([hidden]), .spk-media:not([hidden]), .spk-yt:not([hidden])') || (n.matches('.spk-guide') && !n.hidden);
        return true;
      });
    }
    function step(s, j, dir) { while (j > 0 && j < s.steps.length - 1 && empty(s, j)) j += dir; if (j === 0 && empty(s, 0) && s.steps.length > 1) j = 1; return j; }
    /* Nov 11 2026 (Bethany): Next must not move the page. Whatever was on screen
       stays where it was; only if the new step's title would end up above the
       sticky bars do we nudge it down into view (instantly, no glide). */
    function hold(el) { return el ? { el: el, top: el.getBoundingClientRect().top } : null; }
    function settle(h, act) {
      if (!h) return;
      var d = h.el.getBoundingClientRect().top - h.top;
      if (d) window.scrollBy(0, d);
      var t = act ? act.getBoundingClientRect().top : 0, pad = 110;
      if (act && t < pad) window.scrollBy(0, t - pad);
    }
    function show(i, j, scroll) {
      var h = scroll ? hold(panel.querySelector(':scope > .os-open') || state[i].act) : null;
      j = step(state[i], j, 1);
      state.forEach(function (s, k) {
        s.act.classList.toggle('os-open', k === i);
        s.act.classList.toggle('os-closed', k !== i);
      });
      var s = state[i]; s.at = j; paint(empty);
      s.body.querySelectorAll(':scope > .os-part').forEach(function (n) { n.classList.toggle('os-hide', +n.dataset.osStep !== j); });
      [].forEach.call(s.dots.children, function (d, k) { d.classList.toggle('on', k <= j); });
      s.back.style.visibility = (j > 1 || (j === 1 && !empty(s, 0))) ? 'visible' : 'hidden';
      var last = j >= s.steps.length - 1, after = state[i + 1];
      var label = last ? (after ? (after.title ? 'Next: ' + after.title : 'Next') : 'Done') : 'Next';
      var hand = s.next.querySelector('.nav-hand');
      s.next.textContent = label; if (hand) s.next.insertBefore(hand, s.next.firstChild);
      settle(h, s.act);
    }
    state.forEach(function (s, i) {
      s.title = titleOf(s.act).replace(/^[^A-Za-z]+/, '').split(':')[0];
      s.next.addEventListener('click', function () {
        if (s.at < s.steps.length - 1) return show(i, step(s, s.at + 1, 1), true);
        s.act.classList.add('os-done');
        if (state[i + 1]) show(i + 1, 0, true);
        else { var hd = hold(s.act); s.act.classList.remove('os-open'); s.act.classList.add('os-closed');
          settle(hd, null); }
      });
      s.back.addEventListener('click', function () { var j = s.at - 1; while (j > 0 && empty(s, j)) j--; if (j >= 0 && !(j === 0 && empty(s, 0))) show(i, j, true); });
      if (s.head) s.head.addEventListener('click', function () { if (s.act.classList.contains('os-closed')) show(i, s.act.classList.contains('os-done') ? 0 : s.at, true); });
    });
    ALL.push(state);
    show(0, 0, false);
  }

  /* think-question boxes: one question at a time is enough */
  function oneQuestion() {
    document.querySelectorAll('.tab-panel .callout').forEach(function (c) {
      if (!/Try these first|Think it through|Work through these|answer these/i.test(c.textContent)) return;
      var lis = c.querySelectorAll('li'); for (var i = 1; i < lis.length; i++) lis[i].classList.add('os-off');
    });
  }
  function boot() {
    if (!document.querySelector('.tab-panel .activity')) return;   // one-page lessons (fluency) stay as they are
    document.body.classList.add('os-on');
    try { moveWgrd(); foldHowTo(); dolBox(); finishOrder(); shortTop(); g5Todo(); finishWords(); } catch (e) {}
    oneQuestion();
    document.querySelectorAll('.tab-panel').forEach(setup);
  }
  if (document.readyState === 'complete') setTimeout(boot, 400);
  else window.addEventListener('load', function () { setTimeout(boot, 400); });
})();
