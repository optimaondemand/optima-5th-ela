#!/usr/bin/env python3
"""Week 27 check-in (By the Great Horn Spoon! Ch. 7-9 + Taylor source day), Nov 23 2026. Started from the week 27 quiz on
lesson-27-checkin.html (no Week27 QTI zip existed; the Week28 zip is really week 28), audited against the four lessons after the
week 27 fixes, the scope (v2 scope 27) and the book text. Every MC has four options; the item on the invented informational passage
is replaced by one on the real Taylor source; items added for vocabulary in context, the base-word rule, word families, the poem and
pacing (14 questions, 14 points). Writes assessments/g5-ela-wk27-checkin.json + -key.html and rebuilds the question area of the page.
QTI: python tools/g5sparkle/qti_checkin.py assessments/g5-ela-wk27-checkin.json "planning docs/Week27_CheckIn_QTI.zip" """
import json, io, html, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
Q = {
 "id": "g5-ela-wk27-checkin", "title": "Week 27 Check-In · By the Great Horn Spoon!",
 "description": "This week you read Chapters 7 to 9 and a real 1849 account of San Francisco. You practiced compound and complex sentences, the roots curr/curs and tract, -tion/-sion words and word families, sequence and pacing, and building the middle of an adventure. Show what you know.",
 "chapters": "Ch. 7–9 and Bayard Taylor, Eldorado (1850)",
 "questions": [
  {"n":1,"section":"Grammar","label":"Identification","type":"multiple_choice_question","points":1,"text":"Which sentence from Chapter 7 is a complex sentence?",
   "options":["The paddlewheels twirled, faster and faster, and the bowsprit came around on course.","When the Lady Wilma entered the blue Bay of Callao, Jack counted thirty-one sailing ships at anchor.","The Lady Wilma pushed on.","Jack posted another letter home to Boston."],"answer":1,
   "from":"27.1–27.4 Grammar (real Ch. 7 lines)","status":"fixed (four options; book lines instead of made-up ones)"},
  {"n":2,"section":"Grammar","label":"Combine","type":"essay_question","points":1,"text":"Combine the two sentences into one compound sentence. Use a comma and a joining word (and, but, so).",
   "excerpt":"Water cost a dollar a bucket. Praiseworthy decided they would wait.",
   "key":"Water cost a dollar a bucket, so Praiseworthy decided they would wait. (comma + and/but/so)","from":"27.2 DOL (Ch. 8); 27.1–27.4 Grammar","status":"kept (wording matches Ch. 8)"},
  {"n":3,"section":"Grammar","label":"Application","type":"essay_question","points":1,"text":"Write one complex sentence about Chapter 9 that begins with Although or Because. Put a comma after the first part.",
   "key":"Although/Because + dependent clause, + independent clause, about Ch. 9.","from":"27.3 Grammar","status":"changed (Chapter 9 instead of Chapter 7)"},
  {"n":4,"section":"Morphology & Vocabulary","label":"Root","type":"multiple_choice_question","points":1,"text":"Which word contains a root meaning pull?",
   "options":["excursion","distract","current","occurrence"],"answer":1,"from":"27.1–27.4 Morphology","status":"kept (a fourth option added)"},
  {"n":5,"section":"Morphology & Vocabulary","label":"Context Clues","type":"multiple_choice_question","points":1,"text":"Read the lines from Chapter 7. What does skedaddled mean?",
   "excerpt":"“She’s loaded up with coal and fresh water,” snapped Captain Swain. “Loaded up and skedaddled!”",
   "options":["Left in a hurry","Sank in a storm","Ran out of coal","Waited in the harbor"],"answer":0,"from":"27.1–27.4 Vocabulary (skedaddled, Ch. 7)","status":"new (vocabulary in context; replaces a second root-meaning item)"},
  {"n":6,"section":"Morphology & Vocabulary","label":"Use the Word","type":"essay_question","points":1,"text":"Use the word distraction in a sentence about Jack’s journey. Then tell how its root tract (pull) helps explain its meaning.",
   "key":"A correct sentence + tract = pull, so a distraction pulls your attention away.","from":"27.2 Morphology journal; 27.4 Morphology","status":"kept"},
  {"n":7,"section":"Spelling","label":"Identification","type":"multiple_choice_question","points":1,"text":"Which word is spelled correctly?",
   "options":["distracion","excursion","atraction","confussion"],"answer":1,"from":"27.1–27.4 Spelling","status":"kept (a fourth option added)"},
  {"n":8,"section":"Spelling","label":"Base-Word Rule","type":"multiple_choice_question","points":1,"text":"Which word ends in -sion because its base word ends in de?",
   "options":["decision","direction","celebration","attraction"],"answer":0,"from":"27.1 Spelling rule and sort; 27.4 Spelling","status":"new (the base-word rule; replaces a syllables item)"},
  {"n":9,"section":"Spelling","label":"Word Families","type":"multiple_choice_question","points":1,"text":"Which group of words is one word family?",
   "options":["decide, decision, decisive","direct, divide, dive","tense, ten, tent","invade, inside, invite"],"answer":0,"from":"27.1–27.4 Spelling (word families)","status":"new (the scope's word families)"},
  {"n":10,"section":"Reading","label":"Cause and Effect","type":"multiple_choice_question","points":1,"text":"With no coal left, how does the Lady Wilma get steam up for the final sprint in Chapter 7?",
   "options":["She burns the lumber in her cargo hold.","She buys coal in the Galapagos.","The Sea Raven shares her coal.","She burns the bricks in her hold."],"answer":0,"from":"27.1 Reading (Ch. 7)","status":"kept (a fourth option added)"},
  {"n":11,"section":"Reading","label":"Cause and Effect","type":"essay_question","points":1,"text":"How does Quartz Jackson’s strange request turn into the answer to Jack and Praiseworthy’s money problem? Explain the chain in 2–3 sentences.",
   "key":"His beard and hair hold gold dust from the diggings; Jack pans the cuttings and finds gold; Quartz gives it to them, and they start barbering to earn the fare.","from":"27.2 Reading Q2–Q3 (Ch. 8)","status":"new (replaces a question about the invented passage)"},
  {"n":12,"section":"Reading","label":"Real Account and Novel","type":"essay_question","points":1,"text":"Bayard Taylor paid porters two dollars each and wrote that every newcomer felt “complete bewilderment.” Name one way Jack’s first day in San Francisco in Chapter 8 is like Taylor’s, with one detail from each.",
   "key":"A real link (sky-high prices, crowds, confusion, people selling everything) + one detail from Taylor + one from Ch. 8.","from":"27.4 Taylor source and Info Q2–Q3","status":"new (the real source)"},
  {"n":13,"section":"Reading","label":"Poetry","type":"multiple_choice_question","points":1,"text":"Read the line from Browning’s poem. What does the strong, repeated beat do?",
   "excerpt":"I galloped, Dirck galloped, we galloped all three;",
   "options":["It makes the ride feel fast, like hoofbeats.","It slows the poem down.","It tells us what the good news is.","It shows the riders are lost."],"answer":0,"from":"27.2 Poetry Corner (Browning); 27.4 (Stevenson)","status":"new (the scope's pacing poems)"},
  {"n":14,"section":"Writing","label":"Your Middle","type":"essay_question","points":1,"text":"Write 4–6 sentences from the middle of your adventure. Show the steps of one tense moment in order, end that moment with one short sentence, and include one compound or complex sentence (label it).",
   "key":"Steps in order + a short sentence that lands + a labeled compound or complex sentence.","from":"27.1–27.4 Writer's Workshop; Read Like a Writer (pacing)","status":"changed (adds the pacing focus; now 1 point)"}
 ],
 "passage": {"before": 11, "title": "Reading passage (Chapter 8)", "ch": 8,
   "text": "Quartz Jackson insisted that every lock be caught as it fell.",
   "cite": "Sid Fleischman, By the Great Horn Spoon!, Chapter 8"}
}
assert sum(q['points'] for q in Q['questions']) == 14 and len(Q['questions']) == 14
assert all(len(q['options']) == 4 for q in Q['questions'] if 'options' in q)
io.open(os.path.join(ROOT, 'assessments/g5-ela-wk27-checkin.json'), 'w', encoding='utf-8').write(json.dumps(Q, ensure_ascii=False, indent=1))
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
page = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>G5 Week 27 Check-In Key</title>'
 '<style>body{font:16px/1.5 system-ui,sans-serif;max-width:820px;margin:0 auto;padding:16px;background:#F0F2F8;color:#24324F}h1{font-size:22px;color:#0E1C42}'
 '.q,.psg{background:#fff;border:1px solid #D9E0F0;border-radius:10px;padding:12px 16px;margin:12px 0}.q.new{border-left:5px solid #2B5BA8}.psg{background:#FFF8E6}'
 '.h{font-weight:700;color:#0E1C42}.n{display:inline-block;background:#0E1C42;color:#fff;border-radius:50%%;width:26px;height:26px;text-align:center;line-height:26px;margin-right:6px}'
 '.ok{color:#24502A;font-weight:700}.m{font-size:13px;color:#6B7690;margin-top:6px}</style></head><body>'
 '<h1>%s</h1><p>%s</p><p><b>%s · %d questions · 14 points.</b> Blue edge = changed, fixed or new from the quiz that was on the page.</p>%s</body></html>') % (
 e(Q['title']), e(Q['description']), e(Q['chapters']), len(Q['questions']), rows)
