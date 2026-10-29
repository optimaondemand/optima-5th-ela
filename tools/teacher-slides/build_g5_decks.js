// Build OAO 5th grade ELA teacher decks (Carry On, Mr. Bowditch, weeks 9-14)
// usage: node build_g5_decks.js data.json qw.json outdir
// Every lesson string comes from data.json (extracted from the lesson HTML).
// The optional Quick Write prompts come from qw.json (authored, checked against the novel).
const pptxgen = require('pptxgenjs');
const fs = require('fs');
const [,, dataPath, qwPath, outDir] = process.argv;
const DATA = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
const QW = JSON.parse(fs.readFileSync(qwPath, 'utf8'));

const C = {
  navy: '0E1C42', cyan: '55C8E8', cyanLight: 'E5F7FC', gold: 'C7922C', goldLight: 'FEF6E8',
  green: '1E8E52', greenLight: 'E8F8EF', purple: '6B4FA8', purpleLight: 'F0E8FF', white: 'FFFFFF',
  offWhite: 'F8FAFC', gray: '475569', lightGray: 'CBD5E1', dark: '1E293B', red: 'B4232C', redLight: 'FDECEC',
};
const NOVEL = { title: 'Carry On, Mr. Bowditch', bg: '0E1C42', accent: '55C8E8', emoji: '🧭' };
const F = 'Calibri';
const W = 13.333, H = 7.5, M = 0.55;           // wide layout, margins
const BODY = 20, SMALL = 17, TITLE = 30;        // big, readable type

// ---------- text fitting ----------
// rough capacity model for Calibri: chars per inch ≈ 120 / fontPt; line height ≈ 1.25 * pt
function cap(wIn, hIn, pt) {
  const cpl = Math.max(10, Math.floor(wIn * 140 / pt));
  const lines = Math.max(1, Math.floor(hIn * 72 / (pt * 1.28)));
  return { cpl, lines };
}
function linesFor(text, cpl) {
  return String(text).split('\n').reduce((n, p) => n + Math.max(1, Math.ceil(p.length / cpl)), 0);
}
// split an array of paragraph strings into pages that fit a box
function paginate(items, wIn, hIn, pt, gapLines = 0.5) {
  const { cpl, lines } = cap(wIn, hIn, pt);
  const pages = []; let cur = []; let used = 0;
  for (const it of items) {
    const n = linesFor(it, cpl) + gapLines;
    if (cur.length && used + n > lines) { pages.push(cur); cur = []; used = 0; }
    if (n > lines) { // one giant paragraph: hard-split by sentences
      const sents = it.match(/[^.!?]+[.!?”"]*\s*/g) || [it];
      let buf = '';
      for (const s of sents) {
        if (linesFor(buf + s, cpl) > lines - 1 && buf) { pages.push([buf.trim()]); buf = ''; }
        buf += s;
      }
      cur = [buf.trim()]; used = linesFor(buf, cpl) + gapLines; continue;
    }
    cur.push(it); used += n;
  }
  if (cur.length) pages.push(cur);
  return pages;
}
// largest font (<= start, >= min) at which all items fit on ONE page
function fitPt(items, wIn, hIn, start = BODY, min = 14) {
  for (let pt = start; pt >= min; pt--) if (paginate(items, wIn, hIn, pt).length === 1) return pt;
  return null;
}

// ---------- slide primitives ----------
let pres;
function base(bg = C.white) {
  const s = pres.addSlide(); s.background = { color: bg }; return s;
}
function header(s, title, kicker, color = C.navy, chip) {
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: W, h: 0.12, fill: { color: C.cyan }, line: { color: C.cyan } });
  if (kicker) s.addText(kicker.toUpperCase(), { x: M, y: 0.3, w: W - 2 * M - 2.6, h: 0.35, fontFace: F, fontSize: 13, bold: true, color: C.gold, charSpacing: 2, margin: 0 });
  s.addText(title, { x: M, y: kicker ? 0.62 : 0.4, w: W - 2 * M - (chip ? 2.7 : 0), h: 0.8, fontFace: F, fontSize: TITLE, bold: true, color, margin: 0, valign: 'top', fit: 'shrink' });
  if (chip) {
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: W - M - 2.5, y: 0.42, w: 2.5, h: 0.5, rectRadius: 0.12, fill: { color: chip.color || C.cyan }, line: { color: chip.color || C.cyan } });
    s.addText(chip.text, { x: W - M - 2.5, y: 0.42, w: 2.5, h: 0.5, fontFace: F, fontSize: 14, bold: true, color: C.white, align: 'center', valign: 'middle', margin: 0 });
  }
  s.addShape(pres.shapes.LINE, { x: M, y: 1.5, w: W - 2 * M, h: 0, line: { color: C.lightGray, width: 1 } });
}
const TOP = 1.7, BOTTOM = H - 0.45;
function card(s, x, y, w, h, fill = C.offWhite, border = C.lightGray) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.08, fill: { color: fill }, line: { color: border, width: 1.25 } });
}
function label(s, text, x, y, w, color = C.gray) {
  s.addText(text.toUpperCase(), { x, y, w, h: 0.32, fontFace: F, fontSize: 13, bold: true, color, charSpacing: 1.5, margin: 0 });
}
// paragraphs -> text runs with bullets optional
function paras(items, pt, opts = {}) {
  const out = [];
  items.forEach((t, i) => {
    const o = { fontFace: F, fontSize: pt, color: opts.color || C.dark, breakLine: i < items.length - 1, paraSpaceAfter: Math.round(pt * 0.45) };
    if (opts.bullet) o.bullet = opts.bullet === true ? { code: '25CF' } : opts.bullet;
    if (typeof t === 'object' && t.runs) { t.runs.forEach((r, j) => { const oo = Object.assign({}, o, r.options, { breakLine: j === t.runs.length - 1 ? o.breakLine : false }); if (j > 0) delete oo.bullet; out.push({ text: r.text, options: oo }); }); }
    else out.push({ text: String(t), options: o });
  });
  return out;
}
function notes(s, text) { if (text) s.addNotes(text); }

