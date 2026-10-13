#!/usr/bin/env python3
"""
Tutora AI - README animation builder
------------------------------------
Generates every animated SVG used in README.md (GitHub-safe: pure SVG + SMIL,
no <script>, no foreignObject, no external requests).

Usage (from repo root):
    python scripts/build-readme-assets.py

Optional (recommended, makes slideshow.svg small):
    pip install pillow

Edit SLIDES below to change slideshow titles / subtitles / screenshots,
then re-run the script. Missing screenshots become labelled placeholders.
"""
import base64
import io
import math
import os
import random
import sys
from xml.sax.saxutils import escape

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "assets", "animations")
SHOTS = os.path.join(ROOT, "assets", "screenshots")
os.makedirs(OUT, exist_ok=True)

FONT = "'Segoe UI','Inter',system-ui,-apple-system,Roboto,Helvetica,Arial,sans-serif"
BLUE, PURPLE, CYAN, GREEN, RED, PINK = "#2563eb", "#7c3aed", "#06b6d4", "#10b981", "#ef4444", "#ec4899"

# --------------------------------------------------------------------------
# SLIDESHOW CONFIG  -> change title / subtitle per slide here
# --------------------------------------------------------------------------
SLIDE_SECONDS = 5
SLIDES = [
    ("📊 Studio Dashboard", "Recordings, drafts & narration pipelines in one clean place", "dashboard.png"),
    ("🎙️ AI Tutorial Studio", "Per-step narration powered by the offline Kokoro + Resona engine", "ai-tutorial-studio.png"),
    ("🎬 Multi-Track Timeline & Keynotes", "Animated intro/outro · Fast 3s · Standard 5.5s · Cinematic 8s", "editor-keynote-intro.png"),
    ("🎯 Cursor Polish & Spring Physics", "Smooth paths, click shockwaves, cursor scale up to 4.0×", "cursor-polish-physics.png"),
    ("📹 Dynamic Webcam Bubble", "Zoom-reactive facecam that never covers essential UI", "webcam-bubble-overlay.png"),
    ("💬 Automatic Captions", "Fade · Slide · Bounce · Pop animated subtitles", "auto-captions.png"),
    ("⚡ Universal AI Model Hub", "Bring your own key with zero-failure provider failover", "ai-models-settings.png"),
]


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def svg(w, h, body, defs=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'font-family="{FONT}" role="img">\n<defs>{defs}</defs>\n{body}\n</svg>\n'
    )


