#!/usr/bin/env python3
"""Week 18 accuracy fixes (approved by Bethany Nov 9 2026; audit: claude/g5-ela-wk18-audit.md).
Every replacement asserts its expected count. Run from the repo root. Idempotence: refuses if already applied."""
import io, sys

def spot(sid, words, correct):
    out = []
    for i, w in enumerate(words.split()):
        out.append('<span class="spotter-word" onclick="spotterPick(this,\'%s\')" data-correct="%s">%s</span>'
                   % (sid, 'true' if i == correct else 'false', w))
    return ' '.join(out)

FIX = {
 'lesson-18-1-hbg-ch4.html': [
  # A. Virtue Watch told the Ch. 4 fire in the Ch. 1-2 lesson
  ('When the Nahullo men burn the town and a neighbor is shot, Isaac&rsquo;s father throws himself over his family. He shields them &mdash; then says: &ldquo;Run, and stay together.&rdquo; Courage is not the absence of fear. It is choosing someone else&rsquo;s safety over your own.',
   'At the river, Isaac sees things that frighten him, but he keeps watching. His mother whispers, &ldquo;Don&rsquo;t talk. Just watch.&rdquo; Courage is not the absence of fear. Sometimes it is looking at a hard truth instead of turning away.', 1),
  # C. torches definition
  ('Twenty flaming torches fell on the town.', 'Twenty flaming torches fell on the missionaries&rsquo; house.', 2),
  # G. lesson-made sentence shown as a book quote
  ('Read this sentence: <em>&ldquo;Isaac&rsquo;s father, a quiet and dignified man, held Mother&rsquo;s hand.&rdquo;</em>',
   'Read this example sentence (it is not from the book): <em>Isaac&rsquo;s father, a quiet and dignified man, held Mother&rsquo;s hand.</em>', 1),
 ],
 'lesson-18-2-hbg-ch5.html': [
  # D. Virtue Watch quoted Ch. 5 in the Ch. 3-4 lesson
  ('Old Man doesn&rsquo;t wait for someone else to lead. He stands up, gives everyone a job, and answers a rude question with grace: &ldquo;The older women do not need me to tell them what to do.&rdquo; Courage means stepping forward when no one asked you to.',
   'When a Nahullo man aims his shotgun at the family, Isaac&rsquo;s father moves first: &ldquo;My father threw himself over us and we fell to the ground.&rdquo; Courage is not the absence of fear. It is choosing someone else&rsquo;s safety over your own.', 1),
  ('Twenty flaming torches fell on the town.', 'Twenty flaming torches fell on the missionaries&rsquo; house.', 2),
  # M. lonely: its first beat "lone" ends on an n sound, but it was tagged open
  ('data-group="open" onclick="pickSortChip(this)">lonely<', 'data-group="open" onclick="pickSortChip(this)">paper<', 1),
  # E. Poetry prompt chapter
  ('doing in Chapters 4 and 5?', 'doing in Chapter 4?', 1),
  # F. Day-2 grammar was a copy of Day 1: new Ch. 3-4 sentences + new SWYK
  (spot('spot1', 'Jumper, my dog, was always by my side.', 1), spot('spot1', 'Missus Jonah, his wife, danced on the stones.', 2), 1),
  (spot('spot2', 'Luke, my big brother, left to play stickball.', 1), spot('spot2', 'The willow, the oldest in Choctaw country, hung over the water.', 2), 1),
  (spot('spot3', 'Treaty Talk, news from the Nahullos, had come to town.', 2), spot('spot3', 'Old Man and Old Woman, the two oldest people in town, played in the river.', 5), 1),
  ('Read this sentence: <em>&ldquo;Isaac&rsquo;s father, a quiet and dignified man, held Mother&rsquo;s hand.&rdquo;</em> What is the appositive? What does it tell you about Isaac&rsquo;s father?',
   'Read this example sentence (it is not from the book): <em>Jumper, Isaac&rsquo;s dog, leapt into his arms.</em> What is the appositive? What does it tell you about Jumper?', 1),
 ],
 'lesson-18-3-hbg-ch6.html': [
  ('Twenty flaming torches fell on the town.', 'Twenty flaming torches fell on the missionaries&rsquo; house.', 1),
  # H. three false grammar sentences
  ('He sat in the shallow water.', 'He sat with his back against a tree.', 1),
  ('sat in the shallow water.', 'sat with his back against a tree.', 2),
  (', was already taller than their father.', ', was twelve years old.', 1),
  ('Nita was Isaac&rsquo;s mother. Nita carried the youngest child.', 'Old Man was the oldest man in town. Old Man spoke first in the swamp.', 1),
  # I. graded Q2: the book says "many", not everyone
  ('Everyone accepts them gladly &mdash; except Isaac&rsquo;s family.', 'Many families take them gladly, but Isaac&rsquo;s family stays inside.', 1),
  # J. foreshadowed Ch. 8 and framed the novel's smallpox blankets as history
  ('&ldquo;Men with Blankets&rdquo; sounds almost ordinary until you know what those blankets carried. Ask what the historical context supplies that Isaac never spells out.',
   '&ldquo;Men with Blankets&rdquo; sounds almost ordinary. Watch what Isaac&rsquo;s mother does, and what Isaac sees when Old Man comes close. Then ask what the history around the story (the treaty, the soldiers, the winter) helps you understand that Isaac, at ten, never explains.', 1),
  # M. soldier: its o says its name, but it was tagged closed
  ('data-group="closed" onclick="pickSortChip(this)">soldier<', 'data-group="closed" onclick="pickSortChip(this)">basket<', 1),
 ],
 'lesson-18-4-hbg-ch7.html': [
  ('Twenty flaming torches fell on the town.', 'Twenty flaming torches fell on the missionaries&rsquo; house.', 2),
 ],
 'lesson-18-fluency.html': [
  # O. passage mixed Ch. 4 and Ch. 1 under a "Chapter 1" credit and skipped lines
  (None, None, 0),
 ],
}

