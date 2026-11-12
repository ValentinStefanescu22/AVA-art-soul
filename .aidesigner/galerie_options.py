"""Acasă: 'Ce spun oamenii' + 'Galerie mini' in one block (Vali, 10 nov). Four variants:
A Mozaic          a photo wall with the testimonials set among the photos.
B Bandă           two rows of photos drifting in opposite directions, one large testimonial in the middle.
C Postare         an Instagram post (photo carousel) whose comments are the testimonials, beside the profile grid.
D Galerie         a horizontal strip of tall photos filtered by the document's categories, quotes laid on some photos.
Copy: docs/continut-site.md (Acasă blocks 6 and 7, 'Galerie', 'Testimoniale'). There are no testimonials yet, so they
stay visible [placeholders] built from the two questions the document says to ask after each workshop.

usage: python3 .aidesigner/galerie_options.py
writes .aidesigner/canvas/project/Oameni{A..D}*.dc.html (+ Mobil twins), previews .aidesigner/opt-Oameni*.html,
comparison pages .aidesigner/oameni.html and oameni-mobil.html
"""
import os, subprocess, sys
from about_options2 import P, HERE, FONTS, BASE_CSS, ARROW

SOURCES = {
    "OameniA": ("Framer: Testimonial Mosaic; Framer: Social Proof Wall", "https://www.framer.com/marketplace/components/testimonial-mosaic/"),
    "OameniB": ("Framer: Testimonial Flux; Framer: Infinite Marquee", "https://www.framer.com/marketplace/components/testimonial-flux/"),
    "OameniC": ("Framer: Instagram Post Pro; Framer: Insta Post Slider", "https://www.framer.com/marketplace/components/instagram-post-pro/"),
    "OameniD": ("Framer: Testimonial Gallery; Framer: Vertical Gallery", "https://www.framer.com/marketplace/components/testimonial-gallery/"),
}

H = "Ce spun oamenii"
GAL = "Vezi toată galeria"
IG = "@ava.art.soul pe Instagram"
LINKS = (f'<div class="links"><a class="more" href="#galerie">{GAL} {ARROW}</a>'
         f'<a class="more" href="https://www.instagram.com/ava.art.soul/">{IG} {ARROW}</a></div>')
# real testimonials from Vali (11 nov), in the order he gave; no workshop named
Q = [("Foarte frumos și cozy, chiar am reușit să reflect asupra mea cât timp lucram cu lutul.", "Costin", ""),
     ("A fost o experiență foarte plăcută și relaxantă. Pauzele de socializare dintre activități au fost exact ce trebuia.", "Mario", ""),
     ("Mi-a plăcut «intenția» cu care am pornit atelierul și faptul că acum obiectul semnifică ceva cu adevărat deosebit pentru fiecare.", "Mădălina", ""),
     ("O activitate foarte relaxantă într-un cadru intim și frumos. Revin cu siguranță!", "Adina", "")]

# ---------- photos (blob ids; Unsplash placeholders say so in the alt text) ----------
def ph(id_, alt, pos="50% 50%", cat="ateliere"):
    return dict(src=f"/_blob/{id_}", alt=alt, pos=pos, cat=cat)


IM = {
    "masa": ph("988e3a505fd5ae1db56d481b3d1e33b1", "Atelierul din octombrie: opt oameni în jurul unei mese cu lut, ceai și prăjitură", "50% 55%"),
    "bol": ph("42c18be93cd80d91d6d1d16793e790c6", "Doi participanți își dau din mână în mână un bol de lut, la atelierul din octombrie", "40% 50%"),
    "sus": ph("af69ff19bcdcf8c0410f4609e748d3a2", "Masa atelierului din octombrie văzută de sus, cu lut, căni și pensule", "50% 50%"),
    "pictat": ph("dad600a42f9bdc35b94ba47b4a49fc4a", "O femeie pictează un bol de ceramică (fotografie provizorie)", "40% 50%", "piese"),
    "piese": ph("74f239bfbd557a0a5a661ddd26484b66", "Boluri de ceramică arse, în culori diferite (fotografie provizorie)", "50% 40%", "piese"),
    "maini": ph("27d62de5381eeee8e9ab504567023c22", "Mâini care modelează un bol de lut (fotografie provizorie)", "50% 40%", "piese"),
    "vas": ph("18303291bcb407fd0b37b52607ecebba", "Mâini care își dau din mână în mână un vas de lut (fotografie provizorie)", "50% 45%", "piese"),
    "grup": ph("70ad22aacebcba3dbca6580a21b45332", "Un grup lucrează lutul într-un atelier de ceramică (fotografie provizorie)", "50% 45%"),
    "cani": ph("f2f68570a5d5b88f15c8b0c9d18a7c34", "Două persoane stau la masă, cu câte o cană în mâini (fotografie provizorie)", "50% 50%"),
    "copil": ph("4b9ba5277b8dd3fad28a1395c891c1d1", "Un copil zâmbește, cu un vas de lut în mâini (fotografie provizorie)", "60% 35%"),
    "cabana": ph("8485d5712a94ed66603aeb86f80c0aac", "Cabană de lemn într-o pădure de pini (fotografie provizorie)", "50% 60%", "retreaturi"),
}


