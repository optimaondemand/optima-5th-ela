# -*- coding: utf-8 -*-
"""Pass 3: realign WGRD in Carry On, Mr. Bowditch weeks 9-14 to the v2_poetry S&S.
Built 9-14 = scope 11-16, chapter-for-chapter (Ch 1-4, 5-8, 9-12, 13-16, 17-20, 21-24).
RWM is NOT built here - no verified Bowditch text is available on disk.
Two WGRD markup families: `activity` blocks (22 files) and `wgrd-block` (9.3, 9.4 only)."""
import re, os, shutil, sys

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

KC = ('<div class="key-concept" style="background:#F0F7FF;border-color:#C8DCEE;margin:10px 0;">\n'
      '<div class="key-concept-label" style="color:#3D5285;">\U0001F50D How to Do It</div>\n'
      '<ol style="margin:6px 0 6px 20px;font-size:14px;color:#3A4A6B;line-height:1.8;">\n%s'
      '</ol>\n</div>\n')
def kc(*steps):
    return KC % ''.join('<li><strong>%s:</strong> %s</li>\n' % s for s in steps)

KC9 = kc(("Remember it happened","This was a real life. Ask what Latham could actually have known, and where she must be filling in."),
         ("Watch for story shape","A biography still uses scenes, dialogue and suspense. Notice where Latham writes like a novelist."),
         ("Separate record from craft","Ask which details are the historical record, and which are the author&rsquo;s choices about how to tell it."))
KC10 = kc(("Name the problem","For each event, say plainly what problem it puts in front of Nat."),
          ("Watch what he does with it","Look for the specific action he takes. A life story turns on what a person does next."),
          ("Follow the consequence forward","Ask what this makes possible later. A life story is a chain, not a list."))
KC11 = kc(("Find the moment quitting was an option","Perseverance only shows where giving up was genuinely available."),
          ("Ask what keeps him going","Look for the reason the text gives, not the one you would supply yourself."),
          ("Name the theme as a sentence","Say what the book argues about people who keep going. &ldquo;Perseverance&rdquo; is a topic; a theme is a full sentence."))
KC12 = kc(("Collect the terms","List the navigation and sailing words the chapter needs &mdash; longitude, lunars, masthead, bearing, tables."),
          ("Work out the meaning from the work it does","Ask what the word lets a sailor <em>do</em>. In this book a technical term is a tool, not decoration."),
          ("Test what the term unlocks","Reread the moment with the term defined and see how much the scene changes."))
KC13 = kc(("Find the author in the sentence","Look for words that judge, admire or explain. Those are Latham, not the record."),
          ("Ask what she includes and leaves out","Perspective shows in what gets a whole chapter and what gets a sentence."),
          ("Test it against another telling","Ask how a different biographer &mdash; or Nat himself &mdash; might have written the same event."))
KC14 = kc(("Put the threads together","Hold the events, the problem-solving, the perseverance and the technical work in one view."),
          ("State the significance","Say why this life mattered beyond itself. That is what expository writing about a person has to do."),
          ("Support every claim","For each thing you say about the whole book, name the chapter you would send a reader to."))

WB = ('<div class="callout callout-info" style="margin-top:10px;"><span class="callout-icon">\U0001F3AF</span>'
      '<p><strong>Whole-book thinking:</strong> %s</p></div>\n')

