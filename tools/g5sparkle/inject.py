#!/usr/bin/env python3
"""
inject.py — add the G5 ELA sparkle layer (The Commonplace Book) to one lesson, in place.

    python tools/g5sparkle/inject.py lesson-18-1-hbg-ch4.html \
        --book hbg --week 18 --day 1 \
        --title "How I Became a Ghost" --chapters "Ch. 1–2"

That is a DRY RUN. Add --apply to write.

What it does, and nothing else:
  1. inserts the lesson declaration (#oao-lesson) and this lesson's DATA (#oao-data) before </head>
     (DATA comes from data/g5ela-<week>-<day>.json; a lesson with no file still builds)
  2. adds " (Sparkle)" to <title>. The title is the page's localStorage key, so it must stay unique.
  3. links g5-sparkle.css / g5-sparkle.js before the LAST </body> at the start of a line
     (G5 pages also write '</body>' inside a JS string for the My Work download)
  4. optionally replaces the epigraph (--quote) with a VERIFIED line

The page's own markup is never rewritten. Delete the injected blocks and the file is what it was.
Refuses to run twice. Keeps the file's own line endings.

Ported Nov 2026 from optima-3rd-ela/tools/inject.py for the g5-ela-sparkle-lesson skill.
"""
import argparse, io, json, os, re, sys

MARK_OPEN = "<!-- ═════════ OAO G5 SPARKLE LAYER (additive) ═════════ -->"
MARK_CLOSE = "<!-- ═════════ END OAO G5 SPARKLE ═════════ -->"
BOOKS = ("witch", "jt", "cmb", "bridge", "hbg", "btghs", "year")


def die(msg):
    sys.exit("inject: " + msg)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("lesson")
    ap.add_argument("--book", required=True, choices=BOOKS)
    ap.add_argument("--week", required=True, type=int)
    ap.add_argument("--day", required=True, help="1-4, fluency or checkin")
    ap.add_argument("--title", required=True)
    ap.add_argument("--chapters", required=True)
    ap.add_argument("--quote")
    ap.add_argument("--data")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    if not os.path.isfile(a.lesson):
        die("no such file: " + a.lesson)
    html = io.open(a.lesson, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in html else "\n"
    before = len(html)
    if MARK_OPEN in html or 'id="oao-lesson"' in html or 'id="oao-data"' in html:
        die("%s already carries the layer. Revert it first: git checkout -- %s" % (a.lesson, a.lesson))
    if a.day not in ("1", "2", "3", "4", "fluency", "checkin"):
        die("--day must be 1-4, fluency or checkin")
    day = int(a.day) if a.day.isdigit() else a.day

    decl = {"grade": 5, "subject": "ela", "book": a.book, "week": a.week, "day": day,
            "bookTitle": a.title, "chapters": a.chapters}
    dpath = a.data or os.path.join("data", "g5ela-%d-%s.json" % (a.week, a.day))
    if os.path.isfile(dpath):
        try:
            data = json.loads(io.open(dpath, encoding="utf-8").read())
        except ValueError as e:
            die("%s is not valid JSON: %s" % (dpath, e))
        note = "%s (%d keys)" % (dpath, len(data))
    else:
        data, note = {}, "none (%s not found)" % dpath

    # 1. declaration + DATA before the one </head>
    hits = [m.start() for m in re.finditer(r"(?m)^</head>\r?$", html)]
    if len(hits) != 1:
        die("expected exactly one </head> line, found %d" % len(hits))
    block = ('<script type="application/json" id="oao-lesson">%s</script>%s'
             '<script type="application/json" id="oao-data">%s</script>%s'
             % (json.dumps(decl, ensure_ascii=False), nl,
                json.dumps(data, ensure_ascii=False, indent=1).replace("</", "<\\/").replace("\n", nl), nl))
    html = html[:hits[0]] + block + html[hits[0]:]

    # 2. title marker
    m = re.search(r"<title>(.*?)</title>", html, re.S)
    if not m:
        die("no <title>")
    if "(Sparkle)" not in m.group(1):
        html = html.replace(m.group(0), "<title>%s (Sparkle)</title>" % m.group(1).strip(), 1)

    # 4. epigraph
    if a.quote:
        qm = re.search(r'(<div class="quote-strip-text">)(.*?)(</div>)', html, re.S)
        if not qm:
            die("--quote given but no .quote-strip-text")
        html = html.replace(qm.group(0), "%s&ldquo;%s&rdquo;%s" % (qm.group(1), a.quote, qm.group(3)), 1)

    # 3. link the layer before the last </body> at the start of a line
    ends = [m.start() for m in re.finditer(r"(?m)^</body>", html)]
    if not ends:
        die("no </body> at the start of a line")
    k = ends[-1]
    link = (MARK_OPEN + nl + '<link rel="stylesheet" href="g5-sparkle.css">' + nl +
            '<script src="g5-sparkle.js" defer></script>' + nl + MARK_CLOSE + nl)
    html = html[:k] + link + html[k:]

    print(a.lesson)
    print("  declaration: wk %d day %s, %s, %s" % (a.week, day, a.book, a.chapters))
    print("  data       : " + note)
    print("  size       : %d -> %d (+%d)" % (before, len(html), len(html) - before))
    if not a.apply:
        print("DRY RUN. Re-run with --apply.")
        return
    io.open(a.lesson, "w", encoding="utf-8", newline="").write(html)
    print("written.")


if __name__ == "__main__":
    main()
