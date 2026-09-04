# -*- coding: utf-8 -*-
"""Pass 3b: build RWM sections into Carry On, Mr. Bowditch weeks 9-14 (Days 2 and 3).
Uses the .rwm-block design already present in these files' CSS.
Every mentor sentence verified verbatim against OCR of the chapter PDFs in
planning docs/carry on mr bowditch novel (see tools/bowditch_rwm_picks.md)."""
import re, os, shutil

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSS_ADD = ".rwm-step-text{font-size:15px;color:#1A2A4A;line-height:1.7;}\n"

def step(label, text, prompt, jid, jlabel, placeholder, frame=None):
    lab = 'Your sentence' if jid.endswith('mimic') else 'Your response'
    out  = '      <div class="rwm-step">\n'
    out += '        <div class="rwm-step-label">%s</div>\n' % label
    out += '        <div class="rwm-step-text">%s</div>\n' % text
    if frame:
        out += '        <div class="rwm-frame">%s</div>\n' % frame
    out += '        <div class="textbox-prompt">%s</div>\n' % prompt
    out += '        <div class="journal-label">\U0001F4D3 %s <span class="saved-dot" id="dot-%s"></span></div>\n' % (lab, jid)
    out += ('        <textarea class="journal-box" id="journal-%s" data-label="%s" placeholder="%s" '
            'oninput="autoSave(this,\'dot-%s\');gatherAnswers();"></textarea>\n') % (jid, jlabel, placeholder, jid)
    out += '      </div>\n'
    return out

L_R = '&#x1F4D6; Read like a Reader'
L_W = '&#x270F;&#xFE0F; Read like a Writer'
L_M = '&#x1F58A;&#xFE0F; Mimic'

def block(sentence, reader, rp, writer, wp, mimic, mp, frame=None):
    out  = '  <!-- ═══ RWM ═══ -->\n'
    out += '  <div class="rwm-block">\n'
    out += '    <div class="rwm-label">RWM &mdash; Read like a Reader, Read like a Writer, Mimic</div>\n'
    out += '    <div class="rwm-sentence">&ldquo;%s&rdquo;</div>\n' % sentence
    out += step(L_R, reader, rp, 'rwm-reader', 'RWM — Read like a Reader', 'This sentence shows...')
    out += step(L_W, writer, wp, 'rwm-writer', 'RWM — Read like a Writer', 'Latham built it by...')
    out += step(L_M, mimic,  mp, 'rwm-mimic',  'RWM — Mimic', 'Write your sentence here...', frame)
    out += '  </div>\n\n'
    return out

