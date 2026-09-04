# -*- coding: utf-8 -*-
"""Pass 4b: re-key WGRD in How I Became a Ghost weeks 18-24 to the v2_poetry S&S.
built 18=scope 17, 19=18, 20=19, 21=20, 22=21, 23=22 (+23 on 23.4), 24=24.
Adds the missing "How to Do It" box to all 28 and a whole-book callout to each Day 4.
Chapter titles and events grounded in planning docs/hbg_ocr.txt (all 29 chapters)."""
import re, os, shutil

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

KC = ('<div class="key-concept" style="background:#F0F7FF;border-color:#C8DCEE;margin:10px 0;">\n'
      '<div class="key-concept-label" style="color:#3D5285;">\U0001F50D How to Do It</div>\n'
      '<ol style="margin:6px 0 6px 20px;font-size:14px;color:#3A4A6B;line-height:1.8;">\n%s'
      '</ol>\n</div>\n')
def kc(*steps):
    return KC % ''.join('<li><strong>%s:</strong> %s</li>\n' % s for s in steps)

BOX = {
18: kc(("Learn the context first","Note what the book tells you about Choctaw life in 1830 &mdash; the treaty, the land, the families &mdash; before you judge anyone&rsquo;s choices."),
       ("Listen to who is telling it","Isaac is a ten-year-old boy speaking straight to you. Ask what he knows, what he does not, and what he warns you about before it happens."),
       ("Separate the voice from the events","Ask what changes because Isaac is the one telling it. The same events in a history book would sound nothing like this.")),
19: kc(("Watch what a character does","Not what they say about themselves. Actions under pressure are where a perspective shows."),
       ("Ask what they have lost","In this book, what a person is still willing to carry tells you how they see the world."),
       ("Compare two people in one moment","Give the same event to two characters, and their different perspectives become visible.")),
20: kc(("Name the conflict precisely","Say who wants what, and what stands in the way. &ldquo;Bad things happen&rdquo; is not a conflict."),
       ("Put the events in order","List what happens in sequence, and mark the moment the danger changes shape."),
       ("Watch the pressure rise","Ask what each event makes harder for the next. Rising action is events narrowing a character&rsquo;s choices.")),
21: kc(("Find what comes back","Note the images, objects and phrases that appear more than once &mdash; blankets, footprints, bones, a panther."),
       ("Ask what changes each time","A repeated image is not a symbol until it means more on its later appearance than on its first."),
       ("State the theme as a sentence","Say what the book argues, in a full sentence about people. &ldquo;Family&rdquo; is a topic; a theme is a claim.")),
22: kc(("Find the comparison","Look for similes, metaphors and images where one thing is described as another."),
       ("Ask what it does","A comparison should change what you feel or understand. If it only decorates, it is not doing its job."),
       ("Notice what is left unsaid","Symbolism works by not explaining itself. Ask what Tingle trusts you to work out.")),
23: kc(("Keep the spine, drop the rest","A summary is the events the story would break without &mdash; not everything that happened."),
       ("Say what it was about","A plot summary tells what happened. Add one sentence saying what it meant."),
       ("Check it against the text","Reread and ask whether your summary would mislead someone who has not read the chapter.")),
24: kc(("Name the source type","Fiction, informational text, primary source, secondary source. Each was written by someone, for someone, for a reason."),
       ("Compare what each one can do","A novel gives you what it felt like; a primary source gives you what was recorded. Neither replaces the other."),
       ("Build the comparison on evidence","Make a claim about the two texts, quote from each, and explain why the difference matters.")),
}
SYNTH = kc(("Trace the plot","Lay Isaac&rsquo;s story end to end, from the Choctaw Nation in 1830 to the wagon of the bonepickers."),
           ("Name the conflicts","Which clashes changed him &mdash; with the soldiers, with the road, with what he could no longer be?"),
           ("Describe the perspective","Say what being a ghost let Isaac see that a living boy could not, and what it cost him."),
           ("State the theme","Put the three together in one sentence. The theme is what the plot, the conflicts and the perspective add up to."))

WB = ('<div class="callout callout-info" style="margin-top:10px;"><span class="callout-icon">\U0001F3AF</span>'
      '<p><strong>Whole-book thinking:</strong> %s</p></div>\n')

# fn -> (sub, paragraph, box, whole-book or None)
W = {}
def add(fn, sub, para, wk, wb=None, box=None):
    W[fn] = (sub, para, box if box else BOX[wk], wb)

