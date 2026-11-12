"""Despre 6 'Coperta' refined: same cover (huge 'Alessia' + duotone portrait in front), four ways to set the text.

usage: python3 .aidesigner/coperta_options.py
writes .aidesigner/canvas/project/CopertaA..D*.dc.html (+ Mobil twins) and local previews .aidesigner/opt-Coperta*.html
"""
import os, subprocess, sys
from about_options2 import P, HERE, DUO, ALT, LEAD, BODY, ROLE, LINK, page

S1, S2, S3 = "Sunt Alessia și cred că", "mâinile știu", "uneori lucruri pe care mintea încă nu le-a spus."

COVER = """
.cv{position:relative;overflow:hidden;background:radial-gradient(ellipse 55% 60% at 50% 38%,#F6EEE3 0%,rgba(246,238,227,0) 70%),linear-gradient(180deg,#EFE4D4 0%,#E8D9C3 58%,#E2CDB0 100%)}
.cv .name{position:absolute;left:50%;top:34px;z-index:0;transform:translateX(-50%);margin:0;font:400 clamp(112px,23vw,340px)/.82 var(--display);font-variation-settings:'opsz' 96;letter-spacing:-.04em;color:var(--terra);white-space:nowrap;pointer-events:none;user-select:none}
.cv .stage{position:relative;z-index:1}
.cv .fig{position:relative;margin:0;aspect-ratio:3/4}
.cv .fig img{display:block;width:100%;height:100%;object-fit:contain;object-position:50% 100%}
.cv h2{color:var(--ink)}
.cv h2 em{color:var(--terra-d)}
.cv .role{color:#833A22}
.cv .body{color:#5E4838}
.cv .more{color:var(--ink)}
.fade{-webkit-mask-image:linear-gradient(180deg,#000 74%,transparent 99%);mask-image:linear-gradient(180deg,#000 74%,transparent 99%)}
@media (max-width:980px){.cv .name{top:20px;font-size:27vw}.cv .fig{width:min(100%,420px);margin:9vw auto 0}}
"""

OPTS = {}

# A. Cover line: the sentence sits centred under her, over the faded bottom of the portrait, like the line on a magazine cover.
OPTS["CopertaA"] = ("Coperta A: rând de copertă, centrat", """
.a .stage{display:flex;flex-direction:column;align-items:center;padding:150px 0 120px;text-align:center}
.a .fig{width:540px;-webkit-mask-image:linear-gradient(180deg,#000 46%,transparent 80%);mask-image:linear-gradient(180deg,#000 46%,transparent 80%)}
.a .cap{position:relative;margin-top:-150px;display:flex;flex-direction:column;align-items:center}
.a h2{font-size:clamp(30px,3.3vw,48px);line-height:1.14;max-width:23ch}
.a .rule{width:1px;height:44px;margin:30px 0 26px;background:rgba(131,58,34,.45)}
.a .body{max-width:48ch}
.a .role{margin-top:14px;max-width:none}
@media (max-width:980px){.a .stage{padding:0 0 76px}.a .fig{width:min(100%,400px)}.a .cap{margin-top:-80px}.a h2{font-size:clamp(28px,7.6vw,36px)}.a .rule{height:32px;margin:22px 0 20px}}
""", f"""<div class="wrap stage">
<figure class="fig"><img src="{DUO}" alt="{ALT}"></figure>
<div class="cap"><h2 class="disp" id="despre-h">Sunt Alessia și cred că <em>mâinile știu</em> uneori lucruri pe care mintea încă nu le-a spus.</h2>
<span class="rule" aria-hidden="true"></span><p class="body">{BODY}</p><span class="role">{ROLE}</span>{LINK}</div>
</div>""")

# B. Cover lines: the same sentence, set in three sizes like the lines beside a cover photo, flush against her silhouette.
OPTS["CopertaB"] = ("Coperta B: rânduri de copertă, ierarhie", """
.b .stage{display:grid;grid-template-columns:minmax(0,1fr) 470px minmax(0,1fr);gap:0 52px;min-height:790px}
.b .fig{grid-column:2;grid-row:1;align-self:end}
.b .l{grid-column:1;grid-row:1;align-self:start;padding-top:330px;margin-left:-40px;text-align:right}
.b h2 span{display:block}
.b h2 .s1{font-size:26px;line-height:1.3;font-style:italic;color:#6B5444}
.b h2 .s2{margin:8px -4px 16px 0;font-size:clamp(46px,4.4vw,66px);line-height:1;font-style:italic;color:var(--terra-d);white-space:nowrap}
.b h2 .s3{margin-left:auto;max-width:14ch;font-size:clamp(24px,2.1vw,31px);line-height:1.22}
.b .r{grid-column:3;grid-row:1;align-self:end;padding-bottom:150px;max-width:290px}
.b .r::before{content:"";display:block;width:40px;height:1px;margin-bottom:24px;background:var(--terra-d)}
.b .r .role{margin-bottom:12px}
@media (max-width:980px){.b .stage{grid-template-columns:1fr;min-height:0;padding-bottom:76px}.b .fig{grid-column:1;grid-row:1}.b .l{grid-column:1;grid-row:2;padding-top:0;margin-top:-20px;margin-left:0;text-align:left}.b h2 .s3{margin-left:0;max-width:18ch}.b h2 .s2{font-size:clamp(46px,13vw,60px);margin:6px 0 12px}.b .r{grid-column:1;grid-row:3;padding:30px 0 0;max-width:none}}
""", f"""<div class="wrap stage">
<figure class="fig fade"><img src="{DUO}" alt="{ALT}"></figure>
<div class="l"><h2 class="disp" id="despre-h"><span class="s1">{S1}</span> <span class="s2">{S2}</span> <span class="s3">{S3}</span></h2></div>
<div class="r"><span class="role">{ROLE}</span><p class="body">{BODY}</p>{LINK}</div>
</div>""")

