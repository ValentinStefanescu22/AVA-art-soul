"""Pagina „Despre noi”, part 1: the opening (Alessia Văideanu, fondatoare + bio). Four directions, each from a named source.

usage: python3 .aidesigner/despre_noi_options.py
writes .aidesigner/canvas/project/DespreNoi1..4*.dc.html (+ Mobil twins) and local previews .aidesigner/opt-DespreNoi*.html
Copy: docs/continut-site.md, „Despre noi” → „Alessia Văideanu — fondatoare” (bio cleaned of the Google Docs bold).
The header is Header 1 (chosen for Acasă), shown static at the top of the page, with „Despre noi” as the current page.
"""
import os, re, subprocess, sys
from about_options2 import P, HERE, FONTS, BASE_CSS, BG, DUO, ALT, LIGHT_JS, STATIC_JS
from header_options import HX_CSS, V, header_html

NAME, ROLE = "Alessia Văideanu", "fondatoare"
LEDE = "Sunt Alessia, artist ceramist și consilier acreditat în dezvoltare personală."
BODY = ("Am absolvit Psihologia și acum sunt masterandă în terapii experiențiale și artterapie. Iubesc să creez evenimente "
        "în cadrul cărora oamenii își dau voie să fie prezenți și îi ajut să rămână curioși față de ce prinde formă din "
        "mâinile lor, fără presiune și fără să simtă că trebuie să „știe să facă”.")
# the brand's clay rings: two dark lines, one terracotta
RINGS = ('<svg class="orn" viewBox="0 0 120 34" aria-hidden="true">'
         + "".join(f'<path d="M4 {y}C19 {y-6} 34 {y-6} 49 {y}S79 {y+6} 94 {y}S112 {y-4} 116 {y}" style="stroke:{c}"></path>'
                   for y, c in ((9, "#3A2A20"), (17, "#B4583A"), (25, "#3A2A20")))
         + "</svg>")

SOURCES = {
    "DespreNoi1Revista": "Kinfolk (revista): paginile de profil",
    "DespreNoi2Muzeu": "Rijksmuseum (sălile cu pereți închiși) + etichetele de perete de la MoMA",
    "DespreNoi3Semnatura": "Apple: „hello” scris de mână (Macintosh 1984, iMac 2021)",
    "DespreNoi3BScrisoare": "Patagonia: scrisoarea semnată de Yvon Chouinard („Earth is now our only shareholder”, 2022)",
    "DespreNoi3CPolaroid": "Polaroid SX-70: fotografiile instant semnate pe banda albă",
    "DespreNoi3DLumina": "Gjon Mili, LIFE (1949): Picasso desenând cu lumina",
    "DespreNoi3EOlar": "Leach Pottery, St Ives: sigiliul olarului imprimat în lut",
    "DespreNoiDeschidere": "Despre noi 3D (Gjon Mili, LIFE 1949), fără semnătură și fără efectul de lumină",
    "DespreNoi4PaginaTitlu": "Giambattista Bodoni, Manuale Tipografico (1818): pagina de titlu și frontispiciul oval",
}