RWM = {
 # ---- built week 9 (scope 11): chronological organization in expository writing; grammar appositives
 'lesson-9-2-cmb-ch2.html': block(
   "The first sunny day, when Nat came down to breakfast, he still had not thought of anything to do about his good-luck spell.",
   "Nat has been turning over a good-luck spell for days. This sentence catches him at breakfast still without an idea. What does it tell you about how much time has passed &mdash; and about how long this has been sitting on his mind?",
   "Write 1&ndash;2 sentences explaining what this moment shows about Nat.",
   "Look at the order Latham puts things in. She fixes the time first &mdash; <em>The first sunny day</em> &mdash; then narrows to one moment inside it, <em>when Nat came down to breakfast</em>, and only then tells you how things stand. That is chronological organization working inside a single sentence: the reader is placed in time before being handed the news.",
   "Write 1 sentence explaining why Latham puts the time before the news.",
   "Write one sentence about a moment in Chapter 2 that fixes the time first, then narrows to a single moment, and only then tells the reader what happened.",
   "Write your own sentence using the same technique.",
   frame="The first ___, when [character] ___, he still had not ___."),

 'lesson-9-3-cmb-ch3.html': block(
   "When anyone asked about April 19, 1775, the Battle of Lexington would be the right answer &mdash; no matter what else happened on that day.",
   "April 19, 1775 is also the day something happened in Nat&rsquo;s own family. Latham is pointing out that one date can belong to history and to a single household at the same time. Which answer does the world keep, and which one does Nat keep?",
   "Write 1&ndash;2 sentences explaining what this says about whose story a date belongs to.",
   "This sentence is about how chronology gets organised, and it argues with itself. The main clause gives the official answer. Then the dash adds <em>no matter what else happened on that day</em>, which quietly admits the official answer leaves things out. When you organise writing by date, you are choosing what the date is for.",
   "Write 1 sentence explaining what the part after the dash does to the first half.",
   "Write one sentence that names a date and the event history remembers it for, then use a dash to add what that official answer leaves out. No frame this time &mdash; you have the shape.",
   "Write your own sentence using the same technique."),

 # ---- built week 10 (scope 12): using sequence transitions accurately; grammar verb tense in historical writing
 'lesson-10-2-cmb-ch6.html': block(
   "After they had eaten, Nat spread his work on the table.",
   "Nat has almost no time that belongs to him. Supper ends and the books come out. What does it tell you about him that this is what he does with the end of a day?",
   "Write 1&ndash;2 sentences explaining what this small action shows about Nat.",
   "Two things are working here. <em>After</em> is a sequence transition &mdash; it puts the two actions in order without spending a word explaining. And look at the verbs: <em>had eaten</em> happened first, so it takes the past perfect; <em>spread</em> came second, so it takes the simple past. The tense is what makes the order true. Put both verbs in the same tense and the sequence collapses.",
   "Write 1 sentence explaining how the two different verb tenses show the order of events.",
   "Write one sentence about Chapter 6 that puts two events in order. Open with <em>After</em>, use the past perfect for whatever happened first, and the simple past for what followed.",
   "Write your own sentence using the same technique.",
   frame="After [someone] had ___, [character] ___."),

 'lesson-10-3-cmb-ch7.html': block(
   "But after supper Nat went back to the chandlery to finish the work he had not done.",
   "This is Nat&rsquo;s day after his day is over. He has been teaching himself navigation, surveying and astronomy &mdash; and the bookkeeping is still waiting for him. What is this sentence telling you about the cost of what he is doing?",
   "Write 1&ndash;2 sentences explaining what this shows about the price of Nat&rsquo;s studying.",
   "The sequence is carried by three small moves. <em>But</em> turns against the sentence before it. <em>after supper</em> places the action in the order of the day. And <em>had not done</em> reaches back to work left undone earlier. One short sentence holds three different points in time, and the verb tenses are what keep them straight.",
   "Write 1 sentence naming the three points in time this sentence holds at once.",
   "Write one sentence about Chapter 7 that holds two points in time &mdash; something happening now, and something left undone earlier. Use a sequence word and the past perfect. No frame this time.",
   "Write your own sentence using the same technique."),

 # ---- built week 11 (scope 13): central idea with supporting details; grammar relative pronouns and clauses
 'lesson-11-2-cmb-ch10.html': block(
   "Captain George Crowninshield had built a lookout there for him on a high point &mdash; a solid granite base, with steps leading up to a seat.",
   "Someone built this so that a man could sit and watch for ships coming home. What does the trouble taken &mdash; granite, steps, a seat &mdash; tell you about how much that waiting mattered?",
   "Write 1&ndash;2 sentences explaining what the lookout shows about the people who built it.",
   "The sentence states its idea and then proves it. The main clause is the central idea: a lookout was built on a high point. Everything after the dash is supporting detail, and notice how exact it is &mdash; not &ldquo;a good lookout&rdquo; but <em>a solid granite base, with steps leading up to a seat</em>. Details support an idea by being precise, not by being numerous.",
   "Write 1 sentence explaining how the details after the dash support the main idea.",
   "Write one sentence about something in Chapter 10. State the central idea in the main clause, then add two exact supporting details. Choose specifics, not adjectives.",
   "Write your own sentence using the same technique.",
   frame="[Someone] had built ___ &mdash; ___, with ___."),

 'lesson-11-3-cmb-ch11.html': block(
   "If we argue against any branch of liberty, just because sometimes people abuse that liberty, then we argue against liberty itself.",
   "Dr. Bentley is defending a newspaper that printed something he disagrees with. What is he saying about what happens when you start making exceptions to a freedom?",
   "Write 1&ndash;2 sentences explaining Bentley&rsquo;s argument in your own words.",
   "This is a central idea built as a piece of reasoning: <em>If</em> &hellip; <em>just because</em> &hellip; <em>then</em>. The middle clause is the objection somebody might raise, and Bentley puts it inside his own sentence instead of ignoring it. A central idea is stronger when it answers the obvious complaint on its way past.",
   "Write 1 sentence explaining why Bentley puts the objection inside his own sentence.",
   "Write one <em>If &hellip; just because &hellip; then &hellip;</em> sentence stating something you believe about fairness or freedom. Put the strongest objection inside your own sentence. No frame this time.",
   "Write your own sentence using the same technique."),

 # ---- built week 12 (scope 14): defining terms inside an explanatory paragraph; grammar commas with introductory phrases
 'lesson-12-2-cmb-ch14.html': block(
   "He knew Lem Harvey &mdash; a huge fellow with hulking shoulders and a sullen, swarthy face.",
   "The name Lem Harvey means nothing to a reader and everything to Nat. What does Latham get to skip by telling you who he is right here, before he has done anything?",
   "Write 1&ndash;2 sentences explaining what this tells you about Lem before he acts.",
   "Latham defines a name the moment she uses it. The dash opens a definition and the rest of the sentence fills it in, so the reader never has to stop and wonder. This is the move explanatory writing needs: when a term arrives, define it inside the same sentence rather than in a separate one afterwards.",
   "Write 1 sentence explaining why defining the name inside the same sentence works better than starting a new one.",
   "Write one sentence that names a person, a ship or a tool from Chapter 14 and defines it in the same sentence with a dash. Keep the definition to concrete details.",
   "Write your own sentence using the same technique.",
   frame="[Name] &mdash; ___ with ___ and ___."),

 'lesson-12-3-cmb-ch15.html': block(
   "Celestial navigation &mdash; or sailing by the sky &mdash; is what we&rsquo;ll talk about first.",
   "Nat is about to teach the crew something the experts said ordinary sailors could never learn. Why would he translate the term before he begins?",
   "Write 1&ndash;2 sentences explaining why Nat defines the term first.",
   "This is the cleanest version of the move: the technical term, then <em>or</em>, then the plain-English translation, and then the sentence carries on. The definition sits inside a pair of dashes, so it interrupts nothing. <em>Celestial navigation</em> keeps the precision; <em>sailing by the sky</em> makes it usable. Good explanatory writing keeps both.",
   "Write 1 sentence explaining what the plain-English version adds that the technical term alone could not.",
   "Write one sentence that uses a real navigation term from Chapter 15 and defines it inside a pair of dashes with <em>or</em>. Keep the precise term and add the plain one. No frame this time.",
   "Write your own sentence using the same technique."),

 # ---- built week 13 (scope 15): explaining why details were included; grammar compound/complex sentences
 'lesson-13-2-cmb-ch18.html': block(
   "Little Charlie Waldo, the new cabin boy, listened big-eyed while Prince explained the danger of French spies.",
   "Charlie is the smallest and newest person aboard, and he is listening to a warning about spies. Why does Latham put him in this scene at all?",
   "Write 1&ndash;2 sentences explaining what Charlie&rsquo;s presence adds to the scene.",
   "Every detail here is doing a job. <em>the new cabin boy</em> tells you why he does not already know this. <em>big-eyed</em> tells you how serious the warning sounds to someone hearing it for the first time. And <em>while</em> ties his listening to Prince&rsquo;s explaining, so the two happen at once. Ask it of any detail you write: what would the reader lose without this?",
   "Write 1 sentence explaining what the words <em>the new cabin boy</em> do for the reader.",
   "Write one sentence about Chapter 18 with a person in it, one detail that explains why they matter here, and a <em>while</em> clause putting two actions at the same time. Be ready to say why each detail earns its place.",
   "Write your own sentence using the same technique.",
   frame="[Name], the ___, ___ while [someone] ___."),

 'lesson-13-3-cmb-ch19.html': block(
   "She knew that friends and neighbors &mdash; even old friends and good neighbors &mdash; couldn&rsquo;t fill the emptiness in his heart.",
   "Nat has lost someone. The people around him are kind, and it is not enough. What is this sentence saying about the limits of kindness?",
   "Write 1&ndash;2 sentences explaining what this shows about Nat&rsquo;s grief.",
   "The sentence would still work without its middle. Read it without <em>even old friends and good neighbors</em> and it makes sense, but it stops arguing. That interruption is there to close a door &mdash; it answers the reader who was about to think <em>surely his old friends could help</em>. A detail is often included to head off the objection you were just about to raise.",
   "Write 1 sentence explaining what a reader might think if the middle part were removed.",
   "Write one sentence about Chapter 19 with an interrupting detail between dashes that answers an objection your reader might raise. Test it: read your sentence without the middle and see what it loses. No frame this time.",
   "Write your own sentence using the same technique."),

 # ---- built week 14 (scope 16): conclusion connects central idea to significance; grammar editing
 'lesson-14-2-cmb-ch22.html': block(
   "The man who got a degree from Harvard without ever setting foot in a classroom!",
   "This is how a stranger introduces Nat to his son. Nine years of an indenture, of borrowed books and candlelight, arrive here as a single sentence. What does it mean that this is the version other people tell?",
   "Write 1&ndash;2 sentences explaining what this says about what Nat&rsquo;s life came to mean.",
   "A conclusion has to say why the story mattered, and this one does it inside a single relative clause. <em>who got a degree from Harvard</em> is the achievement; <em>without ever setting foot in a classroom</em> is the significance &mdash; it tells you what kind of achievement it was, and quietly what it cost. The contrast is the whole point, and it is built into the shape of the sentence.",
   "Write 1 sentence explaining how the second half changes the meaning of the first.",
   "Write one sentence that could conclude a piece of writing about Nat. Name what he achieved, then add the contrast that shows what it signifies. One sentence, and no explaining afterwards.",
   "Write your own sentence using the same technique.",
   frame="The ___ who ___ without ever ___."),

 'lesson-14-3-cmb-ch23.html': block(
   "He knew now why Prince always seemed to shed about ten years when they made their landfall.",
   "Nat has watched Captain Prince do this for years without understanding it. Now Nat is the one bringing a ship home. What has changed &mdash; in Prince, or in Nat?",
   "Write 1&ndash;2 sentences explaining what Nat finally understands, and why he understands it now.",
   "The whole sentence turns on two words: <em>knew now</em>. Latham never explains the insight. She reports the moment of getting it and lets you supply the meaning out of everything you have already read. That is how a conclusion earns its significance &mdash; it points back at the book instead of summarising it.",
   "Write 1 sentence explaining why the word <em>now</em> matters so much here.",
   "Write one <em>He knew now why &hellip;</em> sentence about something Nat finally understands by the end of the book. Do not explain the insight &mdash; let the sentence point back at what your reader already knows. No frame this time.",
   "Write your own sentence using the same technique."),
}

