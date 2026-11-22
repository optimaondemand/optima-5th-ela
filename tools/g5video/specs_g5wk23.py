# G5 ELA Word Study films, week 23 (How I Became a Ghost Ch. 24-27), Mason. Reuses each lesson's listen-words clip.
# Fresh examples only (voice, making, microscope, hopping): checked against week 23's pages, DATA and check-in.
# voc/voke and dict are named by the page and by Mason, so Day 1 shows them.
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
V['g5ela-23-1-listen-words'] = dict(title='Word Study', sub='Two roots for speaking', scenes=[
 dict(at=None, items=[(None, LAB('🗣️ Two roots this week are about speaking'))]),
 dict(at='Voc, or voke', items=[(None, PILLS('voc · voke = voice, call')), ('Dict means say', PILLS('dict = say'))]),
 dict(at='Then a year of spelling patterns', items=[(None, LAB('🔤 A year of spelling patterns')), ('all in one sort', BINS('suffix', 'prefix', 'schwa'))]),
 dict(at='In the game', items=[(None, LAB('📣 Raise Your Voice')), ('read each line', SAY('“Please raise your ______.”')), ('fits the blank', ROW(ARW, WD('voice')))]),
])
V['g5ela-23-2-listen-words'] = dict(title='Word Study', sub='Calling out or saying?', scenes=[
 dict(at=None, items=[(None, LAB('Calling out, or saying?')), ('calling out', PILLS('voc · voke · calling out')), ('saying and declaring', PILLS('dict · saying, declaring'))]),
 dict(at='Then sort words by the rule', items=[(None, LAB('Sort by the rule')), (None, ROW(TILE('make'), TILE('-ing', 'key'))), ('explains their spelling', ROW(ARW, WD('making')))]),
 dict(at='Then three new lines', items=[(None, LAB('📣 Three new lines')), (None, D3)]),
])
V['g5ela-23-3-listen-words'] = dict(title='Word Study', sub='Words that connect', scenes=[
 dict(at=None, items=[(None, LAB('🗣️ Speaking roots at work'))]),
 dict(at='Then learn how transition words', items=[(None, LAB('🔗 Transition words')), ('but, because and instead', PILLS('but', 'because', 'instead')), ('show how ideas connect', SAY('“The river was cold, <u>but</u> Jumper jumped in.”'))]),
 dict(at='Then check your own draft', items=[(None, LAB('✏️ Check your own draft')), ('one spelling pattern at a time', TL(('1', '-able or -ible?'), ('2', '-er or -or?')))]),
])
V['g5ela-23-4-listen-words'] = dict(title='Word Study', sub='A year of roots', scenes=[
 dict(at=None, items=[(None, LAB('🗣️ Last day with the speaking roots'))]),
 dict(at='Match words to the roots', items=[(None, ROW(TILE('micro'), TILE('scope', 'key'))), ('collected all year', DEF('micro + scope', 'small + look → a tool for seeing tiny things'))]),
 dict(at='Then explain a spelling pattern', items=[(None, ASK('🧑‍🏫 Why does <b>hopping</b> have two p’s?')), ('teach it to a friend', SAY('“Short vowel, one consonant: double it before -ing.”'))]),
 dict(at='finish the last lines', items=[(None, LAB('📣 The last lines of the game')), (None, D3)]),
])
