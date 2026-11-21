#!/usr/bin/env python3
"""Encode films from /tmp/vid/frames/<key> using /tmp/vid/build/timeline.json.
   python3 encode.py [--silent] key1 key2 ...   -> /tmp/vid/<key>.mp4/.jpg/.vtt + /tmp/vid/sheet.png
   --silent: a silent audio track (Q4: voiced later; re-run timeline+capture on the real clip, same filename)."""
import json, subprocess, sys, os, glob
args = sys.argv[1:]; silent = '--silent' in args; keys = [a for a in args if not a.startswith('--')]
t = json.load(open('/tmp/vid/build/timeline.json'))
def ts(x): return '%02d:%02d:%06.3f' % (int(x // 3600), int(x % 3600 // 60), x % 60)
os.chdir('/tmp/vid'); sheet = []
for k in keys:
    dur = t[k]['dur']
    if silent:
        cmd = f'ffmpeg -y -loglevel error -framerate 12 -i frames/{k}/f%04d.jpg -f lavfi -t {dur:.2f} -i anullsrc=r=44100:cl=mono -c:v libx264 -preset slow -tune stillimage -crf 30 -pix_fmt yuv420p -r 24 -c:a aac -b:a 32k -shortest -movflags +faststart {k}.mp4'
    else:
        cmd = f'ffmpeg -y -loglevel error -framerate 12 -i frames/{k}/f%04d.jpg -i {k}.mp3 -c:v libx264 -preset slow -tune stillimage -crf 30 -pix_fmt yuv420p -r 24 -c:a aac -b:a 96k -af apad -shortest -movflags +faststart {k}.mp4'
    subprocess.run(cmd, shell=True, check=True)
    sc = [s['t'] for s in t[k]['scenes']]
    fr = max(1, int(round((sc[1] - 0.4) * 12)) + 1) if len(sc) > 1 else 6
    subprocess.run(f'cp frames/{k}/f{fr:04d}.jpg {k}.jpg', shell=True, check=True)
    caps = t[k]['caps']; out = ['WEBVTT', '']
    for i, c in enumerate(caps):
        b = caps[i + 1]['t'] if i + 1 < len(caps) else dur
        out += [f"{ts(c['t'])} --> {ts(b)}", c['text'], '']
    open(f'{k}.vtt', 'w').write('\n'.join(out))
    n = len(glob.glob(f'frames/{k}/f*.jpg'))
    for s2 in sc[1:] + [None]:
        f = n - 1 if s2 is None else max(1, int(s2 * 12) - 1)
        sheet.append(f'frames/{k}/f{f:04d}.jpg')
os.makedirs('sheet', exist_ok=True); subprocess.run('rm -f sheet/*', shell=True)
for i, f in enumerate(sheet): subprocess.run(f'cp {f} sheet/{i:03d}.jpg', shell=True)
cols = 3
subprocess.run(f"ffmpeg -y -loglevel error -pattern_type glob -i 'sheet/*.jpg' -vf scale=480:-1,tile={cols}x{(len(sheet)+cols-1)//cols} -frames:v 1 sheet.png", shell=True, check=True)
print('encoded', keys)
