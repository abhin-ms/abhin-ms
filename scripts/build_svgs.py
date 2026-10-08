"""Generates the animated SVGs used in the profile README.

Edit the CONTENT section, then run:  python3 scripts/build_svgs.py
Output goes to assets/. Bump the ?v= number in README.md after re-generating
so GitHub's image cache picks up the change.
"""
import base64
from pathlib import Path
from xml.sax.saxutils import escape as esc

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"
OUT.mkdir(exist_ok=True)

# ---------------------------------------------------------------- CONTENT
NAME = "Abhin M S"
STATUS = "AVAILABLE FOR FREELANCE PROJECTS"
TAGLINE = "Building software that businesses actually run on."
PHRASES = [
    "full-stack dev · FastAPI + React + Laravel",
    "founder: Emiratick · Loopstitch · Town Institutes",
    "ships dashboards, CRMs & WhatsApp bots",
]
META = ["Electronic City, Bengaluru", "1,100+ contributions / yr", "Self-hosted VPS infra"]
FLOAT_CHIPS = [("FastAPI", 812, 92), ("WhatsApp API", 1046, 318), ("React", 838, 330)]

VENTURES = [
    dict(slug="emiratick", name="Emiratick", tag="SAAS", color="#3ddc97",
         lines=["WhatsApp Cloud API platform for", "business messaging, campaigns", "and automation."],
         link="emiratick.ae", icon="chat"),
    dict(slug="loopstitch", name="Loopstitch", tag="LAUNCHING", color="#ff5b5b",
         lines=["Streetwear label + custom prints", "from a single piece. Store built", "in-house on FastAPI + React."],
         link="loopstitch.online", icon="shirt"),
    dict(slug="town", name="Town Institutes", tag="EDTECH", color="#ffb547",
         lines=["Software training & internships —", "Python, Java, React, Laravel.", "Open to every background."],
         link="towninstitutes.com", icon="cap"),
]

BUILDS = [
    ("01", "Analytics dashboards", ["Live KPIs, role-based access,", "Google Sheets sync — runs a", "24-store retail chain."]),
    ("02", "Telecalling CRMs", ["Leads flow in straight from", "Meta lead ads and website", "webhooks to the call queue."]),
    ("03", "WhatsApp automation", ["Cloud API panels, bulk", "campaigns, delivery & cost", "reporting for brands."]),
    ("04", "Queue & token systems", ["QR token generation, staff", "dashboards and live TV", "display boards."]),
    ("05", "E-commerce stores", ["Per-size stock locking,", "hidden admin panel, PDF", "invoices, payment gateway."]),
    ("06", "AI voice agents", ["Prompt-driven agents that", "call customers on a rented", "number. In progress."]),
]

STACK = [
    ("BACKEND", ["FastAPI", "Python", "Laravel", "PHP"]),
    ("FRONTEND", ["React", "Vite", "Tailwind", "TypeScript"]),
    ("DATA", ["MySQL", "MariaDB", "Google Sheets"]),
    ("INFRA", ["aaPanel", "Nginx", "Docker", "Cloudflare", "GH Actions"]),
    ("APIS", ["WhatsApp Cloud", "Meta Graph", "Shopify", "WooCommerce"]),
]

NOW = [
    ("$", "whoami --now", "#8a97a8"),
    (">", "launching loopstitch.online", "#ff5b5b"),
    (">", "building an AI voice-calling agent", "#3ddc97"),
    (">", "scaling Emiratick for more brands", "#3ddc97"),
    (">", "training devs at Town Institutes", "#ffb547"),
    (">", "taking on dashboard & CRM projects", "#5aa9ff"),
]

# ---------------------------------------------------------------- TOKENS
BG, PANEL, LINE = "#0a0e13", "#0f141b", "#1d2633"
TEXT, MUTED = "#e8edf3", "#8a97a8"
GREEN, RED, AMBER, BLUE = "#3ddc97", "#ff5b5b", "#ffb547", "#5aa9ff"
SANS = "'Segoe UI',Ubuntu,'Helvetica Neue',Arial,sans-serif"
MONO = "'JetBrains Mono','SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"