COMMON = """
.op{position:relative;overflow:hidden}
.op h1{margin:0}
.op .fond{display:block;font:italic 400 clamp(22px,2vw,28px)/1.2 var(--display);font-variation-settings:'opsz' 20;color:var(--terra-d)}
.op .lede{margin:0;font:400 clamp(21px,1.9vw,26px)/1.38 var(--display);font-variation-settings:'opsz' 20;text-wrap:pretty}
.op .body{margin-top:18px;color:var(--ink2);max-width:52ch}
.orn{display:block;width:96px;height:28px;fill:none;stroke-width:2.2px;stroke-linecap:round}
/* the signature writes itself once, left to right (a clip that opens). Pinyon Script stands in until we get her real one;
   the same clip works on an image of the real signature */
@keyframes dn-write{from{clip-path:inset(-30% 100% -30% -5%)}to{clip-path:inset(-30% -5% -30% -5%)}}
@media (prefers-reduced-motion:no-preference){.op .write{animation:dn-write 2.4s cubic-bezier(.5,.1,.3,1) 1.2s both}}
/* signature family (Vali, 11 nov: more motion): the name rises letter by letter out of a blur, the portrait is uncovered
   from the bottom up, then the signature writes itself; afterwards the portrait and the signature drift apart a little
   with the cursor (two depths, --mx/--my from a lerp) and a warm light follows it. All still with reduced motion. */
.op{--sp:cubic-bezier(.3,1.32,.5,1);--so:cubic-bezier(.22,1,.36,1)}
.nm .w{display:inline-block;white-space:nowrap}.nm .l{display:inline-block}
:is(.dns,.dnb,.dnc,.dnd,.dne)::before{content:"";position:absolute;inset:0;pointer-events:none;opacity:0;transition:opacity .8s ease;
  background:radial-gradient(circle 440px at var(--gx,70%) var(--gy,40%),rgba(255,222,180,.55),rgba(255,222,180,0) 70%);mix-blend-mode:soft-light}
.dnd::before{background:radial-gradient(circle 440px at var(--gx,70%) var(--gy,40%),rgba(255,196,140,.16),rgba(255,196,140,0) 70%);mix-blend-mode:screen}
:is(.dns,.dnb,.dnc,.dnd,.dne).lit::before{opacity:1}
:is(.dns,.dnb,.dnd,.dne) .fig{translate:calc(var(--mx,0) * -12px) calc(var(--my,0) * -8px)}
.dnc .fig{translate:calc(var(--mx,0) * -10px) calc(var(--my,0) * -8px)}
:is(.dns,.dnb) .sig,.dnd .sigw,.dne .seal{translate:calc(var(--mx,0) * 20px) calc(var(--my,0) * 12px)}
.dnc .ph::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,#DCD6C8,#CEC6B5);opacity:0;pointer-events:none}
@media (prefers-reduced-motion:no-preference){
  .nm .l{animation:dn-l 1s var(--so) backwards;animation-delay:calc(.1s + var(--k) * 40ms)}
  :is(.dns,.dnb,.dnd,.dne) .fig>img{animation:dn-rise 1.5s var(--so) .2s backwards}
  .dnc .fig{animation:dn-drop 1.2s var(--sp) .25s backwards}
  .dnc .ph::after{animation:dn-dev 3.2s ease-out .7s backwards}
  .dnc .write{animation-delay:2.6s}
  .dne .seal{animation:dn-press .9s var(--sp) 1.3s backwards}
  .dne .write{animation-delay:2s}
}
@keyframes dn-l{from{opacity:0;translate:0 .45em;filter:blur(8px)}}
@keyframes dn-rise{from{clip-path:inset(100% 0 0 0);translate:0 40px}to{clip-path:inset(0 0 0 0)}}
@keyframes dn-drop{from{opacity:0;translate:60px -70px;rotate:16deg}}
@keyframes dn-dev{from{opacity:1}to{opacity:0}}
@keyframes dn-press{from{opacity:0;scale:1.5;box-shadow:0 60px 60px -20px rgba(58,30,15,.4)}}
/* one quiet entrance when the page opens: fade + rise 16px, 80ms apart */
@keyframes dn-up{from{opacity:0;translate:0 16px}to{opacity:1;translate:none}}
@media (prefers-reduced-motion:no-preference){.op .a1,.op .a2,.op .a3,.op .a4{animation:dn-up .8s cubic-bezier(.22,1,.36,1) backwards}
.op .a2{animation-delay:.08s}.op .a3{animation-delay:.16s}.op .a4{animation-delay:.24s}}
"""

OPTS = {}

# 1. Revista: a Kinfolk profile spread. Name set large in two lines, a drop cap on the first sentence,
#    the portrait in a tall sand panel with her head breaking out of its top edge.
OPTS["DespreNoi1Revista"] = ("Despre noi 1: profil de revistă", "light", """
.dnr{background:linear-gradient(180deg,#F4EDE4 0%,#EFE4D4 100%);padding:168px 0 112px}
.dnr .stage{display:grid;grid-template-columns:minmax(0,1.08fr) minmax(0,.92fr);grid-template-areas:"head fig" "txt fig";gap:0 88px;align-items:end}
.dnr .head{grid-area:head;align-self:start;padding-top:40px}
.dnr h1{font:400 clamp(64px,8.4vw,124px)/.92 var(--display);font-variation-settings:'opsz' 72;letter-spacing:-.025em}
.dnr h1 span{display:block}.dnr h1 span+span{padding-left:.86em}
.dnr .fond{margin:28px 0 0 .12em}
.dnr .txt{grid-area:txt;max-width:540px;margin-top:64px;padding-top:34px;border-top:1px solid rgba(58,42,32,.2)}
.dnr .lede::first-letter{float:left;font-size:2.95em;line-height:.8;margin:.1em .1em 0 -.02em;color:var(--terra)}
.dnr .fig{grid-area:fig;position:relative;margin:96px 0 0;aspect-ratio:4/5}
.dnr .fig::before{content:"";position:absolute;inset:0;border-radius:30px;corner-shape:squircle;background:radial-gradient(ellipse 70% 55% at 50% 32%,#F5EADB 0%,rgba(245,234,219,0) 72%),linear-gradient(180deg,#E6D5BD 0%,#D8BD9B 100%)}
.dnr .fig img{position:absolute;left:50%;bottom:0;width:112%;translate:-50% 0;clip-path:inset(-60% 5.4% 0 5.4% round 0 0 30px 30px)}
@media (max-width:980px){.dnr{padding:112px 0 72px}.dnr .stage{grid-template-columns:1fr;grid-template-areas:"head" "fig" "txt"}.dnr .head{padding-top:0}.dnr h1{font-size:clamp(54px,15vw,84px)}.dnr .fond{margin-top:18px}.dnr .fig{margin:72px 0 0;width:min(100%,420px);justify-self:center}.dnr .txt{margin-top:40px;padding-top:28px}}
""", """<section class="op dnr" aria-labelledby="dn-h">
<div class="wrap stage">
<div class="head"><h1 class="disp a1" id="dn-h"><span>Alessia</span><span>Văideanu</span></h1><span class="fond a2">@ROLE@</span></div>
<figure class="fig a2"><img src="@DUO@" alt="@ALT@"></figure>
<div class="txt a3"><p class="lede">@LEDE@</p><p class="body">@BODY@</p></div>
</div>
</section>""")