# ---- week 18 (scope 17): historical context + first-person narrative voice
add('lesson-18-1-hbg-ch4.html','Set your reading lens',
 "Good readers of historical fiction do two things at once: they <strong>build the historical context</strong> and they "
 "<strong>listen to the narrator&rsquo;s voice</strong>. Isaac opens by telling you he is a ghost, then takes you back to "
 "the Choctaw Nation in Mississippi in 1830, before the removal. As you read Chapters 1 and 2, notice both the world he "
 "describes and the way he chooses to describe it.",18)
add('lesson-18-2-hbg-ch5.html','Read closely for Isaac&rsquo;s voice',
 "Read closely today and gather evidence. Chapters 3 and 4 are &ldquo;Dancing on the Stones&rdquo; and &ldquo;Fire in the "
 "Hair,&rdquo; and Isaac tells both as a boy who already knows how his story ends. Watch what he says plainly, what he "
 "refuses to explain, and what he warns you about before it happens.",18)
add('lesson-18-3-hbg-ch6.html','Reread — the voice and the history together',
 "Today reread a passage from Chapters 5 or 6 and look at it twice: once for what happened, once for who is telling you. "
 "&ldquo;Men with Blankets&rdquo; sounds almost ordinary until you know what those blankets carried. Ask what the "
 "historical context supplies that Isaac never spells out.",18)
add('lesson-18-4-hbg-ch7.html','Synthesize the week — a boy&rsquo;s voice inside a history',
 "Now put the week together. Chapter 7 is called &ldquo;Snow Monsters,&rdquo; and it is funny &mdash; in the middle of a "
 "forced removal. Ask why Tim Tingle would place it here, and what it tells you about Isaac&rsquo;s family. Then say what "
 "a first-person narrator gives a reader that a history of the same events could not.",18,
 "Across Chapters 1&ndash;7, find the moment where Isaac&rsquo;s voice tells you something a history book could not have "
 "recorded. Then say what the history gives you that Isaac, being ten years old, cannot.")

# ---- week 19 (scope 18): characterization develops perspective
add('lesson-19-1-hbg-ch8.html','Set your reading lens',
 "Good readers notice how <strong>characterization builds a perspective</strong>. A character is not a list of traits "
 "&mdash; they are a way of seeing, assembled out of what they have lived through. Chapter 8 puts the Choctaw people on "
 "the road as the &ldquo;Walking People.&rdquo; As you read, watch what each person carries, and what that says about how "
 "they see what is happening to them.",19)
add('lesson-19-2-hbg-ch9.html','Read closely for perspective',
 "Read closely and gather evidence. Nita is five years old, and she can see the ghost walkers. Watch how the adults "
 "respond to her and how she responds to them. Perspective shows most clearly when two people look at the same thing and "
 "only one of them can see it.",19)
add('lesson-19-3-hbg-ch10.html','Reread — a whole outlook in one line',
 "Today reread the passage in Chapter 10 where Isaac&rsquo;s father tells him he cannot keep his eyes on the bloody "
 "footprints behind him. Reread it and ask what kind of person says that, in that moment, to his son. One line of advice "
 "can carry an entire way of seeing the world.",19)
add('lesson-19-4-hbg-ch11.html','Synthesize the week — two people, one road',
 "Now put the week together. Across Chapters 8&ndash;11 you have watched several people meet the same removal in "
 "different ways. Choose two of them and say how their characterization &mdash; what they do, what they carry, what they "
 "refuse &mdash; produces two different perspectives on the same road.",19,
 "Pick the character whose perspective is furthest from Isaac&rsquo;s. Name what in their life produced it, and find the "
 "passage where the gap between the two of them is clearest.")

# ---- week 20 (scope 19): conflict, events, rising action
add('lesson-20-1-hbg-ch12.html','Set your reading lens',
 "Good readers can <strong>track conflict and rising action</strong>. A story&rsquo;s pressure does not come from bad "
 "things happening &mdash; it comes from each event making the next one harder. Chapter 12 is called &ldquo;Disappearing "
 "Daughter.&rdquo; As you read, name the conflict exactly, and watch what it takes away.",20)
add('lesson-20-2-hbg-ch13.html','Read closely for rising action',
 "Read closely and gather evidence. In Chapter 13 Isaac finally tells his family what he has known since Chapter 1 "
 "&mdash; that he will soon be a ghost. Notice that saying it aloud does not release the tension; it raises it. Track "
 "what changes for his family the moment they know.",20)
add('lesson-20-3-hbg-ch14.html','Reread — the order events happen in',
 "Today reread part of Joseph&rsquo;s story in Chapter 14. Put its events in order, then ask which one made the next one "
 "possible. Joseph tells what the soldiers did in a flat, quiet voice, and the sequence does the work his tone is "
 "refusing to do.",20)
