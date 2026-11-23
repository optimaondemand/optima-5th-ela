#!/usr/bin/env python3
"""Week 25 check-in (By the Great Horn Spoon!, Gold Rush background + Ch. 1-3), Nov 22 2026. Started from the
week 25 quiz already on lesson-25-checkin.html (no Week25 QTI zip existed), audited against the four lessons
after the week 25 fixes, the scope (v2 scope 25) and the book text. Every MC now has four options; the invented
"born to be a butler" quote is gone; audacious (not an aud word) is replaced; Q11 has answer choices; a Read Like
a Writer item is added (14 questions, 14 points). Writes assessments/g5-ela-wk25-checkin.json + -key.html and
rebuilds the question area of lesson-25-checkin.html.
QTI: python tools/g5sparkle/qti_checkin.py assessments/g5-ela-wk25-checkin.json "planning docs/Week25_CheckIn_QTI.zip" """
import json, io, html, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
Q = {
 "id": "g5-ela-wk25-checkin", "title": "Week 25 Check-In · By the Great Horn Spoon!",
 "description": "This week you learned the real history of the Gold Rush and read Chapters 1 to 3. You practiced prepositional phrases for setting, the roots aud and or, long place names and Gold Rush words, and planning an adventure. Show what you know.",
 "chapters": "Gold Rush background and Ch. 1–3",
 "questions": [
  {"n":1,"section":"Grammar","label":"Identification","type":"multiple_choice_question","points":1,"text":"Which sentence uses prepositional phrases to tell where something happens?",
   "options":["Jack was cold and hungry.","Below decks, in the creaking darkness, two stowaways waited.","Praiseworthy was calm and polite.","The captain shouted loudly."],"answer":1,
   "from":"25.1–25.4 Grammar (prepositional phrases for setting)","status":"fixed (four options; the old A and C were not sentences)"},
  {"n":2,"section":"Grammar","label":"Add a Phrase","type":"essay_question","points":1,"text":"Rewrite this sentence. Add a prepositional phrase that tells where or when the action happens.","excerpt":"The captain paced and growled to himself.",
   "key":"Any prepositional phrase of place or time, e.g. In his cabin, the captain paced and growled to himself.","from":"25.1 DOL; 25.2–25.3 Grammar","status":"kept"},
  {"n":3,"section":"Grammar","label":"Application","type":"essay_question","points":1,"text":"Write one sentence about the Lady Wilma's voyage with at least two prepositional phrases. Underline each one.",
   "key":"Two or more prepositional phrases, e.g. At dawn, the ship sailed out of Boston harbor.","from":"25.2–25.3 Grammar (Show What You Know, stacking)","status":"kept"},
  {"n":4,"section":"Morphology & Vocabulary","label":"Root","type":"multiple_choice_question","points":1,"text":"Which pair of words both carry the root or, meaning speak?",
   "options":["audible, audience","oration, oracle","auditorium, audition","audio, auditory"],"answer":1,"from":"25.1–25.4 Morphology","status":"kept (a fourth option added)"},
  {"n":5,"section":"Morphology & Vocabulary","label":"Context Clues","type":"multiple_choice_question","points":1,"text":"Read the sentence from Chapter 2. What does undaunted mean?",
   "excerpt":"“The truth of the matter was that neither Jack nor the butler had the slightest idea how to go about catching a thief. But Praiseworthy was undaunted.”",
   "options":["Not scared off or discouraged","Very tired","Angry and loud","Lost and confused"],"answer":0,"from":"25.1–25.4 Vocabulary (undaunted)","status":"replaced (audacious only looks like an aud word; it comes from a Latin word for bold)"},
  {"n":6,"section":"Morphology & Vocabulary","label":"Use the Word","type":"essay_question","points":1,"text":"Use the word argonaut in a sentence that shows its link to the Greek myth and to the Gold Rush.",
   "key":"A Gold Rush seeker named after Jason's sailors who sailed for the Golden Fleece, e.g. Like the Argonauts of the old myth, the gold-seekers sailed off to find gold.","from":"25.1 Vocabulary (argonaut); Ch. 1","status":"kept"},
  {"n":7,"section":"Spelling","label":"Syllables","type":"multiple_choice_question","points":1,"text":"Which word has five syllables?",
   "options":["Sacramento","equator","California","Argonaut"],"answer":2,"from":"25.1–25.3 Spelling","status":"kept (a fourth option added)"},
  {"n":8,"section":"Spelling","label":"Break It Down","type":"essay_question","points":1,"text":"Write Patagonia in syllables with dots between them. Then write the loudest syllable in capital letters.",
   "key":"Pat•a•go•ni•a; stressed syllable GO.","from":"25.1–25.3 Spelling","status":"kept"},
  {"n":9,"section":"Spelling","label":"Spell It in Context","type":"essay_question","points":1,"text":"Write one sentence about the Gold Rush that uses one of this week's place names and one Gold Rush word (Argonaut or passenger). Spell both correctly.",
   "key":"California, Sacramento, Patagonia or equator + Argonaut or passenger, both spelled correctly.","from":"25.3 Spelling Show What You Know","status":"changed (the scope adds Gold Rush words)"},
  {"n":10,"section":"Reading","label":"Comprehension","type":"multiple_choice_question","points":1,"text":"Why do Jack and Praiseworthy end up shoveling coal at the end of Chapter 1?",
   "options":["Jack refused to be ship's boy and chose to stay with Praiseworthy.","Captain Swain put them in chains.","They volunteered to fix the boiler.","The cook needed help in the galley."],"answer":0,"from":"25.2 Reading (Ch. 1)","status":"kept (a fourth option added)"},
  {"n":11,"section":"Reading","label":"Inference","type":"multiple_choice_question","points":1,"text":"Read the passage from Chapter 2. What does it show about Praiseworthy's plan?",
   "options":["The sow could really tell who was dishonest.","The thief was afraid to touch the sow, so his finger stayed clean.","Praiseworthy saw the thief in the dark.","The captain found the money in the thief's cabin."],"answer":1,"from":"25.3 Reading (Ch. 2)","status":"fixed (it had no answer choices)"},
  {"n":12,"section":"Reading","label":"Theme","type":"essay_question","points":1,"text":"Praiseworthy says, “I was born to my calling” (he means a butler). Yet in Chapters 1–3 he hides in a barrel, shovels coal, and catches a thief. What is one idea the author is showing about who a person really is? Use one detail.",
   "key":"A person is more than a job title; character shows in what you do (e.g. he outwits the thief with the coal-dust sow).","from":"25.4 Reading Q3; What Good Readers Do","status":"fixed (the quote was invented: “born to be a butler”)"},
  {"n":13,"section":"Writing","label":"Read Like a Writer","type":"essay_question","points":1,"text":"This sentence states Jack's problem plainly. Write one sentence that states your own hero's problem just as plainly.",
   "excerpt":"“And then Jack had overheard Banker Stites tell Aunt Arabella that her inheritance was almost gone.” (Chapter 1)",
   "key":"One clear sentence that names the hero and the problem.","from":"25.2 Read Like a Writer (Ch. 1)","status":"new (the scope's Read Like a Writer focus)"},
  {"n":14,"section":"Writing","label":"Your Plan","type":"essay_question","points":1,"text":"Sum up your adventure story plan in 3–5 sentences: your hero, the problem, the setting, and what is at stake.",
   "key":"All four parts present.","from":"25.1–25.4 Writer's Workshop","status":"kept (now 1 point)"}
 ],
 "passage": {"before": 11, "title": "Reading passage (Chapter 2)", "ch": 2,
   "text": "“But one of you, fearing that the sow's squeal would give you away — one of you approached but didn't touch a finger to her back. Look around you, gentlemen. If there is a man among you without coal dust on his finger — he has exposed himself as the thief!”",
   "cite": "Sid Fleischman, By the Great Horn Spoon!, Chapter 2"}
}
assert sum(q['points'] for q in Q['questions']) == 14
io.open(os.path.join(ROOT, 'assessments/g5-ela-wk25-checkin.json'), 'w', encoding='utf-8').write(json.dumps(Q, ensure_ascii=False, indent=1))
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
page = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>G5 Week 25 Check-In Key</title>'
 '<style>body{font:16px/1.5 system-ui,sans-serif;max-width:820px;margin:0 auto;padding:16px;background:#F0F2F8;color:#24324F}h1{font-size:22px;color:#0E1C42}'
 '.q,.psg{background:#fff;border:1px solid #D9E0F0;border-radius:10px;padding:12px 16px;margin:12px 0}.q.new{border-left:5px solid #2B5BA8}.psg{background:#FFF8E6}'
 '.h{font-weight:700;color:#0E1C42}.n{display:inline-block;background:#0E1C42;color:#fff;border-radius:50%%;width:26px;height:26px;text-align:center;line-height:26px;margin-right:6px}'
 '.ok{color:#24502A;font-weight:700}.m{font-size:13px;color:#6B7690;margin-top:6px}</style></head><body>'
 '<h1>%s</h1><p>%s</p><p><b>%s · %d questions · 14 points.</b> Blue edge = changed, fixed or new from the quiz that was on the page.</p>%s</body></html>') % (
 e(Q['title']), e(Q['description']), e(Q['chapters']), len(Q['questions']), rows)
