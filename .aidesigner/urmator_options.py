"""Acasă, block 'Următorul atelier' as an Instagram-style story (Vali, 10 nov: the story idea from the
'Cum arată un atelier' round moves here; that block is dropped). Four ways to stage the same story:
A Bilet          story beside the event's details, like a ticket.
B Vizualizator   the story in the middle, the frames before and after it on the sides, the page tinted by the photo.
C Highlights     round 'highlights' you tap to jump to a frame, as on an Instagram profile.
D Data mare      the date set huge behind the story (like the name on 'Cine sunt'), with a live countdown sticker.
Copy: docs/continut-site.md, 'Evenimente' (card for 15 noiembrie). The description is split across the frames, word for word.

usage: python3 .aidesigner/urmator_options.py
writes .aidesigner/canvas/project/Urmatorul{A..D}*.dc.html (+ Mobil twins), previews .aidesigner/opt-Urmatorul*.html,
comparison pages .aidesigner/urmator.html and urmator-mobil.html
"""
import os, subprocess, sys
from about_options2 import P, HERE, FONTS, BASE_CSS, ARROW

SOURCES = {
    "UrmatorulA": ("Framer: Instagram Story; Framer: StoryCard", "https://www.framer.com/marketplace/components/instagram-story/"),
    "UrmatorulB": ("Instagram pe web (story-ul din mijloc, vecinii pe laturi); Framer: Story Slider",
                   "https://www.framer.com/marketplace/components/story-slider/"),
    "UrmatorulC": ("Instagram: Highlights; Framer: Story Section", "https://www.framer.com/marketplace/components/story-section/"),
    "UrmatorulD": ("Instagram: stickerul Countdown; Framer: Instagram Stories", "https://www.framer.com/marketplace/components/instagram-stories"),
}

# ---------- copy (docs/continut-site.md, Evenimente) ----------
H = "Următorul atelier"
TITLE = "Atelier de ceramică &amp; socializare"
DATE = "15 noiembrie 2026, duminică, ora 17:00 (3 ore)"
WHERE = "Cotroceni, sector 5"
PRICE = "200 lei"
PRICE_NOTE = "include toate materialele, îndrumarea și o băutură și o gustare făcute în casă."
SEATS = "Doar 8 locuri, rezervă-ți locul acum"
WHO = "Alessia, AVA Art &amp; Soul"
CTA = "Mă înscriu"
# the description, split across frames 1-3 word for word; frame 4 is the price line's last sentence
FRAMES = [
    ("cover", None),
    ("t", "O seară liniștită cu lut, culoare și oameni noi. Modelăm împreună,"),
    ("t", "apoi îți pictezi piesa cu underglaze, culori speciale pentru ceramică,"),
    ("t", "iar între timp povestim și ne bucurăm de o băutură și o gustare făcute în casă."),
    ("end", "Piesa modelată și pictată de tine rămâne a ta, după ardere."),
]
HL = ["15 nov", "Modelăm", "Pictăm", "Povestim", "Piesa ta"]

# ---------- images ----------
ATELIER = "/_blob/988e3a505fd5ae1db56d481b3d1e33b1"   # real, October workshop, 2000x1500
REAL_BOL = "/_blob/42c18be93cd80d91d6d1d16793e790c6"  # real, two guests passing a clay bowl
PICTAT = "/_blob/dad600a42f9bdc35b94ba47b4a49fc4a"    # placeholder (Unsplash): painting a bowl with underglaze
PIESE = "/_blob/74f239bfbd557a0a5a661ddd26484b66"     # placeholder (Unsplash): finished bowls
STAMP = "/_blob/61696ece195f787b8ccb139b396a6450"     # alessia-stamp, square
IMGS = [(ATELIER, "Masa atelierului din octombrie: oameni care lucrează lutul, cu ceai și prăjitură", "62% 50%"),
        (REAL_BOL, "Doi participanți își dau din mână în mână un bol de lut, la atelierul din octombrie", "40% 50%"),
        (PICTAT, "O femeie pictează un bol de ceramică cu pensula (fotografie provizorie)", "42% 50%"),
        (ATELIER, "Prăjitură făcută în casă și căni pe masa atelierului din octombrie", "52% 60%"),
        (PIESE, "Boluri de ceramică arse, în culori diferite (fotografie provizorie)", "50% 50%")]
