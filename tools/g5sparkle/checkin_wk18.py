#!/usr/bin/env python3
"""Week 18 check-in as a Canvas quiz: JSON source of truth + readable key (QTI built from the JSON after approval).
Audited against the four lessons AND the scope (v2_poetry, scope week 17). Book lines verified in planning docs/hbg_ocr.txt."""
import json, io, html, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
Q = {
 "id": "g5-ela-wk18-checkin",
 "title": "Week 18 Check-In · How I Became a Ghost",
 "description": "This week you started How I Became a Ghost and met Isaac, a ten-year-old Choctaw boy who tells his story from after it happened. You practiced appositives and precise nouns, the roots mem/memor and script, and open and closed syllables. Show what you know.",
 "chapters": "Ch. 1–7",
 "questions": [
  {"n":1,"section":"Grammar","type":"multiple_choice_question","points":1,"text":"Which sentence contains an appositive?",
   "options":["Isaac looked up at the sun and waited.","Jumper, Isaac’s dog, followed him everywhere in the woods.","Luke left quickly to play stickball before supper.","The old men sat by the river."],"answer":1,
   "from":"18.1–18.2 Grammar (find the appositive)","status":"kept (a fourth option added)"},
  {"n":2,"section":"Grammar","type":"multiple_choice_question","points":1,"text":"Which sentence sets off the appositive correctly?",
   "options":["Mister Jonah a respected elder, sat with his back against the old tree.","Mister Jonah, a respected elder, sat with his back against the old tree.","Mister Jonah, a respected elder sat with his back against the old tree.","Mister Jonah a respected elder sat, with his back against the old tree."],"answer":1,
   "from":"18.1–18.4 Grammar (commas on both sides)","status":"changed: same sentence, now multiple choice (was a written fix)"},
  {"n":3,"section":"Grammar","type":"multiple_choice_question","points":1,"text":"Which sentence uses the most precise nouns?",
   "options":["A man came home with his weapon.","Isaac’s father came home with his shotgun.","Someone came back with a thing.","The person came home with his stuff."],"answer":1,
   "from":"18.1–18.4 Grammar (precise nouns, scope week 17)","status":"new (old Q3 asked for another appositive; precise nouns are in the scope and now taught)"},
  {"n":4,"section":"Morphology & Vocabulary","type":"multiple_choice_question","points":1,"text":"Which root is in the word commemorate?",
   "options":["script (write)","mem / memor (memory)","port (carry)","spect (look)"],"answer":1,
   "from":"18.2–18.4 Morphology","status":"kept (a fourth option added)"},
  {"n":5,"section":"Morphology & Vocabulary","type":"multiple_choice_question","points":1,"text":"Read this sentence from Chapter 4: “The missionaries were visiting another Choctaw town that week, but the Nahullos didn’t know that.” Who are missionaries?",
   "options":["People sent to a place to teach their religion","Soldiers sent to guard a town","The oldest men in a Choctaw town","Men who ride horses at night"],"answer":0,
   "from":"18.1–18.4 Vocabulary (missionaries)","status":"new (old Q5 tested “prophecy,” a word the week never taught, in a sentence that is not from the book)"},
  {"n":6,"section":"Morphology & Vocabulary","type":"essay_question","points":1,"text":"Use the word smothering in a sentence that shows you know what it means.",
   "from":"18.4 Vocabulary (Use the Word)","status":"new (old Q6 used “removal,” not one of the week’s words)"},
  {"n":7,"section":"Spelling","type":"multiple_answers_question","points":1,"text":"Which words begin with an open syllable? Choose all that are right.",
   "options":["nation","Choctaw","cedar","blanket"],"answers":[0,2],
   "from":"18.1–18.2 Spelling sorts","status":"new (old Q7 sorted by number of syllables; the week teaches open and closed)"},
  {"n":8,"section":"Spelling","type":"multiple_choice_question","points":1,"text":"Where does the first beat of government end?",
   "options":["go | vernment","gov | ernment","gover | nment","g | overnment"],"answer":1,
   "from":"18.3 Spelling (split a long word)","status":"new (old Q8 spelled “removal” from a definition)"},
  {"n":9,"section":"Spelling","type":"multiple_choice_question","points":1,"text":"The first syllable of frozen is —",
   "options":["open, because fro ends on the vowel o and the o says its name","closed, because fro ends on a consonant","closed, because the o is short","open, because frozen has two syllables"],"answer":0,
   "from":"18.3 Spelling (frozen)","status":"new (old Q9 split Mississippi, not taught this week)"},
  {"n":10,"section":"Reading","type":"essay_question","points":1,"text":"When Isaac says “Their homes are in town,” what does he think his mother means by “home”? What does his mother actually mean?",
   "from":"18.1 Reading (Ch. 2) and 18.2 (Ch. 3)","status":"kept"},
  {"n":11,"section":"Reading","type":"essay_question","points":2,"text":"In Chapters 2 and 3, Isaac watches three different ways the old people say good-bye by the river. What do all three have in common? What do they tell you about how the Choctaw people feel about leaving their home? Use at least two details from the book.",
   "from":"18.1–18.2 Reading (Ch. 2–3)","status":"kept (“ceremonies” now said plainly)"},
  {"n":12,"section":"Writing","type":"essay_question","points":1,"text":"Isaac steps back into a memory: “When I was only six, I went fishing by myself with my new cane fishing pole.” Write one sentence with I that steps back into a memory of your own and shows how you feel about it.",
   "from":"18.2 Read Like a Writer (first-person narration that reveals memory)","status":"new (old Q12 used a sentence pattern this week’s RWM no longer teaches)"},
  {"n":13,"section":"Writing","type":"essay_question","points":1,"text":"In 2–3 sentences, explain why Tim Tingle begins this story with Isaac already knowing he will become a ghost. What does that do for the reader?",
   "from":"18.1 Big Question; 18.4 Reading","status":"kept"}
 ],
 "passage": {"before": 10, "title": "Reading passage (Chapter 2)",
   "text": "“These men are saying good-bye to their home.”\n“They live in town. Their homes are in town.”\nMy mother gripped my hand tight. “Come on,” she said. “There is more to see.”",
   "cite": "Tim Tingle, How I Became a Ghost, Chapter 2"}
}
io.open(os.path.join(ROOT, 'assessments/g5-ela-wk18-checkin.json'), 'w', encoding='utf-8').write(json.dumps(Q, ensure_ascii=False, indent=1))
e = html.escape
rows = ''
for q in Q['questions']:
    if q['n'] == Q['passage']['before']:
        rows += '<div class="psg"><b>%s</b><p>%s</p><p class="m">%s</p></div>' % (e(Q['passage']['title']), e(Q['passage']['text']).replace('\n', '<br>'), e(Q['passage']['cite']))
    opts = ''
    if 'options' in q:
        right = q.get('answers', [q.get('answer')])
        opts = '<ol type="A">' + ''.join('<li%s>%s%s</li>' % (' class="ok"' if i in right else '', e(o), ' ✓' if i in right else '') for i, o in enumerate(q['options'])) + '</ol>'
    kind = {'multiple_choice_question': 'Multiple choice (auto-graded)', 'multiple_answers_question': 'Choose all (auto-graded)'}.get(q['type'], 'Written (teacher-graded)')
    rows += ('<div class="q %s"><div class="h"><span class="n">%d</span> %s · %s · %d pt</div><p>%s</p>%s<div class="m">Taught in: %s<br>Audit: %s</div></div>'
             % ('new' if q['status'].startswith(('new', 'changed')) else '', q['n'], e(q['section']), kind, q['points'], e(q['text']), opts, e(q['from']), e(q['status'])))
page = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>G5 Week 18 Check-In Key</title>
<style>body{font:16px/1.5 system-ui,sans-serif;max-width:820px;margin:0 auto;padding:16px;background:#F0F2F8;color:#24324F}
h1{font-size:22px;color:#0E1C42}.q,.psg{background:#fff;border:1px solid #D9E0F0;border-radius:10px;padding:12px 16px;margin:12px 0}
.q.new{border-left:5px solid #2B5BA8}.psg{background:#FFF8E6}.h{font-weight:700;color:#0E1C42}.n{display:inline-block;background:#0E1C42;color:#fff;border-radius:50%%;width:26px;height:26px;text-align:center;line-height:26px;margin-right:6px}
.ok{color:#24502A;font-weight:700}.m{font-size:13px;color:#6B7690;margin-top:6px}</style></head><body>
<h1>%s</h1><p>%s</p><p><b>%s · %d questions · %d points.</b> Blue edge = new or changed (the old item tested something week 18 doesn’t teach, or a sentence that isn’t in the book).</p>%s</body></html>''' % (
    e(Q['title']), e(Q['description']), e(Q['chapters']), len(Q['questions']), sum(q['points'] for q in Q['questions']), rows)
io.open(os.path.join(ROOT, 'assessments/g5-ela-wk18-checkin-key.html'), 'w', encoding='utf-8').write(page)
print('ok', sum(q['points'] for q in Q['questions']), 'points')
