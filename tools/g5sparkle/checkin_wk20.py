#!/usr/bin/env python3
"""Week 20 check-in (How I Became a Ghost, Ch. 12-15), Nov 21 2026. Started from the Oct 11 quiz in
planning docs/Week20_CheckIn_HBG_QTI.zip, audited against the four lessons, the scope (v2 scope 19 /
v4 week 20) and planning docs/hbg_ocr.txt. Writes assessments/g5-ela-wk20-checkin.json + -key.html and
rebuilds the question area of lesson-20-checkin.html (which still held the week 18 quiz).
QTI: python tools/g5sparkle/qti_checkin.py assessments/g5-ela-wk20-checkin.json "planning docs/Week20_CheckIn_HBG_QTI.zip" """
import json, io, html, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WK, CH = 20, 'Ch. 12–15'
Q = {
 "id": "g5-ela-wk20-checkin", "title": "Week 20 Check-In · How I Became a Ghost",
 "description": "This week Gabe told the family about Naomi, Isaac told his own secret, and Joseph came back. You practiced commas with clauses and transitions, the roots path and sens/sent, and accent shifts in related words. Show what you know.",
 "chapters": CH,
 "questions": [
  {"n":1,"section":"Grammar","label":"Identification","type":"multiple_choice_question","points":1,"text":"Which sentence uses commas correctly?",
   "options":["Nita was gone, Gabe told the families about Naomi.","Isaac felt the warm shiver, and the ghosts gathered around him.","When the soldiers took Naomi Gabe ran to help her.","Ruth wrapped her blanket tight, so, no one could see her face."],"answer":1,
   "from":"20.1–20.2 Grammar (the three comma rules; find the missing comma)","status":"changed (the old right answer was the same sentence as Q12's model; a new right answer from Ch. 13 and a fourth option added)"},
  {"n":2,"section":"Grammar","label":"Fix the Splice","type":"essay_question","points":1,"text":"This is a comma splice. Fix it so it is correct. Write the whole sentence.","excerpt":"Joseph cut the ropes with a sharp stone, he ran to the river.",
   "key":"Joseph cut the ropes with a sharp stone, and he ran to the river. (Or a period or a semicolon.)",
   "from":"20.3 Grammar (fix comma splices); Ch. 14","status":"kept"},
  {"n":3,"section":"Grammar","label":"Explain","type":"essay_question","points":1,"text":"Add the missing comma, then explain the rule you used.","excerpt":"After Nita was gone Gabe told everyone about Naomi.",
   "key":"After Nita was gone, Gabe told everyone about Naomi. A comma comes after an introductory clause.",
   "from":"20.4 Grammar (explain what the commas do)","status":"kept"},
  {"n":4,"section":"Morphology & Vocabulary","label":"Root Identification","type":"multiple_choice_question","points":1,"text":"The root path means “feeling” and sym- means “with.” Which word means “feeling with someone”?",
   "options":["sensitive","sympathy","apathy","sentiment"],"answer":1,"from":"20.1–20.4 Morphology (path, sens/sent)","status":"kept (a fourth option added)"},
  {"n":5,"section":"Morphology & Vocabulary","label":"Context Clues","type":"multiple_choice_question","points":1,"text":"Read the sentences from Chapter 12. What does determined most likely mean?","excerpt":"“You are right,” he said. “She is a determined little girl. Tonight we can talk.”",
   "options":["Shy and quiet","Firmly decided and not willing to give up","Lost and confused","Angry and loud"],"answer":1,"from":"20.1 Vocabulary (determined)","status":"kept (a fourth option added)"},
  {"n":6,"section":"Morphology & Vocabulary","label":"Use It","type":"essay_question","points":1,"text":"Use the word permission in a sentence that shows you know what it means. Connect it to what Isaac tells Nani Humma in Chapter 15.",
   "key":"Uses permission correctly (being allowed by someone in charge). Isaac tells Nani Humma his parents gave him permission to leave camp.","from":"20.4 Vocabulary (permission)","status":"kept"},
  {"n":7,"section":"Spelling","label":"Hidden Vowel","type":"essay_question","points":1,"text":"The middle vowel in definite is hard to hear. Write a related word where you can hear that vowel clearly, and explain how it helps you spell definite.",
   "key":"define. The accent falls on the i in define, so you can hear it; definite keeps the same i.","from":"20.3–20.4 Spelling (use a related word for the hidden vowel)","status":"kept"},
  {"n":8,"section":"Spelling","label":"Accent Shift","type":"multiple_choice_question","points":1,"text":"In which word does the accent fall on the second syllable?",
   "options":["photograph","photography","history","major"],"answer":1,"from":"20.1–20.2 Spelling (accent shifts; sort by stress)","status":"kept (a fourth option added from this week's list)"},
  {"n":9,"section":"Spelling","label":"Use a Related Word","type":"essay_question","points":1,"text":"Fill in the missing vowel: hist_ry. Then name the related word that tells you which vowel it is.",
   "key":"history (o). historic or historical: the accent moves onto the o.","from":"20.3 Spelling (apply a related word)","status":"kept"},
  {"n":10,"section":"Reading","label":"Detail","type":"essay_question","points":1,"text":"Why did Gabe and Ruth keep Naomi a secret? Why does Gabe feel he can finally tell?",
   "key":"The soldiers said they would take Nita too if they told anyone. Now that Nita is gone, the soldiers cannot hurt them that way.","from":"20.2 Reading (Ch. 13)","status":"kept"},
  {"n":11,"section":"Reading","label":"Inference","type":"essay_question","points":2,"text":"In Chapters 12 to 15, two big secrets come out: Gabe’s secret about Naomi, and Isaac’s secret that he will soon be a ghost. Why did each person keep the secret, and what changes once it is told? Use at least two details from two different chapters.",
   "key":"2 pts: both secrets, with a reason and a result. Gabe kept quiet because the soldiers threatened to take Nita (Ch. 12: “Do not speak of this!”; Ch. 13: he tells). Isaac did not want to upset his family after losing their home; once he tells, he asks them not to stop him if he leaves camp to find Naomi (Ch. 13), and in Ch. 15 he tells Nani Humma his parents gave him permission to leave. 1 pt: one secret or one chapter.",
   "from":"20.1–20.4 Reading (Ch. 12, 13, 15)","status":"kept (key details checked against the book and named by chapter)"},
  {"n":12,"section":"Writing","label":"Read Like a Writer","type":"essay_question","points":1,"text":"Notice the pattern: a time phrase, one change, a comma and but, then a second change that pulls the other way. Write your own sentence with the same shape. Pattern: By ___ the ___, but ___.","excerpt":"“By nightfall the snow stopped, but the air turned bitter and cold.”",
   "key":"Follows By ___ the ___, but ___, with a comma before but and a second change that pulls the other way.","from":"20.2 Read Like a Writer (Ch. 13)","status":"fixed (the section name showed as “{19: }”)"},
  {"n":13,"section":"Writing","label":"Short Response","type":"essay_question","points":1,"text":"In Chapter 15, Joseph explains, “That is what the treaty says. They have to take us safely to our new home in the west.” Isaac answers that he wishes he had never heard of Treaty Talk. In 2–3 sentences, explain how the treaty both protects and hurts the Choctaw people.",
   "key":"It forced the Choctaw from their homes (the cause of the walk and the deaths), but it also makes the soldiers feed them and keep them safe on the way west.","from":"20.4 Reading (Ch. 15)","status":"fixed (the section name showed as “{19: }”)"}
 ],
 "passage": {"before": 10, "title": "Reading passage (Chapter 13)", "ch": 13,
   "text": "“The soldiers. They said they would take Nita away if we told anybody what I am about to tell you. We have another daughter. Her name is Naomi and she is twelve years old.”",
   "cite": "Tim Tingle, How I Became a Ghost, Chapter 13"},
 "rwm_ch": 13
}
assert sum(q['points'] for q in Q['questions']) == 14
io.open(os.path.join(ROOT, 'assessments/g5-ela-wk20-checkin.json'), 'w', encoding='utf-8').write(json.dumps(Q, ensure_ascii=False, indent=1))
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
page = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>G5 Week 20 Check-In Key</title>'
 '<style>body{font:16px/1.5 system-ui,sans-serif;max-width:820px;margin:0 auto;padding:16px;background:#F0F2F8;color:#24324F}h1{font-size:22px;color:#0E1C42}'
 '.q,.psg{background:#fff;border:1px solid #D9E0F0;border-radius:10px;padding:12px 16px;margin:12px 0}.q.new{border-left:5px solid #2B5BA8}.psg{background:#FFF8E6}'
 '.h{font-weight:700;color:#0E1C42}.n{display:inline-block;background:#0E1C42;color:#fff;border-radius:50%%;width:26px;height:26px;text-align:center;line-height:26px;margin-right:6px}'
 '.ok{color:#24502A;font-weight:700}.m{font-size:13px;color:#6B7690;margin-top:6px}</style></head><body>'
 '<h1>%s</h1><p>%s</p><p><b>%s · %d questions · 14 points.</b> Blue edge = changed or fixed from the Oct 11 quiz.</p>%s</body></html>') % (
 e(Q['title']), e(Q['description']), e(Q['chapters']), len(Q['questions']), rows)
