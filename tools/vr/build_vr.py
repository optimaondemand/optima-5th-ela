#!/usr/bin/env python3
"""G5 ELA weekly VR page: tools/vr/week<W>.json -> vr-<W>.html (repo root).

Story Expedition (Bethany, Nov 2026): one VR page per week, always Day 2, its own Canvas assignment.
The lessons, parent guides and DATA never mention VR. Two paths on one page, each turns in ONE thing:
a video of 30 seconds or less with a 2 sentence explanation (Canvas: File Upload ON + Media Recording ON).
  Story Expedition (VR)  build in the headset, record (Library > Camera > Video), submit in the Canvas tab;
                         step 5 earns the novel's chapter token (HBG: a river stone)
  Field Notes Day        an on-page game, plan 2 sentences (not turned in), record in Canvas (Media);
                         earns a field notes stamp
Guide: Mason (G5 ELA narrator, voice 1Mx54eW85zYpnx1WfIdU, eleven_v4). Audio is deferred: the players stay
hidden until assets/audio/guide/mason/g5ela-<W>-vr-{brief,alt,saved}.mp3 exist. Never voice Isaac or a Choctaw character.
Copied from the G4 ELA kit (optima-4th-ela/tools/vr) on 9 Nov 2026.

usage: python3 tools/vr/build_vr.py tools/vr/week18.json
"""
import html, json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import art

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
D = json.load(open(sys.argv[1], encoding='utf-8'))
W, DAY = D['week'], D['day']
PRE = 'g5ela-%d-vr' % W
CANVAS = '%d.%d VR · %s' % (W, DAY, D['title'])
e = lambda t: html.escape(str(t), quote=True)


def strip(t):
    return re.sub(r'<[^>]+>', '', t)


def show(name):
    """app names use " - " (Log Cabin - Wall); student text has no dashes -> Log Cabin (Wall)"""
    return re.sub(r'^(.*?) - (.*)$', r'\1 (\2)', name)


# ── VR step 1: plain numbered list grouped by place, "Name: what it is" ──
def mlist(ms):
    return '<ol class="mlist">' + ''.join('<li><b>%s</b>: %s</li>' % (e(show(m['name'])), e(m['is'])) for m in ms) + '</ol>'
if D.get('groups'):
    groups = ''.join('<p style="margin:8px 0 0;font-size:15px"><b>%s</b></p>%s' % (e(g['h']), mlist([m for m in D['models'] if m.get('group') == g['k']])) for g in D['groups'])
else:
    groups = mlist(D['models'])

# ── help drawer (same images + video as G4 ELA; files in assets/vr/) ──
HS = [
 ('🖥️ First time only: connect Canvas (on your computer)', [
  ('01-login', 'The Optima On Demand login page, with the Sign In button circled.', 'Log in', 'Go to <a href="https://xr.optimaed.com" target="_blank" rel="noopener">xr.optimaed.com</a> on your computer. Log in with the same login you use in VR.'),
  ('02-authorize', 'The Canvas box that asks to connect, with the Authorize button circled.', 'Connect to Canvas', 'Click <b>Connect to Canvas</b>. Log in with your usual Canvas username and password, then click <b>Authorize</b>. You will see <b>Canvas connection completed</b>.'),
  ('03-connected', 'The Canvas page on the website, with the Canvas button and the list of assignments circled.', 'Find our class', 'Click <b>Canvas</b> on the left and pick our class. Our assignments show up. You only do this part one time.')]),
 ('📄 Only if the assignment has a file', [
  ('04-upload', 'The Upload file box, with the Upload File button circled.', 'Get the file ready', 'Open the assignment and click <b>Open in Canvas</b> to download the file. Then click <b>My Files</b> and <b>Upload File</b>.')]),
 ('🥽 In the headset', [
  ('05-explore', 'The Explore tab in the headset, with the tab and the filter box circled.', 'Explore tab', 'Put on your headset. Click the <b>Explore</b> tab and type the map’s name in <b>Filter environments</b>.'),
  ('06-begin-solo', 'A map is picked and the Begin Solo button is circled.', 'Begin Solo', 'Click the map, then click <b>Begin Solo</b>.'),
  ('07-canvas', 'The Canvas tab in the headset, with the tab and the assignment box circled.', 'Read the assignment', 'Press the <b>top button on your right controller</b> to open your menu. Click the <b>Canvas</b> tab and pick our assignment to read the directions. Tip: point at a mint side grip and squeeze to pull the tablet to your hand.'),
  ('08-models', 'The Models tab open in an ocean map, with a list of models.', 'Bring out the models', 'Click <b>Models</b>. Type the exact name in the search box, or scroll with your thumbstick. Click a model to bring it out.'),
  ('08b-move', 'A controller moving a fish model in an ocean map.', 'Move and resize', 'Grab a model with the <b>palm trigger</b>. Turn and move it with the thumbstick. Use <b>both</b> palm triggers to make it bigger or smaller.'),
  ('09-placed', 'A picture file placed in an ocean map.', 'Need a file?', 'Click <b>Library</b>, then <b>Files</b>. Pick your file to place it in the world, next to your model.'),
  ('10-camera', 'The Library camera, with the Height slider circled.', 'Record a video', 'Click <b>Library</b>, then <b>Camera</b>. Move the tablet until your whole scene fits. Slide <b>Height</b> or the zoom bar if you need to. Switch to <b>Video</b> and start recording. Say your 2 sentences, then stop at 30 seconds or less.'),
  ('11-choose', 'The My Files list in the headset, with the newest file circled.', 'Pick your video', 'Click the <b>Canvas</b> tab and pick our assignment. Click <b>Choose from My Files</b>, pick your newest video, then click <b>Use this file</b>.'),
  ('12-submitted', 'The Canvas tab after submitting, with the green Submitted tag circled.', 'Submit to Canvas', 'Click <b>Submit to Canvas</b> and look for the green <b>Submitted</b> tag. To leave VR, press the <b>Meta button</b> on your right controller, then click <b>Quit</b>.')]),
 ('🔁 Didn’t work in VR? Two other ways', [
  ('13-portal-submit', 'The Canvas page on the website, with the Choose from My Files button circled.', 'Use the website', 'Go to <a href="https://xr.optimaed.com" target="_blank" rel="noopener">xr.optimaed.com</a> and click <b>Canvas</b>. Pick our assignment, click <b>Choose from My Files</b>, pick your video and submit it.')])]
