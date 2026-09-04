# -*- coding: utf-8 -*-
"""Pass 4a: replace the 9 unverifiable RWM mentor sentences in How I Became a Ghost
(weeks 20-24, Days 2-3) with verbatim Tingle text, and rewrite the three steps to
analyse the real sentence. Every replacement exact-match verified against
planning docs/hbg_ocr.txt. Keeps this unit's own rwm-box / As a Reader / As a Writer /
Try It markup and its existing textareas."""
import re, os, shutil

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# fn -> (sentence, reader, writer, tryit, frame)
FIX = {
'lesson-20-2-hbg-ch13.html': (
 "By nightfall the snow stopped, but the air turned bitter and cold.",
 "This is the night Isaac tells his family what he has seen. Notice that the snow stopping is not a relief &mdash; the cold gets worse instead. What does the weather do to your sense of what is coming?",
 "Tingle sequences with two moves. <em>By nightfall</em> is a time transition that carries you forward without narrating the hours. Then the comma and <em>but</em> turn the sentence: the easing arrives first, the worsening second. The order is what builds the tension &mdash; put the cold first and the sentence loses its dread.",
 "Write one sentence about Chapter 13 that opens with a time transition, then uses a comma and <em>but</em> to turn from something easing to something getting worse.",
 "By ___, ___ stopped, but ___."),

'lesson-20-3-hbg-ch14.html': (
 "They made their camp for the evening, and by the time I woke up, they were cooking my squirrels for their supper.",
 "Joseph is telling Isaac what the soldiers did to him. A whole night passes inside this one sentence, and he wakes to find them eating his food. What does the calm way he tells it do to you as a reader?",
 "Three time markers and two commas, all in one sentence: <em>for the evening</em>, then <em>and by the time I woke up</em>, then what he found. Tingle skips the entire night rather than narrating it &mdash; that is how you sequence events so tension builds instead of sagging. The comma before <em>and</em> joins two full clauses; the second comma closes the time phrase.",
 "Write one sentence about Chapter 14 that skips over a stretch of time using a phrase like <em>by the time</em>, and punctuate the clauses correctly. A lighter scaffold this time &mdash; you have the pattern.",
 "___, and by the time ___, ___."),

'lesson-21-2-hbg-ch17.html': (
 "He was a powerful and important Choctaw, but he still had a sense of humor.",
 "This is how Isaac describes Chief Pushmataha. Nothing in the sentence is about war or removal. Why would Tingle spend a whole sentence on a great leader&rsquo;s sense of humour?",
 "The sentence is compound &mdash; two independent clauses joined by <em>, but</em> &mdash; and the turn is the point. The first clause gives you what you expected of a chief; the second gives you what you did not. To explain a theme you need details from more than one place: pair the expected detail with the surprising one, and the theme shows up in the gap between them.",
 "Write one compound sentence about a character in Chapter 17 that pairs something expected with something surprising. Join the two clauses with <em>, but</em>.",
 "___ was ___, but ___ still ___."),

'lesson-21-3-hbg-ch18.html': (
 "For the first time I realized what a burden I would be for my family.",
 "Isaac is watching his own father lift his body onto his shoulder. Back in Chapter 13 he told his family he would soon be a ghost. What does he understand now that he did not understand then?",
 "This is a theme sentence, and it works by reaching backwards. <em>For the first time</em> tells you there was a before &mdash; the chapter where he announced it and did not yet grasp it. A theme cannot be explained out of one moment. Tingle builds this one out of two moments far apart, and lets the phrase <em>for the first time</em> do the connecting.",
 "Write one sentence about Chapter 18 that uses a phrase like <em>for the first time</em> or <em>now I understood</em> to connect this chapter to something from earlier in the book.",
 "For the first time ___."),

'lesson-22-2-hbg-ch21.html': (
 "The panther ran to the fire and slapped the burning logs, sending fiery embers all about the camp.",
 "Joseph has become the panther, and this is the distraction that lets Naomi escape. What do you see and hear in this sentence? What does <em>slapped</em> give you that <em>hit</em> would not?",
 "The imagery is built out of exact verbs, not adjectives: <em>ran</em>, <em>slapped</em>, <em>sending</em>. Tingle never describes how the fire looked &mdash; the actions make you see it. Notice the pronoun discipline too: every action belongs to <em>the panther</em>, named once at the front, so nothing turns ambiguous while the sentence gets busy.",
 "Write one sentence about Chapter 21 that makes a reader see something, using two or three exact verbs and no adjectives. Name your subject once at the start and keep every action clearly attached to it.",
 "The ___ ran to the ___ and ___ the ___, sending ___ all about the ___."),

'lesson-22-3-hbg-ch22.html': (
 "In a sudden flash, like a thunderbolt that shook her very being, Naomi realized where she was.",
 "Naomi has been hidden in a stranger&rsquo;s wagon, being treated kindly. This is the moment she works out whose wagon it is. Why a thunderbolt, for a realisation that happens in silence?",
 "Tingle spends the whole middle of the sentence on a simile &mdash; <em>like a thunderbolt that shook her very being</em> &mdash; before he will tell you what she realised. The figurative language arrives first and the fact arrives last, so you feel the shock before you know its cause. That is what imagery is for: it does not decorate the meaning, it delivers it.",
 "Write one sentence about Chapter 22 that puts a simile in the middle, between an opening phrase and the fact at the end. Delay the fact and let the comparison land first.",
 "In a ___, like ___, ___ realized ___."),

'lesson-23-2-hbg-ch25.html': (
 "Ice-covered branches fell all about the camp, destroying the fire circle and toppling the cooking pot.",
 "Leader has just ordered his soldiers to fire into the trees above the Choctaw Council. This one sentence holds everything that came down afterwards. What has Tingle chosen to show you, out of everything that must have happened?",
 "Look at how much is packed in and how little is retold. One main clause &mdash; branches fell &mdash; and then two participles, <em>destroying</em> and <em>toppling</em>, carrying two more events without two more sentences. That is summarising by combining: choose the events that matter, hang them off a single clause, and leave the rest out.",
 "Write one sentence about Chapter 25 that summarises three things happening at once. Use one main clause and two <em>-ing</em> phrases, and leave out everything that does not matter.",
 "___ fell all about the ___, ___ing the ___ and ___ing the ___."),

'lesson-23-3-hbg-ch26.html': (
 "Instead, she carried Nita&rsquo;s body, wrapped in the blanket, and laid it by the fire.",
 "Leader has demanded that the family produce the girl who escaped. Instead of arguing, Nita&rsquo;s mother does this. What does the sentence tell you about her, without telling you anything about how she felt?",
 "The word <em>Instead</em> does the summarising &mdash; it stands in for a whole argument Tingle never writes out. Then two verbs, <em>carried</em> and <em>laid</em>, with the blanket folded in between as a phrase rather than a sentence of its own. Nothing about grief is stated anywhere. A summary earns its power by choosing the one action that says everything.",
 "Write one sentence about Chapter 26 that begins with <em>Instead</em> and reports a single action, with no explaining and no feelings named. A lighter scaffold this time.",
 "Instead, ___ and ___."),

'lesson-24-2-hbg-ch29.html': (
 "The winter was fierce and food was scarce, but our most feared enemy, Leader, left us alone to be with our families.",
 "This comes near the end of Isaac&rsquo;s account. Two hard facts, and then an exception. Why would he close his story by telling you what his enemy did <em>not</em> do?",
 "The sentence is shaped like an argument. Two clauses of evidence &mdash; the winter, the food &mdash; then <em>but</em> introduces the point that matters, with the appositive <em>Leader</em> naming the source of the threat exactly. When you compare a novel against a historical source you need this shape: state the conditions, then the finding, and name people and places precisely.",
 "Write one sentence in that shape about something you have read this week. Give two pieces of evidence, then <em>but</em>, then the point they add up to. Name people and places precisely, the way a formal source comparison does.",
 "___ was ___ and ___ was ___, but ___, ___, ___."),
}

