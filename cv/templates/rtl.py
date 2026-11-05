# -*- coding: utf-8 -*-
"""Small RTL (Arabic) helper layer over python-docx shared by all templates.

In a bidi paragraph OOXML's jc/ind "left" means the logical start edge, which is
the visual right side in Arabic. Helpers below use start/end naming to hide that.
"""
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, Cm, RGBColor

START, END, CENTER = WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.CENTER
LRE, PDF_ = "‪", "‬"


def rgb(h):
    return RGBColor.from_string(h.lstrip("#"))


def _el(tag, **attrs):
    e = OxmlElement(tag)
    for k, v in attrs.items():
        e.set(qn("w:" + k), str(v))
    return e


class RTLDoc:
    def __init__(self, font, size=10, margins=(1.6, 1.8, 1.6, 1.8), ink="1A1A1A"):
        self.doc = Document()
        self.font, self.size, self.ink = font, size, ink
        s = self.doc.sections[0]
        s.page_width, s.page_height = Cm(21.0), Cm(29.7)
        s.top_margin, s.right_margin, s.bottom_margin, s.left_margin = (Cm(m) for m in margins)
        s._sectPr.append(_el("w:bidi"))
        self.section = s
        self.width = s.page_width - s.left_margin - s.right_margin
        st = self.doc.styles["Normal"]
        st.font.name, st.font.size = font, Pt(size)
        rpr = st.element.get_or_add_rPr()
        rf = rpr.find(qn("w:rFonts"))
        for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
            rf.set(qn(a), font)
        rpr.append(_el("w:szCs", val=int(size * 2)))
        rpr.append(_el("w:lang", bidi="ar-IQ"))
        st.paragraph_format.space_after = Pt(0)

    # ------------------------------------------------------------ primitives
    @staticmethod
    def bidi(p):
        ppr = p._p.get_or_add_pPr()
        b = _el("w:bidi")
        for tag in ("w:adjustRightInd", "w:snapToGrid", "w:spacing", "w:ind", "w:jc"):
            nxt = ppr.find(qn(tag))
            if nxt is not None:
                nxt.addprevious(b)
                return
        ppr.append(b)

    def para(self, align=START, before=0, after=0, line=14.5, container=None,
             start_indent=None, end_indent=None, keep_next=False):
        c = container if container is not None else self.doc
        p = c.add_paragraph()
        self.bidi(p)
        p.alignment = align
        pf = p.paragraph_format
        pf.space_before, pf.space_after, pf.line_spacing = Pt(before), Pt(after), Pt(line)
        if start_indent is not None:
            pf.left_indent = Cm(start_indent)
        if end_indent is not None:
            pf.right_indent = Cm(end_indent)
        pf.keep_with_next = keep_next
        return p

    def run(self, p, text, size=None, bold=False, color=None, ltr=False, font=None):
        size = size or self.size
        r = p.add_run(f"{LRE}{text}{PDF_}" if ltr else text)
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.color.rgb = rgb(color or self.ink)
        rp = r._r.get_or_add_rPr()
        if font:
            rf = rp.find(qn("w:rFonts"))
            if rf is None:
                rf = _el("w:rFonts"); rp.insert(0, rf)
            for a in ("w:ascii", "w:hAnsi", "w:cs"):
                rf.set(qn(a), font)
        rp.find(qn("w:sz")).addnext(_el("w:szCs", val=int(size * 2)))
        if bold:
            rp.find(qn("w:b")).addnext(_el("w:bCs"))
        if not ltr:
            rp.append(_el("w:rtl"))
        return r

    @staticmethod
    def shade(p, fill):
        ppr = p._p.get_or_add_pPr()
        ppr.append(_el("w:shd", val="clear", color="auto", fill=fill.lstrip("#")))

    @staticmethod
    def border(p, **sides):
        """sides: top/bottom/start/end -> (size_eighths, color_hex, space_pt)."""
        ppr = p._p.get_or_add_pPr()
        bdr = ppr.find(qn("w:pBdr"))
        if bdr is None:
            bdr = _el("w:pBdr")
            # pBdr must precede shd/tabs/bidi/spacing/ind/jc
            for tag in ("w:shd", "w:tabs", "w:bidi", "w:spacing", "w:ind", "w:jc"):
                nxt = ppr.find(qn(tag))
                if nxt is not None:
                    nxt.addprevious(bdr); break
            else:
                ppr.append(bdr)
        # paragraph borders are visual: in RTL the start edge is the right side
        names = {"top": "top", "start": "right", "bottom": "bottom", "end": "left"}
        for side in ("top", "start", "bottom", "end"):
            if side in sides:
                sz, color, space = sides[side]
                bdr.append(_el("w:" + names[side], val="single", sz=sz, space=space,
                               color=color.lstrip("#")))

    def end_tab(self, p):
        p.paragraph_format.tab_stops.add_tab_stop(self.width, alignment=2)

    def bullet(self, text, lead=None, marker="•", marker_color=None, indent=0.45,
               size=None, line=14.5, after=1.5, lead_color=None, container=None):
        p = self.para(after=after, line=line, start_indent=indent, container=container)
        p.paragraph_format.first_line_indent = -Cm(0.4)
        self.run(p, marker + "  ", size=size, color=marker_color)
        if lead:
            self.run(p, lead + ": ", size=size, bold=True, color=lead_color)
        self.run(p, text, size=size)
        return p

    def contact_line(self, p, parts, size, color, sep="   |   "):
        for i, (txt, ltr) in enumerate(parts):
            if i:
                self.run(p, sep, size=size, color=color)
            self.run(p, txt, size=size, color=color, ltr=ltr)

    # ------------------------------------------------------------ tables (sidebar layout)
    def table(self, widths_cm, fills=None):
        t = self.doc.add_table(rows=1, cols=len(widths_cm))
        tblPr = t._tbl.tblPr
        tblPr.append(_el("w:bidiVisual"))
        for old in tblPr.findall(qn("w:tblW")):
            tblPr.remove(old)
        tblPr.append(_el("w:tblW", w=int(sum(widths_cm) * 567), type="dxa"))
        tblPr.append(_el("w:jc", val="center"))
        lay = _el("w:tblLayout", type="fixed"); tblPr.append(lay)
        grid = t._tbl.tblGrid
        for gc, w in zip(grid.findall(qn("w:gridCol")), widths_cm):
            gc.set(qn("w:w"), str(int(w * 567)))
        borders = _el("w:tblBorders")
        for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
            borders.append(_el("w:" + side, val="nil"))
        tblPr.append(borders)
        mar = _el("w:tblCellMar")
        for side in ("top", "bottom"):
            mar.append(_el("w:" + side, w=0, type="dxa"))
        for side in ("left", "right"):
            mar.append(_el("w:" + side, w=0, type="dxa"))
        tblPr.append(mar)
        for i, w in enumerate(widths_cm):
            cell = t.rows[0].cells[i]
            cell.width = Cm(w)
            tcPr = cell._tc.get_or_add_tcPr()
            if fills and fills[i]:
                tcPr.append(_el("w:shd", val="clear", color="auto", fill=fills[i].lstrip("#")))
            # remove the default empty paragraph later via first-use helper
        return t

    @staticmethod
    def cell_padding(cell, top=0, start=0, bottom=0, end=0):
        tcPr = cell._tc.get_or_add_tcPr()
        m = _el("w:tcMar")
        for side, v in (("top", top), ("left", start), ("bottom", bottom), ("right", end)):
            m.append(_el("w:" + side, w=int(v * 567), type="dxa"))
        tcPr.append(m)

    def save(self, path):
        self.doc.save(path)
