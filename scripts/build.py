"""Builds the profile: every SVG in assets/ (dark + light) and README.md.

    pip install fonttools brotli
    python3 scripts/build.py

Edit the copy in the CONTENT section. Bump V after a rebuild so GitHub's
image cache picks up the new files.
"""
import base64
import html
import io
import re
from pathlib import Path
from xml.sax.saxutils import escape as esc

from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"
FONTS = ROOT / "scripts" / "fonts"
V = 2

# ------------------------------------------------------------------ CONTENT
NAME = "Abhin M S"
PLACE = "Electronic City, Bengaluru"
ROLE = "Freelance developer and founder"
EMAIL = "abhiabhinms@gmail.com"

HELLO = "Hey, I'm Abhin."
INTRO = [
    "I build the software small businesses run on: dashboards, CRMs and "
    "WhatsApp automation. Backend, frontend and hosting, end to end.",
    "I also run three ventures of my own. Tap one to visit.",
]

VENTURES = [
    dict(slug="emiratick", name="Emiratick", url="https://emiratick.ae", link="emiratick.ae",
         desc="WhatsApp Cloud API platform for business campaigns and automation.", color="green"),
    dict(slug="loopstitch", name="Loopstitch", url="https://loopstitch.online", link="loopstitch.online",
         desc="Streetwear and custom prints on premium tees, from a single piece.", color="red"),
    dict(slug="town", name="Town Institutes", url="https://towninstitutes.com", link="towninstitutes.com",
         desc="Software training and internships, open to every background.", color="mari"),
]

WORK_OPEN = "Some things I've built for clients:"
DASH_CAPTION = ("Retail analytics for a 24-store chain, with live KPIs, "
                "role-based access and Google Sheets sync.")
WORK = [
    "A telecalling CRM where Meta ad leads and website bookings land straight in the call queue.",
    "A QR token system with a staff dashboard and a live TV display board.",
]
VOICE_CAPTION = "Working on now: an AI voice agent that phones customers and talks from a prompt you write."

ASK = "What brings you here? Tap an answer."
REPLIES = [
    ("build", "I need software built for my business"),
    ("whatsapp", "I want WhatsApp automation"),
    ("learn", "I want to learn to code"),
    ("tees", "I want custom t-shirts"),
    ("dev", "I'm a developer. What's your setup?"),
]

STACK_OPEN = "What I build with:"
STACK = [
    ("Backend", ["FastAPI", "Python", "Laravel", "PHP"]),
    ("Frontend", ["React", "Vite", "Tailwind", "TypeScript"]),
    ("Data", ["MySQL", "MariaDB", "Google Sheets API"]),
    ("Hosting", ["aaPanel", "Nginx", "Docker", "Cloudflare", "GitHub Actions"]),
    ("Integrations", ["WhatsApp Cloud API", "Meta Graph API", "Shopify", "WooCommerce"]),
]

ACTIVITY = "And here's what my GitHub looks like lately:"
COMPOSE = f"Write to {EMAIL}"

# ------------------------------------------------------------------ TOKENS
THEMES = {
    "dark": dict(bub="#1a2036", bub2="#252c48", text="#e9ecf8", muted="#929ac0", line="#2e3658",
                 mari="#f6b13a", mari_fill="#f6b13a", on_mari="#24180a",
                 green="#3ccf8e", red="#ff5a5f", tee="#f4f4f6", tee_ink="#121212"),
    "light": dict(bub="#eef0f9", bub2="#e1e5f5", text="#161a2e", muted="#59618a", line="#d3d8ee",
                  mari="#a65f00", mari_fill="#ffbe45", on_mari="#2a1b00",
                  green="#0f8a53", red="#d7263d", tee="#15151a", tee_ink="#ffffff"),
}
W = 900
FAMILY = "Brico,'Bricolage Grotesque','Segoe UI',system-ui,-apple-system,sans-serif"
WEIGHTS = {400: "bricolage-grotesque-latin-400-normal.woff2",
           600: "bricolage-grotesque-latin-600-normal.woff2",
           800: "bricolage-grotesque-latin-800-normal.woff2"}
