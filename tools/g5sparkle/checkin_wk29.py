#!/usr/bin/env python3
"""Week 29 check-in (By the Great Horn Spoon! Ch. 13-15 + voice/tone day), Nov 24 2026. Started from lesson-29-checkin.html (13 items, three-option MCs,
the prospect family with prosperous, the beans line misquoted, nothing on Read Like a Writer or the poem); there is no Oct 11 Week29 QTI zip.
Audited against the four lessons after the week 29 fixes, the scope (v2 scope 29) and the book text. Every MC has four options (14 questions, 14 points).
Writes assessments/g5-ela-wk29-checkin.json + -key.html and rebuilds the question area of the page.
QTI: python tools/g5sparkle/qti_checkin.py assessments/g5-ela-wk29-checkin.json "planning docs/Week29_CheckIn_QTI.zip" """
import json, io, html, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
Q = {
 "id": "g5-ela-wk29-checkin", "title": "Week 29 Check-In · By the Great Horn Spoon!",
 "description": "This week you read Chapters 13 to 15. You practiced sentence variety, the endings -ous, -ive and -ity, word families, how a writer builds voice and tone, every part of a poem at once, and revising your adventure for voice, dialogue and description. Show what you know.",
 "chapters": "Ch. 13–15",
 "questions": [
  {"n":1,"section":"Grammar","label":"Identification","type":"multiple_choice_question","points":1,"text":"Which sentence begins with a participial phrase?",
   "options":["Jack held on to Stubb.","Holding the rope tight, Jack waited.","When the dust cleared, a face appeared.","In the morning, they struck the tent."],"answer":1,"from":"29.1–29.4 Grammar","status":"fixed (the old answer was an invented Ch. 15 sentence; a fourth option added)"},
  {"n":2,"section":"Grammar","label":"Vary the Length","type":"essay_question","points":1,"text":"Rewrite this as two sentences, one short and one longer.",
   "excerpt":"Jack walked around the burro and sized him up and then he spit in his hands and climbed on.",
   "key":"Any two sentences, one short and one longer, e.g. Jack sized up the burro. Then he spit in his hands and climbed onto Stubb’s back.","from":"29.1 Grammar (vary length); 29.2 Show What You Know","status":"changed (Ch. 14 events instead of the Ch. 15 coyote hole)"},
  {"n":3,"section":"Grammar","label":"Sentence Openers","type":"multiple_choice_question","points":1,"text":"Which group of sentences starts its sentences in the most different ways?",
   "options":["Jack panned. Jack dug. Jack rested.","Jack panned all morning. After lunch, he dug. Tired at last, he rested.","Jack panned and dug and rested.","Jack panned, and Jack dug, and Jack rested."],"answer":1,"from":"29.1 sort; 29.3 openers; 29.4 before and after","status":"new (replaces a sentence-writing item; the scope's sentence variety)"},
  {"n":4,"section":"Morphology & Vocabulary","label":"Suffix","type":"multiple_choice_question","points":1,"text":"Which ending turns a word into a describing word that means full of?",
   "options":["-ity","-ous","-ive","-ment"],"answer":1,"from":"29.1–29.4 Morphology","status":"kept (a fourth option added)"},
  {"n":5,"section":"Morphology & Vocabulary","label":"Word Meaning","type":"multiple_choice_question","points":1,"text":"What does evasive mean?",
   "options":["Tending to avoid or escape","Full of courage","The state of being well known","A person who gives help"],"answer":0,"from":"29.1–29.4 Vocabulary","status":"changed (was 'use evasive in a sentence'; now multiple choice)"},
  {"n":6,"section":"Morphology & Vocabulary","label":"Context Clues","type":"multiple_choice_question","points":1,"text":"Read the line from Chapter 13. What does notoriety mean here?",
   "excerpt":"The truth of the matter was that Praiseworthy himself began to enjoy his notoriety.",
   "options":["Being well known for something bold","Being very tired","Being afraid of crowds","Being good with money"],"answer":0,"from":"29.1 Read Like a Writer; Vocabulary (notoriety, Ch. 13)","status":"new (vocabulary in context)"},
  {"n":7,"section":"Spelling","label":"Word Families","type":"multiple_choice_question","points":1,"text":"Which word is NOT in the prospect family?",
   "options":["prospector","prospecting","prosperous","prospective"],"answer":2,"from":"29.1–29.4 Spelling (prospect family)","status":"fixed (the old item put prosperous in the prospect family)"},
  {"n":8,"section":"Spelling","label":"Build a Family","type":"essay_question","points":1,"text":"Write three words in the create family. Underline the part that stays the same in all three.",
   "key":"Any three of create, creation, creative, creator, creativity; the base creat stays the same.","from":"29.1–29.3 Spelling families","status":"changed (the old item used the prospect family with prosperous)"},
  {"n":9,"section":"Spelling","label":"Spelling Shift","type":"multiple_choice_question","points":1,"text":"Which word is spelled correctly?",
   "options":["decidive","decisive","desicive","decisiv"],"answer":1,"from":"29.1 sort; 29.4 Spelling","status":"new (the d to s shift in a family)"},
  {"n":10,"section":"Reading","label":"Key Detail","type":"multiple_choice_question","points":1,"text":"Why does Praiseworthy call the bushel of neckties “a brilliant purchase”?",
   "options":["He plans to sell them when the miners want them, and buy a burro.","He wants to wear a different tie every day.","He thinks the auctioneer will give the money back.","He wants Jack to feel better, though he has no plan."],"answer":0,"from":"29.1 Reading Q2 (Ch. 13)","status":"kept (a fourth option added)"},
  {"n":11,"section":"Reading","label":"Character and Tone","type":"essay_question","points":1,"text":"Right after this, Praiseworthy says, “Put some beans on to fry, partner Jack. First thing in the morning we’ll start for Shirt-tail Camp.” What does this show about him? Answer in 2–3 sentences.",
   "key":"He does not give up or dwell on the disappointment; he moves straight to the next plan, steady and hopeful, which keeps the book's tone light.","from":"29.3 Reading Q2 (Ch. 15); 29.4 technique 5","status":"fixed (the line is now quoted exactly; the passage is printed above it)"},
  {"n":12,"section":"Reading","label":"Read Like a Writer","type":"multiple_choice_question","points":1,"text":"In Chapter 15, Fleischman writes: “Yellow poppies had burst open on the hillsides like scatterings of fools’ gold.” What makes this strong description?",
   "options":["It names specific things and compares them to something from the gold fields.","It uses only very short sentences.","It tells exactly how many poppies there were.","It is a line of dialogue."],"answer":0,"from":"29.3 Read Like a Writer (Ch. 15)","status":"new (the scope's Read Like a Writer focus: description)"},
  {"n":13,"section":"Reading","label":"Poetry","type":"multiple_choice_question","points":1,"text":"“Windy Nights” and “Fog” use the same five parts of a poem. How are they different?",
   "options":["Windy Nights gallops with rhyme and a strong beat; Fog is quiet, with short lines that do not rhyme.","Both poems rhyme in pairs.","Fog has a stronger beat than Windy Nights.","Windy Nights has no figurative language."],"answer":0,"from":"29.2 and 29.4 Poetry Corner","status":"new (the scope's poetry idea)"},
  {"n":14,"section":"Writing","label":"Revise for Voice","type":"essay_question","points":1,"text":"Copy one sentence from your adventure draft. Then rewrite it to improve its voice, its dialogue or its description, and name which one you improved.",
   "key":"Original + a revised sentence that is clearly better in the named way (a storyteller's voice, dialogue that sounds like the character, or a specific detail).","from":"29.1–29.4 Writer's Workshop","status":"kept (now 1 point)"}
 ],
 "passage": {"before": 11, "title": "Reading passage (Chapter 15)", "ch": 15,
   "text": "Just as quickly Praiseworthy unclasped his knife and ripped open the lining. They laid open every inch of the coat. They examined and re-examined it, and Jack’s excitement died away. There was no map. There had never been a map sewn in the lining of the coat.",
   "cite": "Sid Fleischman, By the Great Horn Spoon!, Chapter 15"}
}
assert sum(q['points'] for q in Q['questions']) == 14 and len(Q['questions']) == 14
assert all(len(q['options']) == 4 for q in Q['questions'] if 'options' in q)
io.open(os.path.join(ROOT, 'assessments/g5-ela-wk29-checkin.json'), 'w', encoding='utf-8').write(json.dumps(Q, ensure_ascii=False, indent=1))
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
page = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>G5 Week 29 Check-In Key</title>'
 '<style>body{font:16px/1.5 system-ui,sans-serif;max-width:820px;margin:0 auto;padding:16px;background:#F0F2F8;color:#24324F}h1{font-size:22px;color:#0E1C42}'
 '.q,.psg{background:#fff;border:1px solid #D9E0F0;border-radius:10px;padding:12px 16px;margin:12px 0}.q.new{border-left:5px solid #2B5BA8}.psg{background:#FFF8E6}'
 '.h{font-weight:700;color:#0E1C42}.n{display:inline-block;background:#0E1C42;color:#fff;border-radius:50%%;width:26px;height:26px;text-align:center;line-height:26px;margin-right:6px}'
 '.ok{color:#24502A;font-weight:700}.m{font-size:13px;color:#6B7690;margin-top:6px}</style></head><body>'
 '<h1>%s</h1><p>%s</p><p><b>%s · %d questions · 14 points.</b> Blue edge = changed, fixed or new from the quiz that was on the page.</p>%s</body></html>') % (
 e(Q['title']), e(Q['description']), e(Q['chapters']), len(Q['questions']), rows)
