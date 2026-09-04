# -*- coding: utf-8 -*-
"""Pass 2: realign WGRD + RWM in Johnny Tremain weeks 6-8 to the v2_poetry scope & sequence.
Built week 6 = scope week 7; built 7 = scope 8; built 8 = scope 9 (+ scope 10 folded into 8.4)."""
import re, os, shutil

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

KC = ('<div class="key-concept" style="background:#F0F7FF;border-color:#C8DCEE;margin:10px 0;">\n'
      '<div class="key-concept-label" style="color:#3D5285;">\U0001F50D How to Do It</div>\n'
      '<ol style="margin:6px 0 6px 20px;font-size:14px;color:#3A4A6B;line-height:1.8;">\n%s'
      '</ol>\n</div>\n')

def kc(*steps):
    return KC % ''.join('<li><strong>%s:</strong> %s</li>\n' % s for s in steps)

KC6 = kc(("Collect the rules","Note every detail that tells you how this society works &mdash; money, work, rank, religion, and what people are afraid of."),
         ("Ask what the setting allows","For each event, ask what this time and place make possible, and what they make impossible."),
         ("Hold your judgment","Before deciding a character is unfair or foolish, ask what their world would have expected of them."))
KC7 = kc(("Find who stands where","For each character, name what they are loyal to &mdash; a person, a trade, a king, or an idea."),
         ("Ask what it costs","Loyalty usually follows what someone stands to lose. Work out what each one would lose by changing sides."),
         ("Watch the narrator&rsquo;s angle","Notice whose thoughts you are given and whose you are not. That choice shapes whom you side with."))
KC8 = kc(("Find the claim","Look for the moment somebody says what they are fighting for, in their own words."),
         ("Trace the evidence","Ask what experience or event brought them to that claim. Arguments come from somewhere."),
         ("Follow it outward","Track who repeats the argument, who changes it, and who pays for it."))

# fn -> (activity-sub, [paragraphs], key-concept to INSERT or None, whole-book callout or None)
WB = ('<div class="callout callout-info" style="margin-top:10px;"><span class="callout-icon">\U0001F3AF</span>'
      '<p><strong>Whole-book thinking:</strong> %s</p></div>\n')

