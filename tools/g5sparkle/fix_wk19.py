#!/usr/bin/env python3
"""Week 19 accuracy fixes (approved by Bethany Nov 21 2026; audit: claude/g5-ela-wk19-audit.md).
Book lines checked against planning docs/hbg_ocr.txt (Ch. 8-11). Every replacement asserts its count;
div balance must not change. Run once from the repo root."""
import io, re, sys

WW = ('<div class="turn-in-item-text">I wrote my Writing Connection sentence.</div>',
      '<div class="turn-in-item-text">I wrote my Writer&rsquo;s Workshop piece.</div>', 1)
RWMCHK = ('<div class="turn-in-item-text">I wrote my three RWM responses (Reader, Writer, Mimic) on the Reading tab.</div>',
          '<div class="turn-in-item-text">I wrote my three Read Like a Writer answers on the Reading tab.</div>', 1)
FIX = {
 'lesson-19-1-hbg-ch8.html': [
  # 1. Virtue Watch quoted Ch. 9 (Nita's promise) on the Ch. 8 day
  ('In Chapter 9, Nita tucks herself under Isaac&rsquo;s blanket and says &ldquo;I never had a big brother. Will you be my big brother?&rdquo; Isaac says yes. He has just promised to protect a little girl even though he is becoming a ghost. That is perseverance &mdash; committing to someone else&rsquo;s future even when you are uncertain of your own.',
   'In Chapter 8, Isaac&rsquo;s family leaves the swamp with nowhere to go: &ldquo;Early the next morning we gathered our belongings and left the camp. We walked all day and slept in the woods.&rdquo; Then they follow the walkers for three more days, hiding in the tree shadows. Perseverance can look like this: getting up the next morning and walking on.', 1),
  # 2. DOL fix-it came from Ch. 9; now a Ch. 8 sentence
  ('border-left:4px solid #8B3A20;">eventually the sleet stopped and the soldiers said let\'s make camp here</div>',
   'border-left:4px solid #8B3A20;">after sundown gabe and my father built a campfire close to the road</div>', 1),
  ('<strong>Corrected:</strong> Eventually, the sleet stopped and the soldiers said, &ldquo;Let&rsquo;s make camp here.&rdquo;</p>',
   '<strong>Corrected:</strong> After sundown, Gabe and my father built a campfire close to the road.</p>', 1),
  ('Comma after &ldquo;Eventually&rdquo; (transition). Quotation marks and comma around the direct speech.',
   'Comma after the opening phrase &ldquo;After sundown.&rdquo; Capital letters for <em>After</em> and for the name <em>Gabe</em>.', 1),
  ('Five words from Chapters 8–11.', 'Five words from Chapters 8, 9 and 10.', 1),
  WW,
 ],
 'lesson-19-2-hbg-ch9.html': [
  # 2. DOL fix-it came from Ch. 10; now a Ch. 9 sentence
  ('border-left:4px solid #8B3A20;">when i finally lifted my right foot the skin tore away</div>',
   'border-left:4px solid #8B3A20;">when the rain turned to ice we walked without stopping</div>', 1),
  ('<strong>Corrected:</strong> When I finally lifted my right foot, the skin tore away.</p>',
   '<strong>Corrected:</strong> When the rain turned to ice, we walked without stopping.</p>', 1),
  ('Comma after the dependent clause &ldquo;When I finally lifted my right foot.&rdquo; Main clause follows.',
   'Comma after the dependent clause &ldquo;When the rain turned to ice.&rdquo; Main clause follows.', 1),
  # 6. both sides signed the Treaty of Dancing Rabbit Creek (Sept. 1830)
  ('data-explain="This names the actor clearly. It is active voice.">The United States government signed the treaty in 1830.</span>',
   'data-explain="This names the actors clearly. It is active voice.">U.S. commissioners and Choctaw leaders signed the treaty in 1830.</span>', 1),
  RWMCHK, WW,
 ],
 'lesson-19-3-hbg-ch10.html': [
  # 7. the week closes on 19.4
  ('<span class="q-num">3</span>&#127775; <strong>Week Closer.</strong> Over Chapters 8, 9, and 10,', '<span class="q-num">3</span>Over Chapters 8, 9, and 10,', 1),
  ('data-label="Q3 (week closer): Isaac\'s three lessons"', 'data-label="Q3: Isaac\'s three lessons"', 1),
  RWMCHK, WW,
 ],
 'lesson-19-4-hbg-ch11.html': [WW],
}
VCH = {'smallpox': 8, 'belongings': 8, 'sickness': 9, 'refused': 10, 'vanished': 10}
TAG = ' <span class="vocab-ch" style="font-style:normal;font-size:12px;font-weight:700;color:#7A88A8;white-space:nowrap;">Ch. %d</span>'
FLU = '''<div class="fluency-passage">
    <div class="fluency-passage-text">
      Then another voice cut through the snow. &ldquo;Son!&rdquo; It was my father&rsquo;s voice. The Choctaw ghosts vanished.<br><br>
      Far ahead my father waited. I stumbled and fell and my father ran to meet me. He picked me up and held me close. &ldquo;Isaac,&rdquo; he said, &ldquo;take one last look behind you.&rdquo;<br><br>
      I turned my head and saw my footprints in the snow. &ldquo;Son,&rdquo; he said, &ldquo;you cannot keep your eyes on the bloody footprints you have left behind you. You must keep your eyes on where you are going.&rdquo;<br><br>
      I took a deep breath. I nodded. From that moment on, even though my feet burned, I refused to look behind me. I looked where I was going and forgot about the pain. I was stronger than the pain.
    </div>
    <div class="fluency-passage-source">&mdash; Tim Tingle, <em>How I Became a Ghost</em>, Chapter 10</div>
  </div>
  </div>
'''
def main():
    for f, reps in FIX.items():
        s = io.open(f, encoding='utf-8', newline='').read(); orig = s
        for old, new, n in reps:
            c = s.count(old)
            if c != n: sys.exit('%s: expected %d of %r, found %d' % (f, n, old[:70], c))
            s = s.replace(old, new)
        if f.startswith('lesson-19-1'):   # 8. chapter tag on each Day 1 card
            for w, ch in VCH.items():
                m = re.search(r'(<div class="decode-sentence">(?:(?!</div>).)*?>%s</strong>(?:(?!</div>).)*?)(</div>)' % w, s, re.S)
                if not m: sys.exit('no card for ' + w)
                s = s[:m.end(1)] + TAG % ch + s[m.end(1):]
        if s.count('<div') - s.count('</div') != orig.count('<div') - orig.count('</div'):
            sys.exit('%s: div balance changed' % f)
        io.open(f, 'w', encoding='utf-8', newline='').write(s); print('fixed', f)
    f = 'lesson-19-fluency.html'   # 9. one continuous Ch. 10 stretch, credited right
    s = io.open(f, encoding='utf-8', newline='').read(); orig = s
    a = s.index('<div class="fluency-passage"><p>The next morning')
    b = s.index('Chapter 1</div>\n  </div>\n      </div>\n', a) + len('Chapter 1</div>\n  </div>\n      </div>\n')
    s = s[:a] + FLU + '      </div>\n' + s[b:]
    for old, new in [
     ('This week you opened <em>How I Became a Ghost</em> by Tim Tingle. Isaac introduces himself in a way no narrator has before &mdash; as a ghost who isn&rsquo;t a ghost yet. Today you&rsquo;ll practice reading the opening passage with accuracy, smoothness, and the weight it deserves.',
      'This week Isaac&rsquo;s family joined the Choctaw walkers on the road west. Today you&rsquo;ll practice reading the moment in Chapter 10 when his father calls him back, with accuracy, smoothness, and the weight it deserves.'),
     ('Read again. Keep your voice flowing. Let the sentences move naturally. The short last sentence &mdash; &ldquo;Be careful what you wish for&rdquo; &mdash; should feel like a quiet warning, not rushed.',
      'Read it once to yourself first. Then read it again and keep your voice flowing. Let the short sentences (&ldquo;I took a deep breath. I nodded.&rdquo;) each take their own beat.'),
     ('Now bring Isaac to life. He is speaking from the future &mdash; he already knows what happened. Let your voice carry that weight. Slow down on &ldquo;Be careful what you wish for.&rdquo;',
      'Now bring the father&rsquo;s voice to life. He is calm and sure. Slow down on &ldquo;You must keep your eyes on where you are going.&rdquo;'),
     ('including &ldquo;Choctaw&rdquo; and &ldquo;Mississippi&rdquo;?', 'including &ldquo;Choctaw&rdquo; and &ldquo;stumbled&rdquo;?'),
     ('Did my voice carry the feeling of Isaac&rsquo;s warning? Did &ldquo;Be careful what you wish for&rdquo; land the way it should?',
      'Did my voice change for the father&rsquo;s words? Did his last line sound calm and sure?'),
    ]:
        if s.count(old) != 1: sys.exit('fluency: %r x%d' % (old[:60], s.count(old)))
        s = s.replace(old, new)
    if s.count('<div') - s.count('</div') != orig.count('<div') - orig.count('</div'):
        sys.exit('fluency: div balance changed %d vs %d' % (s.count('<div') - s.count('</div'), orig.count('<div') - orig.count('</div')))
    io.open(f, 'w', encoding='utf-8', newline='').write(s); print('fixed', f)
main()