def main():
    for f, reps in FIX.items():
        s = io.open(f, encoding='utf-8', newline='').read(); orig = s
        if f == 'lesson-18-fluency.html':
            a = s.index('<div class="fluency-passage"><p>We returned from the river.')
            b = s.index('<div class="fluency-passage-text">', a)
            s = s[:a] + '<div class="fluency-passage">\r\n    ' + s[b:]
            reps = [
             ('Be careful what you wish for.\r\n    </div>',
              'Be careful what you wish for.<br><br>\r\n      I&rsquo;m ten years old and I&rsquo;m not a ghost yet. My name is Isaac and I have a mother and a father and a big brother, Luke. I have a dog, too. His name is Jumper and he is my best friend. We go everywhere together. We swim in the river together; we chase chickens together.\r\n    </div>', 1),
             ('<div class="step-detail">Read again. Keep your voice flowing.', '<div class="step-detail">Read it once to yourself first. Then read it again and keep your voice flowing.', 1),
             ('including &ldquo;Choctaw&rdquo; and &ldquo;Mississippi&rdquo;?', 'including the names Isaac, Luke, and Jumper?', 1),
             # the removed Ch. 4 paragraphs carried the passage box's </div>; the box now wraps the
             # Ch. 1 text and its credit line, so its </div> moves to after the credit
             ('Chapter 1</div>\r\n  </div>\r\n      </div>\r\n', 'Chapter 1</div>\r\n  </div>\r\n  </div>\r\n      </div>\r\n', 1),
            ]
        for old, new, n in reps:
            c = s.count(old)
            if c != n:
                sys.exit('%s: expected %d of %r, found %d' % (f, n, old[:70], c))
            s = s.replace(old, new)
        if s.count('<div') - s.count('</div') != orig.count('<div') - orig.count('</div'):
            sys.exit('%s: div balance changed' % f)
        io.open(f, 'w', encoding='utf-8', newline='').write(s)
        print('fixed', f)
main()
