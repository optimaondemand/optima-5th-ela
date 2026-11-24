#!/usr/bin/env python3
"""Week 32 accuracy fixes (approved by Bethany Nov 24 2026; audit claude/g5-ela-wk32-audit.md).
A: the year map and year review name all five novels with their real weeks (How I Became a Ghost back), book claims
   rewritten from checked facts, dates fixed, vocabulary groups only hold words taught this year (covenant was never taught;
   reconcile and beneficial were never taught, so the spelling list uses prospector and benefactor from week 29).
B: example sentences: the Choctaw walk west, not north; no two of the five novels were 'written a century apart'.
C: page fixes: teacher notes say what this week is, 'memorise', 'The sheet gives Week 32...' lines, spelling/grammar numbering.
Every replacement asserts its count; div balance must not change; nothing is written unless every file passes.
    python tools/g5sparkle/fix_wk32.py [--apply]"""
import io, re, sys
F = {1: 'lesson-32-1-portfolio-plan.html', 2: 'lesson-32-2-fluency-draft.html', 3: 'lesson-32-3-final-prep.html', 4: 'lesson-32-4-final-present.html'}
def stop(icon, color, wk, title, cls='umap-done'):
    return ('<div class="umap-stop %s"><div class="umap-circle" style="background:%s;border-color:%s;">%s</div><div class="umap-label">%s</div>'
            '<div class="umap-sub" style="max-width:60px;white-space:normal;text-align:center;line-height:1.2;font-size:9px;">%s</div></div>') % (cls, color, color, icon, wk, title)
CON = '<div class="umap-connector"></div>'
JOURNEY = CON.join([stop('📜', '#7B5EA7', 'Wks 1–5', 'The Witch of Blackbird Pond'), stop('🎨', '#C0392B', 'Wks 6–8', 'Johnny Tremain'),
                    stop('🧭', '#1565C0', 'Wks 9–14', 'Carry On, Mr. Bowditch'), stop('✍️', '#2E7D32', 'Wks 15–17', 'Writer&rsquo;s Workshop'),
                    stop('🐕', '#5D4037', 'Wks 18–24', 'How I Became a Ghost'), stop('⛏️', '#C8862A', 'Wks 25–30', 'By the Great Horn Spoon!'),
                    stop('🔍', '#00695C', 'Wk 31', 'The Comparison'), stop('✉️', '#B8860B', 'Wk 32', 'Letter to a Future 5th Grader', 'umap-active')])
UMAP = (re.compile(r'<div class="umap-row">(?:<div class="umap-connector"></div>|<div class="umap-stop[^"]*"><div class="umap-circle"[^>]*>[^<]*</div>'
                   r'<div class="umap-label">[^<]*</div><div class="umap-sub"[^>]*>[^<]*</div></div>)+</div>'),
        lambda m: '<div class="umap-row">' + JOURNEY + '</div>', 1)
def NOTES(text):
    return (re.compile(r'(<strong>Teacher recording notes:</strong> )[^<]*'), lambda m: m.group(1) + text, 1)
SPELL = ('reconcile · reunion · reprieve · counsel · exasperation · beneficial ·', 'prospector · reunion · reprieve · counsel · exasperation · benefactor ·', 1)
SHEET = (re.compile(r'The sheet gives Week 32 Day (\d) a final editing (?:and conventions )?review\. '), lambda m: 'Today is a final editing review. ', 1)
REVIEW = '''<div class="key-concept-label">📚 The Year in Review: Five Novels</div>
        <p><strong>The Witch of Blackbird Pond (Wks 1–5):</strong> Kit Tyler leaves Barbados for a strict Puritan town in Connecticut and finds out what it costs to stand by a friend everyone else fears.</p>
        <p style="margin-top:6px;"><strong>Johnny Tremain (Wks 6–8):</strong> An apprentice silversmith with a burned hand finds a new purpose in Boston as the Revolution begins.</p>
        <p style="margin-top:6px;"><strong>Carry On, Mr. Bowditch (Wks 9–14):</strong> A boy who has to leave school teaches himself navigation at sea and finds the mistakes in the sailors&rsquo; own books.</p>
        <p style="margin-top:6px;"><strong>How I Became a Ghost (Wks 18–24):</strong> Isaac, a Choctaw boy, tells the story of his people&rsquo;s forced journey west from Mississippi, and he tells it as a ghost.</p>
        <p style="margin-top:6px;"><strong>By the Great Horn Spoon! (Wks 25–30):</strong> Jack and the butler Praiseworthy sail around Cape Horn to the gold fields to save the family home, and find out what a fortune is really made of.</p>
        <p style="margin-top:6px;"><strong>The Comparison (Wk 31):</strong> Two of the five novels and a real voice from history, side by side.</p>
      </div>'''
