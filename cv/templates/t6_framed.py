# -*- coding: utf-8 -*-
"""Template 6 — Framed Executive: boxed header card, solid dark section bars with white titles,
olive + gold palette, El Messiri."""
import sys
from rtl import RTLDoc, START, CENTER
import content as C

OLIVE, GOLD, CREAM, INK, MUTED = "2F3E2C", "A8893A", "F7F3E8", "1C1C1C", "5E5A50"
d = RTLDoc("El Messiri", size=10, margins=(1.1, 1.7, 1.0, 1.7), ink=INK)


def boxed(line, align=CENTER, after=0):
    p = d.para(align, line=line, after=after)
    d.shade(p, CREAM)
    d.border(p, top=(18, GOLD, 4), bottom=(18, GOLD, 4), start=(18, GOLD, 8), end=(18, GOLD, 8))
    return p


# header card (adjacent paragraphs with identical borders merge into one frame)
boxed(8)
p = boxed(36); d.run(p, C.NAME, size=26, bold=True, color=OLIVE)
p = boxed(18); d.run(p, C.TITLE_AR, size=11.5, bold=True, color=GOLD)
p = boxed(14); d.run(p, C.TITLE_EN, size=9, color=MUTED, ltr=True)
p = boxed(20)
d.contact_line(p, [(C.LOCATION, False), (C.PHONE, True), (C.EMAIL, True), (C.EMAIL2, True)], 10, OLIVE, sep="    •    ")
boxed(8)

# stats row
p = d.para(CENTER, before=8, line=24)
for i, (num, label) in enumerate(C.STATS):
    if i:
        d.run(p, "   |   ", size=11, color=GOLD)
    d.run(p, num, size=16, bold=True, color=OLIVE, ltr=True)
    d.run(p, " " + label, size=9.5, color=MUTED)


def heading(text):
    p = d.para(before=8, after=4, line=18, keep_next=True)
    d.shade(p, OLIVE)
    d.run(p, "  " + text, size=12, bold=True, color="FFFFFF")


def role(title, org, dates, before=6):
    p = d.para(before=before, line=17, keep_next=True)
    d.end_tab(p)
    d.run(p, title, size=11.5, bold=True, color=OLIVE)
    d.run(p, "\t" + dates, size=10, bold=True, color=GOLD)
    p = d.para(after=2, line=15, keep_next=True)
    d.border(p, bottom=(4, "D9CFB0", 2))
    d.run(p, org, size=10, bold=True, color=MUTED)


def bullet(text, lead=None, **kw):
    return d.bullet(text, lead=lead, marker="•", marker_color=GOLD, lead_color=OLIVE, line=14.5, **kw)


heading("الملخص المهني")
p = d.para(after=2, line=16); d.run(p, C.SUMMARY)

heading("المهارات والقدرات القيادية")
for lead, text in C.COMPETENCIES:
    bullet(text, lead=lead)
p = d.para(before=3, line=13.5, start_indent=0.45)
d.run(p, C.KEYWORDS, size=8.5, color=MUTED, ltr=True)

heading("الخبرة المهنية")
for i, r in enumerate(C.ROLES):
    role(r["title"], r["org"], r["dates"], before=2 if i == 0 else 10)
    for lead, text in r["bullets"]:
        bullet(text, lead=lead)
    for gh, items in r["groups"]:
        if items is None:
            p = d.para(before=7, after=2, line=16, keep_next=True)
            d.shade(p, CREAM)
            d.border(p, start=(24, GOLD, 4))
            d.run(p, " " + gh, size=10.5, bold=True, color=OLIVE)
            continue
        p = d.para(before=4, after=1, line=15, start_indent=0.4, keep_next=True)
        d.run(p, gh, size=10, bold=True, color=GOLD)
        for it in items:
            d.bullet(it, marker="–", marker_color=OLIVE, indent=0.95, size=9.5, line=13.5, after=0)

heading("الشراكات والمشاريع الاستثمارية")
P = C.PARTNERSHIP
role(P["title"], P["org"], "", before=2)
bullet(P["text"])

heading("المؤهل الأكاديمي")
E = C.EDUCATION
role(E["degree"], E["school"], E["year"], before=2)

heading("اللغات")
for lead, text in C.LANGUAGES:
    bullet(text, lead=lead)

d.save(sys.argv[1])
