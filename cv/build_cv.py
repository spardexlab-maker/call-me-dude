# -*- coding: utf-8 -*-
"""Build the Arabic (RTL) executive CV for Eng. Ali Obais Habib as .docx.

Follows the resume-builder skill (github.com/dabydat/resume-builder-skill):
single column, no tables/text boxes/headers/footers, bottom-bordered section
headings, en-dash dates aligned to the far edge, action-verb bullets without
trailing periods, education at the bottom for a senior profile.
"""
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, Cm, RGBColor

FONT = "Cairo"
INK = RGBColor(0x1A, 0x1A, 0x1A)
ACCENT = RGBColor(0x1F, 0x38, 0x64)   # deep navy for name + headings
MUTED = RGBColor(0x50, 0x50, 0x50)

doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)          # A4 (Iraq)
for side in ("left_margin", "right_margin"):
    setattr(sec, side, Cm(1.8))
sec.top_margin = sec.bottom_margin = Cm(1.6)
sec._sectPr.append(OxmlElement("w:bidi"))
TEXT_WIDTH = sec.page_width - sec.left_margin - sec.right_margin

# Base style
st = doc.styles["Normal"]
st.font.name = FONT
st.font.size = Pt(10)
rpr = st.element.get_or_add_rPr()
rfonts = rpr.find(qn("w:rFonts"))
for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
    rfonts.set(qn(a), FONT)
szcs = OxmlElement("w:szCs"); szcs.set(qn("w:val"), "20"); rpr.append(szcs)
lang = OxmlElement("w:lang"); lang.set(qn("w:bidi"), "ar-IQ"); rpr.append(lang)


def _bidi(p):
    ppr = p._p.get_or_add_pPr()
    b = OxmlElement("w:bidi")
    # schema order: bidi must precede spacing/ind/jc
    for tag in ("w:adjustRightInd", "w:snapToGrid", "w:spacing", "w:ind", "w:jc"):
        nxt = ppr.find(qn(tag))
        if nxt is not None:
            nxt.addprevious(b); return
    ppr.append(b)


def _fmt(p, before=0, after=0, line=14.5):
    pf = p.paragraph_format
    pf.space_before, pf.space_after = Pt(before), Pt(after)
    pf.line_spacing = Pt(line)


def run(p, text, size=10, bold=False, color=INK, italic=False):
    r = p.add_run(text)
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = color
    rp = r._r.get_or_add_rPr()
    sz = OxmlElement("w:szCs"); sz.set(qn("w:val"), str(int(size * 2)))
    rp.find(qn("w:sz")).addnext(sz)
    if bold:
        rp.find(qn("w:b")).addnext(OxmlElement("w:bCs"))
    if italic:
        rp.find(qn("w:i")).addnext(OxmlElement("w:iCs"))
    rp.append(OxmlElement("w:rtl"))
    return r


def para(align=WD_ALIGN_PARAGRAPH.LEFT, **kw):  # LEFT == start edge in RTL
    p = doc.add_paragraph()
    _bidi(p)
    p.alignment = align
    _fmt(p, **kw)
    return p


def heading(text):
    p = para(before=9, after=3, line=16)
    run(p, text, size=12, bold=True, color=ACCENT)
    pbdr = OxmlElement("w:pBdr")
    b = OxmlElement("w:bottom")
    for k, v in (("val", "single"), ("sz", "8"), ("space", "1"), ("color", "1F3864")):
        b.set(qn("w:" + k), v)
    pbdr.append(b)
    p._p.get_or_add_pPr().append(pbdr)
    p.paragraph_format.keep_with_next = True
    return p


def role(title, org, dates, before=6):
    """Title + organisation, with dates pushed to the far (left) edge."""
    p = para(before=before, after=1, line=15)
    p.paragraph_format.tab_stops.add_tab_stop(TEXT_WIDTH, alignment=2)  # end-aligned
    run(p, title, size=10.5, bold=True)
    run(p, "  |  " + org, size=10.5, color=INK)
    run(p, "\t" + dates, size=10, bold=True, color=MUTED)
    p.paragraph_format.keep_with_next = True
    return p


def bullet(text, lead=None, level=0, marker="•"):
    p = para(after=1.5, line=14.5)
    indent = Cm(0.45 + 0.55 * level)
    pf = p.paragraph_format
    pf.left_indent = indent           # logical start indent (visual right in RTL)
    pf.first_line_indent = -Cm(0.4)
    run(p, marker + "  ", size=10, color=ACCENT)
    if lead:
        run(p, lead + ": ", bold=True)
    run(p, text)
    return p


def subhead(text, before=4):
    p = para(before=before, after=1, line=15)
    p.paragraph_format.left_indent = Cm(0.2)
    run(p, text, size=10, bold=True, color=ACCENT)
    p.paragraph_format.keep_with_next = True
    return p