N = len(FRAMES)
LINK_ICON = '<svg class="li" viewBox="0 0 16 16" aria-hidden="true"><path d="M6.5 9.5l3-3M7 4.5l1-1a2.5 2.5 0 013.5 3.5l-1 1M9 11.5l-1 1A2.5 2.5 0 014.5 9l1-1" fill="none" stroke="currentColor" style="stroke-width:1.5;stroke-linecap:round"></path></svg>'


def story(countdown=False):
    imgs = "".join(f'<img class="i{k}" src="{s}" alt="{a}" style="object-position:{p}">' for k, (s, a, p) in enumerate(IMGS))
    bars = "".join(f'<span class="bar b{k}"><i></i></span>' for k in range(N))
    cd = ('<div class="cd" aria-label="Timp rămas până la atelier"><span class="cdt">Până la atelier</span><span class="cdn">'
          '<span><b data-u="d">00</b><i>zile</i></span><span><b data-u="h">00</b><i>ore</i></span><span><b data-u="m">00</b><i>min</i></span>'
          '</span></div>') if countdown else ""
    frs = []
    for k, (kind, text) in enumerate(FRAMES):
        if kind == "cover":
            frs.append(f'<div class="fr f{k} cover">{cd}<p class="k">duminică · 15 noiembrie · ora 17:00</p><p class="t">{TITLE}</p><p class="w">{WHERE}</p></div>')
        elif kind == "end":
            frs.append(f'<div class="fr f{k}"><p class="t">{text}</p><p class="w">{PRICE} · {SEATS}</p>'
                       f'<a class="stk" href="#inscriere">{LINK_ICON}{CTA}</a></div>')
        else:
            frs.append(f'<div class="fr f{k}"><p class="t">{text}</p></div>')
    return (f'<div class="sy" onPointerDown="{{{{ hold }}}}" onPointerUp="{{{{ release }}}}" onPointerLeave="{{{{ release }}}}" '
            f'onPointerCancel="{{{{ release }}}}">'
            f'<div class="ph">{imgs}</div><span class="shade" aria-hidden="true"></span>'
            f'<div class="bars" aria-hidden="true">{bars}</div>'
            f'<div class="who" aria-hidden="true"><img src="{STAMP}" alt="">ava.art.soul <span>· 15 nov</span></div>'
            f'<button class="nav p" type="button" aria-label="Cadrul anterior" data-d="-1" onClick="{{{{ step }}}}"></button>'
            f'<button class="nav n" type="button" aria-label="Cadrul următor" data-d="1" onClick="{{{{ step }}}}"></button>'
            f'{"".join(frs)}</div>')


DL = (f'<dl class="dl"><div><dt>Unde</dt><dd>{WHERE}</dd></div><div><dt>Preț</dt><dd class="num">{PRICE}</dd></div>'
      f'<div><dt>Locuri</dt><dd>Doar 8 locuri</dd></div><div><dt>Facilitează</dt><dd>{WHO}</dd></div></dl>')
BUY = f'<div class="buy"><a class="cta" href="#inscriere">{CTA} {ARROW}</a><span class="seats">{SEATS}</span></div>'


def states(root):
    out = []
    for k in range(N):
        a = f'{root}[data-a="{k}"]'
        out.append(f'{a} .sy .i{k}{{opacity:1;transform:none}}{a} .sy .f{k}{{opacity:1;transform:none;pointer-events:auto;transition-delay:.12s}}'
                   f'{a}[data-run] .sy .b{k} i{{animation:syfill 6s linear forwards}}{a}:not([data-run]) .sy .b{k} i{{transform:none}}'
                   + "".join(f'{a} .sy .b{j} i{{transform:none}}' for j in range(k)))
    return "".join(out)


