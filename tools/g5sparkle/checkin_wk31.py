#!/usr/bin/env python3
"""Week 31 check-in (cross-text comparison), Nov 24 2026. Started from lesson-31-checkin.html (13 items, three-option MCs, Q10-Q11 testing the
invented diary and the invented 'three eras' secondary source). Audited against the four lessons after the week 31 fixes and the scope (v2 scope 31).
Every MC has four options (14 questions, 14 points). Writes assessments/g5-ela-wk31-checkin.json + -key.html; with --page it rebuilds the question area.
QTI: python tools/g5sparkle/qti_checkin.py assessments/g5-ela-wk31-checkin.json "planning docs/Week31_CheckIn_QTI.zip"
(Made from checkin_wk30.py.) Old week 30 notes follow: Week 30 check-in (By the Great Horn Spoon! Ch. 16-18 + whole-book synthesis), Nov 24 2026. Started from lesson-31-checkin.html (13 items, three-option MCs,
'valour' planted as a misspelling, the prospect family from week 29, the proposal line misquoted, 'Jack ... dragged along', nothing on the poem);
there is no Oct 11 Week30 QTI zip. Audited against the four lessons after the week 30 fixes, the scope (v2 scope 30) and the book text.
Every MC has four options (14 questions, 14 points). Writes assessments/g5-ela-wk31-checkin.json + -key.html and rebuilds the question area of the page.
QTI: python tools/g5sparkle/qti_checkin.py assessments/g5-ela-wk31-checkin.json "planning docs/Week30_CheckIn_QTI.zip" """
import json, io, html, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
Q = {
 "id": "g5-ela-wk31-checkin", "title": "Week 31 Check-In · Cross-Text Comparison",
 "description": "This week you compared two of the year's novels on one theme, organized the comparison by categories, read three real primary sources, analyzed a whole poem, and reviewed the year's grammar, roots and spelling.",
 "chapters": "The five novels + three primary sources",
 "questions": [
  {"n":1,"section":"Grammar","label":"Comparison Sentence","type":"multiple_choice_question","points":1,"text":"Which comparison sentence is written correctly?",
   "options":["Although Kit Tyler hides her friendship with Hannah. Jack Flagg tells the captain the truth.","Although Kit Tyler hides her friendship with Hannah, Jack Flagg tells the captain the truth.","Kit Tyler hides her friendship with Hannah, Jack Flagg tells the captain the truth.","Although Kit Tyler hides her friendship with Hannah; Jack Flagg tells the captain the truth."],"answer":1,
   "from":"31.1–31.2 Grammar (comparison sentences: although); 31.3 Daily Oral Language model","status":"replaced (the old item’s ‘right’ sentence was a lesson-made claim about Praiseworthy; now a punctuation choice)"},
  {"n":2,"section":"Grammar","label":"Combine with While","type":"essay_question","points":1,"text":"Combine these two sentences into one comparison sentence that begins with While.",
   "excerpt":"Kit Tyler stands trial in Wethersfield. Johnny Tremain carries messages in Boston.",
   "key":"While Kit Tyler stands trial in Wethersfield, Johnny Tremain carries messages in Boston. (While opens the sentence; a comma ends the while clause.)","from":"31.2 Daily Oral Language model; 31.2 Grammar Show What You Know","status":"fixed (same skill; the old pair used a lesson-made claim)"},
  {"n":3,"section":"Grammar","label":"Semicolon","type":"multiple_choice_question","points":1,"text":"Which sentence uses a semicolon correctly?",
   "options":["Isaac loses his home; and Jack leaves his by choice.","Isaac loses; his home and Jack leaves his by choice.","Isaac loses his home; Jack leaves his by choice.","Isaac loses his home, Jack; leaves his by choice."],"answer":2,
   "from":"31.1 Grammar sort; 31.2 Grammar (semicolon tool)","status":"replaced (was ‘write a concluding sentence’; the essay items cover writing)"},
  {"n":4,"section":"Morphology & Vocabulary","label":"Root Meaning","type":"multiple_choice_question","points":1,"text":"Which root means run?",
   "options":["tract","fort","curr / curs","spect"],"answer":2,"from":"31.1–31.2 Morphology (year-long root families); the week’s word game","status":"kept (a fourth option added)"},
  {"n":5,"section":"Morphology & Vocabulary","label":"Word Parts","type":"multiple_choice_question","points":1,"text":"manu means hand and script means write. What is a manuscript?",
   "options":["something written by hand","a map drawn by hand","a book about hands","a printed newspaper"],"answer":0,"from":"31.2 root match; 31.3 Morphology (build the word)","status":"replaced (was ‘persistence’ with three options)"},
  {"n":6,"section":"Morphology & Vocabulary","label":"Context Clues","type":"multiple_choice_question","points":1,"text":"Read the lines from Bayard Taylor’s Eldorado (1850). What does porter mean here?",
   "excerpt":"I asked the landlord whether he could send a porter for our trunks. “There is none belonging to the house,” said he; “every man is his own porter here.”",
   "options":["a person who carries bags and trunks","a ship’s captain","the owner of a hotel","a newspaper reporter"],"answer":0,"from":"31.2 Primary Source B (Taylor); 31.4 word game (port = carry)","status":"replaced (was ‘choose any root and write a sentence’; now vocabulary in context)"},
  {"n":7,"section":"Spelling","label":"Cumulative Words","type":"multiple_choice_question","points":1,"text":"Which word is spelled correctly?",
   "options":["seperate","definately","occurred","embarass"],"answer":2,"from":"31.1 sort; 31.2 taps; 31.4 fixes","status":"changed (the year’s tricky words; four options)"},
  {"n":8,"section":"Spelling","label":"Edit for Spelling","type":"essay_question","points":1,"text":"Find and correct every misspelling. Write the sentences correctly.",
   "excerpt":"Kit Tyler showed remarkable fortitued and persistance. Nevertheles, her notoreity as an accused witch came from the town’s ignorence.",
   "key":"Kit Tyler showed remarkable fortitude and persistence. Nevertheless, her notoriety as an accused witch came from the town’s ignorance. (fortitude, persistence, Nevertheless, notoriety, ignorance)","from":"31.2–31.3 Spelling editing","status":"fixed (‘a witch accussed’ reworded; same five words)"},
  {"n":9,"section":"Spelling","label":"Word Families","type":"multiple_choice_question","points":1,"text":"Which pair belongs to the same word family?",
   "options":["describe / descriptive","fortitude / tenacious","nevertheless / consequently","curious / current"],"answer":0,"from":"31.1–31.4 Spelling and Morphology (word families)","status":"kept (a fourth option added)"},
  {"n":10,"section":"Reading","label":"Source Types","type":"multiple_choice_question","points":1,"text":"Which of these is a primary source?",
   "options":["Henry Bigler’s diary entry, written at Sutter’s Mill on January 24, 1848","By the Great Horn Spoon!, a novel published in 1963","the background card written by Optima for this week","a textbook chapter about the Gold Rush"],"answer":0,
   "from":"31.2 What Good Readers Do and the three primary sources","status":"replaced (tested the invented ‘three eras’ secondary source)"},
  {"n":11,"section":"Reading","label":"Comparison Claim","type":"multiple_choice_question","points":1,"text":"Which comparison claim names both a similarity and a difference?",
   "options":["Both Kit and Jack are brave.","Kit lives in Connecticut, and Jack lives in Boston.","Both Kit and Jack find courage far from home; however, Kit’s costs her the town’s trust, while Jack’s costs him his gold.","Jack is braver than Kit."],"answer":2,
   "from":"31.1 Comparison claim formula; 31.4 Reviewer question 1","status":"replaced (quoted the invented diary)"},
  {"n":12,"section":"Reading","label":"Poetry","type":"multiple_choice_question","points":1,"text":"In “Buffalo Dusk,” why is the middle line so much longer than the others?",
   "options":["It is the only line where the buffaloes are alive, so it runs on like the herd.","Sandburg ran out of room on the page.","It rhymes with the first line.","It tells the year the poem was written."],"answer":0,
   "from":"31.2 and 31.4 Poetry Corner (benchmark check)","status":"new (nothing on the poem before)"},
  {"n":13,"section":"Writing","label":"Category Paragraph","type":"essay_question","points":1,"text":"Write one category paragraph from your essay (4–6 sentences): name the category, put both novels in it with evidence from each, and say why the difference matters. Underline two transition words.",
   "key":"A category named first; both novels inside it with a real moment or exact words from each; at least one sentence of reasoning about why the difference matters; two transitions underlined.","from":"31.1–31.4 Read Like a Writer (categories); 31.2–31.3 Comparison Project","status":"changed (was the four-step ‘comparison paragraph’; now the week’s category paragraph)"},
  {"n":14,"section":"Writing","label":"The Other Side","type":"essay_question","points":1,"text":"Write one sentence a reader who disagrees with your comparison claim might say. Then write one sentence that answers them with evidence from a book.",
   "key":"A fair counter-claim, then an answer that uses a specific moment or exact words from one of the two novels.","from":"31.4 Reviewer question 2 (argue the other side)","status":"new"}
 ],
 "passage": {"before": 0, "title": "", "text": "", "cite": ""}
}
assert sum(q['points'] for q in Q['questions']) == 14 and len(Q['questions']) == 14
assert all(len(q['options']) == 4 for q in Q['questions'] if 'options' in q)
io.open(os.path.join(ROOT, 'assessments/g5-ela-wk31-checkin.json'), 'w', encoding='utf-8').write(json.dumps(Q, ensure_ascii=False, indent=1))
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
page = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>G5 Week 31 Check-In Key</title>'
 '<style>body{font:16px/1.5 system-ui,sans-serif;max-width:820px;margin:0 auto;padding:16px;background:#F0F2F8;color:#24324F}h1{font-size:22px;color:#0E1C42}'
 '.q,.psg{background:#fff;border:1px solid #D9E0F0;border-radius:10px;padding:12px 16px;margin:12px 0}.q.new{border-left:5px solid #2B5BA8}.psg{background:#FFF8E6}'
 '.h{font-weight:700;color:#0E1C42}.n{display:inline-block;background:#0E1C42;color:#fff;border-radius:50%%;width:26px;height:26px;text-align:center;line-height:26px;margin-right:6px}'
 '.ok{color:#24502A;font-weight:700}.m{font-size:13px;color:#6B7690;margin-top:6px}</style></head><body>'
 '<h1>%s</h1><p>%s</p><p><b>%s · %d questions · 14 points.</b> Blue edge = changed, fixed or new from the quiz that was on the page.</p>%s</body></html>') % (
 e(Q['title']), e(Q['description']), e(Q['chapters']), len(Q['questions']), rows)
