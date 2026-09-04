# -*- coding: utf-8 -*-
"""Pass 1: realign WGRD + RWM in Witch weeks 4-5 to the v2_poetry scope & sequence."""
import re, os, shutil, sys

D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

KC_OPEN = ('<div class="key-concept" style="background:#F0F7FF;border-color:#C8DCEE;margin:10px 0;">\n'
           '<div class="key-concept-label" style="color:#3D5285;">\U0001F50D How to Do It</div>\n'
           '<ol style="margin:6px 0 6px 20px;font-size:14px;color:#3A4A6B;line-height:1.8;">\n')
KC_CLOSE = '</ol>\n</div>\n'

THEME_KC = KC_OPEN + (
 "<li><strong>Find the repeated idea:</strong> Notice which big ideas keep coming back — in different chapters, "
 "through different characters, in situations that look nothing alike.</li>\n"
 "<li><strong>Track how it deepens:</strong> Ask what each new appearance adds. A theme develops; it does not simply repeat.</li>\n"
 "<li><strong>Say it as a sentence:</strong> State the theme as a full sentence about people, not a single word. "
 "&ldquo;Freedom&rdquo; is a topic; &ldquo;freedom is worth nothing if you have to become someone else to keep it&rdquo; is a theme.</li>\n"
) + KC_CLOSE

SYNTH_KC = KC_OPEN + (
 "<li><strong>Trace the plot:</strong> Lay the events end to end. What actually happened to Kit, in order, from Saybrook harbour to this chapter?</li>\n"
 "<li><strong>Name the conflicts:</strong> Which clashes changed her — with the town, with Matthew, with William, with herself?</li>\n"
 "<li><strong>Describe the character:</strong> Say what she can do now that she could not do in Chapter 1, and what it cost her to learn it.</li>\n"
 "<li><strong>State the theme:</strong> Put the three together in one sentence. The theme is what the plot, the conflicts and the change add up to.</li>\n"
) + KC_CLOSE

# ---------------------------------------------------------------- WGRD content
WGRD = {
 'lesson-4-1-witch-ch14.html': ('Set your reading lens', [
   "Good readers notice how an author <strong>develops perspective</strong> — the particular angle a character "
   "sees the world from. Perspective is not the same as opinion. It is built out of what a character has lived "
   "through, what they are afraid of, and what they want, and it decides what they notice in the first place.",
   "Chapter 14 hands you the same autumn through several sets of eyes. Kit sees the maples burning red and thinks "
   "of the sea. Judith sees a house going up. Matthew sees a colony about to lose its charter. The narrator lets "
   "you stand behind each of them in turn. Ask yourself:"], None),
 'lesson-4-2-witch-ch15.html': ('Read closely for perspective', [
   "Today the whole chapter is one argument heard four ways. Behind the closed door the men shout about the "
   "charter. In the outer room Rachel worries about supper, Judith about Thanksgiving, and Kit about why William "
   "was let in. None of them is wrong — they are standing in different places. Read closely and gather "
   "evidence of who sees what, and why."], None),
 'lesson-4-3-witch-ch16.html': ('Reread for perspective — the town stocks', [
   "Today you reread one scene: Kit at the town stocks. Notice how much of what you know arrives from the "
   "narrator rather than from anyone speaking. The narrator tells you about the hard little lump of dread "
   "crowding Kit&rsquo;s ribs, and about the smug set of Judith&rsquo;s lips — neither girl says either "
   "thing aloud. Reread the passage and separate what the narrator hands you from what the characters reveal "
   "themselves."], None),
 'lesson-4-4-witch-ch17.html': ('Synthesise the week — whose eyes?', [
   "Now put the week together. Across Chapters 14–17 Speare has moved you from Kit&rsquo;s doorway to "
   "Matthew&rsquo;s company room to the crowd at the stocks to Mercy&rsquo;s sickbed. Chapter 17 is the hardest "
   "test of it: Matthew will not send for Dr. Bulkeley, and you can see exactly why he refuses and exactly why "
   "Rachel begs him to bend. Both are consistent with who they are. Synthesise what you have learned about how "
   "an author builds a perspective — and makes a reader hold two of them at once."], None),
 'lesson-5-1-witch-ch18.html': ('Set your reading lens', [
   "Good readers watch a <strong>theme develop</strong> across chapters. A theme is never announced; it is built. "
   "The author returns to the same big idea again and again, in different situations, until the pattern becomes "
   "visible.",
   "Watch one idea in particular from here to the end of the book: what freedom actually costs. In Chapter 18 Kit "
   "wakes grateful and resolved, and hours later she is locked in the constable&rsquo;s shed — the first "
   "locked door of her life. Ask yourself:"], THEME_KC),
 'lesson-5-2-witch-ch19.html': ('Read closely for the theme', [
   "Chapter 19 is the trial. Read closely and gather evidence, because this chapter puts the week&rsquo;s idea "
   "under more pressure than it has faced yet: what does it cost to tell the truth in front of people who do not "
   "want to hear it? Watch Prudence, who has the least power of anyone in that room and the most to lose. Watch "
   "Adam Cruff change his mind in public. Watch Nat come back to a town that has banished him."], THEME_KC),
 'lesson-5-3-witch-ch20.html': ('Reread for how the theme deepens', [
   "Today reread the passage in Chapter 20 where Kit tells William it is no use. Nothing forces her to do it "
   "— the trial is over, she is safe, and marrying William would settle her future for good. Reread it and "
   "ask what this scene <em>adds</em> to the idea you have been tracking all week. This is where the theme stops "
   "being about surviving other people&rsquo;s judgement and becomes about refusing to lie about who you are."], THEME_KC),
 'lesson-5-4-witch-ch21.html': ('Synthesise the novel — plot, conflict, character, theme', [
   "Now put the whole novel together. Kit arrived by leaping off the Dolphin into Saybrook harbour with silk "
   "dresses and no idea what she was walking into; she ends by choosing to stay. Today you synthesise all four "
   "threads at once — the plot that carried her here, the conflicts that changed her, the person she has "
   "become, and the theme those things together have built."], SYNTH_KC),
}

