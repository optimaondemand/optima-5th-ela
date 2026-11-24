#!/usr/bin/env python3
"""Week 31 pages brought in line with the scope (v2_poetry scope week 31), approved by Bethany Nov 24 2026
(claude/g5-ela-wk31-scope-check.md). One strand per run, each its own commit:
    python tools/g5sparkle/scope_wk31.py rwm|wgrd|plan|revise|review [--apply]
rwm    = Read Like a Writer D1-D4: organizing a comparison using clear categories (mini-lesson + model, frames, apply, revise alone)
wgrd   = What Good Readers Do How to Do It as lens items (Name: tip), one think-question
plan   = the essay plan by category: five paragraphs (opening, two category paragraphs, a real-source paragraph, closing)
revise = Day 3 is the revise day (finish the draft, then revise with the checklist)
review = Day 4 solo 'reviewer's eyes' pass, no partner (students are self-paced)
Model sentences are written by Optima and labeled; every fact in them is checked against the novels."""
import io, re, sys
F = {1: 'lesson-31-1-comparison-plan.html', 2: 'lesson-31-2-comparison-sources.html', 3: 'lesson-31-3-comparison-draft.html', 4: 'lesson-31-4-comparison-submit.html'}
READ_NEXT = re.compile(r'(<div class="tab-next-wrap"><p class="tab-transition-voice">[^<]*</p>\s*<button class="tab-next-btn" onclick="markDone\(\'reading\'\);switchTab\(\'assignment\'\)">)')
RWM_CSS = '''
/* Read Like a Writer box (same as weeks 19-30) */
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
def rwm(sentence, src, reader, writer, tryit, frame):
    fr = '      <div class="rwm-frame">%s</div>\n' % frame if frame else ''
    return ('  <!-- RWM -->\n  <div class="rwm-box">\n'
      '    <div class="rwm-header">&#128214; Read Like a Writer &mdash; Read &bull; Notice &bull; Try</div>\n'
      '    <div class="rwm-sentence">%s <span style="font-size:13px;color:#5A6B8C;font-style:normal;">(%s)</span></div>\n'
      '    <div class="rwm-step"><div class="rwm-step-label">&#128214; As a Reader</div>\n'
      '      <div class="rwm-step-text">%s</div>\n%s    </div>\n'
      '    <div class="rwm-step"><div class="rwm-step-label">&#9999;&#65039; As a Writer</div>\n'
      '      <div class="rwm-step-text">%s</div>\n%s    </div>\n'
      '    <div class="rwm-step"><div class="rwm-step-label">&#128394;&#65039; Try It</div>\n'
      '      <div class="rwm-step-text">%s</div>\n%s%s    </div>\n'
      '  </div>\n\n') % (sentence, src, reader, ta('journal-rwm-reader', 'Read Like a Writer: As a Reader', 'I notice...'), writer,
                        ta('journal-rwm-writer', 'Read Like a Writer: As a Writer', 'The writer...'), tryit, fr, ta('journal-rwm-mimic', 'Read Like a Writer: Try It', 'My sentences...'))
R = {
 1: rwm('Both Kit Tyler and Jack Flagg leave home for a strange new place. <strong>How they arrive:</strong> Kit sails to Connecticut after her grandfather dies, while Jack hides in a potato barrel because he chose to go. <strong>Who helps them:</strong> Kit finds a friend in Hannah Tupper, and Jack has Praiseworthy beside him. <strong>What it costs:</strong> Kit&rsquo;s friendship puts her on trial as a witch; Jack loses his gold in San Francisco Bay.',
        'model written by Optima from <em>The Witch of Blackbird Pond</em> and <em>By the Great Horn Spoon!</em>',
        'Find the three categories in bold. In each one, what does the writer say about Kit, and what about Jack?',
        'This writer sorts the comparison into <strong>categories</strong> and puts <em>both</em> books inside every category. A reader never has to remember Kit for a whole page while waiting for Jack. Each category is a place where the two books stand side by side.',
        'Name two categories for your own two novels (for example: how they arrive, who helps them, what it costs). Write one sentence for one category that names both books.',
        'In ___ [category], ___ [novel 1] ___, while ___ [novel 2] ___.'),
 2: rwm('<strong>Who teaches them:</strong> Johnny Tremain learns from Rab and the Boston Observers, while Nat Bowditch teaches himself from books, one page at a time.',
        'model written by Optima from <em>Johnny Tremain</em> and <em>Carry On, Mr. Bowditch</em>',
        'What is the category? Which word joins the two books?',
        'The category comes first, then both books, joined by one word (<em>while</em>). That order tells the reader what to look for before the details arrive.',
        'Write one sentence for each of your two categories. Use a frame for each one.',
        'In ___ [category], ___ [novel 1] ___; in contrast, ___ [novel 2] ___.<br>Both ___ and ___ ___ when it comes to ___ [category].'),
 3: rwm('<strong>What a real voice adds:</strong> Bayard Taylor&rsquo;s report that &ldquo;every man is his own porter here&rdquo; shows the same do-it-yourself San Francisco that Jack and Praiseworthy land in.',
        'model written by Optima; the quotation is Bayard Taylor, <em>Eldorado</em>, 1850',
        'What does the first sentence of this source paragraph promise the reader?',
        'The category name (<em>what a real voice adds</em>) opens the paragraph, and the quotation is short and exact. The rest of the paragraph explains how the source fits or complicates the novel.',
        'Write the first sentence of your own source paragraph. Start with your category, then quote a few exact words from your source.', None),
 4: rwm('<strong>Before:</strong> Kit is brave. Jack is brave too. <strong>After:</strong> In what it costs them, Kit&rsquo;s courage nearly costs her freedom, while Jack&rsquo;s costs him his gold.',
        'model written by Optima',
        'What changed between the two versions?',
        'On your own this time. Look at the After version. What does the category give the reader that the Before version does not?',
        'Find one paragraph in your draft that talks about one book at a time. Rewrite its first sentence so it names the category and both books.', None),
}
CHK_RWM = '<div class="turn-in-item" onclick="toggleCheck(this)"><div class="turn-in-check"></div><div class="turn-in-item-text">I answered the Read Like a Writer box.</div></div>'
CHKL = '<div class="turn-in-checklist">'
def ol(items): return ''.join('<li><strong>%s:</strong> %s</li>\n          ' % it for it in items)
OL_RE = re.compile(r'(How to Do It</div>\s*<ol[^>]*>\s*)(?:<li>.*?</li>\s*)+(</ol>)', re.S)
SUB_RE = re.compile(r'(What Good Readers Do</div><div class="activity-sub">)[^<]*(</div>)')
Q_RE = re.compile(r'(<div class="socratic-label">&#x1F9E0;[^<]*</div>\s*)(?:<p class="socratic-q">.*?</p>\s*)+', re.S)
W = {
 1: ([('Theme line', 'Name the theme you are tracking, in one sentence.'), ('Author&rsquo;s view', 'For each novel, ask what the author seems to believe about that theme.'),
      ('The difference', 'Look for where the two books disagree. That is where your essay lives.')],
     'Which two of this year&rsquo;s novels treat your theme most differently? What is the difference?'),
 2: ([('Who and when', 'For each source, ask who made it, when, and why.'), ('Can and cannot', 'Ask what the source can tell you, and what it cannot.'),
      ('Fit', 'Ask whether the source agrees with your novel or shows something different.')],
     'What can your primary source tell you that your novel cannot?'),
 3: ([('Strongest proof', 'Find the passage that best supports your comparison.'), ('Complication', 'Look for one passage that does not fit your claim.'),
      ('Decide', 'Change the claim, or explain the complication in your essay.')],
     'Find one passage that does not fit your claim. Will you change the claim, or explain the passage?'),
 4: ([('Claim', 'Read once for the claim. Say it in your own words.'), ('Evidence', 'Read again. Does each piece of evidence fit its category?'),
      ('Reasoning', 'Read a third time for the sentences that explain why the difference matters.')],
     'Where does your essay need a sentence of reasoning more than another piece of evidence?'),
}
def wgrd(d):
    lenses, q = W[d]
    return [(OL_RE, lambda m: m.group(1) + ol(lenses) + m.group(2), 1), (Q_RE, lambda m: m.group(1) + '<p class="socratic-q">%s</p>\n      ' % q, 1)]
# ---- plan by category
STRUCT_OLD = re.compile(r'<div class="key-concept"><div class="key-concept-label">📋 Your Essay Structure</div>.*?</div>', re.S)
STRUCT = ('<div class="key-concept"><div class="key-concept-label">📋 Your Essay Structure &mdash; five paragraphs, organized by category</div>\n'
          '      <p><strong>1. Opening:</strong> a hook, both novels named, and your comparison claim from Day 1.</p>\n'
          '      <p><strong>2. Category 1:</strong> name the category, then both novels side by side, with one piece of evidence from each and what the difference shows.</p>\n'
          '      <p><strong>3. Category 2:</strong> the same, for your second category.</p>\n'
          '      <p><strong>4. A real voice:</strong> your primary source, and how it fits or complicates your novels.</p>\n'
          '      <p><strong>5. Closing:</strong> what the two novels say together, and why it matters.</p>\n    </div>')
PLAN = {
 1: [('Write your comparison claim below. Then list your four pieces of evidence (two per novel).',
      'Write your comparison claim. Then name your two categories, with one piece of evidence from each novel for each category (four in all).', 1),
     ('placeholder="My comparison claim:&#10;Both ___ and ___ argue that [theme idea]; however, while ___ shows this through..., ___ reveals it through...&#10;&#10;Evidence plan:&#10;Novel 1: (a) ... (b) ...&#10;Novel 2: (a) ... (b) ..."',
      'placeholder="My comparison claim:&#10;Both ___ and ___ argue that [theme idea]; however, while ___ shows this through..., ___ reveals it through...&#10;&#10;Category 1: ___&#10;  Novel 1: ...&#10;  Novel 2: ...&#10;Category 2: ___&#10;  Novel 1: ...&#10;  Novel 2: ..."', 1),
     ('For each novel, identify <strong>two specific pieces of evidence</strong> (scenes, moments, or quotes) that support your thesis. Describe each one: what happens, who is involved, and what it shows about the theme.',
      'Choose <strong>two categories</strong> to compare your novels in (for example: how they arrive, who helps them, what it costs). For each category, name one moment from each novel: what happens, who is involved, and what it shows about the theme.', 1),
     ('data-label="Planning Q3: Two pieces of evidence per novel — scene, characters, theme connection"', 'data-label="Planning Q3: Two categories, one moment from each novel in each"', 1),
     ('placeholder="Novel 1 evidence:&#10;  Evidence A: [scene/moment] — this shows the theme because...&#10;  Evidence B: [scene/moment] — this shows the theme because...&#10;&#10;Novel 2 evidence:&#10;  Evidence A: ...&#10;  Evidence B: ..."',
      'placeholder="Category 1: ___&#10;  Novel 1 moment: ... — this shows...&#10;  Novel 2 moment: ... — this shows...&#10;&#10;Category 2: ___&#10;  Novel 1 moment: ...&#10;  Novel 2 moment: ..."', 1),
     ('I wrote my comparison claim and identified four pieces of evidence.', 'I wrote my comparison claim and planned two categories with evidence from both novels.', 1)],
 2: [(STRUCT_OLD, lambda m: STRUCT, 1),
     ('Draft your opening paragraph and at least one body paragraph today. Use your comparison claim from Day 1.',
      'Draft paragraph 1 (your opening) and paragraph 2 (Category 1) today. Use your comparison claim and categories from Day 1.', 1),
     ('data-label="Comparison Project DRAFT: Opening + body paragraph(s)"', 'data-label="Comparison Project DRAFT: Opening + Category 1 paragraph"', 1),
     ('placeholder="[Opening: Hook sentence. Both novels named. Comparison claim.]&#10;&#10;[Body Paragraph 1: Novel 1 claim. Evidence A. Evidence B. Explain.]&#10;&#10;[Body Paragraph 2 — start if time permits]"',
      'placeholder="[1. Opening: hook. Both novels named. Comparison claim.]&#10;&#10;[2. Category 1: name the category. Novel 1 evidence. Novel 2 evidence. What the difference shows.]"', 1),
     ('I drafted my opening paragraph and at least one body paragraph.', 'I drafted my opening and my Category 1 paragraph.', 1)],
}
# ---- Day 3 = revise
REV3 = [
 ('<div class="activity-title">Writing Workshop: The Comparison Paragraph</div><div class="activity-sub">The paragraph that makes your essay a real argument</div>',
  '<div class="activity-title">Writing Workshop: Finish the Draft</div><div class="activity-sub">Category 2, a real voice, and your closing</div>', 1),
 (re.compile(r'<div class="key-concept"><div class="key-concept-label">📌 How to Write the Comparison Paragraph</div>.*?</div>', re.S),
  lambda m: ('<div class="key-concept"><div class="key-concept-label">📌 How to Write the Last Three Paragraphs</div>\n'
             '        <p><strong>3. Category 2:</strong> name the category, then both novels side by side, with evidence from each and what the difference shows.</p>\n'
             '        <p><strong>4. A real voice:</strong> start with the category, quote a few exact words from your primary source, then explain how it fits or complicates your novels.</p>\n'
             '        <p><strong>5. Closing:</strong> say your claim in new words, tell what the comparison shows about the theme, and end with why these two books belong together.</p>\n      </div>'), 1),
 ('<strong>Example comparison paragraph (about courage):</strong>', '<strong>Example category paragraph (category: how they show courage):</strong>', 1),
 ('Write your <strong>comparison paragraph</strong> following the four steps in the How to Write box. Use at least two transition words (however, although, while, in contrast, both... and, therefore, consequently). Underline each transition.',
  'Write paragraph 3 (<strong>Category 2</strong>) and paragraph 4 (<strong>a real voice</strong>). Use at least two transition words (however, although, while, in contrast, both... and, therefore, consequently). Underline each transition.', 1),
 ('data-label="Draft Q1: Comparison paragraph — similarity, key difference, why it matters, bigger idea"', 'data-label="Draft Q1: Category 2 paragraph + real-voice paragraph"', 1),
 ('placeholder="Both ___ and ___ agree that...&#10;However, while ___ shows this through..., ___ reveals it through...&#10;This difference is significant because...&#10;Together, these two novels suggest that..."',
  'placeholder="[3. Category 2: In ___, ___ ..., while ___ ...]&#10;&#10;[4. A real voice: In ___, ___ writes &quot;...&quot; This fits / complicates ___ because...]"', 1),
 ('<div class="swyk-label">📝 Draft Question 3 — Self-Assessment</div>', '<div class="swyk-label">📝 Draft Question 3 — Checklist Pass</div>', 1),
 ('Read your full draft (opening + body 1 + body 2 + comparison + closing). In 3–4 sentences: What is the strongest part of your essay? What is the weakest part — and what would make it stronger?',
  'Read all five paragraphs out loud. Check them against the Revision Checklist on the Assignment tab. In 3&ndash;4 sentences: Which checklist line was hardest to meet, and what will you change?', 1),
 ('Full draft done. Tomorrow: peer review and revise.', 'Full draft done. Now revise it with the checklist.', 1),
 ('<div class="activity-title">Comparison Project &middot; Week 31 &middot; FULL DRAFT COMPLETE</div><div class="activity-sub">All five paragraphs written — ready for peer review</div>',
  '<div class="activity-title">Comparison Project &middot; Week 31 &middot; REVISE</div><div class="activity-sub">Revise all five paragraphs with the checklist</div>', 1),
 (re.compile(r'<div class="key-concept"><div class="key-concept-label">📋 Full Draft Checklist Before Peer Review</div>.*?</div>', re.S),
  lambda m: ('<div class="key-concept"><div class="key-concept-label">📋 Revision Checklist</div>\n'
             '      <p>✓ Opening: a hook, both novels named, and a claim that names the similarity AND the difference</p>\n'
             '      <p>✓ Paragraphs 2 and 3: each starts with its category and puts both novels inside it</p>\n'
             '      <p>✓ Every piece of evidence is a real moment or exact words from the book</p>\n'
             '      <p>✓ Paragraph 4: a few exact words from your primary source, and how they fit or complicate the novels</p>\n'
             '      <p>✓ Closing: the claim in new words, and why these two books belong together</p>\n'
             '      <p>✓ At least 4 different transition words across the essay</p>\n    </div>'), 1),
 ('Copy your full draft here (or confirm all five sections are written). Tomorrow you&rsquo;ll do peer review.',
  'Paste your revised essay here, all five paragraphs. At the top, write one change you made and which checklist line it fixed.', 1),
 ('data-label="Comparison Project FULL DRAFT — all five paragraphs" placeholder="[Full draft — all five paragraphs]"',
  'data-label="Comparison Project REVISED DRAFT — all five paragraphs" placeholder="One change I made: ... (checklist line: ...)&#10;&#10;[Revised essay — all five paragraphs]"', 1),
 ('I completed the comparison paragraph with all four steps and transitions underlined.', 'I wrote my Category 2 and real-voice paragraphs with transitions underlined.', 1),
 ('I completed a self-assessment identifying my essay&rsquo;s strength and one area to improve.', 'I revised all five paragraphs with the Revision Checklist.', 1),
 ('<strong>Project:</strong> I will complete the comparison paragraph and closing of my essay.', '<strong>Project:</strong> I will finish my draft and revise it with a checklist.', 1),
]
# ---- Day 4 solo review
REV4 = [
 ('<div class="intro-card-head-title">What does a strong peer reviewer do — and what do you do with the feedback?</div>', '<div class="intro-card-head-title">How do you read your own essay the way a reviewer would?</div>', 1),
 ('A peer reviewer is not a proofreader. They read to understand — and then ask: Is the claim clear? Is the evidence convincing? Does the comparison actually show a meaningful difference? Today you review a classmate&rsquo;s work (or self-review) and make targeted revisions.',
  'A reviewer is not a proofreader. A reviewer reads to understand, then asks: Is the claim clear? Is the evidence convincing? Does the comparison show a difference that matters? Today you read your own essay with a reviewer&rsquo;s eyes, argue the other side, and make two targeted revisions.', 1),
 ('I will give specific, helpful feedback on a comparison essay (classmate&rsquo;s or own).', 'I will review my own essay as a reviewer would and argue the other side.', 1),
 ('Today you review your own essay (or a classmate&rsquo;s) as a careful reader.', 'Today you review your own essay as a careful reader.', 1),
 ('Synthesize &mdash; read a classmate&rsquo;s comparison', 'Synthesize &mdash; read your own comparison as a reviewer', 1),
 ('Peer review is reading, and it asks the same skill you have used all year: understand before you judge. Read your partner&rsquo;s comparison for what it is <em>trying</em> to say first. Only then ask whether the evidence carries it.',
  'Reviewing is reading, and it uses the skill you have practiced all year: understand before you judge. Read your own essay for what it is <em>trying</em> to say first, as if someone else wrote it. Then ask whether the evidence carries it.', 1),
 ('As you read a classmate&rsquo;s work, ask yourself', 'As you read your own essay, ask yourself', 1),
 ('All reviewed. Peer review and submit.', 'All reviewed. Now read your essay as a reviewer.', 1),
 ('Continue to 👥 Peer Review →', 'Continue to 👥 Reviewer&rsquo;s Eyes →', 1),
 ('<div class="activity-title">Peer Review: Read to Understand, Then Respond</div><div class="activity-sub">Specific feedback that helps — not just praise or nitpicking</div>',
  '<div class="activity-title">Reviewer&rsquo;s Eyes: Read Your Own Draft, Then Respond</div><div class="activity-sub">Specific notes that help, then argue the other side</div>', 1),
 ('📌 The Three Questions of Good Peer Review', '📌 The Three Questions a Reviewer Asks', 1),
 ('<strong>2. Does the comparison paragraph show a meaningful difference?</strong>', '<strong>2. Do your category paragraphs show a difference that matters?</strong>', 1),
 ('<strong>How to write helpful feedback:</strong> Be specific and kind. Not: &ldquo;Your essay is good.&rdquo; Instead: &ldquo;Your comparison claim is clear — I can see the difference between the two novels. Your Body Paragraph 1 has strong evidence. In the comparison paragraph, I couldn&rsquo;t tell why the difference between the two novels MATTERS. One more sentence explaining that would make your argument much stronger.&rdquo;',
  '<strong>How to write a helpful note to yourself:</strong> Be specific. Not: &ldquo;My essay is good.&rdquo; Instead: &ldquo;My claim is clear. Paragraph 2 has strong evidence from both books. In paragraph 3 I never say why the difference MATTERS. One more sentence would fix that.&rdquo;', 1),
 ('👥 Peer Review Question 1', '👥 Reviewer Question 1', 1), ('👥 Peer Review Question 2', '👥 Reviewer Question 2 — Argue the Other Side', 1), ('👥 Peer Review Question 3 — Week Synthesis', '👥 Reviewer Question 3 — Week Synthesis', 1),
 ('Read the full draft (a classmate&rsquo;s, or your own with fresh eyes). Write your answers to the three peer review questions: (1) State the comparison claim in your own words. (2) Is the comparison paragraph showing WHY the difference matters? (3) Are the evidence examples specific?',
  'Read your full draft out loud, as if someone else wrote it. Answer the three reviewer questions: (1) State the claim in your own words. (2) Do the category paragraphs show WHY the difference matters? (3) Is the evidence specific?', 1),
 ('data-label="Peer Review Q1: Three peer review questions answered"', 'data-label="Reviewer Q1: Three reviewer questions answered"', 1),
 ('Write two pieces of specific feedback: (1) Name the strongest part of the essay and explain specifically why it works. (2) Name one part that could be stronger and give a specific suggestion for how to improve it.',
  'Argue the other side. Write 2 sentences a reader who disagrees with your claim might say. Then write 1 sentence that answers them, using evidence from a book.', 1),
 ('data-label="Peer Review Q2: Strongest part + one specific improvement suggestion" placeholder="Strongest part: [specific quote or section] — this works because...&#10;&#10;One part to strengthen: [specific section] — suggestion: ..."',
  'data-label="Reviewer Q2: The other side, and my answer" placeholder="A reader who disagrees might say...&#10;&#10;My answer: In ___, ..."', 1),
 ('data-label="Peer Review Q3 (Week Synthesis): Process reflection — what you learned, what was hardest, what helped"', 'data-label="Reviewer Q3 (Week Synthesis): What I learned, what was hardest, what helped"', 1),
 ('<p>✓ Strengthen the comparison paragraph — add the sentence explaining WHY the difference matters</p>', '<p>✓ Strengthen a category paragraph — add the sentence explaining WHY the difference matters</p>', 1),
 ('I answered all three peer review questions and provided specific feedback.', 'I answered the three reviewer questions and argued the other side.', 1),
 ('Both boys are brave, but their courage is not the same kind: Jack risks a fortune, Isaac survives a loss.', 'Both boys are brave, but their courage is not the same kind: Jack chooses his journey, while Isaac is forced onto his.', 1),
]
def plan(which):
    P = {}
    if which == 'rwm':
        for d in (1, 2, 3, 4):
            P[d] = [(READ_NEXT, lambda m, d=d: R[d] + m.group(1), 1), (CHKL, CHKL + CHK_RWM, 1), ('</style>', RWM_CSS + '</style>', 'first')]
    elif which == 'wgrd':
        for d in (1, 2, 3, 4): P[d] = wgrd(d)
    elif which == 'plan': P = PLAN
    elif which == 'revise': P = {3: REV3}
    elif which == 'review': P = {4: REV4}
    else: sys.exit('strand?')
    return P
def main():
    which = sys.argv[1]; apply = '--apply' in sys.argv
    out = {}
    for k, reps in plan(which).items():
        f = F[k]; s0 = io.open(f, encoding='utf-8', newline='').read(); s = s0
        for old, new, n in reps:
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
