#!/usr/bin/env python3
"""Week 32 pages brought in line with the scope (v2_poetry scope week 32) and the approved plan
("G5 ELA Weeks 31-32: End-of-Year Wrap-Up Plan": Letter to a Future 5th Grader), approved by Bethany Nov 24 2026
(claude/g5-ela-wk32-scope-check.md). One strand per run, each its own commit:
    python tools/g5sparkle/scope_wk32.py packet|wgrd|rwm|poetry|fluency [--apply]
packet  = the Reflect and Assignment tabs build the letter packet (Day 1 Reader's Portrait + five Book Postcards + plan;
          Day 2 read-aloud passage + letter draft; Day 3 revise + Word Gift + P.S.; Day 4 envelope, recording, booklet);
          every 'portfolio/present' line re-pointed at the letter; 32.2's Reflect activity put back inside its tab panel;
          Optima's own quote strips credited plainly to Optima
wgrd    = What Good Readers Do on all four days, lenses (Name: tip): set purpose, gather evidence, reread, synthesize
rwm     = Read Like a Writer D1-D4: voice, tone and pacing (model, frames, apply, alone), lines checked against the books
          (Horn Spoon Ch. 18 and Ch. 1, Bowditch Ch. 12, Johnny Tremain Ch. 8; the same lines weeks 30-31 checked)
poetry  = Poetry Corner points at the Day 4 recording; the Day 4 list names only poems taught this year
fluency = the fluency page: the letter read aloud, then one poem from the year (one recording)"""
import io, re, sys
F = {1: 'lesson-32-1-portfolio-plan.html', 2: 'lesson-32-2-fluency-draft.html', 3: 'lesson-32-3-final-prep.html', 4: 'lesson-32-4-final-present.html', 'flu': 'lesson-32-fluency.html'}
def ta(id_, label, ph, ind='      '):
    return ('%s<textarea class="journal-box" id="%s" data-label="%s" placeholder="%s" oninput="autoSave(this,\'dot-%s\');"></textarea>\n'
            '%s<div class="journal-label">&#128211; <span class="saved-dot" id="dot-%s"></span></div>\n') % (ind, id_, label, ph, id_, ind, id_)
def swyk(label, prompt, box):
    return ('      <div class="swyk" style="margin-bottom:12px;">\n        <div class="swyk-label">%s</div>\n        <div class="swyk-prompt">%s</div>\n%s      </div>\n') % (label, prompt, box)
def act(cls, icon, title, sub, body, style=''):
    return ('<div class="activity %s"%s>\n    <div class="activity-head"><div class="activity-num" style="background:#F9A825;color:#0E1C42;">%s</div><div style="flex:1;">'
            '<div class="activity-title">%s</div><div class="activity-sub">%s</div></div></div>\n    <div class="activity-body">\n%s    </div>\n  </div>') % (cls, (' style="%s"' % style) if style else '', icon, title, sub, body)
def kc(label, ps):
    return '      <div class="key-concept"><div class="key-concept-label">%s</div>\n%s      </div>\n' % (label, ''.join('        <p%s>%s</p>\n' % ('' if i == 0 else ' style="margin-top:6px;"', p) for i, p in enumerate(ps)))
def prog(n):
    names = ['Plan', 'Draft', 'Revise', 'Seal &amp; Send']
    return '      <div class="workshop-progress">%s</div>\n' % ''.join('<span class="wp-step%s">%s%s</span>' % (' active' if i == n else '', '✓ ' if i < n else ('⭐ ' if i == n else ''), x) for i, x in enumerate(names))
def checklist(items):
    return '<div class="turn-in-checklist">' + ''.join('<div class="turn-in-item" onclick="toggleCheck(this)"><div class="turn-in-check"></div><div class="turn-in-item-text">%s</div></div>' % x for x in items) + '</div>'
def block(t, needle):
    if t.count(needle) != 1: raise SystemExit('needle %r x%d' % (needle[:50], t.count(needle)))
    k = t.find(needle); a = max(t.rfind('<div class="activity ', 0, k), t.rfind('<div class="activity"', 0, k)); depth = 0
    for m in re.finditer(r'<div\b|</div>', t[a:]):
        depth += 1 if m.group(0) == '<div' else -1
        if depth == 0: return a, a + m.end()
    raise SystemExit('no end')
def REPL_ACT(needle, new):
    def f(t):
        a, b = block(t, needle); return t[:a] + new + t[b:], 1
    return f
def REPL_CHK(items):
    def f(t):
        return re.subn(r'<div class="turn-in-checklist">(?:<div class="turn-in-item" onclick="toggleCheck\(this\)"><div class="turn-in-check"></div><div class="turn-in-item-text">.*?</div></div>)+</div>', lambda m: checklist(items), t)
    return f
def IN_ACT(needle, pairs):
    """plain replacements inside one activity only"""
    def f(t):
        a, b = block(t, needle); seg = t[a:b]
        for o, n in pairs:
            if o not in seg: raise SystemExit('IN_ACT miss %r' % o[:60])
            seg = seg.replace(o, n)
        return t[:a] + seg + t[b:], 1
    return f