io.open(os.path.join(ROOT, 'assessments/g5-ela-wk25-checkin-key.html'), 'w', encoding='utf-8').write(page)
ICON = {'Grammar': ('grammar', '📝', 'Grammar: Prepositional Phrases'), 'Morphology & Vocabulary': ('morph', '🔬', 'Morphology &amp; Vocabulary'),
        'Spelling': ('spelling', '🔠', 'Spelling: Geography and Gold Rush Words'), 'Reading': ('reading', '📖', 'Reading: Chapters 1&ndash;3'), 'Writing': ('writing', '✍️', 'Writing: Your Adventure Plan')}
out, written, mcs, mc_n, r_n, sec, sn = [], [], [], 0, 0, None, 0
for q in Q['questions']:
    if q['section'] != sec:
        if sec: out.append('  </div>\n\n')
        sec = q['section']; sn += 1; cls, ic, title = ICON[sec]
        pts = sum(x['points'] for x in Q['questions'] if x['section'] == sec)
        out.append('  <!-- SECTION %d: %s -->\n  <div class="section">\n    <div class="section-head">\n      <div class="section-icon %s">%s</div>\n      <div><div class="section-title">%s</div><div class="section-pts">%d points</div></div>\n    </div>\n\n' % (sn, sec.upper(), cls, ic, title, pts))
    if q['n'] == Q['passage']['before']:
        out.append('    <div class="excerpt">%s<br><span style="font-size:13px;">&mdash; Sid Fleischman, <em>By the Great Horn Spoon!</em>, Chapter %d</span></div>\n\n' % (e(Q['passage']['text']), Q['passage']['ch']))
    s = '    <div class="question">\n      <div class="q-label">%s <span class="pts">%d pt</span></div>\n      <div class="q-text"><span class="q-number">%d</span>%s</div>\n' % (e(q['label']), q['points'], q['n'], e(q['text']))
    if q.get('excerpt'): s += '      <div class="excerpt">%s</div>\n' % e(q['excerpt'])
    if 'options' in q:
        mc_n += 1; qid = 'mcq%d' % mc_n
        s += '      <ul class="options" data-qid="%s">\n' % qid + ''.join('        <li onclick="selectOption(this,\'%s\')"><span class="opt-letter">%s</span>%s</li>\n' % (qid, 'ABCD'[i], e(o)) for i, o in enumerate(q['options'])) + '      </ul>\n'
        mcs.append("%s:'%s Q%d (MC)'" % (qid, q['section'].split(' ')[0], q['n']))
    else:
        r_n += 1; rid = 'resp%d' % r_n
        lab = 'Q%d: %s — %s' % (q['n'], q['section'], q['label'])
        written.append("    ['%s','%s']," % (rid, lab.replace("'", "\\'")))
        s += '      <textarea oninput="gatherAnswers()" data-label="%s" id="%s" class="response-box%s" placeholder="Write your answer here..."></textarea>\n' % (html.escape(lab), rid, '' if q['n'] >= 12 else ' short')
    out.append(s + '    </div>\n\n')
out.append('  </div>\n\n')
p = os.path.join(ROOT, 'lesson-25-checkin.html')
s = io.open(p, encoding='utf-8', newline='').read(); orig = s
a = s.index('  <!-- SECTION 1: GRAMMAR -->'); b = s.index('  <!-- GATHERED ANSWERS -->', a)
s = s[:a] + ''.join(out) + s[b:]
import re
s, n1 = re.subn(r"var mcqs = \{[^}]*\};", lambda m: "var mcqs = {%s};" % ','.join(mcs), s)
s, n2 = re.subn(r"var written = \[\n.*?\n  \];", lambda m: "var written = [\n%s\n  ];" % '\n'.join(written), s, flags=re.S)
if (n1, n2) != (1, 1): sys.exit('page js %d %d' % (n1, n2))
if s.count('<div') - s.count('</div') != orig.count('<div') - orig.count('</div'): sys.exit('page: div balance')
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok: json, key, page;', r_n, 'written,', mc_n, 'multiple choice')