io.open(os.path.join(ROOT, 'assessments/g5-ela-wk27-checkin-key.html'), 'w', encoding='utf-8').write(page)
ICON = {'Grammar': ('grammar', '✏️', 'Grammar: Compound &amp; Complex Sentences'), 'Morphology & Vocabulary': ('morph', '🔬', 'Morphology &amp; Vocabulary: <em>curr/curs</em> + <em>tract</em>'),
        'Spelling': ('spelling', '🔠', 'Spelling: <em>&ndash;tion</em> / <em>&ndash;sion</em> and Word Families'), 'Reading': ('reading', '📖', 'Reading: Chapters 7&ndash;9, Taylor and the Poem'), 'Writing': ('writing', '✍️', 'Writing: Your Adventure Middle')}
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
p = os.path.join(ROOT, 'lesson-27-checkin.html')
s = io.open(p, encoding='utf-8', newline='').read(); orig = s
a = s.index('  <div class="section">'); b = s.index('  <div class="gathered-card">', a)
s = s[:a] + ''.join(out) + s[b:]
GA = ("function ga(){\n  var out='WEEK 27 CHECK-IN\\n'+'='.repeat(48)+'\\n\\n';\n"
      "  var mcm={%s};\n  Object.keys(mcm).forEach(k=>{out+=mcm[k]+': '+(mc[k]||'—')+'\\n';});\n"
      "  [%s].forEach(function(r){\n    var e=document.getElementById(r[0]);if(e)out+='\\n'+r[1]+':\\n'+(e.value.trim()||'(no answer)')+'\\n';\n  });\n"
      "  document.getElementById('gatheredOutput').value=out;\n}") % (','.join(mcmap), ','.join(resp))
s, n1 = re.subn(r"function ga\(\)\{.*?\n\}", lambda m: GA, s, count=1, flags=re.S)
if n1 != 1: sys.exit('ga')
if 'mcq7' not in s or "'resp6'" not in s: sys.exit('js maps')
if s.count('<div') - s.count('</div') != orig.count('<div') - orig.count('</div'): sys.exit('page: div balance')
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok: json, key, page;', r_n, 'written,', mc_n, 'multiple choice')
