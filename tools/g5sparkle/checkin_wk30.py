#!/usr/bin/env python3
"""Week 30 check-in (By the Great Horn Spoon! Ch. 16-18 + whole-book synthesis), Nov 24 2026. Started from lesson-30-checkin.html (13 items, three-option MCs,
'valour' planted as a misspelling, the prospect family from week 29, the proposal line misquoted, 'Jack ... dragged along', nothing on the poem);
there is no Oct 11 Week30 QTI zip. Audited against the four lessons after the week 30 fixes, the scope (v2 scope 30) and the book text.
Every MC has four options (14 questions, 14 points). Writes assessments/g5-ela-wk30-checkin.json + -key.html and rebuilds the question area of the page.
QTI: python tools/g5sparkle/qti_checkin.py assessments/g5-ela-wk30-checkin.json "planning docs/Week30_CheckIn_QTI.zip" """
import json, io, html, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
Q = {
 "id": "g5-ela-wk30-checkin", "title": "Week 30 Check-In · By the Great Horn Spoon!",
 "description": "This week you finished the novel with Chapters 16 to 18 and looked back at the whole book. You practiced editing for punctuation, capitalization and clarity, reviewed root families from the unit, edited for spelling, saw how the parts of a poem combine to make meaning, and wrote and published the conclusion of your adventure.",
 "chapters": "Ch. 16–18 + the whole book",
 "questions": [
  {"n":1,"section":"Grammar","label":"Dialogue Punctuation","type":"multiple_choice_question","points":1,"text":"Which sentence is punctuated and capitalized correctly?",
   "options":["“We’ve struck it rich” Jack shouted.","“We’ve struck it rich!” Jack shouted.","“We’ve struck it rich!,” Jack shouted.","“We’ve struck it rich!” jack shouted."],"answer":1,"from":"30.1–30.2 Grammar checklist (dialogue punctuation, capitals)","status":"changed (was a three-option item built on the proposal line)"},
  {"n":2,"section":"Grammar","label":"Edit It","type":"essay_question","points":1,"text":"Edit this sentence for every error in punctuation and capitalization. Write it correctly.",
   "excerpt":"aunt arabella was smiling through a wet sparkle in her eyes marry you why of course i thought youd never ask",
   "key":"Aunt Arabella was smiling through a wet sparkle in her eyes. “Marry you? Why, of course. I thought you’d never ask.”","from":"30.4 Daily Oral Language (Ch. 18 line)","status":"fixed (the old item added a made-up ‘she said’; now the book’s line)"},
  {"n":3,"section":"Grammar","label":"Clarity: Agreement","type":"multiple_choice_question","points":1,"text":"Which sentence is correct?",
   "options":["Each of the miners were paid.","Each of the miners was paid.","Each of the miners are paid.","Each of the miner was paid."],"answer":1,"from":"30.1 sort (agreement pass); 30.3 was/were; 30.4 Grammar","status":"replaced (was ‘write a sentence with a semicolon’, which the pages only list)"},
  {"n":4,"section":"Morphology & Vocabulary","label":"Root Family","type":"multiple_choice_question","points":1,"text":"Which word really has the root fort, meaning strong?",
   "options":["fortitude","fortune","forty","forth"],"answer":0,"from":"30.1–30.4 Morphology (fort family; fortune taught as a look-alike in week 28)","status":"kept (look-alike options added)"},
  {"n":5,"section":"Morphology & Vocabulary","label":"Root Family","type":"multiple_choice_question","points":1,"text":"Which word is in the same root family as audience?",
   "options":["audacious","author","audible","award"],"answer":2,"from":"30.1–30.4 Morphology (aud = hear); 30.3 fill-in","status":"replaced (was the -ance suffix item; this week reviews root families)"},
  {"n":6,"section":"Morphology & Vocabulary","label":"Context Clues","type":"multiple_choice_question","points":1,"text":"Read the line from Chapter 16. What does reprieve mean here?",
   "excerpt":"“Doc Higgins,” said the Justice of the Peace, “you got yourself a temporary reprieve.”",
   "options":["a delay of his punishment","a new job in camp","a ride out of town","a reward for good work"],"answer":0,"from":"30.1–30.4 Vocabulary (reprieve, Ch. 16)","status":"replaced (was ‘choose any root and write a sentence’; now vocabulary in context)"},
  {"n":7,"section":"Spelling","label":"Grade-Level Words","type":"multiple_choice_question","points":1,"text":"Which word is spelled correctly?",
   "options":["recieve","occured","embarrass","seperate"],"answer":2,"from":"30.1 sort; 30.2 taps; 30.4 fixes","status":"changed (unit words instead of the prospect family)"},
  {"n":8,"section":"Spelling","label":"Edit for Spelling","type":"essay_question","points":1,"text":"Find and correct every misspelling. Write the sentences correctly.",
   "excerpt":"Praiseworthy showed remarkable fortitued and tenasity on the voyage. Nevertheles, his notoreity in hangtown came from genuine courage.",
   "key":"Praiseworthy showed remarkable fortitude and tenacity on the voyage. Nevertheless, his notoriety in Hangtown came from genuine courage. (fortitude, tenacity, Nevertheless, notoriety, Hangtown)","from":"30.2–30.3 Spelling editing","status":"fixed (the old item planted the British ‘valour’ as an error)"},
  {"n":9,"section":"Spelling","label":"Base + Ending","type":"multiple_choice_question","points":1,"text":"Which word adds an ending to its base word correctly?",
   "options":["arguement","truely","couragous","valuable"],"answer":3,"from":"30.1–30.4 Spelling (word analysis); the week’s letter game","status":"replaced (the old item tested week 29’s prospect family)"},
  {"n":10,"section":"Reading","label":"Key Event","type":"multiple_choice_question","points":1,"text":"How do Praiseworthy and Jack find their gold?",
   "options":["They follow Dr. Buckbee’s map to its X-mark.","They dig a grave the Justice of the Peace ordered, and hit bedrock.","Pitch-pine Billy tells them where to dig.","They pan the river at Coloma."],"answer":1,"from":"30.1 Reading (Ch. 16); 30.2 Read Like a Writer","status":"kept (a fourth option added)"},
  {"n":11,"section":"Reading","label":"Character","type":"multiple_choice_question","points":1,"text":"Why does Praiseworthy speak up for Cut-Eye Higgins at Shirt-tail Camp?",
   "options":["He thinks Higgins is innocent.","He wants to be the camp’s lawyer.","He gave his word as part of a bargain, and he stands by it.","Jack begs him to."],"answer":2,"from":"30.1 Reading Q1 (Ch. 16: “He’d given his word and he had to stand by it.”)","status":"new"},
  {"n":12,"section":"Reading","label":"Theme","type":"essay_question","points":1,"text":"Near the end, Praiseworthy says this line. Explain how it works as a proposal of marriage and as a way to sum up the whole gold rush story.",
   "excerpt":"“Maybe this isn’t the time or the place, Miss Arabella, but when a man strikes gold he doesn’t lose any time staking a claim.”",
   "key":"Staking a claim means quickly marking what you have found so no one else takes it; Praiseworthy has ‘struck gold’ in Arabella and wants to claim her first. It sums up the story because the partners came for gold but the real treasure is the family.","from":"30.3 Reading Q1 (Ch. 18)","status":"fixed (the line is now quoted exactly)"},
  {"n":13,"section":"Reading","label":"Poetry","type":"multiple_choice_question","points":1,"text":"In “Eldorado,” why does the word shadow come back in every stanza?",
   "options":["It rhymes with knight.","It ties the stanzas together and grows darker as the knight’s search goes on.","It is the name of the knight’s horse.","It shows that the whole poem happens at night."],"answer":1,"from":"30.2 and 30.4 Poetry Corner","status":"new (nothing on the poem before)"},
  {"n":14,"section":"Writing","label":"Your Conclusion","type":"essay_question","points":1,"text":"Copy the last two or three sentences of your published adventure. Then explain in one sentence how your ending connects the adventure, your hero, and what the story means.",
   "key":"The student’s ending plus one sentence naming how it ties together what happened, how the hero changed, and the story’s meaning.","from":"30.1–30.4 Read Like a Writer (conclusions) and Writer’s Workshop","status":"changed (was a general reflection; now the week’s conclusion focus, 1 point)"}
 ],
 "passage": {"before": 10, "title": "Reading passage (Chapter 16)", "ch": 16,
   "text": "They chose a bare spot about half a mile from camp. It was on a bluff covered with oat straw and overlooking the river. They pulled pick and shovel from Stubb’s pack ropes and set to work. “Fine-looking country, isn’t it?” Praiseworthy muttered. “Even to be buried in.” Jack tried not to think about Boston. It would soon be time to start back and all they had to show for their labors was a worthless map. Poor Aunt Arabella, he thought. They would lose the house for sure. The entire trip to California was beginning to look like a wild-goose chase. When they got the hole four feet deep they couldn’t go any farther. They hit bedrock. And struck gold.",
   "cite": "Sid Fleischman, By the Great Horn Spoon!, Chapter 16"}
}
assert sum(q['points'] for q in Q['questions']) == 14 and len(Q['questions']) == 14
assert all(len(q['options']) == 4 for q in Q['questions'] if 'options' in q)
io.open(os.path.join(ROOT, 'assessments/g5-ela-wk30-checkin.json'), 'w', encoding='utf-8').write(json.dumps(Q, ensure_ascii=False, indent=1))
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
page = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>G5 Week 30 Check-In Key</title>'
 '<style>body{font:16px/1.5 system-ui,sans-serif;max-width:820px;margin:0 auto;padding:16px;background:#F0F2F8;color:#24324F}h1{font-size:22px;color:#0E1C42}'
 '.q,.psg{background:#fff;border:1px solid #D9E0F0;border-radius:10px;padding:12px 16px;margin:12px 0}.q.new{border-left:5px solid #2B5BA8}.psg{background:#FFF8E6}'
 '.h{font-weight:700;color:#0E1C42}.n{display:inline-block;background:#0E1C42;color:#fff;border-radius:50%%;width:26px;height:26px;text-align:center;line-height:26px;margin-right:6px}'
 '.ok{color:#24502A;font-weight:700}.m{font-size:13px;color:#6B7690;margin-top:6px}</style></head><body>'
 '<h1>%s</h1><p>%s</p><p><b>%s · %d questions · 14 points.</b> Blue edge = changed, fixed or new from the quiz that was on the page.</p>%s</body></html>') % (
 e(Q['title']), e(Q['description']), e(Q['chapters']), len(Q['questions']), rows)
