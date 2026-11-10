#!/usr/bin/env python3
"""G5 ELA week 18 pilot review (Nov 10 2026): vocabulary out of order + too much to read.

    python tools/g5sparkle/vocab_lean_wk18.py            # dry run
    python tools/g5sparkle/vocab_lean_wk18.py --apply

Vocabulary (all four days): the week's five words appear in BOOK order
(smothering, Nahullo, torches, missionaries, blowguns: Ch. 4, then Ch. 5) on the
cards, word bank, context sentences, match game, fill-in and use-it boxes.
Day 1 drops the two stray cards (treaty, scattered) that sat AFTER the match
check (treaty is week 20's word; the scattered card named the wrong chapter).
Chapter labels fixed ("Chapters 4-7" / "1-7" -> "Chapters 4 and 5").
Match-game meanings are trimmed to their first sentence (the second sentence
named the word and gave the answer away).

Lean: Day 1 think-question lists keep one question; the DOL hint line that
repeats What to do goes; DATA What-to-do lines follow. Never touches answers
a student types, graded boxes, or scope topics.
"""
import io, json, re, sys

ORDER = ["smothering", "Nahullo", "torches", "missionaries", "blowguns"]
CH = {"smothering": 4, "Nahullo": 4, "torches": 4, "missionaries": 4, "blowguns": 5}
SHORT = {
 "Nahullo": "A white person — the Choctaw word Isaac's family uses for the men who come on horseback.",
 "missionaries": "People sent to a place to teach their religion.",
 "blowguns": "Long tubes used to shoot darts.",
 "torches": "Burning sticks carried as a light or a weapon.",
 "smothering": "Covering something so closely that it cannot breathe or burn.",
}
PERM = [3, 2, 4, 0, 1]   # meaning shown beside word i (never its own)
FILES = {1: "lesson-18-1-hbg-ch4.html", 2: "lesson-18-2-hbg-ch5.html",
         3: "lesson-18-3-hbg-ch6.html", 4: "lesson-18-4-hbg-ch7.html"}
APPLY = "--apply" in sys.argv
log = []

def word_of(block):
    for w in ORDER:
        if re.search(r'>\s*%s\s*<|data-answer="%s"|vocab-%s"|\b%s</strong>' % (w, w.lower(), w.lower(), w), block):
            return w
    return None

def reorder(s, pat, name):
    """Find the run of consecutive blocks matching pat; put them in ORDER."""
    ms = list(re.finditer(pat, s, re.S))
    if len(ms) != 5: raise SystemExit("%s: expected 5 blocks, found %d" % (name, len(ms)))
    blocks = {word_of(m.group(0)): m.group(0) for m in ms}
    if set(blocks) != set(ORDER): raise SystemExit("%s: words %s" % (name, list(blocks)))
    out, last = [], 0
    for i, m in enumerate(ms):
        out.append(s[last:m.start()]); out.append(blocks[ORDER[i]]); last = m.end()
    out.append(s[last:])
    log.append(name)
    return "".join(out)

def match_grid(s):
    m = re.search(r'(<div class="match-grid" id="matchGrid">)(.*?)(\n\s*</div>\s*<div class="match-feedback")', s, re.S)
    if not m: return s
    ind = "\n          "
    rows = []
    for i, w in enumerate(ORDER):
        L = "ABCDE"[i]; j = PERM[i]
        rows.append('<div class="match-item is-word" data-match="%s" onclick="matchClick(this)">%s</div>' % (L, w))
        rows.append('<div class="match-item" data-match="%s" onclick="matchClick(this)">%s</div>' % ("ABCDE"[j], SHORT[ORDER[j]]))
    log.append("match grid")
    return s[:m.start()] + m.group(1) + ind + ind.join(rows) + m.group(3) + s[m.end():]

def bank(s):
    return reorder(s, r'<p style="margin:4px 0;"><strong>(?:%s)</strong> &mdash; [^\n]*</p>' % "|".join(ORDER), "word bank")

