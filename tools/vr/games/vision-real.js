  /* ── Field Notes Day game: vision-real ──
     Each card is a moment from the chapters. Students sort it: a vision only Isaac saw, or something that really happened.
     A wrong pick gets the clue; a right pick shows the proof from the book. All cards right = field notes stamp. */
  var GAME = (function () {
    var G = D.game, $ = KIT.$, $$ = KIT.$$, esc = KIT.esc;
    var st = KIT.get('game', { got: [] });   /* got = indexes of cards sorted right */
    var LBL = { vision: '👁 Only Isaac saw it', real: '📍 It really happened' };
    function complete() { return st.got.length === G.cards.length; }
    function save() { KIT.set('game', st); }
    function render() {
      $('#vr-cards').innerHTML = G.cards.map(function (c, i) {
        var got = st.got.indexOf(i) > -1;
        return '<li class="vcard' + (got ? ' got ' + c.ans : '') + '"><div class="vc-t"><span class="vc-ch">' + esc(c.ch) + '</span>' + esc(c.t) + '</div>' +
          (got ? '<div class="vc-why"><b>' + esc(LBL[c.ans]) + '.</b> ' + esc(c.why) + '</div>'
               : '<div class="vc-btns">' + ['vision', 'real'].map(function (a) { return '<button type="button" class="vbtn" data-i="' + i + '" data-a="' + a + '">' + LBL[a] + '</button>'; }).join('') + '</div>') + '</li>';
      }).join('');
      $('#vr-tally').textContent = st.got.length + ' of ' + G.cards.length + ' sorted';
      $$('.vbtn', $('#vr-cards')).forEach(function (b) { b.addEventListener('click', function () {
        var i = +b.dataset.i, c = G.cards[i];
        if (b.dataset.a === c.ans) {
          st.got.push(i); save(); KIT.ding();
          KIT.say(complete() ? '✓ All sorted! You can tell Isaac’s visions from what really happened. Now plan your 2 sentences.' : '✓ Right.', true);
          if (complete()) KIT.fanfare();
          render();
        } else { KIT.bonk(); b.classList.add('no'); KIT.say(G.miss); }
      }); });
      KIT.done(complete()); KIT.refresh();
    }
    return { render: render, complete: complete };
  })();
