#!/usr/bin/env python3
"""Week 24 check-in (How I Became a Ghost, Ch. 28-29 + the source study), Nov 22 2026. Started from the Oct 11 quiz in
planning docs/Week24_CheckIn_HBG_QTI.zip, audited against the four lessons, the scope (v2 scope 24 /
v4 week 24) and planning docs/hbg_ocr.txt. Writes assessments/g5-ela-wk24-checkin.json + -key.html and
rebuilds the question area of lesson-24-checkin.html (which still held the week 18 quiz).
QTI: python tools/g5sparkle/qti_checkin.py assessments/g5-ela-wk24-checkin.json "planning docs/Week24_CheckIn_HBG_QTI.zip" """
import json, io, html, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
Q = {
 "id": "g5-ela-wk24-checkin", "title": "Week 24 Check-In · How I Became a Ghost",
 "description": "This week you finished the novel and set it beside two real sources: a treaty from 1830 and a letter by a Choctaw chief from 1831. You practiced formal style and source transitions, the vocabulary of history, and taking long words apart. Show what you know.",
 "chapters": "Ch. 28–29 and the source study",
 "questions": [
  {"n":1,"section":"Grammar","label":"Identification","type":"multiple_choice_question","points":1,"text":"Which sentence is written in formal style for an essay?",
   "options":["Leader was super mean to Naomi.","In Chapter 28, Naomi chooses to save Leader’s life.","You’d be so scared if a wolf came at you.","Naomi’s pretty much the bravest kid ever."],"answer":1,
   "from":"24.1–24.2 Grammar (formal style); Ch. 28","status":"kept (a fourth option added)"},
  {"n":2,"section":"Grammar","label":"Rewrite","type":"essay_question","points":1,"text":"Rewrite this sentence in formal style.","excerpt":"Pushmataha’s a really big deal in Choctaw history and he totally shows up at the end.",
   "key":"Ex.: Pushmataha, an important figure in Choctaw history, appears at the end of the novel. (No contractions, no slang.)","from":"24.1–24.2 Grammar (formal style)","status":"kept"},
  {"n":3,"section":"Grammar","label":"Source Transition","type":"essay_question","points":1,"text":"Write one sentence about the novel that begins with a source transition, such as According to, Tingle suggests, or In the novel.",
   "key":"Begins with a source transition and says something accurate about the novel.","from":"24.1–24.3 Grammar (source transitions)","status":"kept"},
  {"n":4,"section":"Morphology & Vocabulary","label":"History Words","type":"multiple_choice_question","points":1,"text":"A formal agreement between nations is called a ___.",
   "options":["claim","treaty","evidence","removal"],"answer":1,"from":"24.1–24.4 Morphology (the vocabulary of history)","status":"kept (a fourth option added)"},
  {"n":5,"section":"Morphology & Vocabulary","label":"Context Clues","type":"multiple_choice_question","points":1,"text":"Read the sentence from Chapter 28. What does lifeless mean?","excerpt":"“He locked his jaws around the wolf’s head and lifted him off the ground, swinging him back and forth till the wolf was limp and lifeless.”",
   "options":["Without life; not moving or breathing","Tired but still fighting","Hiding in fear","Very strong and fierce"],"answer":0,"from":"24.1–24.3 Vocabulary","status":"kept (a fourth option added)"},
  {"n":6,"section":"Morphology & Vocabulary","label":"Use It","type":"essay_question","points":1,"text":"Use the word reunited in a sentence that shows you know what it means. Connect it to Chapter 29.",
   "key":"Uses reunited correctly (brought back together). Ex.: Naomi is reunited with her mother and father.","from":"24.4 Vocabulary (Use the Word)","status":"kept"},
  {"n":7,"section":"Spelling","label":"Break It Down","type":"essay_question","points":1,"text":"Break each word into its parts with slashes.","excerpt":"relocation     displacement",
   "key":"re / locat(e) / ion; dis / place / ment","from":"24.1–24.3 Spelling (long-word decoding)","status":"kept"},
  {"n":8,"section":"Spelling","label":"Endings","type":"multiple_choice_question","points":1,"text":"Which ending turns govern into a noun?",
   "options":["-ly","-ful","-ment","-ed"],"answer":2,"from":"24.1 Spelling sort (-ment)","status":"kept (a fourth option added)"},
  {"n":9,"section":"Spelling","label":"Noun Forms","type":"essay_question","points":1,"text":"Write the noun form of each word.","excerpt":"settle → ___   declare → ___   relocate → ___",
   "key":"settlement, declaration, relocation","from":"24.1 and 24.3 Spelling sorts","status":"kept"},
  {"n":10,"section":"Reading","label":"Detail","type":"essay_question","points":1,"text":"Why does Naomi save Leader from the wolf? What does Leader decide to do afterward?",
   "key":"It was the right thing to do; it is the Choctaw way. Leader orders the soldiers to put down their weapons and lets Naomi return to her parents (“You have earned your life today”).","from":"24.1 Reading (Ch. 28)","status":"kept (key checked against the book)"},
  {"n":11,"section":"Reading","label":"Novel and Sources","type":"essay_question","points":2,"text":"How I Became a Ghost is fiction, but the Choctaw removal really happened. Name one thing the novel helps you understand that the two real sources cannot. Then name one thing a real source (the treaty or Harkins’s letter) tells you that the novel cannot. Use a specific detail from each.",
   "key":"2 pts: novel = feelings, family, Choctaw beliefs and a child’s voice (e.g., “It is the Choctaw way,” the reunion in Ch. 29); source = real dates and terms (the falls of 1831, 1832 and 1833; land east of the Mississippi given up) or a real chief’s own words (the removal was not by choice; “with them I must go”). 1 pt: only one side, or no specific detail.",
   "from":"24.3 Reading (the two sources); 24.3–24.4 What Good Readers Do","status":"fixed (now names the two sources that are on the pages)"},
  {"n":12,"section":"Writing","label":"Read Like a Writer","type":"essay_question","points":1,"text":"Notice the pattern: two hard things joined by and, then but and one good thing, with a name set off by commas in the middle. Write your own sentence with the same shape.","excerpt":"“The winter was fierce and food was scarce, but our most feared enemy, Leader, left us alone to be with our families.” (Chapter 29)",
   "key":"Two hardships + but + one good thing; bonus if it sets a name off with commas.","from":"24.2 Read Like a Writer (Ch. 29)","status":"fixed (the section name showed as “{19: , 20: , …}”)"},
  {"n":13,"section":"Writing","label":"Short Response","type":"essay_question","points":1,"text":"The novel begins, “Maybe you have never read a book written by a ghost before. I am a ghost.” It ends with Pushmataha saying, “Chi pisa lachike. I will see you again.” In 2–3 sentences, explain why this is a fitting ending for a story told by a ghost.",
   "key":"Choctaws never say good-bye; the dead stay with the living. Isaac, a ghost, has stayed with his family the whole book, and the ending promises that the people and the story go on.","from":"24.2 Reading (Ch. 29); 21.2 (chi pisa lachike)","status":"fixed (the section name showed as “{19: , 20: , …}”)"}
 ],
 "passage": {"before": 10, "title": "Reading passage (Chapter 28)", "ch": 28,
   "text": "“And you,” he whispered, looking at Naomi. “I vowed that you would die today. Why did you save me?”\n“It was the right thing to do,” said Naomi. “It is the Choctaw way.”",
   "cite": "Tim Tingle, How I Became a Ghost, Chapter 28"},
 "rwm_ch": 29
}
assert sum(q['points'] for q in Q['questions']) == 14
io.open(os.path.join(ROOT, 'assessments/g5-ela-wk24-checkin.json'), 'w', encoding='utf-8').write(json.dumps(Q, ensure_ascii=False, indent=1))
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
page = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>G5 Week 24 Check-In Key</title>'
 '<style>body{font:16px/1.5 system-ui,sans-serif;max-width:820px;margin:0 auto;padding:16px;background:#F0F2F8;color:#24324F}h1{font-size:22px;color:#0E1C42}'
 '.q,.psg{background:#fff;border:1px solid #D9E0F0;border-radius:10px;padding:12px 16px;margin:12px 0}.q.new{border-left:5px solid #2B5BA8}.psg{background:#FFF8E6}'
 '.h{font-weight:700;color:#0E1C42}.n{display:inline-block;background:#0E1C42;color:#fff;border-radius:50%%;width:26px;height:26px;text-align:center;line-height:26px;margin-right:6px}'
 '.ok{color:#24502A;font-weight:700}.m{font-size:13px;color:#6B7690;margin-top:6px}</style></head><body>'
 '<h1>%s</h1><p>%s</p><p><b>%s · %d questions · 14 points.</b> Blue edge = changed or fixed from the Oct 11 quiz.</p>%s</body></html>') % (
 e(Q['title']), e(Q['description']), e(Q['chapters']), len(Q['questions']), rows)
