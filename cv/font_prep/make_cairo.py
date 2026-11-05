import sys,os
from fontTools.ttLib import TTFont
from fontTools.merge import Merger
d=sys.argv[1]; out=os.path.expanduser('~/.fonts'); os.makedirs(out,exist_ok=True)
for w,style in [(400,'Regular'),(700,'Bold')]:
    parts=[]
    for sub in ['arabic','latin']:
        f=TTFont(f'{d}/x/fontsource-cairo-5.3.0/files/cairo-{sub}-{w}-normal.woff'); f.flavor=None
        p=f'{d}/cairo-{sub}-{w}.ttf'; f.save(p); parts.append(p)
    m=Merger().merge(parts)
    for r in m['name'].names:
        if r.nameID==1: r.string='Cairo'
        if r.nameID==2: r.string=style
        if r.nameID in (4,): r.string=f'Cairo {style}'
        if r.nameID==6: r.string=f'Cairo-{style}'
    m['OS/2'].usWeightClass=w
    if w==700: m['OS/2'].fsSelection=(m['OS/2'].fsSelection|0x20)&~0x40; m['head'].macStyle|=1
    m.save(f'{out}/Cairo-{style}.ttf')
print('ok')