COMMON = """
.u{position:relative;padding:120px 0 128px;overflow:hidden}
.u h2{font-size:clamp(44px,5vw,72px);line-height:1}
.u .date{margin:0;font:400 italic 22px/1.35 var(--display);font-variation-settings:'opsz' 20;color:var(--ink2);font-variant-numeric:tabular-nums}
.u .ttl{margin:0;font:400 clamp(30px,2.9vw,42px)/1.1 var(--display);font-variation-settings:'opsz' 20;letter-spacing:-.012em;text-wrap:balance}
.u .dl{display:grid;grid-template-columns:1fr 1fr;gap:18px 32px;margin:0;padding-top:24px;border-top:1px solid rgba(58,42,32,.2)}
.u dt{font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:#833A22}
.u dd{margin:4px 0 0;font-size:16px;line-height:1.45;color:var(--ink)}
.u .num{font-variant-numeric:tabular-nums}
.u .note{margin:0;font-size:15px;line-height:1.55;color:var(--ink2);max-width:46ch;text-wrap:pretty}
.u .buy{display:flex;align-items:center;gap:20px 24px;flex-wrap:wrap}
.u .cta{display:inline-flex;align-items:center;gap:12px;min-height:52px;padding:0 30px;border-radius:999px;background:#9C472C;color:#F8F1E8;font-weight:500;text-decoration:none;transition:background .25s}
.u .cta:hover{background:#833A22}.u .cta:hover .ar{transform:translateX(4px)}
.u .cta:focus-visible{outline:2px solid #9C472C;outline-offset:4px}
.u .seats{font-size:15px;color:#833A22}
/* the story */
.sy{position:relative;width:400px;aspect-ratio:9/16;border-radius:30px;corner-shape:squircle;overflow:hidden;background:#2A170E;isolation:isolate;user-select:none;-webkit-touch-callout:none;box-shadow:0 2px 6px rgba(70,35,15,.18),0 44px 80px -36px rgba(70,35,15,.6)}
.sy .ph,.sy .shade{position:absolute;inset:0}
.sy .ph{z-index:-2}
.sy .ph img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transform:scale(1.08);transition:opacity .55s ease,transform 7s linear}
.sy .shade{z-index:-1;background:linear-gradient(180deg,rgba(22,12,7,.5) 0%,rgba(22,12,7,0) 20%,rgba(22,12,7,0) 46%,rgba(22,12,7,.88) 100%)}
.sy .bars{position:absolute;top:12px;left:12px;right:12px;display:flex;gap:4px;z-index:2}
.sy .bar{flex:1;height:3px;border-radius:2px;background:rgba(255,255,255,.38);overflow:hidden}
.sy .bar i{display:block;height:100%;background:#FFF;transform:scaleX(0);transform-origin:left}
.sy .who{position:absolute;top:26px;left:14px;z-index:2;display:flex;align-items:center;gap:10px;color:#FFF;font-size:14px;font-weight:500;text-shadow:0 1px 8px rgba(0,0,0,.35)}
.sy .who img{width:34px;height:34px;border-radius:50%;object-fit:cover;box-shadow:0 0 0 2px #F2C79C}
.sy .who span{font-weight:400;opacity:.85}
.sy .nav{position:absolute;top:0;bottom:0;width:50%;z-index:1;background:none;border:0;padding:0;margin:0;cursor:pointer}
.sy .nav.p{left:0;width:34%}.sy .nav.n{right:0;width:66%}
.sy .nav:focus-visible{outline:2px solid #F2C79C;outline-offset:-8px;border-radius:24px}
.sy .fr{position:absolute;left:0;right:0;bottom:0;z-index:2;padding:0 26px 30px;color:#F4EDE4;opacity:0;transform:translateY(12px);pointer-events:none;transition:opacity .4s,transform .6s cubic-bezier(.2,.7,.2,1)}
.sy .fr p{margin:0}
.sy .fr .t{font:400 28px/1.2 var(--display);font-variation-settings:'opsz' 20;letter-spacing:-.01em;text-wrap:balance}
.sy .fr.cover .t{font-size:38px;line-height:1.06}
.sy .fr .k{margin-bottom:12px;font-size:14px;letter-spacing:.01em;color:#F2C79C;font-variant-numeric:tabular-nums}
.sy .fr .w{margin-top:12px;font-size:15px;color:#EFE3D3;font-variant-numeric:tabular-nums}
.sy .stk{display:inline-flex;align-items:center;gap:8px;min-height:46px;margin-top:20px;padding:0 20px;border-radius:999px;background:#FBF7F0;color:#2E1D14;font-weight:600;font-size:15px;text-decoration:none;box-shadow:0 8px 20px -8px rgba(0,0,0,.5);transition:transform .25s cubic-bezier(.2,.7,.2,1)}
.sy .stk:hover{transform:scale(1.04)}.sy .stk:focus-visible{outline:2px solid #F2C79C;outline-offset:3px}
.sy .li{width:16px;height:16px;color:#9C472C}
.sy .cd{display:inline-flex;flex-direction:column;gap:8px;margin-bottom:22px;padding:14px 18px 14px;border-radius:18px;background:rgba(251,247,240,.94);color:#2E1D14;box-shadow:0 10px 30px -10px rgba(0,0,0,.5)}
.sy .cdt{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:#833A22;font-weight:600}
.sy .cdn{display:flex;gap:14px}
.sy .cdn span{display:flex;flex-direction:column;align-items:center}
.sy .cdn b{font:400 34px/1 var(--display);font-variation-settings:'opsz' 20;font-variant-numeric:tabular-nums}
.sy .cdn i{font-style:normal;font-size:12px;color:#6B5444;margin-top:4px}
[data-hold] .sy .bar i{animation-play-state:paused!important}
@keyframes syfill{from{transform:scaleX(0)}to{transform:scaleX(1)}}
@media (max-width:820px){.u{padding:76px 0 84px}.u h2{font-size:clamp(40px,11vw,52px)}.u .date{font-size:20px}.u .dl{grid-template-columns:1fr 1fr}.u .buy{flex-direction:column;align-items:stretch}.u .cta{justify-content:center}.u .seats{text-align:center}
.sy{width:100%;max-width:360px}.sy .fr .t{font-size:25px}.sy .fr.cover .t{font-size:33px}.sy .cdn b{font-size:30px}}
@media (prefers-reduced-motion:reduce){.sy .ph img,.sy .fr{transition:none}}
"""