def img(k, cls=""):
    p = IM[k]
    return f'<img{f" class={chr(34)}{cls}{chr(34)}" if cls else ""} src="{p["src"]}" alt="{p["alt"]}" style="object-position:{p["pos"]}" loading="lazy">'


QUOTE_MARK = '<svg class="qm" viewBox="0 0 32 24" aria-hidden="true"><path d="M0 24V14C0 6 4 1.5 12 0l1.4 3C8.6 4.4 6.6 7.2 6.4 11H12v13H0zm18 0V14c0-8 4-12.5 12-14l1.4 3c-4.8 1.4-6.8 4.2-7 8H30v13H18z" style="fill:currentColor"></path></svg>'


def quote(i, cls="q"):
    t, n, w = Q[i]
    return f'<figure class="{cls}">{QUOTE_MARK}<blockquote>{t}</blockquote><figcaption><b>{n}</b>{f"<span>{w}</span>" if w else ""}</figcaption></figure>'


COMMON = """
.og{position:relative;padding:120px 0 128px;overflow:hidden}
.og .head{display:flex;justify-content:space-between;align-items:flex-end;gap:32px;margin-bottom:52px}
.og h2{font-size:clamp(44px,5vw,72px);line-height:1}
.og .links{display:flex;flex-wrap:wrap;gap:4px 28px}
.og .links .more{margin-top:0;color:var(--ink)}
.og img{display:block}
.og .q{margin:0}
.og .q .qm{flex:none;width:30px;height:22px;color:#B4583A;margin-bottom:16px}
.og .q blockquote{margin:0;font:400 22px/1.35 var(--display);font-variation-settings:'opsz' 20;letter-spacing:-.005em;text-wrap:pretty}
.og .q figcaption{display:flex;flex-wrap:wrap;gap:2px 10px;align-items:baseline;margin-top:18px;font-size:15px}
.og .q figcaption b{font-weight:600}
.og .q figcaption span{color:var(--ink2)}
.og button{appearance:none;font:inherit;color:inherit;cursor:pointer}
.og .rd{display:grid;place-items:center;width:44px;height:44px;padding:0;border:0;border-radius:50%;background:#FBF7F0;color:#262626;box-shadow:0 1px 3px rgba(0,0,0,.14),0 6px 16px -6px rgba(0,0,0,.22);transition:transform .2s cubic-bezier(.2,.7,.2,1)}
.og .rd:hover{transform:scale(1.06)}.og .rd svg{width:18px;height:18px}.og .rd.pv svg{transform:rotate(180deg)}
.og .rd:focus-visible,.og .tab:focus-visible{outline:2px solid #9C472C;outline-offset:3px}
@media (max-width:820px){.og{padding:76px 0 84px}.og .head{flex-direction:column;align-items:flex-start;gap:16px;margin-bottom:32px}.og h2{font-size:clamp(40px,11vw,52px)}.og .q blockquote{font-size:20px}}
"""
CHEV = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M6 3.5L10.5 8L6 12.5" fill="none" stroke="currentColor" style="stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round"></path></svg>'
OPTS = {}