// a titled slide whose body is a list of paragraphs; paginates automatically
function textSlides(title, kicker, items, opts = {}) {
  const w = W - 2 * M, h = BOTTOM - TOP - (opts.footer ? 0.6 : 0);
  let pt = fitPt(items, w - 0.5, h - 0.4, opts.pt || 24, 17);
  let pages = pt ? [items] : paginate(items, w - 0.5, h - 0.4, 18);
  pt = pt || 18;
  pages.forEach((pg, i) => {
    const s = base(opts.bg);
    header(s, title + (pages.length > 1 ? `  (${i + 1}/${pages.length})` : ''), kicker, C.navy, opts.chip);
    card(s, M, TOP, w, h, opts.fill || C.offWhite, opts.border || C.lightGray);
    s.addText(paras(pg, pt, { bullet: opts.bullet }), { x: M + 0.25, y: TOP + 0.2, w: w - 0.5, h: h - 0.4, valign: 'top', margin: 0 });
    if (opts.footer) s.addText(opts.footer, { x: M, y: BOTTOM - 0.5, w, h: 0.45, fontFace: F, fontSize: 16, italic: true, color: C.gray, margin: 0 });
    notes(s, opts.notes);
  });
}

// ---------- lesson slides ----------
function titleSlide(L) {
  const s = base(NOVEL.bg);
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: H - 1.25, w: W, h: 1.25, fill: { color: '17295C' }, line: { color: '17295C' } });
  s.addText(`WEEK ${L.week}  ·  DAY ${L.day}  ·  LESSON ${L.week}.${L.day}`, { x: 0.8, y: 1.0, w: 11, h: 0.5, fontFace: F, fontSize: 18, bold: true, color: NOVEL.accent, charSpacing: 3, margin: 0 });
  s.addText(NOVEL.title, { x: 0.8, y: 1.9, w: 11.5, h: 0.9, fontFace: F, fontSize: 44, bold: true, color: C.white, margin: 0 });
  s.addText(`Chapter ${L.chapter} — ${L.chapter_title}`, { x: 0.8, y: 2.85, w: 11.5, h: 0.9, fontFace: F, fontSize: 34, color: C.white, margin: 0 });
  if (L.quote && L.quote.text) {
    s.addText([{ text: L.quote.text, options: { italic: true } }, { text: '  — ' + L.quote.attr, options: { color: NOVEL.accent, fontSize: 16 } }],
      { x: 0.8, y: 4.15, w: 11.6, h: 1.5, fontFace: F, fontSize: 20, color: 'DCE6F5', margin: 0, valign: 'top' });
  }
  s.addText(`${NOVEL.emoji}  Grade 5 ELA  ·  Optima Academy Online`, { x: 0.8, y: H - 1.0, w: 11, h: 0.6, fontFace: F, fontSize: 18, color: 'DCE6F5', margin: 0 });
  notes(s, `Lesson ${L.week}.${L.day}: Chapter ${L.chapter}, "${L.chapter_title}".` + (L.quote ? ` Banner quote: ${L.quote.text} (${L.quote.attr}).` : ''));
}

function objectivesSlide(L) {
  const q = L.intro.find(c => c.objectives.length === 0) || {};
  const o = L.intro.find(c => c.objectives.length) || { objectives: [] };
  const s = base();
  header(s, "Today's Objectives", o.label || `Chapter ${L.chapter}`);
  const lw = 5.2, rw = W - 2 * M - lw - 0.3;
  card(s, M, TOP, lw, BOTTOM - TOP, C.purpleLight, 'D6C8F0');
  label(s, q.label || 'Big Question', M + 0.25, TOP + 0.2, lw - 0.5, C.purple);
  const qItems = [q.title, ...(q.body || [])].filter(Boolean);
  const qpt = fitPt(qItems, lw - 0.5, BOTTOM - TOP - 0.8, 24, 15) || 15;
  s.addText(paras(qItems.map((t, i) => i === 0 ? { runs: [{ text: t, options: { bold: true, color: C.purple } }] } : t), qpt),
    { x: M + 0.25, y: TOP + 0.6, w: lw - 0.5, h: BOTTOM - TOP - 0.8, valign: 'top', margin: 0 });
  const x2 = M + lw + 0.3;
  card(s, x2, TOP, rw, BOTTOM - TOP);
  label(s, 'By the end of this lesson…', x2 + 0.25, TOP + 0.2, rw - 0.5, C.gold);
  const objs = o.objectives.map(t => {
    const m = t.match(/^(.*?:)\s*(.*)$/);
    return m ? { runs: [{ text: m[1] + ' ', options: { bold: true, color: C.navy } }, { text: m[2], options: {} }] } : t;
  });
  const opt = fitPt(o.objectives, rw - 0.5, BOTTOM - TOP - 0.8, BODY, 14) || 14;
  s.addText(paras(objs, opt, { bullet: true }), { x: x2 + 0.25, y: TOP + 0.6, w: rw - 0.5, h: BOTTOM - TOP - 0.8, valign: 'top', margin: 0 });
  notes(s, `Big question: ${q.title || ''} ${(q.body || []).join(' ')}\nObjectives:\n- ${o.objectives.join('\n- ')}`);
}

