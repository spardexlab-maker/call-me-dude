# -*- coding: utf-8 -*-
"""Template 5 — Minimal Timeline: numbered sections, date chips, vertical timeline rail, indigo, Cairo."""
import sys
from rtl import RTLDoc, START, CENTER, _el
import content as C

INDIGO, SOFT, RAIL, INK, MUTED = "3730A3", "A5B4FC", "C7D2FE", "1E1B2E", "6B7280"
d = RTLDoc("Cairo", size=9.5, margins=(1.1, 1.7, 1.0, 1.7), ink=INK)

# ---------------------------------------------------------------- header (start-aligned)
p = d.para(START, line=38); d.run(p, C.NAME, size=28, bold=True, color=INDIGO)
p = d.para(START, line=17); d.run(p, C.TITLE_AR, size=11.5, bold=True, color=INK)
p = d.para(START, line=14); d.run(p, C.TITLE_EN, size=9, color=MUTED, ltr=True)
p = d.para(START, line=18, after=4)
d.contact_line(p, [(C.PHONE, True), (C.EMAIL, True), (C.EMAIL2, True), (C.LOCATION, False)], 9.5, INDIGO, sep="     ")
d.border(p, bottom=(24, INDIGO, 6))

n = [0]


def heading(text):
    n[0] += 1
    p = d.para(before=9, after=3, line=21, keep_next=True)
    d.run(p, f"{n[0]:02d}", size=17, bold=True, color=SOFT, ltr=True)
    d.run(p, "   " + text, size=13, bold=True, color=INDIGO)


def chip(p, text):
    r = d.run(p, f"  {text}  ", size=9, bold=True, color="FFFFFF")
    r._r.get_or_add_rPr().append(_el("w:shd", val="clear", color="auto", fill=INDIGO))


def rail(p):
    d.border(p, start=(12, RAIL, 10))


# stats row
p = d.para(START, before=8, line=26)
for i, (num, label) in enumerate(C.STATS):
    if i:
        d.run(p, "        ", size=9)
    d.run(p, num, size=18, bold=True, color=INDIGO, ltr=True)
    d.run(p, " " + label, size=9, color=MUTED)

heading("الملخص التنفيذي")
p = d.para(line=15.5, start_indent=0.9); d.run(p, C.SUMMARY)

heading("الكفاءات الأساسية")
for lead, text in C.COMPETENCIES:
    p = d.bullet(text, lead=lead, marker="●", marker_color=INDIGO, lead_color=INDIGO, indent=1.3, line=15)
p = d.para(before=3, line=13.5, start_indent=0.9)
d.run(p, C.KEYWORDS, size=8, color=MUTED, ltr=True)

heading("الخبرة المهنية")
for i, r in enumerate(C.ROLES):
    p = d.para(before=2 if i == 0 else 10, after=2, line=17, start_indent=0.9, keep_next=True)
    chip(p, r["dates"])
    p = d.para(line=17, start_indent=0.9, keep_next=True); rail(p)
    p.paragraph_format.space_after = d.doc.styles["Normal"].paragraph_format.space_after
    d.run(p, r["title"], size=11.5, bold=True, color=INK)
    p.add_run().add_break()
    d.run(p, r["org"], size=10, bold=True, color=INDIGO)
    for lead, text in r["bullets"]:
        rail(d.bullet(text, lead=lead, marker="○", marker_color=INDIGO, lead_color=INK, indent=1.3, line=15))
    for gh, items in r["groups"]:
        if items is None:
            p = d.para(before=8, after=1, line=16, start_indent=0.9, keep_next=True); rail(p)
            chip(p, gh)
            continue
        p = d.para(before=4, after=1, line=15, start_indent=0.9, keep_next=True); rail(p)
        d.run(p, gh, size=10, bold=True, color=INDIGO)
        d.run(p, f"  ({len(items)})", size=9, bold=True, color=MUTED, ltr=True)
        for it in items:
            rail(d.bullet(it, marker="·", marker_color=INDIGO, indent=1.6, size=9, line=13, after=0))

heading("الشراكات والاستثمارات")
P = C.PARTNERSHIP
p = d.para(line=17, start_indent=0.9); d.run(p, P["title"], size=11, bold=True)
d.run(p, "   " + P["org"], size=10, bold=True, color=INDIGO)
p = d.para(line=15, start_indent=0.9); d.run(p, P["text"])

heading("التعليم")
E = C.EDUCATION
p = d.para(line=17, start_indent=0.9); chip(p, E["year"])
d.run(p, "   " + E["degree"], size=11, bold=True)
d.run(p, "   " + E["school"], size=10, color=INDIGO, bold=True)

heading("اللغات")
p = d.para(line=16, start_indent=0.9)
for i, (lead, text) in enumerate(C.LANGUAGES):
    if i:
        d.run(p, "        ", size=9)
    d.run(p, lead + "  ", bold=True, color=INDIGO)
    d.run(p, text, color=MUTED)

d.save(sys.argv[1])
