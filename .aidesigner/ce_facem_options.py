"""Homepage block 3, 'Ce oferim': four ways to show the five services (+ the schools line).

usage: python3 .aidesigner/ce_facem_options.py
writes .aidesigner/canvas/project/CeFacem1..4*.dc.html (+ Mobil twins) and local previews .aidesigner/opt-CeFacem*.html
Copy: docs/continut-site.md, the first line of each service page + its facts. Photos: crops of the one real workshop
photo + the hero clay, in natural colour (public/images/servicii/); placeholders until the photo shoot.
"""
import math, os, subprocess, sys
from about_options2 import P, HERE, FONTS, BASE_CSS, ARROW, DUO_SQ

GRUP = "/_blob/af69ff19bcdcf8c0410f4609e748d3a2"
COMPANII = "/_blob/42c18be93cd80d91d6d1d16793e790c6"
PRIVAT = "/_blob/5e489655abd7b9581fb23d21b13616c7"
RETREAT = "/_blob/84d195670e939aba045cc2966fe09dd9"

S = [  # order = 'for you' first, the team path last
    dict(k="grup", name="Ateliere de grup", line="În fiecare lună ne strângem în jurul lutului, cu o temă nouă de fiecare dată.",
         meta=["3 ore", "max. 8 persoane", "de la 200 lei"], cta="Vezi următoarele ateliere", img=GRUP, pos="50% 40%",
         alt="Participanți modelând lut în jurul mesei, la un atelier AVA"),
    dict(k="privat", name="Atelier privat 1:1", line="Lutul, tu și eu. Un atelier de modelaj, în ritmul tău, fără grup și fără grabă.",
         meta=["pentru adulți și copii", "de la 220 lei"], cta="Rezervă un atelier privat", img=PRIVAT, pos="50% 40%",
         alt="O participantă modelează lut la masa atelierului"),
    dict(k="consiliere", name="Consiliere 1:1", line="Te susțin în drumul tău și te ghidez spre versiunea ta autentică.",
         meta=["60–90 min", "online sau față în față", "180 lei / oră"], cta="Programează o ședință", img=DUO_SQ, pos="50% 30%",
         alt="Alessia Văideanu, consilier acreditat în dezvoltare personală"),
    dict(k="retreat", name="Retreaturi", line="Câteva zile departe de oraș, cu lut, natură, liniște și oameni care caută același lucru ca tine.",
         meta=["în curând"], cta="Anunță-mă la lansare", img=RETREAT, pos="50% 50%", alt="Lut sculptat în valuri, în nuanțe de teracotă"),
    dict(k="companii", name="Pentru companii", line="Ateliere de autocunoaștere și conectare pentru echipe, în care lutul este unealta.",
         meta=["4–16 persoane", "la voi sau în locații partenere", "ofertă personalizată"], cta="Cere o ofertă", img=COMPANII, pos="40% 50%",
         alt="Doi colegi modelează lut împreună"),
]
SCOLI = ("Pentru școli și copii", ["de la 6 ani", "60 min", "50 lei / copil"])
HEAD_P = "Pentru tine sau pentru echipa ta."


def meta(s, sep=" · "):
    return f'<span class="m">{sep.join(s["meta"])}</span>'


def more(label, cls="more"):
    return f'<span class="{cls}">{label} {ARROW}</span>'


SCOLI_LINK = f'<a class="sc" href="#scoli"><b>{SCOLI[0]}</b><span>{" · ".join(SCOLI[1])}</span>{ARROW}</a>'

