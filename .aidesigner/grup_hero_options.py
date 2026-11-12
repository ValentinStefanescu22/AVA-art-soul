"""Subpaginile „Ce oferim”, part 1: the opening of a service page, built on „Ateliere de grup” (Vali, 12 nov).
The template for all six service pages is designed on this one, section by section. Four directions, each from a real site.

usage: python3 .aidesigner/grup_hero_options.py
writes .aidesigner/canvas/project/GrupHero1..4*.dc.html (+ Mobil twins) and local previews .aidesigner/opt-GrupHero*.html

Copy: docs/continut-site.md, „Ateliere de grup” (intro sentence, facts) and „Evenimente” (the 15 noiembrie card).
No exact address (CLAUDE.md): „Cotroceni, București”. Button: the label Vali approved on Ce oferim 1, „Vezi următoarele ateliere”.
Photos: all four are real, from the October workshop. Motion per DESIGN.md §8: one load moment, then nothing; reduced motion = still.
"""
import os, subprocess, sys
from about_options2 import P, HERE, FONTS, BASE_CSS, ARROW
from header_options import HX_CSS, V
from cf_pagina_options import header, script, eased_gradient

TITLE = "Ateliere de grup"
LEDE = "În fiecare lună ne strângem în jurul lutului, cu o temă nouă de fiecare dată. Lucrăm cu mâinile, vorbim, ne ascultăm. Nu ai nevoie de experiență, doar de curiozitate."
FACTS = [("Cum funcționează", "atelier lunar, 3 ore, temă diferită"), ("Grup", "maxim 8 persoane, ca să rămână intim"),
         ("Preț", "de la 200 lei / persoană (variază după temă)"), ("Unde", "Cotroceni, București")]
SHORT = ["în fiecare lună", "3 ore", "maxim 8 persoane", "Cotroceni, București"]
# Vali (12 nov): the page lists every upcoming workshop; button wording from Vali's own canvas edit on Ce oferim 1
CTA = "Vezi următoarele ateliere"
EVENTS = [  # docs/continut-site.md, Evenimente; [..] = not known yet
    dict(day="15", mon="noiembrie", mo="nov", wd="duminică", time="ora 17:00", title="Atelier de ceramică &amp; socializare",
         line="O seară liniștită cu lut, culoare și oameni noi. Modelăm împreună, apoi îți pictezi piesa cu underglaze, culori speciale pentru ceramică, iar între timp povestim și ne bucurăm de o băutură și o gustare făcute în casă.",
         where="Cotroceni, sector 5", price="200 lei", incl="materiale, îndrumare, băutură și gustare făcute în casă", sold=True),
    dict(day="6", mon="decembrie", mo="dec", wd="duminică", time="[ORA]", title="Atelier cu tematică de Crăciun",
         line="În spiritul sărbătorilor: ceramică și pictură pe ceramică în același atelier, cu pauze de socializare și gustări.",
         where="[LOCAȚIA]", price="200 lei", incl="ceramică + pictură pe ceramică, gustări", sold=False),
    dict(day="13", mon="decembrie", mo="dec", wd="duminică", time="[ORA]", title="Atelier cu tematică de Crăciun",
         line="În spiritul sărbătorilor: ceramică și pictură pe ceramică în același atelier, cu pauze de socializare și gustări.",
         where="[LOCAȚIA]", price="200 lei", incl="ceramică + pictură pe ceramică, gustări", sold=False),
]


def dates_html(cls="dl"):
    """the upcoming dates, short: „dum. 15 nov · Sold out”"""
    return f'<ul class="{cls}">' + "".join(
        f'<li><span>{e["wd"][:3]}. {e["day"]} {e["mo"]}</span>' + ('<span class="so">Sold out</span>' if e["sold"] else '<span class="ok">locuri libere</span>') + "</li>"
        for e in EVENTS) + "</ul>"

# real photos, October workshop
ROOM = ("/_blob/988e3a505fd5ae1db56d481b3d1e33b1", "Masa lungă de la atelierul din octombrie: opt oameni modelează lut, cu ceai și gustări între ei", "50% 55%")
ROOM2 = ("/_blob/af69ff19bcdcf8c0410f4609e748d3a2", "Participanți aplecați peste bucățile de lut, la masa atelierului", "50% 60%")
BOWL = ("/_blob/42c18be93cd80d91d6d1d16793e790c6", "Doi participanți își arată un bol de lut abia modelat", "50% 40%")
CLAY = ("/_blob/27d62de5381eeee8e9ab504567023c22", "Mâini care modelează un bol de lut", "50% 50%")   # provisional (Unsplash), until more workshop photos
HANDS = ("/_blob/5e489655abd7b9581fb23d21b13616c7", "O participantă concentrată pe piesa ei de lut", "50% 35%")

