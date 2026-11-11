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

  /* split an activity body into steps */
  function chunks(body) {
    var out = [], cur = null, glue = false, prev = null;
    [].slice.call(body.children).forEach(function (k) {
      if (k.matches('.g5-do, .nav-do')) { k.classList.add('os-off'); return; }
      var media = k.matches('.spk-guide-wrap, .spk-guide');
      var afterEx = prev && prev.matches('.task-box, .key-concept') && k.tagName === 'P';   // the line that explains an example stays with it
      var attach = !cur || media ? false :
        glue || afterEx || k.tagName === 'BUTTON' || !shown(k) ||
        k.matches('.spk-write-tools, .dol-answer, .task-box, .match-game, .sort-game, .fillin-game, .spotter-game, .vocab-grid, .decode-steps, .textbox-prompt, textarea, .journal-label, .spk-wc, .spk-coach, .spk-notes-use, .saved-dot');   // a question and its answer box are one step
      if (!attach) { cur = []; out.push(cur); }
      cur.push(k); prev = k;
      // an instruction line or a "notice" heading belongs with what follows it
      var decor = k.matches('.spk-arc-head, .spk-ornament');   // a picture-only ornament is not a step
      glue = decor || (k.matches('.open-book-wrap, .oao-bh-head, .spk-goal, .callout, .g3-model-h, .key-concept, .spk-copia-seed') || (k.tagName === 'P' && !k.querySelector('textarea,input'))) && !k.matches('.swyk');
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

      var bar = el('div', 'os-bar');
      var dots = el('div', 'os-dots');
      steps.forEach(function () { dots.appendChild(el('span', 'os-dot')); });
      var back = el('button', 'os-back', '◂ Back'); back.type = 'button';
      var next = el('button', 'os-next dol-check-btn', 'Next'); next.type = 'button';
      bar.appendChild(back); bar.appendChild(dots); bar.appendChild(next);
      body.appendChild(bar);
      if (steps.length < 2) dots.style.visibility = 'hidden';

      var head = act.querySelector(':scope > .activity-head, :scope > .spk-card-head');
      var check = el('span', 'os-check', '✓');
      if (head) head.appendChild(check);
      return { act: act, body: body, steps: steps, at: 0, back: back, next: next, dots: dots, head: head };
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
      var s = state[i]; s.at = j;
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
    oneQuestion();
    document.querySelectorAll('.tab-panel').forEach(setup);
  }
  if (document.readyState === 'complete') setTimeout(boot, 400);
  else window.addEventListener('load', function () { setTimeout(boot, 400); });
})();
