#!/usr/bin/env python3
"""Generate blueprint-style SVG illustrations for the Hariom Computers site."""
import os

OUT = "/home/claude/agency-site/assets"
os.makedirs(OUT, exist_ok=True)

# Palette
AMBER = "#d97706"
INK = "#0e2338"
LINE = "rgba(16,32,47,0.30)"
LINE_SOFT = "rgba(16,32,47,0.15)"
FILL_SOFT = "rgba(16,60,90,0.05)"
VIOLET = "#5b5fb0"

# Dark variants (used inside dark title-block panels)
D_LINE = "rgba(233,239,245,0.34)"
D_LINE_SOFT = "rgba(233,239,245,0.16)"
D_FILL = "rgba(120,170,220,0.09)"
D_INK = "#eaf0f6"


def grid(w, h, step=20, color=None):
    """Blueprint grid background."""
    c = color or LINE_SOFT
    parts = [f'<rect width="{w}" height="{h}" fill="none"/>']
    x = step
    while x < w:
        parts.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{h}" stroke="{c}" stroke-width="0.5"/>')
        x += step
    y = step
    while y < h:
        parts.append(f'<line x1="0" y1="{y}" x2="{w}" y2="{y}" stroke="{c}" stroke-width="0.5"/>')
        y += step
    return "".join(parts)


def wrap(w, h, body, bg="none"):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}" role="img">'
            f'<rect width="{w}" height="{h}" fill="{bg}"/>{body}</svg>')


def browser_chrome(w, y=0, dark=False):
    """Browser window top bar with traffic-light dots."""
    ln = D_LINE if dark else LINE
    return (f'<rect x="0.5" y="{y+0.5}" width="{w-1}" height="26" fill="none" '
            f'stroke="{ln}" stroke-width="1"/>'
            f'<circle cx="16" cy="{y+13}" r="3.5" fill="{AMBER}" opacity="0.85"/>'
            f'<circle cx="30" cy="{y+13}" r="3.5" fill="{ln}"/>'
            f'<circle cx="44" cy="{y+13}" r="3.5" fill="{ln}"/>'
            f'<rect x="60" y="{y+7}" width="{w-80}" height="12" fill="none" '
            f'stroke="{ln}" stroke-width="1"/>')


# ---------------------------------------------------------------- WORK THUMBS
def work_news(w=560, h=300):
    """News / content platform wireframe."""
    b = [grid(w, h), browser_chrome(w)]
    # masthead
    b.append(f'<rect x="24" y="48" width="180" height="14" fill="{AMBER}" opacity="0.85"/>')
    b.append(f'<rect x="24" y="70" width="110" height="7" fill="{LINE}"/>')
    # hero article
    b.append(f'<rect x="24" y="95" width="320" height="120" fill="{FILL_SOFT}" stroke="{LINE}" stroke-width="1"/>')
    b.append(f'<path d="M24 175 L110 130 L175 175 L235 145 L344 200 L344 215 L24 215 Z" fill="{LINE_SOFT}"/>')
    b.append(f'<circle cx="290" cy="125" r="14" fill="none" stroke="{AMBER}" stroke-width="1.5"/>')
    # sidebar article cards
    for i in range(3):
        y = 95 + i * 42
        b.append(f'<rect x="360" y="{y}" width="176" height="32" fill="none" stroke="{LINE}" stroke-width="1"/>')
        b.append(f'<rect x="368" y="{y+8}" width="90" height="6" fill="{LINE}"/>')
        b.append(f'<rect x="368" y="{y+19}" width="130" height="5" fill="{LINE_SOFT}"/>')
    # footer text lines
    for i, wd in enumerate((300, 250, 180)):
        b.append(f'<rect x="24" y="{232 + i*14}" width="{wd}" height="6" fill="{LINE_SOFT}"/>')
    return wrap(w, h, "".join(b))


