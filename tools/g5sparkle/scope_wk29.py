#!/usr/bin/env python3
"""Week 29 pages brought in line with the scope (v2_poetry scope week 29), approved by Bethany Nov 23 2026
(claude/g5-ela-wk29-scope-check.md). One strand per run, each its own commit:
    python tools/g5sparkle/scope_wk29.py rwm|poetry|wgrd|writing|standards [--apply]
Book lines checked against the By the Great Horn Spoon! text (Ch. 8-15). Morphology, spelling and grammar already match.
Poem: Stevenson, "Windy Nights", A Child's Garden of Verses (1885), checked word for word on Wikisource."""
import io, re, sys
F = {1: 'lesson-29-1-btghs-ch13.html', 2: 'lesson-29-2-btghs-ch14.html', 3: 'lesson-29-3-btghs-ch15.html', 4: 'lesson-29-4-btghs-voice.html',
     'flu': 'lesson-29-fluency.html', 'chk': 'lesson-29-checkin.html'}
READ_NEXT = re.compile(r'(<div class="tab-next-wrap"><p class="tab-transition-voice">[^<]*</p>\s*<button class="tab-next-btn" onclick="markDone\(\'reading\'\);switchTab\(\'assignment\'\)">)')
RWM_CSS = '''
/* Read Like a Writer box (same as weeks 19-28) */
.rwm-box{background:#FFFFFF;border:2px solid #E2E8F4;border-radius:14px;overflow:hidden;margin:18px 0 14px;}
.rwm-header{background:linear-gradient(135deg,#2C5F2E,#1A2D5A);color:#fff;padding:12px 18px;font-size:14px;font-weight:800;text-transform:uppercase;letter-spacing:.8px;}
.rwm-sentence{background:linear-gradient(135deg,#FFFCF0 0%,#FBF5E6 100%);border-bottom:2px solid #F5E6C8;padding:16px 20px;font-family:'Lora',Georgia,serif;font-size:17px;color:#2C5F2E;line-height:1.7;font-style:italic;}
.rwm-step{padding:14px 20px;border-bottom:1.5px solid #E2E8F4;}
.rwm-step:last-child{border-bottom:none;}
.rwm-step-label{display:flex;align-items:center;gap:8px;font-size:14px;color:#C8A850;font-weight:800;text-transform:uppercase;letter-spacing:.5px;margin-bottom:8px;}
.rwm-step-text{font-size:15px;color:#3A4A6B;line-height:1.6;}
.rwm-frame{background:#FAFBFF;border:1.5px dashed #8B3A20;border-radius:8px;padding:10px 14px;margin-top:8px;font-family:'Lora',Georgia,serif;font-size:15px;color:#8B3A20;font-style:italic;}
'''
def ta(id_, label, ph):
    return ('      <textarea class="journal-box" id="%s" data-label="%s" placeholder="%s" oninput="autoSave(this,\'dot-%s\');"></textarea>\n'
            '      <div class="journal-label">&#128211; <span class="saved-dot" id="dot-%s"></span></div>\n') % (id_, label, ph, id_, id_)
def rwm(sentence, ch, reader, writer, tryit, frame):
    fr = '      <div class="rwm-frame">%s</div>\n' % frame if frame else ''
    return ('  <!-- RWM -->\n  <div class="rwm-box">\n'
      '    <div class="rwm-header">&#128214; Read Like a Writer &mdash; Read &bull; Notice &bull; Try</div>\n'
      '    <div class="rwm-sentence">%s <span style="font-size:13px;color:#5A6B8C;">(Chapter %d)</span></div>\n'
      '    <div class="rwm-step"><div class="rwm-step-label">&#128214; As a Reader</div>\n'
      '      <div class="rwm-step-text">%s</div>\n%s    </div>\n'
      '    <div class="rwm-step"><div class="rwm-step-label">&#9999;&#65039; As a Writer</div>\n'
      '      <div class="rwm-step-text">%s</div>\n%s    </div>\n'
      '    <div class="rwm-step"><div class="rwm-step-label">&#128394;&#65039; Try It</div>\n'
      '      <div class="rwm-step-text">%s</div>\n%s%s    </div>\n'
      '  </div>\n\n') % (sentence, ch, reader, ta('journal-rwm-reader', 'Read Like a Writer: As a Reader', 'I notice...'), writer,
                        ta('journal-rwm-writer', 'Read Like a Writer: As a Writer', 'The writer...'), tryit, fr, ta('journal-rwm-mimic', 'Read Like a Writer: Try It', 'My sentences...'))