_FONT = {w: TTFont(FONTS / f) for w, f in WEIGHTS.items()}
_CMAP = {w: f.getBestCmap() for w, f in _FONT.items()}


def tw(s, size, weight=400):
    f, cmap = _FONT[weight], _CMAP[weight]
    upm, hmtx = f["head"].unitsPerEm, f["hmtx"]
    return sum(hmtx[cmap[ord(c)]][0] if ord(c) in cmap else upm * 0.55 for c in s) * size / upm


def wrap(s, size, maxw, weight=400):
    lines, cur = [], ""
    for word in s.split():
        trial = f"{cur} {word}".strip()
        if cur and tw(trial, size, weight) > maxw:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    return lines + [cur]


_font_cache = {}


def font_css(chars):
    key = "".join(sorted(set(chars)))
    if key in _font_cache:
        return _font_cache[key]
    css = []
    for w, fn in WEIGHTS.items():
        ft = TTFont(FONTS / fn)
        opts = subset.Options()
        opts.flavor = "woff2"
        opts.layout_features = ["kern", "liga"]
        sub = subset.Subsetter(opts)
        sub.populate(text=key)
        sub.subset(ft)
        buf = io.BytesIO()
        ft.flavor = "woff2"
        ft.save(buf)
        b64 = base64.b64encode(buf.getvalue()).decode()
        css.append(f"@font-face{{font-family:Brico;font-weight:{w};"
                   f"src:url(data:font/woff2;base64,{b64}) format('woff2')}}")
    _font_cache[key] = "\n".join(css)
    return _font_cache[key]


BASE_CSS = """
.pop{animation:pop .5s cubic-bezier(.2,.9,.3,1.15) both;transform-box:fill-box;transform-origin:0 100%}
@keyframes pop{from{opacity:0;transform:translateY(10px) scale(.96)}to{opacity:1;transform:none}}
.dot{animation:dot 1s ease-in-out infinite;transform-box:fill-box;transform-origin:center}
@keyframes dot{0%,60%,100%{transform:translateY(0);opacity:.4}30%{transform:translateY(-4px);opacity:1}}
"""


def svg(w, h, body, style=""):
    chars = "".join(html.unescape(m) for m in re.findall(r">([^<>]+)<", body)) + " "
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{w}" height="{h:.0f}" viewBox="0 0 {w} {h:.0f}" fill="none">\n<style>\n{font_css(chars)}\n'
        f"text{{font-family:{FAMILY}}}\n{BASE_CSS}\n{style}\n"
        "@media (prefers-reduced-motion: reduce){*{animation:none!important}}\n</style>\n"
        f"{body}\n</svg>\n"
    )


def T(x, y, s, size, fill, weight=400, anchor=None, extra=""):
    a = f' text-anchor="{anchor}"' if anchor else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}"{a}{extra}>{esc(s)}</text>')


def rr(x, y, w, h, tl=18, tr=18, br=18, bl=18):
    return (f"M{x+tl:.1f},{y:.1f} H{x+w-tr:.1f} Q{x+w:.1f},{y:.1f} {x+w:.1f},{y+tr:.1f} "
            f"V{y+h-br:.1f} Q{x+w:.1f},{y+h:.1f} {x+w-br:.1f},{y+h:.1f} H{x+bl:.1f} "
            f"Q{x:.1f},{y+h:.1f} {x:.1f},{y+h-bl:.1f} V{y+tl:.1f} Q{x:.1f},{y:.1f} {x+tl:.1f},{y:.1f} Z")