# 2. Muzeu: the portrait hangs on a dark warm wall like a painting (Rijksmuseum), with a MoMA-style wall label beside it.
#    The name is the exhibition title painted on the wall. The woodsprite is the gallery spotlight; it follows the cursor.
OPTS["DespreNoi2Muzeu"] = ("Despre noi 2: sala de muzeu", "dark", """
.dnm{background:radial-gradient(ellipse 30% 50% at 60% 30%,rgba(255,214,170,.13) 0%,rgba(255,214,170,0) 70%),linear-gradient(180deg,#311E14 0%,#25160F 100%);color:#F4EDE4;padding:176px 0 132px}
.dnm .stage{position:relative;z-index:2;display:grid;grid-template-columns:minmax(0,1fr) 400px 316px;gap:0 52px;align-items:end}
.dnm .head{align-self:start}
.dnm h1{font:400 clamp(56px,5.2vw,76px)/.98 var(--display);font-variation-settings:'opsz' 60;letter-spacing:-.02em;color:#F4EDE4}
.dnm h1 span{display:block}
.dnm .fond{margin-top:22px;color:var(--glowc)}
.dnm .frame{margin:0;padding:18px;background:linear-gradient(135deg,#5B3A27,#3F271A);box-shadow:inset 0 0 0 1px rgba(255,220,180,.14),inset 0 1px 0 rgba(255,220,180,.18),0 40px 70px -30px rgba(0,0,0,.85),0 8px 18px -8px rgba(0,0,0,.6)}
.dnm .mat{padding:30px;background:#EFE4D4;box-shadow:inset 0 2px 7px rgba(40,20,10,.28)}
.dnm .pic{position:relative;aspect-ratio:3/4;overflow:hidden;background:radial-gradient(ellipse 70% 55% at 50% 30%,#F3E7D6 0%,rgba(243,231,214,0) 72%),linear-gradient(180deg,#E6D5BD 0%,#D4B894 100%)}
.dnm .pic img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 0}
.dnm .lab{margin-bottom:6px;padding:24px 24px 26px;background:#F4EDE4;color:var(--ink);font-size:15px;line-height:1.55;box-shadow:0 18px 30px -18px rgba(0,0,0,.7)}
.dnm .lab .who{margin:0;font-weight:600;font-size:16px}
.dnm .lab .rl{margin:0 0 16px;color:var(--ink2)}
.dnm .lab .lede{font:500 15px/1.55 var(--text)}
.dnm .lab .body{margin-top:10px;font-size:15px}
@media (max-width:1180px){.dnm .stage{grid-template-columns:minmax(0,1fr) 340px 290px;gap:0 36px}}
@media (max-width:980px){.dnm{padding:112px 0 80px}.dnm .stage{grid-template-columns:1fr;gap:0}.dnm h1{font-size:clamp(50px,14vw,76px)}.dnm .frame{width:min(100%,320px);justify-self:center;margin-top:56px;padding:14px}.dnm .mat{padding:20px}.dnm .lab{margin-top:40px}}
""", """<section class="op dnm" aria-labelledby="dn-h" ref="{{ secRef }}" onPointerMove="{{ onMove }}" onPointerLeave="{{ onLeave }}">
<div class="glow" aria-hidden="true"></div>
<span class="sprite" aria-hidden="true" ref="{{ spriteRef }}"></span>
<div class="wrap stage">
<div class="head"><h1 class="disp a1" id="dn-h"><span>Alessia</span><span>Văideanu</span></h1><span class="fond a2">@ROLE@</span></div>
<figure class="frame a2" ref="{{ anchorRef }}" data-ax=".5" data-ay=".22" data-wr=".45"><div class="mat"><div class="pic"><img src="@DUO@" alt="@ALT@"></div></div></figure>
<div class="lab a3"><p class="who">@NAME@</p><p class="rl">@ROLE@</p><p class="lede">@LEDE@</p><p class="body">@BODY@</p></div>
</div>
</section>""")

