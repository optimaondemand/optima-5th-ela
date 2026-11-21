#!/usr/bin/env python3
"""Week 22 check-in (How I Became a Ghost, Ch. 20-23), Nov 21 2026. Started from the Oct 11 quiz in
planning docs/Week22_CheckIn_HBG_QTI.zip, audited against the four lessons, the scope (v2 scope 21 /
v4 week 22) and planning docs/hbg_ocr.txt. Writes assessments/g5-ela-wk22-checkin.json + -key.html and
rebuilds the question area of lesson-22-checkin.html (which still held the week 18 quiz).
QTI: python tools/g5sparkle/qti_checkin.py assessments/g5-ela-wk22-checkin.json "planning docs/Week22_CheckIn_HBG_QTI.zip" """
import json, io, html, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
Q = {
 "id": "g5-ela-wk22-checkin", "title": "Week 22 Check-In · How I Became a Ghost",
 "description": "This week Naomi was rescued from the soldiers and hidden by the bonepickers. You practiced clear pronouns, the light roots luc/lum and photo, and Greek and Latin parts in book words. Show what you know.",
 "chapters": "Ch. 20–23",
 "questions": [
  {"n":1,"section":"Grammar","label":"Identification","type":"multiple_choice_question","points":1,"text":"Which sentence has a clear pronoun?",
   "options":["Joseph told Luke that he should hide.","When Isaac met Joseph, he was scared.","Naomi slipped off her boots before she climbed into the wagon.","Leader told Roundman that he was in charge."],"answer":2,
   "from":"22.1–22.3 Grammar (pronoun clarity); Ch. 22","status":"kept (a fourth option added)"},
  {"n":2,"section":"Grammar","label":"Fix It","type":"essay_question","points":1,"text":"Rewrite this sentence so the reader knows exactly who looked angry.","excerpt":"Leader shouted at Pointy Nose, and he looked angry.",
   "key":"Leader shouted at Pointy Nose, and Leader looked angry. (Or any version that names the person.)","from":"22.2–22.3 Grammar; Ch. 20","status":"kept"},
  {"n":3,"section":"Grammar","label":"Explain","type":"essay_question","points":1,"text":"Isaac, Joseph, Luke, and Leader can all be called “he.” Explain why that makes pronouns tricky in this novel, and tell one way a writer can fix it.",
   "key":"With several male characters, he could point to more than one person; repeat the name or rewrite the sentence.","from":"22.1 Grammar (Notice); 22.4","status":"kept"},
  {"n":4,"section":"Morphology & Vocabulary","label":"Root Identification","type":"multiple_choice_question","points":1,"text":"In Chapter 20, “Nita shone like a pale moon. I could see through her.” The root luc means “light” and trans- means “through.” Which word fits Nita?",
   "options":["photograph","translucent","illuminate","lucid"],"answer":1,"from":"22.1, 22.3, 22.4 Morphology (translucent)","status":"kept (a fourth option added)"},
  {"n":5,"section":"Morphology & Vocabulary","label":"Context Clues","type":"multiple_choice_question","points":1,"text":"Read the sentence from Chapter 21. What does distract most likely mean?","excerpt":"“We need some way to distract the soldiers,” Joseph said, “some way to slow them down.”",
   "options":["To pull someone’s attention away","To fight someone","To hide from someone","To follow someone"],"answer":0,"from":"22.1–22.3 Vocabulary (distraction)","status":"kept (a fourth option added)"},
  {"n":6,"section":"Morphology & Vocabulary","label":"Use It","type":"essay_question","points":1,"text":"Use the word ancestors in a sentence that shows you know what it means. Connect it to what the Choctaw ghosts tell the boys in Chapter 23.",
   "key":"Uses ancestors correctly (family members who lived long before you). The ghosts say the boys made the ancestors proud, the highest honor.","from":"22.4 Vocabulary (Use the Word)","status":"kept"},
  {"n":7,"section":"Spelling","label":"Find the Root","type":"essay_question","points":1,"text":"Name the Greek root in each word and what it means: chronology, dialogue, paragraph.",
   "key":"chron = time; log(ue) = word or speech; graph = write","from":"22.1–22.4 Spelling sorts","status":"kept"},
  {"n":8,"section":"Spelling","label":"Word Families","type":"multiple_choice_question","points":1,"text":"Which word shares a root with photograph and paragraph?",
   "options":["chronicle","autograph","dialogue","prologue"],"answer":1,"from":"22.1, 22.3 Spelling sorts","status":"kept (a fourth option added)"},
  {"n":9,"section":"Spelling","label":"Build It","type":"essay_question","points":1,"text":"A story told in the order events happened is told in ___ order. Spell the word, built from chron (time).",
   "key":"chronological","from":"22.3 Spelling sort","status":"kept"},
  {"n":10,"section":"Reading","label":"Detail","type":"essay_question","points":1,"text":"Why does Naomi first say she cannot escape? What does she learn from Isaac and Nita that changes things?",
   "key":"She thinks the soldiers will take her little sister, Nita. She learns Nita has died (the soldiers can’t hurt her anymore), and Nita’s ghost appears and hugs her.","from":"22.1 Reading (Ch. 20)","status":"kept (key checked against the book)"},
  {"n":11,"section":"Reading","label":"Inference","type":"essay_question","points":2,"text":"Naomi’s escape takes many helpers: living people, ghosts, and an animal. Choose two helpers from two different chapters (20–23). Explain what each one does and why it mattered.",
   "key":"2 pts: two helpers, two chapters. Ex.: Jumper splashes into the river to draw the guards away; panther Joseph gnaws the rope and sets a wagon on fire; Nita wakes the council; a councilwoman cuts the rope from Naomi’s wrists; Luke leads her to the bonepickers; the bonepickers hide her in the trunk and use the raccoon’s blood on the bones. 1 pt: one helper or one chapter.",
   "from":"22.1–22.4 Reading (Ch. 20–23)","status":"kept"},
  {"n":12,"section":"Writing","label":"Read Like a Writer","type":"essay_question","points":1,"text":"Notice the pattern: two quick actions, then a comma and an -ing phrase that shows what happened next. Write your own sentence with the same shape.","excerpt":"“The panther ran to the fire and slapped the burning logs, sending fiery embers all about the camp.”",
   "key":"Two actions + comma + -ing result phrase.","from":"22.2 Read Like a Writer (Ch. 21)","status":"fixed (the section name showed as “{19: , 20: , 21: }”)"},
  {"n":13,"section":"Writing","label":"Short Response","type":"essay_question","points":1,"text":"Chapter 22 says the bonepickers’ “job was the hardest and most sacred in all of Choctaw country.” In 2–3 sentences, explain why their wagon is the safest place to hide Naomi.",
   "key":"Most people stay away from the bonepickers (“Most people don’t like to be around us”); the trunk of bones has a secret bottom where Naomi can lie hidden, and soldiers will not want to dig through bones.","from":"22.3 Reading (Ch. 22)","status":"fixed (the section name showed as “{19: , 20: , 21: }”)"}
 ],
 "passage": {"before": 10, "title": "Reading passage (Chapter 20)", "ch": 20,
   "text": "“I have to be watchful to stay alive,” Naomi said. “But you must understand. I can’t leave or the soldiers will take my little sister.”",
   "cite": "Tim Tingle, How I Became a Ghost, Chapter 20"},
 "rwm_ch": 21
}
assert sum(q['points'] for q in Q['questions']) == 14
io.open(os.path.join(ROOT, 'assessments/g5-ela-wk22-checkin.json'), 'w', encoding='utf-8').write(json.dumps(Q, ensure_ascii=False, indent=1))
e = lambda t: html.escape(t, quote=False)
# readable key
rows = ''
for q in Q['questions']:
    if q['n'] == Q['passage']['before']:
        rows += '<div class="psg"><b>%s</b><p>%s</p><p class="m">%s</p></div>' % (e(Q['passage']['title']), e(Q['passage']['text']).replace('\n', '<br>'), e(Q['passage']['cite']))
    opts = ''
    if 'options' in q:
        opts = '<ol type="A">' + ''.join('<li%s>%s%s</li>' % (' class="ok"' if i == q['answer'] else '', e(o), ' ✓' if i == q['answer'] else '') for i, o in enumerate(q['options'])) + '</ol>'
    ex = '<p><i>%s</i></p>' % e(q['excerpt']) if q.get('excerpt') else ''
    key = '<p class="ok">Key: %s</p>' % e(q['key']) if q.get('key') else ''
    kind = 'Multiple choice (auto-graded)' if 'options' in q else 'Written (teacher-graded)'
    rows += ('<div class="q %s"><div class="h"><span class="n">%d</span> %s · %s · %d pt</div><p>%s</p>%s%s%s<div class="m">Taught in: %s<br>Audit: %s</div></div>'
             % ('new' if q['status'].startswith(('changed', 'fixed')) else '', q['n'], e(q['section']), kind, q['points'], e(q['text']), ex, opts, key, e(q['from']), e(q['status'])))
page = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>G5 Week 22 Check-In Key</title>'
 '<style>body{font:16px/1.5 system-ui,sans-serif;max-width:820px;margin:0 auto;padding:16px;background:#F0F2F8;color:#24324F}h1{font-size:22px;color:#0E1C42}'
 '.q,.psg{background:#fff;border:1px solid #D9E0F0;border-radius:10px;padding:12px 16px;margin:12px 0}.q.new{border-left:5px solid #2B5BA8}.psg{background:#FFF8E6}'
 '.h{font-weight:700;color:#0E1C42}.n{display:inline-block;background:#0E1C42;color:#fff;border-radius:50%%;width:26px;height:26px;text-align:center;line-height:26px;margin-right:6px}'
 '.ok{color:#24502A;font-weight:700}.m{font-size:13px;color:#6B7690;margin-top:6px}</style></head><body>'
 '<h1>%s</h1><p>%s</p><p><b>%s · %d questions · 14 points.</b> Blue edge = changed or fixed from the Oct 11 quiz.</p>%s</body></html>') % (
 e(Q['title']), e(Q['description']), e(Q['chapters']), len(Q['questions']), rows)
io.open(os.path.join(ROOT, 'assessments/g5-ela-wk22-checkin-key.html'), 'w', encoding='utf-8').write(page)
# the student page
ICON = {'Grammar': ('grammar', '✏️', 'Grammar: Pronoun Clarity &amp; Antecedents'), 'Morphology & Vocabulary': ('morph', '🌱', 'Morphology &amp; Vocabulary'),
        'Spelling': ('spelling', '🔠', 'Spelling &amp; Word Analysis'), 'Reading': ('reading', '📖', 'Reading Comprehension'), 'Writing': ('writing', '✍️', 'Writing &amp; Read Like a Writer')}
