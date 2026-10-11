#!/usr/bin/env python3
"""Render the README visuals in assets/ — Revenue Puzzles palette, numbers from the example home.

Text is shaped with HarfBuzz and drawn as vector paths, so every SVG renders the same on
GitHub (light and dark), in a browser and offline: no web fonts to load or block. The funnel
numbers are read from examples/gtm-home/motions/*/RESULTS.md, so the chart can't drift from
the example it illustrates.

Requires: pip install fonttools uharfbuzz
Fonts (SIL Open Font License: Bricolage Grotesque, Inter, JetBrains Mono) are downloaded once
from github.com/google/fonts into .cache/fonts/.

Usage:  python scripts/render_assets.py
Social preview PNG: open assets/social.svg in a browser at 1280×640 and screenshot it.
"""
import html
import re
import urllib.request
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
CACHE = ROOT / ".cache" / "fonts"
MOTIONS = ROOT / "examples" / "gtm-home" / "motions"
GOOGLE_FONTS = "https://raw.githubusercontent.com/google/fonts/main/ofl/"

FONTS = {
    "display": ("bricolagegrotesque/BricolageGrotesque[opsz,wdth,wght].ttf", {"wght": 780, "opsz": 96, "wdth": 100}),
    "sans": ("inter/Inter[opsz,wght].ttf", {"wght": 400, "opsz": 14}),
    "semi": ("inter/Inter[opsz,wght].ttf", {"wght": 600, "opsz": 14}),
    "mono": ("jetbrainsmono/JetBrainsMono[wght].ttf", {"wght": 500}),
}

THEMES = {
    "light": {
        "surface": "#FBF9F4", "panel": "#FFFFFF", "row": "#F6F3EC", "border": "#E7E2D8",
        "ink": "#151518", "body": "#4B4B52", "muted": "#6E6E76", "chip": "#F1EDE4",
        "orange": "#FF5A1F", "mark": "#E8500F", "gray_mark": "#8A857B",
        "tint": "#FFE8DD", "tint_text": "#B93D0C", "solid": "#151518", "solid_text": "#FFFFFF",
        "peach": "#FBE9E4", "mint": "#E4F1EC", "sand": "#F5EEDF", "grid": "#E9E4DA",
    },
    "dark": {
        "surface": "#151518", "panel": "#1C1C20", "row": "#222227", "border": "#2E2E34",
        "ink": "#F5F3EE", "body": "#C8C8CE", "muted": "#9A9AA2", "chip": "#26262C",
        "orange": "#FF5A1F", "mark": "#FF6A33", "gray_mark": "#8E8A84",
        "tint": "#3A1E12", "tint_text": "#FF9466", "solid": "#F5F3EE", "solid_text": "#151518",
        "peach": "#2B1E1A", "mint": "#17231E", "sand": "#24201A", "grid": "#2A2A30",
    },
}

ANIMATION = """
.flow{stroke-dasharray:4 8;animation:flow 1.1s linear infinite}
@keyframes flow{to{stroke-dashoffset:-12}}
.pulse{animation:pulse 1.6s ease-in-out infinite}
@keyframes pulse{50%{opacity:.2}}
@media (prefers-reduced-motion:reduce){.flow,.pulse{animation:none}}
"""


# ── fonts and text ──────────────────────────────────────────────────────────


class Font:
    def __init__(self, key: str, path: Path):
        self.key = key
        data = path.read_bytes()
        self.hb = hb.Font(hb.Face(data))
        self.tt = TTFont(path)
        self.upem = self.tt["head"].unitsPerEm
        self.glyphs = self.tt.getGlyphSet()
        self.order = self.tt.getGlyphOrder()

    def shape(self, text: str) -> list:
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.hb, buf, {"kern": True, "liga": True})
        return [(info.codepoint, pos.x_advance, pos.x_offset, pos.y_offset)
                for info, pos in zip(buf.glyph_infos, buf.glyph_positions)]

    def outline(self, gid: int) -> str:
        pen = SVGPathPen(self.glyphs)
        self.glyphs[self.order[gid]].draw(pen)
        return pen.getCommands()


def load_fonts() -> dict:
    CACHE.mkdir(parents=True, exist_ok=True)
    fonts = {}
    for key, (source, axes) in FONTS.items():
        static = CACHE / f"{key}.ttf"
        if not static.exists():
            variable = CACHE / Path(source).name
            if not variable.exists():
                url = GOOGLE_FONTS + source.replace("[", "%5B").replace("]", "%5D")
                print(f"downloading {url}")
                urllib.request.urlretrieve(url, variable)
            instancer.instantiateVariableFont(TTFont(variable), axes).save(static)
        fonts[key] = Font(key, static)
    return fonts


