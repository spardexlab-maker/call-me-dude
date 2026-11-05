# -*- coding: utf-8 -*-
"""Template 4 — Executive Sidebar: charcoal header, grey side column, gold accents, Cairo.

usage: python3 t4_sidebar.py OUT.docx [ar|en] [photo]
  ar|en  language (default ar; en is a left-to-right layout)
  photo  reserve a photo frame at the top of the side column. The frame is a placeholder
         picture: in Word right-click it → Change Picture to drop in the real photo.

Note: uses a 2-column table for layout. Modern ATS read it fine, but for the strictest
parsers prefer the single-column designs.
"""
import os
import sys
from docx.shared import Cm
from rtl import RTLDoc, START, CENTER

OUT = sys.argv[1]
LANG = sys.argv[2] if len(sys.argv) > 2 else "ar"
PHOTO = len(sys.argv) > 3 and sys.argv[3] == "photo"
AR = LANG == "ar"
if AR:
    import content as C
else:
    import content_en as C

L = {
    "ar": dict(contact="التواصل", stats="أرقام بارزة", skills="المهارات", edu="التعليم", langs="اللغات",
               partner="الشراكات", summary="الملخص المهني", comp="الكفاءات الأساسية",
               exp="الخبرة المهنية"),
    "en": dict(contact="Contact", stats="Key Figures", skills="Skills", edu="Education", langs="Languages",
               partner="Partnerships", summary="Professional Summary", comp="Core Competencies",
               exp="Professional Experience"),
}[LANG]

CHAR, GOLD, SIDE, INK, MUTED = "1F2933", "B08D3C", "F1F2F4", "1A1A1A", "5F6B76"
d = RTLDoc("Cairo", size=9.5, margins=(1.0, 0, 1.0, 0), ink=INK, rtl=AR)
PAD = 1.2


