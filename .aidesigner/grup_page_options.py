"""Pagina „Ateliere de grup”, the remaining sections (Vali, 12 nov: hero 2 + lista 3, then the whole page with header and footer).
Built in the chosen language rather than as new variant rounds:
  GrupDetalii  „Cum funcționează”: the doc's facts in hairline columns (the quiet style Alessia asked for informational
               sections), then the collaborations invitation in a dark card (the FAQ's „Ai altă întrebare?” card).
  GrupFaq      the page's FAQ in the FAQ 3 cards chosen on Acasă (faq_options.py), with this page's questions.

usage: python3 .aidesigner/grup_page_options.py   (then pages_combine.py assembles AteliereDeGrup)
Copy: docs/continut-site.md, „Ateliere de grup”. Mine, to approve: the collaborations sentence without „echipă”
(CLAUDE.md: collaborators are never a team) — doc: „…să te avem în echipa noastră de colaboratori”.
"""
import os, subprocess, sys
from about_options2 import P, HERE, FONTS, BASE_CSS, ARROW
import faq_options as fq
from cf_pagina_options import ENTER
from grup_hero_options import ROOM2, pic

HOW = "Atelier lunar, 3 ore, cu o temă diferită de fiecare dată, uneori în colaborare cu alți artiști sau antreprenori."
FACTS = [("Ce include", "Materiale, ghidare, o băutură și o gustare, și posibilitatea de ardere a piesei, la alegerea fiecăruia."),
         ("Grup", "Maxim 8 persoane, ca să rămână intim."),
         ("Preț", "De la 200 lei / persoană, în funcție de temă."),
         ("Unde", "Cotroceni, București. Adresa exactă o primești la înscriere.")]
COLLAB_Q = "Ești artist sau antreprenor și vrei să facem un atelier împreună?"
COLLAB = "Pentru că AVA Art &amp; Soul este o comunitate în continuă creștere, ne-ar face plăcere să te avem alături, printre colaboratorii noștri."
QA = [  # Întrebări frecvente (Ateliere de grup), word for word
    ("Am nevoie de experiență?", "Nu. Vino doar cu curiozitate, de restul ne ocupăm noi."),
    ("Ce să port?", "Alege haine comode, pe care nu te deranjează să le murdărești cu lut. Totuși, stai fără grijă, lutul se ia foarte ușor de pe haine sau piele cu puțină apă caldă."),
    ("Când îmi iau piesa?", "Piesele trec prin uscare și ardere, așa că le poți ridica după 4-6 săptămâni, de la locul atelierului."),
    ("Ce se întâmplă dacă nu mai pot ajunge?", "Fiind o afacere la început de drum, fiecare loc ocupat are un impact asupra noastră. Astfel, suma achitată nu se returnează, dar dacă nu mai poți ajunge și ne anunți cu cel puțin 24 de ore înainte, îți păstrăm un loc la următorul atelier."),
    ("Pot oferi un atelier cadou?", "Da, scrie-ne și pregătim unul."),
]