out, ids, mcs, mc_n, r_n, sec = [], [], [], 0, 0, None
L = 'ABCD'
for q in Q['questions']:
    if q['section'] != sec:
        if sec: out.append('  </div>\n')
        sec = q['section']; cls, ic, title = ICON[sec]
        pts = sum(x['points'] for x in Q['questions'] if x['section'] == sec)
        out.append('  <!-- %s -->\n  <div class="section">\n    <div class="section-head">\n      <div class="section-icon %s">%s</div>\n      <div>\n        <div class="section-title">%s</div>\n        <div class="section-pts">%d points</div>\n      </div>\n    </div>\n\n' % (title.upper().replace('&AMP;', '&amp;'), cls, ic, title, pts))
    if q['n'] == Q['passage']['before']:
        out.append('    <div class="excerpt">\n      %s\n      <div class="excerpt-source">&mdash; Tim Tingle, <em>How I Became a Ghost</em>, Chapter %d</div>\n    </div>\n\n' % (e(Q['passage']['text']).replace('\n', '<br><br>'), Q['passage']['ch']))
    pt = '%d pt%s' % (q['points'], '' if q['points'] == 1 else 's')
    s = '    <div class="question">\n      <div class="q-label">%s <span class="pts">%s</span></div>\n' % (e(q['label']), pt)
    if q['n'] == 12 and q.get('excerpt'):
        s += '      <div class="rwm-model">\n        <div class="rwm-model-label">Model Sentence (Chapter %d)</div>\n        <div class="rwm-model-text">%s</div>\n      </div>\n' % (Q['rwm_ch'], e(q['excerpt']))
    s += '      <div class="q-text"><span class="q-number">%d</span>%s</div>\n' % (q['n'], e(q['text']))
    if q.get('excerpt') and q['n'] != 12:
        s += '      <div class="excerpt">%s</div>\n' % e(q['excerpt'])
    if 'options' in q:
        mc_n += 1; qid = 'mcq%d' % mc_n
        s += '      <ul class="options" data-qid="%s">\n' % qid + ''.join('        <li onclick="selectOption(this)" data-qid="%s"><span class="opt-letter">%s</span>%s</li>\n' % (qid, L[i], e(o)) for i, o in enumerate(q['options'])) + '      </ul>\n'
        mcs.append('  {id:"%s",label:"Q%d: %s — %s"}' % (qid, q['n'], q['section'].replace('&', 'and'), q['label']))
    else:
        r_n += 1; rid = 'resp%d' % r_n; ids.append(rid)
        big = q['points'] > 1 or q['n'] >= 10
        s += '      <textarea oninput="gatherAnswers()" data-label="Q%d: %s" id="%s" class="response-box%s" placeholder="Write your answer here..."></textarea>\n' % (q['n'], html.escape(q['label']), rid, '' if big else ' short')
    s += '    </div>\n\n'
    out.append(s)