n = 0
hd = ''
for title, items in HS:
    hd += '<h4 class="hd-group">%s</h4><ol class="hd-steps">' % title
    for img, alt, b, p in items:
        n += 1
        hd += '<li class="hd-step"><img loading="lazy" src="assets/vr/vr-canvas-help-%s.jpg" alt="%s"><div><span class="hd-n">%d</span><b>%s</b><p>%s</p></div></li>' % (img, e(alt), n, b, p)
    hd += '</ol>'
HELP = ('<details class="helpdrawer" id="vr-help"><summary><span class="hd-ic">🛟</span><span><b>Having trouble in VR?</b><small>Steps with pictures, and a how-to video</small></span><span class="hd-chev" aria-hidden="true">▾</span></summary>'
        '<div class="hd-body"><div class="hd-video"><div class="hd-frame" data-src="https://www.youtube-nocookie.com/embed/slDH-WN4scY?rel=0"></div><p class="hd-cap">How-to video: Optima On-Demand and Canvas</p></div>'
        '<p class="hd-note">These pictures come from other maps. Your map will be <b>%s</b>, but the buttons are the same.</p>%s'
        '<p class="hd-alt">Your videos save to <b>My Files</b> at xr.optimaed.com on their own. You can also download your video there and upload it to the Canvas assignment yourself.</p></div></details>') % (e(D['map']), hd)

# ── Field Notes Day game (games/<name>.js + .css) ──
A = D['alt']
G = A['game']
if G == 'vision-real':
    GAME_HTML = ('<div class="vclue">%s</div><div class="vtally" id="vr-tally"></div><ol class="vcards" id="vr-cards"></ol>') % A['clue']
    GAME_CFG = {'cards': A['cards'], 'miss': A['miss']}
elif G == 'rename-order':
    GAME_HTML = ('<h3 class="gh">1 · The names</h3><div id="ren"></div>'
                 '<h3 class="gh">2 · In order</h3><p class="lock" id="order-lock">Finish part 1 first.</p><p style="font-size:16px">%s</p>'
                 '<div class="road" id="road"><ol class="mile" id="mile"></ol></div><div class="stops" id="stops"></div>') % e(A['orderQ'])
    GAME_CFG = {'rename': A['rename'], 'order': A['order'], 'orderMiss': A['orderMiss']}
else:
    sys.exit('unknown game: ' + G)
GAME_JS = open(os.path.join(HERE, 'games', G + '.js'), encoding='utf-8').read()
GAME_CSS = open(os.path.join(HERE, 'games', G + '.css'), encoding='utf-8').read()

banner, banner_css = art.BANNERS[D['banner']]()
K = D['token']
keep = art.TOKENS[K['art']]
WR = D['write']
TRANSCRIPTS = {k: re.sub(r'\s*\[[^\]]+\]\s*', ' ', v).strip() for k, v in D['scripts'].items()}


def journal_p(t):
    if t.startswith('>'):
        q, _, cite = t[1:].partition('|')
        return '<blockquote>%s<cite>%s</cite></blockquote>' % (e(q.strip()), e(cite.strip()))
    return '<p>%s</p>' % e(t)


