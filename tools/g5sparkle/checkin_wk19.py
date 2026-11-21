#!/usr/bin/env python3
"""Week 19 check-in (How I Became a Ghost, Ch. 8-11), Nov 21 2026. Started from the Oct 11 quiz in
planning docs/Week19_CheckIn_HBG_QTI.zip, audited against the four lessons, the scope (v2 scope 18 /
v4 week 19) and planning docs/hbg_ocr.txt. Writes assessments/g5-ela-wk19-checkin.json + -key.html and
rebuilds the question area of lesson-19-checkin.html (which still held the week 18 quiz).
QTI: python tools/g5sparkle/qti_checkin.py assessments/g5-ela-wk19-checkin.json "planning docs/Week19_CheckIn_HBG_QTI.zip" """
import json, io, html, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
Q = {
 "id": "g5-ela-wk19-checkin", "title": "Week 19 Check-In · How I Became a Ghost",
 "description": "This week Isaac's family joined the Choctaw walkers on the road west. You practiced strong verbs and active voice, the roots anim and spir, and the endings -ive, -al and -ic. Show what you know.",
 "chapters": "Ch. 8–11",
 "questions": [
  {"n":1,"section":"Grammar","label":"Identification","type":"multiple_choice_question","points":1,"text":"Which sentence is in the active voice?",
   "options":["The houses were burned in the night.","The older women sang the Choctaw death song.","The blankets were handed out from the wagons.","Shoes were cut from a blanket."],"answer":1,
   "from":"19.1–19.2 Grammar (active or passive)","status":"kept (a fourth option added; the right sentence is from Ch. 11)"},
  {"n":2,"section":"Grammar","label":"Rewrite","type":"essay_question","points":1,"text":"Rewrite this sentence in the active voice. Make sure the reader knows who did the action.","excerpt":"Blanket shoes were tied on Nita’s feet.",
   "key":"Isaac tied blanket shoes on Nita’s feet. (Any active sentence with Isaac as the subject.)",
   "from":"19.2 Grammar (rewrite in the active voice); Ch. 9","status":"changed (the old sentence was about Ch. 6 blankets; this one is from this week's chapters)"},
  {"n":3,"section":"Grammar","label":"Explain","type":"essay_question","points":1,"text":"A history writer could say “Isaac’s town was burned” or “The Nahullos burned Isaac’s town.” Which version is better for writing about history? Explain what the other version hides.",
   "key":"The active version. The passive version hides who did it; it never names the Nahullos.",
   "from":"19.4 Grammar (active voice names who is responsible)","status":"fixed (the old item said soldiers burned the town; in the book it was the Nahullos)"},
  {"n":4,"section":"Morphology & Vocabulary","label":"Root Identification","type":"multiple_choice_question","points":1,"text":"The root anim means “life, spirit.” The root spir means “breathe.” Which word has the root that means “breathe”?",
   "options":["animal","inspire","unanimous","animate"],"answer":1,"from":"19.1–19.4 Morphology","status":"kept (a fourth option added)"},
  {"n":5,"section":"Morphology & Vocabulary","label":"Context Clues","type":"multiple_choice_question","points":1,"text":"Read the sentences from Chapter 10. What does vanished most likely mean?","excerpt":"“Then another voice cut through the snow. ‘Son!’ It was my father’s voice. The Choctaw ghosts vanished.”",
   "options":["Grew louder and closer","Disappeared suddenly","Began to sing","Walked slowly away"],"answer":1,"from":"19.1–19.3 Vocabulary (vanished)","status":"kept (a fourth option added)"},
  {"n":6,"section":"Morphology & Vocabulary","label":"Use It","type":"essay_question","points":1,"text":"Use the word refused in a sentence that shows you know what it means. Connect it to something Isaac does in Chapter 10 or 11.",
   "key":"Uses refused correctly (said no firmly). Ch. 10: Isaac refused to look behind him. Ch. 11: he had learned never to refuse a gift.","from":"19.4 Vocabulary (Use the Word)","status":"kept"},
  {"n":7,"section":"Spelling","label":"Add the Ending","type":"essay_question","points":1,"text":"Add -ive, -al or -ic to make a describing word. Write all three: protect → ___   season → ___   hero → ___",
   "key":"protective, seasonal, heroic","from":"19.1 Spelling sort","status":"kept"},
  {"n":8,"section":"Spelling","label":"Spot It","type":"multiple_choice_question","points":1,"text":"Which describing word is spelled correctly?",
   "options":["historal","destructive","seasonic","protectal"],"answer":1,"from":"19.1 Spelling sort","status":"kept (a fourth option added)"},
  {"n":9,"section":"Spelling","label":"Tricky Bases","type":"essay_question","points":1,"text":"Add -ive to create and -al to nature. Write both new words. What happened to the base word each time?",
   "key":"creative, natural. The final e drops before the vowel ending.","from":"19.2 and 19.4 Spelling (silent e drops)","status":"kept"},
  {"n":10,"section":"Reading","label":"Detail","type":"essay_question","points":1,"text":"What does Isaac do after his father says these words? What happens to his feet afterward?",
   "key":"He stops looking behind him, keeps walking and forgets the pain. Three days later his feet heal (the healing began with his father’s words).","from":"19.3 Reading (Ch. 10)","status":"kept"},
  {"n":11,"section":"Reading","label":"Inference","type":"essay_question","points":2,"text":"In Chapter 9, Isaac promises to be Nita’s big brother and take care of her. How do Isaac and Nita take care of each other in Chapters 9 to 11? What does Nita’s death in Chapter 11 mean for Isaac’s promise? Use at least two details from two different chapters.",
   "key":"2 pts: two details from two chapters. Ch. 9: he cuts blanket shoes for her feet. Ch. 11: she gives him her shoes; he cuts her another pair. Her death means he can no longer keep the promise while she is alive (Mister Jonah taught him the dead can still help the living). 1 pt: one detail or one chapter.",
   "from":"19.2 and 19.4 Reading (Ch. 9, 11)","status":"kept"},
  {"n":12,"section":"Writing","label":"Read Like a Writer","type":"essay_question","points":1,"text":"Write two sentences with I about a time you were very cold, tired or hungry. First give one detail only you could feel. Then give one plain reaction.","excerpt":"“My feet were freezing cold and burning hot at the same time. I never knew pain could hurt this bad.”",
   "key":"Two first-person sentences: a felt detail, then a plain reaction (thoughts, details, reactions).","from":"19.3 Read Like a Writer (first-person voice: a detail, then a reaction)","status":"changed (the old model taught a pattern this week's Read Like a Writer no longer teaches)"},
  {"n":13,"section":"Writing","label":"Short Response","type":"essay_question","points":1,"text":"In Chapter 8, Isaac says, “The smallpox blankets were ghost-making blankets.” In 2–3 sentences, explain why Isaac’s family waits before taking blankets on the walk, and how Mister Jonah’s ghost helps them decide.",
   "key":"They remember the swamp blankets carried smallpox. Mister Jonah’s ghost tells Isaac the new blankets are safe, so his father asks for blankets in the morning.","from":"19.1 Reading (Ch. 8)","status":"kept"}
 ],
 "passage": {"before": 10, "title": "Reading passage (Chapter 10)",
   "text": "“Son,” he said, “you cannot keep your eyes on the bloody footprints you have left behind you. You must keep your eyes on where you are going.”\nI took a deep breath. I nodded. From that moment on, even though my feet burned, I refused to look behind me. I looked where I was going and forgot about the pain.",
   "cite": "Tim Tingle, How I Became a Ghost, Chapter 10"}
}
assert sum(q['points'] for q in Q['questions']) == 14
io.open(os.path.join(ROOT, 'assessments/g5-ela-wk19-checkin.json'), 'w', encoding='utf-8').write(json.dumps(Q, ensure_ascii=False, indent=1))
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
page = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>G5 Week 19 Check-In Key</title>'
 '<style>body{font:16px/1.5 system-ui,sans-serif;max-width:820px;margin:0 auto;padding:16px;background:#F0F2F8;color:#24324F}h1{font-size:22px;color:#0E1C42}'
 '.q,.psg{background:#fff;border:1px solid #D9E0F0;border-radius:10px;padding:12px 16px;margin:12px 0}.q.new{border-left:5px solid #2B5BA8}.psg{background:#FFF8E6}'
 '.h{font-weight:700;color:#0E1C42}.n{display:inline-block;background:#0E1C42;color:#fff;border-radius:50%%;width:26px;height:26px;text-align:center;line-height:26px;margin-right:6px}'
 '.ok{color:#24502A;font-weight:700}.m{font-size:13px;color:#6B7690;margin-top:6px}</style></head><body>'
 '<h1>%s</h1><p>%s</p><p><b>%s · %d questions · 14 points.</b> Blue edge = changed or fixed from the Oct 11 quiz.</p>%s</body></html>') % (
 e(Q['title']), e(Q['description']), e(Q['chapters']), len(Q['questions']), rows)
