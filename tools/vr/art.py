"""Drawings for the G5 ELA VR pages (inline SVG, no lettering, aria-hidden by the template).
Add a new banner, chapter token or journal stamp here by name; week<W>.json picks it with banner / token.art.
Story Expedition: the VR path earns the novel's chapter token; Field Notes Day earns the field notes stamp."""
import random


def banner_river():
    """HBG wk18 (Ch. 3-4): a river at dusk in the Choctaw homeland. A long wooden pier over a stony
    shallow on the left, the old weeping willow's 'river room' on the right, small cabins on the far hill.
    No fire, no people: the page never redraws the hard scenes."""
    rng = random.Random(18)
    s = ['<svg viewBox="0 0 920 260" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="A river at dusk with a long wooden pier and a weeping willow">',
         '<defs><linearGradient id="sky18" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#22335F"/><stop offset=".5" stop-color="#7D6A9A"/><stop offset=".85" stop-color="#E7A77A"/><stop offset="1" stop-color="#F3CF95"/></linearGradient>',
         '<linearGradient id="riv18" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C99A86"/><stop offset=".35" stop-color="#6F86A3"/><stop offset="1" stop-color="#2F4A63"/></linearGradient>',
         '<radialGradient id="sun18" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#FFE7B0"/><stop offset="1" stop-color="#FFE7B0" stop-opacity="0"/></radialGradient></defs>',
         '<rect width="920" height="260" fill="url(#sky18)"/>',
         '<circle cx="470" cy="150" r="70" fill="url(#sun18)" opacity=".8"/><circle cx="470" cy="150" r="20" fill="#FFE2A6"/>',
         # far hills + cabins
         '<path d="M0 150 Q120 118 240 136 T480 128 T720 134 T920 124 V170 H0Z" fill="#4E5B7E"/>',
         '<path d="M0 162 Q160 140 330 152 T660 148 T920 150 V180 H0Z" fill="#3E5B4E"/>']
    for x in (300, 336, 372, 620, 652):
        s.append('<g transform="translate(%d 140)"><rect x="0" y="6" width="22" height="12" fill="#5B3A26"/><path d="M-3 7 L11 -2 L25 7Z" fill="#3A2416"/><rect x="8" y="10" width="5" height="8" fill="#2B1D12"/></g>' % x)
    # river
    s.append('<path d="M0 176 Q230 166 460 172 T920 170 V260 H0Z" fill="url(#riv18)"/>')
    s.append('<g class="b18-glint" fill="#FFE7B0" opacity=".7">' + ''.join('<rect x="%d" y="%d" width="%d" height="2" rx="1"/>' % (rng.randint(380, 560), rng.randint(180, 236), rng.randint(14, 40)) for _ in range(12)) + '</g>')
    # stony shallow under the pier
    s.append(''.join('<ellipse cx="%.0f" cy="%.0f" rx="%.1f" ry="%.1f" fill="%s"/>' % (rng.uniform(20, 330), rng.uniform(222, 256), rng.uniform(5, 12), rng.uniform(2.5, 5), rng.choice(['#7F8A93', '#98A2A8', '#6C747A', '#A9AFAF'])) for _ in range(46)))
    # the pier
    s.append('<path d="M0 196 L330 204 L330 212 L0 206Z" fill="#8A5F3E"/><path d="M0 196 L330 204" stroke="#B48A63" stroke-width="2"/>')
    for x in range(20, 330, 44):
        s.append('<rect x="%d" y="%d" width="7" height="%d" fill="#5B3A26"/>' % (x, 200 + x * 8 // 330, 34 - x // 40))
    # the willow (river room)
    s.append('<path d="M760 260 Q752 200 772 150 Q780 128 770 104" stroke="#4A3325" stroke-width="16" fill="none" stroke-linecap="round"/>')
    s.append('<g class="b18-sway">')
    s.append('<ellipse cx="772" cy="92" rx="120" ry="44" fill="#6E9B4E"/><ellipse cx="740" cy="80" rx="70" ry="30" fill="#8DB65E"/>')
    for i in range(34):
        x = 660 + i * 7 + rng.uniform(-2, 2)
        s.append('<path d="M%.1f %d Q%.1f %d %.1f %d" stroke="%s" stroke-width="2.4" fill="none" stroke-linecap="round"/>' % (x, 96, x + rng.uniform(-6, 6), 160, x + rng.uniform(-4, 4), 186 + rng.randint(-6, 14), rng.choice(['#9CC56A', '#B5D77A', '#7FAE52'])))
    s.append('</g>')
    # first star
    s.append('<g class="b18-star"><circle cx="150" cy="42" r="2.4" fill="#FFF6DC"/><circle cx="150" cy="42" r="9" fill="#FFF6DC" opacity=".18"/></g>')
    s.append('</svg>')
    css = ('.b18-sway{animation:b18sway 7s ease-in-out infinite;transform-origin:772px 110px}'
           '@keyframes b18sway{0%,100%{transform:rotate(0)}50%{transform:rotate(.8deg)}}'
           '.b18-glint{animation:b18gl 3.5s ease-in-out infinite}@keyframes b18gl{50%{opacity:.3;transform:translateX(6px)}}'
           '.b18-star{animation:b18tw 2.8s ease-in-out infinite}@keyframes b18tw{50%{opacity:.4}}')
    return ''.join(s), css


def token_stone(size=120, cls='keep'):
    """HBG chapter token: a gray river stone on a little paper tag, taped down."""
    return ('<svg class="%s" viewBox="0 0 120 120" width="%d" height="%d" aria-hidden="true">'
            '<rect x="12" y="12" width="96" height="96" rx="6" fill="#FFFBF1" stroke="#E5D3AE" stroke-width="2" transform="rotate(-4 60 60)"/>'
            '<ellipse cx="60" cy="66" rx="32" ry="22" fill="#7F8A93"/><ellipse cx="54" cy="60" rx="24" ry="14" fill="#98A2A8"/>'
            '<ellipse cx="48" cy="56" rx="9" ry="4" fill="#C9CFD2" opacity=".8"/><path d="M40 72 Q60 80 84 70" stroke="#6C747A" stroke-width="2" fill="none"/>'
            '<path d="M30 92 Q46 88 60 92 T90 92" stroke="#6F86A3" stroke-width="2.5" fill="none"/>'
            '<rect x="40" y="6" width="40" height="13" fill="#F2E3B8" opacity=".85" transform="rotate(-6 60 12)"/></svg>') % (cls, size, size)


def journal_stamp_stone():
    return token_stone(60, 'pcs')


def field_stamp(color='#1F3F7A'):
    """Field notes stamp: a round rubber-stamp print (willow over water), no lettering."""
    return ('<svg viewBox="0 0 120 120" aria-hidden="true"><g fill="none" stroke="%s" opacity=".9">'
            '<circle cx="60" cy="60" r="52" stroke-width="5"/><circle cx="60" cy="60" r="42" stroke-width="2" stroke-dasharray="3 4"/>'
            '<path d="M60 86 V50" stroke-width="5" stroke-linecap="round"/><path d="M60 50 Q42 46 34 66 M60 50 Q78 46 86 66 M60 56 Q48 58 44 76 M60 56 Q72 58 76 76" stroke-width="3" stroke-linecap="round"/>'
            '<path d="M28 90 Q44 84 60 90 T92 90" stroke-width="3.5"/></g></svg>') % color


BANNERS = {'river': banner_river}
TOKENS = {'stone': token_stone}
STAMPS = {'stone': journal_stamp_stone}