WGRD = {
 'lesson-6-1-jt-ch1.html': ('Set your reading lens', [
   "Good readers of historical fiction <strong>build background before they judge anything</strong>. A story set in "
   "1773 Boston runs on rules a modern reader does not know yet &mdash; who may speak to whom, what an apprentice "
   "owes his master, what a ruined hand costs a boy who works with his hands. Read Chapter 1 for the world first "
   "and the plot second."], KC6, None),
 'lesson-6-2-jt-ch2.html': ('Read closely for the world Johnny lives in', [
   "Today read closely and gather evidence about the world, not only the events. Chapter 2 puts Johnny&rsquo;s hand "
   "in the crucible and then shows you what Boston does with an injured apprentice: no trade, no indenture, no "
   "place. Forbes never stops to explain the apprentice system &mdash; she lets its consequences do the "
   "explaining. Collect the details that carry it."], KC6, None),
 'lesson-6-4-jt-ch4.html': (None, None, None,
   "Across Chapters 1&ndash;4, list what 1773 Boston has decided for Johnny that he never chose. Then say in one "
   "sentence what this setting makes possible for a boy like him &mdash; and what it makes impossible."),
 'lesson-7-1-jt-ch5.html': ('Set your reading lens', [
   "Good readers notice that <strong>loyalty is a perspective</strong>. Everyone in this book is loyal to "
   "something, and almost nobody agrees about what. Loyalty is not a label a character wears &mdash; it comes out "
   "of what they have, what they stand to lose, and who taught them. Today, watch what Johnny is being let into: a "
   "trade, a friendship, and a room full of men with opinions."], KC7, None),
 'lesson-7-2-jt-ch6.html': ('Read closely for perspective and loyalty', [
   "Read closely and gather evidence today. Chapter 6 is the tea party, and every man in it has a reason. Watch "
   "the secrecy and the disguises, and ask what each one risks by being there. Forbes gives you the "
   "Observers&rsquo; side most fully &mdash; notice what that does to your sympathy, and what she never shows "
   "you at all."], KC7, None),
 'lesson-7-4-jt-ch8.html': (None, None, None,
   "Across Chapters 5&ndash;8, whose loyalty has been tested hardest? Pick one character, name what they were "
   "loyal to at the start of the week and what they are loyal to now, and find the passage where it turned."),
 'lesson-8-1-jt-ch9.html': ('Set your reading lens', [
   "Good readers can <strong>track an argument as it develops</strong>. A cause is not an event &mdash; it is a "
   "claim that enough people came to believe, and it arrives in pieces: a grievance, a slogan, a death, a "
   "decision. Chapter 9 is where the argument stops being talk. Watch how it gets stated, and by whom."], KC8, None),
 'lesson-8-2-jt-ch10.html': ('Read closely for the argument', [
   "Read closely and gather evidence today. Chapter 10 is the night the warning system runs &mdash; the lanterns, "
   "the rides, the counting of hours. Nobody in it makes a speech, and yet the argument is everywhere in what "
   "people are willing to risk. Collect what each action tells you about what these people believe."], KC8, None),
 'lesson-8-4-jt-ch12.html': ('Synthesize the unit — the novel and the argument', [
   "This is the last day of the unit, and today you do two things at once: you finish the novel, and you finish "
   "thinking like someone building an argument. Chapter 12 gives the cause its price &mdash; Rab, who believed it "
   "early and clearly, does not survive it. Synthesize what the historical fiction has shown you with what you "
   "have learned about arguing from evidence."], None,
   "You have read a novel and you are writing an argument. Across the whole book, state in one sentence what "
   "Forbes is arguing about the cause Johnny joins. Then find the two passages you would use as evidence, and say "
   "why you would put them in that order."),
}

# ------------------------------------------------------------------ RWM
def step(label, text, prompt, jid, jlabel, placeholder, frame=None):
    out  = '    <div class="rwm-step">\n'
    out += '      <div class="rwm-step-label">%s</div>\n' % label
    out += '      <div class="rwm-step-text">%s</div>\n' % text
    if frame:
        out += '      <div class="rwm-frame">%s</div>\n' % frame
    out += '      <div class="textbox-prompt">%s</div>\n' % prompt
    lab = 'Your sentence' if jid.endswith('mimic') else 'Your response'
    out += '      <div class="journal-label">\U0001F4D3 %s <span class="saved-dot" id="dot-%s"></span></div>\n' % (lab, jid)
    out += ('      <textarea class="journal-box" id="journal-%s" data-label="%s" placeholder="%s" '
            'oninput="autoSave(this,\'dot-%s\');gatherAnswers();"></textarea>\n') % (jid, jlabel, placeholder, jid)
    out += '    </div>\n'
    return out

L_R = '&#x1F4D6; Read like a Reader'
L_W = '&#x270F;&#xFE0F; Read like a Writer'
L_M = '&#x1F58A;&#xFE0F; Mimic'

def rwm_box(sentence, reader, rp, writer, wp, mimic, mp, frame=None):
    disp = sentence if sentence.lstrip().startswith('&ldquo;') else '&ldquo;%s&rdquo;' % sentence
    out  = '<div class="rwm-box">\n'
    out += '    <div class="rwm-header">RWM &mdash; Read like a Reader, Read like a Writer, Mimic</div>\n'
    out += '    <div class="rwm-sentence">%s</div>\n' % disp
    out += step(L_R, reader, rp, 'rwm-reader', 'RWM — Read like a Reader', 'This sentence shows...')
    out += step(L_W, writer, wp, 'rwm-writer', 'RWM — Read like a Writer', 'Forbes built it by...')
    out += step(L_M, mimic,  mp, 'rwm-mimic',  'RWM — Mimic', 'Write your sentence here...', frame)
    out += '  '
    return out