NOTE = '      <p style="font-size:13px;color:#7A88A8;font-style:italic;margin:8px 0 0;">%s</p>\n'
STRIP_ATTR = (re.compile(r'(<div class="quote-strip-attr">)[^<]*(</div>)'), lambda m: m.group(1) + 'Optima Academy Online &bull; 5th Grade ELA' + m.group(2), 1)
SUBHEAD = ('Portfolio, Presentation &amp; Year-End Synthesis', 'Reader-Writer Portfolio: Letter to a Future 5th Grader', 1)
SWYK_WORD = (re.compile(r'\bSWYK\b'), lambda m: 'Show What You Know', None)
BOOKS = ['The Witch of Blackbird Pond', 'Johnny Tremain', 'Carry On, Mr. Bowditch', 'How I Became a Ghost', 'By the Great Horn Spoon!']
# ---------------- Day 1
D1_REFLECT = act('bl-gold', '✉️', 'Reader&rsquo;s Portrait and Book Postcards', 'The opening of your letter, and one postcard for each novel',
  kc('📦 Your Letter Packet (all week)', [
     '<strong>Day 1:</strong> your Reader&rsquo;s Portrait and five Book Postcards (today)',
     '<strong>Day 2:</strong> the letter: which novel should a new 5th grader read first, and why?',
     '<strong>Day 3:</strong> revise the letter, then add a Word Gift and a P.S.',
     '<strong>Day 4:</strong> design the envelope, then record your letter and one poem',
     'Your letter is real. Your teacher can pass it on to next year&rsquo;s 5th graders.'])
  + swyk('✉️ Reader&rsquo;s Portrait', 'This is how your letter begins. Start with <em>When I started 5th grade, I thought reading was&hellip;</em> Then say what you think now. Name one moment from each of two different novels that changed your mind. Write 3 to 5 sentences.',
         ta('journal-q1', 'Reader&#39;s Portrait (letter opening): September me, me now, one moment from each of two novels', 'When I started 5th grade, I thought reading was...&#10;&#10;Now I think...&#10;&#10;A moment that changed my mind: (book, chapter) ...', '        '))
  + ''.join(swyk('📮 Postcard %d: <em>%s</em>' % (i + 1, b),
                 ('Write three lines: <strong>1.</strong> a pitch: what the book is about, in under 15 words. <strong>2.</strong> a short quote copied exactly from the book, with its chapter. <strong>3.</strong> &ldquo;Read this if you&hellip;&rdquo;' if i == 0 else 'Pitch, quote with its chapter, and &ldquo;Read this if you&hellip;&rdquo;'),
                 ta('journal-pc%d' % (i + 1), 'Book Postcard: %s' % b, 'Pitch: ...&#10;Quote: &quot;...&quot; (Chapter __)&#10;Read this if you...', '        '))
            for i, b in enumerate(BOOKS))
  + NOTE % 'Copy every quote from your book, word for word. If you can&rsquo;t find the exact words, describe the moment instead.')
D1_ASSIGN = act('bl-gold', '✉️', 'Letter Packet &middot; Week 32 &middot; PLAN', 'Plan your letter to a future 5th grader',
  prog(0) + kc('📋 Your Letter Plan', [
     '<strong>Your claim:</strong> Read ___ before ___. Pick two of the five novels.',
     '<strong>Two reasons:</strong> why a new reader should start with your first book. Each reason needs a moment from <em>both</em> books.',
     '<strong>A fair point:</strong> one thing the other book does well.'])
  + '      <div class="textbox-prompt">Write your letter plan: your claim, two reasons, and one fair point.</div>\n'
  + ta('journal-writing', 'Letter PLAN: claim, two reasons with a moment from each book, one fair point', 'Claim: Read ___ before ___.&#10;Reason 1: ...&#10;  Moment from book 1: ...&#10;  Moment from book 2: ...&#10;Reason 2: ...&#10;Fair point for the other book: ...'),
  'margin-bottom:20px;')
D1_CHK = ['I wrote my Reader&rsquo;s Portrait (3 to 5 sentences).',
          'I wrote five Book Postcards, each with a pitch, an exact quote with its chapter, and a &ldquo;Read this if you&hellip;&rdquo; line.',
          'I planned my letter: a claim, two reasons and a fair point.',
          'I finished the Morphology Show What You Know.',
          'I wrote my Daily Oral Language fix in my reading journal.']
# ---------------- Day 2
D2_REFLECT = act('bl-gold', '🎙️', 'Your Passage: Read It Aloud', 'The short passage you will quote in your letter',
  kc('📌 Pick, Mark, Practice', [
     '<strong>Pick:</strong> 2 to 5 sentences from one of your two novels, a passage that shows your first reason.',
     '<strong>Mark:</strong> put a / where you will pause, and write the one word you will say a little stronger in CAPITALS.',
     '<strong>Practice:</strong> read it aloud three times. The last time, read it the way you want a new reader to hear it.'])
  + swyk('🎙️ Read-Aloud Question 1', 'Copy your passage exactly. Write the book and the chapter after it.', ta('journal-q1', 'Passage I will quote in my letter: exact words, book, chapter', '&quot;...&quot;&#10;(Book, Chapter __)', '        '))
  + swyk('🎙️ Read-Aloud Question 2', 'Copy it again with your marks: a / for each pause and CAPITALS for the stronger word. Then write one sentence: why pause there?', ta('journal-q2', 'My pacing marks, and why', 'Marked passage: ... / ... / ...&#10;I pause there because...', '        '))
  + swyk('🎙️ Read-Aloud Question 3', 'Read it aloud three times. Then write 3 sentences: What went well? What was hard? What will you change when you record on Day 4?', ta('journal-q3', 'Read-aloud practice: what went well, what was hard, one change for Day 4', 'What went well: ...&#10;What was hard: ...&#10;What I will change: ...', '        ')))