def day1(s):
    # stray cards after the match check (treaty, scattered)
    s, n = re.subn(r'<div class="vocab-decode-item"><div class="decode-sentence">&ldquo;There is <strong[^>]*>Treaty</strong>.*?(?=\n\s*</div>\s*</div>\s*\n\s*<!-- GRAMMAR)', '', s, flags=re.S)
    if n: log.append("dropped treaty+scattered")
    # the stray cards carried the match-game's closing </div>; put it back
    s = re.sub(r'(<div class="match-feedback" id="matchFeedback">&#x2728; All matched!</div>)\s*\n(\s*</div>\n  </div>\n\n  <!-- GRAMMAR)',
               r'\1\n      </div>\n\2', s, count=1)
    s = reorder(s, r'<div class="vocab-decode-item">\s*<div class="decode-sentence">.*?</div>\s*<div class="flip-card.*?</div>\s*</div>\s*</div>\s*</div>\s*</div>', "day1 cards")
    for w in ORDER:   # chapter tag on each book sentence
        s, n = re.subn(r'(<div class="decode-sentence">&ldquo;(?:(?!</div>).)*<strong style="color:#8B3A20;">%s</strong>(?:(?!</div>).)*?&rdquo;)(</div>)' % w,
                       r'\1 <span class="vocab-ch" style="font-style:normal;font-size:12px;font-weight:700;color:#7A88A8;white-space:nowrap;">Ch. %d</span>\2' % CH[w], s, count=1, flags=re.S)
    s, n = re.subn(r'\s*<p>Seven words from this week&rsquo;s chapters.*?</p>', '', s, count=1, flags=re.S)
    if n: log.append("intro line")
    s = s.replace('Decode &amp; Discover &mdash; words from this week&rsquo;s chapters',
                  'Decode &amp; Discover &mdash; five words you will meet in Chapters 4 and 5', 1)
    s = match_grid(s)
    # one think-question per box
    s = re.sub(r'<p><strong>Try these first:</strong></p>\s*<ul([^>]*)>.*?</ul>',
               r'<p><strong>Try this first:</strong></p>\n      <ul\1>\n      <li>What piece repeats in Group A? What piece repeats in Group B? Cover the rest of each word and read just that piece.</li>\n      </ul>', s, count=1, flags=re.S)
    def first_li(m):
        lis = re.findall(r'<li>.*?</li>', m.group(3), re.S)
        return m.group(1) + m.group(2) + "\n" + lis[0] + "\n" + m.group(4)
    s, n = re.subn(r'(<p><strong>)(Think it through\.</strong></p>\s*<ol[^>]*>)(.*?)(</ol>)', first_li, s, count=1, flags=re.S)
    s, n2 = re.subn(r'(<p><strong>)(Work through these before you read on:</strong></p>\s*<ul[^>]*>)(.*?)(</ul>)', first_li, s, count=1, flags=re.S)
    s = s.replace('Work through these before you read on:', 'Work through this before you read on:')
    log.append("one question x%d" % (1 + n + n2))
    for a, b in [("Think through the three questions.", "Think through the question."),
                 ("Read the sentence and the three questions.", "Read the sentence and the question."),
                 ("Think through the three questions first.", "Think through the question first.")]:
        s = s.replace(a, b)
    return s

