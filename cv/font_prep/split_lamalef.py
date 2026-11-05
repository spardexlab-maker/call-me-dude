"""Replace Cairo's lam-alef ligature with two contextual single substitutions.

The lam glyph is swapped for a copy of the lam-alef shape and the alef for a
zero-width empty glyph. The page looks identical, but each glyph now maps to
one character, so PDF text extraction (ATS parsers) reads "لا" correctly.
"""
import copy, glob
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables import otTables as ot

LAM = {"uniFEDF": "init", "uniFEE0": "medi"}
ALEF = {"uniFE8E": {"init": "uniFEFB", "medi": "uniFEFC"},
        "uniFE84": {"init": "uniFEF7", "medi": "uniFEF8"},
        "uniFE88": {"init": "uniFEF9", "medi": "uniFEFA"},
        "uniFE82": {"init": "uniFEF5", "medi": "uniFEF6"}}

def single(mapping):
    lk = ot.Lookup(); lk.LookupType = 1; lk.LookupFlag = 0
    st = ot.SingleSubst(); st.mapping = mapping; st.Format = 2
    lk.SubTable = [st]; lk.SubTableCount = 1
    return lk

def cov(glyphs):
    c = ot.Coverage(); c.glyphs = glyphs; return c

for path in glob.glob("/root/.fonts/Cairo-*.ttf"):
    f = TTFont(path)
    order = list(f.getGlyphOrder())
    glyf, hmtx = f["glyf"], f["hmtx"]
    new = []
    def add(name, src=None):
        if src:
            glyf[name] = copy.deepcopy(glyf[src]); hmtx[name] = hmtx[src]
        else:
            g = copy.deepcopy(glyf[".notdef"]); g.numberOfContours = 0
            for a in ("coordinates", "endPtsOfContours", "flags", "program", "components"):
                if hasattr(g, a): delattr(g, a)
            glyf[name] = g; hmtx[name] = (0, 0)
        new.append(name)
    add("alef.lamhidden")
    for alef, forms in ALEF.items():
        for form, lig in forms.items():
            add(f"{lig}.split", lig)
    full = list(dict.fromkeys(list(order) + new))
    f.setGlyphOrder(full); glyf.glyphOrder = full
    if "post" in f and hasattr(f["post"], "extraNames"):
        f["post"].formatType = 2.0

    g = f["GSUB"].table
    # drop the original lam-alef ligatures from rlig
    rlig = {i for fr in g.FeatureList.FeatureRecord if fr.FeatureTag == "rlig"
            for i in fr.Feature.LookupListIndex}
    for li in rlig:
        lk = g.LookupList.Lookup[li]
        for st in lk.SubTable:
            s = st.ExtSubTable if lk.LookupType == 7 else st
            if hasattr(s, "ligatures"):
                for k in list(s.ligatures):
                    s.ligatures[k] = [l for l in s.ligatures[k] if not l.LigGlyph.startswith("uniFEF")]
                    if not s.ligatures[k]: del s.ligatures[k]
    lookups = g.LookupList.Lookup
    hide = len(lookups); lookups.append(single({a: "alef.lamhidden" for a in ALEF}))
    lam_lk = {}
    for alef, forms in ALEF.items():
        lam_lk[alef] = len(lookups)
        lookups.append(single({lam: f"{forms[form]}.split" for lam, form in LAM.items()}))
    chain = ot.Lookup(); chain.LookupType = 6; chain.LookupFlag = 0; chain.SubTable = []
    for alef in ALEF:
        st = ot.ChainContextSubst(); st.Format = 3
        st.BacktrackGlyphCount = 0; st.BacktrackCoverage = []
        st.LookAheadGlyphCount = 0; st.LookAheadCoverage = []
        st.InputGlyphCount = 2; st.InputCoverage = [cov(list(LAM)), cov([alef])]
        r0 = ot.SubstLookupRecord(); r0.SequenceIndex = 0; r0.LookupListIndex = lam_lk[alef]
        r1 = ot.SubstLookupRecord(); r1.SequenceIndex = 1; r1.LookupListIndex = hide
        st.SubstLookupRecord = [r0, r1]; st.SubstCount = 2
        chain.SubTable.append(st)
    chain.SubTableCount = len(chain.SubTable)
    ci = len(lookups); lookups.append(chain)
    g.LookupList.LookupCount = len(lookups)
    for fr in g.FeatureList.FeatureRecord:
        if fr.FeatureTag == "rlig":
            fr.Feature.LookupListIndex.append(ci); fr.Feature.LookupCount += 1
    f.save(path)
    print("patched", path)
