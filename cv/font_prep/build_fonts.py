"""Build ATS-friendly Arabic TTFs (Cairo, Noto Naskh Arabic, Tajawal, Amiri, El Messiri) from fontsource packages.

For each family/weight:
  1. merge the Arabic + Latin woff subsets into one TTF and name it,
  2. drop decorative Arabic ligatures (liga/dlig/rlig) that PDF text extraction reverses,
  3. re-implement the mandatory lam-alef ligature as two contextual single
     substitutions (lam -> lam-alef shape, alef -> empty zero-width glyph), so the
     page looks the same while every glyph maps back to exactly one character.

usage: python3 build_fonts.py <dir-with-extracted-fontsource-packages> [out-dir]
"""
import copy, os, re, sys
from fontTools.ttLib import TTFont
from fontTools.merge import Merger
from fontTools.ttLib.tables import otTables as ot

SRC = sys.argv[1]
OUT = os.path.expanduser(sys.argv[2] if len(sys.argv) > 2 else "~/.fonts")
FAMILIES = {
    "Cairo": ("fontsource-cairo-5.3.0", "cairo", [(400, "Regular"), (700, "Bold")]),
    "Noto Naskh Arabic": ("fontsource-noto-naskh-arabic-5.3.0", "noto-naskh-arabic", [(400, "Regular"), (700, "Bold")]),
    "Tajawal": ("fontsource-tajawal-5.3.0", "tajawal", [(400, "Regular"), (800, "Bold")]),
    "Amiri": ("fontsource-amiri-5.3.0", "amiri", [(400, "Regular"), (700, "Bold")]),
    "El Messiri": ("fontsource-el-messiri-5.3.0", "el-messiri", [(400, "Regular"), (700, "Bold")]),
}
LAMALEF = set(range(0xFEF5, 0xFEFD))


def merged(pkg, slug, w, family, style):
    parts = []
    for sub in ("arabic", "latin"):
        f = TTFont(f"{SRC}/{pkg}/files/{slug}-{sub}-{w}-normal.woff")
        f.flavor = None
        p = f"/tmp/_{slug}-{sub}-{w}.ttf"
        f.save(p); parts.append(p)
    m = Merger().merge(parts)
    for r in m["name"].names:
        if r.nameID == 1: r.string = family
        if r.nameID == 2: r.string = style
        if r.nameID == 4: r.string = f"{family} {style}"
        if r.nameID == 6: r.string = f"{family.replace(' ', '')}-{style}"
    if style == "Bold":
        m["OS/2"].usWeightClass = 700
        m["OS/2"].fsSelection = (m["OS/2"].fsSelection | 0x20) & ~0x40
        m["head"].macStyle |= 1
    else:
        m["OS/2"].usWeightClass = 400
    return m


def subtables(lk):
    for st in lk.SubTable:
        yield st.ExtSubTable if lk.LookupType == 7 else st


def single(mapping):
    lk = ot.Lookup(); lk.LookupType = 1; lk.LookupFlag = 0
    st = ot.SingleSubst(); st.mapping = mapping
    lk.SubTable = [st]; lk.SubTableCount = 1
    return lk


def cov(glyphs):
    c = ot.Coverage(); c.glyphs = list(glyphs); return c


def patch(f):
    rev = {}
    for cp, g in f.getBestCmap().items():
        rev.setdefault(g, cp)
    is_lamalef = lambda g: rev.get(g) in LAMALEF or bool(re.search(r"lam.*alef|lamalef|lam_alef", g, re.I))
    gsub = f["GSUB"].table
    feats = {fr.FeatureTag for fr in gsub.FeatureList.FeatureRecord}
    lig_lookups = {i for fr in gsub.FeatureList.FeatureRecord if fr.FeatureTag in ("liga", "dlig", "rlig")
                   for i in fr.Feature.LookupListIndex}
    pairs = {}  # (first, second) -> lamalef glyph
    for li in lig_lookups:
        lk = gsub.LookupList.Lookup[li]
        for s in subtables(lk):
            if not hasattr(s, "ligatures"):
                continue
            for first in list(s.ligatures):
                for l in s.ligatures[first]:
                    if is_lamalef(l.LigGlyph) and len(l.Component) == 1:
                        pairs[(first, l.Component[0])] = l.LigGlyph
                del s.ligatures[first]
    if not pairs:
        return 0
    glyf, hmtx = f["glyf"], f["hmtx"]
    order = list(f.getGlyphOrder()); new = []
    empty = "alef.lamhidden"
    g = copy.deepcopy(glyf[".notdef"]); g.numberOfContours = 0
    for a in ("coordinates", "endPtsOfContours", "flags", "program", "components"):
        if hasattr(g, a): delattr(g, a)
    glyf[empty] = g; hmtx[empty] = (0, 0); new.append(empty)
    for lig in set(pairs.values()):
        glyf[lig + ".split"] = copy.deepcopy(glyf[lig]); hmtx[lig + ".split"] = hmtx[lig]
        new.append(lig + ".split")
    full = list(dict.fromkeys(order + new))
    f.setGlyphOrder(full); glyf.glyphOrder = full
    if "post" in f: f["post"].formatType = 2.0

    lookups = gsub.LookupList.Lookup
    hide = len(lookups)
    lookups.append(single({second: empty for (_, second) in pairs}))
    by_second = {}
    for (first, second), lig in pairs.items():
        by_second.setdefault(second, {})[first] = lig + ".split"
    chain = ot.Lookup(); chain.LookupType = 6; chain.LookupFlag = 8  # ignore marks
    chain.SubTable = []
    for second, firsts in by_second.items():
        idx = len(lookups); lookups.append(single(firsts))
        st = ot.ChainContextSubst(); st.Format = 3
        st.BacktrackGlyphCount = 0; st.BacktrackCoverage = []
        st.LookAheadGlyphCount = 0; st.LookAheadCoverage = []
        st.InputGlyphCount = 2
        st.InputCoverage = [cov(sorted(firsts, key=f.getGlyphID)), cov([second])]
        r0 = ot.SubstLookupRecord(); r0.SequenceIndex = 0; r0.LookupListIndex = idx
        r1 = ot.SubstLookupRecord(); r1.SequenceIndex = 1; r1.LookupListIndex = hide
        st.SubstLookupRecord = [r0, r1]; st.SubstCount = 2
        chain.SubTable.append(st)
    chain.SubTableCount = len(chain.SubTable)
    ci = len(lookups); lookups.append(chain)
    gsub.LookupList.LookupCount = len(lookups)
    tag = "rlig" if "rlig" in feats else "liga"
    for fr in gsub.FeatureList.FeatureRecord:
        if fr.FeatureTag == tag:
            fr.Feature.LookupListIndex.append(ci); fr.Feature.LookupCount += 1
    return len(pairs)


os.makedirs(OUT, exist_ok=True)
for family, (pkg, slug, weights) in FAMILIES.items():
    for w, style in weights:
        f = merged(pkg, slug, w, family, style)
        n = patch(f)
        path = f"{OUT}/{family.replace(' ', '')}-{style}.ttf"
        f.save(path)
        print(f"{path}: lam-alef pairs split = {n}")