F = {}
PREFIX = {"display": "d", "sans": "s", "semi": "b", "mono": "m"}


def num(value: float) -> str:
    text = f"{value:.1f}".rstrip("0").rstrip(".")
    return "0" if text == "-0" else text


def measure(text: str, font: str = "sans", size: float = 16, ls: float = 0) -> float:
    shaped = F[font].shape(text)
    return sum(adv for _, adv, _, _ in shaped) * size / F[font].upem + ls * max(len(shaped) - 1, 0)


def wrap(text: str, maxw: float, font: str = "sans", size: float = 16, ls: float = 0) -> list:
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if line and measure(trial, font, size, ls) > maxw:
            lines.append(line)
            line = word
        else:
            line = trial
    return lines + [line] if line else lines


# ── canvas ──────────────────────────────────────────────────────────────────


class Canvas:
    def __init__(self, width: int, height: int, title: str, desc: str):
        self.w, self.h = width, height
        self.title, self.desc = title, desc
        self.body = []
        self.defs = {}
        self.extra_defs = []

    def add(self, svg: str) -> None:
        self.body.append(svg)

    def text(self, x, y, s, font="sans", size=16, fill="#000", anchor="start", ls=0.0, cls="") -> float:
        """Draw text as glyph paths; y is the baseline. Returns the advance width."""
        f = F[font]
        k = size / f.upem
        shaped = f.shape(s)
        width = measure(s, font, size, ls)
        x0 = x - width if anchor == "end" else x - width / 2 if anchor == "middle" else x
        pen, uses = 0.0, []
        for gid, adv, dx, dy in shaped:
            ref = f"{PREFIX[font]}{gid}"
            if ref not in self.defs:
                self.defs[ref] = f.outline(gid)
            if self.defs[ref]:
                uses.append(f'<use href="#{ref}" x="{num(pen + dx)}"' + (f' y="{num(dy)}"' if dy else "") + "/>")
            pen += adv + ls / k
        klass = f' class="{cls}"' if cls else ""
        self.add(f'<g{klass} fill="{fill}" transform="translate({num(x0)} {num(y)}) scale({k:.5f} {-k:.5f})">{"".join(uses)}</g>')
        return width

    def lines(self, x, y, lines, lead, **kw) -> float:
        for i, line in enumerate(lines):
            self.text(x, y + i * lead, line, **kw)
        return y + (len(lines) - 1) * lead

    def rect(self, x, y, w, h, r=0, fill="none", stroke=None, sw=1, extra=""):
        s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        self.add(f'<rect x="{num(x)}" y="{num(y)}" width="{num(w)}" height="{num(h)}" rx="{num(r)}" fill="{fill}"{s}{extra}/>')

    def line(self, x1, y1, x2, y2, stroke, sw=1, extra=""):
        self.add(f'<line x1="{num(x1)}" y1="{num(y1)}" x2="{num(x2)}" y2="{num(y2)}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round"{extra}/>')

    def circle(self, cx, cy, r, fill, extra=""):
        self.add(f'<circle cx="{num(cx)}" cy="{num(cy)}" r="{num(r)}" fill="{fill}"{extra}/>')

    def svg(self) -> str:
        glyphs = "".join(f'<path id="{ref}" d="{d}"/>' for ref, d in self.defs.items() if d)
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" '
            f'role="img" aria-labelledby="t d">'
            f"<title id=\"t\">{html.escape(self.title)}</title><desc id=\"d\">{html.escape(self.desc)}</desc>"
            f"<style>{ANIMATION}</style><defs>{glyphs}{''.join(self.extra_defs)}</defs>"
            + "".join(self.body)
            + "</svg>\n"
        )


# ── shared pieces ───────────────────────────────────────────────────────────


def frame(c: Canvas, T: dict, fill=None):
    c.rect(1, 1, c.w - 2, c.h - 2, 24, fill or T["surface"], T["border"], 1.5)


def eyebrow(c: Canvas, T: dict, x, y, label, color=None):
    c.line(x, y - 4.5, x + 22, y - 4.5, T["orange"], 2)
    c.text(x + 34, y, label.upper(), "mono", 13.5, color or T["muted"], ls=1.6)


def chip(c: Canvas, T: dict, x, y, label, kind="plain", size=13, h=28):
    pad = 11
    w = measure(label, "mono", size) + 2 * pad
    fills = {
        "plain": (T["panel"], T["body"], T["border"]),
        "row": (T["chip"], T["body"], None),
        "solid": (T["solid"], T["solid_text"], None),
        "orange": (T["tint"], T["tint_text"], None),
        "accent": (T["orange"], "#FFFFFF", None),
    }
    bg, fg, stroke = fills[kind]
    c.rect(x, y, w, h, h / 2, bg, stroke, 1)
    c.text(x + pad, y + h / 2 + size * 0.36, label, "mono", size, fg)
    return w