io.open(os.path.join(ROOT, 'assessments/g5-ela-wk29-checkin-key.html'), 'w', encoding='utf-8').write(page)
ICON = {'Grammar': ('grammar', '✏️', 'Grammar: Sentence Variety for Style'), 'Morphology & Vocabulary': ('morph', '🔬', 'Morphology &amp; Vocabulary: <em>&ndash;ous</em>, <em>&ndash;ive</em>, <em>&ndash;ity</em>'),
        'Spelling': ('spelling', '🔠', 'Spelling: Word Families'), 'Reading': ('reading', '📖', 'Reading: Chapters 13&ndash;15, Voice and the Poems'), 'Writing': ('writing', '✍️', 'Writing: Revise Your Adventure')}
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
p = os.path.join(ROOT, 'lesson-29-checkin.html')
s = io.open(p, encoding='utf-8', newline='').read(); orig = s
a = s.index('  <div class="section">'); b = s.index('  <div class="gathered-card">', a)
s = s[:a] + ''.join(out) + s[b:]
GA = ("function ga(){\n  var out='WEEK 29 CHECK-IN\\n'+'='.repeat(48)+'\\n\\n';\n"
      "  var mcm={%s};\n  Object.keys(mcm).forEach(k=>{out+=mcm[k]+': '+(mc[k]||'—')+'\\n';});\n"
      "  [%s].forEach(function(r){\n    var e=document.getElementById(r[0]);if(e)out+='\\n'+r[1]+':\\n'+(e.value.trim()||'(no answer)')+'\\n';\n  });\n"
      "  document.getElementById('gatheredOutput').value=out;\n}") % (','.join(mcmap), ','.join(resp))
s, n1 = re.subn(r"function ga\(\)\{.*?\n\}", lambda m: GA, s, count=1, flags=re.S)
if n1 != 1: sys.exit('ga')
if 'mcq7' not in s or "'resp4'" not in s: sys.exit('js maps')
if s.count('<div') - s.count('</div') != orig.count('<div') - orig.count('</div'): sys.exit('page: div balance')
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok: json, key, page;', r_n, 'written,', mc_n, 'multiple choice')