OPTS = {}

# ---------- A. Bilet ----------
OPTS["UrmatorulA"] = ("Următorul atelier A: story + bilet", """
.ua{background:linear-gradient(180deg,#F4EDE4 0%,#EDE0CD 100%)}
.ua .grid{display:grid;grid-template-columns:minmax(0,1fr) 400px;gap:110px;align-items:center}
.ua .l{display:flex;flex-direction:column;gap:22px}
.ua .l h2{margin-bottom:18px}
.ua .dl{margin-top:10px}
.ua .buy{margin-top:16px}
@media (max-width:820px){.ua .grid{grid-template-columns:1fr;gap:36px}.ua .l{display:contents}.ua .l h2{order:-3;margin:0}.ua .date{order:-2}.ua .sy{order:-1;justify-self:center}.ua .ttl{display:none}.ua .l>*{margin:0}}
""" + states(".ua"), f"""<section class="u ua" id="evenimente" aria-labelledby="u-h" data-a="0" ref="{{{{ rootRef }}}}">
<div class="wrap grid">
<div class="l"><h2 class="disp" id="u-h">{H}</h2><p class="ttl">{TITLE}</p><p class="date">{DATE}</p>
{DL}<p class="note">{PRICE}, {PRICE_NOTE}</p>{BUY}</div>
{story()}
</div>
</section>""")

# ---------- B. Vizualizator ----------
side_imgs = "".join(f'<img class="i{k}" src="{s}" alt="" style="object-position:{p}">' for k, (s, a, p) in enumerate(IMGS))
bg_imgs = "".join(f'<img class="g{k}" src="{s}" alt="" style="object-position:{p}">' for k, (s, a, p) in enumerate(IMGS))
b_states = "".join(f'.ub[data-a="{k}"] .bg .g{k}{{opacity:1}}'
                   f'.ub[data-a="{k}"] .side.l .i{(k - 1) % N}{{opacity:1}}.ub[data-a="{k}"] .side.r .i{(k + 1) % N}{{opacity:1}}' for k in range(N))