def svg(w, h, body, style=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none">\n'
        f"<style>\n.sans{{font-family:{SANS}}} .mono{{font-family:{MONO}}}\n{style}\n</style>\n{body}\n</svg>\n"
    )


def frame(w, h, rid):
    return (
        f'<defs><pattern id="dots{rid}" width="22" height="22" patternUnits="userSpaceOnUse">'
        f'<circle cx="1.5" cy="1.5" r="1.1" fill="{LINE}"/></pattern>'
        f'<clipPath id="card{rid}"><rect width="{w}" height="{h}" rx="18"/></clipPath></defs>'
        f'<rect width="{w}" height="{h}" rx="18" fill="{BG}"/>'
        f'<g clip-path="url(#card{rid})"><rect width="{w}" height="{h}" fill="url(#dots{rid})" opacity=".55"/></g>'
    )


def border(w, h):
    return f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="17.5" stroke="{LINE}"/>'


def chip(x, y, label, color, size=13, mono=True, fill=None):
    cw = size * (0.62 if mono else 0.56)
    w = int(len(label) * cw + 26)
    h = size + 14
    f = fill or PANEL
    return (
        f'<g transform="translate({x},{y})"><rect width="{w}" height="{h}" rx="{h/2}" fill="{f}" stroke="{color}" stroke-opacity=".45"/>'
        f'<text x="{w/2}" y="{h/2+size*0.36:.1f}" text-anchor="middle" class="{"mono" if mono else "sans"}" '
        f'font-size="{size}" fill="{color}">{esc(label)}</text></g>'
    ), w