def save(name, content):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✓ {name}  ({os.path.getsize(path) // 1024} KB)")


def A(attr, values, dur, kt=None, begin=0, once=False, mode=None, splines=None):
    s = f'<animate attributeName="{attr}" values="{values}" dur="{dur}s" begin="{begin}s"'
    if kt:
        s += f' keyTimes="{kt}"'
    if mode:
        s += f' calcMode="{mode}"'
    if splines:
        s += f' keySplines="{splines}"'
    s += ' fill="freeze"/>' if once else ' repeatCount="indefinite"/>'
    return s


def T(kind, values, dur, kt=None, begin=0, once=False):
    s = (f'<animateTransform attributeName="transform" type="{kind}" values="{values}" '
         f'dur="{dur}s" begin="{begin}s"')
    if kt:
        s += f' keyTimes="{kt}"'
    s += ' fill="freeze"/>' if once else ' repeatCount="indefinite"/>'
    return s


def window(t0, t1, total, fade=0.3):
    """keyTimes/values for an opacity pulse visible between t0 and t1 inside a loop of `total` sec"""
    pts = [(0, 0), (t0, 0), (t0 + fade, 1), (t1 - fade, 1), (t1, 0), (total, 0)]
    kt, vals = [], []
    for t, v in pts:
        t = min(max(t / total, 0), 1)
        if kt and t < kt[-1]:
            t = kt[-1]
        kt.append(t)
        vals.append(v)
    return ";".join(f"{k:.4f}" for k in kt), ";".join(str(v) for v in vals)


def win_anim(t0, t1, total, fade=0.3):
    kt, vals = window(t0, t1, total, fade)
    return A("opacity", vals, total, kt)


def txt(x, y, s, size=18, fill="#e5e7eb", weight=500, anchor="start", extra=""):
    return (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'text-anchor="{anchor}" {extra}>{escape(s)}</text>')


# --------------------------------------------------------------------------
# 1. HERO BANNER
# --------------------------------------------------------------------------
def hero():
    W, H = 1200, 420
    rnd = random.Random(3)
    defs = f'''
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#070b1a"/><stop offset=".55" stop-color="#14123a"/><stop offset="1" stop-color="#0b2540"/></linearGradient>
<linearGradient id="ac" gradientUnits="userSpaceOnUse" x1="60" y1="0" x2="330" y2="0" spreadMethod="reflect">
  <stop offset="0" stop-color="#60a5fa"/><stop offset=".5" stop-color="#c084fc"/><stop offset="1" stop-color="#22d3ee"/>
  <animateTransform attributeName="gradientTransform" type="translate" values="0 0;270 0;0 0" dur="6s" repeatCount="indefinite"/>
</linearGradient>
<radialGradient id="disc"><stop offset="0" stop-color="{PURPLE}"/><stop offset="1" stop-color="{BLUE}"/></radialGradient>
<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="45"/></filter>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>
<pattern id="dots" width="26" height="26" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.2" fill="#fff" opacity=".10"/></pattern>
<clipPath id="round"><rect width="{W}" height="{H}" rx="28"/></clipPath>
<clipPath id="type"><rect x="55" y="120" width="0" height="140">
  <animate attributeName="width" values="0;52;104;156;208;260;312;364;416;470;470" dur="1.8s" begin="0.4s" calcMode="discrete" fill="freeze"/></rect></clipPath>
'''
    b = [f'<g clip-path="url(#round)"><rect width="{W}" height="{H}" fill="url(#bg)"/>',
         f'<rect width="{W}" height="{H}" fill="url(#dots)"/>']
    # floating orbs
    for cx, cy, r, col, dx, dy, d in [(220, 330, 170, PURPLE, 80, -40, 11), (760, 80, 150, BLUE, -70, 60, 13), (1050, 340, 160, CYAN, -60, -50, 15)]:
        b.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}" opacity=".35" filter="url(#blur)">'
                 + T("translate", f"0 0;{dx} {dy};0 0", d) + "</circle>")
    # rising particles
    for _ in range(26):
        x, r, d = rnd.randint(10, W - 10), rnd.uniform(1.2, 3.2), rnd.uniform(8, 16)
        b.append(f'<circle cx="{x}" cy="{H + 10}" r="{r:.1f}" fill="#fff" opacity=".5">'
                 + A("cy", f"{H + 10};-10", f"{d:.1f}", begin=f"-{rnd.uniform(0, 12):.1f}")
                 + A("opacity", "0;.7;0", f"{d:.1f}", begin=f"-{rnd.uniform(0, 8):.1f}") + "</circle>")
    # badge pill
    b.append('<g opacity="0"><rect x="60" y="62" width="392" height="34" rx="17" fill="#ffffff" fill-opacity=".08" stroke="#ffffff" stroke-opacity=".2"/>'
             + txt(80, 85, "🎙️  AI SCREEN-DEMO STUDIO  ·  v1.4.0 stable", 15, "#cbd5e1", 600, extra='letter-spacing="1.2"')
             + A("opacity", "0;1", 0.8, once=True, begin=0.1) + "</g>")
    # typed title + caret
    b.append('<g clip-path="url(#type)">' + txt(60, 228, "Tutora AI", 96, "url(#ac)", 800, extra='textLength="470" lengthAdjust="spacingAndGlyphs"') + "</g>")
    b.append('<rect x="55" y="150" width="5" height="88" rx="2" fill="#22d3ee">'
             + A("x", "55;107;159;211;263;315;367;419;471;525", 1.8, begin=0.4, once=True, mode="discrete")
             + A("opacity", "1;0;1", 0.9) + "</rect>")
    # cycling taglines
    lines = ["Record  •  Narrate  •  Publish", "Offline neural voices. Zero cloud cost.", "Screen demos → polished tutorials in minutes"]
    for i, ln in enumerate(lines):
        kt, vals = window(2.2 + i * 4, 2.2 + i * 4 + 4, 12, 0.5)
        b.append(f'<g opacity="0">' + txt(62, 282, ln, 27, "#e2e8f0", 500)
                 + A("opacity", vals, 12, kt) + T("translate", "0 14;0 0;0 0;0 -10", 4, begin=2.2 + i * 4) .replace('repeatCount="indefinite"', 'repeatCount="indefinite"') + "</g>")
    # floating chips
    chips = [("🔒 100% Offline", 60, 160), ("🎙️ 57 Voices", 230, 150), ("🔍 Auto Zoom", 390, 150), ("⚡ BYOK Failover", 550, 175)]
    for i, (t, x, w) in enumerate(chips):
        b.append(f'<g opacity="0"><g>{T("translate", "0 0;0 -7;0 0", 3.2, begin=i * .5)}'
                 f'<rect x="{x}" y="320" width="{w}" height="40" rx="20" fill="#ffffff" fill-opacity=".07" stroke="url(#ac)" stroke-opacity=".8"/>'
                 + txt(x + w / 2, 346, t, 16, "#f1f5f9", 600, "middle") + "</g>"
                 + A("opacity", "0;1", 0.6, once=True, begin=1.8 + i * 0.25) + "</g>")
    # mic + radial equalizer
    cx, cy = 960, 205
    for i in range(3):
        b.append(f'<circle cx="{cx}" cy="{cy}" r="80" fill="none" stroke="{CYAN}" stroke-width="2" opacity="0">'
                 + A("r", "80;175", 3.6, begin=i * 1.2) + A("opacity", ".55;0", 3.6, begin=i * 1.2) + "</circle>")
    b.append(f'<g transform="translate({cx} {cy})">')
    for k in range(40):
        ang = k * 9
        hs = [rnd.randint(8, 40) for _ in range(5)]
        hs.append(hs[0])
        ys = ";".join(str(-(94 + h)) for h in hs)
        d = rnd.uniform(.9, 1.7)
        col = [CYAN, "#818cf8", "#c084fc"][k % 3]
        b.append(f'<g transform="rotate({ang})"><rect x="-3" y="-110" width="6" height="16" rx="3" fill="{col}" opacity=".9">'
                 + A("height", ";".join(map(str, hs)), f"{d:.2f}", begin=f"-{rnd.uniform(0, 2):.2f}")
                 + A("y", ys, f"{d:.2f}", begin=f"-{rnd.uniform(0, 2):.2f}") + "</rect></g>")
    b.append(f'<circle r="76" fill="url(#disc)">{A("r", "76;80;76", 2.4)}</circle>')
    b.append('<circle r="76" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="2"/>')
    b.append('<g stroke="#fff" stroke-width="5" stroke-linecap="round" fill="none"><rect x="-15" y="-38" width="30" height="52" rx="15" fill="#fff"/>'
             '<path d="M-28 -6 a28 28 0 0 0 56 0"/><path d="M0 22 V40"/><path d="M-15 40 H15"/></g>')
    b.append("</g></g>")
    save("hero-banner.svg", svg(W, H, "\n".join(b), defs))


# --------------------------------------------------------------------------
# 2. SECTION HEADERS (text animates: slide-in + shimmer + travelling glow)
# --------------------------------------------------------------------------
def header(name, emoji, title, sub):
    W, H = 1200, 100
    defs = f'''
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0f172a"/><stop offset="1" stop-color="#1e1b4b"/></linearGradient>
<linearGradient id="sh" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="360" y2="0" spreadMethod="reflect">
  <stop offset="0" stop-color="#93c5fd"/><stop offset=".5" stop-color="#e9d5ff"/><stop offset="1" stop-color="#67e8f9"/>
  <animateTransform attributeName="gradientTransform" type="translate" values="0 0;360 0" dur="3.5s" repeatCount="indefinite"/>
</linearGradient>
<linearGradient id="ln" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{BLUE}" stop-opacity="0"/><stop offset=".3" stop-color="{BLUE}"/><stop offset=".7" stop-color="{PURPLE}"/><stop offset="1" stop-color="{PURPLE}" stop-opacity="0"/></linearGradient>
<filter id="gl" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="4"/></filter>
'''
    body = f'''<rect width="{W}" height="{H}" rx="20" fill="url(#bg)"/>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="19" fill="none" stroke="#ffffff" stroke-opacity=".08"/>
<g>{T("translate", "0 0;0 -6;0 0", 1.8)}{txt(34, 60, emoji, 40)}</g>
<g opacity="0">{txt(100, 54, title, 38, "url(#sh)", 800)}{A("opacity", "0;1", .7, once=True, begin=.1)}{T("translate", "-40 0;0 0", .7, once=True, begin=.1)}</g>
<g opacity="0">{txt(102, 76, sub, 15, "#94a3b8", 500)}{A("opacity", "0;1", .8, once=True, begin=.5)}</g>
<rect x="34" y="86" width="{W-68}" height="3" rx="1.5" fill="url(#ln)" opacity=".8"/>
<circle cy="87.5" r="5" fill="#fff" filter="url(#gl)" cx="34">{A("cx", f"34;{W-34}", 4.5)}{A("opacity", "0;1;1;0", 4.5, "0;.1;.9;1")}</circle>
<circle cy="87.5" r="2.5" fill="#fff" cx="34">{A("cx", f"34;{W-34}", 4.5)}{A("opacity", "0;1;1;0", 4.5, "0;.1;.9;1")}</circle>'''
    save(f"h-{name}.svg", svg(W, H, body, defs))


# --------------------------------------------------------------------------
# 3. PIPELINE (record -> script -> voice -> export)
# --------------------------------------------------------------------------
def pipeline():
    W, H = 1200, 270
    defs = f'''<linearGradient id="ac" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BLUE}"/><stop offset="1" stop-color="{PURPLE}"/></linearGradient>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b1020"/><stop offset="1" stop-color="#18163b"/></linearGradient>
<filter id="gl" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="6"/></filter>'''
    xs = [150, 450, 750, 1050]
    nodes = [("🎥", "Record", "Screen, cam & cursor"), ("🧠", "AI Script", "Narration from timeline"),
             ("🎙️", "Offline Voice", "Kokoro + Resona TTS"), ("🚀", "Export", "Polished video, ready")]
    b = [f'<rect width="{W}" height="{H}" rx="24" fill="url(#bg)"/>',
         f'<path d="M150 105 H1050" stroke="#334155" stroke-width="4" stroke-linecap="round"/>',
         f'<path d="M150 105 H1050" stroke="url(#ac)" stroke-width="4" stroke-dasharray="10 12" stroke-linecap="round">{A("stroke-dashoffset", "0;-44", 1.2)}</path>']
    for i, (x, (ic, t, s)) in enumerate(zip(xs, nodes)):
        b.append(f'<circle cx="{x}" cy="105" r="46" fill="none" stroke="{CYAN}" stroke-width="3" opacity="0">'
                 + A("r", "46;70;70", 6, "0;.25;1", begin=2 * i) + A("opacity", ".8;0;0", 6, "0;.25;1", begin=2 * i) + "</circle>")
        b.append(f'<g>{T("translate", "0 0;0 -5;0 0", 3, begin=i * .4)}<circle cx="{x}" cy="105" r="46" fill="url(#ac)"/>'
                 f'<circle cx="{x}" cy="105" r="46" fill="none" stroke="#fff" stroke-opacity=".3" stroke-width="2"/>'
                 + txt(x, 120, ic, 40, anchor="middle") + "</g>")
        b.append(txt(x, 192, f"{i + 1}. {t}", 22, "#f1f5f9", 700, "middle"))
        b.append(txt(x, 218, s, 15, "#94a3b8", 500, "middle"))
    b.append(f'<circle r="9" fill="#fff" filter="url(#gl)"><animateMotion dur="6s" repeatCount="indefinite" path="M150 105 H1050"/></circle>')
    b.append(f'<circle r="5" fill="#fff"><animateMotion dur="6s" repeatCount="indefinite" path="M150 105 H1050"/></circle>')
    save("pipeline.svg", svg(W, H, "\n".join(b), defs))


# --------------------------------------------------------------------------
# 4. FEATURE CARDS (staggered entrance + float + shine + rotating border)
# --------------------------------------------------------------------------
def cards():
    W, H = 1200, 690
    cw, ch, gap = 370, 200, 25
    feats = [("🎙️", "Offline Neural Voice", ["Kokoro v1.0 + Resona engine,", "57 voices, zero cloud API cost"]),
             ("🧠", "AI Script Generation", ["Step-by-step narration written", "straight from your capture timeline"]),
             ("🔍", "Auto Zoom & Motion", ["Dynamic zooms on a motion-driven", "multi-track timeline"]),
             ("🎯", "Cursor Spring Physics", ["Smoothed paths, click ripples,", "shockwaves, up to 4.0× size"]),
             ("📹", "Webcam Bubble", ["Zoom-reactive facecam overlay in", "circle, pill or custom radius"]),
             ("💬", "Animated Captions", ["Fade, Slide, Bounce & Pop with", "custom typography tokens"]),
             ("🎬", "Keynote Intro / Outro", ["Fast 3s · Standard 5.5s ·", "Cinematic 8s · 5 layouts"]),
             ("⚡", "Universal AI Hub", ["BYOK: Gemini, Groq, OpenRouter,", "OpenAI & Claude with failover"]),
             ("📁", "Open .tutora Format", ["Opens .recordly & .guidely too.", "Everything stored as plain JSON"])]
    defs = f'''<linearGradient id="cg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0f172a"/><stop offset="1" stop-color="#1e1b4b"/></linearGradient>
<linearGradient id="bd" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BLUE}"/><stop offset=".5" stop-color="{PURPLE}"/><stop offset="1" stop-color="{CYAN}"/>
  <animateTransform attributeName="gradientTransform" type="rotate" values="0 .5 .5;360 .5 .5" dur="8s" repeatCount="indefinite"/></linearGradient>
<linearGradient id="tt" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#e2e8f0"/><stop offset="1" stop-color="#a5b4fc"/></linearGradient>
<clipPath id="cc"><rect width="{cw}" height="{ch}" rx="20"/></clipPath>'''
    b = []
    for i, (ic, t, ls) in enumerate(feats):
        x = 20 + (i % 3) * (cw + gap)
        y = 20 + (i // 3) * (ch + gap)
        g = [f'<g transform="translate({x} {y})"><g opacity="0">{A("opacity", "0;1", .7, once=True, begin=i * .15)}'
             f'{T("translate", "0 34;0 0", .7, once=True, begin=i * .15)}',
             f'<g>{T("translate", f"0 0;0 -6;0 0", 4 + (i % 3), begin=i * .3)}',
             f'<rect width="{cw}" height="{ch}" rx="20" fill="url(#cg)" stroke="url(#bd)" stroke-width="2"/>',
             f'<g clip-path="url(#cc)"><rect y="-20" width="70" height="{ch + 40}" fill="#fff" opacity=".07" transform="skewX(-20)">{A("x", "-160;520", 5, begin=i * .7)}</rect></g>',
             f'<circle cx="62" cy="64" r="34" fill="{[BLUE, PURPLE, CYAN][i % 3]}" opacity=".25">{A("r", "34;40;34", 2.5, begin=i * .2)}</circle>',
             txt(62, 78, ic, 36, anchor="middle"),
             txt(114, 58, t, 22, "url(#tt)", 800),
             txt(114, 82, f"0{i + 1}", 13, "#64748b", 700, extra='letter-spacing="2"'),
             txt(34, 134, ls[0], 17, "#cbd5e1", 500), txt(34, 160, ls[1], 17, "#cbd5e1", 500),
             '</g></g></g>']
        b.append("".join(g))
    save("feature-cards.svg", svg(W, H, "\n".join(b), defs))


# --------------------------------------------------------------------------
# 5. CURSOR PHYSICS demo (raw jitter vs spring smooth)
# --------------------------------------------------------------------------
def cursor():
    W, H = 1000, 340
    rnd = random.Random(11)
    p0, p1 = (50, 205), (385, 95)
    pts = []
    n = 26
    for k in range(n + 1):
        t = k / n
        x = p0[0] + (p1[0] - p0[0]) * t
        y = p0[1] + (p1[1] - p0[1]) * t - math.sin(t * math.pi) * 70
        if 0 < k < n:
            x += rnd.uniform(-11, 11)
            y += rnd.uniform(-11, 11)
        pts.append((x, y))
    raw = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    smooth = f"M{p0[0]} {p0[1]} Q {(p0[0] + p1[0]) / 2:.0f} {(p0[1] + p1[1]) / 2 - 140:.0f} {p1[0]} {p1[1]}"
    D = 5
    defs = f'''<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b1020"/><stop offset="1" stop-color="#18163b"/></linearGradient>
<linearGradient id="pn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#111827"/><stop offset="1" stop-color="#0f172a"/></linearGradient>'''
    cur = '<path d="M0 0 L0 17 L4.5 13 L8 20 L10.5 19 L7 12 L13 12 Z" fill="#fff" stroke="#0f172a" stroke-width="1.3" stroke-linejoin="round"/>'

    def panel(px, label, color, path, lin):
        mode = "" if lin else 'calcMode="spline" keySplines="0.45 0 0.2 1;0 0 1 1"'
        kp = "0;1;1"
        s = [f'<g transform="translate({px} 60)"><rect width="460" height="250" rx="16" fill="url(#pn)" stroke="#ffffff" stroke-opacity=".1"/>',
             f'<circle cx="22" cy="20" r="5" fill="#ef4444"/><circle cx="40" cy="20" r="5" fill="#f59e0b"/><circle cx="58" cy="20" r="5" fill="#22c55e"/>',
             txt(230, 25, label, 15, color, 700, "middle"),
             # fake button target
             f'<rect x="325" y="72" width="120" height="46" rx="12" fill="{BLUE}" opacity=".9"/>',
             f'<rect x="325" y="72" width="120" height="46" rx="12" fill="#fff" opacity="0">{A("opacity", "0;0;.5;0;0", D, "0;.55;.6;.75;1")}</rect>',
             txt(385, 101, "Export ▸", 16, "#fff", 700, "middle"),
             # trail
             f'<path d="{path}" pathLength="1" fill="none" stroke="{color}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="1 1" stroke-dashoffset="1">'
             + A("stroke-dashoffset", "1;0;0", D, "0;.55;1") + A("opacity", "1;1;0;0", D, "0;.88;.98;1") + "</path>"]
        if lin:
            s.append(f'<g>{cur}<animateMotion dur="{D}s" repeatCount="indefinite" keyPoints="{kp}" keyTimes="0;.55;1" calcMode="linear" path="{path}"/></g>')
        else:
            s.append(f'<g>{cur}<animateMotion dur="{D}s" repeatCount="indefinite" keyPoints="{kp}" keyTimes="0;.55;1" {mode} path="{path}"/></g>')
        return "".join(s)

    b = [f'<rect width="{W}" height="{H}" rx="24" fill="url(#bg)"/>']
    b.append(panel(20, "✖  Raw mouse input — jittery", RED, raw, True))
    b.append(txt(70, 235, "hand shake, hard to follow", 14, "#64748b", 500))
    b.append("</g>")
    b.append(panel(520, "✔  Tutora spring smoothing", GREEN, smooth, False))
    # shockwave rings on smooth panel
    for i in range(3):
        b.append(f'<circle cx="{p1[0]}" cy="{p1[1]}" r="0" fill="none" stroke="{GREEN}" stroke-width="3" opacity="0">'
                 + A("r", "0;0;46;46", D, f"0;{.55 + i * .05};{.9 + i * .02};1")
                 + A("opacity", "0;.9;0;0", D, f"0;{.55 + i * .05};{.9 + i * .02};1") + "</circle>")
    b.append(txt(70, 235, "spring physics + click shockwave", 14, "#64748b", 500))
    b.append("</g>")
    save("cursor-physics.svg", svg(W, H, "\n".join(b), defs))


# --------------------------------------------------------------------------
# 6. VOICE ENGINE
# --------------------------------------------------------------------------
def voice():
    W, H = 1000, 320
    rnd = random.Random(5)
    defs = f'''<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#06201d"/><stop offset="1" stop-color="#14123a"/></linearGradient>
<linearGradient id="eq" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{GREEN}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>'''
    b = [f'<rect width="{W}" height="{H}" rx="24" fill="url(#bg)"/>',
         txt(40, 52, "🎙️ Embedded Neural Voice Studio", 24, "#ecfeff", 800),
         txt(40, 78, "Kokoro v1.0 + Resona · runs 100% on your machine", 15, "#94a3b8", 500)]
    langs = ["American English", "British English", "Hindi", "Natural Hinglish"]
    total = 8
    for i, l in enumerate(langs):
        y = 100 + i * 44
        b.append(f'<rect x="40" y="{y}" width="400" height="36" rx="10" fill="#fff" fill-opacity=".05"/>')
        b.append(f'<g opacity="0"><rect x="40" y="{y}" width="400" height="36" rx="10" fill="{GREEN}" fill-opacity=".28" stroke="{GREEN}"/>'
                 f'<rect x="40" y="{y}" width="6" height="36" rx="3" fill="{GREEN}"/>{win_anim(i * 2, i * 2 + 2, total, .25)}</g>')
        b.append(f'<circle cx="68" cy="{y + 18}" r="6" fill="{[BLUE, PINK, "#f59e0b", PURPLE][i]}"/>')
        b.append(txt(88, y + 24, l, 17, "#e2e8f0", 600))
        b.append(f'<g opacity="0">{txt(420, y + 24, "▶ speaking", 13, GREEN, 700, "end")}{win_anim(i * 2, i * 2 + 2, total, .25)}</g>')
    # equalizer
    for k in range(38):
        x = 500 + k * 12.5
        hs = [rnd.randint(14, 120) for _ in range(6)]
        hs.append(hs[0])
        ys = ";".join(f"{170 - h / 2:.0f}" for h in hs)
        d = rnd.uniform(.7, 1.6)
        b.append(f'<rect x="{x:.1f}" y="110" width="7" height="60" rx="3.5" fill="url(#eq)">'
                 + A("height", ";".join(map(str, hs)), f"{d:.2f}", begin=f"-{rnd.uniform(0, 2):.2f}")
                 + A("y", ys, f"{d:.2f}", begin=f"-{rnd.uniform(0, 2):.2f}") + "</rect>")
    pills = [("57 voices", 40, 150), ("0 cloud API cost", 210, 190), ("CUDA → CPU fallback", 420, 230)]
    for i, (t, x, w) in enumerate(pills):
        b.append(f'<g>{T("translate", "0 0;0 -4;0 0", 3, begin=i * .6)}<rect x="{x}" y="268" width="{w}" height="34" rx="17" fill="none" stroke="{CYAN}" stroke-opacity=".7"/>'
                 + txt(x + w / 2, 291, t, 15, "#a5f3fc", 700, "middle") + "</g>")
    save("voice-engine.svg", svg(W, H, "\n".join(b), defs))


# --------------------------------------------------------------------------
# 7. FAILOVER
# --------------------------------------------------------------------------
def failover():
    W, H, D = 1060, 300, 12
    defs = f'''<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b1020"/><stop offset="1" stop-color="#1e1b4b"/></linearGradient>
<filter id="gl" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="5"/></filter>'''
    provs = ["Gemini", "Groq", "OpenRouter", "OpenAI", "Claude"]
    px = [290, 460, 630, 800, 970]
    b = [f'<rect width="{W}" height="{H}" rx="24" fill="url(#bg)"/>',
         txt(40, 46, "⚡ Zero-failure failover", 24, "#f1f5f9", 800),
         txt(40, 70, "Rate limit (HTTP 429) or quota hit? Tutora jumps to your next provider mid-generation.", 14, "#94a3b8")]
    b.append('<path d="M130 150 H1000" stroke="#334155" stroke-width="3" stroke-dasharray="8 10">' + A("stroke-dashoffset", "0;-36", 1.2) + "</path>")
    b.append(f'<circle cx="100" cy="150" r="34" fill="{BLUE}"/>' + txt(100, 162, "🎙️", 30, anchor="middle") + txt(100, 206, "Tutora AI", 14, "#cbd5e1", 700, "middle"))
    for i, (p, x) in enumerate(zip(provs, px)):
        dim = ' opacity=".55"' if i > 2 else ""
        b.append(f'<g{dim}><rect x="{x - 70}" y="115" width="140" height="70" rx="14" fill="#0f172a" stroke="#475569" stroke-width="2"/>'
                 + txt(x, 156, p, 18, "#e2e8f0", 700, "middle") + "</g>")
    # states
    states = [(0, 0.8, 3.0, RED), (1, 3.2, 5.2, RED), (2, 5.6, 10.0, GREEN)]
    for i, t0, t1, col in states:
        x = px[i]
        b.append(f'<g opacity="0"><rect x="{x - 70}" y="115" width="140" height="70" rx="14" fill="{col}" fill-opacity=".18" stroke="{col}" stroke-width="3"/>{win_anim(t0, t1, D, .25)}</g>')
    b.append(f'<g opacity="0">{txt(px[0], 112 - 8, "⛔ 429", 17, RED, 800, "middle")}{win_anim(.8, 3.0, D)}</g>')
    b.append(f'<g opacity="0">{txt(px[1], 104, "⛔ quota", 17, RED, 800, "middle")}{win_anim(3.2, 5.2, D)}</g>')
    b.append(f'<g opacity="0">{txt(px[2], 104, "✓ 200 OK", 17, GREEN, 800, "middle")}{win_anim(5.6, 10.0, D)}</g>')
    # packet
    tms = [0, .8, 2.4, 3.2, 4.8, 5.6, 9.6, 10.6, 12]
    xs = [100, 290, 290, 460, 460, 630, 630, 100, 100]
    kt = ";".join(f"{t / D:.4f}" for t in tms)
    for r, op, fl in [(11, 1, ""), (18, .5, ' filter="url(#gl)"')]:
        b.append(f'<circle cy="150" r="{r}" fill="#fff" opacity="{op}"{fl} cx="100">{A("cx", ";".join(map(str, xs)), D, kt)}</circle>')
    caps = [(.8, 3.0, "Gemini → HTTP 429 rate limit …", RED), (3.2, 5.2, "Groq → quota exceeded, switching …", RED),
            (5.6, 10.0, "OpenRouter → ✓ script generation continues, no interruption", GREEN)]
    for t0, t1, c, col in caps:
        b.append(f'<g opacity="0">{txt(W / 2, 256, c, 19, col, 700, "middle")}{win_anim(t0, t1, D, .25)}</g>')
    save("failover.svg", svg(W, H, "\n".join(b), defs))


# --------------------------------------------------------------------------
# 8. DIVIDER
# --------------------------------------------------------------------------
def divider():
    W, H = 1200, 40
    defs = f'''<linearGradient id="ln" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{BLUE}" stop-opacity="0"/><stop offset=".5" stop-color="{PURPLE}"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></linearGradient>
<filter id="gl" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="4"/></filter>'''
    b = [f'<rect x="40" y="19" width="{W - 80}" height="2" rx="1" fill="url(#ln)"/>']
    for i, x in enumerate([300, 600, 900]):
        b.append(f'<g transform="translate({x} 20) rotate(45)"><rect x="-6" y="-6" width="12" height="12" fill="{[BLUE, PURPLE, CYAN][i]}">'
                 + A("opacity", ".3;1;.3", 2.4, begin=i * .6) + "</rect></g>")
    b.append(f'<circle cy="20" r="6" fill="#fff" filter="url(#gl)" cx="40">{A("cx", f"40;{W - 40}", 5)}</circle>')
    save("divider.svg", svg(W, H, "\n".join(b), defs))


# --------------------------------------------------------------------------
# 9. SLIDESHOW (screenshots embedded as base64 so it works inside <img>)
# --------------------------------------------------------------------------
def load_shot(fname):
    path = os.path.join(SHOTS, fname)
    if not os.path.exists(path):
        return None
    try:
        from PIL import Image
        im = Image.open(path).convert("RGB")
        tw, th = 1400, 788
        r = max(tw / im.width, th / im.height)
        im = im.resize((int(im.width * r) + 1, int(im.height * r) + 1))
        l, t = (im.width - tw) // 2, (im.height - th) // 2
        im = im.crop((l, t, l + tw, t + th))
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=74, optimize=True)
        return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    except ImportError:
        mime = "image/png" if fname.lower().endswith("png") else "image/jpeg"
        print("  ! Pillow missing: embedding raw image (file will be large). pip install pillow")
        with open(path, "rb") as f:
            return f"data:{mime};base64," + base64.b64encode(f.read()).decode()


def slideshow():
    W, H = 1200, 880
    N, d = len(SLIDES), SLIDE_SECONDS
    total = N * d
    FX, FY, FW, FH = 40, 150, 1120, 630  # image area
    defs = f'''<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#070b1a"/><stop offset=".6" stop-color="#14123a"/><stop offset="1" stop-color="#0b2540"/></linearGradient>
<linearGradient id="ac" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="400" y2="0" spreadMethod="reflect"><stop offset="0" stop-color="#93c5fd"/><stop offset=".5" stop-color="#e9d5ff"/><stop offset="1" stop-color="#67e8f9"/>
<animateTransform attributeName="gradientTransform" type="translate" values="0 0;400 0" dur="4s" repeatCount="indefinite"/></linearGradient>
<linearGradient id="pg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{BLUE}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>
<clipPath id="imgclip"><rect x="{FX}" y="{FY}" width="{FW}" height="{FH}"/></clipPath>
<filter id="gl" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="18"/></filter>'''
    b = [f'<rect width="{W}" height="{H}" rx="28" fill="url(#bg)"/>',
         f'<circle cx="150" cy="60" r="130" fill="{PURPLE}" opacity=".3" filter="url(#gl)">{T("translate", "0 0;120 20;0 0", 12)}</circle>',
         f'<circle cx="1050" cy="800" r="150" fill="{CYAN}" opacity=".22" filter="url(#gl)">{T("translate", "0 0;-100 -30;0 0", 14)}</circle>']
    # titles
    for i, (title, sub, _) in enumerate(SLIDES):
        t0, t1 = i * d, (i + 1) * d
        kt, vals = window(t0, t1, total, .6)
        tk = f"0;{t0 / total:.4f};{min((t0 + .7) / total, 1):.4f};1"
        b.append(f'<g opacity="0">{txt(FX, 66, title, 38, "url(#ac)", 800)}{txt(FX + 2, 102, sub, 18, "#94a3b8", 500)}'
                 + A("opacity", vals, total, kt) + T("translate", "-40 0;-40 0;0 0;0 0", total, tk) + "</g>")
        b.append(f'<g opacity="0">{txt(W - FX, 66, f"{i + 1:02d} / {N:02d}", 22, "#64748b", 700, "end")}{A("opacity", vals, total, kt)}</g>')
    # window chrome
    b.append(f'<rect x="{FX}" y="{FY - 28}" width="{FW}" height="{FH + 28}" rx="16" fill="#0f172a" stroke="#ffffff" stroke-opacity=".12"/>')
    for k, c in enumerate(["#ef4444", "#f59e0b", "#22c55e"]):
        b.append(f'<circle cx="{FX + 22 + k * 20}" cy="{FY - 14}" r="5.5" fill="{c}"/>')
    # slides
    pal = [(BLUE, PURPLE), (PURPLE, PINK), (CYAN, BLUE), (GREEN, CYAN), (PINK, PURPLE), (BLUE, CYAN), (PURPLE, BLUE)]
    b.append('<g clip-path="url(#imgclip)">')
    for i, (title, sub, fname) in enumerate(SLIDES):
        t0, t1 = i * d, (i + 1) * d
        kt, vals = window(t0, t1, total, .6)
        data = load_shot(fname)
        kk = f"0;{t0 / total:.4f};{t1 / total:.4f};1"
        g = [f'<g opacity="0">']
        if data:
            g.append(f'<image x="{FX}" y="{FY}" width="{FW}" height="{FH}" preserveAspectRatio="xMidYMid slice" href="{data}">'
                     + A("x", f"{FX};{FX};{FX - 28};{FX - 28}", total, kk) + A("y", f"{FY};{FY};{FY - 16};{FY - 16}", total, kk)
                     + A("width", f"{FW};{FW};{FW + 56};{FW + 56}", total, kk) + A("height", f"{FH};{FH};{FH + 32};{FH + 32}", total, kk) + "</image>")
        else:
            c1, c2 = pal[i % len(pal)]
            g.append(f'<defs><linearGradient id="ph{i}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient></defs>'
                     f'<rect x="{FX}" y="{FY}" width="{FW}" height="{FH}" fill="url(#ph{i})" opacity=".55"/>'
                     + txt(W / 2, FY + FH / 2 - 6, title, 44, "#fff", 800, "middle")
                     + txt(W / 2, FY + FH / 2 + 34, f"add assets/screenshots/{fname} and re-run the build script", 20, "#e2e8f0", 500, "middle"))
        g.append(A("opacity", vals, total, kt) + "</g>")
        b.append("".join(g))
    b.append("</g>")
    # progress + dots
    b.append(f'<rect x="{FX}" y="{FY + FH + 22}" width="{FW}" height="5" rx="2.5" fill="#fff" fill-opacity=".1"/>')
    b.append(f'<rect x="{FX}" y="{FY + FH + 22}" width="0" height="5" rx="2.5" fill="url(#pg)">{A("width", f"0;{FW}", d, begin=0)}</rect>')
    gap = 34
    sx = W / 2 - (N - 1) * gap / 2
    for i in range(N):
        x = sx + i * gap
        b.append(f'<circle cx="{x}" cy="{FY + FH + 58}" r="5" fill="#475569"/>')
        b.append(f'<circle cx="{x}" cy="{FY + FH + 58}" r="8" fill="{CYAN}" opacity="0">{win_anim(i * d, (i + 1) * d, total, .3)}</circle>')
    save("slideshow.svg", svg(W, H, "\n".join(b), defs))


# --------------------------------------------------------------------------
if __name__ == "__main__":
    print(f"Building animated assets -> {OUT}")
    hero()
    for n, e, t, s in [
        ("what", "💡", "What is Tutora AI?", "One desktop studio for capture, scripts, voices & video"),
        ("download", "📥", "Download & Releases", "Grab the signed installer for your platform"),
        ("tour", "🌟", "Visual Feature Tour", "Seven screens, one auto-playing slideshow"),
        ("features", "🧩", "Everything Inside", "The full toolbox at a glance"),
        ("quickstart", "🚀", "Quick Start", "From first recording to finished tutorial in 5 steps"),
        ("specs", "💻", "System Requirements", "Runs on modest hardware, flies with a GPU"),
        ("format", "📁", "Project Format", "Open, portable, backward compatible"),
        ("community", "🤝", "Community & Support", "Bugs, ideas and stars are all welcome"),
        ("license", "📜", "License", "Free software under AGPL-3.0"),
    ]:
        header(n, e, t, s)
    pipeline()
    cards()
    cursor()
    voice()
    failover()
    divider()
    slideshow()
    print("Done ✔")