# ---------- A. Mozaic ----------
A_TILES = [("a", "masa"), ("q1", 0), ("b", "pictat"), ("c", "piese"), ("d", "bol"), ("q2", 1), ("e", "grup"), ("f", "maini"), ("g", "cani"), ("q3", 2)]
a_tiles = "".join((f'<div class="t {a} qt">{quote(v)}</div>' if a.startswith("q") else f'<div class="t {a} pt">{img(v)}</div>') for a, v in A_TILES)
OPTS["OameniA"] = ("Ce spun oamenii A: mozaic", """
.oa{background:#F4EDE4}
.oa .wall{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));grid-auto-rows:215px;gap:14px;
grid-template-areas:"a a q1 b" "a a q1 c" "d q2 q2 e" "f g q3 e"}
""" + "".join(f'.oa .{a}{{grid-area:{a}}}' for a, _ in A_TILES) + """
.oa .t{position:relative;border-radius:22px;corner-shape:squircle;overflow:hidden}
.oa .pt img{width:100%;height:100%;object-fit:cover;transition:transform 1.1s cubic-bezier(.2,.7,.2,1)}
.oa .pt:hover img{transform:scale(1.04)}
.oa .qt{display:flex;padding:30px 30px 28px;background:#E9DBC6}
.oa .qt .q{display:flex;flex-direction:column;justify-content:space-between;width:100%}
.oa .q2{background:#9C472C;color:#FBF4EA}.oa .q2 .qm{color:#F2C79C}.oa .q2 figcaption span{color:#F3DCC8}
.oa .q2 blockquote{font-size:23px;max-width:34ch}
.oa .q3{background:#3A2A20;color:#F4EDE4}.oa .q3 .qm{color:#F2C79C}.oa .q3 figcaption span{color:#D9C7B4}
.oa .q3 blockquote{font-size:19px}
@media (max-width:820px){.oa .wall{grid-template-columns:1fr 1fr;grid-auto-rows:auto;gap:10px;grid-template-areas:"a a" "q1 q1" "b c" "q2 q2" "d e" "f g" "q3 q3"}
.oa .pt{height:170px}.oa .a{height:240px}.oa .qt{padding:24px 22px}.oa .q2 blockquote{font-size:21px}.oa .q3 blockquote{font-size:19px}}
""", f"""<section class="og oa" id="oameni" aria-labelledby="og-h">
<div class="wrap"><div class="head"><h2 class="disp" id="og-h">{H}</h2>{LINKS}</div>
<div class="wall">{a_tiles}</div></div>
</section>""")

# ---------- B. Bandă ----------
ROW1 = ["masa", "pictat", "cani", "piese", "bol", "copil"]
ROW2 = ["maini", "grup", "sus", "vas", "cabana", "pictat"]


def row(keys, cls):
    one = "".join(f'<li>{img(k)}</li>' for k in keys)
    dup = "".join(f'<li aria-hidden="true">{img(k).replace(IM[k]["alt"], "")}</li>' for k in keys)
    return f'<div class="mq {cls}"><ul>{one}{dup}</ul></div>'