def work_ecommerce(w=560, h=300):
    """E-commerce storefront wireframe."""
    b = [grid(w, h), browser_chrome(w)]
    b.append(f'<rect x="24" y="48" width="120" height="12" fill="{AMBER}" opacity="0.85"/>')
    # nav
    for i in range(4):
        b.append(f'<rect x="{300 + i*58}" y="50" width="44" height="7" fill="{LINE}"/>')
    # product grid
    for r in range(2):
        for c in range(4):
            x = 24 + c * 130
            y = 80 + r * 108
            b.append(f'<rect x="{x}" y="{y}" width="112" height="96" fill="{FILL_SOFT}" stroke="{LINE}" stroke-width="1"/>')
            # product silhouette
            b.append(f'<rect x="{x+26}" y="{y+16}" width="60" height="42" fill="{LINE_SOFT}"/>')
            b.append(f'<rect x="{x+12}" y="{y+68}" width="60" height="6" fill="{LINE}"/>')
            b.append(f'<rect x="{x+12}" y="{y+80}" width="34" height="7" fill="{AMBER}" opacity="0.7"/>')
    # cart badge
    b.append(f'<circle cx="524" cy="53" r="11" fill="none" stroke="{AMBER}" stroke-width="1.5"/>')
    b.append(f'<path d="M519 49h2l2 7h5" stroke="{AMBER}" stroke-width="1.3" fill="none"/>')
    return wrap(w, h, "".join(b))


def work_automation(w=560, h=300):
    """Automated publishing / cron platform — node diagram."""
    b = [grid(w, h)]
    nodes = [(90, 80, "SRC"), (90, 220, "SRC"), (280, 150, "CRON"), (470, 80, "WEB"), (470, 220, "SOCIAL")]
    # connections
    conn = [((90, 80), (280, 150)), ((90, 220), (280, 150)),
            ((280, 150), (470, 80)), ((280, 150), (470, 220))]
    for (x1, y1), (x2, y2) in conn:
        mx = (x1 + x2) / 2
        b.append(f'<path d="M{x1} {y1} C{mx} {y1}, {mx} {y2}, {x2} {y2}" '
                 f'fill="none" stroke="{LINE}" stroke-width="1.5" stroke-dasharray="5 4"/>')
    for x, y, label in nodes:
        is_hub = label == "CRON"
        r = 42 if is_hub else 34
        stroke = AMBER if is_hub else LINE
        sw = 2 if is_hub else 1.5
        b.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#ffffff" stroke="{stroke}" stroke-width="{sw}"/>')
        b.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{FILL_SOFT}" stroke="none"/>')
        fill = AMBER if is_hub else "#4b6172"
        b.append(f'<text x="{x}" y="{y+4}" text-anchor="middle" font-family="IBM Plex Mono, monospace" '
                 f'font-size="12" fill="{fill}">{label}</text>')
    # clock accent on hub
    b.append(f'<circle cx="280" cy="150" r="54" fill="none" stroke="{AMBER}" stroke-width="1" '
             f'stroke-dasharray="3 6" opacity="0.6"/>')
    return wrap(w, h, "".join(b))