GATHER = ("o+='\\nRWM \\u2014 READ, WRITE, MIMIC\\n'+'\\u2500'.repeat(36)+'\\n';"
          "['journal-rwm-reader','journal-rwm-writer','journal-rwm-mimic'].forEach(function(id){"
          "var el=document.getElementById(id);if(!el)return;"
          "o+='\\n'+el.getAttribute('data-label')+'\\n'+(el.value.trim()||'(no answer)')+'\\n';});")

def patch(fn):
    p = os.path.join(D, fn)
    s = open(p, encoding='utf-8').read()
    orig = s
    notes = []

    if '<div class="rwm-block">' in s:
        print('%-26s ALREADY HAS RWM - skipped' % fn); return

    # 1. add the one missing CSS rule
    if '.rwm-step-text' not in s:
        anchor = '.rwm-frame{'
        i = s.find(anchor)
        s = s[:i] + CSS_ADD + s[i:]
        notes.append('css')

    # 2. insert the block at the end of the Word Study tab
    wrap = -1
    for pat in (r'<div class="tab-next-wrap">', r'<div class="tab-bridge">'):
        for m in re.finditer(pat, s):
            if "switchTab('reading')" in s[m.start():m.start() + 900]:
                wrap = m.start(); break
        if wrap > 0:
            break
    if wrap < 0:
        raise SystemExit('%s: no Word Study exit block' % fn)
    s = s[:wrap] + RWM[fn] + '  ' + s[wrap:]
    notes.append('rwm')

    # 3. gatherAnswers collection
    if 'journal-rwm-reader' not in s[s.find('function gatherAnswers'):s.find('function gatherAnswers') + 3000]:
        anchor = "o+='\\nWRITING CONNECTION\\n'"
        i = s.find(anchor)
        if i > 0:
            s = s[:i] + GATHER + s[i:]
            notes.append('gather')
        else:
            notes.append('!!NO-GATHER-ANCHOR')

    # 4. turn-in checklist item
    if 'three RWM responses' not in s:
        mt = re.search(r'( *)<div class="turn-in-item"', s)
        if mt:
            item = ('%s<div class="turn-in-item" onclick="toggleCheck(this)">\n'
                    '%s  <div class="turn-in-check"></div>\n'
                    '%s  <div class="turn-in-item-text">I wrote my three RWM responses (Reader, Writer, Mimic) in Word Study.</div>\n'
                    '%s</div>\n') % (mt.group(1), mt.group(1), mt.group(1), mt.group(1))
            s = s[:mt.start()] + item + s[mt.start():]
            notes.append('turnin')

    shutil.copy2(p, p + '.bak')
    open(p, 'w', encoding='utf-8').write(s)
    print('%-26s %s' % (fn, ', '.join(notes)))

for fn in sorted(RWM, key=lambda f: (int(re.match(r'lesson-(\d+)', f).group(1)), f)):
    patch(fn)