class Seq:
    """Plays messages one after another: a typing bubble, then the message pops in."""

    def __init__(self, c, start=0.4, gap=0.55, typing=0.8):
        self.c, self.t, self.gap, self.typing = c, start, gap, typing
        self.css, self.n = [], 0

    def add(self, x, y, inner, typing=True):
        out = []
        if typing:
            t0, t1 = self.t, self.t + self.typing
            self.n += 1
            k = f"ty{self.n}"
            p0, p1 = t0 / t1 * 100, 99.5
            frames = (f"0%,{p0:.2f}%{{opacity:0}}{p0+0.01:.2f}%,{p1}%{{opacity:1}}100%{{opacity:0}}"
                      if p0 > 0 else f"0%,{p1}%{{opacity:1}}100%{{opacity:0}}")
            self.css.append(f"@keyframes {k}{{{frames}}}")
            dots = "".join(
                f'<circle class="dot" style="animation-delay:{i*0.15:.2f}s" cx="{x+20+i*12}" cy="{y+20}" r="3.6" fill="{self.c["muted"]}"/>'
                for i in range(3))
            out.append(f'<g opacity="0" style="animation:{k} {t1:.2f}s linear forwards">'
                       f'<path d="{rr(x, y, 64, 40, 5, 18, 18, 18)}" fill="{self.c["bub"]}"/>{dots}</g>')
            self.t = t1
        out.append(f'<g class="pop" style="animation-delay:{self.t:.2f}s">{inner}</g>')
        self.t += self.gap
        return "".join(out)


def bubble(c, x, y, lines, size=18, weight=400, color=None, padx=18, pady=14, lh=None, tail=True, minw=0):
    lh = lh or size * 1.42
    w = max(minw, max(tw(l, size, weight) for l in lines) + 2 * padx)
    h = len(lines) * lh + 2 * pady - (lh - size * 1.05)
    body = [f'<path d="{rr(x, y, w, h, 5 if tail else 18, 18, 18, 18)}" fill="{c["bub"]}"/>']
    for i, l in enumerate(lines):
        body.append(T(x + padx, y + pady + size * 0.93 + i * lh, l, size, color or c["text"], weight))
    return "".join(body), w, h


# ------------------------------------------------------------------ PIECES
def head(c):
    av = base64.b64encode((OUT / "avatar.jpg").read_bytes()).decode()
    style = """
.typ{animation:typ 1.6s steps(1) forwards}
@keyframes typ{0%{opacity:1}100%{opacity:0}}
.onl{opacity:0;animation:onl 1.6s steps(1) forwards}
@keyframes onl{0%{opacity:0}100%{opacity:1}}
.ring{animation:ring 2.4s ease-out 1.6s infinite;transform-box:fill-box;transform-origin:center}
@keyframes ring{from{opacity:.7;transform:scale(1)}to{opacity:0;transform:scale(2.4)}}"""
    b = [
        f'<defs><clipPath id="av"><circle cx="34" cy="44" r="34"/></clipPath></defs>',
        f'<image clip-path="url(#av)" x="0" y="10" width="68" height="68" href="data:image/jpeg;base64,{av}" '
        f'xlink:href="data:image/jpeg;base64,{av}"/>',
        f'<circle class="ring" cx="60" cy="70" r="6" fill="{c["green"]}"/>',
        f'<circle cx="60" cy="70" r="8" fill="{c["green"]}" stroke="{c["bub"]}" stroke-width="3"/>',
        T(86, 42, NAME, 28, c["text"], 800),
        f'<g class="typ">{T(86, 70, "typing", 16, c["mari"], 600)}'
        + "".join(f'<circle class="dot" style="animation-delay:{i*0.15:.2f}s" cx="{86+tw("typing",16,600)+8+i*8}" cy="66" r="2.2" fill="{c["mari"]}"/>' for i in range(3))
        + "</g>",
        f'<g class="onl">{T(86, 70, "online", 16, c["green"], 600)}</g>',
        T(W, 42, ROLE, 16, c["text"], 600, "end"),
        T(W, 68, PLACE, 16, c["muted"], 400, "end"),
        f'<line x1="0" y1="99" x2="{W}" y2="99" stroke="{c["line"]}"/>',
    ]
    return svg(W, 100, "\n".join(b), style)


def intro(c):
    s = Seq(c, start=0.9)
    b, y = [], 6
    inner, w, h = bubble(c, 0, y, [HELLO], size=60, weight=800, padx=26, pady=20)
    b.append(s.add(0, y, inner))
    y += h + 10
    for msg in INTRO:
        inner, w, h = bubble(c, 0, y, wrap(msg, 19, 600), size=19)
        b.append(s.add(0, y, inner))
        y += h + 10
    return svg(W, y + 4, "\n".join(b), "\n".join(s.css))