OPTS["UrmatorulB"] = ("Următorul atelier B: vizualizator", """
.ub{background:#E9DCCB;isolation:isolate}
.ub .bg{position:absolute;inset:-60px;z-index:-2}
.ub .bg img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;filter:blur(48px) saturate(.9);transform:scale(1.15);transition:opacity 1s ease}
.ub::before{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(180deg,rgba(244,237,228,.86) 0%,rgba(240,230,216,.74) 50%,rgba(244,237,228,.9) 100%)}
.ub .top{display:flex;flex-direction:column;align-items:center;text-align:center;gap:14px;margin-bottom:52px}
.ub .stage{display:flex;align-items:center;justify-content:center;gap:44px}
.ub .side{position:relative;width:200px;aspect-ratio:9/16;border-radius:20px;corner-shape:squircle;overflow:hidden;padding:0;border:0;cursor:pointer;background:#2A170E;opacity:.62;transform:scale(.96);transition:opacity .3s,transform .4s cubic-bezier(.2,.7,.2,1);box-shadow:0 24px 50px -30px rgba(70,35,15,.6)}
.ub .side:hover{opacity:.9;transform:none}
.ub .side img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity .5s}
.ub .side .ar{position:absolute;left:50%;top:50%;width:22px;height:22px;margin:-11px 0 0 -11px;padding:12px;border-radius:50%;background:rgba(251,247,240,.92);color:#2E1D14;box-sizing:content-box}
.ub .side.l .ar{transform:rotate(180deg)}
.ub .side:focus-visible{outline:2px solid #9C472C;outline-offset:4px}
.ub .info{display:flex;flex-direction:column;align-items:center;gap:22px;margin-top:52px;text-align:center}
.ub .facts{display:flex;flex-wrap:wrap;justify-content:center;gap:8px 28px;margin:0;font-size:16px;color:var(--ink)}
.ub .facts span{display:inline-flex;gap:8px}.ub .facts b{font-weight:500;color:#833A22}
.ub .buy{justify-content:center}
@media (max-width:820px){.ub .side{display:none}.ub .top{margin-bottom:32px}.ub .info{margin-top:32px}.ub .facts{flex-direction:column;gap:6px}.ub .buy{width:100%}}
""" + b_states + states(".ub"), f"""<section class="u ub" id="evenimente" aria-labelledby="u-h" data-a="0" ref="{{{{ rootRef }}}}">
<div class="bg" aria-hidden="true">{bg_imgs}</div>
<div class="wrap">
<div class="top"><h2 class="disp" id="u-h">{H}</h2><p class="date">{DATE}</p></div>
<div class="stage">
<button class="side l" type="button" aria-label="Cadrul anterior" data-d="-1" onClick="{{{{ step }}}}">{side_imgs}{ARROW}</button>
{story()}
<button class="side r" type="button" aria-label="Cadrul următor" data-d="1" onClick="{{{{ step }}}}">{side_imgs}{ARROW}</button>
</div>
<div class="info"><p class="facts"><span><b>Unde</b>{WHERE}</span><span><b>Preț</b>{PRICE}</span><span><b>Facilitează</b>{WHO}</span></p>
<p class="note">{PRICE}, {PRICE_NOTE}</p>{BUY}</div>
</div>
</section>""")

# ---------- C. Highlights ----------
hl = "".join(f'<li><button class="hl h{k}" type="button" data-i="{k}" aria-pressed="{str(k == 0).lower()}" onClick="{{{{ pick }}}}">'
             f'<span class="ring"><img src="{IMGS[k][0]}" alt="" style="object-position:{IMGS[k][2]}"></span><span class="lb">{HL[k]}</span></button></li>'
             for k in range(N))
c_states = "".join(f'.uc[data-a="{k}"] .h{k} .ring{{background:linear-gradient(135deg,#9C472C,#C07A4E 55%,#E3A36F);transform:scale(1.06)}}'
                   f'.uc[data-a="{k}"] .h{k} .lb{{color:var(--ink);font-weight:600}}' for k in range(N))