b_quotes = "".join(f'<div class="bq b{i}">{quote(i)}</div>' for i in range(3))
b_dots = "".join(f'<button class="dot" type="button" data-i="{i}" aria-label="Testimonialul {i + 1}" onClick="{{{{ pick }}}}"></button>' for i in range(3))
OPTS["OameniB"] = ("Ce spun oamenii B: bandă", """
.ob{background:#EFE4D4}
.ob .head{flex-direction:column;align-items:center;text-align:center;gap:18px}
.ob .mq{overflow:hidden;-webkit-mask-image:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent);mask-image:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent)}
.ob .mq ul{display:flex;gap:14px;width:max-content;list-style:none;margin:0;padding:0;animation:obl 70s linear infinite}
.ob .mq.r2 ul{animation-name:obr;animation-duration:80s}
.ob .mq:hover ul{animation-play-state:paused}
.ob .mq li{height:250px;aspect-ratio:4/5;border-radius:20px;corner-shape:squircle;overflow:hidden;flex:none}
.ob .mq li:nth-child(3n+2){aspect-ratio:3/2}
.ob .mq img{width:100%;height:100%;object-fit:cover}
@keyframes obl{to{transform:translateX(-50%) translateX(-7px)}}
@keyframes obr{from{transform:translateX(-50%) translateX(-7px)}to{transform:none}}
.ob .mid{position:relative;display:grid;justify-items:center;margin:56px auto;max-width:820px;text-align:center}
.ob .bq{grid-area:1/1;opacity:0;transform:translateY(8px);transition:opacity .6s,transform .8s cubic-bezier(.2,.7,.2,1);pointer-events:none}
.ob .bq .qm{margin:0 auto 22px;width:38px;height:28px}
.ob .bq blockquote{font-size:clamp(26px,2.6vw,36px);line-height:1.25}
.ob .bq figcaption{justify-content:center}
.ob .dots{display:flex;gap:6px;margin-top:28px}
.ob .dot{width:44px;height:44px;padding:0;border:0;background:none;display:grid;place-items:center}
.ob .dot::before{content:"";width:8px;height:8px;border-radius:50%;background:#CDB79C;transition:background .3s,transform .3s}
.ob .dot:focus-visible{outline:2px solid #9C472C;outline-offset:-6px;border-radius:50%}
.ob .head{margin-bottom:48px}
""" + "".join(f'.ob[data-a="{i}"] .b{i}{{opacity:1;transform:none;pointer-events:auto}}.ob[data-a="{i}"] .dot:nth-child({i + 1})::before{{background:#9C472C;transform:scale(1.25)}}' for i in range(3)) + """
@media (max-width:820px){.ob .mq li{height:170px}.ob .mid{margin:36px 20px}.ob .bq blockquote{font-size:22px}}
@media (prefers-reduced-motion:reduce){.ob .mq ul{animation:none}.ob .mq{overflow-x:auto}}
""", f"""<section class="og ob" id="oameni" aria-labelledby="og-h" data-a="0" ref="{{{{ rootRef }}}}" data-rotate="">
<div class="wrap"><div class="head"><h2 class="disp" id="og-h">{H}</h2>{LINKS}</div></div>
{row(ROW1, "r1")}
<div class="mid" aria-live="polite">{b_quotes}<div class="dots">{b_dots}</div></div>
{row(ROW2, "r2")}
</section>""")

# ---------- C. Postare ----------
C_SLIDES = ["masa", "bol", "pictat", "piese"]
c_slides = "".join(f'<li class="s{i}">{img(k)}</li>' for i, k in enumerate(C_SLIDES))
c_dots = "".join(f'<span class="d{i}"></span>' for i in range(len(C_SLIDES)))
c_comments = "".join(f'<li class="cm"><span class="av" aria-hidden="true"></span><div><p><b>{Q[i][1]}</b> {Q[i][0]}</p><span class="w">{Q[i][2]}</span></div></li>' for i in range(3))
C_GRID = ["sus", "pictat", "cani", "maini", "masa", "piese", "grup", "vas", "copil"]
c_grid = "".join(f'<li>{img(k)}</li>' for k in C_GRID)
ICONS = {
    "heart": '<path d="M12 20s-7-4.4-7-10a4 4 0 017-2.6A4 4 0 0119 10c0 5.6-7 10-7 10z"></path>',
    "comm": '<path d="M20 11.5a8 8 0 01-11.6 7.1L4 20l1.4-4.2A8 8 0 1120 11.5z"></path>',
    "send": '<path d="M21 4L10 14M21 4l-7 17-4-7-7-4 18-6z"></path>',
    "save": '<path d="M6 3h12v18l-6-4.5L6 21z"></path>',
}


def icon(k):
    return f'<svg viewBox="0 0 24 24" aria-hidden="true" style="fill:none;stroke:currentColor;stroke-width:1.7;stroke-linejoin:round;stroke-linecap:round">{ICONS[k]}</svg>'