add('lesson-20-4-hbg-ch15.html','Synthesize the week — where the danger changed',
 "Now put the week together. Lay the events of Chapters 12&ndash;15 end to end and, for each one, ask what it made "
 "harder. Then find the point where the danger stopped being the road itself and became the people driving them along "
 "it.",20,
 "Across the book so far, name the single event that narrowed Isaac&rsquo;s choices the most. Defend your answer with "
 "what came before it and what became impossible after.")

# ---- week 21 (scope 20): theme through repeated images and ideas
add('lesson-21-1-hbg-ch16.html','Set your reading lens',
 "Good readers watch a <strong>theme develop through repetition</strong>. Tim Tingle builds meaning by bringing the same "
 "images back &mdash; blankets, footprints, bones, a panther &mdash; each time carrying a little more than before. "
 "Chapter 16 sends Isaac and Joseph after Naomi. As you read, start a list of what you have seen already.",21)
add('lesson-21-2-hbg-ch17.html','Read closely for what returns',
 "Read closely and gather evidence. Chapter 17 is Isaac&rsquo;s goodbye to his family. Notice how much of it is built "
 "from things you have already met in this book, used again in a new situation. That is how a theme accumulates &mdash; "
 "not by being explained, but by returning.",21)
add('lesson-21-3-hbg-ch18.html','Reread — trace one idea backwards',
 "Today reread a passage from Chapter 18 and trace one repeated idea back through the book. This is the chapter the whole "
 "novel has been moving toward. Ask what an image you first met in Chapter 6 or Chapter 10 means here, and whether it has "
 "changed on the way.",21)
add('lesson-21-4-hbg-ch19.html','Synthesize the week — name the theme',
 "Now put the week together. Choose one image that has repeated across Chapters 16&ndash;19 and earlier, and state in one "
 "full sentence what this book argues through it. Then name the two places you would point to as evidence.",21,
 "State the theme of this novel as one sentence about people, not a single word. Then find the earliest place the book "
 "began building it, and the place where it became unmistakable.")

# ---- week 22 (scope 21): figurative language, symbolism, author choices
add('lesson-22-1-hbg-ch20.html','Set your reading lens',
 "Good readers analyse <strong>figurative language and an author&rsquo;s choices</strong>. Tim Tingle rarely explains a "
 "feeling. He hands you an image and lets it do the work. Chapter 20 is called &ldquo;Naomi the Strong.&rdquo; As you "
 "read, mark every place where something is described as being like something else.",22)
add('lesson-22-2-hbg-ch21.html','Read closely for the images',
 "Read closely and gather evidence. The panther in Chapter 21 is both a real animal and something more, and Tingle never "
 "once stops to tell you which. Collect the images in this chapter and ask what each is doing besides describing.",22)
add('lesson-22-3-hbg-ch22.html','Reread — how the sentence is built',
 "Today reread the moment in Chapter 22 when Naomi works out where she is. Reread it for how the sentence is built rather "
 "than what it reports: Tingle spends the middle of it on a comparison and saves the fact for the very end.",22)
add('lesson-22-4-hbg-ch23.html','Synthesize the week — the image carrying the most',
 "Now put the week together. Across Chapters 20&ndash;23, choose the one image you think carries the most weight and "
 "explain what it means without using the word <em>symbol</em>. Then say what Tingle gained by never explaining it "
 "himself.",22,
 "Choose the figurative image that has done the most work across the whole novel. Explain it in your own words, then find "
 "the place where a reader could first have understood it.")

# ---- week 23 (scope 22; day 4 = scope 23 synthesis)
add('lesson-23-1-hbg-ch24.html','Set your reading lens',
 "Good readers can <strong>summarise plot and theme accurately</strong> &mdash; which means choosing, not shortening. "
 "Chapter 24 is called &ldquo;A Soldier&rsquo;s Vow.&rdquo; As you read, keep asking which events this chapter would "
 "break without, and which ones you could leave out and lose nothing.",23)
add('lesson-23-2-hbg-ch25.html','Read closely, then summarise as you go',
 "Read closely and gather evidence. Chapter 25 holds a great deal of action in very few pages. Practise summarising as "
 "you read: after each turn, say in one sentence what has actually changed. A summary that lists everything is not a "
 "summary.",23)
add('lesson-23-3-hbg-ch26.html','Reread — two sentences, no more',
 "Today reread a passage from Chapter 26 and summarise it in two sentences: one for what happened, one for what it meant. "
 "Then read your summary beside the passage and ask whether it would mislead somebody who had not read it.",23)
