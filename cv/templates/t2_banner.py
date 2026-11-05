# -*- coding: utf-8 -*-
"""Template 2 — Modern Banner: full-bleed teal header band, tinted section bars, Tajawal."""
import sys
from docx.shared import Cm, Pt
from rtl import RTLDoc, START, CENTER
import content as C

TEAL, DARK, TINT, MUTED = "0F766E", "134E4A", "E6F4F2", "5B6B6A"
d = RTLDoc("Tajawal", size=10.5, margins=(1.0, 1.7, 1.4, 1.7))
BLEED = 1.7  # cm, pull band paragraphs out to the page edge


def band(align=CENTER, before=0, after=0, line=16):
    p = d.para(align, before=before, after=after, line=line, start_indent=-BLEED, end_indent=-BLEED)
    d.shade(p, TEAL)
    return p


# ---------------------------------------------------------------- header band
band(line=14)
p = band(line=34); d.run(p, C.NAME, size=26, bold=True, color="FFFFFF")
p = band(line=18); d.run(p, C.TITLE_AR, size=12, bold=True, color="FFFFFF")
p = band(line=15); d.run(p, C.TITLE_EN, size=9.5, color="CCE7E3", ltr=True)
p = band(line=20)
d.contact_line(p, [(C.LOCATION, False), (C.PHONE, True), (C.EMAIL, True)], 10, "FFFFFF")
band(line=14)

# stats strip (tinted)
p = d.para(CENTER, line=26, start_indent=-BLEED, end_indent=-BLEED)
d.shade(p, TINT)
for i, (num, label) in enumerate(C.STATS):
    if i:
        d.run(p, "      ", size=10)
    d.run(p, num, size=15, bold=True, color=TEAL, ltr=True)
    d.run(p, " " + label, size=10, color=DARK)


def heading(text):
    p = d.para(before=12, after=5, line=19, keep_next=True)
    d.shade(p, TINT)
    d.border(p, start=(36, TEAL, 6))
    d.run(p, " " + text, size=12.5, bold=True, color=DARK)


def role(r, before=6):
    p = d.para(before=before, after=0, line=16, keep_next=True)
    d.end_tab(p)
    d.run(p, r["title"], size=11.5, bold=True, color=TEAL)
    d.run(p, "\t" + r["dates"], size=10.5, bold=True, color=TEAL)
    p = d.para(after=2, line=15, keep_next=True)
    d.run(p, r["org"], size=10.5, bold=True, color=MUTED)


heading("الملخص التنفيذي")
p = d.para(after=2, line=16); d.run(p, C.SUMMARY)

heading("الكفاءات الأساسية")
for lead, text in C.COMPETENCIES:
    d.bullet(text, lead=lead, marker="•", marker_color=TEAL, lead_color=DARK, line=15)
p = d.para(before=3, line=14, start_indent=0.45)
d.run(p, "Keywords: " + C.KEYWORDS, size=8.5, color=MUTED, ltr=True)

heading("الخبرة المهنية")
for i, r in enumerate(C.ROLES):
    role(r, before=2 if i == 0 else 9)
    for lead, text in r["bullets"]:
        d.bullet(text, lead=lead, marker="•", marker_color=TEAL, lead_color=DARK, line=15)
    for gh, items in r["groups"]:
        p = d.para(before=5, after=1, line=15, start_indent=0.3, keep_next=True)
        d.run(p, gh, size=10.5, bold=True, color=TEAL)
        p = d.para(after=1, line=15, start_indent=0.3)
        for j, it in enumerate(items):
            if j:
                d.run(p, "   •   ", size=10, bold=True, color=TEAL)
            d.run(p, it, size=10)

heading("الشراكات والاستثمارات")
P = C.PARTNERSHIP
p = d.para(before=2, after=1, line=16); d.run(p, P["title"], size=11.5, bold=True, color=TEAL)
d.run(p, "  |  " + P["org"], size=10.5, bold=True, color=MUTED)
d.bullet(P["text"], marker="•", marker_color=TEAL, line=15)

heading("التعليم")
E = C.EDUCATION
p = d.para(before=2, line=16); d.end_tab(p)
d.run(p, E["degree"], size=11.5, bold=True, color=TEAL)
d.run(p, "  |  " + E["school"], size=10.5, bold=True, color=MUTED)
d.run(p, "\t" + E["year"], size=10, bold=True, color=TEAL)

heading("اللغات")
for lead, text in C.LANGUAGES:
    d.bullet(text, lead=lead, marker="•", marker_color=TEAL, lead_color=DARK, line=15)

d.save(sys.argv[1])