io.open(os.path.join(ROOT, 'assessments/g5-ela-wk20-checkin-key.html'), 'w', encoding='utf-8').write(page)
# the student page
ICON = {'Grammar': ('grammar', '✏️', 'Grammar: Commas with Clauses &amp; Transitions'), 'Morphology & Vocabulary': ('morph', '🌱', 'Morphology &amp; Vocabulary'),
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
p = os.path.join(ROOT, 'lesson-20-checkin.html')
s = io.open(p, encoding='utf-8', newline='').read(); orig = s
a = s.index('  <!-- GRAMMAR: Appositives -->'); b = s.index('</div>\n\n<div class="gathered-card">', a)
s = s[:a] + ''.join(out) + s[b:]
reps = [
 ('You&rsquo;ll answer questions about grammar, morphology, spelling, reading, and writing &mdash; all connected to <em>How I Became a Ghost</em>.',
  'This week two big secrets came out. You&rsquo;ll answer questions about grammar, morphology, spelling, reading, and writing from Chapters 12 to 15 of <em>How I Became a Ghost</em>.'),
 ('var ids = ["resp1","resp2","resp3","resp4","resp5","resp6","resp7","resp8","resp9","resp10"];', 'var ids = [%s];' % ','.join('"%s"' % i for i in ids)),
 ('  {id:"mcq1",label:"Q1: Grammar — Appositive identification"},\n  {id:"mcq2",label:"Q4: Morphology — Root identification"},\n  {id:"mcq3",label:"Q5: Vocabulary — Context clue"}\n', ',\n'.join(mcs) + '\n'),
 ("'Week 20 Check-In — How I Became a Ghost (Ch. 1–3)'", "'Week 20 Check-In — How I Became a Ghost (Ch. 12–15)'"),
]
for o, n in reps:
    if s.count(o) != 1: sys.exit('page: %r x%d' % (o[:60], s.count(o)))
    s = s.replace(o, n)
if s.count('<div') - s.count('</div') != orig.count('<div') - orig.count('</div'): sys.exit('page: div balance')
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok: json, key, page;', len(ids), 'written,', len(mcs), 'multiple choice')