def venture(c, v, idx):
    CW, CH = 290, 336
    col = c[v["color"]]
    b = [f'<g class="pop" style="animation-delay:{0.3+idx*0.15:.2f}s">',
         f'<path d="{rr(0, 0, CW, CH, 5, 20, 20, 20)}" fill="{c["bub"]}"/>',
         f'<rect x="8" y="8" width="{CW-16}" height="150" rx="14" fill="{col}" fill-opacity=".16"/>']
    mx, my = 8, 8
    style = ""
    if v["slug"] == "emiratick":
        q = "Is order 2041 shipped?"
        a = "Out for delivery today"
        w1 = tw(q, 13) + 24
        w2 = tw(a, 13, 600) + 46
        b.append(f'<path d="{rr(mx+16, my+26, w1, 34, 4, 14, 14, 14)}" fill="{c["bub2"]}"/>')
        b.append(T(mx + 28, my + 48, q, 13, c["text"]))
        x2 = mx + CW - 16 - 16 - w2
        b.append(f'<g class="pop" style="animation-delay:1.3s"><path d="{rr(x2, my+72, w2, 34, 14, 4, 14, 14)}" fill="{col}"/>')
        b.append(T(x2 + 12, my + 94, a, 13, c["bub"], 600))
        tx = x2 + w2 - 26
        b.append(f'<path d="M{tx},{my+90} l3,3 l6,-7 M{tx+5},{my+93} l2,0 l6,-7" stroke="{c["bub"]}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></g>')
        b.append(T(mx + 16, my + 136, "Sent automatically in 0.4 s", 12, col, 600))
    elif v["slug"] == "loopstitch":
        style = (".swap{animation:swap 6s steps(1) infinite}"
                 f"@keyframes swap{{0%{{fill:{c['tee']}}}33%{{fill:#2b2b30}}66%{{fill:#6b4428}}}}")
        sx, sy, k = mx + (CW - 16) / 2 - 62, my + 18, 1.24
        tee = ("M30 10 L8 22 L17 42 L28 37 L28 92 L72 92 L72 37 L83 42 L92 22 L70 10 "
               "C66 18 58 22 50 22 C42 22 34 18 30 10 Z")
        b.append(f'<g transform="translate({sx:.1f},{sy}) scale({k})">'
                 f'<path class="swap" d="{tee}" fill="{c["tee"]}" stroke="{c["line"]}" stroke-width="1"/>'
                 f'<text x="50" y="58" text-anchor="middle" font-size="15" font-weight="800" fill="{col}">LS</text></g>')
        b.append(f'<rect x="{mx+12}" y="{my+12}" width="{tw("Launching soon",12,600)+20}" height="24" rx="12" fill="{col}"/>')
        b.append(T(mx + 22, my + 28, "Launching soon", 12, "#ffffff", 600))
    else:
        code = [("print(", c["text"]), ('"Hello, Town!"', col), (")", c["text"])]
        b.append(f'<rect x="{mx+16}" y="{my+18}" width="{CW-48}" height="76" rx="10" fill="{c["bub"]}"/>')
        for i, cc in enumerate([c["red"], c["mari"], c["green"]]):
            b.append(f'<circle cx="{mx+30+i*12}" cy="{my+32}" r="3.5" fill="{cc}" fill-opacity=".8"/>')
        x = mx + 30
        for s_, colr in code:
            b.append(T(x, my + 70, s_, 15, colr, 600))
            x += tw(s_, 15, 600)
        b.append(f'<rect x="{x+3:.1f}" y="{my+56}" width="2.5" height="18" fill="{col}">'
                 f'<animate attributeName="opacity" values="1;0;1" dur="1s" calcMode="discrete" repeatCount="indefinite"/></rect>')
        x = mx + 16
        for i, lang in enumerate(["Python", "Java", "React", "Laravel"]):
            lw = tw(lang, 12, 600) + 18
            b.append(f'<rect x="{x:.1f}" y="{my+108}" width="{lw:.1f}" height="24" rx="12" '
                     f'fill="{col if i == 0 else c["bub"]}"/>')
            b.append(T(x + 9, my + 124, lang, 12, c["bub"] if i == 0 else c["text"], 600))
            x += lw + 6
    b.append(T(18, 196, v["name"], 23, c["text"], 800))
    for i, ln in enumerate(wrap(v["desc"], 15, CW - 36)):
        b.append(T(18, 224 + i * 21, ln, 15, c["muted"]))
    b.append(f'<line x1="18" y1="{CH-50}" x2="{CW-18}" y2="{CH-50}" stroke="{c["line"]}"/>')
    b.append(T(18, CH - 21, v["link"], 15, col, 600))
    ax, ay = CW - 30, CH - 30
    b.append(f'<path d="M{ax},{ay+10} L{ax+10},{ay} M{ax+2},{ay} H{ax+10} V{ay+8}" stroke="{col}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
    b.append("</g>")
    return svg(CW, CH, "\n".join(b), style)


def work(c):
    s = Seq(c, start=0.3, gap=0.3, typing=0.5)
    b, y = [], 4
    inner, w, h = bubble(c, 0, y, [WORK_OPEN], size=19, weight=600)
    b.append(s.add(0, y, inner))
    y += h + 10

    # dashboard attachment
    BW, pad = 600, 10
    cap = wrap(DASH_CAPTION, 17, BW - 36)
    ch = 210
    BH = pad + ch + 14 + len(cap) * 24 + 10
    vals = [.42, .55, .48, .7, .62, .81, .58, .74, .9, .68, .78, .95]
    cx0, cy0, cw = pad + 22, y + pad + 48, BW - 2 * pad - 44
    bw = cw / len(vals) * 0.56
    hmax = ch - 72
    d = [f'<path d="{rr(0, y, BW, BH, 5, 18, 18, 18)}" fill="{c["bub"]}"/>',
         f'<rect x="{pad}" y="{y+pad}" width="{BW-2*pad}" height="{ch}" rx="12" fill="{c["bub2"]}"/>',
         T(pad + 22, y + pad + 30, "Sales by store, this month", 14, c["muted"], 600)]
    chip = "24 stores live"
    cwid = tw(chip, 12, 600) + 22
    d.append(f'<rect x="{BW-pad-22-cwid:.1f}" y="{y+pad+14}" width="{cwid:.1f}" height="24" rx="12" fill="{c["green"]}" fill-opacity=".18"/>')
    d.append(T(BW - pad - 22 - cwid + 11, y + pad + 30, chip, 12, c["green"], 600))
    pts = []
    for i, v in enumerate(vals):
        bx = cx0 + i * cw / len(vals) + (cw / len(vals) - bw) / 2
        bh = v * hmax
        by = cy0 + hmax - bh
        colr = c["mari_fill"] if i == len(vals) - 1 else c["line"]
        d.append(f'<rect class="bar" style="animation-delay:{0.9+i*0.06:.2f}s" x="{bx:.1f}" y="{by:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="4" fill="{colr}"/>')
        pts.append((bx + bw / 2, by - 14))
    line = "M" + " L".join(f"{px:.1f},{py:.1f}" for px, py in pts)
    d.append(f'<path class="spark" d="{line}" pathLength="1" stroke="{c["mari"]}" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>')
    lx, ly = pts[-1]
    d.append(f'<circle class="pop" style="animation-delay:2.2s" cx="{lx:.1f}" cy="{ly:.1f}" r="5" fill="{c["mari"]}"/>')
    for i, ln in enumerate(cap):
        d.append(T(18, y + pad + ch + 30 + i * 24, ln, 17, c["text"]))
    b.append(s.add(0, y, "".join(d)))
    y += BH + 10

    for msg in WORK:
        inner, w, h = bubble(c, 0, y, wrap(msg, 17, 560), size=17, tail=False)
        b.append(s.add(0, y, inner))
        y += h + 10

    # voice note
    VW = 600
    cap = wrap(VOICE_CAPTION, 17, VW - 36)
    VH = 76 + len(cap) * 24 + 14
    v = [f'<path d="{rr(0, y, VW, VH, 18, 18, 18, 18)}" fill="{c["bub"]}"/>',
         f'<circle cx="44" cy="{y+40}" r="24" fill="{c["mari_fill"]}"/>',
         f'<path d="M38,{y+29} L53,{y+40} L38,{y+51} Z" fill="{c["on_mari"]}"/>']
    heights = [6, 12, 20, 14, 26, 18, 10, 22, 30, 16, 24, 12, 28, 20, 8, 18, 26, 14, 22, 10,
               16, 30, 20, 12, 24, 18, 8, 14, 26, 20, 12, 22, 16, 10, 18, 6]
    gx, gw = 84, 6.4
    bars = "".join(f'<rect x="{gx+i*12:.1f}" y="{y+40-hh/2:.1f}" width="{gw}" height="{hh}" rx="3"/>'
                   for i, hh in enumerate(heights))
    total = len(heights) * 12
    v.append(f'<g fill="{c["line"]}">{bars}</g>')
    v.append(f'<defs><clipPath id="prog"><rect class="prog" x="{gx}" y="{y+10}" width="{total}" height="60"/></clipPath></defs>')
    v.append(f'<g fill="{c["mari"]}" clip-path="url(#prog)">{bars}</g>')
    v.append(T(VW - 18, y + 46, "0:42", 14, c["muted"], 600, "end"))
    for i, ln in enumerate(cap):
        v.append(T(18, y + 96 + i * 24, ln, 17, c["text"]))
    b.append(s.add(0, y, "".join(v)))
    y += VH + 4

    style = """
.bar{animation:bar .8s cubic-bezier(.2,.8,.2,1) both;transform-box:fill-box;transform-origin:50% 100%}
@keyframes bar{from{transform:scaleY(0)}}
.spark{stroke-dasharray:1;stroke-dashoffset:1;animation:draw 1.2s ease-out 1.6s forwards}
@keyframes draw{to{stroke-dashoffset:0}}
.prog{transform-box:fill-box;transform-origin:0 50%;animation:prog 9s linear infinite}
@keyframes prog{from{transform:scaleX(0)}to{transform:scaleX(1)}}
""" + "\n".join(s.css)
    return svg(W, y, "\n".join(b), style)


def simple(c, text, weight=600, start=0.3):
    s = Seq(c, start=start)
    inner, w, h = bubble(c, 0, 4, wrap(text, 19, 640, weight), size=19, weight=weight)
    return svg(W, h + 8, s.add(0, 4, inner), "\n".join(s.css))


def reply_btn(c, label):
    BW, BH = 430, 48
    b = [f'<rect x="1" y="1" width="{BW-2}" height="{BH-2}" rx="{(BH-2)/2}" stroke="{c["mari"]}" stroke-width="1.6"/>',
         f'<path d="M30,17 L22,24 L30,31 M22,24 H36 C42,24 46,28 46,34" stroke="{c["mari"]}" stroke-width="2" '
         'stroke-linecap="round" stroke-linejoin="round"/>',
         T(58, 30.5, label, 16, c["mari"], 600)]
    return svg(BW, BH, "\n".join(b))


def stack(c):
    s = Seq(c, start=0.3)
    x0, padx, lab_w = 0, 20, 128
    rows = []
    y = 4 + 18 + 24
    body = [T(padx, 4 + 18 + 19 * 0.93, STACK_OPEN, 19, c["text"], 600)]
    y = 4 + 18 + 19 + 22
    maxx = 0
    for lab, items in STACK:
        body.append(T(padx, y + 21, lab, 15, c["muted"], 600))
        x = padx + lab_w
        for it in items:
            iw = tw(it, 15, 600) + 26
            body.append(f'<rect x="{x:.1f}" y="{y}" width="{iw:.1f}" height="32" rx="16" fill="{c["bub2"]}"/>')
            body.append(T(x + 13, y + 21, it, 15, c["text"], 600))
            x += iw + 8
        maxx = max(maxx, x)
        y += 42
    BW, BH = maxx + padx - 8, y - 4 + 10
    inner = f'<path d="{rr(0, 4, BW, BH, 5, 18, 18, 18)}" fill="{c["bub"]}"/>' + "".join(body)
    return svg(W, BH + 8, s.add(0, 4, inner), "\n".join(s.css))


def compose(c):
    H = 64
    b = [f'<rect x="1" y="4" width="{W-80}" height="56" rx="28" fill="{c["bub"]}" stroke="{c["line"]}"/>',
         f'<rect x="28" y="20" width="2.5" height="24" fill="{c["mari"]}">'
         '<animate attributeName="opacity" values="1;0;1" dur="1.1s" calcMode="discrete" repeatCount="indefinite"/></rect>',
         T(40, 38.5, COMPOSE, 18, c["muted"]),
         f'<circle cx="{W-32}" cy="32" r="28" fill="{c["mari_fill"]}"/>',
         f'<path d="M{W-44},{32} L{W-20},{21} L{W-27},{44} L{W-33},{35} Z M{W-33},{35} L{W-20},{21}" '
         f'fill="{c["on_mari"]}" stroke="{c["on_mari"]}" stroke-width="1.6" stroke-linejoin="round"/>']
    return svg(W, H, "\n".join(b))


# ------------------------------------------------------------------ README
def pic(name, alt, width="100%", extra=""):
    return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="./assets/{name}-dark.svg?v={V}">'
            f'<source media="(prefers-color-scheme: light)" srcset="./assets/{name}-light.svg?v={V}">'
            f'<img src="./assets/{name}-dark.svg?v={V}" width="{width}" alt="{esc(alt)}"{extra}></picture>')