# ---------------------------------------------------------------- BANNER
def banner():
    W, H = 1200, 420
    avatar = base64.b64encode((ROOT / "assets" / "avatar.jpg").read_bytes()).decode()
    style = f"""
.pulse{{animation:pulse 1.8s ease-in-out infinite;transform-box:fill-box;transform-origin:center}}
@keyframes pulse{{0%,100%{{opacity:1;transform:scale(1)}}50%{{opacity:.35;transform:scale(.7)}}}}
.spin{{animation:spin 18s linear infinite;transform-box:fill-box;transform-origin:center}}
.spinr{{animation:spin 9s linear infinite reverse;transform-box:fill-box;transform-origin:center}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
.float1{{animation:float 4.5s ease-in-out infinite}}
.float2{{animation:float 5.5s ease-in-out -1.5s infinite}}
.float3{{animation:float 5s ease-in-out -3s infinite}}
@keyframes float{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-9px)}}}}
.glow{{animation:drift 14s ease-in-out infinite alternate}}
@keyframes drift{{to{{transform:translate(120px,40px)}}}}
.caret{{animation:blink 1s steps(1) infinite}}
@keyframes blink{{50%{{opacity:0}}}}
.fadeup{{animation:fadeup .9s cubic-bezier(.2,.7,.2,1) both}}
.d1{{animation-delay:.15s}} .d2{{animation-delay:.3s}} .d3{{animation-delay:.45s}} .d4{{animation-delay:.6s}}
@keyframes fadeup{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1;transform:none}}}}
.under{{animation:under 2.4s cubic-bezier(.6,0,.2,1) .4s both}}
@keyframes under{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
"""
    b = [frame(W, H, "b")]
    b.append(
        f'<defs><radialGradient id="g1"><stop offset="0" stop-color="{GREEN}" stop-opacity=".22"/><stop offset="1" stop-color="{GREEN}" stop-opacity="0"/></radialGradient>'
        f'<radialGradient id="g2"><stop offset="0" stop-color="{RED}" stop-opacity=".16"/><stop offset="1" stop-color="{RED}" stop-opacity="0"/></radialGradient>'
        f'<linearGradient id="nameg" x1="0" x2="1"><stop offset="0" stop-color="{TEXT}"/><stop offset=".55" stop-color="{TEXT}"/><stop offset="1" stop-color="{GREEN}"/></linearGradient>'
        f'<linearGradient id="ring" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{GREEN}"/><stop offset=".5" stop-color="{GREEN}" stop-opacity="0"/><stop offset="1" stop-color="{RED}"/></linearGradient>'
        f'<clipPath id="av"><circle cx="980" cy="210" r="118"/></clipPath></defs>'
    )
    b.append('<g clip-path="url(#cardb)">')
    b.append('<g class="glow"><circle cx="160" cy="80" r="320" fill="url(#g1)"/></g>')
    b.append('<circle cx="1080" cy="400" r="300" fill="url(#g2)"/>')
    b.append("</g>")

    # status chip
    c, cw = chip(60, 48, STATUS, GREEN, 12)
    b.append(f'<g class="fadeup">{c}<circle cx="{60+cw+16}" cy="61" r="0"/></g>')
    b.append(f'<circle class="pulse" cx="{60+cw+18}" cy="61.5" r="5" fill="{GREEN}"/>')

    b.append(f'<text x="60" y="138" class="sans fadeup d1" font-size="22" fill="{MUTED}">Hey, I\'m</text>')
    b.append(f'<text x="56" y="212" class="sans fadeup d1" font-size="74" font-weight="800" letter-spacing="-1.5" fill="url(#nameg)">{esc(NAME)}</text>')
    b.append(f'<rect class="under" x="60" y="228" width="120" height="5" rx="2.5" fill="{GREEN}" style="transform-origin:60px 230px"/>')

    # typing line
    fs, cw_ = 22, 22 * 0.6
    x0, y0 = 92, 280
    T, n = 15.0, len(PHRASES)
    w = T / n
    frames = []  # (t, phrase, k)
    for i, p in enumerate(PHRASES):
        s, L = i * w, len(p)
        for k in range(L + 1):
            frames.append((s + 0.38 * w * k / L, i, k))
        for k in range(L, -1, -2):
            frames.append((s + 0.82 * w + 0.12 * w * (L - k) / L, i, k))
    frames.sort()
    kt = ";".join(f"{t/T:.4f}" for t, _, _ in frames)
    b.append(f'<text x="60" y="{y0}" class="mono" font-size="{fs}" fill="{GREEN}">&gt;</text>')
    for i, p in enumerate(PHRASES):
        vals = ";".join(f"{(k*cw_ if ph == i else 0):.1f}" for _, ph, k in frames)
        b.append(
            f'<clipPath id="ty{i}"><rect x="{x0}" y="{y0-24}" height="34" width="0">'
            f'<animate attributeName="width" dur="{T}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{kt}" values="{vals}"/></rect></clipPath>'
            f'<text x="{x0}" y="{y0}" class="mono" font-size="{fs}" fill="{TEXT}" clip-path="url(#ty{i})">{esc(p)}</text>'
        )
    cx = ";".join(f"{x0 + k*cw_ + 2:.1f}" for _, _, k in frames)
    b.append(
        f'<rect class="caret" x="{x0}" y="{y0-19}" width="11" height="23" fill="{GREEN}">'
        f'<animate attributeName="x" dur="{T}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{kt}" values="{cx}"/></rect>'
    )

    b.append(f'<text x="60" y="328" class="sans fadeup d2" font-size="18" fill="{MUTED}">{esc(TAGLINE)}</text>')

    x = 60
    for j, m in enumerate(META):
        col = [TEXT, GREEN, TEXT][j]
        c, cw = chip(0, 0, m, MUTED if col == TEXT else GREEN, 12)
        b.append(f'<g transform="translate({x},352)"><g class="fadeup d{j+2}">{c}</g></g>')
        x += cw + 10

    # avatar
    b.append(f'<circle cx="980" cy="210" r="150" stroke="{LINE}" stroke-dasharray="2 9" stroke-width="2" class="spin"/>')
    b.append(f'<circle cx="980" cy="210" r="134" stroke="url(#ring)" stroke-width="3" class="spinr"/>')
    b.append(f'<circle cx="980" cy="210" r="121" fill="{PANEL}"/>')
    b.append(f'<image clip-path="url(#av)" x="862" y="92" width="236" height="236" preserveAspectRatio="xMidYMid slice" href="data:image/jpeg;base64,{avatar}" xlink:href="data:image/jpeg;base64,{avatar}"/>')
    b.append(f'<g class="spin"><circle cx="980" cy="60" r="5" fill="{GREEN}"/><circle cx="980" cy="210" r="150" fill="none"/></g>')
    for k, (lab, fx, fy) in enumerate(FLOAT_CHIPS):
        c, _ = chip(fx, fy, lab, [GREEN, GREEN, BLUE][k], 12, fill="#0d1218")
        b.append(f'<g class="float{k+1}">{c}</g>')

    b.append(border(W, H))
    return svg(W, H, "\n".join(b), style)


