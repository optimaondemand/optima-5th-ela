#!/usr/bin/env python3
"""Cut whole sentences out of a recorded Opti clip, free (no re-recording).
Forced alignment with pocketsphinx (pip install pocketsphinx; its English model ships inside the package).
    python trim.py in.mp3 out.mp3 "full script" "sentence to cut" ["another" ...]
Prints the new script. Cuts sit in the pause before/after each removed sentence; joins keep ~0.45 s of quiet."""
import sys, re, subprocess, json
from pocketsphinx import Decoder
EXTRA = {  # words the bundled dictionary lacks (CMU phones)
    'ment': 'M EH N T', 'sist': 'S IH S T', 'dict': 'D IH K T', 'lev': 'L EH V', 'struct': 'S T R AH K T', 'opti': 'AA P T IY', 'contrite': 'K AH N T R AY T', 'jemmy': 'JH EH M IY', 'inter': 'IH N T ER',
    'cutwater': 'K AH T W AO T ER', 'ish': 'IH SH', 'tle': 'T AH L', 'dle': 'D AH L', 'mulishness': 'M Y UW L IH SH N AH S',
    'broadsides': 'B R AO D S AY D Z', 'flummox': 'F L AH M AH K S', 'copia': 'K OW P IY AH', 'asper': 'AE S P ER', 'teleport': 'T EH L AH P AO R T', 'ruffian': 'R AH F IY AH N', 'pud': 'P UH D', "jemmy's": 'JH EH M IY Z', 'rupt': 'R AH P T', 'clod': 'K L AA D', 'preposition': 'P R EH P AH Z IH SH AH N', 'prepositions': 'P R EH P AH Z IH SH AH N Z', 'spect': 'S P EH K T', 'ger': 'G ER', 'tas': 'T AE S', 'hel': 'HH EH L', 'mudlarking': 'M AH D L AA R K IH NG', 'tic': 'T IH K', 'bur': 'B ER', 'cop': 'K AA P', 'por': 'P AO R', 'tant': 'T AH N T', 'im': 'IH M', 'ba': 'B EY', 'wilder': 'W IH L D ER', 'prepositional': 'P R EH P AH Z IH SH AH N AH L', 'merriment': 'M EH R IY M AH N T', 'squished': 'S K W IH SH T', "puppy's": 'P AH P IY Z', 'lic': 'L IH K', 'rlic': 'R L IH K', 'trenchers': 'T R EH N CH ER Z', 'gar': 'G AA R', 'dow': 'D OW', 'ful': 'F UH L', 'gladn': 'G L AE D N', 'gladness': 'G L AE D N AH S', 'appositives': 'AH P AA Z AH T IH V Z', 'appositive': 'AH P AA Z AH T IH V', 'voc': 'V OW K', 'voke': 'V OW K'}
NUM = {'1': 'one', '2': 'two', '3': 'three', '4': 'four', '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine', '10': 'ten', '11': 'eleven', '12': 'twelve', '13': 'thirteen', '14': 'fourteen', '15': 'fifteen', '16': 'sixteen', '17': 'seventeen', '18': 'eighteen', '19': 'nineteen', '20': 'twenty'}
def words(t): return [NUM.get(w, w) for w in re.sub(r"[^a-z0-9' ]+", ' ', t.lower().replace('-', ' ')).split() if w]
def align(mp3, text):
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', mp3, '-ar', '16000', '-ac', '1', '-f', 's16le', '-'], capture_output=True).stdout
    d = Decoder(samprate=16000, bestpath=False)
    oov = [w for w in set(words(text)) if d.lookup_word(w) is None]
    for w in oov:
        if w not in EXTRA: raise SystemExit('add a pronunciation to EXTRA for: ' + ' '.join(sorted(set(oov) - set(EXTRA))))
        d.add_word(w, EXTRA[w], True)
    d.set_align_text(' '.join(words(text)))
    d.start_utt(); d.process_raw(raw, full_utt=True); d.end_utt()
    d.set_alignment(); d.start_utt(); d.process_raw(raw, full_utt=True); d.end_utt()
    out = [(re.sub(r'\(\d+\)$', '', s.name), s.start / 100, (s.start + s.duration) / 100) for s in d.get_alignment()]
    return [w for w in out if w[0] not in ('<sil>', '<s>', '</s>')]
def sentences(t): return [m.group(0).strip() for m in re.finditer(r'[^.?!]+[.?!]?', t) if m.group(0).strip()]
if __name__ == '__main__':
    src, dst, script, cuts = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
    al = align(src, script); W = words(script)
    assert [a[0] for a in al] == W, ('alignment words differ', [a[0] for a in al][:20], W[:20])
    keep, i = [], 0      # per sentence: (keep?, first word idx, last word idx)
    for s in sentences(script):
        n = len(words(s)); keep.append((s not in cuts, i, i + n - 1, s)); i += n
    for c in cuts: assert any(c == k[3] for k in keep), ('not a sentence of the script', c)
    segs, cur = [], None
    for k, a, b, s in keep:
        if k:
            if cur is None: cur = [a, b]
            else: cur[1] = b
        elif cur is not None: segs.append(cur); cur = None
    if cur: segs.append(cur)
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', src], capture_output=True, text=True).stdout)
    spans = []
    for a, b in segs:
        st = 0.0 if a == 0 else max(0, al[a][1] - 0.22)
        en = dur if b == len(al) - 1 else min(dur, al[b][2] + 0.23)
        spans.append((st, en))
    f = ''.join('[0:a]atrim=%.3f:%.3f,asetpts=PTS-STARTPTS,afade=t=in:d=0.04,afade=t=out:st=%.3f:d=0.06[s%d];' % (s, e, max(0, e - s - 0.06), n) for n, (s, e) in enumerate(spans))
    f += ''.join('[s%d]' % n for n in range(len(spans))) + 'concat=n=%d:v=0:a=1[o]' % len(spans)
    subprocess.check_call(['ffmpeg', '-y', '-loglevel', 'error', '-i', src, '-filter_complex', f, '-map', '[o]', '-c:a', 'libmp3lame', '-b:a', '128k', dst])
    print(json.dumps({'script': ' '.join(k[3] for k in keep if k[0]), 'spans': spans, 'was': round(dur, 2)}))