function wgrdSlide(L) {
  const w = L.wgrd; if (!w) return;
  const items = [...w.body];
  if (w.steps.length) items.push(...w.steps.map(t => '• ' + t));
  if (w.watch && w.watch.length) items.push('Watch for as you read:', ...w.watch.map(t => '• ' + t));
  textSlides('📚 What Good Readers Do', w.strategy || 'Set your reading lens', items, { notes: 'Read the lens aloud before students open their books.' });
}

function dolSlides(L) {
  const d = L.dol; if (!d || !d.model) return;
  // model + notes
  let s = base();
  header(s, '📝 Daily Oral Language — Study What’s Right', 'Correct model — notice what each highlighted part teaches');
  const w = W - 2 * M;
  card(s, M, TOP, w, 1.5, C.greenLight, '9ED9B5');
  const runs = [];
  let rest = d.model;
  // bold the highlighted words in order
  d.notes.forEach(([word]) => {
    const i = rest.indexOf(word);
    if (i >= 0) { if (i) runs.push({ text: rest.slice(0, i) }); runs.push({ text: word, options: { bold: true, color: C.green, underline: { style: 'sng' } } }); rest = rest.slice(i + word.length); }
  });
  if (rest) runs.push({ text: rest });
  s.addText(runs.map(r => ({ text: r.text, options: Object.assign({ fontFace: F, fontSize: 26, color: C.dark }, r.options || {}) })), { x: M + 0.3, y: TOP + 0.1, w: w - 0.6, h: 1.3, valign: 'middle', margin: 0, fit: 'shrink' });
  const nItems = d.notes.filter(n => n[1]).map(([wd, ex]) => ({ runs: [{ text: wd + ' — ', options: { bold: true, color: C.green } }, { text: ex }] }));
  const flat = d.notes.map(([wd, ex]) => wd + ' — ' + ex);
  const pt = fitPt(flat, w - 0.5, BOTTOM - TOP - 1.9, 20, 14) || 14;
  label(s, 'What each highlighted part teaches', M, TOP + 1.65, w);
  s.addText(paras(nItems, pt, { bullet: true }), { x: M + 0.1, y: TOP + 2.0, w: w - 0.2, h: BOTTOM - TOP - 2.0, valign: 'top', margin: 0 });
  notes(s, 'Tap-and-notice only — no answer needed. Ask students why each highlighted word or mark is correct before revealing the explanation.');
  // fix-it x2
  [false, true].forEach(rev => {
    const s2 = base();
    header(s2, '📝 Daily Oral Language — Fix It', rev ? 'Answer revealed' : 'How many errors can you find?', C.navy, { text: rev ? 'ANSWER' : 'CHAT PROMPT', color: rev ? C.green : C.cyan });
    label(s2, 'Needs fixing', M, TOP, w, C.red);
    card(s2, M, TOP + 0.35, w, 1.55, C.redLight, 'F2B8BC');
    s2.addText(d.fix || '', { x: M + 0.3, y: TOP + 0.4, w: w - 0.6, h: 1.45, fontFace: F, fontSize: 26, color: C.dark, valign: 'middle', margin: 0, fit: 'shrink' });
    if (!rev) {
      s2.addText('Rewrite the sentence correctly in your reading journal. Use the model to guide you.', { x: M, y: TOP + 2.2, w, h: 0.6, fontFace: F, fontSize: 20, bold: true, color: C.navy, margin: 0 });
    } else {
      label(s2, '✅ Corrected', M, TOP + 2.15, w, C.green);
      card(s2, M, TOP + 2.5, w, 1.4, C.greenLight, '9ED9B5');
      s2.addText(d.answer || '', { x: M + 0.3, y: TOP + 2.55, w: w - 0.6, h: 1.3, fontFace: F, fontSize: 26, bold: true, color: C.green, valign: 'middle', margin: 0, fit: 'shrink' });
      if (d.fixes) s2.addText(d.fixes, { x: M, y: TOP + 4.05, w, h: BOTTOM - TOP - 4.05, fontFace: F, fontSize: fitPt([d.fixes], w, BOTTOM - TOP - 4.1, 18, 13) || 13, color: C.gray, italic: true, valign: 'top', margin: 0 });
    }
    notes(s2, `Fix-it: ${d.fix}\nCorrected: ${d.answer}\n${d.fixes || ''}`);
  });
}

function poemSlide(L) {
  const p = L.poem; if (!p) return;
  const s = base();
  header(s, '🪶 ' + (p.heading || 'Poetry Corner'), p.title);
  const lw = 6.6, rw = W - 2 * M - lw - 0.3;
  card(s, M, TOP, lw, BOTTOM - TOP, C.goldLight, 'EBD3A2');
  s.addText(p.author, { x: M + 0.25, y: TOP + 0.15, w: lw - 0.5, h: 0.4, fontFace: F, fontSize: 15, italic: true, color: C.gray, margin: 0 });
  const lines = p.lines.map(l => l || ' ');
  const nLines = lines.length;
  const pt = Math.max(13, Math.min(22, Math.floor((BOTTOM - TOP - 0.8) * 72 / (nLines * 1.22))));
  s.addText(lines.map((l, i) => ({ text: l, options: { fontFace: 'Georgia', fontSize: pt, color: C.dark, italic: true, breakLine: i < lines.length - 1 } })),
    { x: M + 0.25, y: TOP + 0.6, w: lw - 0.5, h: BOTTOM - TOP - 0.75, valign: 'top', margin: 0, fit: 'shrink' });
  const x2 = M + lw + 0.3;
  card(s, x2, TOP, rw, BOTTOM - TOP, C.purpleLight, 'D6C8F0');
  label(s, '🧠 Think about this', x2 + 0.25, TOP + 0.2, rw - 0.5, C.purple);
  const qs = p.questions.length ? p.questions : p.intro;
  const qpt = fitPt(qs, rw - 0.5, BOTTOM - TOP - 0.8, BODY, 13) || 13;
  s.addText(paras(qs, qpt), { x: x2 + 0.25, y: TOP + 0.6, w: rw - 0.5, h: BOTTOM - TOP - 0.8, valign: 'top', margin: 0 });
  notes(s, 'Read the poem aloud. Give students a moment to notice before discussing.\n' + p.intro.join(' '));
}