# C. Clean cover, then an editorial band: name + portrait alone, the text in a wide row underneath, after a hairline.
OPTS["CopertaC"] = ("Coperta C: copertă curată, text dedesubt", """
.c .stage{display:flex;flex-direction:column}
.c .fig{width:520px;align-self:center;margin-top:150px}
.c .band{position:relative;display:grid;grid-template-columns:minmax(0,7fr) minmax(0,4fr);gap:72px;align-items:end;padding:52px 0 120px;border-top:1px solid rgba(58,42,32,.2)}
.c h2{font-size:clamp(32px,3.6vw,52px);line-height:1.12;max-width:20ch}
.c .role{margin-bottom:12px}
@media (max-width:980px){.c .fig{width:min(100%,420px);margin-top:9vw}.c .band{grid-template-columns:1fr;gap:22px;padding:30px 0 76px}.c h2{font-size:clamp(28px,7.6vw,36px)}}
""", f"""<div class="wrap stage">
<figure class="fig fade"><img src="{DUO}" alt="{ALT}"></figure>
<div class="band"><h2 class="disp" id="despre-h">Sunt Alessia și cred că <em>mâinile știu</em> uneori lucruri pe care mintea încă nu le-a spus.</h2>
<div><span class="role">{ROLE}</span><p class="body">{BODY}</p>{LINK}</div></div>
</div>""")

# D. Asymmetric cover: the name runs from the left, the portrait stands at the right over its last letters,
#    which leaves a real column for the text under the name.
OPTS["CopertaD"] = ("Coperta D: copertă asimetrică", """
.d .name{left:max(36px,calc(50% - 584px));transform:none}
.d .stage{display:grid;grid-template-columns:minmax(0,1fr) 500px;gap:0 64px;min-height:850px}
.d .fig{grid-column:2;grid-row:1;align-self:end}
.d .l{grid-column:1;grid-row:1;align-self:end;padding:0 0 128px}
.d h2{font-size:clamp(32px,3.5vw,50px);line-height:1.12;max-width:19ch}
.d .row{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:40px;align-items:end;margin-top:36px;padding-top:28px;border-top:1px solid rgba(58,42,32,.2)}
.d .role{margin-top:0}
@media (max-width:980px){.d .name{left:16px}.d .stage{grid-template-columns:1fr;min-height:0}.d .fig{grid-column:1;grid-row:1;width:min(88%,400px);margin:12vw 0 0 auto}.d .l{grid-row:2;margin-top:-16px;padding-bottom:76px}.d h2{font-size:clamp(28px,7.6vw,36px)}.d .row{grid-template-columns:1fr;gap:16px}}
""", f"""<div class="wrap stage">
<figure class="fig fade"><img src="{DUO}" alt="{ALT}"></figure>
<div class="l"><h2 class="disp" id="despre-h">Sunt Alessia și cred că <em>mâinile știu</em> uneori lucruri pe care mintea încă nu le-a spus.</h2>
<div class="row"><p class="body">{BODY}</p><div><span class="role">{ROLE}</span>{LINK}</div></div></div>
</div>""")

for name, (title, css, inner) in OPTS.items():
    cls = name[-1].lower()
    html = f'<section class="cv {cls}" id="despre" aria-labelledby="despre-h">\n<p class="name" aria-hidden="true">Alessia</p>\n{inner}\n</section>'
    for suffix, w, h in (("", 1440, 1000), ("Mobil", 390, 1100)):
        f = os.path.join(P, f"{name}{suffix}.dc.html")
        open(f, "w", encoding="utf-8").write(page(title + (" · mobil" if suffix else ""), False, COVER + css, html, w, h))
        if not suffix:
            subprocess.run([sys.executable, os.path.join(HERE, "dc2html.py"), f, os.path.join(HERE, f"opt-{name}.html")], check=True)