OPTS["UrmatorulC"] = ("Următorul atelier C: highlights", """
.uc{background:#EFE4D4}
.uc .grid{display:grid;grid-template-columns:400px minmax(0,1fr);gap:110px;align-items:center}
.uc .r{display:flex;flex-direction:column;gap:22px}
.uc .r h2{margin-bottom:18px}
.uc .hls{display:flex;gap:18px;list-style:none;margin:10px 0 6px;padding:0}
.uc .hl{display:flex;flex-direction:column;align-items:center;gap:10px;min-width:72px;padding:0;border:0;background:none;cursor:pointer;font:inherit;color:var(--ink2)}
.uc .ring{display:block;width:72px;height:72px;padding:3px;border-radius:50%;background:#CDB79C;box-sizing:border-box;transition:transform .35s cubic-bezier(.2,.7,.2,1),background .3s}
.uc .hl:not([data-seen]) .ring{background:linear-gradient(135deg,#B4583A,#C07A4E 60%,#E3A36F)}
.uc .ring img{display:block;width:100%;height:100%;border-radius:50%;object-fit:cover;box-shadow:0 0 0 3px #EFE4D4}
.uc .lb{font-size:13px;line-height:1.2}
.uc .hl:hover .ring{transform:scale(1.06)}
.uc .hl:focus-visible{outline:2px solid #9C472C;outline-offset:6px;border-radius:12px}
.uc .buy{margin-top:8px}
@media (max-width:820px){.uc .grid{grid-template-columns:1fr;gap:28px}.uc .r{display:contents}.uc .r h2{order:-4;margin:0}.uc .date{order:-3}.uc .hls{order:-2;margin:0 -20px;padding:4px 20px 6px;overflow-x:auto;scrollbar-width:none;gap:14px}.uc .sy{order:-1;justify-self:center}.uc .ttl{display:none}.uc .r>*{margin:0}}
""" + c_states + states(".uc"), f"""<section class="u uc" id="evenimente" aria-labelledby="u-h" data-a="0" ref="{{{{ rootRef }}}}">
<div class="wrap grid">
{story()}
<div class="r"><h2 class="disp" id="u-h">{H}</h2><p class="ttl">{TITLE}</p><p class="date">{DATE}</p>
<ul class="hls" aria-label="Cadrele story-ului">{hl}</ul>
{DL}<p class="note">{PRICE}, {PRICE_NOTE}</p>{BUY}</div>
</div>
</section>""")

# ---------- D. Data mare ----------
OPTS["UrmatorulD"] = ("Următorul atelier D: data mare + countdown", """
.ud{background:radial-gradient(ellipse 55% 60% at 50% 40%,#F6EEE3 0%,rgba(246,238,227,0) 70%),linear-gradient(180deg,#EFE4D4 0%,#E8D9C3 60%,#E2CDB0 100%)}
.ud .big{position:absolute;left:50%;top:236px;z-index:0;transform:translateX(-50%);margin:0;white-space:nowrap;font:400 clamp(100px,14.5vw,212px)/.84 var(--display);font-variation-settings:'opsz' 96;letter-spacing:-.04em;color:var(--terra);pointer-events:none;user-select:none}
.ud .wrap{z-index:1}
.ud h2{text-align:center;margin-bottom:48px}
.ud .stage{display:grid;grid-template-columns:minmax(0,1fr) 380px minmax(0,1fr);gap:56px;align-items:end;padding-top:120px}
.ud .sy{width:380px}
.ud .l{display:flex;flex-direction:column;align-items:flex-end;text-align:right;gap:14px;padding-bottom:40px}
.ud .r{display:flex;flex-direction:column;gap:20px;padding-bottom:40px}
.ud .dl{grid-template-columns:1fr}
@media (max-width:820px){.ud .big{top:150px;font-size:15vw}.ud h2{margin-bottom:0}.ud .stage{grid-template-columns:1fr;gap:28px;padding-top:22vw}.ud .sy{width:100%;justify-self:center}.ud .l{order:1;align-items:center;text-align:center;padding:0}.ud .r{padding:0}.ud .dl{grid-template-columns:1fr 1fr}}
""" + states(".ud"), f"""<section class="u ud" id="evenimente" aria-labelledby="u-h" data-a="0" ref="{{{{ rootRef }}}}">
<p class="big" aria-hidden="true">15 noiembrie</p>
<div class="wrap">
<h2 class="disp" id="u-h">{H}</h2>
<div class="stage">
<div class="l"><p class="ttl">{TITLE}</p><p class="date">{DATE}</p></div>
{story(countdown=True)}
<div class="r">{DL}<p class="note">{PRICE}, {PRICE_NOTE}</p>{BUY}</div>
</div>
</div>
</section>""")