RWM = {
 'lesson-6-2-jt-ch2.html': rwm_box(
   "He walked all over Boston, his hand thrust deep in his breeches pocket.",
   "Johnny&rsquo;s hand has been ruined and he cannot work. He is not walking anywhere in particular &mdash; he "
   "is walking so that he does not have to sit still and be looked at. Why does he keep the hand in his pocket?",
   "Write 1&ndash;2 sentences explaining what the hidden hand tells you about Johnny.",
   "Count how much history Forbes puts in this sentence without explaining any of it: <em>Boston</em>, and "
   "<em>breeches</em>. She never stops to tell you that a boy in 1773 wore knee breeches with a pocket at the "
   "hip, and she does not need to &mdash; the detail does its work while the sentence gets on with the walking. "
   "That is how historical context earns its place: it rides inside the action instead of interrupting it.",
   "Write 1 sentence explaining how Forbes gives you the period without stopping to explain it.",
   "Write one sentence about a character moving through Boston. Put one true period detail inside it &mdash; a "
   "garment, a tool, a trade, a street &mdash; and do not explain the detail. Let the action carry it.",
   "Write your own sentence using the same technique.",
   frame="[Character] ___, his ___ ___ in his ___."),

 'lesson-6-3-jt-ch3.html': rwm_box(
   "Without heeding anyone, he crossed Dock Square and in a moment&rsquo;s time stood beside the brick Town House "
   "at the head of King Street.",
   "Johnny has been turned away from every silversmith&rsquo;s shop in Boston. This is the walk he takes "
   "afterwards. What does the pace of it &mdash; crossing a square, standing at a corner &mdash; tell you about "
   "what he is doing with himself?",
   "Write 1&ndash;2 sentences explaining what this walk shows about Johnny&rsquo;s situation.",
   "Forbes names three real places in one sentence &mdash; Dock Square, the brick Town House, the head of King "
   "Street &mdash; and explains none of them. She writes as though you live there. That trust is the craft move: "
   "naming a place precisely makes the world solid, while explaining it would turn the reader into a tourist.",
   "Write 1 sentence explaining what the real place names do that a general description could not.",
   "Write one sentence that moves a character through two or three named places without explaining any of them. "
   "Precise names, no tour guide. Trust your reader the way Forbes trusts hers. No frame this time &mdash; you "
   "have the pattern.",
   "Write your own sentence using the same technique."),

 'lesson-7-2-jt-ch6.html': rwm_box(
   "Johnny did not care for Molineaux because he bellowed and roared so loudly.",
   "Molineaux is one of the Observers &mdash; on Johnny&rsquo;s own side of the argument. Johnny still does not "
   "like him. What does that tell you about how Johnny judges people?",
   "Write 1&ndash;2 sentences explaining what this shows about Johnny&rsquo;s perspective.",
   "The sentence is a claim bolted to its evidence. The claim is <em>did not care for Molineaux</em>; the evidence "
   "is exactly one thing &mdash; <em>he bellowed and roared so loudly</em>. Forbes does not pile on three "
   "reasons, because one precise detail is more convincing than a list. Notice the pronoun too: <em>he</em> could "
   "mean Johnny or Molineaux, and only the sense of the sentence tells you which. In your own writing that is a "
   "risk worth avoiding &mdash; keep it obvious who <em>he</em> is.",
   "Write 1 sentence explaining why one precise detail supports the claim better than several vague ones.",
   "Write one sentence that makes a claim about a character in Chapter 6 and supports it with exactly one precise "
   "detail from the text. Make sure any pronoun you use points clearly to one person.",
   "Write your own sentence using the same technique.",
   frame="[Character] did not care for ___ because ___."),

 'lesson-7-3-jt-ch7.html': rwm_box(
   "The subscriptions had dropped, partly because many people could not afford a paper, and partly because so "
   "many Whig families were leaving Boston for the country.",
   "The Port Act has closed Boston and the <em>Observer</em> is losing readers. Two different kinds of people have "
   "stopped subscribing. What does each group tell you about what the closing has done to the city?",
   "Write 1&ndash;2 sentences explaining what the lost subscriptions reveal about Boston.",
   "Forbes states the claim first &mdash; <em>the subscriptions had dropped</em> &mdash; then gives two pieces of "
   "evidence in the same shape: <em>partly because&hellip; and partly because&hellip;</em>. The parallel wording "
   "is what makes the evidence feel weighed rather than guessed at, and <em>partly</em> is an honest word: it "
   "admits that neither reason explains the whole thing.",
   "Write 1 sentence explaining what the word <em>partly</em> adds to the claim.",
   "Write one sentence that states a claim about Boston in Chapter 7 and supports it with two pieces of evidence "
   "in parallel wording. Use <em>partly because&hellip; and partly because&hellip;</em> if it helps, and be "
   "honest about what your evidence does not prove.",
   "Write your own sentence using the same technique."),

 'lesson-8-2-jt-ch10.html': rwm_box(
   "Gage had sent him either because he knew he was a better officer than Colonel Smith or because he had a way "
   "with Yankees.",
   "Nobody has told Johnny why Gage chose this officer. This sentence is somebody working it out from the "
   "outside. What can you actually know about a decision you did not witness?",
   "Write 1&ndash;2 sentences explaining what this sentence knows and what it only guesses.",
   "This is a reasoning sentence: one piece of evidence &mdash; <em>Gage had sent him</em> &mdash; followed by "
   "explanation. Look at how honest the structure is. Forbes writes <em>either because&hellip; or "
   "because&hellip;</em>, laying out two possible explanations and refusing to choose. A reasoning sentence does "
   "not have to be certain; it has to show its thinking. The word <em>because</em> is what marks the explanation "
   "off from the evidence.",
   "Write 1 sentence explaining how <em>either&hellip; or&hellip;</em> keeps the reasoning honest.",
   "Write one sentence about a choice someone makes in Chapter 10. State what they did, then give two possible "
   "explanations joined by <em>either because&hellip; or because&hellip;</em>. Do not decide between them.",
   "Write your own sentence using the same technique.",
   frame="[Person] ___ either because ___ or because ___."),

 'lesson-8-3-jt-ch11.html': rwm_box(
   "But the people of Boston knew no more than Gage that the fighting had begun.",
   "The fighting has started at Lexington. Boston does not know. Gage, who ordered the march, does not know "
   "either. What does it do to you as a reader to know something that everybody in the chapter does not?",
   "Write 1&ndash;2 sentences explaining what this gap between reader and city creates.",
   "The whole weight of this sentence sits on its first word. <em>But</em> is a contrast transition, and here it "
   "is doing the work of an explanation &mdash; it tells you to read this fact against the one before it. Forbes "
   "gives you the evidence, that Boston knew nothing, and lets the transition supply the reasoning. When you "
   "write, a transition is not decoration: <em>but</em>, <em>because</em> and <em>so</em> each tell your reader "
   "what to do with the sentence coming next.",
   "Write 1 sentence explaining what work the word <em>But</em> does here.",
   "Write two sentences about Chapter 11. Make the first one a plain fact, then open the second with <em>But</em>, "
   "<em>because</em> or <em>so</em> &mdash; whichever tells your reader the right thing to do with that fact.",
   "Write your own sentences using the same technique."),
}