R = {
 1: rwm('The truth of the matter was that Praiseworthy himself began to enjoy his notoriety.', 13,
        'Who seems to be telling you this, and how does the teller feel about Praiseworthy?',
        'This is <strong>voice</strong>. The narrator sounds like a storyteller letting you in on a secret: <em>The truth of the matter was&hellip;</em> He could have written &ldquo;Praiseworthy liked being famous.&rdquo; Instead he uses a big word, <em>notoriety</em>, with a wink. Fancy words used for fun are part of Fleischman&rsquo;s voice.',
        'Find one sentence in your adventure draft that sounds flat. Rewrite it so it sounds like a storyteller is telling it. You can use it in your Workshop plan.', None),
 2: rwm('&ldquo;Stubb&rsquo;s a proud animal,&rdquo; the man had said when they bought him. &ldquo;Sometimes he thinks he&rsquo;s a mule.&rdquo;', 14,
        'What does the way the man talks tell you about him?',
        'This is <strong>dialogue</strong>. The man talks like a real person in the diggings: short, plain and a little funny. He doesn&rsquo;t say &ldquo;This animal is stubborn and believes he is better than other burros.&rdquo; Good dialogue sounds like the person talking, not like the author.',
        'Use the frame to rewrite one line of dialogue from your adventure draft so it sounds like your character.', 'Instead of saying ___, my character would say, &ldquo;___.&rdquo;'),
 3: rwm('Yellow poppies had burst open on the hillsides like scatterings of fools&rsquo; gold.', 15,
        'What picture do you see? Which words make it?',
        'This is <strong>description</strong>. Fleischman names a real flower (<em>poppies</em>) and a real place (<em>the hillsides</em>), then compares them to something from the gold fields (<em>fools&rsquo; gold</em>). The comparison fits the world of the story.',
        'Find one vague detail in your adventure draft. Replace it with a specific one that fits your story&rsquo;s world, the way Fleischman&rsquo;s poppies fit his. Write the new sentence.', None),
 4: rwm('Pay dirt eluded them &mdash; but the next bend in the river might make their fortune.', 15,
        'How does this sentence make you feel about the partners&rsquo; luck?',
        'On your own this time. What makes this sentence sound like Fleischman? Think about the word <em>eluded</em>, the dash, and how the sentence ends.',
        'Write 2&ndash;3 sentences: name one thing that makes this sentence sound like Fleischman, then write one sentence for your adventure that uses the same move.', None),
}
CHK_RWM = '<div class="turn-in-item" onclick="toggleCheck(this)"><div class="turn-in-check"></div><div class="turn-in-item-text">I answered the Read Like a Writer box on the Reading tab.</div></div>'
CHKL = '<div class="turn-in-checklist">'

# ---- poetry (Day 2 poem swap; Day 4 contrast line)
OLD_LINES = re.compile(r'<div class="poetry-title">&ldquo;From a Railway Carriage&rdquo;</div>.*?</div>\s*</div>\s*<div class="callout callout-tip"><span class="callout-icon">💡</span><p>Five elements.*?</p></div>', re.S)
NEW_LINES = '''<div class="poetry-title">&ldquo;Windy Nights&rdquo;</div>
        <div class="poetry-author">Robert Louis Stevenson, <em>A Child&rsquo;s Garden of Verses</em>, 1885 &mdash; public domain</div>
        <div class="poetry-lines">
          Whenever the moon and stars are set,<br>
          Whenever the wind is high,<br>
          All night long in the dark and wet,<br>
          A man goes riding by.<br>
          Late in the night when the fires are out,<br>
          Why does he gallop and gallop about?<br>
          <br>
          Whenever the trees are crying aloud,<br>
          And ships are tossed at sea,<br>
          By, on the highway, low and loud,<br>
          By at the gallop goes he.<br>
          By at the gallop he goes, and then<br>
          By he comes back at the gallop again.<br>
        </div>
      </div>
      <div class="callout callout-tip"><span class="callout-icon">💡</span><p>Five elements are all working at once here. <strong>Form:</strong> two stanzas of six lines; the first asks a question, the second answers with the rider going by. <strong>Rhyme:</strong> pairs that chime, like <em>set/wet</em>, <em>out/about</em>, <em>then/again</em>. <strong>Meter:</strong> a quick, bouncing beat, like hooves. <strong>Line breaks:</strong> short lines that come in a rush, with <em>By</em> starting line after line. <strong>Figurative language:</strong> trees &ldquo;crying aloud&rdquo; (personification), and a rider who might be the wind itself.</p></div>'''