# 3. Semnătura: Apple's handwritten "hello". Her first name writes itself once in Pinyon Script across the portrait,
#    like a signature on a photograph (left to right, a clip that opens; nothing moves with reduced motion).
OPTS["DespreNoi3Semnatura"] = ("Despre noi 3: semnătura", "light", """
.dns{background:radial-gradient(ellipse 42% 60% at 72% 42%,#F9F2E8 0%,rgba(249,242,232,0) 70%),linear-gradient(180deg,#F4EDE4 0%,#EADCC7 100%);padding:150px 0 0}
.dns .stage{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,540px);grid-template-areas:"head fig" "txt fig";gap:0 72px;min-height:780px}
.dns .head{grid-area:head;align-self:end}
.dns h1{font:400 clamp(52px,5.8vw,86px)/1 var(--display);font-variation-settings:'opsz' 48;letter-spacing:-.02em}
.dns .fond{margin-top:16px}
.dns .txt{grid-area:txt;align-self:start;max-width:540px;margin-top:44px;padding-bottom:120px}
.dns .fig{grid-area:fig;position:relative;margin:0;align-self:end}
.dns .fig img{display:block;width:100%;-webkit-mask-image:linear-gradient(180deg,#000 78%,transparent 99%);mask-image:linear-gradient(180deg,#000 78%,transparent 99%)}
.dns .sig{position:absolute;left:-30%;bottom:15%;margin:0;font:400 clamp(130px,14vw,210px)/1.2 var(--script);color:var(--terra);rotate:-8deg;white-space:nowrap;pointer-events:none;user-select:none;text-shadow:0 1px 0 rgba(255,248,238,.6)}
@media (max-width:980px){.dns{padding:112px 0 0}.dns .stage{grid-template-columns:1fr;grid-template-areas:"head" "fig" "txt";min-height:0}.dns h1{font-size:clamp(46px,13vw,68px)}.dns .fig{width:min(100%,420px);justify-self:center;margin-top:28px}.dns .sig{left:-6%;bottom:9%;font-size:clamp(96px,30vw,150px)}.dns .txt{margin-top:8px;padding-bottom:76px}}
""", """<section class="op dns" aria-labelledby="dn-h" ref="{{ secRef }}">
<div class="wrap stage">
<div class="head">@NAMESPLIT@<span class="fond a2">@ROLE@</span></div>
<figure class="fig a2"><img src="@DUO@" alt="@ALT@"><p class="sig write" aria-hidden="true">Alessia</p></figure>
<div class="txt a3"><p class="lede">@LEDE@</p><p class="body">@BODY@</p></div>
</div>
</section>""")

FAM = """
.@C@ .stage{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,540px);grid-template-areas:"head fig" "txt fig";gap:0 72px;min-height:780px}
.@C@ .head{grid-area:head;align-self:end}
.@C@ h1{font:400 clamp(52px,5.8vw,86px)/1 var(--display);font-variation-settings:'opsz' 48;letter-spacing:-.02em}
.@C@ .fond{margin-top:16px}
.@C@ .txt{grid-area:txt;align-self:start;max-width:540px;margin-top:44px;padding-bottom:120px}
.@C@ .fig{grid-area:fig;position:relative;margin:0;align-self:end}
.@C@ .fig>img{display:block;width:100%;-webkit-mask-image:linear-gradient(180deg,#000 78%,transparent 99%);mask-image:linear-gradient(180deg,#000 78%,transparent 99%)}
.@C@ .sig{margin:0;font-family:var(--script);font-weight:400;white-space:nowrap;pointer-events:none;user-select:none}
@media (max-width:980px){.@C@{padding-top:112px!important}.@C@ .stage{grid-template-columns:1fr;grid-template-areas:"head" "fig" "txt";min-height:0}.@C@ h1{font-size:clamp(46px,13vw,68px)}.@C@ .fig{width:min(100%,420px);justify-self:center;margin-top:28px}.@C@ .txt{margin-top:8px;padding-bottom:76px}}
"""
HEAD = '<div class="head">@NAMESPLIT@<span class="fond a2">@ROLE@</span></div>'
TXT = '<div class="txt a3"><p class="lede">@LEDE@</p><p class="body">@BODY@</p>'