def flow_chips(c, T, x, y, maxw, labels, kind="plain", gap=7, row_gap=8, size=13, h=28) -> float:
    """Lay chips out left to right, wrapping at maxw. A label may be (text, kind). Returns the height used."""
    cx, cy = x, y
    for item in labels:
        label, style = item if isinstance(item, tuple) else (item, kind)
        w = measure(label, "mono", size) + 22
        if cx > x and cx + w > x + maxw:
            cx, cy = x, cy + h + row_gap
        chip(c, T, cx, cy, label, style, size, h)
        cx += w + gap
    return cy + h - y


def logo(c: Canvas, T: dict, x, y, s=13, gap=3.5, dark_bg=False):
    ink = "#F5F3EE" if dark_bg else T["ink"]
    for i, (dx, dy) in enumerate([(0, 0), (1, 0), (0, 1), (1, 1)]):
        c.rect(x + dx * (s + gap), y + dy * (s + gap), s, s, s * 0.3, T["orange"] if i == 3 else ink)


def wordmark(c: Canvas, T: dict, x, baseline, size=19, dark_bg=False) -> float:
    ink = "#F5F3EE" if dark_bg else T["ink"]
    w = c.text(x, baseline, "Revenu", "display", size, ink, ls=-0.2)
    w += c.text(x + w, baseline, "e", "display", size, T["orange"])
    w += c.text(x + w, baseline, " Puzzles", "display", size, ink, ls=-0.2)
    return w


def arrow_defs(c: Canvas, T: dict):
    c.extra_defs.append(
        f'<marker id="ah" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        f'<path d="M1 1.5 L8 5 L1 8.5" fill="none" stroke="{T["orange"]}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></marker>'
    )


def connector(c: Canvas, T: dict, d: str, label=None, lx=0, ly=0):
    c.add(f'<path d="{d}" fill="none" stroke="{T["orange"]}" stroke-width="1.6" stroke-opacity=".35"/>')
    c.add(f'<path d="{d}" fill="none" stroke="{T["orange"]}" stroke-width="1.6" class="flow" marker-end="url(#ah)"/>')
    if label:
        w = measure(label.upper(), "mono", 11.5, 1.2) + 18
        c.rect(lx - w / 2, ly - 11, w, 22, 11, T["surface"], T["orange"], 1)
        c.text(lx, ly + 4.2, label.upper(), "mono", 11.5, T["tint_text"], anchor="middle", ls=1.2)


# ── data from the example home ──────────────────────────────────────────────


def funnel(motion: str) -> dict:
    text = (MOTIONS / motion / "RESULTS.md").read_text(encoding="utf-8")
    table = text.split("## Funnel", 1)[1].split("\n## ", 1)[0]
    counts = {}
    for row in table.splitlines():
        cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
        if len(cells) >= 2 and cells[1].isdigit():
            counts[cells[0]] = int(cells[1])
    return counts


JULY = funnel("2026-07-outbound-holdco-data-leads")
SEPT = funnel("2026-09-outbound-agency-ops")


# ── 1 · hero ────────────────────────────────────────────────────────────────


