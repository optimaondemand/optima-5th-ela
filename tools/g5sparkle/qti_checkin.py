#!/usr/bin/env python3
"""qti_checkin.py: build a Canvas QTI 1.2 zip for a G5 ELA weekly check-in, in the same shape
as planning docs/WeekNN_CheckIn_QTI.zip (imsmanifest.xml + <id>/<id>.xml + <id>/assessment_meta.xml).

    python tools/g5sparkle/qti_checkin.py assessments/g5-ela-wk18-checkin.json "planning docs/Week18_CheckIn_QTI.zip"

Reads the check-in JSON (questions with type, points, text, options, answer / answers; optional passage
{before, title, text, cite}). One attempt, unpublished, answers not shown. The idents are derived from
the JSON id, so a rebuild keeps the same quiz identity."""
import hashlib, html, io, json, re, sys, zipfile
from xml.sax.saxutils import escape

src, out = sys.argv[1], sys.argv[2]
d = json.load(io.open(src, encoding="utf-8"))
week = int(re.search(r"wk(\d+)", d["id"]).group(1))
book = d["title"].split("·", 1)[1].strip() if "·" in d["title"] else d["title"]
title = "Week %d Check-In: %s" % (week, book)
h = hashlib.md5(d["id"].encode()).hexdigest()
gid, mid, rid, aid = "g" + h, "m" + h, "r" + h, "a" + h
qs = d["questions"]
total = sum(q["points"] for q in qs)
sec_pts = {}
for q in qs:
    sec_pts[q["section"]] = sec_pts.get(q["section"], 0) + q["points"]

def p(t): return "<p>%s</p>" % html.escape(t, quote=False)
def num(x): return ("%.1f" % x)
def meta(label, val): return "<qtimetadatafield><fieldlabel>%s</fieldlabel><fieldentry>%s</fieldentry></qtimetadatafield>" % (label, val)

items = []
for q in qs:
    n, t = q["n"], q["type"]
    sp = sec_pts[q["section"]]
    body = "<p><strong>%s (%d point%s)</strong></p>" % (html.escape(q["section"], quote=False), sp, "" if sp == 1 else "s")
    P = d.get("passage")
    if P and P.get("before") == n:
        lines = "".join(p(l) for l in P["text"].split("\n"))
        body += "<p><em>%s</em></p><blockquote>%s</blockquote><p><em>%s</em></p>" % (
            html.escape(P["title"], quote=False), lines, html.escape(P["cite"], quote=False))
    body += p(q["text"])
    ident = "i" + hashlib.md5(("%s-%d" % (d["id"], n)).encode()).hexdigest()
    md = meta("question_type", t) + meta("points_possible", num(q["points"]))
    if t in ("multiple_choice_question", "multiple_answers_question"):
        ids = [str(1000 + i) for i in range(len(q["options"]))]
        md += meta("original_answer_ids", ",".join(ids))
        card = "Single" if t == "multiple_choice_question" else "Multiple"
        labels = "".join('<response_label ident="%s"><material><mattext texttype="text/plain">%s</mattext></material></response_label>'
                         % (i, escape(o)) for i, o in zip(ids, q["options"]))
        pres = '<response_lid ident="response1" rcardinality="%s"><render_choice>%s</render_choice></response_lid>' % (card, labels)
        if t == "multiple_choice_question":
            cond = '<varequal respident="response1">%s</varequal>' % ids[q["answer"]]
        else:
            right = set(q["answers"])
            cond = "<and>" + "".join(
                ('<varequal respident="response1">%s</varequal>' % ids[i]) if i in right else
                ('<not><varequal respident="response1">%s</varequal></not>' % ids[i]) for i in range(len(ids))) + "</and>"
        proc = ('<respcondition continue="No"><conditionvar>%s</conditionvar>'
                '<setvar action="Set" varname="SCORE">100</setvar></respcondition>' % cond)
    elif t == "essay_question":
        pres = '<response_str ident="response1" rcardinality="Single"><render_fib><response_label ident="answer1" rshuffle="No"/></render_fib></response_str>'
        proc = '<respcondition continue="No"><conditionvar><other/></conditionvar></respcondition>'
    else:
        sys.exit("unsupported type " + t)
    items.append('<item ident="%s" title="Week %d Question %d"><itemmetadata><qtimetadata>%s</qtimetadata></itemmetadata>'
                 '<presentation><material><mattext texttype="text/html">%s</mattext></material>%s</presentation>'
                 '<resprocessing><outcomes><decvar maxvalue="100" minvalue="0" varname="SCORE" vartype="Decimal"/></outcomes>%s</resprocessing></item>'
                 % (ident, week, n, md, escape(body), pres, proc))

qti = ('<?xml version="1.0" encoding="UTF-8"?>\n<questestinterop xmlns="http://www.imsglobal.org/xsd/ims_qtiasiv1p2" '
       'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.imsglobal.org/xsd/ims_qtiasiv1p2 '
       'http://www.imsglobal.org/xsd/ims_qtiasiv1p2p1.xsd">\n<assessment ident="%s" title="%s"><qtimetadata>%s</qtimetadata>\n'
       '<section ident="root_section">\n%s\n</section>\n</assessment>\n</questestinterop>\n'
       % (gid, escape(title, {'"': "&quot;"}), meta("cc_maxattempts", "1"), "\n".join(items)))
desc = escape(p(d["description"]))
ameta = ('<?xml version="1.0" encoding="UTF-8"?>\n<quiz identifier="%s" xmlns="http://canvas.instructure.com/xsd/cccv1p0" '
         'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://canvas.instructure.com/xsd/cccv1p0 '
         'https://canvas.instructure.com/xsd/cccv1p0.xsd"><title>%s</title><description>%s</description>'
         '<shuffle_answers>false</shuffle_answers><scoring_policy>keep_highest</scoring_policy><quiz_type>assignment</quiz_type>'
         '<points_possible>%s</points_possible><allowed_attempts>1</allowed_attempts><one_question_at_a_time>false</one_question_at_a_time>'
         '<show_correct_answers>false</show_correct_answers><available>false</available><assignment identifier="%s"><title>%s</title>'
         '<points_possible>%s</points_possible><grading_type>points</grading_type><submission_types>online_quiz</submission_types>'
         '<workflow_state>unpublished</workflow_state></assignment></quiz>\n'
         % (gid, escape(title), desc, num(total), aid, escape(title), num(total)))
man = ('<?xml version="1.0" encoding="UTF-8"?>\n<manifest identifier="%s" xmlns="http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1" '
       'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1 '
       'http://www.imsglobal.org/xsd/imscp_v1p1.xsd"><metadata><schema>IMS Content</schema><schemaversion>1.1.3</schemaversion></metadata>'
       '<organizations/><resources><resource identifier="%s" type="imsqti_xmlv1p2"><file href="%s/%s.xml"/><dependency identifierref="%s"/></resource>'
       '<resource identifier="%s" type="associatedcontent/imscc_xmlv1p1/learning-application-resource" href="%s/assessment_meta.xml">'
       '<file href="%s/assessment_meta.xml"/></resource></resources></manifest>\n' % (mid, gid, gid, gid, rid, rid, gid, gid))
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("imsmanifest.xml", man)
    z.writestr("%s/%s.xml" % (gid, gid), qti)
    z.writestr("%s/assessment_meta.xml" % gid, ameta)
print("wrote %s: %s, %d questions, %s points" % (out, title, len(qs), num(total)))