COMMON = """
.cf{position:relative;background:var(--paper);padding:120px 0 128px;overflow:hidden}
.cf .head{display:flex;justify-content:space-between;align-items:flex-end;gap:40px;margin-bottom:56px}
.cf .head h2{font-size:clamp(44px,5vw,72px);line-height:1}
.cf .head p{margin:0;color:var(--ink2);font:400 italic 22px/1.3 var(--display);font-variation-settings:'opsz' 20}
.cf .m{display:block;font-size:14px;line-height:1.5;color:#833A22;font-variant-numeric:tabular-nums}
.cf .more{display:inline-flex;align-items:center;gap:10px;min-height:44px;font-weight:500;background:linear-gradient(currentColor,currentColor) 0 calc(100% - 9px)/100% 1px no-repeat;transition:background-size .3s cubic-bezier(.2,.7,.2,1)}
.cf a{text-decoration:none}
.cf a:hover .more{background-size:0 1px;background-position:100% calc(100% - 9px)}
.cf a:hover .ar{transform:translateX(4px)}
.cf .sc{display:inline-flex;align-items:center;flex-wrap:wrap;gap:6px 14px;min-height:44px;color:var(--ink)}
.cf .sc b{font:400 22px/1.2 var(--display);font-variation-settings:'opsz' 20}
.cf .sc span{font-size:14px;color:#833A22;font-variant-numeric:tabular-nums}
.cf .sc:hover .ar{transform:translateX(4px)}
@media (max-width:820px){.cf{padding:76px 0 84px}.cf .head{flex-direction:column;align-items:flex-start;gap:12px;margin-bottom:32px}.cf .head h2{font-size:clamp(40px,11vw,52px)}.cf .head p{font-size:20px}}
"""

OPTS = {}

# 1. Două drumuri: the 'for you' services as an editorial list; hovering a row swaps the photo in the frame beside it.
#    The team path gets its own dark clay band, so a company sees itself at a glance.
rows1 = "".join(
    f'<li class="row"><a href="#{s["k"]}" data-i="{i}" onMouseEnter="{{{{ pick }}}}" onFocus="{{{{ pick }}}}">'
    f'<img class="th" src="{s["img"]}" alt="" style="object-position:{s["pos"]}">'
    f'<span class="n">{s["name"]}</span><span class="l">{s["line"]}</span>{meta(s)}'
    f'<span class="go" aria-hidden="true">{ARROW}</span></a></li>' for i, s in enumerate(S[:4]))