GATHER = """  output+='\\n';
  output+='\\u270D\\uFE0F RWM \\u2014 READ, WRITE, MIMIC\\n';
  output+='\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\u2500\\n';
  ['journal-rwm-reader','journal-rwm-writer','journal-rwm-mimic'].forEach(function(id){
    var el=document.getElementById(id);
    if(!el)return;
    output+='\\n'+(el.getAttribute('data-label')||id)+'\\n';
    output+=(el.value.trim()||'(no answer)')+'\\n';
  });
"""

OLD_NOTE = ("As you read, pay close attention to the characters&#x27; actions and motivations. "
            "Think about how events connect to the bigger ideas in the story.")
NEW_NOTE = {6:("As you read, build the world first &mdash; notice the rules of 1773 Boston that the story runs on, "
               "and ask what this setting makes possible and impossible."),
            7:("As you read, track perspective and loyalty &mdash; name what each character is loyal to, and what "
               "they stand to lose by changing sides."),
            8:("As you read, track the argument as it develops &mdash; who states the cause, what brought them to "
               "it, and who repeats it.")}

FILES = sorted(set(list(WGRD) + list(RWM)) | {'lesson-6-3-jt-ch3.html','lesson-7-3-jt-ch7.html','lesson-8-3-jt-ch11.html'})