POETRY = {2: [(OLD_LINES, NEW_LINES, 1)],
          4: [('produce a galloping train in one poem and a silent cat in the other.', 'produce a galloping rider in one poem and a silent cat in the other.', 1)]}

# ---- WGRD lenses
def ol(items):
    return ''.join('<li><strong>%s:</strong> %s</li>\n          ' % it for it in items)
LENS = {
 1: [('Mark a sentence', 'Mark a sentence that could only come from this book, and ask what makes it so.'),
     ('Notice the word', 'Notice a word Fleischman chose when a plainer one was there.'),
     ('Hear the rhythm', 'Listen for where the sentences turn short, and ask why there.')],
 2: [('Find the tone words', 'In one passage, find the words that carry the tone.'),
     ('Swap one', 'Swap one for a plainer word and reread. What is lost?'),
     ('Ask why', 'Ask why the author made that choice.')],
 3: [('Find the danger', 'Find the most dangerous moment in the chapter.'),
     ('Hear the telling', 'Reread it. Does the narrator sound alarmed, or calm?'),
     ('Feel the gap', 'Ask what the gap between the danger and the calm telling does to you.')],
 4: [('Name three features', 'Name three things about the voice, with an example for each.'),
     ('Ask what it allows', 'Ask what this voice lets Fleischman do in a hard story.'),
     ('Ask what it costs', 'Ask what this voice makes harder to say.')],
}
OL_RE = re.compile(r'(How to Do It</div>\s*<ol[^>]*>\s*)(?:<li>.*?</li>\s*){3}(</ol>)', re.S)
WATCH = {
 1: ('deadpan treatment as anything else.</p>', 'deadpan treatment as anything else. As you read Chapter 13, watch for one sentence that sounds like nobody but this narrator.</p>'),
 2: ('Voice is not an accident; it is a stack of decisions.</p>', 'Voice is not an accident; it is a stack of decisions. As you read Chapter 14, watch the words Fleischman picks for Stubb.</p>'),
 3: ('Today <strong>reread</strong> a moment of real danger &mdash; a grizzly, a coyote hole, a genuine emergency &mdash; and watch the voice stay steady. That steadiness is a choice, and it is the most distinctive thing about how this book sounds.</p>',
     'Today <strong>reread</strong> the most dangerous moment in Chapter 15 and watch the voice stay steady. That steadiness is a choice, and it is a big part of how this book sounds. Watch whether the narrator ever sounds scared.</p>'),
 4: ('what does this voice let Fleischman do that a different one could not?</p>', 'what does this voice let Fleischman do that a different one could not? Pull the week together: one sentence from Chapter 13, 14 or 15 that shows the voice best.</p>'),
}
Q3FIX = (3, 'Reread the grizzly passage. How would it feel if the narrator sounded frightened? What is gained by the calm?',
         'Reread the most dangerous moment. How would it feel if the narrator sounded frightened? What is gained by the calm?')
def one_question(s):
    i = s.find('How to Do It</div>'); j = s.find('class="socratic-box"', i)
    a = s.find('<p class="socratic-q">', j); b = s.find('</p>', a) + 4
    c = s.find('<p class="socratic-q">', b); d = s.find('</p>', c) + 4
    if min(i, j, a, c) < 0 or s.find('</div>', b) < c: sys.exit('no second question')
    return s[:b] + s[d:]

# ---- writing
PROG = '      <span class="wp-step active">⭐ Revise</span>\n    </div>\n'
def stage(text):
    return PROG + '    <div class="callout callout-info" style="margin-top:10px;"><span class="callout-icon">&#128204;</span><p>%s</p></div>\n' % text
TITLE = 'Writer&rsquo;s Workshop &middot; Week 29 &middot; REVISE</div>'
OLDBOX = 'textbox-prompt">Choose one paragraph from your draft and revise it for voice, dialogue, or description. Write both the original and the revised version.'
def wr(step, text, box):
    return [(TITLE, 'Writer&rsquo;s Workshop &middot; Week 29 &middot; REVISE &middot; %s</div>' % step, 1), (PROG, stage(text), 1), (OLDBOX, 'textbox-prompt">' + box, 1)]