D2_ASSIGN = act('bl-gold', '✉️', 'Letter Packet &middot; Week 32 &middot; DRAFT', 'Write the whole letter',
  prog(1) + kc('✉️ How Your Letter Goes', [
     '<strong>1. Greeting:</strong> Dear future 5th grader,',
     '<strong>2. Opening:</strong> your Reader&rsquo;s Portrait (use the one you edited in Grammar today).',
     '<strong>3. Claim:</strong> Read ___ before ___.',
     '<strong>4. Reason 1:</strong> the reason, a moment from each book, and what it shows. You can quote your passage here.',
     '<strong>5. Reason 2:</strong> the same, for your second reason.',
     '<strong>6. A fair point:</strong> one thing the other book does well.',
     '<strong>7. Closing:</strong> one last sentence to the new reader, then your first name.'])
  + '      <div class="callout callout-tip"><span class="callout-icon">💡</span><p>Write to a 10-year-old who has not read either book. Don&rsquo;t tell how the books end.</p></div>\n'
  + '      <div class="textbox-prompt">Draft your whole letter here. Aim for 3 to 5 paragraphs.</div>\n'
  + ta('journal-writing', 'Letter DRAFT: greeting, opening, claim, two reasons with evidence from both books, a fair point, closing', 'Dear future 5th grader,&#10;&#10;When I started 5th grade...&#10;&#10;Read ___ before ___. ...&#10;&#10;Your friend,&#10;___'),
  'margin-bottom:20px;')
D2_CHK = ['I copied my passage exactly and marked my pauses.', 'I read my passage aloud three times.',
          'I finished the Grammar Show What You Know (my edited Reader&rsquo;s Portrait).',
          'I drafted my whole letter: a claim, two reasons from both books, a fair point and a closing.']
# ---------------- Day 3
D3_GIFT = '\n  ' + act('bl-gold', '🎁', 'Word Gift and P.S.', 'Two small gifts for the new reader',
  swyk('🎁 Word Gift', 'Pick three roots from this year. For each one write the root and its meaning, one word built from it, and a tip for using the root on a new word.',
       ta('journal-gift', 'Word Gift: three roots, a word for each, and a tip', 'Root 1: ___ means ___. A word: ___. Tip: ...&#10;Root 2: ...&#10;Root 3: ...', '        '))
  + '      <p style="font-size:14px;color:#3A4A6B;margin:4px 0 12px;">Roots from this year: <em>spect, script, rupt, dict, nav, port, graph, vis, voc, aud, curr, tract, fort, val</em>.</p>\n'
  + swyk('✏️ P.S.', 'End your letter with a P.S.: one piece of advice for 5th grade reading and writing, in one or two sentences.',
         ta('journal-ps', 'P.S.: one piece of advice', 'P.S. ...', '        ')))
def GIFT(t):
    a, b = block(t, 'Revision: Three Targeted Improvements</div>'); return t[:b] + D3_GIFT + t[b:], 1
D3_ASSIGN = act('bl-gold', '✉️', 'Letter Packet &middot; Week 32 &middot; REVISE', 'Your revised letter, with the Word Gift and the P.S.',
  prog(2) + kc('📋 Before Tomorrow', [
     '✓ Make your three revisions from today.',
     '✓ Give every sentence the voice test: would a 10-year-old understand it, and does it sound like you?',
     '✓ Add your Word Gift and your P.S. after your signature.',
     '✓ Read the whole letter aloud twice and time it (2 to 3 minutes).'])
  + '      <div class="textbox-prompt">Write your revised letter here, with the Word Gift and the P.S. at the end.</div>\n'
  + ta('journal-writing', 'Letter REVISED: the letter with three revisions, the Word Gift and the P.S.', 'Dear future 5th grader,&#10;...&#10;&#10;Your friend,&#10;___&#10;&#10;Word Gift: ...&#10;&#10;P.S. ...'),
  'margin-bottom:20px;')
D3_CHK = ['I made three revisions: vague to specific, the honest sentence, and the last sentence.',
          'I finished the Spelling Show What You Know.', 'I wrote my Word Gift and my P.S.',
          'I read my whole letter aloud twice and timed it (2 to 3 minutes).']