FIX = {
 1: [UMAP, NOTES('Week 32 Day 1. This week each student writes a letter to a future 5th grader about two of this year&rsquo;s novels. Today is the Reader&rsquo;s Portrait and five Book Postcards. Keep the reading journal and the year&rsquo;s notes close by.'),
     ('Isaac walks north Jack sails west.', 'Isaac walks west Jack sails south.', 1),
     ('You studied <strong>20+ roots and suffixes</strong> across six units this year.', 'You studied <strong>roots and suffixes</strong> in every unit this year.', 1),
     SPELL, SHEET],
 2: [NOTES('Week 32 Day 2. Today students practice reading one short passage aloud and draft the letter to a future 5th grader. Keep the reading journal and the two chosen novels close by.'), SPELL],
 3: [NOTES('Week 32 Day 3. Today students revise the letter for a 10-year-old reader and write the Word Gift and the P.S. Keep the letter draft close by.'),
     ('> written a century apart.</div>', '> set in different centuries.</div>', 1), SPELL],
 4: [UMAP, NOTES('Week 32 Day 4. The last lesson of the year: students seal and send the letter, then record it with one poem from the year.'),
     (re.compile(r'<div class="key-concept-label">📚 The Year in Review: Five Novels</div>.*?</p>\s*</div>', re.S), lambda m: REVIEW, 1),
     (re.compile(r'You read about a girl accused of witchcraft in 1687,.*?and then compared them all\.'),
      lambda m: 'You read about a girl accused of witchcraft in colonial Connecticut, an apprentice silversmith in Boston before the Revolution, a self-taught navigator on the sailing ships of the 1790s, a Choctaw boy on his people&rsquo;s forced journey west, and a butler and a boy crossing 15,000 miles in 1849, and then you compared them.', 1),
     ('A list to memorise.', 'A list to memorize.', 1),
     ('<strong>From the historical novels (Wks 1–14):</strong> defiance, conviction, tyranny, rebellion, apprentice, covenant, celestial,',
      '<strong>From the historical novels (Wks 1–24):</strong> defiance, conviction, tyranny, rebellion, apprentice, declaration, celestial,', 1),
     ('<strong>From the adventure novels (Wks 25–31):</strong>', '<strong>From By the Great Horn Spoon! (Wks 25–30):</strong>', 1),
     ('two from the historical novels (Wks 1–14), two from the adventure novels (Wks 25–31)', 'two from the historical novels (Wks 1–24), two from By the Great Horn Spoon! (Wks 25–30)', 1),
     ('<div class="activity-num" style="background:#7B5EA7;">4</div><div style="flex:1;"><div class="activity-title">&#x1F520; Spelling: Final Editing',
      '<div class="activity-num" style="background:#7B5EA7;">3</div><div style="flex:1;"><div class="activity-title">&#x1F520; Spelling: Final Editing', 1),
     ('<div class="activity-num" style="background:#52B788;">3</div><div style="flex:1;"><div class="activity-title">✏️ Grammar: Final Conventions',
      '<div class="activity-num" style="background:#52B788;">4</div><div style="flex:1;"><div class="activity-title">✏️ Grammar: Final Conventions', 1),
     SHEET],
}
def run(apply):
    ok = True; out = {}
    for k, reps in FIX.items():
        fn = F[k]; t = io.open(fn, encoding='utf-8', newline='').read(); o = t
        for i, r in enumerate(reps):
            pat, new, n = r
            if isinstance(pat, str):
                c = t.count(pat)
                if c != n: print('FAIL', fn, i, 'count', c, '!=', n, repr(pat[:80])); ok = False; continue
                t = t.replace(pat, new)
            else:
                t, c = pat.subn(new, t)
                if c != n: print('FAIL', fn, i, 'regex count', c, '!=', n, pat.pattern[:80]); ok = False
        if o.count('<div') - o.count('</div>') != t.count('<div') - t.count('</div>'):
            print('FAIL div balance', fn); ok = False
        out[fn] = t; print(fn, len(o), '->', len(t))
    if ok and apply:
        for fn, t in out.items(): io.open(fn, 'w', encoding='utf-8', newline='').write(t)
        print('written')
    elif not ok: sys.exit(1)
run('--apply' in sys.argv)