frames1 = "".join(f'<img class="f{i}" src="{s["img"]}" alt="{s["alt"]}" style="object-position:{s["pos"]}">' for i, s in enumerate(S[:4]))
co = S[4]
OPTS["CeFacem1Drumuri"] = ("Ce oferim 1: două drumuri", """
.d1 .grid{display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:80px;align-items:start}
.d1 h3{margin:0 0 14px;font:400 italic 24px/1.2 var(--display);font-variation-settings:'opsz' 20;color:#833A22}
.d1 .list{list-style:none;margin:0;padding:0;border-top:1px solid rgba(58,42,32,.18)}
.d1 .row a{position:relative;display:grid;grid-template-columns:minmax(0,1fr) 48px;column-gap:28px;padding:26px 0 24px;border-bottom:1px solid rgba(58,42,32,.18);color:var(--ink)}
.d1 .row .th{display:none}
.d1 .n{grid-column:1;font:400 clamp(28px,2.7vw,40px)/1.08 var(--display);font-variation-settings:'opsz' 20;letter-spacing:-.01em;transition:transform .35s cubic-bezier(.2,.7,.2,1)}
.d1 .l{grid-column:1;margin-top:8px;color:var(--ink2);max-width:50ch;text-wrap:pretty}
.d1 .m{grid-column:1;margin-top:6px}
.d1 .go{grid-column:2;grid-row:1/4;align-self:center;display:grid;place-items:center;width:48px;height:48px;border-radius:50%;box-shadow:inset 0 0 0 1px rgba(58,42,32,.25);transition:background-color .3s,color .3s}
.d1 .list[data-a="0"] .row:nth-child(1) .n,.d1 .list[data-a="1"] .row:nth-child(2) .n,.d1 .list[data-a="2"] .row:nth-child(3) .n,.d1 .list[data-a="3"] .row:nth-child(4) .n{transform:translateX(10px)}
.d1 .list[data-a="0"] .row:nth-child(1) .go,.d1 .list[data-a="1"] .row:nth-child(2) .go,.d1 .list[data-a="2"] .row:nth-child(3) .go,.d1 .list[data-a="3"] .row:nth-child(4) .go{background:var(--ink);color:var(--paper)}
.d1 .frame{position:sticky;top:32px;margin:0;aspect-ratio:4/5;border-radius:26px;corner-shape:squircle;overflow:hidden;background:#C9A47E;box-shadow:0 40px 70px -44px rgba(58,42,32,.6)}
.d1 .frame img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transform:scale(1.05);transition:opacity .5s ease,transform 1.1s cubic-bezier(.2,.7,.2,1)}
.d1 .grid[data-a="0"] .f0,.d1 .grid[data-a="1"] .f1,.d1 .grid[data-a="2"] .f2,.d1 .grid[data-a="3"] .f3{opacity:1;transform:none}
.d1 .team{margin-top:104px;position:relative;background:#2E1D14;color:#F4EDE4;border-radius:30px;corner-shape:squircle;overflow:hidden;display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);align-items:stretch}
.d1 .team img{display:block;width:100%;height:100%;min-height:380px;object-fit:cover}
.d1 .team .tx{padding:60px 64px;display:flex;flex-direction:column;justify-content:center;align-items:flex-start}
.d1 .team h3{color:var(--glowc)}
.d1 .team .tn{margin:0;font:400 clamp(34px,3.4vw,50px)/1.05 var(--display);font-variation-settings:'opsz' 20}
.d1 .team .l{margin:14px 0 0;color:#E6D7C4;max-width:46ch}
.d1 .team .m{margin-top:10px;color:var(--glowc)}
.d1 .btn{display:inline-flex;align-items:center;gap:10px;min-height:48px;margin-top:28px;padding:0 24px;border-radius:999px;background:#F4EDE4;color:#2E1D14;font-weight:500;transition:background-color .25s}
.d1 .btn:hover{background:#fff}
.d1 .team .sc{margin-top:18px;color:#F4EDE4}
.d1 .team .sc span{color:var(--glowc)}
@media (max-width:820px){.d1 .grid{grid-template-columns:1fr;gap:0}.d1 .frame{display:none}.d1 .row a{grid-template-columns:76px minmax(0,1fr);column-gap:16px;padding:20px 0}.d1 .row .th{display:block;grid-row:1/4;width:76px;height:96px;border-radius:14px;object-fit:cover}.d1 .n,.d1 .l,.d1 .m{grid-column:2}.d1 .n{font-size:26px}.d1 .l{font-size:15.5px}.d1 .go{display:none}.d1 .list .row .n{transform:none!important}.d1 .team{grid-template-columns:1fr;margin-top:64px;border-radius:24px}.d1 .team img{min-height:0;aspect-ratio:16/10}.d1 .team .tx{padding:32px 24px 36px}}
@media (prefers-reduced-motion:reduce){.d1 .frame img{transform:none}}
""", f"""<section class="cf d1" id="ce-facem" aria-labelledby="cf-h">
<div class="wrap">
<div class="head"><h2 class="disp" id="cf-h">Ce oferim</h2><p>{HEAD_P}</p></div>
<div class="grid" data-a="0" ref="{{{{ gridRef }}}}">
<div><h3>Pentru tine</h3><ul class="list" data-a="0" ref="{{{{ listRef }}}}">{rows1}</ul></div>
<figure class="frame" aria-hidden="true">{frames1}</figure>
</div>
<div class="team"><img src="{co['img']}" alt="{co['alt']}" style="object-position:{co['pos']}">
<div class="tx"><h3>Pentru echipa ta</h3><p class="tn">{co['name']}</p><p class="l">{co['line']}</p>{meta(co)}
<a class="btn" href="#companii">{co['cta']} {ARROW}</a>{SCOLI_LINK}</div></div>
</div>
</section>""", "pick")

# 2. Galeria: one horizontal shelf of tall photo cards (group workshops twice as wide), swipe on phones, arrows on desktop.
cards2 = "".join(
    f'<li class="card{" big" if i == 0 else ""}"><a href="#{s["k"]}"><span class="ph"><img src="{s["img"]}" alt="{s["alt"]}" style="object-position:{s["pos"]}"></span>'
    f'{meta(s)}<span class="n">{s["name"]}</span><span class="l">{s["line"]}</span>{more(s["cta"])}</a></li>'
    for i, s in enumerate([S[0], S[1], S[2], S[4], S[3]]))