# ---------------- Day 4
D4_ASSIGN = act('bl-gold', '✉️', 'Letter Packet &middot; Week 32 &middot; SEAL &amp; SEND', 'Your envelope, your recording, your finished packet',
  prog(3)
  + '      <div class="callout callout-tip"><span class="callout-icon">🏆</span><p>You did it. Five novels and thirty-two weeks. You read about a girl accused of witchcraft in colonial Connecticut, an apprentice silversmith in Boston, a self-taught navigator, a Choctaw boy on his people&rsquo;s forced journey west, and a butler and a boy in the Gold Rush. You wrote an adventure, a literary response, a comparison, and now a letter.</p></div>\n'
  + kc('✉️ Seal and Send, in Three Steps', [
     '<strong>1. Envelope:</strong> write the address line, the one letter for your wax seal (your first initial), and the setting from your favorite novel that goes on your stamp.',
     '<strong>2. Recording:</strong> in this week&rsquo;s Canvas fluency assignment, record your letter (2 to 3 minutes), then one poem from this year. Hold up your envelope or one postcard at the start.',
     '<strong>3. Booklet:</strong> open the Reader-Writer Portfolio project page, paste in your comparison essay and every part of your letter packet, tap <strong>Make my booklet</strong>, save it as a PDF, and upload it in Canvas.'])
  + swyk('✉️ Your Envelope', 'Write the three parts of your envelope: the address line, your seal initial, and your stamp&rsquo;s setting with one sentence on why you chose it.',
         ta('journal-envelope', 'Envelope: address line, seal initial, stamp setting and why', 'To: a future 5th grader at Optima Academy Online&#10;Seal initial: ___&#10;Stamp: (a setting from a novel) ... because ...', '        '))
  + '      <div class="textbox-prompt">Paste your final letter here, exactly as you will send it, with the Word Gift and the P.S.</div>\n'
  + ta('journal-writing', 'FINAL LETTER: the letter as sent, with the Word Gift and the P.S.', 'Dear future 5th grader,&#10;...'),
  'margin-bottom:20px;border:2px solid #F9A825;')
D4_CHK = ['I answered the three Year-End Synthesis questions.', 'I finished the Vocabulary Show What You Know.',
          'I wrote my envelope and pasted my final letter.', 'I recorded my letter and one poem in Canvas.',
          'I made my booklet PDF and uploaded it in Canvas.']