DET_CSS = """
.gd{position:relative;background:linear-gradient(180deg,#EDE0CD 0%,#F4EDE4 100%);padding:112px 0 120px;--so:cubic-bezier(.22,1,.36,1)}
.gd h2{font-size:clamp(40px,4.4vw,64px);line-height:1.05}
.gd .how{margin:20px 0 0;max-width:40ch;font:400 clamp(20px,1.7vw,24px)/1.45 var(--display);font-variation-settings:'opsz' 20;color:#4A382C;text-wrap:pretty}
.gd dl{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:0 40px;margin:52px 0 0}
.gd dl>div{padding-top:22px;border-top:1px solid rgba(58,42,32,.22)}
.gd dt{font:400 italic 21px/1.3 var(--display);font-variation-settings:'opsz' 20;color:var(--terra-d)}
.gd dd{margin:8px 0 0;font-size:16.5px;line-height:1.6;color:#4A382C;text-wrap:pretty}
.gd .co{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:20px 48px;align-items:center;margin-top:72px;padding:40px 44px;border-radius:22px;corner-shape:squircle;background:#3A2A20;color:#F4EDE4}
.gd .co .q{margin:0;font:400 italic clamp(24px,2.2vw,30px)/1.3 var(--display);font-variation-settings:'opsz' 20;text-wrap:balance}
.gd .co p+p{margin:12px 0 0;max-width:62ch;color:#D8C6B2;font-size:16.5px;line-height:1.6;text-wrap:pretty}
.gd .btn-c{display:inline-flex;align-items:center;justify-content:center;min-height:52px;padding:0 30px;border-radius:999px;background:#F4EDE4;color:#2E1D14;font:500 15px/1 var(--text);letter-spacing:.02em;text-decoration:none;white-space:nowrap;transition:background-color .25s ease}
.gd .btn-c:hover{background:#FFF8EE}
.gd .btn-c:focus-visible{outline:2px solid #F2C79C;outline-offset:3px}
@keyframes gd-up{from{opacity:0;translate:0 16px}}
.gd.js:not(.in) .ri{opacity:0}
.gd.js.in .ri{animation:gd-up .8s var(--so) backwards;animation-delay:calc(var(--i,0) * 80ms)}
@media (max-width:980px){
  .gd{padding:72px 0 80px}
  .gd dl{grid-template-columns:1fr;gap:22px;margin-top:32px}.gd dl>div{padding-top:16px}
  .gd .co{grid-template-columns:1fr;margin-top:48px;padding:28px 24px}.gd .co .btn-c{width:100%;box-sizing:border-box}
}
@media (prefers-reduced-motion:reduce){.gd *{animation:none!important}}
"""
DET_HTML = ('<section class="gd" aria-labelledby="gd-h" ref="{{ secRef }}"><div class="wrap">'
            f'<h2 class="disp ri" id="gd-h">Cum funcționează</h2><p class="how ri" style="--i: 1">{HOW}</p><dl>'
            + "".join(f'<div class="ri" style="--i: {i + 2}"><dt>{a}</dt><dd>{b}</dd></div>' for i, (a, b) in enumerate(FACTS))
            + f'</dl><aside class="co ri" style="--i: 2" aria-label="Colaborări"><div><p class="q">{COLLAB_Q}</p><p>{COLLAB}</p></div>'
            f'<a class="btn-c" href="#contact">Scrie-ne</a></aside></div></section>')


SOL_H = "Ai deja un grup?"
SOL = ("Dacă vreți să veniți împreună, cu prietenii, cu familia sau pentru o zi specială, pregătesc un atelier doar pentru voi, "
       "la o dată care vă convine și cu o temă aleasă împreună. Scrie-mi câți sunteți și ce v-ar plăcea, iar eu revin cu o propunere.")
SOL_BTN = "Solicită un atelier"
SOL_NOTE = "Îți răspundem în maxim 24 de ore."   # Contact, docs/continut-site.md
SOL_CSS = """
.gs{position:relative;background:#EDE0CD;padding:0 0 104px;--so:cubic-bezier(.22,1,.36,1)}
.gs .card{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,6fr);border-radius:22px;corner-shape:squircle;overflow:hidden;background:#FBF7F1;box-shadow:0 0 0 1px rgba(58,42,32,.06),0 30px 60px -44px rgba(70,35,15,.5)}
.gs .ph{position:relative;min-height:360px;overflow:hidden}
.gs .ph img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.gs .tx{display:flex;flex-direction:column;align-items:flex-start;justify-content:center;padding:52px 56px}
.gs h2{font-size:clamp(36px,3.6vw,52px);line-height:1.05}
.gs .tx>p{margin:18px 0 0;max-width:46ch;font-size:17px;line-height:1.65;color:#4A382C;text-wrap:pretty}
.gs .btn{display:inline-flex;align-items:center;justify-content:center;min-height:52px;margin-top:28px;padding:0 30px;border-radius:999px;background:#9C472C;color:#F8F1E8;font:500 15px/1 var(--text);letter-spacing:.02em;text-decoration:none;transition:background-color .25s ease}
.gs .btn:hover{background:#833A22}
.gs .btn:focus-visible{outline:2px solid #9C472C;outline-offset:3px}
.gs .note{margin:12px 0 0;font-size:14px;color:var(--ink2)}
@keyframes gs-up{from{opacity:0;translate:0 16px}}
@keyframes gs-uncover{from{clip-path:inset(0 100% 0 0)}}
.gs.js:not(.in) .ri{opacity:0}
.gs.js.in .ri{animation:gs-up .8s var(--so) backwards;animation-delay:calc(var(--i,0) * 80ms)}
.gs.js:not(.in) .ph{clip-path:inset(0 100% 0 0)}
.gs.js.in .ph{animation:gs-uncover 1.1s var(--so) backwards}
@media (max-width:980px){
  .gs{padding:0 0 72px}
  .gs .card{grid-template-columns:1fr}.gs .ph{min-height:0;aspect-ratio:4/3}
  .gs .tx{padding:28px 22px 26px}.gs .btn{width:100%;box-sizing:border-box}
}
@media (prefers-reduced-motion:reduce){.gs *{animation:none!important;clip-path:none!important}}
"""
SOL_HTML = ('<section class="gs" id="solicita" aria-labelledby="gs-h" ref="{{ secRef }}"><div class="wrap"><div class="card">'
            f'<div class="ph">{pic(ROOM2)}</div><div class="tx"><h2 class="disp ri" id="gs-h">{SOL_H}</h2>'
            f'<p class="ri" style="--i: 1">{SOL}</p><a class="btn ri" style="--i: 2" href="#contact">{SOL_BTN}</a>'
            f'<p class="note ri" style="--i: 3">{SOL_NOTE}</p></div></div></div></section>')