OPTS["CeFacem2Galerie"] = ("Ce oferim 2: galerie orizontală", """
.d2 .head .side{display:flex;align-items:center;gap:28px}
.d2 .arrows{display:flex;gap:10px}
.d2 .arrows button{display:grid;place-items:center;width:52px;height:52px;border:0;border-radius:50%;background:transparent;color:var(--ink);box-shadow:inset 0 0 0 1px rgba(58,42,32,.3);cursor:pointer;transition:background-color .25s,color .25s}
.d2 .arrows button:hover{background:var(--ink);color:var(--paper)}
.d2 .arrows button:focus-visible{outline:2px solid var(--terra-d);outline-offset:3px}
.d2 .arrows .prev .ar{transform:scaleX(-1)}
.d2 .track{display:flex;gap:28px;margin:0;padding:0 max(40px,calc(50% - 580px)) 8px;list-style:none;overflow-x:auto;scroll-snap-type:x mandatory;scroll-padding:0 max(40px,calc(50% - 580px));scrollbar-width:none;overscroll-behavior-x:contain}
.d2 .track::-webkit-scrollbar{display:none}
.d2 .card{flex:0 0 340px;scroll-snap-align:start}
.d2 .card.big{flex-basis:560px}
.d2 .card a{display:flex;flex-direction:column;color:var(--ink)}
.d2 .ph{display:block;height:450px;border-radius:24px;corner-shape:squircle;overflow:hidden;background:#C9A47E;margin-bottom:22px}
.d2 .ph img{display:block;width:100%;height:100%;object-fit:cover;transition:transform 1s cubic-bezier(.2,.7,.2,1)}
.d2 .card a:hover .ph img{transform:scale(1.04)}
.d2 .n{margin-top:6px;font:400 32px/1.1 var(--display);font-variation-settings:'opsz' 20;letter-spacing:-.01em}
.d2 .l{margin-top:10px;color:var(--ink2);font-size:16px;line-height:1.55;text-wrap:pretty}
.d2 .more{margin-top:10px;align-self:flex-start}
.d2 .foot{margin-top:44px;padding-top:22px;border-top:1px solid rgba(58,42,32,.18)}
@media (max-width:820px){.d2 .arrows{display:none}.d2 .track{gap:16px;padding:0 20px 8px;scroll-padding:0 20px}.d2 .card,.d2 .card.big{flex-basis:78vw}.d2 .ph{height:auto;aspect-ratio:4/5}.d2 .n{font-size:28px}}
@media (prefers-reduced-motion:reduce){.d2 .ph img{transition:none}}
""", f"""<section class="cf d2" id="ce-facem" aria-labelledby="cf-h">
<div class="wrap head"><h2 class="disp" id="cf-h">Ce oferim</h2><div class="side"><p>{HEAD_P}</p>
<div class="arrows"><button class="prev" type="button" aria-label="Înapoi" onClick="{{{{ prev }}}}">{ARROW}</button><button type="button" aria-label="Înainte" onClick="{{{{ next }}}}">{ARROW}</button></div></div></div>
<ul class="track" ref="{{{{ trackRef }}}}" aria-label="Serviciile AVA">{cards2}</ul>
<div class="wrap"><div class="foot">{SCOLI_LINK}</div></div>
</section>""", "scroll")

# 3. Prim-plan: the monthly group workshop is the front door, so it takes the big photo; the rest line up beside it.
s0 = S[0]
rows3 = "".join(
    f'<li><a href="#{s["k"]}"><img src="{s["img"]}" alt="" style="object-position:{s["pos"]}"><span class="tx"><span class="n">{s["name"]}</span>'
    f'<span class="l">{s["line"]}</span>{meta(s)}</span></a></li>' for s in [S[4], S[1], S[2], S[3]])
