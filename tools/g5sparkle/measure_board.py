#!/usr/bin/env python3
"""measure_board.py - find the 32 painted spaces on the G5 year board and print them in PATH order
(row 1 left->right, row 2 right->left, row 3 left->right, row 4 right->left), ready to paste into
BOARD.spaces in g5-sparkle.js. Needs opencv (pip install opencv-python-headless).
    python measure_board.py assets/maps/year-board.jpg
"""
import sys, json, cv2, numpy as np
im = cv2.imread(sys.argv[1]); H, W = im.shape[:2]
g = cv2.medianBlur(cv2.cvtColor(im, cv2.COLOR_BGR2GRAY), 5)
c = cv2.HoughCircles(g, cv2.HOUGH_GRADIENT, dp=1, minDist=70, param1=80, param2=35, minRadius=26, maxRadius=40)
c = [tuple(map(int, v)) for v in np.round(c[0])]
hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
c = [v for v in c if np.median(hsv[v[1]-8:v[1]+8, v[0]-8:v[0]+8].reshape(-1, 3), 0)[1] > 30 and v[1] > 120]
ys = sorted(set(round(v[1] / 60) for v in c))
rows = {}
for v in c: rows.setdefault(min(ys, key=lambda y: abs(y - v[1] / 60)), []).append(v)
out = []
for i, k in enumerate(sorted(rows)):
    out += sorted(rows[k], key=lambda v: v[0], reverse=bool(i % 2))
print(len(out), 'spaces'); print(json.dumps([[x, y] for x, y, r in out]))