def work_aggregator(w=560, h=300):
    """Product aggregation — feeds merging into a list."""
    b = [grid(w, h)]
    # source feeds (left)
    for i in range(3):
        y = 60 + i * 90
        b.append(f'<rect x="24" y="{y}" width="120" height="58" fill="{FILL_SOFT}" stroke="{LINE}" stroke-width="1"/>')
        b.append(f'<rect x="36" y="{y+14}" width="60" height="6" fill="{LINE}"/>')
        b.append(f'<rect x="36" y="{y+28}" width="90" height="5" fill="{LINE_SOFT}"/>')
        b.append(f'<rect x="36" y="{y+39}" width="70" height="5" fill="{LINE_SOFT}"/>')
        # arrow into merge point
        b.append(f'<path d="M150 {y+29} C200 {y+29}, 200 150, 250 150" fill="none" '
                 f'stroke="{AMBER}" stroke-width="1.4" opacity="0.8"/>')
    # merge node
    b.append(f'<circle cx="262" cy="150" r="14" fill="none" stroke="{AMBER}" stroke-width="2"/>')
    b.append(f'<path d="M256 150h12M262 144v12" stroke="{AMBER}" stroke-width="1.6"/>')
    b.append(f'<line x1="276" y1="150" x2="320" y2="150" stroke="{LINE}" stroke-width="1.5"/>')
    # unified result list (right)
    b.append(f'<rect x="320" y="46" width="216" height="208" fill="none" stroke="{LINE}" stroke-width="1.5"/>')
    for i in range(5):
        y = 62 + i * 38
        b.append(f'<rect x="334" y="{y}" width="30" height="26" fill="{LINE_SOFT}"/>')
        b.append(f'<rect x="374" y="{y+4}" width="88" height="6" fill="{LINE}"/>')
        b.append(f'<rect x="374" y="{y+16}" width="56" height="5" fill="{LINE_SOFT}"/>')
        b.append(f'<rect x="486" y="{y+6}" width="34" height="8" fill="{AMBER}" opacity="0.65"/>')
    return wrap(w, h, "".join(b))


# ------------------------------------------------------- SERVICE HERO PANELS
def svc_wordpress(w=420, h=262):
    b = [grid(w, h, 20, D_LINE_SOFT), browser_chrome(w, 0, dark=True)]
    b.append(f'<rect x="20" y="44" width="110" height="10" fill="{AMBER}" opacity="0.9"/>')
    # content blocks / layered CMS feel
    b.append(f'<rect x="20" y="68" width="250" height="86" fill="{D_FILL}" stroke="{D_LINE}" stroke-width="1"/>')
    b.append(f'<rect x="32" y="82" width="120" height="7" fill="{D_LINE}"/>')
    b.append(f'<rect x="32" y="98" width="200" height="5" fill="{D_LINE_SOFT}"/>')
    b.append(f'<rect x="32" y="110" width="170" height="5" fill="{D_LINE_SOFT}"/>')
    b.append(f'<rect x="32" y="126" width="70" height="16" fill="{AMBER}" opacity="0.75"/>')
    # sidebar widgets
    for i in range(3):
        y = 68 + i * 32
        b.append(f'<rect x="286" y="{y}" width="114" height="24" fill="none" stroke="{D_LINE}" stroke-width="1"/>')
    # plugin/module stack
    for i in range(3):
        x = 20 + i * 86
        b.append(f'<rect x="{x}" y="170" width="74" height="60" fill="none" stroke="{D_LINE}" stroke-width="1"/>')
        b.append(f'<circle cx="{x+37}" cy="192" r="10" fill="none" stroke="{AMBER}" stroke-width="1.4"/>')
        b.append(f'<rect x="{x+16}" y="210" width="42" height="5" fill="{D_LINE_SOFT}"/>')
    return wrap(w, h, "".join(b))


def svc_laravel(w=420, h=262):
    """Backend / API layers diagram."""
    b = [grid(w, h, 20, D_LINE_SOFT)]
    layers = [("CLIENT", 38), ("API LAYER", 100), ("BUSINESS LOGIC", 162), ("DATABASE", 224)]
    for i, (label, y) in enumerate(layers):
        accent = i == 1
        stroke = AMBER if accent else D_LINE
        b.append(f'<rect x="40" y="{y-22}" width="340" height="44" fill="{D_FILL}" '
                 f'stroke="{stroke}" stroke-width="{2 if accent else 1}"/>')
        color = AMBER if accent else D_INK
        b.append(f'<text x="60" y="{y+4}" font-family="IBM Plex Mono, monospace" font-size="12" '
                 f'fill="{color}">{label}</text>')
        # connector arrows
        if i < len(layers) - 1:
            ny = layers[i+1][1] - 22
            b.append(f'<path d="M210 {y+22} L210 {ny}" stroke="{D_LINE}" stroke-width="1.4"/>')
            b.append(f'<path d="M206 {ny-6} L210 {ny} L214 {ny-6}" fill="none" stroke="{D_LINE}" stroke-width="1.4"/>')
    # DB cylinder hint
    b.append(f'<ellipse cx="342" cy="212" rx="18" ry="6" fill="none" stroke="{AMBER}" stroke-width="1.3"/>')
    b.append(f'<path d="M324 212v12a18 6 0 0 0 36 0v-12" fill="none" stroke="{AMBER}" stroke-width="1.3"/>')
    return wrap(w, h, "".join(b))