OPTS["CeFacem3PrimPlan"] = ("Ce oferim 3: prim-plan", """
.d3 .grid{display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:56px;align-items:stretch}
.d3 .feat{position:relative;display:flex;flex-direction:column;justify-content:flex-end;min-height:680px;border-radius:30px;corner-shape:squircle;overflow:hidden;color:#F4EDE4;isolation:isolate}
.d3 .feat img{position:absolute;inset:0;z-index:-2;width:100%;height:100%;object-fit:cover;transition:transform 1.2s cubic-bezier(.2,.7,.2,1)}
.d3 .feat::after{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(180deg,rgba(30,16,10,0) 30%,rgba(30,16,10,.55) 58%,rgba(30,16,10,.88) 100%)}
.d3 .feat:hover img{transform:scale(1.03)}
.d3 .feat .tx{padding:48px 52px}
.d3 .feat .m{color:var(--glowc)}
.d3 .feat .n{display:block;margin-top:8px;font:400 clamp(40px,4vw,60px)/1.02 var(--display);font-variation-settings:'opsz' 20;letter-spacing:-.015em}
.d3 .feat .l{display:block;margin-top:14px;max-width:40ch;color:#EFE3D3;font-size:18px}
.d3 .btn{display:inline-flex;align-items:center;gap:10px;min-height:48px;margin-top:26px;padding:0 24px;border-radius:999px;background:#F4EDE4;color:#2E1D14;font-weight:500}
.d3 .side{display:flex;flex-direction:column}
.d3 .side ul{list-style:none;margin:0;padding:0;border-top:1px solid rgba(58,42,32,.18)}
.d3 .side ul a{display:grid;grid-template-columns:104px minmax(0,1fr);gap:22px;align-items:center;padding:20px 0;border-bottom:1px solid rgba(58,42,32,.18);color:var(--ink)}
.d3 .side img{width:104px;height:124px;border-radius:16px;object-fit:cover;transition:transform .5s cubic-bezier(.2,.7,.2,1)}
.d3 .side ul a:hover img{transform:scale(.96) rotate(-2deg)}
.d3 .side .n{display:block;font:400 26px/1.1 var(--display);font-variation-settings:'opsz' 20}
.d3 .side .l{display:block;margin-top:6px;color:var(--ink2);font-size:15px;line-height:1.5}
.d3 .side .m{margin-top:4px;font-size:13.5px}
.d3 .side .sc{margin-top:auto;padding-top:22px}
@media (max-width:820px){.d3 .grid{grid-template-columns:1fr;gap:28px}.d3 .feat{min-height:540px;border-radius:24px}.d3 .feat .tx{padding:28px 24px}.d3 .side ul a{grid-template-columns:84px minmax(0,1fr);gap:16px}.d3 .side img{width:84px;height:104px}}
""", f"""<section class="cf d3" id="ce-facem" aria-labelledby="cf-h">
<div class="wrap">
<div class="head"><h2 class="disp" id="cf-h">Ce oferim</h2><p>{HEAD_P}</p></div>
<div class="grid">
<a class="feat" href="#{s0['k']}"><img src="{s0['img']}" alt="{s0['alt']}" style="object-position:{s0['pos']}"><span class="tx">{meta(s0)}<span class="n">{s0['name']}</span><span class="l">{s0['line']}</span><span class="btn">{s0['cta']} {ARROW}</span></span></a>
<div class="side"><ul>{rows3}</ul>{SCOLI_LINK}</div>
</div>
</div>
</section>""", None)


# 4. Ștampile: no photos yet, so each service is a ceramic stamp, like the one in the hero, pressed at a slight angle.
def pot(cx, top, w, h):
    n, b = w * .26, w * .5
    return (f"M{cx - n:.1f} {top:.1f}H{cx + n:.1f}M{cx - n * .8:.1f} {top:.1f}C{cx - n * .8:.1f} {top + h * .18:.1f} {cx - b:.1f} {top + h * .3:.1f} {cx - b:.1f} {top + h * .62:.1f}"
            f"C{cx - b:.1f} {top + h * .86:.1f} {cx - b * .6:.1f} {top + h:.1f} {cx:.1f} {top + h:.1f}C{cx + b * .6:.1f} {top + h:.1f} {cx + b:.1f} {top + h * .86:.1f} {cx + b:.1f} {top + h * .62:.1f}"
            f"C{cx + b:.1f} {top + h * .3:.1f} {cx + n * .8:.1f} {top + h * .18:.1f} {cx + n * .8:.1f} {top:.1f}")