S = {
 1: [REPL_ACT('Your Year-End Portfolio: Three Parts</div>', D1_REFLECT), REPL_ACT('Year-End Portfolio &middot; Week 32 &middot; PLAN</div>', D1_ASSIGN), REPL_CHK(D1_CHK),
     IN_ACT('Speaking: Voice, Tone &amp; Pacing', [('What Makes a Presentation Stick', 'What Makes a Letter Sound Like You'),
        ('Your presentation should sound like YOU speaking about something you care about, not a report being read aloud.', 'Your letter and your recording should sound like you talking about something you care about, not a report read aloud.'),
        ('can be funny in your presentation', 'can be funny in your letter'), ('can move your listener too', 'can move a new reader too'),
        ('Make eye contact (or talk to the camera). If your eyes are buried in your script, you&rsquo;ve lost your audience.', 'When you record, look up from the page now and then. A reader who looks up sounds like they mean it.'),
        ('would be hard to present', 'would be hard to read aloud')]),
     ('I will plan all three parts of my year-end portfolio reflection.', 'I will write my Reader&rsquo;s Portrait and five Book Postcards, and plan my letter.', 1),
     ('I will study what voice, tone, and pacing mean for a spoken presentation.', 'I will study how voice, tone and pacing work in a letter and in a recording.', 1),
     (re.compile(r'This week you build and present your <strong>year-end portfolio</strong>.*?draft, revise, and present\.'),
      lambda m: 'This week you finish your Reader-Writer Portfolio with a real letter to next year&rsquo;s 5th graders: which of this year&rsquo;s novels should they read first, and why? Today you write your Reader&rsquo;s Portrait and five Book Postcards. Then you draft, revise, and seal and send.', 1),
     ('before your portfolio goes out.', 'before your letter goes out.', 1), ('All reviewed. Time to plan your portfolio.', 'All reviewed. Time to start your letter packet.', 1),
     ('Portfolio planned. Tomorrow you draft it.', 'Packet started. Tomorrow you draft the letter.', 1),
     ('Week 32 &mdash; Year-End Synthesis &amp; Portfolio', 'Week 32: Letter to a Future 5th Grader', 1),
     ('WEEK 32 · DAY 1 — Year-End Portfolio\nPortfolio Plan: Three Parts', 'WEEK 32 · DAY 1 — Letter to a Future 5th Grader\nReader&#39;s Portrait, Book Postcards and Letter Plan', 1),
     SUBHEAD, STRIP_ATTR, SWYK_WORD],
 2: [('id="tab-reading">\n  \n</div>\n', 'id="tab-reading">\n', 1),
     ('<button class="tab-next-btn" onclick="markDone(\'reading\');switchTab(\'assignment\')">Continue to 📬 Assignment →</button></div>\n<div class="tab-panel" id="tab-assignment">',
      '<button class="tab-next-btn" onclick="markDone(\'reading\');switchTab(\'assignment\')">Continue to 📬 Assignment →</button></div>\n</div><div class="tab-panel" id="tab-assignment">', 1),
     REPL_ACT('Your Favorite Fluency Excerpt: The Performance</div>', D2_REFLECT), REPL_ACT('Year-End Portfolio &middot; Week 32 &middot; DRAFT</div>', D2_ASSIGN), REPL_CHK(D2_CHK),
     ('Before you submit your final portfolio reflection, check every sentence for:', 'Before you send your letter, check every sentence for:', 1),
     ('this portfolio draft', 'this letter draft', 1), ('Take your Reader&rsquo;s Portrait from Day 1 (Part 1 of your portfolio)', 'Take your Reader&rsquo;s Portrait from Day 1 (the opening of your letter)', 1),
     ('I will draft all three parts of my year-end portfolio.', 'I will draft my letter to a future 5th grader.', 1),
     ('in your portfolio draft (any part)', 'in your letter draft', 1), ('Scan your portfolio draft', 'Scan your letter draft', 1), ('you used in your portfolio', 'you used in your letter', 1),
     ('Performance practiced. Now draft your full portfolio.', 'Passage practiced. Now draft your letter.', 1),
     ('Read your favorite passage — and draft your portfolio', 'Read your passage aloud, then draft your letter', 1),
     ('Final Grammar Checklist — For Your Portfolio Piece', 'Final Grammar Checklist — For Your Letter', 1),
     ('WEEK 32 · DAY 2 — Year-End Portfolio\nFluency Performance + Full Draft', 'WEEK 32 · DAY 2 — Letter to a Future 5th Grader\nRead-Aloud Practice + Letter Draft', 1),
     SUBHEAD, STRIP_ATTR, SWYK_WORD],
 3: [IN_ACT('Revision: Three Targeted Improvements</div>', [('Three Revision Moves for a Portfolio', 'Three Revision Moves for a Letter'), ('in your portfolio and replace', 'in your letter and replace'),
        ('This is the sentence that makes a portfolio real.', 'This is the sentence that makes a letter real.'), ('for your portfolio', 'for your letter'), ('Your final sentence should be', 'Your last sentence should be')]),
     GIFT,
     REPL_ACT('Year-End Portfolio &middot; Week 32 &middot; REVISE</div>', D3_ASSIGN), REPL_CHK(D3_CHK),
     ('A portfolio reflection is not a book report. It is a portrait.', 'A letter to a younger reader is not a book report. It is a conversation.', 1),
     ('Edit your full portfolio for grade-level spelling', 'Edit your whole letter for grade-level spelling', 1),
     ('used in your portfolio', 'used in your letter', 2), ('I will edit my full portfolio draft for all grade-level spelling.', 'I will edit my whole letter for grade-level spelling.', 1),
     ('I will read my full portfolio aloud twice and time it.', 'I will read my whole letter aloud twice and time it.', 1),
     ('The best portfolio writing sounds like you', 'The best letters sound like you', 1), ('Find one sentence in your portfolio that fails', 'Find one sentence in your letter that fails', 1),
     ('Read each sentence of your portfolio aloud.', 'Read each sentence of your letter aloud.', 1), ('Read your portfolio draft aloud, slowly', 'Read your letter draft aloud, slowly', 1),
     ('Run a full spelling edit on your portfolio draft.', 'Run a full spelling edit on your letter draft.', 1),
     ('Revised. Tomorrow you present it.', 'Revised. Tomorrow you seal and send it.', 1),
     ('WEEK 32 · DAY 3 — Year-End Portfolio\nRevised and Ready to Present', 'WEEK 32 · DAY 3 — Letter to a Future 5th Grader\nRevised, with the Word Gift and the P.S.', 1),
     ('The most honest sentence in any portfolio', 'The most honest sentence in any letter', 2),
     SUBHEAD, STRIP_ATTR, SWYK_WORD],
 4: [REPL_ACT('Year-End Portfolio &middot; Week 32 &middot; PRESENT</div>', D4_ASSIGN), REPL_CHK(D4_CHK),
     (re.compile(r'(Year-End Synthesis Question 2</div>\s*<div class="swyk-prompt">).*?(</div>)', re.S),
      lambda m: m.group(1) + 'Which character from this year would you want beside you on the first day of 6th grade? Name one moment from the book that shows why, with its chapter.' + m.group(2), 1),
     (re.compile(r'id="journal-q2" data-label="[^"]*" placeholder="[^"]*"'),
      lambda m: 'id="journal-q2" data-label="Year-End Q2: The character I would want beside me in 6th grade, and one moment that shows why" placeholder="I would want ___ from ___ beside me, because...&#10;One moment that shows it: (Chapter __) ..."', 1),
     ('Before you submit your final portfolio reflection, check every sentence for:', 'Before you send your letter, check every sentence for:', 1),
     ('Final Grammar Checklist — For Your Portfolio Piece', 'Final Grammar Checklist — For Your Letter', 1),
     (re.compile(r'Read your final portfolio one last time\.(.*?)Sign your name at the bottom[^<]*'), lambda m: 'Read your final letter one last time.' + m.group(1) + 'Sign your name at the bottom.', 1),
     ('🌟 Year complete. Present your portfolio.', '🌟 Year complete. Now seal and send your letter.', 1),
     ('Continue to 📬 Present →', 'Continue to 📬 Seal &amp; Send →', 1),
     ('WEEK 32 · DAY 4 — YEAR-END FINAL\nPortfolio Submission + Year-End Synthesis', 'WEEK 32 · DAY 4 — YEAR-END FINAL\nLetter to a Future 5th Grader + Year-End Synthesis', 1),
     SUBHEAD, STRIP_ATTR, SWYK_WORD],
}
# ---------------- WGRD
W = {
 1: ('Set your purpose: the whole year', 'This week you look back over all five novels and pick two for your letter. Watch for the moments you still remember without looking.',
     [('Look back', 'Name the five novels and one thing you remember from each.'), ('Pick two', 'Choose the two novels your letter will be about.'), ('One moment', 'For each, find one scene that stayed with you.')],
     'Which two novels will your letter be about, and what moment from each do you remember best?'),
 2: ('Gather evidence from both books', 'Today you collect proof for your letter. Watch for one moment in each book that shows the same reason.',
     [('Reason', 'Say in one sentence why a new reader should start with your first book.'), ('Proof', 'Find one moment in each book that shows that reason.'), ('Fair', 'Find one thing the other book does well.')],
     'What moment from each book proves your first reason?'),
 3: ('Reread a key passage', 'Today you reread the passage you chose and look at how the author wrote it. Watch for one choice the author made: a word, a short sentence, or a pause.',
     [('Reread', 'Open your book to the passage you will quote and read it again slowly.'), ('Choice', 'Name one choice the author made: a word, a short sentence, or a pause.'), ('Effect', 'Say what that choice does to a reader.')],
     'What did the author do in your passage that you want a new reader to notice?'),
 4: ('Put the year together', 'Today you look across the whole year. Watch for one idea that shows up in more than one book.',
     [('Across', 'Name one idea that runs through more than one novel.'), ('Change', 'Name one way you read differently now than in September.'), ('Pass it on', 'Choose the one thing a new reader should know.')],
     'What one idea from this year would you pass on to a new 5th grader?'),
}
def wgrd_html(d):
    sub, intro, lenses, q = W[d]
    return ('\n  <div class="activity bl-plum">\n    <div class="activity-head"><div class="activity-num" style="background:#7B5EA7;">&#x1F4DA;</div><div style="flex:1;"><div class="activity-title">What Good Readers Do</div><div class="activity-sub">%s</div></div></div>\n'
            '    <div class="activity-body">\n      <p>%s</p>\n      <div class="key-concept" style="background:#F0F7FF;border-color:#C8DCEE;margin:10px 0;">\n'
            '        <div class="key-concept-label" style="color:#3D5285;">&#x1F50D; How to Do It</div>\n        <ol style="margin:6px 0 6px 20px;font-size:14px;color:#3A4A6B;line-height:1.8;">\n%s          </ol>\n      </div>\n'
            '      <div class="socratic-box">\n        <div class="socratic-label">&#x1F9E0; As you work, ask yourself</div>\n        <p class="socratic-q">%s</p>\n      </div>\n    </div>\n  </div>\n') % (
            sub, intro, ''.join('          <li><strong>%s:</strong> %s</li>\n' % x for x in lenses), q)