def hero(T: dict) -> Canvas:
    c = Canvas(1200, 580, "Compound GTM by Revenue Puzzles",
               "Every campaign makes the next one easier. A go-to-market skill for Claude with an evidence-graded GTM home.")
    frame(c, T)
    x = 64
    logo(c, T, x, 52)
    w = wordmark(c, T, x + 42, 73)
    c.text(x + 42 + w + 12, 73, "/", "display", 19, T["muted"])
    c.text(x + 42 + w + 30, 73, "Compound GTM", "display", 19, T["ink"], ls=-0.2)

    eyebrow(c, T, x, 140, "Open-source skill for Claude · MIT")
    size, lead = 60, 64
    for i, line in enumerate(["Every campaign", "makes the next", "one easier."]):
        base = 212 + i * lead
        if i == 2:
            uw = measure("one easier", "display", size, -2.1)
            c.rect(x, base + 4, uw, 9, 2, T["orange"])
        c.text(x, base, line, "display", size, T["ink"], ls=-2.1)

    para = ("A skill for Claude that keeps your ICP, positioning, proof and plays in one home — "
            "and writes every campaign's lessons back in, graded by evidence.")
    c.lines(x, 392, wrap(para, 540, "sans", 18.5), 28, font="sans", size=18.5, fill=T["body"])

    stats = [("24", "moves, one front door"), ("4", "evidence levels"),
             (f"{JULY['Meeting']} → {SEPT['Meeting']}", "meetings in the example")]
    sx = x
    for value, caption in stats:
        vw = c.text(sx, 510, value, "display", 30, T["ink"], ls=-0.6)
        c.text(sx, 536, caption, "sans", 15, T["muted"])
        sx += max(vw, measure(caption, "sans", 15)) + 36

    # terminal card, in the style of revenuepuzzles.com
    cx, cy, cw = 652, 64, 484
    c.extra_defs.append('<filter id="sh" x="-10%" y="-10%" width="120%" height="130%">'
                        '<feDropShadow dx="0" dy="10" stdDeviation="14" flood-color="#151518" flood-opacity=".08"/></filter>')
    rows = [
        ("HUMAN", "solid", "sets the hypothesis", "done"),
        ("PLAN", "row", "brief.md · kill if < 3 positive / 100", "done"),
        ("RUN", "row", f"sequence.md · {SEPT['Reached']} contacts", "done"),
        ("REVIEW", "orange", f"results · {SEPT['Meeting']} meetings / {SEPT['Reached']}", "done"),
        ("COMPOUND", "orange", "6 lessons → ICP · PLAYS · PROOF", "running"),
        ("HUMAN", "solid", "confirms what gets written", "awaiting review"),
        ("NEXT", "row", "uk-agency-ops starts from here", "queued"),
    ]
    rh, rg = 44, 9
    ch = 64 + len(rows) * (rh + rg) + 12
    c.rect(cx, cy, cw, ch, 20, T["panel"], T["border"], 1.2, ' filter="url(#sh)"')
    for i, color in enumerate([T["orange"], T["grid"], T["grid"]]):
        c.circle(cx + 24 + i * 16, cy + 30, 5, color)
    c.text(cx + 80, cy + 35, "motions / 2026-09-agency-ops", "mono", 13.5, T["muted"])
    c.text(cx + cw - 22, cy + 35, "home: quillmark", "mono", 13.5, T["muted"], anchor="end")
    c.line(cx, cy + 56, cx + cw, cy + 56, T["border"], 1)
    for i, (tag, kind, label, status) in enumerate(rows):
        ry = cy + 70 + i * (rh + rg)
        c.rect(cx + 14, ry, cw - 28, rh, 10, T["row"])
        tw = chip(c, T, cx + 24, ry + 10.5, tag, kind, 11.5, 23)
        c.text(cx + 24 + tw + 10, ry + 27, label, "mono", 13.5, T["ink"])
        if status == "running":
            sw = measure("running", "mono", 13)
            c.circle(cx + cw - 30 - sw - 12, ry + 22, 4, T["orange"], ' class="pulse"')
            c.text(cx + cw - 28, ry + 26.5, "running", "mono", 13, T["tint_text"], anchor="end")
        else:
            c.text(cx + cw - 28, ry + 26.5, status, "mono", 13, T["muted"], anchor="end")
    return c


# ── 2 · the loop ────────────────────────────────────────────────────────────