# 3B. Scrisoarea: the bio is a short letter; she signs it underneath, the way Chouinard signed Patagonia's 2022 letter.
OPTS["DespreNoi3BScrisoare"] = ("Despre noi 3B: semnătura sub text", "light", FAM.replace("@C@", "dnb") + """
.dnb{background:radial-gradient(ellipse 42% 60% at 72% 42%,#F9F2E8 0%,rgba(249,242,232,0) 70%),linear-gradient(180deg,#F4EDE4 0%,#EADCC7 100%);padding:150px 0 0}
.dnb .sig{display:inline-block;margin:26px 0 0 -4px;font-size:clamp(84px,8vw,118px);line-height:1.15;color:var(--terra);rotate:-5deg;transform-origin:0 60%}
@media (max-width:980px){.dnb .sig{font-size:84px;margin-top:14px}}
""", '<section class="op dnb" aria-labelledby="dn-h" ref="{{ secRef }}"><div class="wrap stage">' + HEAD
   + '<figure class="fig a2"><img src="@DUO@" alt="@ALT@"></figure>'
   + TXT + '<p class="sig write" aria-hidden="true">Alessia</p></div></div></section>')

# 3C. Polaroid: the portrait is an instant print, tilted on the page; she signs the white strip, like a signed Polaroid.
OPTS["DespreNoi3CPolaroid"] = ("Despre noi 3C: polaroid semnat", "light", FAM.replace("@C@", "dnc") + """
.dnc{background:radial-gradient(ellipse 40% 55% at 72% 45%,#F9F2E8 0%,rgba(249,242,232,0) 70%),linear-gradient(180deg,#F4EDE4 0%,#EADCC7 100%);padding:150px 0 0}
@media (min-width:981px){.dnc .stage{grid-template-columns:minmax(0,1fr) 460px;min-height:740px}}
.dnc .fig{align-self:center;padding:20px 20px 0;background:#FBF7F0;rotate:3deg;box-shadow:0 1px 1px rgba(58,42,32,.08),0 30px 50px -24px rgba(58,42,32,.5),0 8px 16px -10px rgba(58,42,32,.3);transition:rotate .3s cubic-bezier(.2,.7,.2,1)}
@media (hover:hover){.dnc .fig:hover{rotate:1deg}}
.dnc .ph{position:relative;aspect-ratio:1/1.05;overflow:hidden;background:radial-gradient(ellipse 70% 55% at 50% 30%,#F3E7D6 0%,rgba(243,231,214,0) 72%),linear-gradient(180deg,#E6D5BD 0%,#D4B894 100%);box-shadow:inset 0 0 0 1px rgba(58,42,32,.08)}
.dnc .ph img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 0}
.dnc .strip{display:flex;align-items:center;justify-content:center;height:112px}
.dnc .sig{font-size:78px;line-height:1.2;color:var(--ink);rotate:-4deg}
.dnc .txt{padding-bottom:140px}
@media (max-width:980px){.dnc .fig{width:min(86%,360px);margin-top:36px;padding:14px 14px 0}.dnc .strip{height:84px}.dnc .sig{font-size:60px}.dnc .txt{margin-top:40px;padding-bottom:76px}}
""", '<section class="op dnc" aria-labelledby="dn-h" ref="{{ secRef }}"><div class="wrap stage">' + HEAD
   + '<figure class="fig a2"><div class="ph"><img src="@DUO@" alt="@ALT@"></div><div class="strip"><p class="sig write" aria-hidden="true">Alessia</p></div></figure>'
   + TXT + '</div></div></section>')

