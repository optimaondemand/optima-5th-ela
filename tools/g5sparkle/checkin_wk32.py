#!/usr/bin/env python3
"""Week 32 check-in (Letter to a Future 5th Grader), Nov 25 2026. Started from lesson-32-checkin.html (13 items for 14 points, three-option
MCs; Q10 tested the invented week 31 'secondary source' of three kinds of courage; Q4 used 'impersistence', which is not a word; 'four novels').
Audited against the four lessons after the week 32 fixes and the scope (v2 scope 32: final editing, morphology reflection, voice/tone/pacing,
poem read aloud, portfolio reflection). Every MC has four options (14 questions, 14 points). Writes assessments/g5-ela-wk32-checkin.json + -key.html;
with --page it rebuilds the question area. Book lines checked: Horn Spoon Ch. 18 (scope_wk30), Bowditch Ch. 12 (OCR).
QTI: python tools/g5sparkle/qti_checkin.py assessments/g5-ela-wk32-checkin.json "planning docs/Week32_CheckIn_QTI.zip"
(Made from checkin_wk31.py.)"""
import json, io, html, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
Q = json.loads(r'''{
 "id": "g5-ela-wk32-checkin",
 "title": "Week 32 Check-In · Letter to a Future 5th Grader",
 "description": "This week you wrote a letter to a future 5th grader about two of the year's novels, studied voice, tone and pacing, read a poem aloud, and did a final review of the year's grammar, roots and spelling.",
 "chapters": "The five novels + one real Gold Rush letter",
 "questions": [
  {
   "n": 1,
   "section": "Grammar",
   "label": "Agreement",
   "type": "multiple_choice_question",
   "points": 1,
   "text": "Which sentence is ready to publish?",
   "options": [
    "Each of the boys were changed by the journey.",
    "Each of the boys was changed by the journey.",
    "each of the boys was changed by the journey.",
    "Each of the boys was changed by the journey"
   ],
   "answer": 1,
   "from": "32.4 Grammar (One Last Check); 32.3 Grammar (was / were); 32.1 Grammar sort",
   "status": "replaced (was a 'which sentence has the best voice' item with three options and no grammar rule)"
  },
  {
   "n": 2,
   "section": "Grammar",
   "label": "Titles",
   "type": "multiple_choice_question",
   "points": 1,
   "text": "Which sentence capitalizes the book title correctly?",
   "options": [
    "I read carry on, mr. bowditch in the fall.",
    "I read Carry On, Mr. Bowditch in the fall.",
    "I read Carry on, mr. Bowditch in the fall.",
    "I read Carry On Mr Bowditch in the fall."
   ],
   "answer": 1,
   "from": "32.2 and 32.4 final grammar checklist (titles); 32.3 Daily Oral Language",
   "status": "replaced (was 'write a sentence that begins with a participial phrase', not taught this week)"
  },
  {
   "n": 3,
   "section": "Grammar",
   "label": "Fix a Run-On",
   "type": "essay_question",
   "points": 1,
   "text": "Fix the capitals and the run-on. Write the sentences correctly.",
   "excerpt": "i chose this book because it made me laugh it also made me think about keeping promises",
   "key": "I chose this book because it made me laugh. It also made me think about keeping promises. (Or: ...laugh, and it also made me think... Capital I twice; the run-on split or joined correctly; end mark.)",
   "from": "32.1-32.4 Daily Oral Language; 32.4 Grammar (before and after)",
   "status": "fixed (same skill; a shorter sentence with no book claims)"
  },
  {
   "n": 4,
   "section": "Morphology & Vocabulary",
   "label": "Prefix",
   "type": "multiple_choice_question",
   "points": 1,
   "text": "In the word inaudible, what does in- mean?",
   "options": [
    "not",
    "into",
    "again",
    "before"
   ],
   "answer": 0,
   "from": "32.4 Morphology (Which word part is doing the work?); 32.3 build the word",
   "status": "replaced (was 'impersistence', which is not an English word)"
  },
  {
   "n": 5,
   "section": "Morphology & Vocabulary",
   "label": "Root",
   "type": "multiple_choice_question",
   "points": 1,
   "text": "The root port means carry. Which word is built from it?",
   "options": [
    "portable",
    "potable",
    "possible",
    "popular"
   ],
   "answer": 0,
   "from": "32.3 word game; year-long root review (port, Bowditch unit)",
   "status": "kept (a root item; four options, a root from the year)"
  },
  {
   "n": 6,
   "section": "Morphology & Vocabulary",
   "label": "Context Clues",
   "type": "multiple_choice_question",
   "points": 1,
   "text": "Read the sentence. What does fortitude mean?",
   "excerpt": "Even after months of storms and hard work, Jack kept going. He showed great fortitude.",
   "options": [
    "strength to keep going through hard times",
    "a large fort",
    "good luck",
    "a loud voice"
   ],
   "answer": 0,
   "from": "32.4 Morphology (-itude, fort); 32.4 Vocabulary list",
   "status": "replaced (was 'name any root and write a sentence')"
  },
  {
   "n": 7,
   "section": "Spelling",
   "label": "Tricky Words",
   "type": "multiple_choice_question",
   "points": 1,
   "text": "Which word is spelled correctly?",
   "options": [
    "definately",
    "separate",
    "embarass",
    "diffrent"
   ],
   "answer": 1,
   "from": "32.1 tap the correct spellings; 32.4 Spelling (type the right spelling)",
   "status": "changed (the week's tricky words; four options)"
  },
  {
   "n": 8,
   "section": "Spelling",
   "label": "Edit for Spelling",
   "type": "essay_question",
   "points": 1,
   "text": "Find and correct every misspelling. Write the sentence correctly.",
   "excerpt": "I recieve a new book every week, and I seperate the ones I love from the ones that embarass me.",
   "key": "I receive a new book every week, and I separate the ones I love from the ones that embarrass me. (receive, separate, embarrass)",
   "from": "32.2 Spelling (find the misspellings in a draft); 32.3 Spelling Show What You Know",
   "status": "fixed (no longer a claim about Praiseworthy)"
  },
  {
   "n": 9,
   "section": "Spelling",
   "label": "Word Families",
   "type": "multiple_choice_question",
   "points": 1,
   "text": "Which word belongs to the same word family as persist?",
   "options": [
    "persistence",
    "perspective",
    "personal",
    "pursuit"
   ],
   "answer": 0,
   "from": "32.1-32.3 spelling list (persistence); week 29 word families",
   "status": "changed (four options)"
  },
  {
   "n": 10,
   "section": "Reading",
   "label": "Pacing",
   "type": "multiple_choice_question",
   "points": 1,
   "text": "Read the lines from By the Great Horn Spoon!, Chapter 18. Why does Sid Fleischman use three short sentences?",
   "excerpt": "They looked very much like a family. They felt like a family. They were a family.",
   "options": [
    "Each sentence goes one step further, and the short last one lands hardest.",
    "He forgot to join them with commas.",
    "They describe three different families.",
    "Short sentences always mean a chapter is ending."
   ],
   "answer": 0,
   "from": "32.1 Read Like a Writer (pacing)",
   "status": "replaced (tested the invented week 31 'secondary source')"
  },
  {
   "n": 11,
   "section": "Reading",
   "label": "Tone",
   "type": "multiple_choice_question",
   "points": 1,
   "text": "Captain Prince doubted Nat's figures, and Nat turned out to be right. What is Nat's tone in these lines from Carry On, Mr. Bowditch, Chapter 12?",
   "excerpt": "“Of course,” Nat said. “It’s a simple matter of mathematics, sir.”",
   "options": [
    "calm and sure",
    "angry",
    "scared",
    "silly"
   ],
   "answer": 0,
   "from": "32.3 Read Like a Writer (tone); 32.3 Virtue Watch",
   "status": "new"
  },
  {
   "n": 12,
   "section": "Reading",
   "label": "Primary Source",
   "type": "multiple_choice_question",
   "points": 1,
   "text": "Louise Clappe wrote letters from a California mining camp in 1851 and 1852. Why is her letter a primary source?",
   "options": [
    "She wrote it at the time, about a place she was living in.",
    "It is a novel about the Gold Rush.",
    "Optima wrote it for this lesson.",
    "It was written in 2026."
   ],
   "answer": 0,
   "from": "32.2 card 'Real history: letters that crossed time'; week 31 sources",
   "status": "new"
  },
  {
   "n": 13,
   "section": "Reading",
   "label": "Poetry",
   "type": "multiple_choice_question",
   "points": 1,
   "text": "In Amy Lowell’s “Wind and Silver,” the third line is much longer than the others. How should a reader read it aloud?",
   "options": [
    "Let it run a little faster, like the flashing fish-ponds, then land softly on the last line.",
    "Skip it, because it is too long.",
    "Stop after every word.",
    "Read it the same way as every other line."
   ],
   "answer": 0,
   "from": "32.2 Poetry Corner (read it three ways; the tip); 32.4 Poetry Corner",
   "status": "new (nothing on the poem before)"
  },
  {
   "n": 14,
   "section": "Writing",
   "label": "Your Letter",
   "type": "essay_question",
   "points": 1,
   "text": "Write the claim sentence of your letter (Read ___ before ___). Then write one reason, with a moment from each of the two books.",
   "key": "A claim that names two of the five novels; one reason; a real moment (or exact words) from each book that supports it.",
   "from": "32.1 letter plan; 32.2 letter draft; 32.2 Read Like a Writer (the claim in your own voice)",
   "status": "replaced (was 'write your final closing sentence')"
  }
 ],
 "passage": {
  "before": 0,
  "title": "",
  "text": "",
  "cite": ""
 }
}''')
assert sum(q['points'] for q in Q['questions']) == 14 and len(Q['questions']) == 14
assert all(len(q['options']) == 4 for q in Q['questions'] if 'options' in q)
io.open(os.path.join(ROOT, 'assessments/g5-ela-wk32-checkin.json'), 'w', encoding='utf-8').write(json.dumps(Q, ensure_ascii=False, indent=1))
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
page = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>G5 Week 32 Check-In Key</title>'
 '<style>body{font:16px/1.5 system-ui,sans-serif;max-width:820px;margin:0 auto;padding:16px;background:#F0F2F8;color:#24324F}h1{font-size:22px;color:#0E1C42}'
 '.q,.psg{background:#fff;border:1px solid #D9E0F0;border-radius:10px;padding:12px 16px;margin:12px 0}.q.new{border-left:5px solid #2B5BA8}.psg{background:#FFF8E6}'
 '.h{font-weight:700;color:#0E1C42}.n{display:inline-block;background:#0E1C42;color:#fff;border-radius:50%%;width:26px;height:26px;text-align:center;line-height:26px;margin-right:6px}'
 '.ok{color:#24502A;font-weight:700}.m{font-size:13px;color:#6B7690;margin-top:6px}</style></head><body>'
 '<h1>%s</h1><p>%s</p><p><b>%s · %d questions · 14 points.</b> Blue edge = changed, fixed or new from the quiz that was on the page.</p>%s</body></html>') % (
 e(Q['title']), e(Q['description']), e(Q['chapters']), len(Q['questions']), rows)