def day2(s):
    s = reorder(s, r'<p style="font-size:15px;color:#3A4A6B;line-height:1\.8;margin-bottom:\d+(?:px)?;">&ldquo;[^\n]*?<strong style="color:#8B3A20;">(?:%s)</strong>[^\n]*?</p>' % "|".join(ORDER), "day2 sentences")
    s = re.sub(r'(margin-bottom:)0(;">&ldquo;)', r'\g<1>10px\2', s, count=1)
    ms = list(re.finditer(r'margin-bottom:10px;">&ldquo;[^\n]*?<strong style="color:#8B3A20;">(?:%s)</strong>' % "|".join(ORDER), s))
    last = ms[-1]; s = s[:last.start()] + s[last.start():last.end()].replace("margin-bottom:10px", "margin-bottom:0", 1) + s[last.end():]
    s = s.replace("Read each sentence from Chapters 4–7.", "Read each sentence from Chapters 4 and 5.")
    s = re.sub(r" Both roots show up everywhere in Chapter 1 &mdash;.*?</em>\.", "", s, count=1)  # not true: neither root is in Ch. 1
    return match_grid(s)

def day3(s):
    s = reorder(s, r'<div class="fillin-item">[^\n]*?</div>', "day3 fill-in")
    return s.replace("each sentence from Chapters 1–7", "each sentence from Chapters 4 and 5")

def day4(s):
    return reorder(s, r'<div class="vocab-use-item".*?</textarea>\s*</div>', "day4 use-it")

def common(s):
    s = bank(s) if 'class="vocab-bank"' in s else s
    s, n = re.subn(r'\s*<div class="dol-hint">Tap the highlighted words to see what&rsquo;s correct\.</div>', '', s)
    if n: log.append("dol hint")
    return s

def more(s, d):
    """Second pass (same review): repeats that add reading but not teaching."""
    # vocab lead-in lines on Days 2-4 repeat What to do
    s, n = re.subn(r'\s*<p>(?:You met these words yesterday\.|You have read these words and worked out|You have worked with these words all week\.)[^\n]*?</p>', '', s, count=1)
    if n: log.append("vocab lead-in")
    if d == 4:   # use-it boxes: the meaning, first sentence only (the bank above has the rest)
        for w in ORDER:
            s, n = re.subn(r'(<div style="font-size:18px;font-weight:700;color:#8B3A20;margin-bottom:4px;">%s <span[^>]*>&mdash; )[^<]*(</span>)' % w,
                           lambda m: m.group(1) + SHORT[w] + m.group(2), s, count=1)
        log.append("use-it meanings")
    if d in (2, 3, 4):   # How to Do It is word-for-word Day 1's: closed, one tap away
        s, n = re.subn(r'<div class="key-concept" style="([^"]*)">\s*<div class="key-concept-label" style="color:#3D5285;">🔍 How to Do It</div>\s*(<ol.*?</ol>)\s*</div>',
                       r'<details class="key-concept" style="\1"><summary class="key-concept-label" style="color:#3D5285;cursor:pointer;">🔍 How to Do It &mdash; the same three steps as Day 1 (tap to open)</summary>\n\2\n</details>', s, count=1, flags=re.S)
        if n: log.append("how-to folded")
        s = s.replace("Read the three steps in How to Do It.", "Open How to Do It if you need the steps.")
    return s

for d, f in FILES.items():
    log.clear()
    h = io.open(f, encoding="utf-8", newline="").read()
    h2 = more(common({1: day1, 2: day2, 3: day3, 4: day4}[d](h)), d)
    print(f, "|", ", ".join(log), "| chars %+d" % (len(h2) - len(h)))
    if d in (1, 2):   # DATA file mirrors the inline DATA
        jf = "data/g5ela-18-%d.json" % d; j = io.open(jf, encoding="utf-8").read()
        j = j.replace("Read the three steps in How to Do It.", "Open How to Do It if you need the steps.")
        for a, b in [("Think through the three questions.", "Think through the question."),
                     ("Read the sentence and the three questions.", "Read the sentence and the question."),
                     ("Think through the three questions first.", "Think through the question first.")]:
            j = j.replace(a, b)
        json.loads(j)
        if APPLY: io.open(jf, "w", encoding="utf-8").write(j)
    if APPLY: io.open(f, "w", encoding="utf-8", newline="").write(h2)
print("APPLIED" if APPLY else "dry run")
