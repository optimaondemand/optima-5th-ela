# G5 ELA Word Study films, week 24 (How I Became a Ghost Ch. 28-29 + source study), Mason. Reuses each lesson's listen-words clip.
# Fresh examples only (replanting, inspector, hopeful, a casual/formal pair): checked against week 24's pages, DATA and check-in.
# No Choctaw words or names on screen.
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
D3 = '<div class="dots6">● ● ●</div>'
V['g5ela-24-1-listen-words'] = dict(title='Word Study', sub='Words a historian uses', scenes=[
 dict(at=None, items=[(None, LAB('📜 Words a historian uses with care')), ('claim, evidence, reasoning', PILLS('claim', 'evidence', 'reasoning')), ('treaty, removal, nation', PILLS('treaty', 'removal', 'nation'))]),
 dict(at='Then formal style', items=[(None, LAB('✏️ Formal style')), ('the way an essay talks', SAY('“According to the letter, …”'))]),
 dict(at='In the game', items=[(None, LAB('🌽 Ears of Corn')), ('peel the husks', ROW(TILE('re'), TILE('plant', 'key'), TILE('ing'))), ('find the base word', ROW(ARW, WD('plant')))]),
])
V['g5ela-24-2-listen-words'] = dict(title='Word Study', sub='Formal or casual?', scenes=[
 dict(at=None, items=[(None, ASK('What does each history word really claim?'))]),
 dict(at='Then tell formal writing', items=[(None, LAB('Formal or casual?')), (None, SAY('“It was super cold.”')), ('from casual talk', SAY('“The winter was severe.”'))]),
 dict(at='sort long words', items=[(None, ROW(TILE('in'), TILE('spect', 'key'), TILE('or'))), ('at their center', DEF('spect', 'look'))]),
 dict(at='Three new ears', items=[(None, LAB('🌽 Three new ears of corn')), (None, D3)]),
])
V['g5ela-24-3-listen-words'] = dict(title='Word Study', sub='Name your source', scenes=[
 dict(at=None, items=[(None, LAB('📜 History words at work')), ('primary source, secondary source', PILLS('primary source', 'secondary source')), ('perspective, bias', PILLS('perspective', 'bias'))]),
 dict(at='Then practice naming', items=[(None, LAB('Name your source first')), ('before every claim', SAY('“<u>According to the treaty,</u> …”'))]),
 dict(at='In the game', items=[(None, ROW(TILE('hope', 'key'), TILE('ful'))), ('stand alone as a word', ROW(ARW, WD('hope')))]),
])
V['g5ela-24-4-listen-words'] = dict(title='Word Study', sub='The exact word', scenes=[
 dict(at=None, items=[(None, ASK('Why does the exact word matter?')), ('when you write about history', PILLS('claim', 'evidence', 'reasoning'))]),
 dict(at='Keep the novel and the record apart', items=[(None, LAB('Keep them apart')), (None, SAY('“In the novel, …”')), ('in every sentence', SAY('“The treaty states, …”'))]),
 dict(at='Then open the last three', items=[(None, LAB('🌽 The last three ears of corn')), (None, D3)]),
])