def svc_shopify(w=420, h=262):
    b = [grid(w, h, 20, D_LINE_SOFT), browser_chrome(w, 0, dark=True)]
    # product hero
    b.append(f'<rect x="20" y="44" width="150" height="120" fill="{D_FILL}" stroke="{D_LINE}" stroke-width="1"/>')
    b.append(f'<rect x="48" y="70" width="94" height="68" fill="{D_LINE_SOFT}"/>')
    # product detail
    b.append(f'<rect x="186" y="50" width="130" height="8" fill="{D_LINE}"/>')
    b.append(f'<rect x="186" y="68" width="70" height="14" fill="{AMBER}" opacity="0.85"/>')
    for i in range(3):
        b.append(f'<rect x="186" y="{94 + i*13}" width="{180 - i*30}" height="5" fill="{D_LINE_SOFT}"/>')
    # add to cart button
    b.append(f'<rect x="186" y="140" width="130" height="26" fill="none" stroke="{AMBER}" stroke-width="1.6"/>')
    b.append(f'<text x="251" y="157" text-anchor="middle" font-family="IBM Plex Mono, monospace" '
             f'font-size="10" fill="{AMBER}">ADD TO CART</text>')
    # variant swatches
    for i in range(4):
        b.append(f'<circle cx="{332 + 0}" cy="{58 + i*26}" r="9" fill="none" stroke="{D_LINE}" stroke-width="1.2"/>')
    # checkout steps
    for i in range(3):
        x = 20 + i * 132
        b.append(f'<rect x="{x}" y="186" width="118" height="46" fill="none" stroke="{D_LINE}" stroke-width="1"/>')
        b.append(f'<text x="{x+12}" y="{212}" font-family="IBM Plex Mono, monospace" font-size="10" '
                 f'fill="{AMBER}">0{i+1}</text>')
        b.append(f'<rect x="{x+34}" y="205" width="62" height="5" fill="{D_LINE_SOFT}"/>')
        b.append(f'<rect x="{x+34}" y="215" width="40" height="5" fill="{D_LINE_SOFT}"/>')
    return wrap(w, h, "".join(b))


def svc_custom(w=420, h=262):
    """Custom app — dashboard with charts."""
    b = [grid(w, h, 20, D_LINE_SOFT), browser_chrome(w, 0, dark=True)]
    # sidebar
    b.append(f'<rect x="20" y="44" width="72" height="196" fill="{D_FILL}" stroke="{D_LINE}" stroke-width="1"/>')
    for i in range(5):
        y = 58 + i * 26
        c = AMBER if i == 1 else D_LINE_SOFT
        b.append(f'<rect x="30" y="{y}" width="52" height="7" fill="{c}"/>')
    # stat cards
    for i in range(3):
        x = 104 + i * 100
        b.append(f'<rect x="{x}" y="44" width="88" height="52" fill="none" stroke="{D_LINE}" stroke-width="1"/>')
        b.append(f'<rect x="{x+12}" y="56" width="32" height="5" fill="{D_LINE_SOFT}"/>')
        b.append(f'<text x="{x+12}" y="{82}" font-family="IBM Plex Mono, monospace" font-size="16" '
                 f'fill="{AMBER}">{[74, 12, 96][i]}%</text>')
    # bar chart
    b.append(f'<rect x="104" y="108" width="188" height="132" fill="none" stroke="{D_LINE}" stroke-width="1"/>')
    bars = [40, 66, 52, 88, 72, 104]
    for i, bh in enumerate(bars):
        x = 120 + i * 28
        b.append(f'<rect x="{x}" y="{224 - bh}" width="16" height="{bh}" fill="{AMBER}" '
                 f'opacity="{0.45 + i*0.09:.2f}"/>')
    # line chart panel
    b.append(f'<rect x="304" y="108" width="96" height="132" fill="none" stroke="{D_LINE}" stroke-width="1"/>')
    b.append(f'<polyline points="316,210 336,182 356,196 376,152 392,164" fill="none" '
             f'stroke="{AMBER}" stroke-width="1.8"/>')
    for px, py in [(316, 210), (336, 182), (356, 196), (376, 152), (392, 164)]:
        b.append(f'<circle cx="{px}" cy="{py}" r="2.6" fill="{AMBER}"/>')
    return wrap(w, h, "".join(b))


