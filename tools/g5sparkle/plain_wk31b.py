#!/usr/bin/env python3
"""Week 31 plain-language pass, round 2 (long-step trim from the Playwright Next-only walk; aim about 110 words a step).
Wording and folds only; no graded item, answer or key changes. Primary-source steps stay long on purpose.
- What Good Readers Do intros cut to two sentences, the last one naming what to watch for (skill 8f.4)
- the grammar spiral list folded on Days 2 and 4, the cumulative spelling list folded on Days 2 and 3 ("from Day 1")
- Read Like a Writer Day 1 model trimmed to two categories; the Day 3 example paragraph shortened; the 31.2 how-to-read box and background card shortened
- the game's 'What am I looking at?' text shortened (DATA, both places, via setdata.py)
- 31.4: 'Peer Review' left in the tab, banner, objective, video title and footer now says Reviewer's Eyes / Review (the <title> stays: it is the save key)"""
import io, re, sys, json, subprocess
F = {1: 'lesson-31-1-comparison-plan.html', 2: 'lesson-31-2-comparison-sources.html', 3: 'lesson-31-3-comparison-draft.html', 4: 'lesson-31-4-comparison-submit.html'}
INTRO = re.compile(r'(What Good Readers Do</div><div class="activity-sub">[^<]*</div></div></div>\s*<div class="activity-body">\s*<p>).*?(</p>)', re.S)
NEW_INTRO = {1: 'This week you read across all five novels. Watch for where two books treat the same theme differently.',
             2: 'A primary source was made by someone who was there; a novel was imagined later. Watch for what your source shows that your novel cannot.',
             3: 'Today reread with your claim in hand. Watch for the one passage that does not fit it.',
             4: 'Read your own essay as if someone else wrote it. Watch for the places that need reasoning more than evidence.'}
def fold(label, summary):
    return (re.compile(r'(<div class="key-concept[^>]*><div class="key-concept-label">' + re.escape(label) + r'</div>)(.*?)(</div>\s*<div class="swyk)', re.S),
            lambda m: m.group(1) + '<details><summary style="cursor:pointer;font-weight:700;color:#3D5285;">' + summary + '</summary>' + m.group(2) + '</details>' + m.group(3), 1)
SPIRAL = fold('📌 Grammar Spiral Review — All Year', 'The year&rsquo;s grammar tools, from Day 1. Open it if you need it.')
SPELL = fold('📌 Cumulative Spelling — All Units', 'The year&rsquo;s spelling list, from Day 1. Open it if you need it.')
REP = {
 1: [(INTRO, lambda m: m.group(1) + NEW_INTRO[1] + m.group(2), 1),
     ('Both Kit Tyler and Jack Flagg leave home for a strange new place. <strong>How they arrive:</strong> Kit sails to Connecticut after her grandfather dies, while Jack hides in a potato barrel because he chose to go. <strong>Who helps them:</strong>',
      'Both Kit Tyler and Jack Flagg leave home for a strange new place. <strong>Who helps them:</strong>', 1),
     ('Find the three categories in bold.', 'Find the two categories in bold.', 1)],
 2: [(INTRO, lambda m: m.group(1) + NEW_INTRO[2] + m.group(2), 1), SPIRAL, SPELL,
     ('<p><strong>2. Quote precisely:</strong> Find one phrase that could strengthen your argument. Copy it exactly.</p>', '<p><strong>2. Quote precisely:</strong> Copy one short phrase exactly.</p>', 1),
     ('<p><strong>3. Explain the connection:</strong> Don&rsquo;t just quote — explain <em>why</em> this evidence matters for your theme.</p>', '<p><strong>3. Explain:</strong> Say <em>why</em> it matters for your theme.</p>', 1),
     ('<p>A novel can show you a made-up character&rsquo;s thoughts. A <strong>primary source</strong> is something made at the time by someone who was there: a diary, a letter, a newspaper report. It cannot show you a character&rsquo;s thoughts, but it shows you what one real person saw and believed.</p>',
      '<p>A <strong>primary source</strong> is made at the time by someone who was there, like a diary, a letter or a news report.</p>', 1)],
 3: [(INTRO, lambda m: m.group(1) + NEW_INTRO[3] + m.group(2), 1), SPELL,
     ('However, Kit&rsquo;s courage is inward — she endures suspicion and isolation without public announcement, while Praiseworthy&rsquo;s courage is quietly outward — each calm action performed in full view of others who notice exactly what he is doing. ',
      'However, Kit&rsquo;s courage is quiet and hidden, while Praiseworthy&rsquo;s is calm and in plain view. ', 1)],
 4: [(INTRO, lambda m: m.group(1) + NEW_INTRO[4] + m.group(2), 1), SPIRAL,
     ('font-weight="700">Peer Review &amp; Revision</text>', 'font-weight="700">Review &amp; Revision</text>', 1),
     ('<div class="info-value">Peer Review &amp; Revision</div>', '<div class="info-value">Review &amp; Revision</div>', 'opt'),
     ('👥 Peer Review<span class="tab-check">', '👥 Reviewer&rsquo;s Eyes<span class="tab-check">', 1),
     ('<strong>Peer Review:</strong> I will review my own essay', '<strong>Reviewer&rsquo;s Eyes:</strong> I will review my own essay', 1),
     ('Week 31 Day 4: Peer Review &amp; Submit', 'Week 31 Day 4: Review &amp; Submit', 2),
     ('Peer Review & Final Submission</span>', 'Review & Final Submission</span>', 1),
     ('Day 4: Peer Review &amp; Submission</div>', 'Day 4: Review &amp; Submission</div>', 1)],
}
apply = '--apply' in sys.argv
for k, reps in REP.items():
    f = F[k]; s0 = io.open(f, encoding='utf-8', newline='').read(); s = s0
    for old, new, n in reps:
        if n == 'opt':
            s = s.replace(old, new); continue
        if isinstance(old, str):
            c = s.count(old)
            if c != n: sys.exit('%s: %d x %r' % (f, c, old[:70]))
            s = s.replace(old, new)
        else:
            s, c = old.subn(new, s)
            if c != n: sys.exit('%s: %d x re %r' % (f, c, old.pattern[:60]))
    if s.count('<div') - s.count('</div>') != s0.count('<div') - s0.count('</div>'): sys.exit('div ' + f)
    print('ok', f, 'Peer Review left (outside <title>):', len(re.findall('Peer Review', re.sub(r'<title>.*?</title>', '', s))))
    if apply: io.open(f, 'w', encoding='utf-8', newline='').write(s)
LOOK = "Five novels and one more book on the shelf: You. Two words with the same root are a pair. Each pair you find ties two worlds together with a gold thread."
if apply:
    t = io.open('tools/g5sparkle/data_wk31.py', encoding='utf-8').read()
    t = re.sub(r'LOOK = \(.*?\)\n', 'LOOK = %r\n' % LOOK, t, count=1, flags=re.S)
    io.open('tools/g5sparkle/data_wk31.py', 'w', encoding='utf-8').write(t)
    for d in (1, 2, 3, 4):
        g = json.load(io.open('data/g5ela-31-%d.json' % d, encoding='utf-8'))['game']; g['look'] = LOOK
        json.dump({'game': g}, io.open('planning docs/_pv/w31/pg%d.json' % d, 'w', encoding='utf-8'), ensure_ascii=False)
        subprocess.check_call([sys.executable, 'tools/g5sparkle/setdata.py', F[d], 'data/g5ela-31-%d.json' % d, 'planning docs/_pv/w31/pg%d.json' % d, '--apply'])
    print('written')