GLYPH = {
    "grup": pot(20, 25, 14, 18) + pot(32, 19, 18, 24) + pot(44, 25, 14, 18),
    "privat": pot(32, 16, 24, 30) + "M24 33Q32 36 40 33",
    "consiliere": "M21 24a5 5 0 1 0 0.01 0M43 24a5 5 0 1 0 0.01 0M12 45c0-8 4-12 9-12s9 4 9 12M34 45c0-8 4-12 9-12s9 4 9 12",
    "retreat": "M32 22a7 7 0 1 0 0.01 0M12 36q5-4 10 0t10 0t10 0t10 0M12 43q5-4 10 0t10 0t10 0t10 0M12 50q5-4 10 0t10 0t10 0t10 0",
    "companii": "M32 32m-11 0a11 11 0 1 0 22 0a11 11 0 1 0 -22 0" + "".join(
        f"M{32 + 17 * math.cos(a):.1f} {32 + 17 * math.sin(a):.1f}m-2.4 0a2.4 2.4 0 1 0 4.8 0a2.4 2.4 0 1 0 -4.8 0"
        for a in [i * math.pi / 3 + math.pi / 6 for i in range(6)]),
}
ROT = [-6, 4, -3, 6, -4]
SHORT = dict(grup="Vezi atelierele", privat="Rezervă", consiliere="Programează", retreat="Anunță-mă", companii="Cere o ofertă")


def stamp(s, i):
    r = 41
    ring = f"{s['name'].upper()} · {s['name'].upper()} ·".replace("&", "&amp;")
    dark = s["k"] == "companii"
    return (f'<svg class="st{" dk" if dark else ""}" viewBox="0 0 100 100" aria-hidden="true" style="--r:{ROT[i]}deg">'
            f'<circle cx="50" cy="50" r="48" class="disc"></circle><circle cx="50" cy="50" r="33" class="in"></circle>'
            f'<defs><path id="sp{i}" d="M50 50m-{r} 0a{r} {r} 0 1 1 {2 * r} 0a{r} {r} 0 1 1 -{2 * r} 0"></path></defs>'
            f'<text class="rt"><textPath href="#sp{i}" textLength="{2 * math.pi * r - 3:.1f}" lengthAdjust="spacing">{ring}</textPath></text>'
            f'<g transform="translate(27 27) scale(.72)"><path class="gl" d="{GLYPH[s["k"]]}"></path></g></svg>')


cols4 = "".join(
    f'<li class="{"team" if s["k"] == "companii" else ""}"><a href="#{s["k"]}">{stamp(s, i)}<span class="tx"><span class="n">{s["name"]}</span>'
    f'<span class="l">{s["line"]}</span>{meta(s)}{more(SHORT[s["k"]])}</span></a></li>' for i, s in enumerate(S))
OPTS["CeFacem4Stampile"] = ("Ce oferim 4: ștampile", """
.d4{background:radial-gradient(ellipse 70% 60% at 50% 0%,#FAF5EE 0%,rgba(250,245,238,0) 70%),var(--paper)}
.d4 .row{display:grid;grid-template-columns:repeat(4,minmax(0,1fr)) 1px minmax(0,1.1fr);gap:0 28px;margin:0;padding:0;list-style:none}
.d4 .row::before{content:"";grid-column:5;grid-row:1;background:rgba(58,42,32,.18)}
.d4 .row li{grid-row:1}
.d4 .row li.team{grid-column:6}
.d4 li a{display:flex;flex-direction:column;color:var(--ink)}
.d4 .st{display:block;width:100%;max-width:176px;aspect-ratio:1;margin:0 0 28px -6px;transform:rotate(var(--r));transition:transform .45s cubic-bezier(.2,.7,.2,1),filter .45s;filter:drop-shadow(0 14px 18px rgba(58,42,32,.22))}
.d4 li a:hover .st,.d4 li a:focus-visible .st{transform:rotate(0) scale(.96);filter:drop-shadow(0 4px 6px rgba(58,42,32,.25))}
.d4 .disc{fill:#E6D5BD;stroke:rgba(58,42,32,.22);stroke-width:.6px}
.d4 .in{fill:none;stroke:#9C472C;stroke-width:.7px}
.d4 .rt{font:600 6.1px var(--text);letter-spacing:.06em;fill:#3A2A20}
.d4 .gl{fill:none;stroke:#9C472C;stroke-width:2.1px;stroke-linecap:round;stroke-linejoin:round}
.d4 .st.dk .disc{fill:#3A2A20;stroke:none}.d4 .st.dk .in{stroke:#F2C79C}.d4 .st.dk .rt{fill:#F4EDE4}.d4 .st.dk .gl{stroke:#F2C79C}
.d4 .n{font:400 27px/1.1 var(--display);font-variation-settings:'opsz' 20;letter-spacing:-.01em}
.d4 .l{display:block;margin-top:10px;color:var(--ink2);font-size:15.5px;line-height:1.55;text-wrap:pretty}
.d4 .m{margin-top:10px;font-size:13.5px}
.d4 .more{margin-top:8px}
.d4 .foot{margin-top:56px;padding-top:22px;border-top:1px solid rgba(58,42,32,.18);display:flex;justify-content:space-between;align-items:center;gap:24px}
.d4 .foot i{font:400 italic 20px/1.3 var(--display);color:#833A22}
@media (max-width:1100px){.d4 .row{grid-template-columns:1fr;gap:0}.d4 .row::before{display:none}.d4 .row li,.d4 .row li.team{grid-column:1;grid-row:auto}.d4 li a{display:grid;grid-template-columns:104px minmax(0,1fr);gap:20px;align-items:start;padding:22px 0;border-bottom:1px solid rgba(58,42,32,.16)}.d4 .st{margin:0;max-width:104px}.d4 .n{font-size:26px}.d4 .foot{flex-direction:column;align-items:flex-start}}
""", f"""<section class="cf d4" id="ce-facem" aria-labelledby="cf-h">
<div class="wrap">
<div class="head"><h2 class="disp" id="cf-h">Ce oferim</h2><p>{HEAD_P}</p></div>
<ul class="row">{cols4}</ul>
<div class="foot"><i>Și pentru cei mici:</i>{SCOLI_LINK}</div>
</div>
</section>""", None)