def svc_ai(w=420, h=262):
    """AI integration — neural net + chat bubbles."""
    b = [grid(w, h, 20, D_LINE_SOFT)]
    # neural network
    cols = [(70, [70, 130, 190]), (150, [56, 106, 156, 206]), (230, [80, 131, 182])]
    pts = {}
    for ci, (x, ys) in enumerate(cols):
        for yi, y in enumerate(ys):
            pts.setdefault(ci, []).append((x, y))
    for ci in range(len(cols) - 1):
        for (x1, y1) in pts[ci]:
            for (x2, y2) in pts[ci + 1]:
                b.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{D_LINE_SOFT}" stroke-width="0.7"/>')
    for ci, plist in pts.items():
        for (x, y) in plist:
            fill = AMBER if ci == 1 else "none"
            op = "0.85" if ci == 1 else "1"
            b.append(f'<circle cx="{x}" cy="{y}" r="7" fill="{fill}" opacity="{op}" '
                     f'stroke="{AMBER if ci==1 else D_LINE}" stroke-width="1.4"/>')
    # chat bubbles
    b.append(f'<rect x="282" y="52" width="118" height="42" rx="3" fill="{D_FILL}" stroke="{D_LINE}" stroke-width="1"/>')
    b.append(f'<rect x="294" y="64" width="72" height="5" fill="{D_LINE_SOFT}"/>')
    b.append(f'<rect x="294" y="76" width="52" height="5" fill="{D_LINE_SOFT}"/>')
    b.append(f'<rect x="282" y="110" width="118" height="54" rx="3" fill="none" stroke="{AMBER}" stroke-width="1.5"/>')
    b.append(f'<rect x="294" y="122" width="86" height="5" fill="{AMBER}" opacity="0.7"/>')
    b.append(f'<rect x="294" y="134" width="66" height="5" fill="{AMBER}" opacity="0.5"/>')
    b.append(f'<rect x="294" y="146" width="78" height="5" fill="{AMBER}" opacity="0.5"/>')
    # typing dots
    for i in range(3):
        b.append(f'<circle cx="{296 + i*14}" cy="192" r="4" fill="{D_LINE}"/>')
    b.append(f'<text x="282" y="228" font-family="IBM Plex Mono, monospace" font-size="10" '
             f'fill="{AMBER}">MODEL → RESPONSE</text>')
    return wrap(w, h, "".join(b))