# ---------------------------------------------------------------- SECTION LABEL
def label(text, num):
    W, H = 1200, 64
    style = f"""
.ln{{animation:grow 1.6s cubic-bezier(.6,0,.2,1) both;transform-box:fill-box;transform-origin:left}}
@keyframes grow{{from{{transform:scaleX(0)}}}}"""
    tw = len(text) * 15 + 70
    b = [
        f'<text x="0" y="40" class="mono" font-size="14" fill="{GREEN}">{num}</text>',
        f'<text x="38" y="40" class="mono" font-size="20" font-weight="700" letter-spacing="3" fill="{TEXT}">{esc(text)}</text>',
        f'<rect class="ln" x="{tw}" y="33" width="{W-tw}" height="1.5" fill="{LINE}"/>',
        f'<rect class="ln" x="{tw}" y="32.5" width="80" height="2.5" fill="{GREEN}"/>',
    ]
    return svg(W, H, "\n".join(b), style)


# ---------------------------------------------------------------- VENTURE CARD
ICONS = {
    "chat": '<path d="M4 18 6 12.8A8 8 0 1 1 9.4 16L4 18Z" stroke="{c}" stroke-width="2" stroke-linejoin="round"/><path d="M9 10h6M9 13h3.5" stroke="{c}" stroke-width="2" stroke-linecap="round"/>',
    "shirt": '<path d="M8 3 3.5 5.5 5 10l2.5-1V20h9V9l2.5 1L20.5 5.5 16 3c-.6 1.8-2.1 3-4 3s-3.4-1.2-4-3Z" stroke="{c}" stroke-width="2" stroke-linejoin="round"/>',
    "cap": '<path d="m2 9 10-5 10 5-10 5L2 9Z" stroke="{c}" stroke-width="2" stroke-linejoin="round"/><path d="M6 11v5c3 2.5 9 2.5 12 0v-5M22 9v6" stroke="{c}" stroke-width="2" stroke-linecap="round"/>',
}