def _wg(d): return lambda m: m.group(1) + wgrd_html(d)
WG = {d: [(re.compile(r'(<div class="tab-panel" id="tab-reading">)'), _wg(d), 1)] for d in (1, 2, 3, 4)}
# ---------------- RWM
RWM_CSS = '''
/* Read Like a Writer box (same as weeks 19-31) */
.rwm-box{background:#FFFFFF;border:2px solid #E2E8F4;border-radius:14px;overflow:hidden;margin:18px 0 14px;}
.rwm-header{background:linear-gradient(135deg,#2C5F2E,#1A2D5A);color:#fff;padding:12px 18px;font-size:14px;font-weight:800;text-transform:uppercase;letter-spacing:.8px;}
.rwm-sentence{background:linear-gradient(135deg,#FFFCF0 0%,#FBF5E6 100%);border-bottom:2px solid #F5E6C8;padding:16px 20px;font-family:'Lora',Georgia,serif;font-size:17px;color:#2C5F2E;line-height:1.7;font-style:italic;}
.rwm-step{padding:14px 20px;border-bottom:1.5px solid #E2E8F4;}
.rwm-step:last-child{border-bottom:none;}
.rwm-step-label{display:flex;align-items:center;gap:8px;font-size:14px;color:#C8A850;font-weight:800;text-transform:uppercase;letter-spacing:.5px;margin-bottom:8px;}
.rwm-step-text{font-size:15px;color:#3A4A6B;line-height:1.6;}
.rwm-frame{background:#FAFBFF;border:1.5px dashed #8B3A20;border-radius:8px;padding:10px 14px;margin-top:8px;font-family:'Lora',Georgia,serif;font-size:15px;color:#8B3A20;font-style:italic;}
'''
def rwm(sentence, src, reader, writer, tryit, frame):
    fr = '      <div class="rwm-frame">%s</div>\n' % frame if frame else ''
    return ('  <!-- RWM -->\n  <div class="rwm-box">\n'
      '    <div class="rwm-header">&#128214; Read Like a Writer &mdash; Read &bull; Notice &bull; Try</div>\n'
      '    <div class="rwm-sentence">%s <span style="font-size:13px;color:#5A6B8C;font-style:normal;">(%s)</span></div>\n'
      '    <div class="rwm-step"><div class="rwm-step-label">&#128214; As a Reader</div>\n      <div class="rwm-step-text">%s</div>\n%s    </div>\n'
      '    <div class="rwm-step"><div class="rwm-step-label">&#9999;&#65039; As a Writer</div>\n      <div class="rwm-step-text">%s</div>\n%s    </div>\n'
      '    <div class="rwm-step"><div class="rwm-step-label">&#128394;&#65039; Try It</div>\n      <div class="rwm-step-text">%s</div>\n%s%s    </div>\n'
      '  </div>\n\n') % (sentence, src, reader, ta('journal-rwm-reader', 'Read Like a Writer: As a Reader', 'I notice...'), writer,
                        ta('journal-rwm-writer', 'Read Like a Writer: As a Writer', 'The writer...'), tryit, fr, ta('journal-rwm-mimic', 'Read Like a Writer: Try It', 'My sentences...'))