io.open(os.path.join(ROOT, 'assessments/g5-ela-wk24-checkin-key.html'), 'w', encoding='utf-8').write(page)
# the student page
ICON = {'Grammar': ('grammar', '✏️', 'Grammar: Formal Style &amp; Source Transitions'), 'Morphology & Vocabulary': ('morph', '🌱', 'Morphology &amp; Vocabulary'),
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
p = os.path.join(ROOT, 'lesson-24-checkin.html')
s = io.open(p, encoding='utf-8', newline='').read(); orig = s
a = s.index('  <!-- GRAMMAR: Appositives -->'); b = s.index('</div>\n\n<div class="gathered-card">', a)
s = s[:a] + ''.join(out) + s[b:]
reps = [
 ('You&rsquo;ll answer questions about grammar, morphology, spelling, reading, and writing &mdash; all connected to <em>How I Became a Ghost</em>.',
  'You finished the novel and read two real sources beside it. You&rsquo;ll answer questions about grammar, history words, spelling, reading, and writing from Chapters 28 and 29 of <em>How I Became a Ghost</em> and the source study.'),
 ('var ids = ["resp1","resp2","resp3","resp4","resp5","resp6","resp7","resp8","resp9","resp10"];', 'var ids = [%s];' % ','.join('"%s"' % i for i in ids)),
 ('  {id:"mcq1",label:"Q1: Grammar — Appositive identification"},\n  {id:"mcq2",label:"Q4: Morphology — Root identification"},\n  {id:"mcq3",label:"Q5: Vocabulary — Context clue"}\n', ',\n'.join(mcs) + '\n'),
 ("'Week 24 Check-In — How I Became a Ghost (Ch. 1–3)'", "'Week 24 Check-In — How I Became a Ghost (Ch. 28–29)'"),
]
for o, n in reps:
    if s.count(o) != 1: sys.exit('page: %r x%d' % (o[:60], s.count(o)))
    s = s.replace(o, n)
if s.count('<div') - s.count('</div') != orig.count('<div') - orig.count('</div'): sys.exit('page: div balance')
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok: json, key, page;', len(ids), 'written,', len(mcs), 'multiple choice')