def venture(v):
    W, H = 400, 250
    c = v["color"]
    style = f"""
.sweep{{animation:sweep 3.2s cubic-bezier(.6,0,.2,1) infinite}}
@keyframes sweep{{0%{{transform:translateX(-140px)}}60%,100%{{transform:translateX({W}px)}}}}
.pulse{{animation:pulse 2.2s ease-in-out infinite;transform-box:fill-box;transform-origin:center}}
@keyframes pulse{{0%,100%{{opacity:.9}}50%{{opacity:.25}}}}
.halo{{animation:halo 2.6s ease-out infinite;transform-box:fill-box;transform-origin:center}}
@keyframes halo{{from{{transform:scale(1);opacity:.5}}to{{transform:scale(1.55);opacity:0}}}}"""
    b = [frame(W, H, v["slug"])]
    b.append(
        f'<defs><linearGradient id="sw{v["slug"]}" x1="0" x2="1"><stop offset="0" stop-color="{c}" stop-opacity="0"/>'
        f'<stop offset=".5" stop-color="{c}"/><stop offset="1" stop-color="{c}" stop-opacity="0"/></linearGradient>'
        f'<radialGradient id="gl{v["slug"]}"><stop offset="0" stop-color="{c}" stop-opacity=".18"/><stop offset="1" stop-color="{c}" stop-opacity="0"/></radialGradient></defs>'
    )
    b.append(f'<g clip-path="url(#card{v["slug"]})"><circle cx="{W}" cy="0" r="200" fill="url(#gl{v["slug"]})"/>'
             f'<rect class="sweep" x="0" y="0" width="140" height="2.5" fill="url(#sw{v["slug"]})"/></g>')
    b.append(f'<rect class="halo" x="28" y="28" width="48" height="48" rx="14" stroke="{c}"/>')
    b.append(f'<rect x="28" y="28" width="48" height="48" rx="14" fill="{c}" fill-opacity=".12" stroke="{c}" stroke-opacity=".5"/>')
    b.append(f'<g transform="translate(40,40)">{ICONS[v["icon"]].format(c=c)}</g>')
    tc, tw = chip(0, 0, v["tag"], c, 11)
    b.append(f'<g transform="translate({W-28-tw},38)">{tc}</g>')
    b.append(f'<text x="28" y="118" class="sans" font-size="25" font-weight="700" fill="{TEXT}">{esc(v["name"])}</text>')
    for i, ln in enumerate(v["lines"]):
        b.append(f'<text x="28" y="{148+i*22}" class="sans" font-size="15" fill="{MUTED}">{esc(ln)}</text>')
    b.append(f'<line x1="28" y1="{H-46}" x2="{W-28}" y2="{H-46}" stroke="{LINE}"/>')
    b.append(f'<circle class="pulse" cx="34" cy="{H-24}" r="4" fill="{c}"/>')
    b.append(f'<text x="46" y="{H-19.5}" class="mono" font-size="13.5" fill="{c}">{esc(v["link"])}</text>')
    b.append(f'<text x="{W-28}" y="{H-19}" text-anchor="end" class="mono" font-size="15" fill="{c}">↗</text>')
    b.append(border(W, H))
    return svg(W, H, "\n".join(b), style)