R = {
 1: rwm('They looked very much like a family. They felt like a family. They were a family.', '<em>By the Great Horn Spoon!</em>, Chapter 18',
        'Read the three sentences aloud. What changes from the first sentence to the last?',
        'Fleischman uses three short sentences, and each one goes a step further: <em>looked</em>, <em>felt</em>, <em>were</em>. Short sentences slow a reader down, and the last one lands hardest. That is <strong>pacing</strong>: the writer decides where you pause.',
        'Write three short sentences about your year as a reader, each one going a step further. You might use them to end your letter.', 'I ___. I ___. Now I ___.'),
 2: rwm('&ldquo;We&rsquo;re partners, sir.&rdquo;', 'Jack, <em>By the Great Horn Spoon!</em>, Chapter 1',
        'What does Jack sound like here: polite, scared, or sure? Which words tell you?',
        'Three words carry Jack&rsquo;s <strong>voice</strong>: short, polite (<em>sir</em>), and firm. Voice is how a person sounds on the page. Your letter needs your own voice, the way you would talk to a younger kid you want to help.',
        'Write the claim sentence of your letter in your own voice. Use a frame if it helps.',
        'If you only read one book from my year, make it ___, because ___.<br>Trust me: read ___ before ___. Here&rsquo;s why.'),
 3: rwm('&ldquo;Of course,&rdquo; Nat said. &ldquo;It&rsquo;s a simple matter of mathematics, sir.&rdquo;', '<em>Carry On, Mr. Bowditch</em>, Chapter 12',
        'The captain doubted Nat&rsquo;s figures, and Nat turned out to be right. What is Nat&rsquo;s tone here: angry, proud, or calm?',
        'Nat could have bragged. His <strong>tone</strong> stays calm and sure instead, and that makes him sound more confident, not less. Tone is the feeling in the words. A letter to a younger reader works best with a warm, sure tone: not bossy, not stiff.',
        'Find one sentence in your letter that sounds bossy or stiff. Write it, then rewrite it so it sounds warm and sure.', None),
 4: rwm('&ldquo;We give all we have, lives, property, safety, skills &hellip; we fight, we die, for a simple thing. Only that a man can stand up.&rdquo;', 'James Otis, <em>Johnny Tremain</em>, Chapter 8',
        'Read it aloud. Where do you pause? Which sentence is short, and why?',
        'On your own this time. Look at how the long list builds and the short last sentence lands. Where will you slow down when you record your own letter?',
        'Copy the two sentences of your letter you most want a new reader to hear. Put a / where you will pause when you record.', None),
}
READ_NEXT = re.compile(r'(<div class="tab-next-wrap"><p class="tab-transition-voice">[^<]*</p>\s*<button class="tab-next-btn" onclick="markDone\(\'reading\'\);switchTab\(\'assignment\'\)">)')
CHK_RWM = '<div class="turn-in-item" onclick="toggleCheck(this)"><div class="turn-in-check"></div><div class="turn-in-item-text">I answered the Read Like a Writer box.</div></div>'
def _rw(d): return lambda m: R[d] + m.group(1)
RW = {d: [('</style>\n</head>', RWM_CSS + '</style>\n</head>', 1), (READ_NEXT, _rw(d), 1),
          (re.compile(r'(<div class="turn-in-checklist">)'), lambda m: m.group(1) + CHK_RWM, 1)] for d in (1, 2, 3, 4)}
