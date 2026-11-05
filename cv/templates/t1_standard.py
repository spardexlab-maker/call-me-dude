# -*- coding: utf-8 -*-
"""Template 1 — Standard ATS: single column, navy headings with rule, Cairo (resume-builder skill layout)."""
import sys
from rtl import RTLDoc, START, CENTER
import content as C

NAVY, INK, MUTED = "1F3864", "1A1A1A", "505050"
d = RTLDoc("Cairo", size=10, margins=(1.6, 1.8, 1.6, 1.8), ink=INK)

p = d.para(CENTER, line=26); d.run(p, C.NAME, size=20, bold=True, color=NAVY)
p = d.para(CENTER, line=16, after=2); d.run(p, C.TITLE_AR, size=11, bold=True)
p = d.para(CENTER, line=14, after=2); d.run(p, C.TITLE_EN, size=9.5, color=MUTED, ltr=True)
p = d.para(CENTER, line=15, after=2)
d.contact_line(p, [(C.LOCATION, False), (C.PHONE, True), (C.EMAIL, True)], 10, MUTED)


def heading(text):
    p = d.para(before=9, after=3, line=16, keep_next=True)
    d.run(p, text, size=12, bold=True, color=NAVY)
    d.border(p, bottom=(8, NAVY, 1))


def role(title, org, dates, before=6):
    p = d.para(before=before, after=1, line=15, keep_next=True)
    d.end_tab(p)
    d.run(p, title, size=10.5, bold=True)
    d.run(p, "  |  " + org, size=10.5)
    d.run(p, "\t" + dates, size=10, bold=True, color=MUTED)


def bullet(text, lead=None, **kw):
    return d.bullet(text, lead=lead, marker="•", marker_color=NAVY, **kw)


heading("الملخص المهني")
p = d.para(after=2, line=15.5); d.run(p, C.SUMMARY)

heading("الكفاءات الأساسية")
for lead, text in C.COMPETENCIES:
    bullet(text, lead=lead)
p = d.para(before=2, after=1, line=14, start_indent=0.45)
d.run(p, "Keywords: " + C.KEYWORDS, size=9, color=MUTED, ltr=True)

heading("الخبرة المهنية")
for i, r in enumerate(C.ROLES):
    role(r["title"], r["org"], r["dates"], before=3 if i == 0 else 8)
    for lead, text in r["bullets"]:
        bullet(text, lead=lead)
    for gh, items in r["groups"]:
        if items is None:
            p = d.para(before=6, after=1, line=15, start_indent=0.2, keep_next=True)
            d.run(p, gh, size=10.5, bold=True, color=INK)
            continue
        p = d.para(before=3, after=1, line=15, start_indent=0.45, keep_next=True)
        d.run(p, gh, size=10, bold=True, color=NAVY)
        for it in items:
            d.bullet(it, marker="–", marker_color=NAVY, indent=1.0, line=14.5, after=0.5)

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