OPTS["OameniC"] = ("Ce spun oamenii C: postare", """
.oc{background:linear-gradient(180deg,#F4EDE4 0%,#EDE0CD 100%)}
.oc .grid{display:grid;grid-template-columns:480px minmax(0,1fr);gap:96px;align-items:start}
.oc .post{background:#FFFDF9;border:1px solid rgba(58,42,32,.12);border-radius:22px;corner-shape:squircle;overflow:hidden;box-shadow:0 30px 60px -40px rgba(70,35,15,.45)}
.oc .ph{display:flex;align-items:center;gap:12px;padding:14px 16px;font-size:14px}
.oc .ph img{width:34px;height:34px;border-radius:50%;object-fit:cover;box-shadow:0 0 0 2px #F2C79C}
.oc .ph b{display:block;font-weight:600}.oc .ph span{color:var(--ink2);font-size:13px}
.oc .car{position:relative;aspect-ratio:1;overflow:hidden;background:#2A170E}
.oc .car ul{list-style:none;margin:0;padding:0;display:flex;height:100%;transition:transform .55s cubic-bezier(.22,.8,.2,1)}
.oc .car li{flex:none;width:100%;height:100%}
.oc .car img{width:100%;height:100%;object-fit:cover}
.oc .car .rd{position:absolute;top:50%;margin-top:-16px;width:32px;height:32px}
.oc .car .rd svg{width:16px;height:16px}
.oc .car .rd::before{content:"";position:absolute;inset:-6px}
.oc .car .pv{left:12px}.oc .car .nx{right:12px}
.oc .acts{display:flex;align-items:center;gap:16px;padding:12px 16px 4px}
.oc .acts svg{width:24px;height:24px}.oc .acts .sv{margin-left:auto}
.oc .dts{position:absolute;left:0;right:0;top:50%;transform:translateY(-50%);pointer-events:none;display:flex;justify-content:center;gap:4px}
.oc .acts{position:relative}
.oc .dts span{width:6px;height:6px;border-radius:50%;background:#CDB79C}
.oc .cap{margin:14px 16px 0;font-size:15px;line-height:1.5}
.oc .cap b{font-weight:600}
.oc .cms{list-style:none;margin:14px 0 0;padding:0 16px 20px;display:flex;flex-direction:column;gap:14px}
.oc .cm{display:flex;gap:12px;font-size:15px;line-height:1.5}
.oc .cm p{margin:0;font-family:var(--display);font-variation-settings:'opsz' 20;font-size:18px;line-height:1.35}
.oc .cm p b{font-family:var(--text);font-size:15px;font-weight:600;margin-right:4px}
.oc .cm .w{display:block;margin-top:4px;font-size:13px;color:var(--ink2)}
.oc .av{flex:none;width:30px;height:30px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#E9D2B5,#C9A27E)}
.oc .r h2{margin-bottom:22px}
.oc .lead{margin:0 0 36px;color:var(--ink2);font:400 italic 22px/1.35 var(--display);font-variation-settings:'opsz' 20}
.oc .pg3{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,1fr);gap:4px;border-radius:16px;overflow:hidden}
.oc .pg3 li{aspect-ratio:1;overflow:hidden}
.oc .pg3 img{width:100%;height:100%;object-fit:cover;transition:transform .9s cubic-bezier(.2,.7,.2,1),opacity .3s}
.oc .pg3 li:hover img{transform:scale(1.05);opacity:.9}
.oc .links{margin-top:28px}
""" + "".join(f'.oc[data-a="{i}"] .car ul{{transform:translateX(-{i * 100}%)}}.oc[data-a="{i}"] .dts .d{i}{{background:#9C472C}}' for i in range(len(C_SLIDES))) + """
.oc[data-a="0"] .car .pv,.oc[data-a="3"] .car .nx{opacity:0;pointer-events:none}
@media (max-width:820px){.oc .grid{grid-template-columns:1fr;gap:40px}.oc .r{display:contents}.oc .r h2{order:-2;margin:0}.oc .lead{order:-1;margin:-24px 0 0;font-size:20px}.oc .cm p{font-size:17px}}
""", f"""<section class="og oc" id="oameni" aria-labelledby="og-h" data-a="0" data-n="{len(C_SLIDES)}" ref="{{{{ rootRef }}}}">
<div class="wrap grid">
<article class="post" aria-label="Postare: atelierul din octombrie">
<div class="ph"><img src="/_blob/61696ece195f787b8ccb139b396a6450" alt=""><div><b>ava.art.soul</b><span>București</span></div></div>
<div class="car"><ul>{c_slides}</ul>
<button class="rd pv" type="button" aria-label="Fotografia anterioară" data-d="-1" onClick="{{{{ step }}}}">{CHEV}</button>
<button class="rd nx" type="button" aria-label="Fotografia următoare" data-d="1" onClick="{{{{ step }}}}">{CHEV}</button></div>
<div class="acts" aria-hidden="true">{icon("heart")}{icon("comm")}{icon("send")}<span class="sv">{icon("save")}</span><div class="dts">{c_dots}</div></div>
<p class="cap"><b>ava.art.soul</b> [Descrierea postării: câteva cuvinte despre atelierul din octombrie]</p>
<ul class="cms" aria-label="Ce spun oamenii">{c_comments}</ul>
</article>
<div class="r"><h2 class="disp" id="og-h">{H}</h2><p class="lead">Din ateliere, pe Instagram.</p>
<ul class="pg3">{c_grid}</ul>{LINKS}</div>
</div>
</section>""")