# ---------------- poetry
PO = {
 2: [('For your portfolio you will read a poem aloud.', 'On Day 4 you will record one poem from this year.', 1)],
 4: [('Pick any poem from this year &mdash; Stevenson&rsquo;s train, Sandburg&rsquo;s fog or buffaloes, Hopkins, Hughes, Frost, Tennyson, Pound, Lowell.',
      'Pick any poem from this year: Stevenson&rsquo;s train, Sandburg&rsquo;s fog or buffaloes, Carroll&rsquo;s &ldquo;Jabberwocky&rdquo;, Tennyson&rsquo;s eagle, Frost&rsquo;s snowy woods, Poe&rsquo;s &ldquo;Eldorado&rdquo;, or Lowell&rsquo;s moon.', 1),
     ('then write your portfolio note:', 'then write a note:', 1)],
}
# ---------------- fluency
FLU_NEW = '''<div class="intro"><p>This is your last fluency recording of 5th grade. You record two things, one after the other: your letter to a future 5th grader, then one poem from this year. Read your letter the way you want a new reader to hear it.</p></div>

  <div class="passage" style="background:#FFF8E8;border:2.5px solid #F9A825;">
    <div class="passage-label" style="color:#B8860B;">✉️ What You Read Aloud</div>
    <div class="passage-text" style="background:#FFF3C0;border:2px dashed #F9A825;border-radius:12px;padding:20px;font-family:Georgia,serif;font-size:18px;line-height:2.0;color:#5A4A20;">
      <p style="margin-bottom:12px;"><strong>1.</strong> Your letter (2 to 3 minutes), from &ldquo;Dear future 5th grader&rdquo; to your P.S.</p>
      <p><strong>2.</strong> One poem from this year, read whole.</p>
      <p style="margin-top:12px;font-size:14px;line-height:1.7;">Poems you know: Stevenson&rsquo;s &ldquo;From a Railway Carriage&rdquo;, Sandburg&rsquo;s &ldquo;Fog&rdquo; or &ldquo;Buffalo Dusk&rdquo;, Carroll&rsquo;s &ldquo;Jabberwocky&rdquo;, Tennyson&rsquo;s &ldquo;The Eagle&rdquo;, Frost&rsquo;s &ldquo;Stopping by Woods on a Snowy Evening&rdquo;, Poe&rsquo;s &ldquo;Eldorado&rdquo;, Lowell&rsquo;s &ldquo;Wind and Silver&rdquo;.</p>
    </div>
    <div class="passage-source">Your letter &bull; Your poem &bull; Your voice</div>
  </div>

  <div class="steps"><div class="steps-title">🌟 Your Final Fluency Recording</div>
    <div class="step"><div class="step-num">1</div><div class="step-content"><div class="step-label">Get Ready</div><div class="step-detail">Have your final letter and your poem in front of you. Look at the / marks you made for your pauses.</div></div></div>
    <div class="step"><div class="step-num">2</div><div class="step-content"><div class="step-label">Record</div><div class="step-detail">In this week&rsquo;s Canvas fluency assignment, hold up your envelope or one postcard, read your letter, pause, then read your poem. Look up from the page now and then.</div></div></div>
  </div>

  <div class="self-check" style="background:#FFF8E8;border:2px solid #F9A825;">
    <div class="self-check-title" style="color:#B8860B;">✅ Final Fluency Checklist</div>
    <div class="check-item"><span class="check-icon">🎯</span><span>My reading is accurate: every word right, including the names from the books.</span></div>
    <div class="check-item"><span class="check-icon">🌊</span><span>My reading is smooth: no stopping to start a sentence over.</span></div>
    <div class="check-item"><span class="check-icon">🎭</span><span>My tone is warm and sure, and I paused where I marked a /.</span></div>
    <div class="check-item"><span class="check-icon">📜</span><span>I read my poem at the pace it asks for.</span></div>
    <div class="check-item"><span class="check-icon">✉️</span><span>I showed my envelope or a postcard at the start.</span></div>
  </div>

  <div class="submit-box" style="background:linear-gradient(135deg,#FFF3C0,#FFF8E8);border:2px solid #F9A825;">
    <div class="submit-box-title" style="color:#B8860B;">📤 Final Recording</div>
    <p>Record your letter and your poem in this week&rsquo;s Canvas fluency assignment. This is the last fluency recording of 5th Grade ELA. Make it the one you&rsquo;re most proud of.</p>
  </div>
</div>
<div class="footer">'''
FL = {'flu': [(re.compile(r'<div class="intro"><p>This is your final fluency performance.*?</div>\n<div class="footer">', re.S), lambda m: FLU_NEW, 1)]}
STRANDS = {'packet': S, 'wgrd': WG, 'rwm': RW, 'poetry': PO, 'fluency': FL}
def run(strand, apply):
    ok = True; out = {}
    for k, reps in STRANDS[strand].items():
        fn = F[k]; t = io.open(fn, encoding='utf-8', newline='').read(); o = t
        for i, r in enumerate(reps):
            if callable(r):
                t, c = r(t)
                if c != 1: print('FAIL', fn, i, 'fn count', c); ok = False
                continue
            pat, new, n = r
            if isinstance(pat, str):
                c = t.count(pat)
                if (n is not None and c != n) or c == 0: print('FAIL', fn, i, 'count', c, '!=', n, repr(pat[:80])); ok = False; continue
                t = t.replace(pat, new)
            else:
                t, c = pat.subn(new, t)
                if (n is not None and c != n) or c == 0: print('FAIL', fn, i, 'regex count', c, '!=', n, pat.pattern[:80]); ok = False
        if o.count('<div') - o.count('</div>') != t.count('<div') - t.count('</div>'):
            print('FAIL div balance', fn, o.count('<div') - o.count('</div>'), t.count('<div') - t.count('</div>')); ok = False
        out[fn] = t; print(fn, len(o), '->', len(t))
    if ok and apply:
        for fn, t in out.items(): io.open(fn, 'w', encoding='utf-8', newline='').write(t)
        print('written')
    elif not ok: sys.exit(1)
run(sys.argv[1], '--apply' in sys.argv)