SOURCES = {
    "GrupHero1Galerie": "airbnb.com/experiences: galeria de poze sus, apoi detaliile și cardul de rezervare care stă lângă text",
    "GrupHero2Aman": "aman.com: fotografia pe tot ecranul, titlul centrat, totul foarte liniștit",
    "GrupHero3Continuare": "apple.com, paginile de produs: o deschidere închisă care se luminează lin spre fotografie (aici, ca pagina „Ce oferim”)",
    "GrupHero4Invitatie": "lu.ma: pagina unui eveniment, cu coperta pătrată în stânga și invitația în dreapta",
}


def pic(p, cls="", extra=""):
    src, alt, pos = p
    return f'<img class="{cls}" src="{src}" alt="{alt}" style="object-position: {pos}"{extra}>'


def h1(cls=""):
    k, ws = 0, []
    for w in TITLE.split():
        ls = []
        for ch in w:
            ls.append(f'<span class="l" style="--k: {k}">{ch}</span>'); k += 1
        ws.append('<span class="w" aria-hidden="true">' + "".join(ls) + "</span>")
    return f'<h1 class="disp gh {cls}" id="gh-h" aria-label="{TITLE}">' + " ".join(ws) + "</h1>"


def cta(cls="btn"):
    return f'<a class="{cls}" href="#ateliere">{CTA}</a>'   # Vali (12 nov): solid buttons carry no arrow


COMMON = """
.gp{position:relative;overflow:clip;--so:cubic-bezier(.22,1,.36,1)}
.gp a{text-decoration:none}
.gh{font-size:clamp(60px,7.4vw,108px);line-height:.98;letter-spacing:-.022em;font-variation-settings:'opsz' 72}
.gh .w{display:inline-block;white-space:nowrap}.gh .l{display:inline-block}
.gp .lede{margin:0;font:400 clamp(20px,1.7vw,24px)/1.45 var(--display);font-variation-settings:'opsz' 20;text-wrap:pretty}
.gp .btn{display:inline-flex;align-items:center;justify-content:center;gap:12px;min-height:52px;padding:0 28px;border-radius:999px;background:#9C472C;color:#F8F1E8;font:500 15px/1 var(--text);letter-spacing:.02em;transition:background-color .25s ease,translate .2s var(--so)}
.gp .btn:hover{background:#833A22}.gp .btn:hover .ar{transform:translateX(4px)}
.gp .btn:active{translate:0 1px}
.gp .btn:focus-visible{outline:2px solid #9C472C;outline-offset:3px}
.gp .meta{display:flex;flex-wrap:wrap;gap:6px 0;margin:0;padding:0;list-style:none;font-size:15px;color:var(--ink2);font-variant-numeric:tabular-nums}
.gp .meta li:not(:last-child)::after{content:"·";margin:0 10px}
.gp img{display:block;width:100%;height:100%;object-fit:cover}
@keyframes gh-l{from{opacity:0;translate:0 .4em;filter:blur(8px)}}
@keyframes gh-up{from{opacity:0;translate:0 16px}}
@keyframes gh-uncover{from{clip-path:inset(100% 0 0 0 round 22px)}}
@media (prefers-reduced-motion:no-preference){
  .gh .l{animation:gh-l 1s var(--so) backwards;animation-delay:calc(.1s + var(--k) * 40ms)}
  .gp .up{animation:gh-up .8s var(--so) backwards;animation-delay:var(--d,.5s)}
}
@media (max-width:980px){.gh{font-size:clamp(48px,13.5vw,72px)}.gp .meta{font-size:14px}}
@media (prefers-reduced-motion:reduce){.gp *{animation:none!important;transition:none!important}}
"""

OPTS = {}