# 3D. Lumina: dark, like Mili's photos of Picasso drawing with a light pen. The woodsprite is the pen:
#     it runs ahead of the signature and leaves it behind as warm light, then fades.
OPTS["DespreNoi3DLumina"] = ("Despre noi 3D: semnătura scrisă cu lumină", "dark", FAM.replace("@C@", "dnd") + """
.dnd{background:radial-gradient(ellipse 40% 55% at 72% 45%,rgba(255,200,150,.11) 0%,rgba(255,200,150,0) 70%),linear-gradient(180deg,#2E1C13 0%,#22140D 100%);color:#F4EDE4;padding:150px 0 0}
.dnd h1{color:#F4EDE4}.dnd .fond{color:var(--glowc)}.dnd .lede{color:#EFE3D3}.dnd .body{color:#D8C6B2}
.dnd .fig>img{-webkit-mask-image:radial-gradient(ellipse 80% 70% at 50% 34%,#000 58%,transparent 100%);mask-image:radial-gradient(ellipse 80% 70% at 50% 34%,#000 58%,transparent 100%)}
.dnd .sigw{position:absolute;left:-30%;bottom:15%;rotate:-8deg}
.dnd .sig{font-size:clamp(130px,14vw,210px);line-height:1.2;color:#FFF1DC;text-shadow:0 0 5px rgba(255,232,200,.95),0 0 18px rgba(255,186,120,.7),0 0 46px rgba(214,120,60,.5)}
.dnd .pen{position:absolute;left:0;top:55%;width:10px;height:10px;margin:-5px 0 0 -5px;border-radius:50%;opacity:0;pointer-events:none;background:radial-gradient(circle,#FFFDF6 0 35%,rgba(255,246,228,.9) 52%,rgba(255,236,206,0) 74%);box-shadow:0 0 16px 6px rgba(255,250,238,.85),0 0 60px 26px rgba(255,214,160,.45)}
@keyframes dn-pen{0%{left:2%;top:70%;opacity:0}6%{opacity:1}18%{top:24%}32%{top:72%}46%{top:38%}60%{top:66%}76%{top:36%}92%{opacity:1}100%{left:99%;top:52%;opacity:0}}
@media (prefers-reduced-motion:no-preference){.dnd .pen{animation:dn-pen 2.4s cubic-bezier(.5,.1,.3,1) 1.2s both}}
@media (max-width:980px){.dnd .sigw{left:-6%;bottom:9%}.dnd .sig{font-size:clamp(96px,30vw,150px)}}
""", '<section class="op dnd" aria-labelledby="dn-h" ref="{{ secRef }}"><div class="wrap stage">' + HEAD
   + '<figure class="fig a2"><img src="@DUO@" alt="@ALT@"><div class="sigw" aria-hidden="true"><p class="sig write">Alessia</p><span class="pen"></span></div></figure>'
   + TXT + '</div></div></section>')

# 3E. Olarul: potters press their seal into the clay near the foot of a piece (Leach Pottery's St Ives mark).
#     Her signature is pressed into a disc of the hero's clay, laid against the portrait.
OPTS["DespreNoi3EOlar"] = ("Despre noi 3E: semnătura imprimată în lut", "light", FAM.replace("@C@", "dne") + """
.dne{background:radial-gradient(ellipse 42% 60% at 72% 42%,#F9F2E8 0%,rgba(249,242,232,0) 70%),linear-gradient(180deg,#F4EDE4 0%,#EADCC7 100%);padding:150px 0 0}
.dne .seal{position:absolute;left:-15%;bottom:14%;width:250px;aspect-ratio:1;display:grid;place-items:center;border-radius:50%;overflow:hidden;rotate:-8deg;background:url(@BG@) 40% 60%/360% no-repeat;box-shadow:inset 0 -12px 26px rgba(40,15,5,.42),inset 0 8px 18px rgba(255,200,160,.16),inset 0 0 0 1px rgba(255,220,190,.14),0 24px 38px -18px rgba(58,30,15,.62),0 4px 8px -4px rgba(58,30,15,.4)}
.dne .seal::before{content:"";position:absolute;inset:15px;border-radius:50%;box-shadow:inset 1.5px 1.5px 2px rgba(20,6,2,.5),1px 1px 0 rgba(255,214,180,.28)}
.dne .sig{position:relative;font-size:94px;line-height:1.25;color:rgba(52,20,9,.66);rotate:-6deg;text-shadow:1px 1.5px 0 rgba(255,206,168,.34),-1px -1px 1px rgba(20,6,2,.5)}
@media (max-width:980px){.dne .seal{left:-3%;bottom:8%;width:168px}.dne .seal::before{inset:10px}.dne .sig{font-size:64px}}
""", '<section class="op dne" aria-labelledby="dn-h" ref="{{ secRef }}"><div class="wrap stage">' + HEAD
   + '<figure class="fig a2"><img src="@DUO@" alt="@ALT@"><div class="seal" aria-hidden="true"><p class="sig write">Alessia</p></div></figure>'
   + TXT + '</div></div></section>')


