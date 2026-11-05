# -*- coding: utf-8 -*-
"""Template 3 — Classic Naskh: formal, centered, framed headings, burgundy accent, Amiri."""
import sys
from rtl import RTLDoc, START, CENTER
import content as C

WINE, INK, GREY, RULE = "7A1F2B", "111111", "555555", "B9A27A"
d = RTLDoc("Amiri", size=10.5, margins=(1.3, 1.9, 1.3, 1.9), ink=INK)

# ---------------------------------------------------------------- header
p = d.para(CENTER, line=40); d.run(p, C.NAME, size=26, bold=True, color=WINE)
p = d.para(CENTER, line=18, after=1); d.run(p, C.TITLE_AR, size=12, bold=True)
p = d.para(CENTER, line=14, after=4); d.run(p, C.TITLE_EN, size=9, color=GREY, ltr=True)
p = d.para(CENTER, line=18, after=6)
d.border(p, top=(4, RULE, 4), bottom=(4, RULE, 4))
d.contact_line(p, [(C.LOCATION, False), (C.PHONE, True), (C.EMAIL, True)], 10, INK, sep="   ◆   ")


def heading(text):
    p = d.para(CENTER, before=9, after=5, line=19, keep_next=True)
    d.run(p, "❖  ", size=9, color=RULE)
    d.run(p, text, size=13.5, bold=True, color=WINE)
    d.run(p, "  ❖", size=9, color=RULE)
    d.border(p, bottom=(6, WINE, 2))


def role(title, org, dates, before=8):
    p = d.para(before=before, line=18, keep_next=True)
    d.end_tab(p)
    d.run(p, title, size=12, bold=True, color=INK)
    d.run(p, "\t" + dates, size=10.5, bold=True, color=WINE)
    p = d.para(after=2, line=16, keep_next=True)
    d.run(p, org, size=11, color=WINE)


heading("الملخص التنفيذي")
p = d.para(CENTER, line=16, start_indent=0.6, end_indent=0.6); d.run(p, C.SUMMARY)

heading("الكفاءات الأساسية")
for lead, text in C.COMPETENCIES:
    d.bullet(text, lead=lead, marker="◆", marker_color=WINE, lead_color=WINE, line=15.5, size=10.5)
p = d.para(CENTER, before=3, line=14)
d.run(p, C.KEYWORDS, size=8.5, color=GREY, ltr=True)

heading("الخبرة المهنية")
for i, r in enumerate(C.ROLES):
    role(r["title"], r["org"], r["dates"], before=2 if i == 0 else 10)
    for lead, text in r["bullets"]:
        d.bullet(text, lead=lead, marker="◆", marker_color=WINE, lead_color=INK, line=15.5)
    for gh, items in r["groups"]:
        p = d.para(before=6, after=1, line=15.5, start_indent=0.45, keep_next=True)
        d.run(p, gh, size=11, bold=True, color=WINE)
        p = d.para(after=1, line=15.5, start_indent=0.45)
        d.run(p, "، ".join(it.replace(" — ", " (", 1) + ")" for it in items), size=10.5)

heading("الشراكات والاستثمارات")
P = C.PARTNERSHIP
role(P["title"], P["org"], "", before=2)
d.bullet(P["text"], marker="◆", marker_color=WINE, line=15.5)

heading("التعليم")
E = C.EDUCATION
role(E["degree"], E["school"], E["year"], before=2)

heading("اللغات")
p = d.para(CENTER, line=15.5)
for i, (lead, text) in enumerate(C.LANGUAGES):
    if i:
        d.run(p, "     ◆     ", size=9, color=RULE)
    d.run(p, lead + ": ", bold=True, color=WINE)
    d.run(p, text)

d.save(sys.argv[1])