# ---------------------------------------------------------------- RWM content
def step(label, text, prompt, jid, jlabel, placeholder, frame=None):
    out  = '    <div class="rwm-step">\n'
    out += '      <div class="rwm-step-label">%s</div>\n' % label
    out += '      <div class="rwm-step-text">%s</div>\n' % text
    if frame:
        out += '      <div class="rwm-frame">%s</div>\n' % frame
    out += '      <div class="textbox-prompt">%s</div>\n' % prompt
    out += '      <div class="journal-label">\U0001F4D3 Your response <span class="saved-dot" id="dot-%s"></span></div>\n' % jid
    out += ('      <textarea class="journal-box" id="journal-%s" data-label="%s" placeholder="%s" '
            'oninput="autoSave(this,\'dot-%s\');gatherAnswers();"></textarea>\n') % (jid, jlabel, placeholder, jid)
    out += '    </div>\n'
    return out

L_READER = '&#x1F4D6; Read like a Reader'
L_WRITER = '&#x270F;&#xFE0F; Read like a Writer'
L_MIMIC  = '&#x1F58A;&#xFE0F; Mimic'

def rwm_box(sentence, reader, rprompt, writer, wprompt, mimic, mprompt, frame=None):
    out  = '<div class="rwm-box">\n'
    out += '    <div class="rwm-header">RWM &mdash; Read like a Reader, Read like a Writer, Mimic</div>\n'
    disp = sentence if sentence.lstrip().startswith('&ldquo;') else '&ldquo;%s&rdquo;' % sentence
    out += '    <div class="rwm-sentence">%s</div>\n' % disp
    out += step(L_READER, reader, rprompt, 'rwm-reader', 'RWM — Read like a Reader', 'This sentence shows...')
    out += step(L_WRITER, writer, wprompt, 'rwm-writer', 'RWM — Read like a Writer', 'The author built it by...')
    out += step(L_MIMIC,  mimic,  mprompt, 'rwm-mimic',  'RWM — Mimic', 'Write your sentence here...', frame)
    out += '  '
    return out