# fn -> (sub or None, [paragraphs] or None, how-to box or None, whole-book text or None)
W = {
 'lesson-9-1-cmb-ch1.html': ('Set your reading lens before you open the book', [
   "Good readers of <strong>biography</strong> read two things at once: a life that really happened, and an "
   "author&rsquo;s decisions about how to tell it. Nathaniel Bowditch was a real boy in Salem, and Jean Lee "
   "Latham tells his story with scenes, dialogue and suspense borrowed from fiction. As you read Chapter 1, "
   "notice the record and the storytelling both."], KC9, None),
 'lesson-9-2-cmb-ch2.html': ('Read closely — where a real life turns into a story', [
   "Read closely today and gather evidence. Chapter 2 gives Nat a real decision to make, and Latham writes it as "
   "a scene with dialogue rather than a summary of events. Ask yourself what a plain record of Nat&rsquo;s life "
   "would have said about this day &mdash; and what Latham does instead."], KC9, None),
 'lesson-9-3-cmb-ch3.html': ('Reread — a real life, shaped by an author', [
   "Today reread one passage from Chapter 3 and look at it as an author&rsquo;s work. Latham had no recording of "
   "these conversations. She had letters, records and dates, and she built scenes out of them. Reread the passage "
   "and ask which parts must rest on the record, and which parts are Latham deciding how the moment should "
   "<em>feel</em>."], KC9, None),
 'lesson-9-4-cmb-ch4.html': ('Synthesize the week — biography as literature', [
   "Now put the week together. Across Chapters 1&ndash;4 you have met a real boy whose story is being shaped by a "
   "writer. Say what you have learned about how biography works: what it owes to the facts, and what it borrows "
   "from fiction to make a life readable."], KC9,
   "Across Chapters 1&ndash;4, pick the one scene that feels most like a novel. Say what the record underneath it "
   "probably was, and what Latham added to turn it into a scene. Then say whether you think the addition was fair."),

 'lesson-10-1-cmb-ch5.html': ('Set your reading lens', [
   "Good readers of a life story watch <strong>problems and what a person does with them</strong>. An event only "
   "matters in a biography if it changes what someone can do next. In Chapter 5 Latham lets Nat believe something "
   "better is coming, and then closes the door. Read for the problem that creates, and for what Nat starts doing "
   "about it."], KC10, None),
 'lesson-10-2-cmb-ch6.html': ('Read closely for the problem and the response', [
   "Read closely and gather evidence. Chapter 6 hands Nat both a problem and a way of meeting it &mdash; "
   "<em>sail by ash breeze</em>, which means rowing when the wind dies. Notice what he does immediately after he "
   "hears it. In a life story, advice only counts once you can see it turn into an action."], KC10, None),
 'lesson-10-3-cmb-ch7.html': ('Reread — how one solution builds the next', [
   "Today reread the passage in Chapter 7 where Nat works through the calculations. Latham never tells you he was "
   "brilliant; she shows you exactly what he did. Reread it and trace the chain: what problem sent him to the "
   "book, what he did about it, and what that made possible next."], KC10, None),
 'lesson-10-4-cmb-ch8.html': ('Synthesize the week — a chain of problems solved', [
   "Now put the week together. Look back across Chapters 5&ndash;8 and lay the events end to end. For each one, "
   "name the problem and name what Nat did with it &mdash; then say what the chain adds up to. A life story is "
   "built out of what someone does after things go wrong."], KC10,
   "Across Chapters 5&ndash;8, which single problem changed the most about what Nat could do afterwards? Name it, "
   "name what he did, and trace forward to one later thing it made possible."),

 'lesson-11-1-cmb-ch9.html': ('Set your reading lens', [
   "Good readers watch <strong>perseverance become a theme</strong>. An &ldquo;anchor to windward&rdquo; is a real "
   "safety measure: in a storm a sailor heaves an anchor out on the side the wind comes from, so the ship cannot "
   "drift. By Chapter 9 Nat has built one in his mind. Ask what he has been holding onto through nine years, and "
   "what this book is beginning to say about people who keep going."], KC11, None),
 'lesson-11-2-cmb-ch10.html': ('Read closely for what the perseverance cost', [
   "Read closely and gather evidence. Chapter 10 is the hinge of the book: after nine years, the indenture ends. "
   "Notice how Latham handles it &mdash; whether she dwells on the feeling, hurries past it, or shows it "
   "sideways. What an author chooses to linger on is where you find the theme."], KC11, None),
 'lesson-11-3-cmb-ch11.html': ('Reread — perseverance turning into skill', [
   "Today reread the passage in Chapter 11 where everything Nat built in the chandlery &mdash; mathematics, "
   "navigation, astronomy &mdash; finally gets used. Reread it and ask what those nine years actually bought "
   "him. This is where the book&rsquo;s argument about persistence stops being encouragement and becomes "
   "evidence."], KC11, None),
 'lesson-11-4-cmb-ch12.html': ('Synthesize the week — name the theme', [
   "Now put the week together. The chapter titles across Chapters 9&ndash;12 make a sentence of their own: Anchor "
   "to Windward, Freedom, What Next?, Down to the Sea. Say in one full sentence what this book argues about "
   "perseverance &mdash; not the word, the claim."], KC11,
   "State the theme of this book about perseverance as one full sentence about people. Then find the chapter from "
   "1&ndash;12 that gives you the strongest evidence for it, and the one that complicates it."),

 'lesson-12-1-cmb-ch13.html': ('Set your reading lens', [
   "Good readers treat <strong>technical vocabulary</strong> as a way into meaning, not an obstacle. Chapter 13 "
   "turns on one term: the navigation book sailors trusted with their lives, and the hundreds of calculation "
   "errors Nat finds in it. You cannot feel how serious that is until you know what a navigation table is "
   "<em>for</em>. Read for the words that carry the danger."], KC12, None),
 'lesson-12-2-cmb-ch14.html': ('Read closely for the words that carry the meaning', [
   "Read closely and gather evidence. Chapter 14 brings Nat back to Salem, and the language shifts with the "
   "setting &mdash; harbor and community words in place of open-sea ones. Collect the terms this chapter needs, "
   "and for each one ask what it lets a person do."], KC12, None),
 'lesson-12-3-cmb-ch15.html': ('Reread — one term, and what it makes possible', [
   "Today reread the moment in Chapter 15 when the lookout cries <em>Sail ho!</em> from the masthead. Three words, "
   "and everyone on deck has to decide whether to flee, fight or hold course. Reread it and work out how much of "
   "the tension is living inside the vocabulary itself."], KC12, None),
 'lesson-12-4-cmb-ch16.html': ('Synthesize the week — technical language as an argument', [
   "Now put the week together. Chapter 16 gives the week its organizing idea: Nat insists that the hardest "
   "calculations, the ones experts say ordinary sailors cannot manage, are &ldquo;a simple matter of "
   "mathematics.&rdquo; That claim only works if the words are explained. Say how technical vocabulary carries "
   "the meaning of this whole week."], KC12,
   "Nat&rsquo;s whole project is making expert language usable by ordinary sailors. Pick two technical terms from "
   "Chapters 13&ndash;16 and explain each one the way Nat would &mdash; plainly enough that a reader who has "
   "never been to sea could use it."),

 'lesson-13-1-cmb-ch17.html': ('Set your reading lens', [
   "Good readers notice the <strong>author&rsquo;s perspective</strong> inside a biography. Latham is not neutral "
   "about Nathaniel Bowditch &mdash; she admires him, and that admiration decides which moments get a whole "
   "chapter and which get a sentence. In Chapter 17 the moon is both a precise instrument for finding longitude "
   "and something closer to wonder. That double vision is hers, not the record&rsquo;s."], KC13, None),
 'lesson-13-2-cmb-ch18.html': ('Read closely for the author’s hand', [
   "Read closely and gather evidence. Chapter 18 is a rescue at sea, and Latham does not report it flatly &mdash; "
   "she writes the dark, the spray, the hurry. Ask why a biographer would make you <em>feel</em> a scene instead "
   "of summarizing it, and what that choice tells you about how she sees Nat."], KC13, None),
 'lesson-13-3-cmb-ch19.html': ('Reread — whose judgment are you reading?', [
   "Today reread the passage in Chapter 19 where Nat&rsquo;s own certainty runs against his orders. Reread it and "
   "ask whose side the writing is on. Notice the words that carry a verdict &mdash; an author&rsquo;s "
   "perspective usually hides inside an adjective."], KC13, None),
 'lesson-13-4-cmb-ch20.html': ('Synthesize the week — the biographer’s point of view', [
   "Now put the week together. Chapter 20 is called &ldquo;Book Sailing,&rdquo; and the phrase is itself an "
   "opinion about what Nat did. Say what Latham&rsquo;s perspective on Nathaniel Bowditch is, and point to three "
   "places in Chapters 17&ndash;20 where you can see it."], KC13,
   "Latham admires Nat. Find one place in the book where that admiration makes the story stronger, and one place "
   "where you would like to have heard from someone who disagreed with him."),

 'lesson-14-1-cmb-ch21.html': (None, None, KC14, None),
 'lesson-14-2-cmb-ch22.html': (None, None, KC14, None),
 'lesson-14-3-cmb-ch23.html': (None, None, KC14, None),
 'lesson-14-4-cmb-ch24.html': (None, None, KC14,
   "You have read a life and you are writing about it. In one sentence, say what Nathaniel Bowditch&rsquo;s life "
   "changed for people who never met him. Then name the three chapters you would use as evidence, and say why in "
   "that order."),
}