# ---------------------------------------------------------------- BUILDS GRID
def builds():
    W, H = 1200, 470
    cols, gx, gy, pad = 3, 18, 18, 22
    tw = (W - 2 * pad - (cols - 1) * gx) / cols
    th = (H - 2 * pad - gy) / 2
    style = """
.tile{animation:fadeup .8s cubic-bezier(.2,.7,.2,1) both}
@keyframes fadeup{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}
.bar{animation:bar 4s ease-in-out infinite;transform-box:fill-box;transform-origin:left}
@keyframes bar{0%,100%{transform:scaleX(.25)}50%{transform:scaleX(1)}}"""
    accents = [GREEN, BLUE, GREEN, AMBER, RED, BLUE]
    b = [frame(W, H, "w")]
    for i, (num, title, lines) in enumerate(BUILDS):
        x = pad + (i % cols) * (tw + gx)
        y = pad + (i // cols) * (th + gy)
        a = accents[i]
        b.append(f'<g transform="translate({x:.1f},{y:.1f})"><g class="tile" style="animation-delay:{i*0.12:.2f}s">')
        b.append(f'<rect width="{tw:.1f}" height="{th:.1f}" rx="14" fill="{PANEL}" stroke="{LINE}"/>')
        b.append(f'<text x="22" y="40" class="mono" font-size="13" fill="{a}">{num}</text>')
        b.append(f'<rect class="bar" style="animation-delay:{i*0.5:.1f}s" x="52" y="34" width="{tw-74:.0f}" height="2" rx="1" fill="{a}" fill-opacity=".55"/>')
        b.append(f'<text x="22" y="80" class="sans" font-size="20" font-weight="700" fill="{TEXT}">{esc(title)}</text>')
        for j, ln in enumerate(lines):
            b.append(f'<text x="22" y="{110+j*22}" class="sans" font-size="14.5" fill="{MUTED}">{esc(ln)}</text>')
        b.append("</g></g>")
    b.append(border(W, H))
    return svg(W, H, "\n".join(b), style)


# ---------------------------------------------------------------- STACK
def stack():
    W, H = 590, 330
    style = """
.row{animation:fadeup .7s cubic-bezier(.2,.7,.2,1) both}
@keyframes fadeup{from{opacity:0;transform:translateX(-10px)}to{opacity:1;transform:none}}"""
    cols = [GREEN, BLUE, AMBER, RED, GREEN]
    b = [frame(W, H, "s")]
    b.append(f'<text x="28" y="44" class="mono" font-size="14" fill="{MUTED}">~/stack</text>')
    b.append(f'<text x="{W-28}" y="44" text-anchor="end" class="mono" font-size="12" fill="{GREEN}">● daily drivers</text>')
    for i, (lab, items) in enumerate(STACK):
        y = 70 + i * 50
        b.append(f'<g class="row" style="animation-delay:{i*0.12:.2f}s">')
        b.append(f'<text x="28" y="{y+20}" class="mono" font-size="11.5" letter-spacing="1.5" fill="{MUTED}">{lab}</text>')
        x = 118
        for it in items:
            c, w = chip(x, y + 2, it, cols[i], 12)
            if x + w > W - 24:
                break
            b.append(c)
            x += w + 8
        b.append("</g>")
    b.append(border(W, H))
    return svg(W, H, "\n".join(b), style)


# ---------------------------------------------------------------- NOW (terminal)
def now():
    W, H = 590, 330
    step, start = 0.55, 0.3
    total = start + step * len(NOW) + 6
    style = f"""
.caret{{animation:blink 1s steps(1) infinite}}
@keyframes blink{{50%{{opacity:0}}}}"""
    b = [frame(W, H, "n")]
    b.append(f'<rect x="1" y="1" width="{W-2}" height="50" rx="17" fill="{PANEL}"/><rect x="1" y="34" width="{W-2}" height="17" fill="{PANEL}"/>')
    b.append(f'<line x1="1" y1="51" x2="{W-1}" y2="51" stroke="{LINE}"/>')
    for k, col in enumerate([RED, AMBER, GREEN]):
        b.append(f'<circle cx="{30+k*20}" cy="26" r="6" fill="{col}" fill-opacity=".85"/>')
    b.append(f'<text x="{W/2}" y="31" text-anchor="middle" class="mono" font-size="12.5" fill="{MUTED}">abhin@town ~ now</text>')
    # each line appears at its own delay, holds, then the block clears and replays
    for i, (p, txt, col) in enumerate(NOW):
        f = (start + i * step) / total
        y = 92 + i * 36
        b.append(
            f'<g opacity="0"><animate attributeName="opacity" dur="{total:.2f}s" repeatCount="indefinite" '
            f'calcMode="discrete" keyTimes="0;{f:.4f};0.96" values="0;1;0"/>'
            f'<text x="28" y="{y}" class="mono" font-size="15" fill="{col}">{esc(p)}</text>'
            f'<text x="50" y="{y}" class="mono" font-size="15" fill="{TEXT if i else MUTED}">{esc(txt)}</text></g>'
        )
    y = 92 + len(NOW) * 36
    b.append(f'<text x="28" y="{y}" class="mono" font-size="15" fill="{GREEN}">$</text>')
    b.append(f'<rect class="caret" x="50" y="{y-14}" width="9" height="18" fill="{GREEN}"/>')
    b.append(border(W, H))
    return svg(W, H, "\n".join(b), style)


def write(name, content):
    (OUT / name).write_text(content, encoding="utf-8")
    print(f"{name:24s} {len(content)/1024:6.1f} KB")


if __name__ == "__main__":
    write("banner.svg", banner())
    for v in VENTURES:
        write(f"venture-{v['slug']}.svg", venture(v))
    write("label-ventures.svg", label("VENTURES", "01"))
    write("label-builds.svg", label("WHAT I BUILD FOR CLIENTS", "02"))
    write("label-stack.svg", label("STACK & RIGHT NOW", "03"))
    write("label-activity.svg", label("ACTIVITY", "04"))
    write("builds.svg", builds())
    write("stack.svg", stack())
    write("now.svg", now())