add('lesson-23-4-hbg-ch27.html','Synthesize — character, conflict, perspective, theme',
 "Now put everything together. Today you synthesise all four threads at once. Across the whole book, say who Isaac has "
 "become, what he was up against, what being a ghost let him see, and what all of it adds up to.",23,
 "In one sentence, say what this novel is finally about. Then name the chapter you would give a reader who had time for "
 "only one, and say why that chapter carries the book.",
 box=SYNTH)

# ---- week 24 (scope 24): compare fiction with informational/primary/secondary sources
add('lesson-24-1-hbg-ch28.html','Set your reading lens',
 "Good readers can <strong>compare a novel with the sources behind it</strong>. This week you finish Isaac&rsquo;s story "
 "and then set it beside the historical record of Choctaw removal. As you read Chapter 28, begin noticing what only a "
 "novel can tell you.",24)
add('lesson-24-2-hbg-ch29.html','Read closely for what a document could not hold',
 "Read closely and gather evidence. Chapter 29 closes Isaac&rsquo;s account. Mark the passages you would want to set "
 "beside a historical document &mdash; the moments where you would ask, did it really happen this way, and how would "
 "anyone know?",24)
add('lesson-24-3-hbg-ch28-29.html','Reread — the novel and the source side by side',
 "Today you read a source next to the novel. Work with both in front of you and ask what each one is for. A primary "
 "source records what somebody wrote down at the time; a novel gives you a ten-year-old boy&rsquo;s voice, which no "
 "document preserved. Ask what each makes possible, and what each leaves out.",24)
add('lesson-24-4-hbg-ch28-29.html','Synthesize — write the comparison',
 "Now put it together and write the comparison. State a claim about how the novel and the source treat the same history, "
 "quote from both, and explain why the difference matters. This is the whole year&rsquo;s reading habits turned into one "
 "piece of source-based writing.",24,
 "Historical fiction and a primary source disagree about nothing factual here, and still tell you different things. Say "
 "what each one is for, and what a reader would miss having only one of them.")

OBJ = {
'lesson-18-1-hbg-ch4.html':"I will <em>define</em> the historical context of Choctaw removal and describe Isaac&rsquo;s first-person voice in Chapters 1&ndash;2.",
'lesson-18-2-hbg-ch5.html':"I will <em>identify</em> what Isaac&rsquo;s narration reveals, and refuses to reveal, in Chapters 3&ndash;4.",
'lesson-18-3-hbg-ch6.html':"I will <em>analyze</em> how the historical context of Chapters 5&ndash;6 supplies what Isaac never explains.",
'lesson-18-4-hbg-ch7.html':"I will <em>explain</em> what a first-person narrator gives a reader that a history of the same events could not.",
'lesson-19-1-hbg-ch8.html':"I will <em>define</em> perspective by naming what each character carries on the road in Chapter 8.",
'lesson-19-2-hbg-ch9.html':"I will <em>identify</em> how Nita&rsquo;s perspective differs from the adults&rsquo; in Chapter 9.",
'lesson-19-3-hbg-ch10.html':"I will <em>analyze</em> what one line of his father&rsquo;s advice reveals about how he sees the world.",
'lesson-19-4-hbg-ch11.html':"I will <em>explain</em> how characterization produces two different perspectives on the same removal.",
'lesson-20-1-hbg-ch12.html':"I will <em>define</em> the conflict in Chapter 12 by naming who wants what and what stands in the way.",
'lesson-20-2-hbg-ch13.html':"I will <em>identify</em> how Chapter 13 raises the tension rather than releasing it.",
'lesson-20-3-hbg-ch14.html':"I will <em>analyze</em> the order of events in Joseph&rsquo;s story and what each one made possible.",
'lesson-20-4-hbg-ch15.html':"I will <em>explain</em> how the conflict of Chapters 12&ndash;15 rises, and where the danger changed shape.",
'lesson-21-1-hbg-ch16.html':"I will <em>define</em> how a repeated image builds meaning, and begin tracking the ones this book reuses.",
'lesson-21-2-hbg-ch17.html':"I will <em>identify</em> the images in Chapter 17 that the book has used before.",
'lesson-21-3-hbg-ch18.html':"I will <em>analyze</em> one repeated idea in Chapter 18 and how its meaning has changed since it first appeared.",
'lesson-21-4-hbg-ch19.html':"I will <em>explain</em> the theme of Chapters 16&ndash;19 in one full sentence, supported by two places in the text.",
'lesson-22-1-hbg-ch20.html':"I will <em>define</em> figurative language and mark every comparison in Chapter 20.",
'lesson-22-2-hbg-ch21.html':"I will <em>identify</em> what the panther is doing in Chapter 21 besides being an animal.",
'lesson-22-3-hbg-ch22.html':"I will <em>analyze</em> how one sentence in Chapter 22 is built to deliver its meaning through a comparison.",
'lesson-22-4-hbg-ch23.html':"I will <em>explain</em> what the novel&rsquo;s strongest image means, and what the author gained by leaving it unexplained.",
'lesson-23-1-hbg-ch24.html':"I will <em>define</em> an accurate summary by deciding which events Chapter 24 would break without.",
'lesson-23-2-hbg-ch25.html':"I will <em>identify</em> what actually changes at each turn of Chapter 25 and summarise it in one sentence each.",
'lesson-23-3-hbg-ch26.html':"I will <em>analyze</em> my own two-sentence summary of Chapter 26 against the passage itself.",
'lesson-23-4-hbg-ch27.html':"I will <em>synthesize</em> character, conflict, perspective and theme across the whole novel.",
'lesson-24-1-hbg-ch28.html':"I will <em>define</em> the difference between historical fiction and a historical source.",
'lesson-24-2-hbg-ch29.html':"I will <em>identify</em> the passages in Chapter 29 I would set beside a historical document, and why.",
'lesson-24-3-hbg-ch28-29.html':"I will <em>analyze</em> what a primary source and a novel each make possible, and what each leaves out.",
'lesson-24-4-hbg-ch28-29.html':"I will <em>explain</em> a source comparison with a claim, evidence from both texts, and reasoning.",
}