# ---------------------------------------------------------------- Header
p = para(WD_ALIGN_PARAGRAPH.CENTER, after=0, line=26)
run(p, "المهندس علي عبيس حبيب", size=20, bold=True, color=ACCENT)
p = para(WD_ALIGN_PARAGRAPH.CENTER, after=2, line=16)
run(p, "مهندس ميكانيك استشاري  |  رئيس مجلس إدارة ومدير عام مشاريع تنفيذية", size=11, bold=True)
p = para(WD_ALIGN_PARAGRAPH.CENTER, after=2, line=15)
run(p, "جمهورية العراق   |   ", size=10, color=MUTED)
r = p.add_run("\u202a+964 783 333 7069\u202c")  # keep LTR inside RTL line; r.font.size = Pt(10); r.font.color.rgb = MUTED
run(p, "   |   ", size=10, color=MUTED)
r = p.add_run("info@al-ezza.com"); r.font.size = Pt(10); r.font.color.rgb = MUTED

# ---------------------------------------------------------------- Summary
heading("الملخص التنفيذي")
p = para(after=2, line=15.5)
run(p, "مهندس ميكانيك استشاري بخبرة تتجاوز 30 عاماً في الهندسة الميكانيكية وإدارة المشاريع "
       "الإنشائية والصناعية الكبرى في العراق. قاد محفظة تضم 25 مشروعاً استراتيجياً في 11 محافظة "
       "عراقية، منها 13 مشروعاً منجزاً بالكامل و12 مشروعاً قيد التنفيذ، في قطاعات محطات معالجة "
       "الصرف الصحي ومحطات الإسالة والضخ، والمستشفيات الكبرى، والأبراج والمجمعات السكنية، والجسور "
       "والطرق الحضرية. يجمع بين القيادة العليا رئيساً لمجلس إدارة مجموعة النماء للاستثمار والتطوير "
       "الصناعي، والإدارة المركزية لمشاريع مجموعة العزة للمقاولات والاستثمارات، وإدارة شراكات "
       "استثمارية وطنية في قطاع الأمن الغذائي.")

# ---------------------------------------------------------------- Competencies
heading("الكفاءات الأساسية")
bullet("إدارة المشاريع الإنشائية والكهروميكانيكية العملاقة (Megaprojects)، قيادة التحالفات "
       "والشراكات، إدارة سلاسل الإمداد، التخطيط التشغيلي وإعداد الموازنات التقديرية",
       lead="القيادة والإدارة الاستراتيجية")
bullet("التفاوض المتقدم، إدارة العقود الهندسية والتجارية وعقود الفيديك (FIDIC)، تسوية "
       "النزاعات التعاقدية، هيكلة الشراكات الاستثمارية", lead="العقود والتفاوض")
bullet("المنظومات الميكانيكية والهيدروليكية، محطات الرفع والضخ ومعالجة المياه والصرف الصحي، "
       "الفحص والتشغيل التجريبي والتسليم (Testing & Commissioning)", lead="الاختصاص الفني")
bullet("AutoCAD لإعداد وتدقيق المخططات الهندسية والتنفيذية، Microsoft Project للجدولة، "
       "Microsoft Office (Word, Excel, PowerPoint) للتقارير الفنية وإدارة البيانات",
       lead="البرمجيات")

# ---------------------------------------------------------------- Experience
heading("الخبرة المهنية")

role("رئيس مجلس الإدارة", "مجموعة النماء للاستثمار والتطوير الصناعي", "2019 – الآن", before=3)
bullet("رسم الخطط الاستراتيجية وأشرف على تأسيس وإدارة محفظة صناعية متكاملة من 5 قطاعات "
       "إنتاجية تغذّي مشاريع الإنشاء والبنى التحتية في العراق")
bullet("أشرف على تصنيع القوالب المعمارية المعقدة والواجهات الهندسية الحديثة",
       lead="معامل الخرسانة المسلحة بالألياف الزجاجية (GRC)")
bullet("أدار خطوط الإنتاج الآلية لتصنيع المقرنص والكيربستون وقطع الشتايكر للمشاريع الحضرية والسكنية",
       lead="معامل المنتجات الخرسانية والأسمنتية")
bullet("أشرف على تشغيل خطوط التقطير والتوزيع الكيميائي للأغراض الصناعية والتخصصية",
       lead="معامل الكحول الصناعي والمذيبات")
bullet("وجّه إنتاج وتوريد المواد والملحقات البلاستيكية المخصصة للمشاريع الإنشائية",
       lead="معامل اللدائن والبلاستيك")
bullet("أشرف على ورش التجميع والصيانة الميكانيكية والكهربائية وتصنيع لوحات السيطرة والتحكم الصناعي",
       lead="الورش والأقسام الكهربائية المركزية")

role("مدير عام المشاريع", "مجموعة العزة للمقاولات والاستثمارات", "2004 – الآن")
bullet("قاد تنفيذ محفظة من 25 مشروعاً استراتيجياً في 11 محافظة عراقية، متولياً الإشراف "
       "الهندسي والإداري والتعاقدي الشامل من مرحلة التعاقد حتى التسليم النهائي")