def loop(T: dict) -> Canvas:
    c = Canvas(1200, 806, "How Compound GTM works",
               "Plan, run, pressure-test, review and compound: every move reads the GTM home first, "
               "and every motion writes its lessons back into it. All 24 moves shown in place.")
    frame(c, T)
    arrow_defs(c, T)
    x = 60
    eyebrow(c, T, x, 74, "How it works")
    c.lines(x, 128, ["One loop. One home.", "Orange lines between them."], 50, font="display", size=44, fill=T["ink"], ls=-1.4)
    para = ("Every move reads the GTM home before it writes. Every motion ends by writing what it "
            "learned back in — graded by evidence, confirmed by a person.")
    c.lines(700, 108, wrap(para, 440, "sans", 17), 26, font="sans", size=17, fill=T["body"])

    stages = [
        ("01 · Plan", "Make it testable", "Hypothesis, success and kill criteria.", ["brief", "play"], "panel"),
        ("02 · Run", "Ship from the home", "Buyer words, backed claims, one ask.", ["sequence", "asset", "discovery"], "panel"),
        ("Gate", "Pressure-test", "Five reviewers before anything ships.", ["buyer", "cfo", "rival", "inbox", "committee"], "solid"),
        ("03 · Review", "Read it honestly", "Counts, denominators, real reasons.", ["results", "winloss", "retro"], "panel"),
        ("04 · Compound", "Write it back", "Each lesson to its file, dated, graded.", ["compound", "audit"], "panel"),
    ]
    top, ch, gap = 228, 252, 20
    cw = (1080 - gap * 4) / 5
    for i, (label, title, caption, moves, style) in enumerate(stages):
        sx = x + i * (cw + gap)
        dark = style == "solid"
        c.rect(sx, top, cw, ch, 16, T["solid"] if dark else T["panel"], None if dark else T["border"], 1.2)
        ink = T["solid_text"] if dark else T["ink"]
        sub = T["muted"] if not dark else ("#B9B9C0" if T is THEMES["light"] else "#55555C")
        c.text(sx + 18, top + 32, label.upper(), "mono", 12.5, T["orange"], ls=1.4)
        tsize = 22
        while measure(title, "display", tsize, -0.5) > cw - 32:
            tsize -= 0.5
        c.text(sx + 18, top + 66, title, "display", tsize, ink, ls=-0.5)
        c.lines(sx + 18, top + 94, wrap(caption, cw - 36, "sans", 15), 22, font="sans", size=15, fill=sub)
        flow_chips(c, T, sx + 18, top + 142, cw - 30, moves, "orange" if dark else "row", 6, 7, 13.5, 27)
        if i < 4:
            ax = sx + cw + 2
            connector(c, T, f"M{num(ax)} {top + ch / 2} H{num(ax + gap - 6)}")

    # the GTM home
    hy, hh = 572, 178
    c.rect(x, hy, 1080, hh, 18, T["peach"], T["border"], 1.2)
    eyebrow(c, T, x + 24, hy + 34, "The GTM home · plain Markdown, any agent", T["tint_text"])
    c.text(x + 24, hy + 72, "What every motion starts from", "display", 24, T["ink"], ls=-0.5)
    files = ["ICP.md", "POSITIONING.md", "PROOF.md", "PLAYS.md", "VOICE.md", "COMPANY.md", ("motions/", "accent")]
    flow_chips(c, T, x + 24, hy + 92, 530, files, "solid", 7, 8, 13.5, 30)
    kx = x + 620
    c.text(kx, hy + 34, "KEPT CURRENT BY", "mono", 12.5, T["muted"], ls=1.4)
    flow_chips(c, T, kx, hy + 50, 440, ["setup", "onboard", "icp", "why-now", "signals",
                                         "alternatives", "positioning", "offer", "proof"], "plain", 6, 8, 13.5, 28)

    # the loop: compound writes down into the home, plan reads up from it
    comp_x = x + 4 * (cw + gap) + cw / 2
    plan_x = x + cw / 2
    connector(c, T, f"M{num(comp_x)} {top + ch + 4} V{hy - 6}", "writes · graded", comp_x, (top + ch + hy) / 2)
    connector(c, T, f"M{num(plan_x)} {hy - 4} V{top + ch + 6}", "reads first", plan_x, (top + ch + hy) / 2)
    c.text(600, 786, "All 24 moves, each in its place. Call one directly — /cg-buyer, /cg-retro — or describe the work to /cg-desk.",
           "sans", 15, T["muted"], anchor="middle")
    return c


# ── 3 · see it compound ─────────────────────────────────────────────────────