JS = """class Component extends DCLogic {
  componentDidMount() {
    var self = this, reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (!this.root) return;
    this.go(0);
    var cd = this.root.querySelectorAll('.cd [data-u]');
    if (cd.length) {
      var target = Date.UTC(2026, 10, 15, 15, 0, 0);  // 15 Nov 2026, 17:00 in Bucharest (UTC+2)
      var pad = function (n) { return (n < 10 ? '0' : '') + n; };
      this.tickCd = function () {
        var s = Math.max(0, Math.floor((target - Date.now()) / 1000)), v = { d: Math.floor(s / 86400), h: Math.floor(s % 86400 / 3600), m: Math.floor(s % 3600 / 60) };
        for (var i = 0; i < cd.length; i++) cd[i].textContent = pad(v[cd[i].getAttribute('data-u')]);
      };
      this.tickCd(); this.cdTimer = setInterval(this.tickCd, 20000);
    }
    if (reduce) return;
    this.root.setAttribute('data-run', '');
    this.onEnd = function (e) {
      if (e.animationName !== 'syfill') return;
      var a = parseInt(self.root.getAttribute('data-a'), 10);
      if (a < """ + str(N - 1) + """) self.go(a + 1);   // stops on the last frame, the one with the button
    };
    this.root.addEventListener('animationend', this.onEnd);
  }
  componentWillUnmount() { clearInterval(this.cdTimer); if (this.root && this.onEnd) this.root.removeEventListener('animationend', this.onEnd); }
  renderVals() {
    var self = this, n = """ + str(N) + """;
    if (!this.cb) {
      this.go = function (i) {
        if (!self.root) return;
        self.root.setAttribute('data-a', String(i));
        var h = self.root.querySelectorAll('.hl');
        for (var k = 0; k < h.length; k++) { h[k].setAttribute('aria-pressed', String(k === i)); if (k === i) h[k].setAttribute('data-seen', ''); }
      };
      this.cb = {
        rootRef: function (el) { self.root = el; },
        step: function (e) {
          var a = parseInt(self.root.getAttribute('data-a'), 10) + parseInt(e.currentTarget.getAttribute('data-d'), 10);
          self.go((a + n) % n);
        },
        pick: function (e) { self.go(parseInt(e.currentTarget.getAttribute('data-i'), 10)); },
        hold: function () { if (self.root) self.root.setAttribute('data-hold', ''); },
        release: function () { if (self.root) self.root.removeAttribute('data-hold'); }
      };
    }
    return this.cb;
  }
}"""


def page(title, css, html, w, h):
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
{BASE_CSS}{COMMON}{css}</style>
</helmet>
<div class="pg">
{html}
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{w},"height":{h}}}}}'>
{JS}
</script>
</body>
</html>
"""


if __name__ == "__main__":
    for name, (title, css, html) in OPTS.items():
        for suffix, w, h in (("", 1440, 1100), ("Mobil", 390, 1500)):
            f = os.path.join(P, f"{name}{suffix}.dc.html")
            open(f, "w", encoding="utf-8").write(page(title + (" · mobil" if suffix else ""), css, html, w, h))
            if not suffix:
                subprocess.run([sys.executable, os.path.join(HERE, "dc2html.py"), f, os.path.join(HERE, f"opt-{name}.html")], check=True)
    names = list(OPTS)
    open(os.path.join(HERE, "urmator.html"), "w").write('<!doctype html><meta charset="utf-8"><title>Următorul atelier</title><style>body{margin:0}iframe{width:1440px;height:1250px;border:0;display:block}</style>' + "".join(f'<iframe src="opt-{n}.html"></iframe>' for n in names))
    open(os.path.join(HERE, "urmator-mobil.html"), "w").write('<!doctype html><meta charset="utf-8"><title>Următorul atelier mobil</title><style>body{margin:0;padding:10px;background:#1b1b1b;display:flex;gap:12px;color:#ddd;font:13px system-ui}figure{margin:0;flex:none}iframe{width:390px;height:1800px;border:0;display:block}</style>' + "".join(f'<figure><figcaption>{n}</figcaption><iframe src="opt-{n}.html"></iframe></figure>' for n in names))