JS = {
    "pick": """class Component extends DCLogic {
  renderVals() {
    var self = this;
    if (!this.cb) this.cb = {
      gridRef: function (el) { self.grid = el; },
      listRef: function (el) { self.list = el; },
      pick: function (e) {
        var i = e.currentTarget.getAttribute('data-i');
        if (self.grid) self.grid.setAttribute('data-a', i);
        if (self.list) self.list.setAttribute('data-a', i);
      }
    };
    return this.cb;
  }
}""",
    "scroll": """class Component extends DCLogic {
  renderVals() {
    var self = this;
    var go = function (dir) {
      if (!self.track) return;
      var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      self.track.scrollBy({ left: dir * 368, behavior: reduce ? 'auto' : 'smooth' });
    };
    if (!this.cb) this.cb = {
      trackRef: function (el) { self.track = el; },
      prev: function () { go(-1); },
      next: function () { go(1); }
    };
    return this.cb;
  }
}""",
    None: "class Component extends DCLogic {\n  renderVals() { return {}; }\n}",
}


def page(title, css, html, js, w, h):
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
{JS[js]}
</script>
</body>
</html>
"""


if __name__ == "__main__":
    for name, (title, css, html, js) in OPTS.items():
        for suffix, w, h in (("", 1440, 1200), ("Mobil", 390, 1800)):
            f = os.path.join(P, f"{name}{suffix}.dc.html")
            open(f, "w", encoding="utf-8").write(page(title + (" · mobil" if suffix else ""), css, html, js, w, h))
            if not suffix:
                subprocess.run([sys.executable, os.path.join(HERE, "dc2html.py"), f, os.path.join(HERE, f"opt-{name}.html")], check=True)
    names = list(OPTS)
    open(os.path.join(HERE, "cefacem.html"), "w").write('<!doctype html><meta charset="utf-8"><title>Ce oferim</title><style>body{margin:0}iframe{width:1440px;height:1500px;border:0;display:block}</style>' + "".join(f'<iframe src="opt-{n}.html"></iframe>' for n in names))
    open(os.path.join(HERE, "cefacem-mobil.html"), "w").write('<!doctype html><meta charset="utf-8"><title>Ce oferim mobil</title><style>body{margin:0;padding:10px;background:#1b1b1b;display:flex;gap:12px;color:#ddd;font:13px system-ui}figure{margin:0}iframe{width:390px;height:2200px;border:0;display:block}</style>' + "".join(f'<figure><figcaption>{n}</figcaption><iframe src="opt-{n}.html"></iframe></figure>' for n in names))
