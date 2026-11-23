#!/usr/bin/env python3
"""Week 26 check-in (By the Great Horn Spoon! Ch. 4-6 + humor day), Nov 23 2026. Started from the week 26 quiz
already on lesson-26-checkin.html (no Week26 QTI zip existed; ELA OAO/checkin-qti/week-26 is G3's), audited
against the four lessons after the week 26 fixes, the scope (v2 scope 26) and the book text. Every MC has four
options; the invented 26.2 lines in Q2 are replaced with real Ch. 5 lines; a vocabulary context item, a
spelling-in-quoted-speech item and a Read Like a Writer item are added (14 questions, 14 points).
Writes assessments/g5-ela-wk26-checkin.json + -key.html and rebuilds the question area of lesson-26-checkin.html.
QTI: python tools/g5sparkle/qti_checkin.py assessments/g5-ela-wk26-checkin.json "planning docs/Week26_CheckIn_QTI.zip" """
import json, io, html, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
Q = {
 "id": "g5-ela-wk26-checkin", "title": "Week 26 Check-In · By the Great Horn Spoon!",
 "description": "This week you read Chapters 4 to 6 and studied how Fleischman makes you laugh. You practiced dialogue punctuation and paragraphing, the roots rid/ris and lud/lus, dialogue tags and spelling in quoted speech, and drafting a scene with voice. Show what you know.",
 "chapters": "Ch. 4–6 and the humor day",
 "questions": [
  {"n":1,"section":"Grammar","label":"Identification","type":"multiple_choice_question","points":1,"text":"Which sentence is punctuated correctly?",
   "options":["“It’s that boy”, he shouted, waving the meat cleaver.","“It’s that boy,” he shouted, waving the meat cleaver.","“It’s that boy,” He shouted, waving the meat cleaver.","“It’s that boy” he shouted waving the meat cleaver."],"answer":1,
   "from":"26.1 DOL model (Ch. 4); 26.1–26.4 Grammar","status":"fixed (four options; the book's exact line)"},
  {"n":2,"section":"Grammar","label":"Correction","type":"essay_question","points":1,"text":"Fix the punctuation and paragraphing. Each speaker needs a new paragraph.",
   "excerpt":"Stuff and nonsense Praiseworthy would say even though he believed every word of it. Well said Mr. Azariah Jones I hope he doesn't try that.",
   "key":"“Stuff and nonsense,” Praiseworthy would say, even though he believed every word of it. / (new paragraph) “Well,” said Mr. Azariah Jones, “I hope he doesn’t try that.”",
   "from":"26.2 DOL (Ch. 5)","status":"fixed (the old lines were invented)"},
  {"n":3,"section":"Grammar","label":"Application","type":"essay_question","points":1,"text":"Write a 3-line dialogue set aboard the Lady Wilma. Use quotation marks, commas inside the closing marks, and a new paragraph for each new speaker.",
   "key":"Three lines, correct marks, new paragraph per speaker.","from":"26.2 Grammar Show What You Know; 26.3 Grammar","status":"kept"},
  {"n":4,"section":"Morphology & Vocabulary","label":"Root","type":"multiple_choice_question","points":1,"text":"Which word contains a root meaning play or jest?",
   "options":["derisive","ludicrous","risible","ridicule"],"answer":1,"from":"26.1–26.4 Morphology","status":"kept (a fourth option added)"},
  {"n":5,"section":"Morphology & Vocabulary","label":"Context Clues","type":"multiple_choice_question","points":1,"text":"Read the sentence from Chapter 6. What does monotony mean?",
   "excerpt":"“Even a haircut broke the monotony of these endless days at sea.”",
   "options":["Boring sameness, with nothing new happening","Great danger","A loud argument","Stormy weather"],"answer":0,"from":"26.1–26.4 Vocabulary (monotony, Ch. 6)","status":"new (vocabulary in context; replaces a second root-meaning item)"},
  {"n":6,"section":"Morphology & Vocabulary","label":"Use the Word","type":"essay_question","points":1,"text":"Use the word ludicrous in a sentence about this week's chapters. Then tell how its root lud (play) helps explain its meaning.",
   "key":"A sentence using ludicrous correctly + lud = play/jest, so something laughable like a joke.","from":"26.1 Morphology; 26.3 Morphology journal","status":"kept"},
  {"n":7,"section":"Spelling","label":"Identification","type":"multiple_choice_question","points":1,"text":"Which dialogue tag is spelled correctly?",
   "options":["exclaimed","interupted","stamered","comanded"],"answer":0,"from":"26.1–26.4 Spelling","status":"kept (a fourth option added)"},
  {"n":8,"section":"Spelling","label":"Spelling in Quoted Speech","type":"multiple_choice_question","points":1,"text":"In Chapter 4, Mountain Jim says a bit of singing will pass the time. Which spelling shows how he says it?",
   "options":["singin’","sing’in","singin","’singing"],"answer":0,"from":"26.1–26.4 Spelling (spelling in quoted speech)","status":"new (the scope's quoted-speech half; replaces bellowed in syllables)"},
  {"n":9,"section":"Spelling","label":"Tag Choice","type":"multiple_choice_question","points":1,"text":"A character speaks quietly and grumpily, under their breath. Which dialogue tag fits best?",
   "options":["bellowed","commanded","muttered","exclaimed"],"answer":2,"from":"26.1 Spelling sort; 26.4 Spelling","status":"kept (a fourth option added; the written explanation dropped)"},
  {"n":10,"section":"Reading","label":"Comprehension","type":"multiple_choice_question","points":1,"text":"How does Jack's time as a stowaway lead to the solution in Chapter 6?",
   "options":["He hid in the potato barrels and sucked the potatoes, so he knew they were juicy enough to keep grape cuttings alive.","He ran away from home, so he understood how Monsieur Gaunt felt.","He was small, so he could reach the potatoes deep in the hold.","He was ship's boy, so he knew where the fresh water was kept."],"answer":0,
   "from":"26.3 Reading (Ch. 6)","status":"kept (a fourth option added)"},
  {"n":11,"section":"Reading","label":"Inference","type":"essay_question","points":1,"text":"Read the line from Chapter 5. Why does Praiseworthy say “Stuff and nonsense” if he believes the stories? What does this show about his role among the passengers?",
   "key":"He keeps calm on the outside to steady the frightened passengers; he is a calm leader (self-control).","from":"26.2 Reading Q2; Virtue Watch","status":"kept"},
  {"n":12,"section":"Reading","label":"Humor Analysis","type":"essay_question","points":1,"text":"Choose one comic moment from Chapters 4–6. Name the technique that makes it funny (comic contrast, the straight face, or the ticking clock) and explain in 2–3 sentences.",
   "key":"A real moment + a named technique + how it works.","from":"26.4 How Fleischman Makes You Laugh","status":"kept"},
  {"n":13,"section":"Writing","label":"Read Like a Writer","type":"essay_question","points":1,"text":"In this line, a reaction sits in the middle of the speech, set off by commas. Write one line for your own scene the same way: dialogue, a reaction, then more dialogue.",
   "excerpt":"“You mean to say, sir,” said Mr. Azariah Jones, turning white, “that we’ve been bouncing around in that awful place?” (Chapter 5)",
   "key":"Speech + tag with a reaction set off by commas + more speech, punctuated correctly.","from":"26.2 Read Like a Writer (Ch. 5)","status":"new (the scope's Read Like a Writer focus)"},
  {"n":14,"section":"Writing","label":"Your Scene","type":"essay_question","points":1,"text":"Copy 4–6 sentences from your adventure scene. Include correctly punctuated dialogue, one of this week's dialogue tags, and a moment that shows your hero's voice.",
   "key":"Dialogue punctuated correctly + a tag from the list + a voice moment.","from":"26.1–26.4 Writer's Workshop","status":"kept (now 1 point)"}
 ],
 "passage": {"before": 11, "title": "Reading passage (Chapter 5)", "ch": 5,
   "text": "“Stuff and nonsense,” Praiseworthy would say, even though he believed every word of it.",
   "cite": "Sid Fleischman, By the Great Horn Spoon!, Chapter 5"}
}
assert sum(q['points'] for q in Q['questions']) == 14 and len(Q['questions']) == 14
assert all(len(q['options']) == 4 for q in Q['questions'] if 'options' in q)
io.open(os.path.join(ROOT, 'assessments/g5-ela-wk26-checkin.json'), 'w', encoding='utf-8').write(json.dumps(Q, ensure_ascii=False, indent=1))
e = lambda t: html.escape(t, quote=False)
rows = ''
for q in Q['questions']:
    if q['n'] == Q['passage']['before']:
        rows += '<div class="psg"><b>%s</b><p>%s</p><p class="m">%s</p></div>' % (e(Q['passage']['title']), e(Q['passage']['text']), e(Q['passage']['cite']))
    opts = ('<ol type="A">' + ''.join('<li%s>%s%s</li>' % (' class="ok"' if i == q['answer'] else '', e(o), ' ✓' if i == q['answer'] else '') for i, o in enumerate(q['options'])) + '</ol>') if 'options' in q else ''
    ex = '<p><i>%s</i></p>' % e(q['excerpt']) if q.get('excerpt') else ''
    key = '<p class="ok">Key: %s</p>' % e(q['key']) if q.get('key') else ''
    kind = 'Multiple choice (auto-graded)' if 'options' in q else 'Written (teacher-graded)'
    rows += ('<div class="q %s"><div class="h"><span class="n">%d</span> %s · %s · %d pt</div><p>%s</p>%s%s%s<div class="m">Taught in: %s<br>Audit: %s</div></div>'
             % ('new' if q['status'].startswith(('changed', 'fixed', 'new', 'replaced')) else '', q['n'], e(q['section']), kind, q['points'], e(q['text']), ex, opts, key, e(q['from']), e(q['status'])))
page = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>G5 Week 26 Check-In Key</title>'
 '<style>body{font:16px/1.5 system-ui,sans-serif;max-width:820px;margin:0 auto;padding:16px;background:#F0F2F8;color:#24324F}h1{font-size:22px;color:#0E1C42}'
 '.q,.psg{background:#fff;border:1px solid #D9E0F0;border-radius:10px;padding:12px 16px;margin:12px 0}.q.new{border-left:5px solid #2B5BA8}.psg{background:#FFF8E6}'
 '.h{font-weight:700;color:#0E1C42}.n{display:inline-block;background:#0E1C42;color:#fff;border-radius:50%%;width:26px;height:26px;text-align:center;line-height:26px;margin-right:6px}'
 '.ok{color:#24502A;font-weight:700}.m{font-size:13px;color:#6B7690;margin-top:6px}</style></head><body>'
 '<h1>%s</h1><p>%s</p><p><b>%s · %d questions · 14 points.</b> Blue edge = changed, fixed or new from the quiz that was on the page.</p>%s</body></html>') % (
 e(Q['title']), e(Q['description']), e(Q['chapters']), len(Q['questions']), rows)
io.open(os.path.join(ROOT, 'assessments/g5-ela-wk26-checkin-key.html'), 'w', encoding='utf-8').write(page)
ICON = {'Grammar': ('grammar', '✏️', 'Grammar: Dialogue Punctuation and Paragraphing'), 'Morphology & Vocabulary': ('morph', '🔬', 'Morphology &amp; Vocabulary: <em>rid/ris</em> + <em>lud/lus</em>'),
        'Spelling': ('spelling', '🔠', 'Spelling: Dialogue Tags and Quoted Speech'), 'Reading': ('reading', '📖', 'Reading: Chapters 4&ndash;6'), 'Writing': ('writing', '✍️', 'Writing: Your Adventure Scene')}
