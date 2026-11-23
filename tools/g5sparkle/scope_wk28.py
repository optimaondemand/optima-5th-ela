#!/usr/bin/env python3
"""Week 28 pages brought in line with the scope (v2_poetry scope week 28), approved by Bethany Nov 23 2026
(claude/g5-ela-wk28-scope-check.md). One strand per run, each its own commit:
    python tools/g5sparkle/scope_wk28.py rwm|wgrd|writing|standards [--apply]
Book lines checked against the By the Great Horn Spoon! text (Ch. 10-12). Spelling, grammar and poetry already match.
"""
import io, re, sys
F = {1: 'lesson-28-1-btghs-ch10.html', 2: 'lesson-28-2-btghs-ch11.html', 3: 'lesson-28-3-btghs-ch12.html', 4: 'lesson-28-4-btghs-theme.html',
     'flu': 'lesson-28-fluency.html', 'chk': 'lesson-28-checkin.html'}
READ_NEXT = re.compile(r'(<div class="tab-next-wrap"><p class="tab-transition-voice">[^<]*</p>\s*<button class="tab-next-btn" onclick="markDone\(\'reading\'\);switchTab\(\'assignment\'\)">)')
RWM_CSS = '''
/* Read Like a Writer box (same as weeks 19-27) */
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
def rwm(sentence, ch, writer, tryit, frame):
    fr = '      <div class="rwm-frame">%s</div>\n' % frame if frame else ''
    return ('  <!-- RWM -->\n  <div class="rwm-box">\n'
      '    <div class="rwm-header">&#128214; Read Like a Writer &mdash; Read &bull; Notice &bull; Try</div>\n'
      '    <div class="rwm-sentence">%s <span style="font-size:13px;color:#5A6B8C;">(Chapter %d)</span></div>\n'
      '    <div class="rwm-step"><div class="rwm-step-label">&#128214; As a Reader</div>\n'
      '      <div class="rwm-step-text">What does the character choose to do here? What does that choice show he cares about?</div>\n%s    </div>\n'
      '    <div class="rwm-step"><div class="rwm-step-label">&#9999;&#65039; As a Writer</div>\n'
      '      <div class="rwm-step-text">%s</div>\n%s    </div>\n'
      '    <div class="rwm-step"><div class="rwm-step-label">&#128394;&#65039; Try It</div>\n'
      '      <div class="rwm-step-text">%s</div>\n%s%s    </div>\n'
      '  </div>\n\n') % (sentence, ch, ta('journal-rwm-reader', 'Read Like a Writer: As a Reader', 'He chooses to... It shows he cares about...'), writer,
                        ta('journal-rwm-writer', 'Read Like a Writer: As a Writer', 'I notice...'), tryit, fr, ta('journal-rwm-mimic', 'Read Like a Writer: Try It', 'My sentences...'))
R = {
 1: rwm('&ldquo;I&rsquo;ll thank you to return that picture to my bag,&rdquo; he warned, stamping each word out of cold steel.', 10,
        'This is a <strong>character choice</strong>. All through the robbery Praiseworthy stays calm. He shows his bare hand, he watches his carpetbag dumped in the dirt, and he says nothing. Only the picture of Aunt Arabella makes him speak like this. Fleischman shows what a character values by what he will <em>not</em> give up. That is one way a theme is built.',
        'In 2 sentences, name one choice a character makes in Chapter 10 and what it shows he values. You can use it as evidence in your literary response.', None),
 2: rwm('He forced down another mouthful. He was afraid the miner would take back the name if he didn&rsquo;t drain the can.', 11,
        'Jack <strong>chooses</strong> to keep drinking coffee he can hardly swallow. Fleischman tells us why in the second sentence: Jack wants to keep the name <em>Jamoka Jack</em>. The choice shows what Jack wants most in the diggings: to belong, and to be taken for a real miner.',
        'Use the frame to write about one choice from Chapter 10 or 11.', 'When ___ chose to ___, it showed that ___. Fleischman seems to be saying ___.'),
 3: rwm('Praiseworthy shouldered the pick. He gave up trying to explain. &hellip; If they preferred a tall tale to the facts, let them have it.', 12,
        'Praiseworthy, who cares about getting things exactly right, <strong>chooses</strong> to stop correcting the story. The choice is small, but it shows him changing: the diggings are teaching him to bend. A choice that changes a character is strong evidence for a theme.',
        'Find the place in your literary response where your evidence is weakest. Replace it, or add to it, with one character choice from Chapters 10&ndash;12, and explain what the choice shows.', None),
 4: rwm('Praiseworthy gave Jack a passing wink. As long as the citizens of Hangtown were determined to hang a reputation on him, it might as well be the best.', 12,
        'On your own this time. Name the choice Praiseworthy makes here, say what it shows about him, and say which theme it supports.',
        'Write 2&ndash;3 sentences: one choice from this week&rsquo;s chapters, what it shows, and the theme it supports. Use one transition.', None),
}
CHK_RWM = '<div class="turn-in-item" onclick="toggleCheck(this)"><div class="turn-in-check"></div><div class="turn-in-item-text">I answered the Read Like a Writer box on the Reading tab.</div></div>'
CHKL = '<div class="turn-in-checklist">'


# ---- WGRD lenses
def ol(items):
    return ''.join('<li><strong>%s:</strong> %s</li>\n          ' % it for it in items)
LENS = {
 1: [('Count the cost', 'Note what each event costs a character and what it gains him.'),
     ('Spot the repeat', 'Ask what idea keeps coming back in different events.'),
     ('Collect first', 'Gather events before you name a theme.')],
 2: [('Name both sides', 'For each conflict, name what each side wants.'),
     ('Find the test', 'Ask what the conflict is testing: courage, honesty, loyalty or greed.'),
     ('Catch the change', 'Notice who changes his mind, and what changed it.')],
 3: [('Find the costly choice', 'Find a passage where a character makes a choice that costs him something.'),
     ('Ask what it shows', 'Ask what the choice says about what he values.'),
     ('Ask if the book agrees', 'Then ask whether the book agrees with him.')],
 4: [('Say it in one sentence', 'Write your theme as an idea, not a topic.'),
     ('Test it three times', 'Check it against three events from this week.'),
     ('Fix the wording', 'Revise the words until the theme fits all three.')],
}
OL_RE = re.compile(r'(How to Do It</div>\s*<ol[^>]*>\s*)(?:<li>.*?</li>\s*){3}(</ol>)', re.S)
WATCH = {
 1: ('watch what they are adding up to.</p>', 'watch what they are adding up to. As you read Chapter 10, watch what Praiseworthy hands over calmly, and what he will not.</p>'),
 2: ('where a theme becomes visible.</p>', 'where a theme becomes visible. As you read, watch what Jack is willing to do to be accepted in the diggings.</p>'),
 3: ('are the same thing.</p>', 'are the same thing. As you read, watch what Praiseworthy does when the truth and his welcome pull different ways.</p>'),
 4: ('or do you need to change it?</p>', 'or do you need to change it? Then pull the week together: one choice from Chapter 10, 11 or 12 and the theme it shows.</p>'),
}

# ---- writing
PROG = '  <span class="wp-step">Revise &amp; Publish</span>\n</div>\n'
def stage(text):
    return PROG + '<div class="callout callout-info" style="margin-top:10px;"><span class="callout-icon">&#128204;</span><p>%s</p></div>\n' % text
TITLE = 'Writer&rsquo;s Workshop &middot; Week 28 &middot; LITERARY RESPONSE</div>'
TIPO = '— and supports it with <strong>specific evidence</strong> from the text.</p>'
TIPN = 'and supports it with <strong>specific evidence</strong> from the text. This week the strongest evidence is a <strong>character&rsquo;s choice</strong>: what someone decides to do, and what that shows he values.</p>'
def wr(step, text):
    return [(TITLE, 'Writer&rsquo;s Workshop &middot; Week 28 &middot; LITERARY RESPONSE &middot; %s</div>' % step, 1), (PROG, stage(text), 1), ('TIPFIX', None, 'tip')]
WR = {
 1: wr('Plan', '<strong>Today&rsquo;s step: Plan.</strong> Don&rsquo;t write the whole response yet. In your box, write (1) a one-sentence theme claim and (2) two character choices you have read about so far that could prove it, a few words each. That is your plan.'),
 2: wr('Draft with support', '<strong>Today&rsquo;s step: Draft with support.</strong> Turn your plan into sentences. If you get stuck, use these frames: <em>In By the Great Horn Spoon!, Sid Fleischman shows that ___.</em> &middot; <em>When ___ chose to ___, it showed ___.</em> &middot; <em>Furthermore, ___.</em>'),
 3: wr('Revise', '<strong>Today&rsquo;s step: Revise using a checklist.</strong> Check your response: (1) your claim is an idea, not a topic; (2) you have at least two pieces of evidence, each a character&rsquo;s choice from the book; (3) you explain what each choice shows; (4) a transition with a comma links your ideas; (5) your closing says why it matters. Fix anything missing.'),
 4: wr('Submit', '<strong>Today&rsquo;s step: Submit.</strong> Read your response once more, then put the whole response in the box below. It goes to your teacher with the rest of your work when you copy it into Canvas.'),
}
EE41 = ' &middot; <span class="fl-code">ELA.K12.EE.4.1</span>'
ST = {k: [(EE41, '', 1)] for k in F}

def plan(which):
    P = {}
    if which == 'rwm':
        for d in (1, 2, 3, 4):
            P[d] = [(READ_NEXT, lambda m, d=d: R[d] + m.group(1), 1), (CHKL, CHKL + CHK_RWM, 1), ('</style>', RWM_CSS + '</style>', 'first')]
    elif which == 'wgrd':
        for d in (1, 2, 3, 4): P[d] = [(OL_RE, lambda m, d=d: m.group(1) + ol(LENS[d]) + m.group(2), 1), (WATCH[d][0], WATCH[d][1], 1)]
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
            if n == 'tip':
                c = s.count(TIPO)
                if c != 1: sys.exit('%s: %d x tip' % (f, c))
                s = s.replace(' ' + TIPO, ', ' + TIPN); continue
            if n == 'first':
                if old not in s: sys.exit('%s: no %r' % (f, old))
                s = s.replace(old, new, 1); continue
            if new is None:
                if s.count(old) != n: sys.exit('%s: %d x %r after' % (f, s.count(old), old))
                continue
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
