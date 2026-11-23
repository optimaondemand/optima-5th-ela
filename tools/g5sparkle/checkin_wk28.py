#!/usr/bin/env python3
"""Week 28 check-in (By the Great Horn Spoon! Ch. 10-12 + theme day), Nov 23 2026. Started from lesson-28-checkin.html (Grammar/Spelling labels swapped, Q4 keyed prevail) and planning docs/Week28_CheckIn_QTI.zip
(Oct 11; section-name bug, three-option MCs), audited against the four lessons after the week 28 fixes, the scope (v2 scope 28)
and the book text. Every MC has four options; items added for introductory phrases, vocabulary in context, the spelling change at the
join, Read Like a Writer (character choices) and the poem (14 questions, 14 points). Writes assessments/g5-ela-wk28-checkin.json + -key.html and rebuilds the question area of the page.
QTI: python tools/g5sparkle/qti_checkin.py assessments/g5-ela-wk28-checkin.json "planning docs/Week28_CheckIn_QTI.zip" """
import json, io, html, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
Q = {
 "id": "g5-ela-wk28-checkin", "title": "Week 28 Check-In · By the Great Horn Spoon!",
 "description": "This week you read Chapters 10 to 12. You practiced transitions and introductory phrases, the roots fort and val/valid, the endings -ity, -ment and -ness, how character choices build a theme, two themes in one poem, and a literary response. Show what you know.",
 "chapters": "Ch. 10–12",
 "questions": [
  {"n":1,"section":"Grammar","label":"Identification","type":"multiple_choice_question","points":1,"text":"Which transition shows a contrast between two ideas?",
   "options":["furthermore","consequently","nevertheless","meanwhile"],"answer":2,"from":"28.1–28.4 Grammar","status":"kept (a fourth option added)"},
  {"n":2,"section":"Grammar","label":"Punctuate","type":"essay_question","points":1,"text":"Rewrite the sentence with correct punctuation.",
   "excerpt":"The road agents held the stage nevertheless Praiseworthy stayed calm.",
   "key":"The road agents held the stage; nevertheless, Praiseworthy stayed calm. (semicolon before, comma after)","from":"28.1 and 28.3 Grammar rule; Oct 11 QTI Q3","status":"kept from the Oct 11 quiz (made-up sentence, not a book line)"},
  {"n":3,"section":"Grammar","label":"Introductory Phrase","type":"multiple_choice_question","points":1,"text":"Which sentence puts the comma in the right place?",
   "options":["After a long climb, the stage reached the top of the hill.","After a long climb the stage, reached the top of the hill.","After, a long climb the stage reached the top of the hill.","After a long climb the stage reached, the top of the hill."],"answer":0,
   "from":"28.1 sort; 28.2 hunt; 28.4 comma choice","status":"new (introductory phrases; the scope's second half)"},
  {"n":4,"section":"Morphology & Vocabulary","label":"Root","type":"multiple_choice_question","points":1,"text":"Which word contains the root val (strong, worth)?",
   "options":["fortify","effort","valor","festival"],"answer":2,"from":"28.1–28.4 Morphology","status":"fixed (the page keyed prevail, whose root is spelled vail; festival is a look-alike decoy)"},
  {"n":5,"section":"Morphology & Vocabulary","label":"Root Meaning","type":"multiple_choice_question","points":1,"text":"What does fortitude mean, based on its root?",
   "options":["A place built for defense","Strength and courage in hard times","The act of making something stronger","Great luck"],"answer":1,"from":"28.1 Morphology and cards; 28.3 match","status":"kept (a fourth option added)"},
  {"n":6,"section":"Morphology & Vocabulary","label":"Context Clues","type":"multiple_choice_question","points":1,"text":"Read the line from Chapter 11. What does exasperation mean here?",
   "excerpt":"Praiseworthy’s patience was a marvel — and an exasperation.",
   "options":["Great annoyance","Great joy","A long wait","A pleasant surprise"],"answer":0,"from":"28.1–28.4 Vocabulary (exasperation, Ch. 11)","status":"new (vocabulary in context; replaces 'use valor in a sentence')"},
  {"n":7,"section":"Spelling","label":"Identification","type":"multiple_choice_question","points":1,"text":"Which word is spelled correctly?",
   "options":["amazment","boldness","curiousity","lonelyness"],"answer":1,"from":"28.1–28.4 Spelling","status":"kept (a fourth option added)"},
  {"n":8,"section":"Spelling","label":"Build the Noun","type":"essay_question","points":1,"text":"Turn each word into an abstract noun and name the ending you used: valid, achieve, dark.",
   "key":"validity (-ity), achievement (-ment), darkness (-ness)","from":"28.1 Spelling journal","status":"kept"},
  {"n":9,"section":"Spelling","label":"Base Word Change","type":"multiple_choice_question","points":1,"text":"In which word does the base word change its spelling when the ending is added?",
   "options":["bold + ness = boldness","argue + ment = argument","pay + ment = payment","dark + ness = darkness"],"answer":1,"from":"28.3 Spelling fill-in; 28.4 Spelling","status":"new (spelling change at the join; replaces a sentence-writing item)"},
  {"n":10,"section":"Reading","label":"Key Detail","type":"multiple_choice_question","points":1,"text":"How does Praiseworthy keep the gold dust safe during the robbery in Chapter 10?",
   "options":["He pulls off his glove carefully but casually, and the dust stays in the fingers.","He hides it inside his hat.","He drops it in the dirt so the outlaws miss it.","He gives it to Jack to hide."],"answer":0,"from":"28.1 Reading Q2 (Ch. 10)","status":"kept (a fourth option added)"},
  {"n":11,"section":"Reading","label":"Character Choice","type":"essay_question","points":1,"text":"Why does Praiseworthy stop trying to correct the miners’ story? What does this choice show about him? Answer in 2–3 sentences.",
   "key":"The miners won't listen and prefer the tall tale; he decides to go along (even adds to it), which shows he can bend, has a sense of humor, and is adapting to life in the diggings.","from":"28.3 Reading Q2 (Ch. 12)","status":"kept (1 point; the passage is now printed above it)"},
  {"n":12,"section":"Reading","label":"Read Like a Writer","type":"multiple_choice_question","points":1,"text":"In Chapter 11, Jack forces down coffee he can hardly swallow. What does this choice show?",
   "options":["He wants to belong and keep the name Jamoka Jack.","He loves strong coffee.","He is trying to stay awake.","He wants to make Pitch-pine Billy angry."],"answer":0,"from":"28.2 Read Like a Writer (Ch. 11)","status":"new (the scope's Read Like a Writer focus: theme through character choices)"},
  {"n":13,"section":"Reading","label":"Poetry","type":"multiple_choice_question","points":1,"text":"Tennyson’s eagle clasps the crag and falls like a thunderbolt, but he also lives in lonely lands. What does this show?",
   "options":["A poem can carry more than one theme at once.","The poem has no theme.","The eagle is afraid of falling.","The poem is only about the weather."],"answer":0,"from":"28.2 and 28.4 Poetry Corner (Tennyson)","status":"new (the scope's poetry idea)"},
  {"n":14,"section":"Writing","label":"Literary Response Opening","type":"essay_question","points":1,"text":"Write the opening of your literary response (3–5 sentences). Include the book title, the author’s name, your theme claim, and one character’s choice as evidence. Use one transition and one abstract noun (-ity, -ment or -ness), and underline the abstract noun.",
   "key":"Title + Sid Fleischman + a theme claim (an idea, not a topic) + one character choice + a transition + an underlined abstract noun.","from":"28.1–28.4 Writer's Workshop","status":"changed (adds the character-choice focus; now 1 point)"}
 ],
 "passage": {"before": 11, "title": "Reading passage (Chapter 12)", "ch": 12,
   "text": "Praiseworthy shouldered the pick. He gave up trying to explain. It seemed to him that every man in the diggings became hard of hearing when he wanted to, and he’d had enough of that for one day. If they preferred a tall tale to the facts, let them have it.",
   "cite": "Sid Fleischman, By the Great Horn Spoon!, Chapter 12"}
}
assert sum(q['points'] for q in Q['questions']) == 14 and len(Q['questions']) == 14
assert all(len(q['options']) == 4 for q in Q['questions'] if 'options' in q)
io.open(os.path.join(ROOT, 'assessments/g5-ela-wk28-checkin.json'), 'w', encoding='utf-8').write(json.dumps(Q, ensure_ascii=False, indent=1))
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
page = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>G5 Week 28 Check-In Key</title>'
 '<style>body{font:16px/1.5 system-ui,sans-serif;max-width:820px;margin:0 auto;padding:16px;background:#F0F2F8;color:#24324F}h1{font-size:22px;color:#0E1C42}'
 '.q,.psg{background:#fff;border:1px solid #D9E0F0;border-radius:10px;padding:12px 16px;margin:12px 0}.q.new{border-left:5px solid #2B5BA8}.psg{background:#FFF8E6}'
 '.h{font-weight:700;color:#0E1C42}.n{display:inline-block;background:#0E1C42;color:#fff;border-radius:50%%;width:26px;height:26px;text-align:center;line-height:26px;margin-right:6px}'
 '.ok{color:#24502A;font-weight:700}.m{font-size:13px;color:#6B7690;margin-top:6px}</style></head><body>'
 '<h1>%s</h1><p>%s</p><p><b>%s · %d questions · 14 points.</b> Blue edge = changed, fixed or new from the quiz that was on the page.</p>%s</body></html>') % (
 e(Q['title']), e(Q['description']), e(Q['chapters']), len(Q['questions']), rows)