OBJ = {
 'lesson-9-1-cmb-ch1.html':"I will <em>define</em> what makes a biography literary nonfiction by noticing where Latham tells Nat&rsquo;s real life like a story.",
 'lesson-9-2-cmb-ch2.html':"I will <em>identify</em> the storytelling choices Latham makes in Chapter 2 &mdash; scene and dialogue instead of summary.",
 'lesson-9-3-cmb-ch3.html':"I will <em>analyze</em> a passage from Chapter 3 to separate what rests on the record from what Latham shaped.",
 'lesson-9-4-cmb-ch4.html':"I will <em>explain</em> what biography owes to fact and what it borrows from fiction, across Chapters 1&ndash;4.",
 'lesson-10-1-cmb-ch5.html':"I will <em>define</em> how one event can reshape a life by naming the problem Chapter 5 creates for Nat.",
 'lesson-10-2-cmb-ch6.html':"I will <em>identify</em> the problem Chapter 6 puts in front of Nat and the action he takes about it.",
 'lesson-10-3-cmb-ch7.html':"I will <em>analyze</em> the chain in Chapter 7 &mdash; what sent Nat to the calculations, what he did, and what it made possible.",
 'lesson-10-4-cmb-ch8.html':"I will <em>explain</em> how the problems Nat solved across Chapters 5&ndash;8 shape the rest of his life story.",
 'lesson-11-1-cmb-ch9.html':"I will <em>define</em> perseverance in this book by naming what Nat has held onto through nine years.",
 'lesson-11-2-cmb-ch10.html':"I will <em>identify</em> how Latham handles the end of the indenture, and what her choice reveals about the theme.",
 'lesson-11-3-cmb-ch11.html':"I will <em>analyze</em> what nine years of study actually bought Nat, as evidence for the book&rsquo;s argument about persistence.",
 'lesson-11-4-cmb-ch12.html':"I will <em>explain</em> the theme of Chapters 9&ndash;12 in one full sentence about people, not a single word.",
 'lesson-12-1-cmb-ch13.html':"I will <em>define</em> how technical vocabulary carries meaning by explaining what a navigation table is for.",
 'lesson-12-2-cmb-ch14.html':"I will <em>identify</em> the technical terms Chapter 14 needs and say what each one lets a person do.",
 'lesson-12-3-cmb-ch15.html':"I will <em>analyze</em> how much of the tension in Chapter 15 lives inside the sailing vocabulary itself.",
 'lesson-12-4-cmb-ch16.html':"I will <em>explain</em> how technical vocabulary supports the meaning of Chapters 13&ndash;16.",
 'lesson-13-1-cmb-ch17.html':"I will <em>define</em> author perspective in biography by finding Latham&rsquo;s admiration in Chapter 17.",
 'lesson-13-2-cmb-ch18.html':"I will <em>identify</em> the choices Latham makes in Chapter 18 that show how she sees Nat.",
 'lesson-13-3-cmb-ch19.html':"I will <em>analyze</em> whose judgment the writing carries in Chapter 19, down to the adjectives.",
 'lesson-13-4-cmb-ch20.html':"I will <em>explain</em> Latham&rsquo;s perspective on Nathaniel Bowditch and point to evidence in Chapters 17&ndash;20.",
}