// ---- Quick Write (optional, teacher's choice) ----
function qwSlides(L) {
  const q = QW[`${L.week}.${L.day}`]; if (!q) return;
  const scaffold = ['I think...', 'because...', 'One piece of evidence is...', 'This matters because...'].concat(q.rebut ? ['Someone might disagree, but...'] : []);
  if (L.week === 9 && L.day === 1) {
    textSlides('✏️ Quick Write — How It Works', 'Optional routine · use it on any day you have time', [
      'The Quick Write is optional. Use it when it helps; skip it when the lesson needs the time.',
      '1 minute — read the prompt.',
      '5 minutes — write without stopping. Pick a side and defend it.',
      '1 minute — make ONE revision decision.',
      '3 minutes — share, and listen for someone who disagrees.',
      'In 5th grade, a quick write is not "what happened?" It is "which mattered most — and how do you know?"',
    ], { bg: C.goldLight, fill: C.white, border: 'EBD3A2', notes: 'Introduce once. After today the routine runs on its own when you choose to use it.' });
  }
  let s = base();
  header(s, '✏️ Quick Write (Optional)', 'Read the prompt — 1 minute');
  card(s, M, TOP, W - 2 * M, 2.9, C.goldLight, C.gold);
  s.addText(q.prompt, { x: M + 0.35, y: TOP + 0.15, w: W - 2 * M - 0.7, h: 2.6, fontFace: F, fontSize: fitPt([q.prompt], W - 2 * M - 0.7, 2.5, 28, 18) || 18, color: C.dark, valign: 'middle', margin: 0 });
  label(s, 'Sentence scaffold (use what helps)', M, TOP + 3.15, W - 2 * M, C.gold);
  s.addText(scaffold.join('   →   '), { x: M, y: TOP + 3.5, w: W - 2 * M, h: 0.9, fontFace: F, fontSize: 20, color: C.navy, margin: 0, valign: 'top' });
  notes(s, 'Optional routine. Read the prompt aloud. Remind students: pick a side, defend it with evidence' + (q.rebut ? ', and answer someone who disagrees.' : '.'));
  // writing time
  s = base(C.goldLight);
  s.addText('✏️  Writing Time', { x: M, y: 0.4, w: W - 2 * M, h: 0.8, fontFace: F, fontSize: 36, bold: true, color: C.navy, align: 'center', margin: 0 });
  s.addText('5 minutes — keep your pencil moving!', { x: M, y: 1.15, w: W - 2 * M, h: 0.5, fontFace: F, fontSize: 22, color: C.gold, align: 'center', margin: 0 });
  card(s, M, 1.9, W - 2 * M, 2.4, C.white, C.gold);
  s.addText([{ text: 'Prompt: ', options: { bold: true, color: C.gold } }, { text: q.prompt }], { x: M + 0.3, y: 2.0, w: W - 2 * M - 0.6, h: 2.2, fontFace: F, fontSize: fitPt([q.prompt], W - 2 * M - 0.6, 2.1, 24, 16) || 16, color: C.dark, valign: 'middle', margin: 0 });
  card(s, 3.2, 4.55, W - 6.4, 2.5, C.white, 'EBD3A2');
  s.addText(paras(['Scaffold, if you need it:', ...scaffold], 19), { x: 3.45, y: 4.65, w: W - 6.9, h: 2.3, valign: 'top', margin: 0 });
  notes(s, 'Set a 5-minute timer. Remind: choose a side, defend with evidence.');
  // edit
  s = base(C.greenLight);
  s.addText('🔍  Edit & Revise', { x: M, y: 0.6, w: W - 2 * M, h: 0.8, fontFace: F, fontSize: 36, bold: true, color: C.navy, align: 'center', margin: 0 });
  s.addText('1 minute — one deliberate decision, not a full edit pass', { x: M, y: 1.4, w: W - 2 * M, h: 0.5, fontFace: F, fontSize: 22, color: C.green, align: 'center', margin: 0 });
  card(s, 1.6, 2.4, W - 3.2, 1.9, C.white, C.green);
  s.addText([{ text: "Today's revision check: ", options: { bold: true, color: C.green } }, { text: q.edit_focus }], { x: 1.9, y: 2.5, w: W - 3.8, h: 1.7, fontFace: F, fontSize: 26, color: C.dark, valign: 'middle', align: 'center', margin: 0 });
  s.addText('Revision = improving ideas.   Editing = fixing conventions.   Pick ONE thing.', { x: M, y: 4.8, w: W - 2 * M, h: 0.6, fontFace: F, fontSize: 20, italic: true, color: C.gray, align: 'center', margin: 0 });
  notes(s, 'Focus: ' + q.edit_focus);
  // share
  s = base(C.cyanLight);
  s.addText('🗣️  Share Time', { x: M, y: 0.6, w: W - 2 * M, h: 0.8, fontFace: F, fontSize: 36, bold: true, color: C.navy, align: 'center', margin: 0 });
  s.addText("3 minutes — let's hear your thinking!", { x: M, y: 1.4, w: W - 2 * M, h: 0.5, fontFace: F, fontSize: 22, color: '1B7FA0', align: 'center', margin: 0 });
  card(s, 2.0, 2.4, W - 4.0, 2.6, C.white, C.cyan);
  s.addText(paras(['Raise your hand to share, or paste your writing in the chat.', 'If you disagree with a classmate’s choice, say so respectfully — and give your evidence. That is part of the thinking.'], 22),
    { x: 2.3, y: 2.55, w: W - 4.6, h: 2.3, valign: 'middle', margin: 0 });
  notes(s, 'Call on 3–4 students. Invite respectful disagreement about their choice and defense.');
}