io.open(os.path.join(ROOT, 'assessments/g5-ela-wk28-checkin-key.html'), 'w', encoding='utf-8').write(page)
ICON = {'Grammar': ('grammar', '✏️', 'Grammar: Transitions &amp; Introductory Phrases'), 'Morphology & Vocabulary': ('morph', '🔬', 'Morphology &amp; Vocabulary: <em>fort</em> + <em>val/valid</em>'),
        'Spelling': ('spelling', '🔠', 'Spelling: Abstract Noun Endings <em>&ndash;ity</em>, <em>&ndash;ment</em>, <em>&ndash;ness</em>'), 'Reading': ('reading', '📖', 'Reading: Chapters 10&ndash;12 and the Poem'), 'Writing': ('writing', '✍️', 'Writing: Your Literary Response')}
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
p = os.path.join(ROOT, 'lesson-28-checkin.html')
s = io.open(p, encoding='utf-8', newline='').read(); orig = s
a = s.index('  <div class="section">'); b = s.index('  <div class="gathered-card">', a)
s = s[:a] + ''.join(out) + s[b:]
GA = ("function ga(){\n  var out='WEEK 28 CHECK-IN\\n'+'='.repeat(48)+'\\n\\n';\n"
      "  var mcm={%s};\n  Object.keys(mcm).forEach(k=>{out+=mcm[k]+': '+(mc[k]||'—')+'\\n';});\n"
      "  [%s].forEach(function(r){\n    var e=document.getElementById(r[0]);if(e)out+='\\n'+r[1]+':\\n'+(e.value.trim()||'(no answer)')+'\\n';\n  });\n"
      "  document.getElementById('gatheredOutput').value=out;\n}") % (','.join(mcmap), ','.join(resp))
s, n1 = re.subn(r"function ga\(\)\{.*?\n\}", lambda m: GA, s, count=1, flags=re.S)
if n1 != 1: sys.exit('ga')
if 'mcq7' not in s or "'resp4'" not in s: sys.exit('js maps')
if s.count('<div') - s.count('</div') != orig.count('<div') - orig.count('</div'): sys.exit('page: div balance')
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok: json, key, page;', r_n, 'written,', mc_n, 'multiple choice')