# Deschiderea aleasă (Vali, 11 nov, feedback de la Alessia): 3D without the signature and without any light (no pen,
# no glow, no warm halo in the background). The portrait sits in a plain rectangle: no border, no frame, no shadow.
OPTS["DespreNoiDeschidere"] = ("Despre noi: deschiderea (din 3D, fără semnătură și fără lumină)", "dark", FAM.replace("@C@", "dnh") + """
.dnh{background:linear-gradient(180deg,#2E1C13 0%,#22140D 100%);color:#F4EDE4;padding:150px 0 120px}
.dnh h1{color:#F4EDE4}.dnh .fond{color:var(--glowc)}.dnh .lede{color:#EFE3D3}.dnh .body{color:#D8C6B2}
.dnh .stage{min-height:0;align-items:center}
.dnh .head{align-self:end}
.dnh .txt{padding-bottom:0}
.dnh .fig{align-self:center;overflow:hidden}
.dnh .fig>img{aspect-ratio:4/5;object-fit:cover;object-position:50% 6%;-webkit-mask-image:none;mask-image:none;background:linear-gradient(180deg,#E6D5BD 0%,#D4B894 100%)}
@media (prefers-reduced-motion:no-preference){.dnh .fig>img{animation:dn-rise 1.5s var(--so) .2s backwards}}
@media (max-width:980px){.dnh{padding-bottom:76px!important}.dnh .txt{margin-top:32px;padding-bottom:0}}
""", '<section class="op dnh" aria-labelledby="dn-h"><div class="wrap stage">' + HEAD
   + '<figure class="fig a2"><img src="@DUO@" alt="@ALT@"></figure>'
   + TXT + '</div></div></section>')

# 4. Pagina de titlu: Bodoni's Manuale Tipografico. Symmetry, a double-rule border, an oval frontispiece portrait,
#    the brand's clay rings as the fleuron between title and text. Bodoni Moda is the site's display face, so it fits.
OPTS["DespreNoi4PaginaTitlu"] = ("Despre noi 4: pagina de titlu", "light", """
.dnt{background:#F4EDE4;padding:132px 0 96px}
.dnt .page{position:relative;max-width:980px;margin:0 auto;padding:76px 64px 84px;box-sizing:border-box;text-align:center;border:1px solid rgba(58,42,32,.42)}
.dnt .page::before{content:"";position:absolute;inset:7px;border:1px solid rgba(58,42,32,.22);pointer-events:none}
.dnt .oval{position:relative;width:250px;height:328px;margin:0 auto;border-radius:50%;overflow:hidden;background:radial-gradient(ellipse 70% 55% at 50% 34%,#F3E7D6 0%,rgba(243,231,214,0) 72%),linear-gradient(180deg,#E6D5BD 0%,#D4B894 100%);box-shadow:0 0 0 8px #F4EDE4,0 0 0 9px rgba(156,71,44,.7),0 0 0 13px #F4EDE4,0 0 0 14px rgba(156,71,44,.35)}
.dnt .oval img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 6%}
.dnt h1{margin-top:60px;font:400 clamp(46px,6vw,86px)/1 var(--display);font-variation-settings:'opsz' 48;letter-spacing:.01em}
.dnt .fond{margin-top:14px}
.dnt .orn{margin:36px auto}
.dnt .lede{max-width:32ch;margin:0 auto;font-style:italic}
.dnt .body{margin:18px auto 0;max-width:54ch;text-wrap:balance}
@media (max-width:980px){.dnt{padding:96px 0 48px}.dnt .wrap{padding:0 12px}.dnt .page{padding:52px 22px 60px}.dnt .oval{width:196px;height:258px}.dnt h1{margin-top:44px;font-size:clamp(40px,11.6vw,60px)}.dnt .orn{margin:28px auto}.dnt .body{text-wrap:pretty}}
""", """<section class="op dnt" aria-labelledby="dn-h">
<div class="wrap"><div class="page">
<figure class="oval a1" style="margin: 0 auto"><img src="@DUO@" alt="@ALT@"></figure>
<h1 class="disp a2" id="dn-h">@NAME@</h1><span class="fond a2">@ROLE@</span>
<div class="a3">@RINGS@</div>
<div class="a4"><p class="lede">@LEDE@</p><p class="body">@BODY@</p></div>
</div></div>
</section>""")