def ext_pic(dark, light, alt, width="100%"):
    return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="{dark}">'
            f'<source media="(prefers-color-scheme: light)" srcset="{light}">'
            f'<img src="{dark}" width="{width}" alt="{esc(alt)}"></picture>')


ANSWERS = {
    "build": f"""I build business software end to end: database, API, admin panels, deployment and hosting.

- **Analytics dashboards** with live KPIs, role-based access and Google Sheets sync
- **Telecalling CRMs** that pull leads from Meta lead ads and website forms
- **Queue and token systems** with QR tokens, staff screens and TV displays
- **Online stores** with per-size stock, invoices and payment gateways

Usually FastAPI or Laravel with React and MySQL, deployed on a VPS with automatic deploys from GitHub.

**[Email me about your project](mailto:{EMAIL}?subject=Project%20enquiry%20from%20GitHub)**""",
    "whatsapp": """That's what **[Emiratick](https://emiratick.ae)** does. It runs on the official WhatsApp Cloud API:

- Bulk campaigns with approved templates
- Automated replies and order updates
- Delivery, read and cost reports per campaign

**[Visit emiratick.ae](https://emiratick.ae)**""",
    "learn": """Come to **[Town Institutes](https://towninstitutes.com)** in Electronic City, Bengaluru.

- Python, Java, React, Laravel and more
- Internships on real projects
- No IT background needed

**[Visit towninstitutes.com](https://towninstitutes.com)**""",
    "tees": """**[Loopstitch](https://loopstitch.online)** prints your design on premium tees, starting from a single piece.

- Your own artwork or one of our streetwear designs
- Oversized fits in heavyweight cotton

**[Visit loopstitch.online](https://loopstitch.online)** · Instagram **[@loopstitch_co](https://www.instagram.com/loopstitch_co)**""",
    "dev": """- **Apps:** FastAPI or Laravel APIs, React + Vite + Tailwind frontends, MySQL or MariaDB
- **Servers:** VPS managed with aaPanel and Nginx, Docker for side services, Cloudflare in front
- **Deploys:** GitHub Actions on every push to main
- **This profile:** generated by [`scripts/build.py`](scripts/build.py), plain animated SVGs with an embedded font, no JavaScript""",
}