def story(T: dict) -> Canvas:
    c = Canvas(1200, 800, "See it compound: the worked example",
               f"July: {JULY['Meeting']} meeting from {JULY['Reached']} contacts. The retro wrote four lines into the GTM home. "
               f"September started from them: {SEPT['Meeting']} meetings from {SEPT['Reached']} contacts. Fictional vendor.")
    frame(c, T)
    arrow_defs(c, T)
    x = 60
    eyebrow(c, T, x, 74, "See it compound · worked example, fictional vendor")
    c.lines(x, 128, ["Nine replies became four lines.", "The next campaign started from them."], 50,
            font="display", size=42, fill=T["ink"], ls=-1.3)

    top, ch = 220, 230
    # July
    c.rect(x, top, 290, ch, 16, T["panel"], T["border"], 1.2)
    c.text(x + 22, top + 34, "JULY · HOLDCO DATA LEADS", "mono", 12.5, T["muted"], ls=1)
    w = c.text(x + 22, top + 118, str(JULY["Meeting"]), "display", 76, T["gray_mark"], ls=-2)
    c.text(x + 30 + w, top + 118, "meeting", "display", 24, T["ink"], ls=-0.4)
    c.lines(x + 22, top + 156, [f"from {JULY['Reached']} contacts", "kill criterion hit", "play retired"], 22,
            font="sans", size=15, fill=T["body"])

    # the retro
    rx, rw = x + 330, 440
    c.rect(rx, top, rw, ch, 16, T["peach"], T["border"], 1.2)
    c.text(rx + 22, top + 34, "RETRO · 2026-08-04 → GTM HOME", "mono", 12.5, T["tint_text"], ls=1)
    lessons = [
        ("ICP", "Data units aren’t the entry point", "Heard ×4"),
        ("ICP", "Agency ops own the reporting pain", "Heard ×4"),
        ("POSITIONING", "Drop “media efficiency” as lead", "Observed"),
        ("PLAYS", "Retire the play, keep the reason", "Observed"),
    ]
    for i, (file, lesson, level) in enumerate(lessons):
        ly = top + 58 + i * 40
        c.rect(rx + 16, ly, rw - 32, 32, 8, T["panel"])
        tw = chip(c, T, rx + 22, ly + 5.5, file, "solid", 11, 21)
        c.text(rx + 22 + tw + 9, ly + 21, lesson, "sans", 14.5, T["ink"])
        c.text(rx + rw - 24, ly + 21, level, "mono", 12, T["muted"], anchor="end")

    # September
    sx = rx + rw + 40
    sw = 1140 - sx
    c.rect(sx, top, sw, ch, 16, T["panel"], T["orange"], 1.6)
    c.text(sx + 22, top + 34, "SEPTEMBER · AGENCY OPS", "mono", 12.5, T["tint_text"], ls=1)
    w = c.text(sx + 22, top + 118, str(SEPT["Meeting"]), "display", 76, T["mark"], ls=-2)
    c.text(sx + 30 + w, top + 118, "meetings", "display", 24, T["ink"], ls=-0.4)
    c.lines(sx + 22, top + 156, [f"from {SEPT['Reached']} contacts", "success criterion hit", "play promoted to working"], 22,
            font="sans", size=15, fill=T["body"])

    connector(c, T, f"M{x + 294} {top + ch / 2} H{rx - 6}")
    connector(c, T, f"M{rx + rw + 4} {top + ch / 2} H{sx - 6}")

    # dumbbell: the same funnel, two campaigns, counts not rates
    stages = [("Replied", "Replied"), ("Positive replies", "Positive reply"), ("Meetings", "Meeting"), ("Qualified", "Qualified")]
    py, row_h = 540, 44
    px0, px1 = x + 190, 1080
    vmax = 35
    scale = lambda v: px0 + (px1 - px0) * v / vmax
    c.text(x, py - 34, "The funnel, July vs September", "semi", 16, T["ink"])
    c.text(x, py - 12, "Counts from the two RESULTS.md files", "sans", 14.5, T["muted"])
    # legend
    lx = 1140
    for label, color in [(f"September · {SEPT['Reached']} contacts", T["mark"]), (f"July · {JULY['Reached']} contacts", T["gray_mark"])]:
        lw = measure(label, "sans", 14.5)
        c.text(lx, py - 22, label, "sans", 14.5, T["body"], anchor="end")
        c.circle(lx - lw - 12, py - 26.5, 5, color)
        lx -= lw + 40
    for tick in range(0, vmax + 1, 10):
        tx = scale(tick)
        c.line(tx, py + 6, tx, py + 6 + row_h * len(stages), T["grid"], 1)
        c.text(tx, py + 28 + row_h * len(stages), str(tick), "mono", 13, T["muted"], anchor="middle")
    for i, (label, key) in enumerate(stages):
        ry = py + 6 + row_h * i + row_h / 2
        c.text(x, ry + 5.5, label, "sans", 16, T["body"])
        a, b = scale(JULY[key]), scale(SEPT[key])
        c.line(a, ry, b, ry, T["grid"], 4)
        c.circle(a, ry, 7, T["gray_mark"], f' stroke="{T["surface"]}" stroke-width="2"')
        c.circle(b, ry, 7, T["mark"], f' stroke="{T["surface"]}" stroke-width="2"')
        c.text(a - 14, ry + 5, str(JULY[key]), "mono", 14, T["muted"], anchor="end")
        c.text(b + 14, ry + 5, str(SEPT[key]), "mono", 14, T["ink"])
    c.text(600, 778, "Invented company and numbers. Different lists and months — a story, not a controlled test.",
           "sans", 14.5, T["muted"], anchor="middle")
    return c


# ── 4 · evidence levels ─────────────────────────────────────────────────────