# ---------- D. Galerie cu citate ----------
D_CARDS = [("masa", 0), ("pictat", None), ("bol", 1), ("cani", None), ("grup", 2), ("copil", None), ("sus", None),
           ("piese", None), ("maini", None), ("vas", None), ("cabana", None)]


def dcard(k, qi):
    cat = IM[k]["cat"]
    q = f'<div class="ov">{quote(qi)}</div>' if qi is not None else ""
    return f'<li class="cd c-{cat}{" hasq" if q else ""}">{img(k)}{q}</li>'


d_cards = "".join(dcard(k, q) for k, q in D_CARDS) + '<li class="cd c-retreaturi soon"><p>[poze și testimoniale de la retreaturi, imediat ce le ai]</p></li>'
TABS = [("ateliere", "Ateliere"), ("piese", "Piese"), ("retreaturi", "Retreaturi")]
d_tabs = "".join(f'<button class="tab" type="button" data-f="{k}" onClick="{{{{ filter }}}}">{t}</button>' for k, t in TABS)
OPTS["OameniD"] = ("Ce spun oamenii D: galerie cu citate", """
.od{background:#F4EDE4}
.od .bar{display:flex;justify-content:space-between;align-items:center;gap:20px;margin-bottom:28px}
.od .tabs{display:flex;gap:8px;flex-wrap:wrap}
.od .tab{min-height:44px;padding:0 20px;border-radius:999px;border:1px solid rgba(58,42,32,.25);background:none;font-size:15px;transition:background .25s,color .25s,border-color .25s}
.od .tab:hover{border-color:var(--ink)}
.od .arrows{display:flex;gap:10px}
.od .track{display:flex;gap:16px;list-style:none;margin:0;padding:6px max(40px,calc(50% - 580px)) 24px;overflow-x:auto;scroll-snap-type:x mandatory;scroll-padding:0 max(40px,calc(50% - 580px));scrollbar-width:none;scroll-behavior:smooth}
.od .track::-webkit-scrollbar{display:none}
.od .cd{position:relative;flex:none;width:330px;height:460px;border-radius:22px;corner-shape:squircle;overflow:hidden;scroll-snap-align:start;background:#DCC4A4}
.od .cd.hasq{width:400px}
.od .cd img{width:100%;height:100%;object-fit:cover;transition:transform 1.1s cubic-bezier(.2,.7,.2,1)}
.od .cd:hover img{transform:scale(1.04)}
.od .ov{position:absolute;inset:auto 0 0 0;padding:120px 28px 28px;background:linear-gradient(180deg,rgba(22,12,7,0) 0%,rgba(22,12,7,.82) 60%);color:#F4EDE4}
.od .ov .qm{color:#F2C79C}.od .ov figcaption span{color:#E6D6C4}
.od .soon{display:grid;place-items:center;padding:32px;background:#E9DBC6;color:var(--ink2);text-align:center;font:400 italic 22px/1.35 var(--display);font-variation-settings:'opsz' 20}
.od .foot{margin-top:28px}
""" + "".join(f'.od[data-f="{k}"] .tab[data-f="{k}"]{{background:var(--ink);color:#F4EDE4;border-color:var(--ink)}}'
              f'.od[data-f="{k}"] .cd:not(.c-{k}){{display:none}}' for k, _ in TABS) + """
@media (max-width:820px){.od .bar{flex-direction:column;align-items:flex-start}.od .arrows{display:none}.od .track{padding:6px 20px 20px;scroll-padding:0 20px;gap:12px}.od .cd{width:250px;height:360px}.od .cd.hasq{width:300px}.od .ov{padding:90px 20px 22px}.od .ov blockquote{font-size:18px}}
""", f"""<section class="og od" id="oameni" aria-labelledby="og-h" data-f="ateliere" ref="{{{{ rootRef }}}}">
<div class="wrap"><div class="head"><h2 class="disp" id="og-h">{H}</h2>{LINKS}</div>
<div class="bar"><div class="tabs" role="group" aria-label="Categorii">{d_tabs}</div>
<div class="arrows"><button class="rd pv" type="button" aria-label="Înapoi" data-d="-1" onClick="{{{{ scroll }}}}">{CHEV}</button><button class="rd nx" type="button" aria-label="Înainte" data-d="1" onClick="{{{{ scroll }}}}">{CHEV}</button></div></div></div>
<ul class="track" ref="{{{{ trackRef }}}}">{d_cards}</ul>
</section>""")

