# G5 ELA Word Study films, weeks 18-21 (How I Became a Ghost), Mason. Reuses each lesson's listen-words clip.
# Rules and fresh examples only: every example word was checked against that week's pages, DATA and check-in.
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
# ── Week 18 · mem/memor + script/scrib · open and closed beats · Stones in the River
V['g5ela-18-1-listen-words'] = dict(title='Word Study', sub='Two hidden word parts', scenes=[
 dict(at=None, items=[(None, LAB('📖 Two word parts run through the whole book'))]),
 dict(at='One is about remembering', items=[(None, TL(('🧠', 'one is about remembering'))), ('One is about writing', TL(('✍️', 'one is about writing')))]),
 dict(at='Isaac is doing both', items=[(None, SAY('Isaac remembers… and writes it all down.')), ('Try to find them', ASK('🔍 Find both parts before the page tells you.'))]),
 dict(at='When you get to the river game', items=[(None, LAB('🪨 The river game')), ('say each word slowly', WD('<span>nap</span><span class="pt">kin</span>')), ('listen for where', ASK('Where does your voice stop?'))], dots='listen for where'),
])
V['g5ela-18-2-listen-words'] = dict(title='Word Study', sub='Match the word to its root', scenes=[
 dict(at=None, items=[(None, LAB('🧩 Match each word to its root')), ('match each word', ROW(WD('<span class="pt">scrib</span>ble'), ARW, DEF('scrib', 'write')))], hl=[('to its root', '.pt')]),
 dict(at="you read this week's words", items=[(None, SAY('📖 Then read the week’s words inside sentences from the book.'))]),
 dict(at='In the river game', items=[(None, LAB('🪨 The river game')), ('say each word slowly', WD('<span>ro</span><span class="pt">bot</span>')), ('listen for where', ASK('Where does your voice stop?'))], dots='listen for where'),
])
V['g5ela-18-3-listen-words'] = dict(title='Word Study', sub='Roots at work', scenes=[
 dict(at=None, items=[(None, LAB('✏️ Build appositives yourself')), ('build appositives', SAY('Mason, <u>a mapmaker from the coast</u>, packed his maps.'))]),
 dict(at='use your roots', items=[(None, WD('pre<span class="pt">script</span>ion')), ('words you have never seen', DEF('script', 'write → written ahead of time'))], hl=[('use your roots', '.pt')]),
 dict(at='The river game has root stones', items=[(None, LAB('🪨 Root stones')), ('Tap only the letters', WD('<span class="pt">mem</span>os'))], hl=[('letters of the root', '.pt')]),
])
V['g5ela-18-4-listen-words'] = dict(title='Word Study', sub='Last day with these roots', scenes=[
 dict(at=None, items=[(None, LAB('🏁 Last day with mem and script'))]),
 dict(at='Build the words from their pieces', items=[(None, ROW('<span class="tile">in</span>', '<span class="tile key">scrib</span>', '<span class="tile">e</span>')), ('then use', ROW(ARW, WD('inscribe')))]),
 dict(at="use this week's words in your own", items=[(None, ASK('✏️ This week’s words, your own sentences.'))]),
 dict(at='Finish your river crossing', items=[(None, LAB('🪨 Finish the crossing')), (None, '<div class="dots6">● ● ● ● ● ●</div>')]),
])
# ── Week 19 · anim + spir · -ive/-al/-ic · Footprints
V['g5ela-19-1-listen-words'] = dict(title='Word Study', sub='Life and breath', scenes=[
 dict(at=None, items=[(None, LAB('🌱 Two roots this week'))]),
 dict(at='One means life', items=[(None, TL(('🌱', 'one means life'))), ('One means breath', TL(('🌬️', 'one means breath'))), ('Long ago', SAY('Long ago, people thought those were almost the same thing.'))]),
 dict(at='Look for them', items=[(None, ASK('🔍 Look in words you already know.'))]),
 dict(at='Then three endings', items=[(None, LAB('Three endings make a describing word')), (None, PILLS('-ive', '-al', '-ic'))]),
 dict(at='In the footprint game', items=[(None, LAB('👣 The footprint game')), ('say each word out loud', ROW(WD('fest'), '<span class="glue">+</span>', WD('ive', 'on'))), ('before you pick', ASK('🗣️ Say it first. Then pick.'))]),
])
V['g5ela-19-2-listen-words'] = dict(title='Word Study', sub='Which root is hiding?', scenes=[
 dict(at=None, items=[(None, PILLS('anim · life', 'spir · breath'))]),
 dict(at='Now decide which one', items=[(None, ROW(WD('<span class="pt">anim</span>ated'), ARW, DEF('anim', 'life'))), ('Some words carry both', ASK('Some words carry both ideas.'))], hl=[('hiding in each word', '.pt')]),
 dict(at='Then sort the describing words', items=[(None, WD('<span class="pt">comic</span>al')), ('Find the smaller word', ASK('🔍 Find the smaller word inside first.'))], hl=[('Find the smaller word', '.pt')]),
 dict(at='Then the footprint game', items=[(None, LAB('👣 Six new words to build')), (None, '<div class="dots6">● ● ● ● ● ●</div>')]),
])
V['g5ela-19-3-listen-words'] = dict(title='Word Study', sub='Build it in your head', scenes=[
 dict(at=None, items=[(None, LAB('🌱 Put the roots to work'))]),
 dict(at='In Spelling', items=[(None, LAB('New spelling words')), ('Build each describing word', ASK('🧠 Build it in your head first.'))]),
 dict(at='If the base ends in a silent e', items=[(None, ROW(WD('expens<s>e</s>'), '<span class="glue">+ ive</span>')), ('check whether it stays', ROW(ARW, WD('expensive')))]),
 dict(at='The footprint game works', items=[(None, LAB('👣 Same in the footprint game'))]),
])
V['g5ela-19-4-listen-words'] = dict(title='Word Study', sub='Watch the base', scenes=[
 dict(at=None, items=[(None, LAB('🌬️ Last day with life and breath'))]),
 dict(at='Today you explain', items=[(None, ASK('One idea, two roots. Why?'))]),
 dict(at='In Spelling', items=[(None, LAB('Watch the base when an ending is added'))]),
 dict(at='Sometimes a silent e drops', items=[(None, ROW(WD('arriv<s>e</s>'), ARW, WD('arrival'))), ('Sometimes the base changes more', ROW(WD('metal'), ARW, WD('metal<span class="pt">l</span>ic'))), ('Sometimes nothing changes', ROW(WD('acrobat'), ARW, WD('acrobatic')))], hl=[('Sometimes the base changes more', '.pt')]),
 dict(at='Look closely at the base', items=[(None, ASK('🔍 Look closely at the base each time.'))]),
])
# ── Week 20 · path + sens · stress shift · schwa · Council Fire
V['g5ela-20-1-listen-words'] = dict(title='Word Study', sub='Two feeling roots', scenes=[
 dict(at=None, items=[(None, LAB('❤️ Two roots about feeling'))]),
 dict(at='One leans toward emotion', items=[(None, TL(('❤️', 'path · emotion'))), ('One leans toward the senses', TL(('👁️', 'sens · the senses')))]),
 dict(at='Then listen to long words', items=[(None, LAB('When a word grows, its strong beat can move')), ('When a word grows', WD('ad·<span class="st">MIRE</span>')), ('its strongest beat can move', WD('ad·mi·<span class="st">RA</span>·tion'))]),
 dict(at='In the council fire game', items=[(None, LAB('🔥 The council fire game')), ('say each word out loud', WD('<span class="st">SEN</span>·sor')), ('tap the beat', ASK('Tap the beat you say the strongest.'))]),
])
V['g5ela-20-2-listen-words'] = dict(title='Word Study', sub='Emotion or the senses?', scenes=[
 dict(at=None, items=[(None, LAB('Which feeling root?')), ('the one for emotion', TL(('❤️', 'path · emotion'))), ('or the one for the senses', TL(('👁️', 'sens · the senses')))]),
 dict(at='Then sort words by where the stress', items=[(None, BINS('strong 1st beat', 'strong 2nd beat'))]),
 dict(at='Say each word twice', items=[(None, ROW(WD('<span class="st">COM</span>·pose'), '<span class="glue no">✗</span>')), ('leaning on a different beat', ROW(WD('com·<span class="st">POSE</span>'), '<span class="glue yes">✓</span>')), ('Only one way sounds right', ASK('Only one way sounds right.'))]),
])
V['g5ela-20-3-listen-words'] = dict(title='Word Study', sub='Bring the quiet vowel back', scenes=[
 dict(at=None, items=[(None, LAB('❤️ Feeling roots at work'))]),
 dict(at='Then the spelling words', items=[(None, WD('comp<span class="blank"></span>sition')), ('say a related word', ROW(ARW, WD('com·<span class="st">POSE</span>'))), ('The vowel comes back', WD('comp<span class="pt">o</span>sition'))], hl=[('The vowel comes back', '.pt')]),
 dict(at='The council fire game uses', items=[(None, LAB('🔥 Same trick in the council fire game'))]),
])
V['g5ela-20-4-listen-words'] = dict(title='Word Study', sub='Find a loud relative', scenes=[
 dict(at=None, items=[(None, LAB('❤️ Last day with the feeling roots'))]),
 dict(at='Explain the difference', items=[(None, TL(('🤝', 'feeling with someone'))), ('feeling from inside', TL(('🫶', 'feeling from inside their experience'))), ('feeling from inside', ASK('Explain the difference in your own words.'))]),
 dict(at='In spelling', items=[(None, WD('adm<span class="blank"></span>ration')), ('Find a relative', ROW(ARW, WD('ad·<span class="st">MIRE</span>'))), ('makes it loud', WD('adm<span class="pt">i</span>ration'))], hl=[('makes it loud', '.pt')]),
])
# ── Week 21 · vis + spect · homophones · The Spyglass
V['g5ela-21-1-listen-words'] = dict(title='Word Study', sub='Two sight roots', scenes=[
 dict(at=None, items=[(None, LAB('🔭 Two roots about sight'))]),
 dict(at='One means see', items=[(None, TL(('👁️', 'vis · see'))), ('One means look', TL(('🔍', 'spect · look')))]),
 dict(at='Then words that sound the same', items=[(None, ROW(WD('bear'), WD('bare'))), ('A spell checker', ASK('✔️ A spell checker says both are fine.'))]),
 dict(at='In the spyglass game', items=[(None, LAB('🔭 The spyglass game')), ('find the root first', WD('<span class="pt">vis</span>or')), ('then the meaning', DEF('vis', 'see'))], hl=[('find the root first', '.pt')]),
])
V['g5ela-21-2-listen-words'] = dict(title='Word Study', sub='See or look?', scenes=[
 dict(at=None, items=[(None, LAB('Which root: see, or look?')), ('see, or look', PILLS('vis · see', 'spect · look'))]),
 dict(at='Then sort the sound alike words', items=[(None, LAB('Sort sound-alike words by their job')), ('who owns something', TL(('👤', 'owns something'))), ('name a thing', TL(('📦', 'names a thing'))), ('squeeze two words', TL(('🗜️', 'two words squeezed'))), ('squeeze two words', WD("we're = we + are"))]),
 dict(at='Then five new words', items=[(None, LAB('🔭 Five new words in the spyglass'))]),
])
V['g5ela-21-3-listen-words'] = dict(title='Word Study', sub='Thing, action, or squeezed?', scenes=[
 dict(at=None, items=[(None, LAB('🔭 Sight roots at work'))]),
 dict(at='Then the sound alike words again', items=[(None, BINS('a thing', 'an action', 'two words squeezed'))]),
 dict(at='Say it in a sentence', items=[(None, SAY('A <u>bear</u> padded across the snow.')), ('to check', ASK('📦 a thing'))]),
 dict(at='Then five new words', items=[(None, LAB('🔭 Five new words in the spyglass'))]),
])
V['g5ela-21-4-listen-words'] = dict(title='Word Study', sub='Looking and seeing', scenes=[
 dict(at=None, items=[(None, LAB('🔭 Last day with the sight roots'))]),
 dict(at='Explain the difference', items=[(None, ROW(WD('🔍 looking'), WD('👁️ seeing'))), ('looking and seeing', ASK('What is the difference? Explain it your way.'))]),
 dict(at='Then the academic pairs', items=[(None, LAB('Pairs that trip up grown writers')), ('affect and effect', ROW(WD('affect'), WD('effect'))), ('principal and principle', ROW(WD('principal'), WD('principle')))]),
 dict(at='Then the last five words', items=[(None, LAB('🔭 The last five spyglass words')), (None, '<div class="dots6">● ● ● ● ●</div>')]),
])