MOTION_JS = """class Component extends DCLogic {
  componentDidMount() {
    var s = this.sec; if (!s || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    var c = { x: 0, y: 0, gx: 0, gy: 0 }, t = { x: 0, y: 0, gx: 0, gy: 0 }, raf = 0, first = true;
    var step = function () {
      raf = 0;
      c.x += (t.x - c.x) * 0.07; c.y += (t.y - c.y) * 0.07; c.gx += (t.gx - c.gx) * 0.12; c.gy += (t.gy - c.gy) * 0.12;
      s.style.setProperty('--mx', c.x.toFixed(3)); s.style.setProperty('--my', c.y.toFixed(3));
      s.style.setProperty('--gx', c.gx.toFixed(1) + 'px'); s.style.setProperty('--gy', c.gy.toFixed(1) + 'px');
      if (Math.abs(t.x - c.x) + Math.abs(t.y - c.y) + Math.abs(t.gx - c.gx) / 100 + Math.abs(t.gy - c.gy) / 100 > 0.002) raf = requestAnimationFrame(step);
    };
    this.move = function (e) {
      if (e.pointerType !== 'mouse') return;
      var r = s.getBoundingClientRect();
      t.x = (e.clientX - r.left) / r.width * 2 - 1; t.y = (e.clientY - r.top) / r.height * 2 - 1;
      t.gx = e.clientX - r.left; t.gy = e.clientY - r.top;
      if (first) { c.gx = t.gx; c.gy = t.gy; first = false; }
      s.classList.add('lit'); if (!raf) raf = requestAnimationFrame(step);
    };
    this.leave = function () { t.x = 0; t.y = 0; s.classList.remove('lit'); if (!raf) raf = requestAnimationFrame(step); };
    s.addEventListener('pointermove', this.move); s.addEventListener('pointerleave', this.leave);
  }
  componentWillUnmount() { if (this.sec && this.move) { this.sec.removeEventListener('pointermove', this.move); this.sec.removeEventListener('pointerleave', this.leave); } }
  renderVals() { var self = this; if (!this.cb) this.cb = { secRef: function (el) { self.sec = el; } }; return this.cb; }
}"""


def header(tone):
    """Header 1 as it sits at the top of a page that has no 'next workshop' strip: static, no handlers."""
    h = header_html("1").replace('data-tone="dark"', f'data-tone="{tone}"').replace('ref="{{ hxRef }}"', 'style="--y: 42px"')
    h = re.sub(r'\s(?:on[A-Z]\w+|ref)="\{\{[^}]*\}\}"', "", h)
    h = h.replace(' aria-current="page"', "", 1).replace('<a href="#despre">', '<a href="#despre" aria-current="page">', 1)
    assert 'aria-current="page">Despre noi' in h
    return h


def name_split():
    """the h1 as words of letters, so each letter can rise on its own; screen readers get the plain name"""
    k, out = 0, []
    for w in NAME.split():
        ls = []
        for ch in w:
            ls.append(f'<span class="l" style="--k: {k}">{ch}</span>'); k += 1
        out.append('<span class="w" aria-hidden="true">' + "".join(ls) + "</span>")
    return f'<h1 class="disp nm" id="dn-h" aria-label="{NAME}">' + " ".join(out) + "</h1>"


def fill(s):
    s = s.replace("@NAMESPLIT@", name_split())
    for k, v in dict(NAME=NAME, ROLE=ROLE, LEDE=LEDE, BODY=BODY, DUO=DUO, ALT=ALT, RINGS=RINGS, BG=BG).items():
        s = s.replace(f"@{k}@", v)
    return s


def page(name, title, tone, css, html, w, h):
    src = SOURCES[name]
    return f"""<!doctype html>
<html lang="ro">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
{FONTS}
<style>
{BASE_CSS}{HX_CSS}{V["1Pastila"]["css"]}{COMMON}{fill(css)}</style>
</helmet>
<div class="pg hxv v1" data-src="{src}">
{header(tone)}
{fill(html)}
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{w},"height":{h}}}}}'>
{MOTION_JS if name.startswith("DespreNoi3") else LIGHT_JS if "secRef" in html else STATIC_JS}
</script>
</body>
</html>
"""


# preview heights, measured in the browser (desktop 1440, phone 390)
H = {"DespreNoi1Revista": (1000, 1210), "DespreNoi2Muzeu": (810, 1225), "DespreNoi3Semnatura": (930, 1130), "DespreNoi4PaginaTitlu": (1240, 1100),
     "DespreNoi3BScrisoare": (930, 1241), "DespreNoi3CPolaroid": (890, 1118), "DespreNoi3DLumina": (930, 1130), "DespreNoi3EOlar": (930, 1130), "DespreNoiDeschidere": (945, 1125)}

if __name__ == "__main__":
    for name, (title, tone, css, html) in OPTS.items():
        for suffix, w, h in (("", 1440, H[name][0]), ("Mobil", 390, H[name][1])):
            f = os.path.join(P, f"{name}{suffix}.dc.html")
            open(f, "w", encoding="utf-8").write(page(name, title + (" · mobil" if suffix else ""), tone, css, html, w, h))
            if not suffix:
                subprocess.run([sys.executable, os.path.join(HERE, "dc2html.py"), f, os.path.join(HERE, f"opt-{name}.html")], check=True)
        print("wrote", name)