WR = {
 1: wr('Plan', '<strong>Today&rsquo;s step: Plan.</strong> Don&rsquo;t rewrite yet. Pick one paragraph from your adventure draft and copy it into the box. Under it, list three spots to change: one place where the voice sounds flat, one line of dialogue, and one vague detail.',
       'Plan: copy the paragraph you will revise, then list your three spots to change (voice, dialogue, description).')
    + [('placeholder="ORIGINAL:&#10;[paste your original paragraph here]&#10;&#10;REVISED:&#10;[write your improved version here]"',
        'placeholder="MY PARAGRAPH:&#10;[paste the paragraph here]&#10;&#10;THREE SPOTS TO CHANGE:&#10;1. Voice:&#10;2. Dialogue:&#10;3. Description:"', 1)],
 2: wr('Draft with support', '<strong>Today&rsquo;s step: Draft with support.</strong> Rewrite your paragraph, starting with the dialogue. If you get stuck, use these frames: <em>Instead of saying ___, my character would say, &ldquo;___.&rdquo;</em> &middot; <em>Not just ___, but ___.</em> (for a specific detail)',
       'Draft: write your original paragraph, then your rewritten version with better dialogue.'),
 3: wr('Revise', '<strong>Today&rsquo;s step: Revise using a checklist.</strong> Check your paragraph: (1) it sounds like a storyteller, not a list of facts; (2) every line of dialogue sounds like the person saying it; (3) at least one detail is specific (a name, a color, a sound); (4) one short sentence lands a key moment; (5) the sentences start in different ways. Fix anything missing.',
       'Revise: write your paragraph again after checking it against the five checklist points.'),
 4: wr('Submit', '<strong>Today&rsquo;s step: Submit.</strong> Read your paragraph out loud once more. Put the final version in the box below with one sentence about your biggest change. It goes to your teacher when you copy your work into Canvas.',
       'Submit: your final revised paragraph, then one sentence about the biggest change you made.'),
}
R14 = '<span class="fl-code">ELA.5.R.1.4</span>'
ST = {k: [(R14, R14 + ' &middot; <span class="fl-code">ELA.5.R.3.1</span>', 1)] for k in F}

def plan(which):
    P = {}
    if which == 'rwm':
        for d in (1, 2, 3, 4):
            P[d] = [(READ_NEXT, lambda m, d=d: R[d] + m.group(1), 1), (CHKL, CHKL + CHK_RWM, 1), ('</style>', RWM_CSS + '</style>', 'first')]
    elif which == 'poetry': P = POETRY
    elif which == 'wgrd':
        for d in (1, 2, 3, 4):
            P[d] = [(OL_RE, lambda m, d=d: m.group(1) + ol(LENS[d]) + m.group(2), 1), (WATCH[d][0], WATCH[d][1], 1), (None, None, 'oneq')]
        P[3].append((Q3FIX[1], Q3FIX[2], 1))
    elif which == 'writing': P = WR
    elif which == 'standards': P = ST
    else: sys.exit('strand?')
    return P
def main():
    which = sys.argv[1]; apply = '--apply' in sys.argv
    out = {}
    for k, reps in plan(which).items():
        f = F[k]; s0 = io.open(f, encoding='utf-8', newline='').read(); s = s0
        for old, new, n in reps:
            if n == 'oneq': s = one_question(s); continue
            if n == 'first':
                if old not in s: sys.exit('%s: no %r' % (f, old))
                s = s.replace(old, new, 1); continue
            if isinstance(old, str):
                c = s.count(old)
                if c != n: sys.exit('%s: %d x %r' % (f, c, old[:70]))
                s = s.replace(old, new)
            else:
                s, c = old.subn(new, s)
                if c != n: sys.exit('%s: %d x re %r' % (f, c, old.pattern[:60]))
        if s.count('<div') - s.count('</div>') != s0.count('<div') - s0.count('</div>'): sys.exit('div balance ' + f)
        out[f] = s; print(which, 'ok', f)
    if apply:
        for f, s in out.items(): io.open(f, 'w', encoding='utf-8', newline='').write(s)
        print('written')
main()