// ---- Word Study ----
function shuffleStable(arr, seed) {
  const a = arr.slice(); let x = seed || 7;
  for (let i = a.length - 1; i > 0; i--) { x = (x * 9301 + 49297) % 233280; const j = Math.floor(x / 233280 * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; }
  // ensure not identical order
  if (a.length > 1 && a.every((v, i) => v === arr[i])) a.push(a.shift());
  return a;
}
function strandColor(title) {
  if (/Morph/i.test(title)) return C.purple;
  if (/Vocab/i.test(title)) return '1B7FA0';
  if (/Gramm/i.test(title)) return C.gold;
  return C.navy;
}
function teachSlide(A, kicker) {
  // explanatory text from the activity (minus instruction-y lines that only make sense on screen)
  const drop = /^(Tap|Type your answer|Practice:|Quick Match!|Drag|Click|Sort the|Combine them\. Type)/i;
  const items = A.text.filter(t => !drop.test(t) && t.length > 3);
  if (A.tasks && !A.text.some(t => /^Before$/i.test(t))) A.tasks.forEach(t => items.push(t.replace(/^Before\s*/i, 'Before: ').replace(/\s*After\s*/i, '\nAfter: ')));
  if (!items.length) return;
  textSlides(A.title, kicker || A.sub, items, { notes: `${A.title} — ${A.sub}. Teach from this slide; the practice follows.` });
}
function revealPair(A, kind, renderQ, renderA, noteQ, noteA) {
  [false, true].forEach(rev => {
    const s = base();
    header(s, A.title, (A.sub || '') + (rev ? '  ·  answers' : ''), C.navy, { text: rev ? 'ANSWERS' : 'CHAT PROMPT', color: rev ? C.green : C.cyan });
    (rev ? renderA : renderQ)(s);
    notes(s, rev ? noteA : noteQ);
  });
}
function grid(s, cells, cols, opts = {}) {
  const w = W - 2 * M, gap = 0.2;
  const cw = (w - gap * (cols - 1)) / cols;
  const rows = Math.ceil(cells.length / cols);
  const ch = Math.min(opts.maxH || 1.6, (BOTTOM - (opts.top || TOP) - gap * (rows - 1)) / rows);
  cells.forEach((c, i) => {
    const x = M + (i % cols) * (cw + gap), y = (opts.top || TOP) + Math.floor(i / cols) * (ch + gap);
    card(s, x, y, cw, ch, c.fill || C.offWhite, c.border || C.lightGray);
    s.addText(c.runs, { x: x + 0.2, y: y + 0.08, w: cw - 0.4, h: ch - 0.16, valign: 'middle', margin: 0, fit: 'shrink' });
  });
}
function run(t, o = {}) { return Object.assign({ text: t, options: Object.assign({ fontFace: F, fontSize: o.size || BODY, color: o.color || C.dark, bold: !!o.bold, italic: !!o.italic, breakLine: !!o.br }) }); }

function matchSlides(A) {
  const pairs = A.match.filter(p => p[0] && p[1]); if (!pairs.length) return;
  const defs = shuffleStable(pairs.map(p => p[1]), pairs.length * 13);
  const letters = 'ABCDEFGH';
  revealPair(A, 'match',
    s => {
      label(s, 'Match each word to its meaning', M, TOP, 6);
      pairs.forEach((p, i) => {
        const y = TOP + 0.45 + i * ((BOTTOM - TOP - 0.45) / pairs.length);
        const hh = (BOTTOM - TOP - 0.45) / pairs.length - 0.15;
        card(s, M, y, 3.6, hh, C.purpleLight, 'D6C8F0');
        s.addText(`${i + 1}. ${p[0]}`, { x: M + 0.2, y, w: 3.3, h: hh, fontFace: F, fontSize: 22, bold: true, color: C.purple, valign: 'middle', margin: 0, fit: 'shrink' });
        card(s, M + 3.9, y, W - 2 * M - 3.9, hh);
        s.addText(`${letters[i]}. ${defs[i]}`, { x: M + 4.1, y, w: W - 2 * M - 4.3, h: hh, fontFace: F, fontSize: 19, color: C.dark, valign: 'middle', margin: 0, fit: 'shrink' });
      });
    },
    s => {
      label(s, 'Matched', M, TOP, 6, C.green);
      pairs.forEach((p, i) => {
        const y = TOP + 0.45 + i * ((BOTTOM - TOP - 0.45) / pairs.length);
        const hh = (BOTTOM - TOP - 0.45) / pairs.length - 0.15;
        card(s, M, y, W - 2 * M, hh, C.greenLight, '9ED9B5');
        s.addText([run(p[0] + '  =  ', { bold: true, color: C.green, size: 22 }), run(p[1], { size: 20 })], { x: M + 0.25, y, w: W - 2 * M - 0.5, h: hh, valign: 'middle', margin: 0, fit: 'shrink' });
      });
    },
    'Students match each word to its meaning. Letters are scrambled.',
    'Answers:\n' + pairs.map(p => `${p[0]} = ${p[1]}`).join('\n'));
}
function sortSlides(A) {
  const cols = A.sort.columns; if (!cols.length) return;
  revealPair(A, 'sort',
    s => {
      label(s, 'Sort these words', M, TOP, 6);
      const bank = A.sort.bank;
      card(s, M, TOP + 0.4, W - 2 * M, 1.6, C.cyanLight, 'A6DDEE');
      s.addText(bank.join('     ·     '), { x: M + 0.3, y: TOP + 0.45, w: W - 2 * M - 0.6, h: 1.5, fontFace: F, fontSize: fitPt([bank.join('  ·  ')], W - 2 * M - 0.6, 1.4, 26, 16) || 16, bold: true, color: C.navy, align: 'center', valign: 'middle', margin: 0 });
      label(s, 'Into these groups', M, TOP + 2.25, 6);
      grid(s, cols.map(c => ({ runs: [run(c.header, { bold: true, color: C.navy, size: 22 })] })), cols.length, { top: TOP + 2.65, maxH: 1.2 });
    },
    s => {
      const w = W - 2 * M, gap = 0.2, cw = (w - gap * (cols.length - 1)) / cols.length;
      cols.forEach((c, i) => {
        const x = M + i * (cw + gap);
        card(s, x, TOP, cw, BOTTOM - TOP, C.greenLight, '9ED9B5');
        s.addText([run(c.header, { bold: true, color: C.green, size: 21, br: true }), run(' ', { size: 8, br: true }), ...c.words.map((wd, j) => run(wd, { size: 22, br: j < c.words.length - 1 }))],
          { x: x + 0.2, y: TOP + 0.15, w: cw - 0.4, h: BOTTOM - TOP - 0.3, valign: 'top', margin: 0, fit: 'shrink' });
      });
    },
    'Students sort the words into the groups before you reveal.',
    'Sorted:\n' + cols.map(c => `${c.header}: ${c.words.join(', ')}`).join('\n'));
}
function choiceLikeSlides(A, qs, kindLabel) {
  // qs: [{prompt, options:[{text,correct,why}]}]
  const maxPer = qs.some(q => (q.prompt + q.options.map(o => o.text).join(' ')).length > 260) ? 2 : 3;
  const per = Math.ceil(qs.length / Math.ceil(qs.length / maxPer));
  for (let i = 0; i < qs.length; i += per) {
    const chunk = qs.slice(i, i + per);
    const part = qs.length > per ? ` (${Math.floor(i / per) + 1}/${Math.ceil(qs.length / per)})` : '';
    const B = Object.assign({}, A, { title: A.title + part });
    const draw = rev => s => {
      const top = TOP, hh = (BOTTOM - top) / chunk.length - 0.18;
      chunk.forEach((q, k) => {
        const y = top + k * (hh + 0.18);
        card(s, M, y, W - 2 * M, hh, C.offWhite);
        const runs = [];
        if (q.prompt) runs.push(run(`${i + k + 1}. ${q.prompt}`, { bold: true, color: C.navy, size: 20, br: true }));
        q.options.forEach((o, j) => {
          const good = rev && o.correct;
          runs.push(run((good ? '✅ ' : '◻ ') + o.text, { size: 19, color: good ? C.green : (rev ? C.gray : C.dark), bold: good, br: j < q.options.length - 1 }));
        });
        s.addText(runs, { x: M + 0.25, y: y + 0.08, w: W - 2 * M - 0.5, h: hh - 0.16, valign: 'middle', margin: 0, fit: 'shrink', paraSpaceAfter: 4 });
      });
    };
    revealPair(B, kindLabel, draw(false), draw(true), 'Students choose before you reveal.',
      'Answers:\n' + chunk.map((q, k) => `${i + k + 1}. ${q.options.filter(o => o.correct).map(o => o.text).join(' / ')}` + (q.options.find(o => o.correct && o.why) ? ` — ${q.options.find(o => o.correct).why}` : '')).join('\n'));
  }
}
function inlineSpotSlides(A, q) {
  const draw = rev => s => {
    card(s, M, TOP, W - 2 * M, 0.9, C.cyanLight, 'A6DDEE');
    s.addText(q.prompt, { x: M + 0.25, y: TOP + 0.05, w: W - 2 * M - 0.5, h: 0.8, fontFace: F, fontSize: 20, bold: true, color: C.navy, valign: 'middle', margin: 0, fit: 'shrink' });
    card(s, M, TOP + 1.1, W - 2 * M, BOTTOM - TOP - 1.1);
    const runs = [];
    q.options.forEach((o, i) => runs.push(run(o.text + (i < q.options.length - 1 ? ' ' : ''), { size: 28, bold: rev && o.correct, color: rev && o.correct ? C.red : C.dark })));
    s.addText(runs, { x: M + 0.35, y: TOP + 1.25, w: W - 2 * M - 0.7, h: BOTTOM - TOP - 1.4, valign: 'top', margin: 0, fit: 'shrink', lineSpacingMultiple: 1.3 });
  };
  revealPair(A, 'inline', draw(false), draw(true), 'Students find the words to tap before you reveal.',
    'Words to tap: ' + q.options.filter(o => o.correct).map(o => o.text + (o.why ? ` (${o.why})` : '')).join('; '));
}
function fillSlides(A) {
  const items = A.fill.filter(f => f.answer); if (!items.length) return;
  const show = (f, rev) => {
    const parts = f.text.split(/⟦|⟧/);
    // parts: before, answer, after
    return [run(parts[0] || '', { size: 22 }), run(rev ? (parts[1] || f.answer) : '_______', { size: 22, bold: true, color: rev ? C.green : C.navy }), run(parts.slice(2).join('') || '', { size: 22 })];
  };
  revealPair(A, 'fill',
    s => {
      let y = TOP;
      if (A.bank) { s.addText(A.bank, { x: M, y, w: W - 2 * M, h: 0.5, fontFace: F, fontSize: 20, italic: true, color: C.gold, margin: 0 }); y += 0.6; }
      const hh = (BOTTOM - y) / items.length - 0.15;
      items.forEach((f, i) => { card(s, M, y + i * (hh + 0.15), W - 2 * M, hh); s.addText([run(`${i + 1}.  `, { size: 22, bold: true, color: C.gray }), ...show(f, false)], { x: M + 0.25, y: y + i * (hh + 0.15), w: W - 2 * M - 0.5, h: hh, valign: 'middle', margin: 0, fit: 'shrink' }); });
    },
    s => {
      let y = TOP; if (A.bank) y += 0.6;
      const hh = (BOTTOM - y) / items.length - 0.15;
      items.forEach((f, i) => { card(s, M, y + i * (hh + 0.15), W - 2 * M, hh, C.greenLight, '9ED9B5'); s.addText([run(`${i + 1}.  `, { size: 22, bold: true, color: C.gray }), ...show(f, true)], { x: M + 0.25, y: y + i * (hh + 0.15), w: W - 2 * M - 0.5, h: hh, valign: 'middle', margin: 0, fit: 'shrink' }); });
    },
    'Students fill each blank before you reveal.',
    'Answers: ' + items.map((f, i) => `${i + 1}. ${f.answer}`).join('  '));
}
function cardsSlide(A) {
  const cs = A.cards.filter(c => c.word); if (!cs.length) return;
  const s = base();
  header(s, A.title, A.sub);
  const cols = cs.length > 4 ? 3 : 2;
  grid(s, cs.map(c => ({ runs: [run(c.word, { bold: true, color: '1B7FA0', size: 24, br: true }), run(c.def || '', { size: 18, br: !!c.ex }), ...(c.ex ? [run(c.ex, { size: 16, italic: true, color: C.gray })] : [])], fill: C.cyanLight, border: 'A6DDEE' })), cols, { maxH: 2.6 });
  notes(s, 'Word cards. Have students say each word, then use it in a sentence about the chapter.\n' + cs.map(c => `${c.word}: ${c.def}`).join('\n'));
}
function menuSlide(A) {
  const s = base();
  header(s, A.title, 'Choose one way to show what you know');
  grid(s, A.menu.map(([t, d], i) => ({ runs: [run(`Option ${i + 1}: ${t}`, { bold: true, color: C.navy, size: 21, br: true }), run(d, { size: 18 })] })), 2, { maxH: 2.6 });
  notes(s, 'Choice board. Students pick one option.');
}
function swykSlide(A) {
  const k = A.swyk; if (!k || !k.prompt) return;
  textSlides('⭐ ' + (k.label || 'Show What You Know'), 'Graded today', [k.prompt, ...(k.task ? ['What to write: ' + k.task] : [])],
    { fill: C.goldLight, border: C.gold, chip: { text: 'SWYK', color: C.gold }, notes: 'This is the graded Show What You Know for today. Students write it in the Word Study tab.' });
}
function wordStudy(L) {
  L.words.forEach(A => {
    teachSlide(A);
    if (A.cards) cardsSlide(A);
    if (A.match) matchSlides(A);
    if (A.sort) sortSlides(A);
    if (A.fill) fillSlides(A);
    if (A.spot) {
      const inl = A.spot.filter(q => q.options.length > 4), reg = A.spot.filter(q => q.options.length <= 4);
      inl.forEach(q => inlineSpotSlides(A, q));
      if (reg.length) choiceLikeSlides(A, reg.map(q => ({ prompt: q.prompt, options: q.options })), 'spot');
    }
    if (A.choice) choiceLikeSlides(A, A.choice, 'choice');
    if (A.menu) menuSlide(A);
    if (A.swyk) swykSlide(A);
  });
}

function rwmSlides(L) {
  const r = L.rwm; if (!r || !r.sentence) return;
  const s = base();
  header(s, '🔍 RWM — Read like a Reader, Read like a Writer, Mimic', `Mentor sentence · Chapter ${L.chapter}`);
  card(s, M, TOP, W - 2 * M, 1.6, C.goldLight, C.gold);
  s.addText(r.sentence, { x: M + 0.3, y: TOP + 0.1, w: W - 2 * M - 0.6, h: 1.4, fontFace: 'Georgia', fontSize: 24, italic: true, color: C.dark, valign: 'middle', margin: 0, fit: 'shrink' });
  const steps = r.steps.map(([l, t]) => ({ l, t }));
  const w = (W - 2 * M - 0.4) / Math.max(1, steps.length);
  steps.forEach((st, i) => {
    const x = M + i * (w + 0.2), y = TOP + 1.85;
    card(s, x, y, w, BOTTOM - y);
    s.addText([run(st.l, { bold: true, color: C.navy, size: 19, br: true }), run(st.t, { size: 16 })], { x: x + 0.2, y: y + 0.1, w: w - 0.4, h: BOTTOM - y - 0.2, valign: 'top', margin: 0, fit: 'shrink' });
  });
  notes(s, 'Read the sentence aloud twice. Work through Reader → Writer → Mimic.');
  if (r.frame) {
    const s2 = base();
    header(s2, '🖊️ Mimic — Your Turn', 'Use the same technique in your own sentence');
    card(s2, M, TOP, W - 2 * M, 1.4, C.goldLight, C.gold);
    s2.addText(r.sentence, { x: M + 0.3, y: TOP + 0.1, w: W - 2 * M - 0.6, h: 1.2, fontFace: 'Georgia', fontSize: 22, italic: true, color: C.dark, valign: 'middle', margin: 0, fit: 'shrink' });
    const mimic = r.steps.find(st => /Mimic/i.test(st[0]));
    if (mimic) s2.addText(mimic[1], { x: M, y: TOP + 1.6, w: W - 2 * M, h: 1.6, fontFace: F, fontSize: fitPt([mimic[1]], W - 2 * M, 1.5, 22, 15) || 15, color: C.dark, margin: 0, valign: 'top' });
    label(s2, 'Sentence frame', M, TOP + 3.35, 6, C.gold);
    card(s2, M, TOP + 3.7, W - 2 * M, 1.2, C.white, C.gold);
    s2.addText(r.frame, { x: M + 0.3, y: TOP + 3.75, w: W - 2 * M - 0.6, h: 1.1, fontFace: F, fontSize: 26, bold: true, color: C.navy, valign: 'middle', margin: 0, fit: 'shrink' });
    notes(s2, 'Students write their own sentence in the reading journal.');
  }
}

function readingSlide(L) {
  const R = L.reading;
  const items = [];
  if (L.tracker) items.push(L.tracker);
  if (R.intro && R.intro.length) items.push(...R.intro.filter(t => !/^Read these first/.test(t)).map(t => t.replace(/\s*Read these first\..*$/, '')));
  else if (R.summary) items.push(R.summary);
  textSlides('📖 Reading Focus', (R.title || `Read: Chapter ${L.chapter}`).replace(/^Read:\s*/, ''), items, { fill: C.cyanLight, border: 'A6DDEE', notes: 'Set up the reading. Students open their novels to Chapter ' + L.chapter + '.' });
  if (R.pauses.length) {
    textSlides('⏸️ Pause & Think', `Stopping points in Chapter ${L.chapter}`, R.pauses.map(([l, q]) => ({ runs: [run((l || '').replace(/^⏸️\s*/, '') + ': ', { bold: true, color: C.navy }), run(q)] })).map(x => x),
      { fill: C.purpleLight, border: 'D6C8F0', notes: 'Preview the stopping points before students read, so they know where to pause.' });
  }
}
// textSlides with run objects: paginate needs plain strings for measuring
const _textSlides = textSlides;
textSlides = function (title, kicker, items, opts) {
  const plain = items.map(t => (typeof t === 'object' && t.runs) ? t.runs.map(r => r.text).join('') : t);
  if (items.every(t => typeof t === 'string')) return _textSlides(title, kicker, items, opts);
  // rich: fit or split evenly by measurement on plain strings
  const w = W - 2 * M, h = BOTTOM - TOP;
  let pt = fitPt(plain, w - 0.5, h - 0.4, (opts && opts.pt) || 24, 17);
  const pages = pt ? [items] : (() => { const pp = paginate(plain, w - 0.5, h - 0.4, 18); let k = 0; return pp.map(pg => pg.map(() => items[k++])); })();
  pt = pt || 18;
  pages.forEach((pg, i) => {
    const s = base(opts.bg);
    header(s, title + (pages.length > 1 ? `  (${i + 1}/${pages.length})` : ''), kicker, C.navy, opts.chip);
    card(s, M, TOP, w, h, opts.fill || C.offWhite, opts.border || C.lightGray);
    s.addText(paras(pg.map(x => typeof x === 'object' ? { runs: x.runs.map(r => ({ text: r.text, options: Object.assign({}, r.options, { fontSize: pt }) })) } : x), pt), { x: M + 0.25, y: TOP + 0.2, w: w - 0.5, h: h - 0.4, valign: 'top', margin: 0 });
    notes(s, opts.notes);
  });
};

function partASlide(L) {
  const qs = L.assign.partA; if (!qs.length) return;
  textSlides('Comprehension Questions — Preview', (L.assign.partA_title || 'Part A') + ' · what students will answer', qs.map((q, i) => ({ runs: [run(`${i + 1}.  `, { bold: true, color: C.gold }), run(q)] })),
    { notes: 'Preview only. Students answer these after reading, in the Assignment tab.' });
}
function workshopSlides(L) {
  const ws = L.assign.workshop; if (!ws) return;
  const items = [];
  ws.sections.forEach(([lab, txt]) => {
    if (!txt) return;
    items.push(lab ? { runs: [run(lab.replace(/^[^\w“"]+/, '') + ': ', { bold: true, color: C.gold }), run(txt)] } : txt);
  });
  if (!items.length) return;
  textSlides('✍️ ' + ws.title, (ws.stage ? `Stage: ${ws.stage} · ` : '') + (ws.sub || ''), items, { fill: C.goldLight, border: 'EBD3A2', notes: `Writer’s Workshop — ${ws.stage}: ${ws.sub}` });
}

function buildLesson(L) {
  pres = new pptxgen();
  pres.layout = 'LAYOUT_WIDE';
  pres.author = 'Optima Academy Online';
  pres.title = `Lesson ${L.week}.${L.day} — Carry On, Mr. Bowditch, Chapter ${L.chapter}`;
  titleSlide(L);
  objectivesSlide(L);
  wgrdSlide(L);
  dolSlides(L);
  poemSlide(L);
  qwSlides(L);
  wordStudy(L);
  rwmSlides(L);
  readingSlide(L);
  partASlide(L);
  workshopSlides(L);
  const name = L.file.replace(/\.html$/, '-slides.pptx');
  return pres.writeFile({ fileName: `${outDir}/${name}` }).then(() => name);
}

(async () => {
  fs.mkdirSync(outDir, { recursive: true });
  const only = process.env.ONLY;
  for (const L of DATA) {
    if (only && `${L.week}.${L.day}` !== only) continue;
    const n = await buildLesson(L);
    console.log('built', n);
  }
})();