OLD_NOTE = ("As you read, pay close attention to the characters&#x27; actions and motivations. "
            "Think about how events connect to the bigger ideas in the story.")
NEW_NOTE = {
 9:"As you read, remember this is a real life being shaped by a writer &mdash; notice the record and the storytelling both.",
 10:"As you read, name the problem each event creates and watch what Nat actually does about it.",
 11:"As you read, watch perseverance become a theme &mdash; what Nat holds onto, and what it costs him.",
 12:"As you read, treat the navigation words as tools &mdash; work out what each one lets a sailor do.",
 13:"As you read, look for Latham&rsquo;s own perspective &mdash; the words that judge, admire, or explain.",
 14:"As you read, synthesize the whole book &mdash; the events, the persistence, the technical work, and why this life mattered.",
}

def patch(fn):
    p = os.path.join(D, fn)
    s = open(p, encoding='utf-8').read()
    orig = s
    w = int(re.match(r'lesson-(\d+)', fn).group(1))
    notes = []
    sub, paras, box, wb = W[fn]

    if '<div class="wgrd-block">' in s:                      # 9.3 / 9.4 family
        blk = s.find('<div class="wgrd-block">')
        end = s.find('</div>', s.find('class="wgrd-body"', blk))
        if sub:
            m = re.search(r'<div class="wgrd-strategy">(.*?)</div>', s[blk:end + 20], re.S)
            s = s[:blk + m.start(1)] + sub + s[blk + m.end(1):]
            notes.append('strategy')
            blk = s.find('<div class="wgrd-block">')
        mb = re.search(r'<div class="wgrd-body">(.*?)</div>', s[blk:], re.S)
        bs, be = blk + mb.start(1), blk + mb.end(1)
        if paras:
            s = s[:bs] + ' '.join(paras) + s[be:]
            notes.append('body')
        close = s.find('</div>', s.find('class="wgrd-body"', blk)) + len('</div>')
        add = (box or '') + ((WB % wb) if wb and 'Whole-book thinking' not in s else '')
        if add:
            s = s[:close] + '\n    ' + add + '  ' + s[close:]
            notes.append('howto' + ('+wholebook' if wb else ''))
    else:                                                     # activity family
        m = re.search(r'<div class="activity-title">[^<]*What Good Readers Do[^<]*</div>\s*'
                      r'<div class="activity-sub">(.*?)</div>', s, re.S)
        if not m:
            raise SystemExit('%s: no WGRD head' % fn)
        if sub:
            s = s[:m.start(1)] + sub + s[m.end(1):]
            notes.append('sub')
            m = re.search(r'<div class="activity-title">[^<]*What Good Readers Do[^<]*</div>\s*'
                          r'<div class="activity-sub">(.*?)</div>', s, re.S)
        b = s.find('<div class="activity-body">', m.start())
        bs = b + len('<div class="activity-body">')
        cands = [x for x in [s.find('<div class="key-concept"', bs),
                             s.find('<div class="socratic-box"', bs),
                             s.find('<div class="callout', bs)] if x > 0]
        nxt = min(cands)
        new = ''
        if paras:
            new = '\n' + ''.join('      <p>%s</p>\n' % x for x in paras)
        else:
            new = s[bs:nxt]
        if box:
            new = new.rstrip() + '\n' + box
        if wb and 'Whole-book thinking' not in s:
            new = new.rstrip() + '\n' + (WB % wb)
            notes.append('wholebook')
        s = s[:bs] + new + '      ' + s[nxt:]
        notes.append('paras' if paras else 'kept-paras')
        if box: notes.append('howto')

    if fn in OBJ:
        mo = re.search(r'(<strong>Reading:</strong>\s*)(.*?)(</span>)', s, re.S)
        if mo:
            s = s[:mo.start(2)] + OBJ[fn] + s[mo.end(2):]
            notes.append('obj')
    if OLD_NOTE in s:
        s = s.replace(OLD_NOTE, NEW_NOTE[w]); notes.append('vidnote')
    s = s.replace('Synthesise', 'Synthesize')

    if s != orig:
        shutil.copy2(p, p + '.bak')
        open(p, 'w', encoding='utf-8').write(s)
        print('%-26s %s' % (fn, ', '.join(notes)))
    else:
        print('%-26s NO CHANGE' % fn)

only = sys.argv[1:] if len(sys.argv) > 1 else None
for fn in sorted(W, key=lambda f: (int(re.match(r'lesson-(\d+)', f).group(1)), f)):
    if only and not any(o in fn for o in only):
        continue
    patch(fn)