NEW_NOTE = {
18:"As you read, build the historical context and listen to Isaac&rsquo;s voice &mdash; what he knows, and what he tells you before it happens.",
19:"As you read, watch what each character does and carries &mdash; that is where a perspective shows.",
20:"As you read, name the conflict precisely and track what each event makes harder for the next.",
21:"As you read, note the images that come back, and ask what each one carries the second time.",
22:"As you read, mark every comparison and ask what it does besides describe.",
23:"As you read, keep summarising: after each turn, say in one sentence what has actually changed.",
24:"As you read, notice what only a novel can tell you &mdash; and what only a historical source can.",
}
OLD_NOTES = [
 "As you read, pay close attention to the characters&#x27; actions and motivations. Think about how events connect to the bigger ideas in the story.",
]

def patch(fn):
    p = os.path.join(D, fn)
    s = open(p, encoding='utf-8').read()
    orig = s
    wk = int(re.match(r'lesson-(\d+)', fn).group(1))
    sub, para, box, wb = W[fn]
    notes = []

    m = re.search(r'<div class="activity-title">[^<]*What Good Readers Do[^<]*</div>\s*'
                  r'<div class="activity-sub">(.*?)</div>', s, re.S)
    if not m:
        print('%-30s !! no WGRD head' % fn); return
    s = s[:m.start(1)] + sub + s[m.end(1):]
    notes.append('sub')

    m = re.search(r'<div class="activity-title">[^<]*What Good Readers Do[^<]*</div>\s*'
                  r'<div class="activity-sub">.*?</div>', s, re.S)
    b = s.find('<div class="activity-body">', m.end())
    bs = b + len('<div class="activity-body">')
    stop = s.find('<div class="thinking-stop"', bs)
    if stop < 0:
        print('%-30s !! no thinking-stop' % fn); return
    new = '\n      <p>%s</p>\n' % para
    new += box
    if wb:
        new += (WB % wb); notes.append('wholebook')
    new += '      '
    s = s[:bs] + new + s[stop:]
    notes.append('para+howto')

    mo = re.search(r'(<strong>Reading:</strong>\s*)(.*?)(</span>)', s, re.S)
    if mo and fn in OBJ:
        s = s[:mo.start(2)] + OBJ[fn] + s[mo.end(2):]; notes.append('obj')
    for old in OLD_NOTES:
        if old in s:
            s = s.replace(old, NEW_NOTE[wk]); notes.append('vidnote'); break

    if s != orig:
        shutil.copy2(p, p + '.bak')
        open(p, 'w', encoding='utf-8').write(s)
        print('%-30s %s' % (fn, ', '.join(notes)))
    else:
        print('%-30s NO CHANGE' % fn)

for fn in sorted(W, key=lambda f: (int(re.match(r'lesson-(\d+)', f).group(1)), f)):
    patch(fn)