def repl_one(seg, cls, new):
    m = re.search(r'(<div class="%s">)(.*?)(</div>)' % cls, seg, re.S)
    if not m:
        return seg, False
    return seg[:m.start(2)] + new + seg[m.end(2):], True

def patch(fn):
    p = os.path.join(D, fn)
    s = open(p, encoding='utf-8').read()
    orig = s
    sent, reader, writer, tryit, frame = FIX[fn]

    i = s.find('<div class="rwm-box">')
    if i < 0:
        print('%-26s !! no rwm-box' % fn); return
    end = s.find('</div>', s.rfind('journal-rwm-mimic', i)) + len('</div>')
    end = s.find('</div>', end) + len('</div>')
    seg = s[i:end]
    notes = []

    seg, ok = repl_one(seg, 'rwm-sentence', '&ldquo;%s&rdquo;' % sent)
    notes.append('sentence' if ok else '!!sentence')

    # the three step-texts, in document order
    texts = [reader, writer, tryit]
    out, pos, n = [], 0, 0
    for m in re.finditer(r'(<div class="rwm-step-text">)(.*?)(</div>)', seg, re.S):
        if n < 3:
            out.append(seg[pos:m.start(2)]); out.append(texts[n]); pos = m.end(2); n += 1
    out.append(seg[pos:])
    seg = ''.join(out)
    notes.append('steps%d' % n)

    if frame:
        seg, ok = repl_one(seg, 'rwm-frame', frame)
        notes.append('frame' if ok else 'no-frame-div')

    s = s[:i] + seg + s[end:]
    if s != orig:
        shutil.copy2(p, p + '.bak')
        open(p, 'w', encoding='utf-8').write(s)
        print('%-26s %s' % (fn, ', '.join(notes)))
    else:
        print('%-26s NO CHANGE' % fn)

for fn in sorted(FIX, key=lambda f: (int(re.match(r'lesson-(\d+)', f).group(1)), f)):
    patch(fn)