def svc_maintenance(w=420, h=262):
    """Maintenance — uptime monitor + status checks."""
    b = [grid(w, h, 20, D_LINE_SOFT)]
    # uptime graph panel
    b.append(f'<rect x="20" y="30" width="380" height="110" fill="{D_FILL}" stroke="{D_LINE}" stroke-width="1"/>')
    b.append(f'<text x="34" y="52" font-family="IBM Plex Mono, monospace" font-size="10" '
             f'fill="{D_INK}" opacity="0.7">UPTIME · 30 DAYS</text>')
    b.append(f'<text x="336" y="52" font-family="IBM Plex Mono, monospace" font-size="13" fill="#5fe08f">99.9%</text>')
    # uptime bars
    for i in range(38):
        x = 34 + i * 9.6
        down = i in (11, 25)
        color = "#e0574f" if down else "#5fe08f"
        h_bar = 34 if down else 52
        b.append(f'<rect x="{x:.1f}" y="{124 - h_bar}" width="6" height="{h_bar}" fill="{color}" opacity="0.8"/>')
    # checklist rows
    rows = [("CORE UPDATES", True), ("PLUGIN UPDATES", True), ("BACKUP VERIFIED", True), ("SECURITY SCAN", True)]
    for i, (label, ok) in enumerate(rows):
        y = 164 + i * 26
        b.append(f'<rect x="20" y="{y-14}" width="380" height="22" fill="none" stroke="{D_LINE_SOFT}" stroke-width="1"/>')
        b.append(f'<text x="38" y="{y+1}" font-family="IBM Plex Mono, monospace" font-size="10" '
                 f'fill="{D_INK}" opacity="0.75">{label}</text>')
        b.append(f'<path d="M370 {y-4} l4 5 l8 -9" fill="none" stroke="{AMBER}" stroke-width="1.8"/>')
    return wrap(w, h, "".join(b))


def hero_home(w=420, h=262):
    """Home hero: agency (front) + Hariom Computers (behind) relationship."""
    b = [grid(w, h, 20, D_LINE_SOFT)]
    # back panel = us
    b.append(f'<rect x="60" y="40" width="200" height="150" fill="{D_FILL}" stroke="{D_LINE}" '
             f'stroke-width="1" stroke-dasharray="6 4"/>')
    b.append(f'<text x="74" y="62" font-family="IBM Plex Mono, monospace" font-size="10" '
             f'fill="{AMBER}">Hariom Computers</text>')
    # code lines on back panel
    for i, wd in enumerate((110, 78, 132, 94, 60)):
        b.append(f'<rect x="74" y="{76 + i*18}" width="{wd}" height="6" fill="{AMBER}" opacity="{0.5 - i*0.06:.2f}"/>')
    # front panel = your agency
    b.append(f'<rect x="150" y="86" width="210" height="146" fill="{INK}" stroke="{AMBER}" stroke-width="1.6"/>')
    b.append(f'<rect x="150" y="86" width="210" height="26" fill="none" stroke="{AMBER}" stroke-width="1.6"/>')
    b.append(f'<text x="164" y="104" font-family="IBM Plex Mono, monospace" font-size="10" '
             f'fill="{AMBER}">YOUR AGENCY</text>')
    b.append(f'<rect x="164" y="128" width="120" height="8" fill="{D_INK}" opacity="0.85"/>')
    for i, wd in enumerate((178, 150, 166)):
        b.append(f'<rect x="164" y="{148 + i*14}" width="{wd}" height="5" fill="{D_LINE}"/>')
    b.append(f'<rect x="164" y="196" width="86" height="22" fill="{AMBER}" opacity="0.85"/>')
    return wrap(w, h, "".join(b))


FILES = {
    "work-news.svg": work_news(),
    "work-ecommerce.svg": work_ecommerce(),
    "work-automation.svg": work_automation(),
    "work-aggregator.svg": work_aggregator(),
    "svc-wordpress.svg": svc_wordpress(),
    "svc-laravel.svg": svc_laravel(),
    "svc-shopify.svg": svc_shopify(),
    "svc-custom.svg": svc_custom(),
    "svc-ai.svg": svc_ai(),
    "svc-maintenance.svg": svc_maintenance(),
    "hero-home.svg": hero_home(),
}

for name, content in FILES.items():
    path = os.path.join(OUT, name)
    with open(path, "w") as f:
        f.write(content)
    print(f"{name}: {len(content):,} bytes")

print(f"\n{len(FILES)} SVG files written to {OUT}")