g = D['guide']
head = ('%s · %s, %s. Guide: %s (folder %s, voice %s; audio deferred). Map: %s. Models: %s. Step 5: %s. Field Notes Day game: %s. Token: %s.'
        % (CANVAS, D['book'], D['chapters'], g['name'], g['folder'], g['voice'], D['map'],
           ', '.join(m['name'] for m in D['models']), ', '.join(D['steps']['extraModels']), G, K['name'])).replace('--', '-')

J = D['journal']
REPL = {
 '{{CANVAS}}': e(CANVAS), '{{HEADCOMMENT}}': e(head), '{{WEEK}}': str(W), '{{TITLE}}': e(D['title']), '{{BOOK}}': e(D['book']), '{{CHAPTERS}}': e(D['chapters']),
 '{{GUIDE}}': e(g['name']), '{{BANNER}}': banner, '{{PRE}}': PRE,
 '{{L_BRIEF}}': e(D['labels']['brief']), '{{L_ALT}}': e(D['labels']['alt']), '{{L_SAVED}}': e(D['labels']['saved']),
 '{{PC_KICKER}}': e(J['kicker']), '{{PC_H}}': e(J['h']), '{{PC_BODY}}': ''.join(journal_p(p) for p in J['body']),
 '{{PC_SIGN}}': e(J['sign']), '{{PC_WORD}}': J['word'], '{{STAMP_ART}}': art.STAMPS[K['art']](),
 '{{KEEP_NAME}}': e(K['name']), '{{KEEP_SHORT}}': e(K['name'][0].upper() + K['name'][1:]), '{{KEEP_TITLE}}': e(K['name'][0].upper() + K['name'][1:] + ' earned!'),
 '{{KEEP_LINE}}': e(K['line']), '{{KEEP_ART}}': keep(70, 'peekart'), '{{KEEP_ART_BIG}}': keep(120, 'keep'), '{{BMARK_ART}}': art.field_stamp(),
 '{{MINUTES}}': str(D['minutes']), '{{MISSION_H}}': e(D['mission']['h']), '{{MISSION_P}}': e(D['mission']['p']), '{{JOB}}': e(D['job']),
 '{{GROUPS}}': groups, '{{MAP}}': e(D['map']), '{{MAP_FILTER}}': e(D['mapFilter']),
 '{{S_BUILD}}': D['steps']['build'], '{{S_SAY}}': D['steps']['say'], '{{S_FRAME}}': e(D['steps']['frame']), '{{S_EXTRA}}': D['steps']['extra'], '{{FITS}}': e(D['steps']['fits']),
 '{{HELP}}': HELP, '{{POINTS}}': e(D['points']),
 '{{ALT_H}}': e(A['h']), '{{ALT_JOB}}': e(A['job']), '{{ALT_P}}': e(A['p']), '{{GAME_HTML}}': GAME_HTML, '{{GAME_CSS}}': GAME_CSS + banner_css, '{{GAME_JS}}': GAME_JS,
 '{{WRITE_Q}}': WR['q'], '{{CHIPS}}': ''.join('<span class="chip" data-chip="%s">%s</span>' % (c['k'], e(c['t'])) for c in WR['chips']),
 '{{NCHIPS}}': str(len(WR['chips'])), '{{STARTERS}}': ''.join('<li>%s</li>' % e(s) for s in WR['starters']),
 '{{CREDITS}}': e(D.get('credits', '')),
 '{{DATA}}': json.dumps({'week': W, 'pre': PRE, 'canvas': CANVAS, 'guide': {k: g[k] for k in ('name', 'initials', 'color', 'folder')},
                          'transcripts': TRANSCRIPTS, 'game': GAME_CFG, 'chips': [{'k': c['k'], 'rx': c['rx']} for c in WR['chips']],
                          'writeQ': strip(WR['q'])}, ensure_ascii=False).replace('</', '<\\/'),
}
page = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
for k, v in REPL.items():
    page = page.replace(k, v)
left = re.findall(r'\{\{\w+\}\}', page)
assert not left, left
out = os.path.join(ROOT, 'vr-%d.html' % W)
open(out, 'w', encoding='utf-8', newline='\n').write(page)
json.dump({'pre': PRE, 'voice': g['voice'], 'folder': g['folder'], 'model': 'eleven_v4', 'status': 'deferred until Bethany says to add clips',
           'clips': {k: {'file': 'assets/audio/guide/%s/%s-%s.mp3' % (g['folder'], PRE, k), 'prompt': v, 'transcript': TRANSCRIPTS[k]} for k, v in D['scripts'].items()}},
          open(os.path.join(HERE, 'week%d-scripts.json' % W), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('wrote', out, '(%d KB)' % (len(page.encode()) // 1024))