RWM = {
 'lesson-4-2-witch-ch15.html': rwm_box(
   "&ldquo;Oh, I don&rsquo;t think there&rsquo;ll be any fighting,&rdquo; said Judith confidently.",
   "Judith is answering Kit in the chilly upstairs chamber, after an hour of angry men shouting behind a closed "
   "door. Read her words on their own and she sounds calm and reasonable. But you have heard what she was not "
   "listening to. What does her confidence tell you about the world Judith lives inside?",
   "Write 1–2 sentences explaining what the narrator lets you know that Judith does not.",
   "Look at what Speare put <em>outside</em> the quotation marks. Judith&rsquo;s own words stop at the comma; "
   "then the narrator adds two words of her own — <em>said Judith confidently</em>. That adverb is not "
   "Judith&rsquo;s. It is the narrator&rsquo;s judgement of Judith, handed to you in the same breath as her "
   "speech. Notice the punctuation that makes it possible: the comma sits <em>inside</em> the closing quotation "
   "mark, then the tag, then the period.",
   "Write 1 sentence explaining what the narrator&rsquo;s tag adds that the dialogue alone could not.",
   "Write one line of dialogue that someone in Chapter 15 could have said — Kit, Rachel, Matthew or Judith "
   "— then add a narrator&rsquo;s tag with an adverb that tells the reader how to hear it. Punctuate it "
   "exactly the way Speare does.",
   "Write your own sentence using the same technique.",
   frame="&ldquo;___,&rdquo; said [character] [adverb]."),

 'lesson-4-3-witch-ch16.html': rwm_box(
   "Kit had no doubt at all who one at least of the culprits in the stocks would be, and neither, by the smug "
   "set of her pretty lips, had Judith.",
   "Neither girl has said a word. Kit has not admitted she knows Nat is in the stocks; Judith has not said she "
   "knows it too. Yet by the end of this one sentence you know both things. Where did each piece of knowledge "
   "come from?",
   "Write 1–2 sentences explaining how you know what each girl is thinking.",
   "Speare reaches the two girls in completely different ways inside a single sentence. For Kit she goes straight "
   "inside — <em>had no doubt at all</em> — because a narrator can do that. For Judith she has to stay "
   "outside and read a face: <em>by the smug set of her pretty lips</em>. That is the difference between narrator "
   "information and character perspective, built into the grammar of one sentence.",
   "Write 1 sentence naming the two different ways Speare reveals what each girl knows.",
   "Write one sentence that reveals what two people are thinking — one from the inside, in plain narration, "
   "and the other from the outside, through something a reader could actually see: a face, a gesture, a hand. No "
   "frame this time. You have the pattern.",
   "Write your own sentence using the same technique."),

 'lesson-5-2-witch-ch19.html': rwm_box(
   "In the warm rush of pride that welled up in her, Kit forgot her fear.",
   "Prudence has just read aloud, in front of the whole room, the thing everyone insisted she could never do. Kit "
   "is on trial for witchcraft. And in this sentence her fear simply goes. What does that tell you about what "
   "fear had been holding in place?",
   "Write 1–2 sentences explaining what this moment shows about courage.",
   "The sentence is built so that one thing pushes out another. It opens with an introductory phrase — "
   "<em>In the warm rush of pride that welled up in her</em> — set off by a comma, so the pride arrives "
   "first and fills the whole opening. Only then does the main clause land: <em>Kit forgot her fear</em>. Speare "
   "never writes that courage is what happens when something matters more than fear. The shape of the sentence "
   "says it for her.",
   "Write 1 sentence explaining how the order of the two parts creates the meaning.",
   "Write one sentence in that shape about a moment from Chapter 19. Open with an introductory phrase naming a "
   "feeling, put a comma after it, then finish with what that feeling pushed out. Your sentence should mean more "
   "than the event it reports.",
   "Write your own sentence using the same technique.",
   frame="In the ___ of ___, [character] forgot ___."),

 'lesson-5-3-witch-ch20.html': rwm_box(
   "In some contradictory way grief seemed to have etched on Mercy&rsquo;s thin face a beauty it had never "
   "possessed.",
   "John Holbrook has been taken captive and Mercy cannot cry about it. Nobody in the house says her grief has "
   "made her beautiful — Kit notices it. What is Speare telling you about Mercy that the events on their own "
   "would not?",
   "Write 1–2 sentences explaining what this sentence shows about Mercy.",
   "Two craft moves are doing the work. The sentence opens with an introductory phrase — <em>In some "
   "contradictory way</em> — which warns you before you begin that what follows should not fit together. "
   "Then it hands you a verb borrowed from metalwork: grief <em>etched</em> her face. Nothing there is literally "
   "true. That is how a sentence carries an idea past the event it reports. Notice too that Speare takes no comma "
   "after the opening phrase — it is short enough to carry without one. Compare it with yesterday&rsquo;s "
   "sentence, where the longer opening phrase needed one.",
   "Write 1 sentence explaining how the word <em>etched</em> changes what the sentence means.",
   "Write one sentence about a character in Chapter 20 that means more than it says. Open with a short "
   "introductory phrase, and choose one verb that is not literally true. Decide for yourself whether your phrase "
   "needs a comma.",
   "Write your own sentence using the same technique."),
}

# ---------------------------------------------------------------- apply
def patch(fn):
    p = os.path.join(D, fn)
    s = open(p, encoding='utf-8').read()
    orig = s

    # --- WGRD
    sub, paras, kc = WGRD[fn]
    m = re.search(r'<div class="activity-title">[^<]*What Good Readers Do[^<]*</div>\s*'
                  r'<div class="activity-sub">(.*?)</div>', s)
    if not m:
        raise SystemExit('%s: no WGRD head' % fn)
    s = s[:m.start(1)] + sub + s[m.end(1):]

    b = s.find('<div class="activity-body">', m.start())
    bodystart = b + len('<div class="activity-body">')
    nxt = min(x for x in [s.find('<div class="key-concept"', bodystart),
                          s.find('<div class="socratic-box"', bodystart)] if x > 0)
    new = '\n' + ''.join('      <p>%s</p>\n' % x for x in paras)
    if kc:
        new += kc
    else:
        new += '      '
    s = s[:bodystart] + new + s[nxt:]

    # --- RWM
    if fn in RWM:
        i = s.find('<div class="rwm-box">')
        if i < 0:
            raise SystemExit('%s: no rwm-box' % fn)
        j = s.find('</div>', s.rfind('</div>', i, s.find('<div class="tab-next-wrap">', i)))
        end = s.find('<div class="tab-next-wrap">', i)
        # rwm-box ends at the last </div> before tab-next-wrap
        k = s.rfind('</div>', i, end)
        s = s[:i] + RWM[fn] + s[k:]

    if s != orig:
        shutil.copy2(p, p + '.bak')
        open(p, 'w', encoding='utf-8').write(s)
        print('patched', fn)
    else:
        print('NO CHANGE', fn)

for fn in WGRD:
    patch(fn)