# 1. Airbnb Experiences: title and facts on top, a mosaic of the real photos, then the intro beside a booking card.
OPTS["GrupHero1Galerie"] = ("Ateliere de grup 1: galerie + card de rezervare", "light", """
.g1{background:#F4EDE4;padding:132px 0 96px}
.g1 .top{display:flex;align-items:end;justify-content:space-between;gap:24px 48px;flex-wrap:wrap}
.g1 .meta{margin-bottom:14px}
.g1 .mos{display:grid;grid-template-columns:2fr 1fr 1fr;grid-template-rows:220px 220px;gap:8px;margin-top:40px;border-radius:22px;corner-shape:squircle;overflow:hidden}
.g1 .mos figure{margin:0;overflow:hidden}
.g1 .mos .a{grid-row:1/3}.g1 .mos .b{grid-row:1/3}
.g1 .mos img{transition:transform 1.2s var(--so)}
@media (hover:hover){.g1 .mos figure:hover img{transform:scale(1.04)}}
@media (prefers-reduced-motion:no-preference){.g1 .mos figure{animation:gh-uncover 1.1s var(--so) backwards;animation-delay:calc(.35s + var(--i) * 110ms)}}
.g1 .low{display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:56px;margin-top:56px;align-items:start}
.g1 .facts{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:22px 36px;margin:36px 0 0;padding:30px 0 0;border-top:1px solid rgba(58,42,32,.16)}
.g1 .facts dt{font:400 italic 19px/1.3 var(--display);font-variation-settings:'opsz' 20;color:var(--terra-d)}
.g1 .facts dd{margin:4px 0 0;font-size:16px;line-height:1.55;color:#4A382C}
.g1 .card{position:sticky;top:96px;padding:30px 30px 28px;border-radius:22px;corner-shape:squircle;background:#FBF7F1;box-shadow:0 0 0 1px rgba(58,42,32,.06),0 24px 48px -36px rgba(70,35,15,.45)}
.g1 .card .pr{margin:0;font:400 40px/1 var(--display);font-variation-settings:'opsz' 20;font-variant-numeric:tabular-nums}
.g1 .card .pr small{font:400 16px/1 var(--text);color:var(--ink2);margin-left:6px}.g1 .card .pr .from{margin:0 8px 0 0}
.g1 .card .note{margin:10px 0 22px;font-size:14.5px;color:var(--ink2)}
.g1 .card .btn{width:100%;justify-content:center;box-sizing:border-box}
.g1 .card .nx{margin-top:22px;padding-top:18px;border-top:1px solid rgba(58,42,32,.12);font-size:14px;color:var(--ink2)}
.g1 .card .nx>p{margin:0 0 6px;font:400 italic 18px/1.3 var(--display);font-variation-settings:'opsz' 20;color:var(--ink)}
.gp .dl{margin:0;padding:0;list-style:none}
.gp .dl li{display:flex;justify-content:space-between;align-items:center;gap:12px;min-height:40px;border-bottom:1px solid rgba(58,42,32,.08);font-variant-numeric:tabular-nums}
.gp .dl li:last-child{border-bottom:0}
.gp .dl .so{flex:none;display:inline-flex;align-items:center;min-height:26px;padding:0 11px;border-radius:999px;border:1px solid #9C472C;color:#9C472C;font-size:12.5px;font-weight:600}
.gp .dl .ok{font-size:13px;color:#4F5A43}
@media (max-width:980px){
  .g1{padding:104px 0 64px}
  .g1 .mos{grid-template-columns:1fr 1fr;grid-template-rows:240px 150px;margin-top:28px;border-radius:18px}
  .g1 .mos .a{grid-column:1/3;grid-row:auto}.g1 .mos .b{grid-row:auto}.g1 .mos .d{display:none}
  .g1 .low{grid-template-columns:1fr;gap:32px;margin-top:32px}
  .g1 .facts{grid-template-columns:1fr;gap:16px;margin-top:28px;padding-top:24px}
  .g1 .card{position:static;padding:24px 22px}
}
""", '<section class="gp g1" aria-labelledby="gh-h" ref="{{ secRef }}"><div class="wrap">'
    f'<div class="top">{h1()}<ul class="meta up" style="--d: .45s">{"".join(f"<li>{m}</li>" for m in SHORT)}</ul></div>'
    f'<div class="mos"><figure class="a" style="--i: 0">{pic(ROOM)}</figure><figure class="b" style="--i: 1">{pic(BOWL)}</figure>'
    f'<figure class="c" style="--i: 2">{pic(HANDS)}</figure><figure class="d" style="--i: 3">{pic(CLAY)}</figure></div>'
    f'<div class="low"><div class="up" style="--d: .7s"><p class="lede">{LEDE}</p><dl class="facts">'
    + "".join(f"<div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in FACTS) + '</dl></div>'
    f'<aside class="card up" style="--d: .85s" aria-label="Rezervare"><p class="pr"><small class="from">de la</small>200 lei<small>/ persoană</small></p>'
    f'<p class="note">Locul se confirmă după plată.</p>{cta()}'
    f'<div class="nx"><p>Atelierele care urmează</p>{dates_html()}</div></aside></div>'
    '</div></section>')

# 2. Aman: one real photo, full screen, a warm veil, the title centred and quiet; the photo melts into the page below.
OPTS["GrupHero2Aman"] = ("Ateliere de grup 2: fotografie pe tot ecranul", "dark", """
.g2{position:relative;min-height:860px;display:flex;align-items:center;justify-content:center;text-align:center;color:#F4EDE4;background:#2E1C13;isolation:isolate}
.g2 .bg{position:absolute;inset:0;z-index:-2;overflow:hidden}
.g2 .bg img{object-position:50% 55%}
@keyframes g2-settle{from{transform:scale(1.08)}}
@media (prefers-reduced-motion:no-preference){.g2 .bg img{animation:g2-settle 2.4s var(--so) backwards}}
/* veil: darker behind the text, then the photo eases into the paper of the next section (eased, no band) */
.g2::before{content:"";position:absolute;inset:0;z-index:-1;background:radial-gradient(ellipse 60% 52% at 50% 46%,rgba(28,14,8,.74) 0%,rgba(28,14,8,.52) 70%,rgba(28,14,8,.4) 100%)}
.g2::after{content:"";position:absolute;left:0;right:0;bottom:0;height:300px;z-index:-1;background:linear-gradient(180deg,rgba(244,237,228,0) 0%,rgba(244,237,228,.03) 18%,rgba(244,237,228,.12) 36%,rgba(244,237,228,.3) 54%,rgba(244,237,228,.56) 70%,rgba(244,237,228,.8) 84%,rgba(244,237,228,.95) 94%,#F4EDE4 100%)}
.g2 .in{max-width:760px;padding:150px 24px 230px}
.g2 .lede{margin:26px auto 0;max-width:36ch;color:#EFE3D3}
.g2 .pills{display:flex;justify-content:center;flex-wrap:wrap;gap:8px;margin:28px 0 0;padding:0;list-style:none}
.g2 .pills li{display:inline-flex;align-items:center;min-height:36px;padding:0 16px;border-radius:999px;background:rgba(244,237,228,.1);box-shadow:inset 0 0 0 1px rgba(244,237,228,.32);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);font-size:14.5px;font-variant-numeric:tabular-nums}
.g2 .btn{margin-top:34px;background:#F4EDE4;color:#2E1D14}
.g2 .btn:hover{background:#FFF8EE}
.g2 .btn:focus-visible{outline-color:#F2C79C}
@media (max-width:980px){.g2 .bg img{object-position:12% 55%}.g2{min-height:780px}.g2 .in{padding:128px 20px 200px}.g2::after{height:220px}.g2 .lede{font-size:19px}}
""", '<section class="gp g2" aria-labelledby="gh-h" ref="{{ secRef }}">'
    f'<div class="bg">{pic(ROOM)}</div><div class="in">{h1()}'
    f'<p class="lede up" style="--d: .55s">{LEDE}</p>'
    f'<ul class="pills up" style="--d: .7s">{"".join(f"<li>{m}</li>" for m in ["în fiecare lună", "3 ore", "gustare și băutură incluse", "de la 200 lei"])}</ul>'
    f'<div class="up" style="--d: .85s">{cta()}</div></div></section>')

# 3. apple.com product pages / our own Ce oferim: the page opens brown, eases to cream (OKLab, eased) and the photo rises out of it.
OPTS["GrupHero3Continuare"] = ("Ateliere de grup 3: continuarea paginii „Ce oferim”", "dark", """
.g3{background:""" + eased_gradient(300, 760) + """;padding:184px 0 104px;text-align:center}
.g3 .gh{color:#F4EDE4}
.g3 .lede{max-width:38ch;margin:26px auto 0;color:#EFE3D3}
.g3 .ph{position:relative;max-width:1160px;margin:84px auto 0;aspect-ratio:21/9;border-radius:26px;corner-shape:squircle;overflow:hidden;box-shadow:0 40px 80px -50px rgba(46,28,19,.7)}
@keyframes g3-rise{from{opacity:0;translate:0 60px;scale:.96}}
@media (prefers-reduced-motion:no-preference){.g3 .ph{animation:g3-rise 1.3s var(--so) .5s backwards}}
.g3 .row{display:flex;justify-content:center;align-items:center;flex-wrap:wrap;gap:20px 40px;margin-top:40px}
.g3 .meta{font-size:16px}
@media (max-width:980px){
  .g3{background:""" + eased_gradient(250, 640) + """;padding:128px 0 64px}
  .g3 .ph{margin:56px 0 0;aspect-ratio:4/3;border-radius:20px}
  .g3 .row{flex-direction:column;gap:20px;margin-top:28px}.g3 .meta{justify-content:center;font-size:14.5px}
}
""", '<section class="gp g3" aria-labelledby="gh-h" ref="{{ secRef }}"><div class="wrap">'
    f'{h1()}<p class="lede up" style="--d: .5s">{LEDE}</p>'
    f'<div class="ph">{pic(ROOM)}</div>'
    f'<div class="row up" style="--d: .9s"><ul class="meta">{"".join(f"<li>{m}</li>" for m in SHORT + ["de la 200 lei"])}</ul>{cta()}</div>'
    '</div></section>')

# 4. lu.ma event page: a square cover on the left, the invitation on the right, the next date at the bottom.
OPTS["GrupHero4Invitatie"] = ("Ateliere de grup 4: invitație", "light", """
.g4{background:linear-gradient(180deg,#F4EDE4 0%,#EDE0CD 100%);padding:144px 0 104px}
.g4 .stage{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,6fr);gap:72px;align-items:center}
.g4 .cov{position:relative;aspect-ratio:1;border-radius:26px;corner-shape:squircle;overflow:hidden;box-shadow:0 30px 60px -40px rgba(70,35,15,.6)}
@media (prefers-reduced-motion:no-preference){.g4 .cov{animation:gh-uncover 1.2s var(--so) .25s backwards}}
.g4 .lede{margin-top:24px;max-width:34ch;color:#4A382C}
.g4 .rows{margin:32px 0 0;padding:0;list-style:none;border-top:1px solid rgba(58,42,32,.16)}
.g4 .rows li{display:grid;grid-template-columns:150px 1fr;gap:16px;padding:14px 0;border-bottom:1px solid rgba(58,42,32,.16);font-size:16px;line-height:1.5}
.g4 .rows b{font:400 italic 18px/1.4 var(--display);font-variation-settings:'opsz' 20;color:var(--terra-d)}
.g4 .rows span{color:#4A382C}
.g4 .act{display:flex;align-items:center;flex-wrap:wrap;gap:16px 24px;margin-top:32px}
.g4 .d4{flex:1;min-width:220px;max-width:300px;font-size:14px;color:var(--ink2)}
@media (max-width:980px){
  .g4{padding:104px 0 64px}
  .g4 .stage{grid-template-columns:1fr;gap:32px}
  .g4 .cov{aspect-ratio:4/3;border-radius:20px}
  .g4 .rows li{grid-template-columns:1fr;gap:2px;padding:12px 0}
}
""", '<section class="gp g4" aria-labelledby="gh-h" ref="{{ secRef }}"><div class="wrap stage">'
    f'<div class="cov">{pic(BOWL)}</div>'
    f'<div>{h1()}<p class="lede up" style="--d: .5s">{LEDE}</p>'
    f'<ul class="rows up" style="--d: .65s">' + "".join(f"<li><b>{a}</b><span>{b}</span></li>" for a, b in FACTS) + '</ul>'
    f'<div class="act up" style="--d: .8s">{cta()}{dates_html("dl d4")}</div>'
    '</div></div></section>')


def page(name, title, tone, css, html, w, h):
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
{BASE_CSS}{HX_CSS}{V["1Pastila"]["css"]}{COMMON}{css}</style>
</helmet>
<div class="pg hxv v1" data-src="{SOURCES[name]}">
{header(tone)}
{html}
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{w},"height":{h}}}}}'>
{script()}
</script>
</body>
</html>
"""


# preview heights, measured in the browser (desktop 1440, phone 390)
H = {"GrupHero1Galerie": (1336, 1698), "GrupHero2Aman": (905, 789), "GrupHero3Continuare": (1231, 938), "GrupHero4Invitatie": (997, 1268)}

if __name__ == "__main__":
    for name, (title, tone, css, html) in OPTS.items():
        for suffix, w, h in (("", 1440, H[name][0]), ("Mobil", 390, H[name][1])):
            f = os.path.join(P, f"{name}{suffix}.dc.html")
            open(f, "w", encoding="utf-8").write(page(name, title + (" · mobil" if suffix else ""), tone, css, html, w, h))
            if not suffix:
                subprocess.run([sys.executable, os.path.join(HERE, "dc2html.py"), f, os.path.join(HERE, f"opt-{name}.html")], check=True, capture_output=True)
        print("wrote", name)
    names = list(OPTS)
    open(os.path.join(HERE, "grup-hero-mobil.html"), "w").write('<!doctype html><meta charset="utf-8"><title>Ateliere de grup hero mobil</title><style>body{margin:0;padding:10px;background:#1b1b1b;display:flex;gap:12px;color:#ddd;font:13px system-ui}figure{margin:0}iframe{width:390px;height:1700px;border:0;display:block}</style>' + "".join(f'<figure><figcaption>{n}</figcaption><iframe src="opt-{n}.html"></iframe></figure>' for n in names))