JS = """class Component extends DCLogic {
  componentDidMount() {
    var self = this, r = this.root, reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (r) {
      var tabs = r.querySelectorAll('.tab');
      for (var i = 0; i < tabs.length; i++) tabs[i].setAttribute('aria-pressed', String(tabs[i].getAttribute('data-f') === r.getAttribute('data-f')));
    }
    if (!r || reduce || !r.hasAttribute('data-rotate')) return;
    r.addEventListener('pointerenter', function () { self.hold = true; });
    r.addEventListener('pointerleave', function () { self.hold = false; });
    this.timer = setInterval(function () {
      if (self.hold || Date.now() - (self.last || 0) < 12000) return;
      r.setAttribute('data-a', String((parseInt(r.getAttribute('data-a'), 10) + 1) % 3));
    }, 7000);
  }
  componentWillUnmount() { clearInterval(this.timer); }
  renderVals() {
    var self = this;
    if (!this.cb) this.cb = {
      rootRef: function (el) { self.root = el; }, trackRef: function (el) { self.track = el; },
      pick: function (e) { self.last = Date.now(); self.root.setAttribute('data-a', e.currentTarget.getAttribute('data-i')); },
      step: function (e) {
        var n = parseInt(self.root.getAttribute('data-n'), 10), a = parseInt(self.root.getAttribute('data-a'), 10) + parseInt(e.currentTarget.getAttribute('data-d'), 10);
        self.root.setAttribute('data-a', String(Math.max(0, Math.min(n - 1, a))));
      },
      filter: function (e) {
        var f = e.currentTarget.getAttribute('data-f'); self.root.setAttribute('data-f', f);
        var tabs = self.root.querySelectorAll('.tab');
        for (var i = 0; i < tabs.length; i++) tabs[i].setAttribute('aria-pressed', String(tabs[i] === e.currentTarget));
        if (self.track) self.track.scrollLeft = 0;
      },
      scroll: function (e) { if (self.track) self.track.scrollBy({ left: 420 * parseInt(e.currentTarget.getAttribute('data-d'), 10), behavior: 'smooth' }); }
    };
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
        if name == "OameniB":
            continue  # oameni_banda.py owns B now
        for suffix, w, h in (("", 1440, 1200), ("Mobil", 390, 1800)):
            f = os.path.join(P, f"{name}{suffix}.dc.html")
            open(f, "w", encoding="utf-8").write(page(title + (" · mobil" if suffix else ""), css, html, w, h))
            if not suffix:
                subprocess.run([sys.executable, os.path.join(HERE, "dc2html.py"), f, os.path.join(HERE, f"opt-{name}.html")], check=True)
    names = list(OPTS)
    open(os.path.join(HERE, "oameni.html"), "w").write('<!doctype html><meta charset="utf-8"><title>Ce spun oamenii</title><style>body{margin:0}iframe{width:1440px;height:1300px;border:0;display:block}</style>' + "".join(f'<iframe src="opt-{n}.html"></iframe>' for n in names))
    open(os.path.join(HERE, "oameni-mobil.html"), "w").write('<!doctype html><meta charset="utf-8"><title>Ce spun oamenii mobil</title><style>body{margin:0;padding:10px;background:#1b1b1b;display:flex;gap:12px;color:#ddd;font:13px system-ui}figure{margin:0;flex:none}iframe{width:390px;height:2000px;border:0;display:block}</style>' + "".join(f'<figure><figcaption>{n}</figcaption><iframe src="opt-{n}.html"></iframe></figure>' for n in names))
