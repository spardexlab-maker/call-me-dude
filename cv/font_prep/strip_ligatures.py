# Keep only lam-alef in Cairo's 'rlig' so PDF text extraction stays faithful
from fontTools.ttLib import TTFont
import glob,re
def lamalef(g): return bool(re.fullmatch(r'uniFEF[5-9A-C]',g))
for path in glob.glob('/root/.fonts/Cairo-*.ttf'):
    f=TTFont(path); cmap=f.getBestCmap(); g=f['GSUB'].table
    rlig={i for fr in g.FeatureList.FeatureRecord if fr.FeatureTag=='rlig' for i in fr.Feature.LookupListIndex}
    kept=dropped=0
    for li in rlig:
        lk=g.LookupList.Lookup[li]
        for st in lk.SubTable:
            s=st.ExtSubTable if lk.LookupType==7 else st
            if not hasattr(s,'ligatures'): continue
            for first,ligs in list(s.ligatures.items()):
                keep=[l for l in ligs if lamalef(l.LigGlyph)]
                dropped+=len(ligs)-len(keep); kept+=len(keep)
                if keep: s.ligatures[first]=keep
                else: del s.ligatures[first]
    f.save(path); print(path,'kept',kept,'dropped',dropped)