out.append('  </div>\n\n')
p = os.path.join(ROOT, 'lesson-22-checkin.html')
s = io.open(p, encoding='utf-8', newline='').read(); orig = s
a = s.index('  <!-- GRAMMAR: Appositives -->'); b = s.index('</div>\n\n<div class="gathered-card">', a)
s = s[:a] + ''.join(out) + s[b:]
reps = [
 ('You&rsquo;ll answer questions about grammar, morphology, spelling, reading, and writing &mdash; all connected to <em>How I Became a Ghost</em>.',
  'Naomi escapes from the soldiers and hides with the bonepickers. You&rsquo;ll answer questions about grammar, morphology, spelling, reading, and writing from Chapters 20 to 23 of <em>How I Became a Ghost</em>.'),
 ('var ids = ["resp1","resp2","resp3","resp4","resp5","resp6","resp7","resp8","resp9","resp10"];', 'var ids = [%s];' % ','.join('"%s"' % i for i in ids)),
 ('  {id:"mcq1",label:"Q1: Grammar — Appositive identification"},\n  {id:"mcq2",label:"Q4: Morphology — Root identification"},\n  {id:"mcq3",label:"Q5: Vocabulary — Context clue"}\n', ',\n'.join(mcs) + '\n'),
 ("'Week 22 Check-In — How I Became a Ghost (Ch. 1–3)'", "'Week 22 Check-In — How I Became a Ghost (Ch. 20–23)'"),
]
for o, n in reps:
    if s.count(o) != 1: sys.exit('page: %r x%d' % (o[:60], s.count(o)))
    s = s.replace(o, n)
if s.count('<div') - s.count('</div') != orig.count('<div') - orig.count('</div'): sys.exit('page: div balance')
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok: json, key, page;', len(ids), 'written,', len(mcs), 'multiple choice')