def evidence(T: dict) -> Canvas:
    c = Canvas(1200, 490, "Four evidence levels",
               "Observed, Heard and Reported can appear in customer-facing copy with their backing. Believed never ships as fact.")
    frame(c, T)
    x = 60
    eyebrow(c, T, x, 74, "Four evidence levels")
    c.text(x, 128, "Not every line gets to ship.", "display", 42, T["ink"], ls=-1.3)
    para = ("Most GTM docs are mostly hunches written in the voice of facts. "
            "Every durable line in the home carries a level, so the difference stays visible.")
    c.lines(700, 104, wrap(para, 440, "sans", 17), 26, font="sans", size=17, fill=T["body"])

    levels = [
        ("Observed", "We saw it in our own data.", "Ships with the number and period.", "(Observed · 11 / 240 · 2026-09)", True),
        ("Heard", "A buyer said it, in their words.", "Ships within its permission.", "(Heard ×5 · discovery calls)", True),
        ("Reported", "A third party published it.", "Ships with source and date.", "(Reported · analyst · 2026-05)", True),
        ("Believed", "Our hypothesis, untested.", "Never ships as fact. Test it first.", "(Believed · founder view)", False),
    ]
    top, ch, cw = 196, 220, 270
    c.rect(x, top, 1080, ch, 16, T["panel"], T["border"], 1.2)
    for i, (name, meaning, rule, tag, ships) in enumerate(levels):
        sx = x + i * cw
        if not ships:
            c.add(f'<path d="M{sx} {top} H{sx + cw - 16} A16 16 0 0 1 {sx + cw} {top + 16} V{top + ch - 16} '
                  f'A16 16 0 0 1 {sx + cw - 16} {top + ch} H{sx} Z" fill="{T["peach"]}"/>')
        if i:
            c.line(sx, top, sx, top + ch, T["border"], 1.2)
        c.text(sx + 22, top + 34, f"LEVEL {i + 1}", "mono", 12.5, T["muted"], ls=1.4)
        c.text(sx + 22, top + 70, name, "display", 28, T["ink"], ls=-0.6)
        c.text(sx + 22, top + 100, meaning, "semi", 15, T["ink"])
        c.text(sx + 22, top + 123, rule, "sans", 14.5, T["body"])
        c.text(sx + 22, top + 157, tag, "mono", 12, T["muted"])
        c.rect(sx + 22, top + 182, cw - 44, 6, 3, T["grid"])
        if ships:
            c.rect(sx + 22, top + 182, cw - 44, 6, 3, T["orange"])
        c.text(sx + cw - 22, top + 208, "in customer copy" if ships else "never as fact", "mono", 12, T["tint_text"] if not ships else T["muted"], anchor="end")
    c.text(x, 460, "Proof also carries a permission tag:", "sans", 15, T["body"])
    px = x + measure("Proof also carries a permission tag:", "sans", 15) + 12
    for name, kind in [("public", "row"), ("anonymised", "row"), ("internal", "solid")]:
        px += chip(c, T, px, 442, name, kind, 12, 26) + 6
    c.text(px + 6, 460, "— unknown means internal.", "sans", 15, T["body"])
    return c


# ── 5 · reviewer lenses ─────────────────────────────────────────────────────


def lenses(T: dict) -> Canvas:
    c = Canvas(1200, 440, "Five reviewer lenses",
               "Buyer, CFO, rival, inbox and committee read a draft before it ships, then merge into one verdict, one fix list and a fixed version.")
    frame(c, T)
    x = 60
    eyebrow(c, T, x, 74, "Pressure-test")
    c.text(x, 128, "Five reviewers who owe you nothing.", "display", 42, T["ink"], ls=-1.3)
    para = ("Run them before anything ships. Lenses diagnose; the review merges them into one verdict, "
            "one fix list and a fixed version.")
    c.lines(760, 104, wrap(para, 380, "sans", 17), 26, font="sans", size=17, fill=T["body"])
    cards = [
        ("/cg-buyer", "The buyer", "“Would I reply — on my phone, between meetings?”"),
        ("/cg-cfo", "The CFO", "“Where’s the return, and compared to what?”"),
        ("/cg-rival", "Their best rep", "“How do I take this apart on my next call?”"),
        ("/cg-inbox", "The inbox", "“Open, archive or report? Two seconds.”"),
        ("/cg-committee", "The committee", "“Who blocks this, and what would move them?”"),
    ]
    top, ch, gap = 192, 196, 16
    cw = (1080 - gap * 4) / 5
    for i, (cmd, who, question) in enumerate(cards):
        sx = x + i * (cw + gap)
        c.rect(sx, top, cw, ch, 16, T["panel"], T["border"], 1.2)
        chip(c, T, sx + 16, top + 18, cmd, "orange", 12.5, 26)
        c.text(sx + 18, top + 84, who, "display", 23, T["ink"], ls=-0.5)
        c.lines(sx + 18, top + 118, wrap(question, cw - 34, "sans", 16), 24, font="sans", size=16, fill=T["body"])
    c.text(x, 418, "Pick lenses by asset: cold email → buyer + inbox · page → buyer · proposal → committee + cfo · competitive deal → + rival.",
           "sans", 15, T["muted"])
    return c


# ── 6 · call to action ──────────────────────────────────────────────────────