out, resp, mcmap, mc_n, r_n, sec = [], [], [], 0, 0, None
for q in Q['questions']:
    if q['section'] != sec:
        if sec: out.append('  </div>\n\n')
        sec = q['section']; cls, ic, title = ICON[sec]
        pts = sum(x['points'] for x in Q['questions'] if x['section'] == sec)
        out.append('  <!-- %s -->\n  <div class="section">\n    <div class="section-head"><div class="section-icon %s">%s</div><div><div class="section-title">%s</div><div class="section-pts">%d points</div></div></div>\n' % (sec.upper(), cls, ic, title, pts))
    if q['n'] == Q['passage']['before']:
        out.append('    <div class="excerpt">%s<br><span style="font-size:13px;">&mdash; Sid Fleischman, <em>By the Great Horn Spoon!</em>, Chapter %d</span></div>\n' % (e(Q['passage']['text']), Q['passage']['ch']))
    s = '    <div class="question">\n      <div class="q-label">%s <span class="pts">%d pt</span></div>\n      <div class="q-text"><span class="q-number">%d</span>%s</div>\n' % (e(q['label']), q['points'], q['n'], e(q['text']))
    if q.get('excerpt'): s += '      <div class="excerpt">%s</div>\n' % e(q['excerpt'])
    if 'options' in q:
        mc_n += 1; qid = 'mcq%d' % mc_n
        s += '      <ul class="options" data-qid="%s">\n' % qid + ''.join('        <li onclick="sel(this,\'%s\')"><span class="opt-letter">%s</span>%s</li>\n' % (qid, 'ABCD'[i], e(o)) for i, o in enumerate(q['options'])) + '      </ul>\n'
        mcmap.append("%s:'%s Q%d'" % (qid, q['section'].split(' ')[0], q['n']))
    else:
        r_n += 1; rid = 'resp%d' % r_n
        lab = 'Q%d: %s — %s' % (q['n'], q['section'], q['label'])
        resp.append("['%s','%s']" % (rid, lab.replace("'", "\\'")))
        s += '      <textarea oninput="ga()" data-label="%s" id="%s" class="response-box%s" placeholder="Write your answer here..."></textarea>\n' % (html.escape(lab), rid, '' if q['n'] >= 12 else ' short')
    out.append(s + '    </div>\n')
out.append('  </div>\n\n')
p = os.path.join(ROOT, 'lesson-26-checkin.html')
s = io.open(p, encoding='utf-8', newline='').read(); orig = s
a = s.index('  <!-- GRAMMAR -->'); b = s.index('  <!-- GATHERED -->', a)
s = s[:a] + ''.join(out) + s[b:]
s, n1 = re.subn(r"var mc=\{[^}]*\};", lambda m: "var mc={%s};" % ','.join(mcmap), s)
s, n2 = re.subn(r"\[\['resp1'.*?\]\]\.forEach", lambda m: "[%s].forEach" % ','.join(resp), s, flags=re.S)
if (n1, n2) != (1, 1): sys.exit('page js %d %d' % (n1, n2))
if s.count('<div') - s.count('</div') != orig.count('<div') - orig.count('</div'): sys.exit('page: div balance')
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok: json, key, page;', r_n, 'written,', mc_n, 'multiple choice')