io.open(os.path.join(ROOT, 'assessments/g5-ela-wk32-checkin-key.html'), 'w', encoding='utf-8').write(page)
ICON = {'Grammar': ('grammar', '✏️', 'Grammar: Final Editing'), 'Morphology & Vocabulary': ('morph', '🔬', 'Morphology &amp; Vocabulary: The Year&rsquo;s Roots'),
        'Spelling': ('spelling', '🔠', 'Spelling: Final Review'), 'Reading': ('reading', '📖', 'Reading: Voice, Tone, Pacing and a Real Letter'), 'Writing': ('writing', '✍️', 'Writing: Your Letter')}
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
        s += '      <textarea oninput="ga()" data-label="%s" id="%s" class="response-box%s" placeholder="Write your answer here..."></textarea>\n' % (html.escape(lab), rid, '' if q['n'] >= 14 else ' short')
    out.append(s + '    </div>\n')
out.append('  </div>\n\n')
p = os.path.join(ROOT, 'lesson-32-checkin.html')
s = io.open(p, encoding='utf-8', newline='').read(); orig = s
a = s.index('  <div class="section">'); b = s.index('  <div class="gathered-card"', a)
s = s[:a] + ''.join(out) + s[b:]
GA = ("function ga(){\n  var out='WEEK 32 CHECK-IN\\n'+'='.repeat(48)+'\\n\\n';\n"
      "  var mcm={%s};\n  Object.keys(mcm).forEach(k=>{out+=mcm[k]+': '+(mc[k]||'—')+'\\n';});\n"
      "  [%s].forEach(function(r){\n    var e=document.getElementById(r[0]);if(e)out+='\\n'+r[1]+':\\n'+(e.value.trim()||'(no answer)')+'\\n';\n  });\n"
      "  document.getElementById('gatheredOutput').value=out;\n}") % (','.join(mcmap), ','.join(resp))
s, n1 = re.subn(r"function ga\(\)\{.*?\n\}", lambda m: GA, s, count=1, flags=re.S)
if n1 != 1: sys.exit('ga')
if 'mcq7' not in s or "'resp3'" not in s: sys.exit('js maps')
if s.count('<div') - s.count('</div') != orig.count('<div') - orig.count('</div'): sys.exit('page: div balance')
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok: json, key, page;', r_n, 'written,', mc_n, 'multiple choice')