def faq_html():
    acc = "".join(f'<details name="faq-grup"{" open" if i == 0 else ""}><summary><span class="qq">{q}</span>{fq.ICON}</summary>'
                  f'<div class="ans"><p>{a}</p></div></details>' for i, (q, a) in enumerate(QA))
    return (f'<section class="fq f3" id="intrebari" aria-labelledby="fq-h" ref="{{{{ secRef }}}}"><div class="wrap">'
            f'<div class="head ri"><h2 class="disp" id="fq-h">{fq.H}</h2></div>'
            f'<div class="cards"><div class="acc ri" style="--i: 1">{acc}</div><aside class="other ri" style="--i: 2" aria-label="{fq.ASK}">'
            f'<p class="ask">{fq.ASK}</p><p class="reply">{fq.REPLY}</p><div class="links">{fq.WRITE}{fq.ALL}</div></aside></div></div></section>')


FAQ_CSS = fq.COMMON + fq.OPTS["Faq3Carduri"][2] + """
@keyframes fq-up{from{opacity:0;translate:0 16px}}
.fq.js:not(.in) .ri{opacity:0}
.fq.js.in .ri{animation:fq-up .8s cubic-bezier(.22,1,.36,1) backwards;animation-delay:calc(var(--i,0) * 80ms)}
@media (prefers-reduced-motion:reduce){.fq .ri{animation:none!important}}
"""

OPTS = {"GrupSolicita": ("Ateliere de grup: ai deja un grup?", SOL_CSS, SOL_HTML),
        "GrupDetalii": ("Ateliere de grup: cum funcționează + colaborări", DET_CSS, DET_HTML),
        "GrupFaq": ("Ateliere de grup: întrebări frecvente", FAQ_CSS, faq_html())}
H = {"GrupSolicita": (547, 767), "GrupDetalii": (834, 1181), "GrupFaq": (934, 1112)}


def page(title, css, html, w, h):
    js = ("class Component extends DCLogic {\n  componentDidMount() {" + ENTER + "\n  }\n"
          "  componentWillUnmount() { if (this.io) this.io.disconnect(); }\n"
          "  renderVals() { var self = this; if (!this.cb) this.cb = { secRef: function (el) { self.sec = el; } }; return this.cb; }\n}")
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
{BASE_CSS}{css}</style>
</helmet>
<div class="pg">
{html}
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{w},"height":{h}}}}}'>
{js}
</script>
</body>
</html>
"""


if __name__ == "__main__":
    for name, (title, css, html) in OPTS.items():
        for suffix, w, h in (("", 1440, H[name][0]), ("Mobil", 390, H[name][1])):
            f = os.path.join(P, f"{name}{suffix}.dc.html")
            open(f, "w", encoding="utf-8").write(page(title + (" · mobil" if suffix else ""), css, html, w, h))
            if not suffix:
                subprocess.run([sys.executable, os.path.join(HERE, "dc2html.py"), f, os.path.join(HERE, f"opt-{name}.html")], check=True, capture_output=True)
        print("wrote", name)