def cta(T: dict) -> Canvas:
    c = Canvas(1200, 300, "Revenue Puzzles — GTM operating partner",
               "Want Compound GTM running inside your team? Revenue Puzzles builds the home from your calls and CRM and wires the plays to your tools.")
    c.rect(1, 1, c.w - 2, c.h - 2, 24, "#151518", "#2E2E34", 1.5)
    x = 60
    logo(c, T, x, 48, dark_bg=True)
    wordmark(c, T, x + 42, 69, dark_bg=True)
    c.text(x, 124, "GTM OPERATING PARTNER · HUMANS + AGENTS", "mono", 13.5, "#FF7A45", ls=1.6)
    c.text(x, 174, "Want this running inside your team?", "display", 38, "#FFFFFF", ls=-1.1)
    para = ("The home built from your calls and CRM, plays wired to your tools, agents doing the legwork "
            "— and people making the calls.")
    c.lines(x, 214, wrap(para, 640, "sans", 17), 26, font="sans", size=17, fill="#B9B9C0")
    label = "revenuepuzzles.com  →"
    bw = measure(label, "semi", 18) + 56
    bx, by = 1140 - bw, 118
    c.rect(bx, by, bw, 56, 28, T["orange"])
    c.text(bx + bw / 2, by + 35, label, "semi", 18, "#FFFFFF", anchor="middle")
    c.text(1140, 212, "Forward Deployed Implementation · GTM Audit", "sans", 15, "#B9B9C0", anchor="end")
    c.text(1140, 238, "Warsaw · London · EN / PL", "sans", 15, "#9A9AA2", anchor="end")
    return c


# ── 7 · social preview ──────────────────────────────────────────────────────


def social(T: dict) -> Canvas:
    c = Canvas(1280, 640, "Compound GTM by Revenue Puzzles", "Every campaign makes the next one easier.")
    c.rect(0, 0, 1280, 640, 0, T["surface"])
    x = 80
    logo(c, T, x, 70, 15, 4)
    w = wordmark(c, T, x + 48, 94, 22)
    c.text(x + 48 + w + 14, 94, "/ open-source skill for Claude", "display", 22, T["muted"], ls=-0.2)
    c.text(x, 262, "Compound GTM", "display", 104, T["ink"], ls=-3.6)
    uw = measure("next one easier.", "display", 44, -1.2)
    lead = measure("Every campaign makes the ", "display", 44, -1.2)
    c.rect(x + lead, 344, uw - 12, 8, 2, T["orange"])
    c.text(x, 336, "Every campaign makes the next one easier.", "display", 44, T["ink"], ls=-1.2)
    fx = x
    for label in ["24 moves", "evidence-graded GTM home", "Claude + Claude Code"]:
        fx += chip(c, T, fx, 404, label, "plain", 16, 38) + 10
    c.text(x, 560, "github.com/RevenuePuzzles/Compound-gtm", "mono", 18, T["muted"])

    # the logo as the loop: plan → run → review → compound, clockwise from bottom-left
    s, g = 124, 34
    gx, gy = 962, 222
    arrow_defs(c, T)
    cells = {"RUN": (0, 0), "REVIEW": (1, 0), "PLAN": (0, 1), "COMPOUND": (1, 1)}
    for name, (dx, dy) in cells.items():
        px, py = gx + dx * (s + g), gy + dy * (s + g)
        accent = name == "COMPOUND"
        c.rect(px, py, s, s, 30, T["orange"] if accent else T["ink"])
        c.text(px + s / 2, py + s / 2 + 5, name, "mono", 14, "#FFFFFF" if accent else T["surface"], anchor="middle", ls=1)
    for d in [f"M{gx + s / 2} {gy + s + g - 4} V{gy + s + 6}",                # plan → run
              f"M{gx + s + 4} {gy + s / 2} H{gx + s + g - 6}",                # run → review
              f"M{gx + s + g + s / 2} {gy + s + 4} V{gy + s + g - 6}",        # review → compound
              f"M{gx + s + g - 4} {gy + s + g + s / 2} H{gx + s + 6}"]:       # compound → plan
        connector(c, T, d)
    return c


# ── write ───────────────────────────────────────────────────────────────────


def main() -> None:
    F.update(load_fonts())
    ASSETS.mkdir(exist_ok=True)
    themed = {"hero": hero, "loop": loop, "story": story, "evidence": evidence, "lenses": lenses}
    written = []
    for name, draw in themed.items():
        for theme, tokens in THEMES.items():
            path = ASSETS / f"{name}-{theme}.svg"
            path.write_text(draw(tokens).svg(), encoding="utf-8")
            written.append(path)
    for name, draw in {"cta": cta, "social": social}.items():
        path = ASSETS / f"{name}.svg"
        path.write_text(draw(THEMES["light"]).svg(), encoding="utf-8")
        written.append(path)
    for path in written:
        print(f"{path.relative_to(ROOT)}  {path.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