def patch(fn):
    p = os.path.join(D, fn)
    s = open(p, encoding='utf-8').read()
    orig = s
    w = int(re.match(r'lesson-(\d+)', fn).group(1))
    notes = []

    m = re.search(r'<div class="activity-title">[^<]*What Good Readers Do[^<]*</div>\s*'
                  r'<div class="activity-sub">(.*?)</div>', s)
    if not m:
        raise SystemExit('%s: no WGRD head' % fn)

    if fn in WGRD:
        sub, paras, box, wb = WGRD[fn]
        if sub:
            s = s[:m.start(1)] + sub + s[m.end(1):]
            m = re.search(r'<div class="activity-title">[^<]*What Good Readers Do[^<]*</div>\s*'
                          r'<div class="activity-sub">(.*?)</div>', s)
            notes.append('sub')
        b = s.find('<div class="activity-body">', m.start())
        bs = b + len('<div class="activity-body">')
        cands = [x for x in [s.find('<div class="key-concept"', bs),
                             s.find('<div class="socratic-box"', bs)] if x > 0]
        nxt = min(cands)
        if paras:
            new = '\n' + ''.join('      <p>%s</p>\n' % x for x in paras)
            new += box if box else '      '
            s = s[:bs] + new + s[nxt:]
            notes.append('paras' + ('+howto' if box else ''))
        if wb:
            # insert whole-book callout just before the socratic-box in the WGRD block
            m2 = re.search(r'<div class="activity-title">[^<]*What Good Readers Do[^<]*</div>', s)
            sb = s.find('<div class="socratic-box"', m2.end())
            if 'Whole-book thinking' not in s:
                s = s[:sb] + (WB % wb) + s[sb:]
                notes.append('wholebook')

    if fn in RWM:
        i = s.find('<div class="rwm-box">')
        if i >= 0:
            end = s.find('<div class="tab-next-wrap">', i)
            k = s.rfind('</div>', i, end)
            s = s[:i] + RWM[fn] + s[k:]
            notes.append('rwm-replaced')
        else:
            wrap = -1
            for mw in re.finditer(r'<div class="tab-next-wrap">', s):
                if "switchTab('reading')" in s[mw.start():mw.start() + 500]:
                    wrap = mw.start(); break
            if wrap < 0:
                raise SystemExit('%s: no Word Study tab-next-wrap' % fn)
            s = s[:wrap] + '<!-- ═══ RWM ═══ -->\n  ' + RWM[fn] + '</div>\n\n  ' + s[wrap:]
            notes.append('rwm-added')
        g = s.find('function gatherAnswers')
        gend = s.find('\n}', g)
        if 'journal-rwm-reader' not in s[g:gend]:
            mm = re.search(r"\n( *)output\+='[^']*PRACTICE ACTIVITY STATUS", s[g:gend])
            if mm:
                s = s[:g + mm.start() + 1] + GATHER + s[g + mm.start() + 1:]
                notes.append('gather')
            else:
                notes.append('!!NO-GATHER-ANCHOR')

    if OLD_NOTE in s:
        s = s.replace(OLD_NOTE, NEW_NOTE[w]); notes.append('vidnote')
    s = s.replace('Synthesise', 'Synthesize')

    if s != orig:
        shutil.copy2(p, p + '.bak')
        open(p, 'w', encoding='utf-8').write(s)
        print('%-26s %s' % (fn, ', '.join(notes)))
    else:
        print('%-26s NO CHANGE' % fn)

for fn in FILES:
    patch(fn)