bullet("سلّم 13 مشروعاً منجزاً بالكامل، تشمل 6 مشاريع مياه وصرف صحي، ومجسرين حضريين، "
       "و5 مستشفيات بسعة إجمالية تتجاوز 800 سرير")
bullet("يقود حالياً 12 مشروعاً قيد التنفيذ، منها 8 مشاريع شبكات ومحطات مجاري وماء وبنى تحتية، "
       "و4 مشاريع سكنية وأبراج من بينها مجمع العزة السكني (3,000 وحدة سكنية)")
bullet("أدار عقود الفيديك (FIDIC) والتفاوض مع الجهات المالكة والاستشارية، وضبط الجداول "
       "الزمنية والموازنات وسلاسل الإمداد عبر مواقع عمل متعددة في آنٍ واحد")

subhead("المشاريع المنجزة — المياه والصرف الصحي")
for t in ["محطة معالجة مجاري طويريج المركزية — كربلاء المقدسة",
          "مشروع شبكات ومحطات مجاري كربلاء المركزية (المرحلة المنجزة) — كربلاء المقدسة",
          "محطة معالجة مجاري الشامية — الديوانية",
          "مشروع ماء غماس ومحطات الضخ المرافقة — الديوانية",
          "محطة معالجة مجاري الرميثة — المثنى",
          "مشروع ماء وبنى تحتية — أسماء الزهور"]:
    bullet(t, level=1, marker="–")

subhead("المشاريع المنجزة — القطاع الصحي")
for t in ["مستشفى كركوك العام (400 سرير) — كركوك",
          "مستشفى كربلاء التخصصي للنسائية والتوليد (300 سرير) — كربلاء المقدسة",
          "مستشفى الرحمانية (100 سرير) — الشعلة، بغداد",
          "مستشفى الشهيد الصدر — النجف الأشرف",
          "مستشفى الصدر — ميسان"]:
    bullet(t, level=1, marker="–")

subhead("المشاريع المنجزة — الجسور والطرق الحضرية")
for t in ["مجسر نادر الإنشائي — الحلة، بابل",
          "مجسر البتيرة الكونكريتي — ميسان"]:
    bullet(t, level=1, marker="–")

subhead("قيد التنفيذ — شبكات الصرف الصحي والمياه والبنى التحتية")
for t in ["شبكات ومحطة معالجة مجاري سبع البور — بغداد",
          "شبكات ومحطات مجاري قضاء كبيسة — الأنبار",
          "شبكات ومحطات مجاري قضاء عانة — الأنبار",
          "شبكات ومحطة معالجة مجاري الخالص — ديالى",
          "شبكات ومحطة مجاري غرب بعقوبة — ديالى",
          "شبكات ومجاري قضاء علي الشرقي — ميسان",
          "مشروع ماء المسيب ومحطات الضخ والتوزيع — بابل",
          "البنى التحتية والخدمات المتكاملة لحي الحوراء (المرحلتان الأولى والثانية) — الكوت، واسط"]:
    bullet(t, level=1, marker="–")

subhead("قيد التنفيذ — التطوير السكني والأبراج")
for t in ["مجمع العزة السكني (3,000 وحدة سكنية متكاملة البنى والخدمات) — ميسان",
          "أبراج حلم بغداد (مجمعات سكنية وأبراج فندقية متكاملة) — بغداد",
          "مجمع الفردوس السكني الاستثماري (أبنية متعددة الطوابق) — كربلاء المقدسة",
          "برج السحاب السكني (برج متعدد الطوابق) — كربلاء المقدسة"]:
    bullet(t, level=1, marker="–")

role("مدير المشروع الفني — محطات معالجة مجاري كربلاء", "مجموعة العزة للمقاولات والاستثمارات",
     "2008 – 2012", before=8)
bullet("أشرف ميدانياً على توريد وتركيب واختبار المنظومات الميكانيكية والهيدروليكية ومحطات "
       "الرفع والمعالجة المركزية")
bullet("قاد الطواقم الفنية في الموقع، وأجرى الفحوصات التشغيلية حتى التسليم النهائي للمشروع")

# ---------------------------------------------------------------- Partnerships
heading("الشراكات والاستثمارات")
role("عضو مجلس إدارة وشريك مساهم", "مطحنة نور السبطين", "", before=2)
bullet("شارك في إدارة مشروع استثماري لإنتاج الحبوب وتعزيز الأمن الغذائي، بالشراكة مع العتبة "
       "الحسينية المقدسة")

# ---------------------------------------------------------------- Education
heading("التعليم")
role("بكالوريوس هندسة ميكانيكية", "الجامعة التكنولوجية — بغداد", "1994", before=2)

# ---------------------------------------------------------------- Languages
heading("اللغات")
bullet("اللغة الأم", lead="العربية")
bullet("إجادة مهنية تامة في المراسلات الهندسية والمفاوضات الفنية", lead="الإنجليزية")

out = __import__("sys").argv[1] if len(__import__("sys").argv) > 1 else "CV_Ali_Obais_Habib.docx"
doc.save(out)
print("saved", out)