io.open(os.path.join(ROOT, 'assessments/g5-ela-wk31-checkin-key.html'), 'w', encoding='utf-8').write(page)
ICON = {'Grammar': ('grammar', '✏️', 'Grammar: Comparison Sentences'), 'Morphology & Vocabulary': ('morph', '🔬', 'Morphology &amp; Vocabulary: Year-Long Roots'),
        'Spelling': ('spelling', '🔠', 'Spelling: Cumulative Review'), 'Reading': ('reading', '📖', 'Reading: Sources, Claims and the Poem'), 'Writing': ('writing', '✍️', 'Writing: Your Comparison')}
if '--page' not in sys.argv: print('json + key written; run with --page to rebuild the page'); sys.exit(0)
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
        s += '      <textarea oninput="ga()" data-label="%s" id="%s" class="response-box%s" placeholder="Write your answer here..."></textarea>\n' % (html.escape(lab), rid, '' if q['n'] >= 11 else ' short')
    out.append(s + '    </div>\n')
out.append('  </div>\n\n')
p = os.path.join(ROOT, 'lesson-31-checkin.html')
s = io.open(p, encoding='utf-8', newline='').read(); orig = s
a = s.index('  <div class="section">'); b = s.index('  <div class="gathered-card">', a)
s = s[:a] + ''.join(out) + s[b:]
GA = ("function ga(){\n  var out='WEEK 31 CHECK-IN\\n'+'='.repeat(48)+'\\n\\n';\n"
      "  var mcm={%s};\n  Object.keys(mcm).forEach(k=>{out+=mcm[k]+': '+(mc[k]||'—')+'\\n';});\n"
      "  [%s].forEach(function(r){\n    var e=document.getElementById(r[0]);if(e)out+='\\n'+r[1]+':\\n'+(e.value.trim()||'(no answer)')+'\\n';\n  });\n"
      "  document.getElementById('gatheredOutput').value=out;\n}") % (','.join(mcmap), ','.join(resp))
s, n1 = re.subn(r"function ga\(\)\{.*?\n\}", lambda m: GA, s, count=1, flags=re.S)
if n1 != 1: sys.exit('ga')
if 'mcq7' not in s or "'resp4'" not in s: sys.exit('js maps')
if s.count('<div') - s.count('</div') != orig.count('<div') - orig.count('</div'): sys.exit('page: div balance')
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok: json, key, page;', r_n, 'written,', mc_n, 'multiple choice')