io.open(os.path.join(ROOT, 'assessments/g5-ela-wk30-checkin-key.html'), 'w', encoding='utf-8').write(page)
ICON = {'Grammar': ('grammar', '✏️', 'Grammar: Editing for Punctuation, Capitalization and Clarity'), 'Morphology & Vocabulary': ('morph', '🔬', 'Morphology &amp; Vocabulary: Root Families'),
        'Spelling': ('spelling', '🔠', 'Spelling: Editing for Spelling'), 'Reading': ('reading', '📖', 'Reading: Chapters 16&ndash;18, the Whole Book and the Poem'), 'Writing': ('writing', '✍️', 'Writing: Your Conclusion')}
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
p = os.path.join(ROOT, 'lesson-30-checkin.html')
s = io.open(p, encoding='utf-8', newline='').read(); orig = s
a = s.index('  <div class="section">'); b = s.index('  <div class="gathered-card">', a)
s = s[:a] + ''.join(out) + s[b:]
GA = ("function ga(){\n  var out='WEEK 30 FINAL UNIT CHECK-IN\\n'+'='.repeat(48)+'\\n\\n';\n"
      "  var mcm={%s};\n  Object.keys(mcm).forEach(k=>{out+=mcm[k]+': '+(mc[k]||'—')+'\\n';});\n"
      "  [%s].forEach(function(r){\n    var e=document.getElementById(r[0]);if(e)out+='\\n'+r[1]+':\\n'+(e.value.trim()||'(no answer)')+'\\n';\n  });\n"
      "  document.getElementById('gatheredOutput').value=out;\n}") % (','.join(mcmap), ','.join(resp))
s, n1 = re.subn(r"function ga\(\)\{.*?\n\}", lambda m: GA, s, count=1, flags=re.S)
if n1 != 1: sys.exit('ga')
if 'mcq7' not in s or "'resp4'" not in s: sys.exit('js maps')
if s.count('<div') - s.count('</div') != orig.count('<div') - orig.count('</div'): sys.exit('page: div balance')
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok: json, key, page;', r_n, 'written,', mc_n, 'multiple choice')