io.open(os.path.join(ROOT, 'assessments/g5-ela-wk19-checkin-key.html'), 'w', encoding='utf-8').write(page)
# the student page
ICON = {'Grammar': ('grammar', '✏️', 'Grammar: Strong Verbs &amp; Active Voice'), 'Morphology & Vocabulary': ('morph', '🌱', 'Morphology &amp; Vocabulary'),
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
        out.append('    <div class="excerpt">\n      %s\n      <div class="excerpt-source">&mdash; Tim Tingle, <em>How I Became a Ghost</em>, Chapter 10</div>\n    </div>\n\n' % e(Q['passage']['text']).replace('\n', '<br><br>'))
    pt = '%d pt%s' % (q['points'], '' if q['points'] == 1 else 's')
    s = '    <div class="question">\n      <div class="q-label">%s <span class="pts">%s</span></div>\n' % (e(q['label']), pt)
    if q['n'] == 12 and q.get('excerpt'):
        s += '      <div class="rwm-model">\n        <div class="rwm-model-label">Model Sentences (Chapter 10)</div>\n        <div class="rwm-model-text">%s</div>\n      </div>\n' % e(q['excerpt'])
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
p = os.path.join(ROOT, 'lesson-19-checkin.html')
s = io.open(p, encoding='utf-8', newline='').read(); orig = s
a = s.index('  <!-- GRAMMAR: Appositives -->'); b = s.index('</div>\n\n<div class="gathered-card">', a)
s = s[:a] + ''.join(out) + s[b:]
reps = [
 ('You&rsquo;ll answer questions about grammar, morphology, spelling, reading, and writing &mdash; all connected to <em>How I Became a Ghost</em>.',
  'This week Isaac&rsquo;s family joined the Choctaw walkers. You&rsquo;ll answer questions about grammar, morphology, spelling, reading, and writing from Chapters 8 to 11 of <em>How I Became a Ghost</em>.'),
 ('var ids = ["resp1","resp2","resp3","resp4","resp5","resp6","resp7","resp8","resp9","resp10"];', 'var ids = [%s];' % ','.join('"%s"' % i for i in ids)),
 ('  {id:"mcq1",label:"Q1: Grammar — Appositive identification"},\n  {id:"mcq2",label:"Q4: Morphology — Root identification"},\n  {id:"mcq3",label:"Q5: Vocabulary — Context clue"}\n', ',\n'.join(mcs) + '\n'),
 ("'Week 19 Check-In — How I Became a Ghost (Ch. 1–3)'", "'Week 19 Check-In — How I Became a Ghost (Ch. 8–11)'"),
]
for o, n in reps:
    if s.count(o) != 1: sys.exit('page: %r x%d' % (o[:60], s.count(o)))
    s = s.replace(o, n)
if s.count('<div') - s.count('</div') != orig.count('<div') - orig.count('</div'): sys.exit('page: div balance')
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok: json, key, page;', len(ids), 'written,', len(mcs), 'multiple choice')
