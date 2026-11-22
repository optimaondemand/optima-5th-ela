# G5 ELA Word Study films, week 22 (How I Became a Ghost Ch. 20-23), Mason. Reuses each lesson's listen-words clip.
# Fresh examples only (telescope, photon, biology, monograph, telephone): checked against week 22's pages, DATA and check-in.
# Day 1 names no root: the spelling sort wants students to notice graph / chron / log first.
def LAB(t): return '<div class="lab">%s</div>' % t
def ASK(t): return '<div class="ask">%s</div>' % t
def SAY(t): return '<div class="say">%s</div>' % t
def WD(t, c=''): return '<div class="wd %s">%s</div>' % (c, t)
def TL(*a): return '<div class="steps">%s</div>' % ''.join('<span><i>%s</i>%s</span>' % x for x in a)
def DEF(w, m): return '<div class="def"><b>%s</b><span>%s</span></div>' % (w, m)
def ROW(*h): return '<div class="parts">%s</div>' % ''.join(h)
ARW = '<span class="glue">→</span>'
def PILLS(*p): return '<div class="chips">%s</div>' % ''.join('<span>%s</span>' % x for x in p)
def BINS(*b): return '<div class="bins">%s</div>' % ''.join('<span>%s</span>' % x for x in b)
V = {}
TILE = lambda t, k='': '<span class="tile %s">%s</span>' % (k, t)
D4 = '<div class="dots6">● ● ● ●</div>'
V['g5ela-22-1-listen-words'] = dict(title='Word Study', sub='Two roots for light', scenes=[
 dict(at=None, items=[(None, LAB('💡 Two roots this week mean light'))]),
 dict(at='One came from Latin', items=[(None, TL(('🏛️', 'one came from Latin'))), ('one from Greek', TL(('🏺', 'one came from Greek')))]),
 dict(at='Then long words about books', items=[(None, LAB('📚 Long words about books')), ('built from parts', ASK('🧩 Built from parts you already know.'))]),
 dict(at='In the lantern game', items=[(None, LAB('🏮 The lantern game')), ('build each word', ROW(TILE('tele'), TILE('scope', 'key'))), ('watch the lantern', ROW(ARW, WD('telescope')))]),
])
V['g5ela-22-2-listen-words'] = dict(title='Word Study', sub='Latin light or Greek light?', scenes=[
 dict(at=None, items=[(None, LAB('Latin light or Greek light?')), ('from Latin or from Greek', PILLS('luc · lum · Latin', 'photo · Greek'))]),
 dict(at='Then sort long book words', items=[(None, LAB('Sort by the root in the center')), ('root at their center', WD('bio<span class="pt">log</span>y'))], hl=[('root at their center', '.pt')]),
 dict(at='Then four new lanterns', items=[(None, LAB('🏮 Four new lanterns')), (None, D4)]),
])
V['g5ela-22-3-listen-words'] = dict(title='Word Study', sub='A word you have never studied', scenes=[
 dict(at=None, items=[(None, LAB('💡 Light words at work'))]),
 dict(at='Then try book words', items=[(None, LAB('A book word you have never studied')), (None, WD('monograph'))]),
 dict(at='Break each one into its parts', items=[(None, ROW(TILE('mono'), TILE('graph', 'key'))), ('work out the meaning', DEF('mono + graph', 'one + write → writing about one subject'))]),
 dict(at='Then four new lanterns', items=[(None, LAB('🏮 Four new lanterns')), (None, D4)]),
])
V['g5ela-22-4-listen-words'] = dict(title='Word Study', sub='Light and understanding', scenes=[
 dict(at=None, items=[(None, LAB('💡 Last day with the light roots'))]),
 dict(at='Explain why writers use light', items=[(None, SAY('“Now I <u>see</u> what you mean.”')), ('talk about understanding', ASK('Why do we talk about understanding as light?'))]),
 dict(at='Then build words of your own', items=[(None, ROW(TILE('tele'), TILE('phone', 'key'))), ('Greek and Latin parts', ROW(ARW, WD('telephone')))]),
 dict(at='light the last lanterns', items=[(None, LAB('🏮 The last lanterns of the week')), (None, D4)]),
])