def placeholder_png():
    """Neutral portrait placeholder (silhouette) generated once into templates/assets/."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "photo_placeholder.png")
    if os.path.exists(path):
        return path
    from PIL import Image, ImageDraw
    os.makedirs(os.path.dirname(path), exist_ok=True)
    w, h = 600, 720
    im = Image.new("RGB", (w, h), "#D5D9DF")
    dr = ImageDraw.Draw(im)
    dr.ellipse((w * 0.33, h * 0.17, w * 0.67, h * 0.46), fill="#A9B0BA")          # head
    dr.ellipse((w * 0.14, h * 0.52, w * 0.86, h * 1.18), fill="#A9B0BA")          # shoulders
    dr.rectangle((0, 0, w - 1, h - 1), outline="#B08D3C", width=10)               # gold frame
    im.save(path)
    return path


def band(line, after=0):
    p = d.para(START, line=line, after=after, start_indent=PAD, end_indent=PAD)
    d.shade(p, CHAR)
    return p


band(10)
p = band(34); d.run(p, C.NAME, size=25, bold=True, color="FFFFFF")
if AR:
    p = band(18); d.run(p, C.TITLE_AR, size=11.5, bold=True, color=GOLD)
    p = band(14); d.run(p, C.TITLE_EN, size=9, color="C9CED6", ltr=True)
else:
    p = band(18); d.run(p, C.TITLE, size=11, bold=True, color=GOLD)
band(12)

SIDE_W, MAIN_W = 6.6, 21.0 - 6.6
t = d.table([SIDE_W, MAIN_W], fills=[SIDE, None])
side, main = t.rows[0].cells
d.cell_padding(side, top=0.5, start=0.7, bottom=0.4, end=0.6)
d.cell_padding(main, top=0.5, start=0.7, bottom=0.4, end=PAD)


def s_head(text, before=10):
    p = d.para(before=before, after=3, line=16, container=side)
    d.run(p, text, size=11, bold=True, color=CHAR)
    d.border(p, bottom=(12, GOLD, 2))


def s_line(text, ltr=False, bold=False, size=9.5, color=INK, after=1):
    p = d.para(after=after, line=14, container=side)
    d.run(p, text, size=size, bold=bold, color=color, ltr=ltr)
    return p


# ---------------------------------------------------------------- sidebar
if PHOTO:
    p = side.add_paragraph()        # no fixed line height, so the picture is not clipped
    d.bidi(p)
    p.alignment = CENTER
    p.paragraph_format.space_after = Cm(0.25)
    p.add_run().add_picture(placeholder_png(), width=Cm(3.6))

s_head(L["contact"], before=0)
s_line(C.PHONE, ltr=True)
s_line(C.EMAIL, ltr=True, size=9)
s_line(C.EMAIL2, ltr=True, size=9)
s_line(C.LOCATION)

s_head(L["stats"])
for num, label in C.STATS:
    p = d.para(after=2, line=22, container=side)
    d.run(p, num, size=17, bold=True, color=GOLD, ltr=True)
    d.run(p, "  " + label, size=9.5, color=CHAR)

s_head(L["skills"])
for tag in C.SKILL_TAGS:
    d.bullet(tag, marker="▪", marker_color=GOLD, indent=0.4, size=9.5, line=14, after=1, container=side)

s_head(L["edu"])
s_line(C.EDUCATION["degree"], bold=True)
s_line(C.EDUCATION["school"], color=MUTED)
s_line(C.EDUCATION["year"], bold=True, color=GOLD)

s_head(L["langs"])
for lead, text in C.LANGUAGES:
    s_line(lead, bold=True, after=0); s_line(text, color=MUTED, size=9, after=3)

s_head(L["partner"])
s_line(C.PARTNERSHIP["title"], bold=True)
s_line(C.PARTNERSHIP["org"], color=GOLD, bold=True)
s_line(C.PARTNERSHIP["text"], color=MUTED, size=9)

if AR:  # English keywords help English-language ATS read the Arabic CV
    s_head("Keywords")
    s_line(C.KEYWORDS, ltr=True, size=8, color=MUTED)


# ---------------------------------------------------------------- main column
def m_head(text, before=12):
    p = d.para(before=before, after=4, line=18, container=main)
    d.run(p, "▌", size=13, color=GOLD)
    d.run(p, " " + text, size=13, bold=True, color=CHAR)


m_head(L["summary"], before=0)
p = d.para(after=2, line=15, container=main); d.run(p, C.SUMMARY, size=9.5)

m_head(L["comp"])
for lead, text in C.COMPETENCIES:
    d.bullet(text, lead=lead, marker="•", marker_color=GOLD, lead_color=CHAR, line=14.5, container=main)

m_head(L["exp"])
for i, r in enumerate(C.ROLES):
    p = d.para(before=2 if i == 0 else 9, line=16, container=main)
    p.paragraph_format.tab_stops.add_tab_stop(Cm(MAIN_W - 0.7 - PAD), alignment=2)  # dates to far edge
    d.run(p, r["title"], size=11, bold=True, color=CHAR)
    d.run(p, "\t" + r["dates"], size=9.5, bold=True, color=MUTED)
    p = d.para(after=2, line=14, container=main)
    d.run(p, r["org"], size=9.5, bold=True, color=GOLD)
    for lead, text in r["bullets"]:
        d.bullet(text, lead=lead, marker="•", marker_color=GOLD, lead_color=CHAR, line=14.5, container=main)
    for gh, items in r["groups"]:
        if items is None:
            p = d.para(before=7, after=1, line=16, container=main)
            d.run(p, gh, size=10.5, bold=True, color=GOLD)
            d.border(p, bottom=(4, GOLD, 1))
            continue
        p = d.para(before=4, after=1, line=14.5, start_indent=0.3, container=main)
        d.run(p, gh, size=10, bold=True, color=CHAR)
        for it in items:
            d.bullet(it, marker="–", marker_color=GOLD, indent=0.8, size=9, line=13.5, after=0, container=main)

# drop the empty default paragraph each new cell starts with
for c in (side, main):
    first = c.paragraphs[0]
    if not first.text and not first._p.xpath(".//w:drawing"):
        first._p.getparent().remove(first._p)

d.save(OUT)