def readme():
    STREAK = ("https://streak-stats.demolab.com?user=abhin-ms&hide_border=true&border_radius=20"
              "&background={bg}&ring={ring}&fire={fire}&currStreakNum={num}&sideNums={num}"
              "&currStreakLabel={ring}&sideLabels={muted}&dates={muted}")
    GRAPH = ("https://github-readme-activity-graph.vercel.app/graph?username=abhin-ms&bg_color={bg}"
             "&color={muted}&title_color={num}&line={ring}&point={fire}&area=true&area_color={ring}"
             "&hide_border=true&radius=20&custom_title=Contributions%20in%20the%20last%2031%20days")
    tok = {"dark": dict(bg="1A2036", ring="F6B13A", fire="FF5A5F", num="E9ECF8", muted="929AC0"),
           "light": dict(bg="EEF0F9", ring="A65F00", fire="D7263D", num="161A2E", muted="59618A")}
    snake = "https://raw.githubusercontent.com/abhin-ms/abhin-ms/output/snake{}.svg"

    cards = "\n".join(f'<a href="{v["url"]}">{pic("venture-" + v["slug"], v["name"] + ": " + v["desc"], "32%")}</a>'
                      for v in VENTURES)
    parts = [
        "<!-- Generated by scripts/build.py. Edit the content there, then run it. -->",
        pic("head", f"{NAME}, {ROLE}, {PLACE}"),
        pic("intro", HELLO + " " + " ".join(INTRO)),
        f'<p>\n{cards}\n</p>',
        pic("work", " ".join([WORK_OPEN, DASH_CAPTION] + WORK + [VOICE_CAPTION])),
        pic("ask", ASK),
    ]
    for key, label in REPLIES:
        parts.append(f'<details>\n<summary>{pic("reply-" + key, label, "430", ' align="absmiddle"')}</summary>\n\n'
                     f'{ANSWERS[key]}\n\n</details>')
    parts += [
        pic("stack", STACK_OPEN + " " + "; ".join(f"{l}: {', '.join(i)}" for l, i in STACK)),
        pic("activity", ACTIVITY),
        ext_pic(STREAK.format(**tok["dark"]), STREAK.format(**tok["light"]), "GitHub streak"),
        ext_pic(GRAPH.format(**tok["dark"]), GRAPH.format(**tok["light"]), "Contribution graph"),
        ext_pic(snake.format("-dark"), snake.format(""), "Snake eating my contribution graph"),
        f'<a href="mailto:{EMAIL}">{pic("compose", COMPOSE)}</a>',
        f'<p><a href="mailto:{EMAIL}">Email</a> &nbsp;&nbsp;&nbsp; '
        f'<a href="https://www.instagram.com/loopstitch_co">Loopstitch on Instagram</a> &nbsp;&nbsp;&nbsp; '
        f'<img src="https://komarev.com/ghpvc/?username=abhin-ms&color=a65f00&style=flat-square&label=profile%20views" '
        f'alt="Profile views" align="absmiddle"></p>',
    ]
    return "\n\n".join(parts) + "\n"


def main():
    OUT.mkdir(exist_ok=True)
    for f in OUT.glob("*.svg"):
        f.unlink()
    for name, c in THEMES.items():
        files = {"head": head(c), "intro": intro(c), "work": work(c), "compose": compose(c),
                 "ask": simple(c, ASK), "activity": simple(c, ACTIVITY), "stack": stack(c)}
        for i, v in enumerate(VENTURES):
            files["venture-" + v["slug"]] = venture(c, v, i)
        for key, label in REPLIES:
            files["reply-" + key] = reply_btn(c, label)
        for k, content in files.items():
            (OUT / f"{k}-{name}.svg").write_text(content, encoding="utf-8")
    (ROOT / "README.md").write_text(readme(), encoding="utf-8")
    total = sum(f.stat().st_size for f in OUT.glob("*.svg"))
    print(f"{len(list(OUT.glob('*.svg')))} SVGs, {total/1024:.0f} KB total; README.md written")


if __name__ == "__main__":
    main()
