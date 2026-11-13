"""Ce oferim › Pentru companii (Vali, 12 nov: the service template, applied to the next page).
Built on the „Ateliere de grup” page, which is the template for every service page:
  CompHero      the chosen hero (2, Aman: one photo on the whole screen), with this page's copy. No new variants.
  CompFormate1..4  NEW section, four variants: when it helps, the formats, the possible themes.
  CompDetalii   „Cum funcționează” as on Ateliere de grup (hairline columns), the dark card is „Cine facilitează”,
                plus a visible placeholder for the proof the doc doesn't have yet (logos, an HR testimonial).
  CompOferta1..4   NEW section, four variants: the offer request form (the doc's fields).
  CompFaq       the page's FAQ in the FAQ 3 cards.

usage: python3 .aidesigner/companii_options.py
writes .aidesigner/canvas/project/Comp*.dc.html (+ Mobil twins) and local previews .aidesigner/opt-Comp*.html

Copy: docs/continut-site.md, „Pentru companii” + its FAQ. The line under the title is Vali's canvas edit on Ce oferim
(„Evenimente de autocunoaștere…”). Mine, to approve (marked MINE below): the pills, „Când e de folos”, the form's goal
options, the GDPR line, „Trimite cererea”, the 3 steps in form 1, the form's group labels.
Photo: the companies photo from Ce oferim is provisional (Unsplash) until there are photos from a company workshop.
"""
import os, subprocess, sys
from about_options2 import P, HERE, FONTS, BASE_CSS, ARROW, DUO
import grup_hero_options as gh
import grup_page_options as gp
import faq_options as fq
from ce_facem2_options import IMG
from cf_pagina_options import ENTER

# ---- copy (docs/continut-site.md, Pentru companii) ----
TITLE = "Pentru companii"
LEDE = "Evenimente de autocunoaștere și conectare pentru echipe, în care lutul este unealta."
BODY = ("Oferim o pauză reală de la stres și oboseală, în care colegii se descoperă ca oameni, nu doar ca roluri. "
        "Lutul ține mâinile ocupate, iar restul vine de la sine: liniște, râs, conversații sincere.")
HELPS = ["Stres și oboseală", "Echipe noi sau remote care nu se cunosc", "Dificultăți în comunicare", "Nevoia de o pauză reală"]
HELPS_H = "Când e de folos"                                       # MINE (doc label: „Ce problemă rezolvă”)
FORMATS = [("3 ore", "Atelier de modelaj în lut"), ("jumătate de zi", "Lut și teme de wellbeing"),
           ("lunar", "Program de wellbeing"), ("la cerere", "Teambuilding")]
FORMATS_H = "Formate"
THEMES = ["Gestionarea stresului", "Comunicare și încredere", "Echipa ca întreg", "Ce mă motivează"]
THEMES_H = "Teme posibile"
PILLS = ["3 ore sau jumătate de zi", "4–16 persoane", "venim la voi", "ofertă personalizată"]   # MINE, from the doc's facts
CTA = "Cere o ofertă"                                             # the label Vali approved on Ce oferim
PHOTO = (IMG["companii"], "Mâini care își dau din mână în mână un vas de lut (fotografie provizorie)", "50% 40%")

HOW = "Venim cu toate materialele, la sediul firmei sau într-o locație parteneră AVA."
FACTS = [("Grup", "De la 4 la 16 persoane. Pentru echipe mai mari, împărțim grupul sau facem mai multe sesiuni."),
         ("Unde", "La voi la birou, în locații partenere AVA sau într-un spațiu ales de voi."),
         ("Preț", "La cerere, cu ofertă personalizată."),
         ("Factură", "Emitem factură pe firmă.")]
WHO_H = "Cine facilitează"
WHO = "Alessia Văideanu, consilier acreditat în dezvoltare personală și artist ceramist."
PROOF = ["[LOGO-URI DE FIRME, CU ACORDUL LOR]", "[TESTIMONIAL DE LA UN HR]"]

QA = [  # Întrebări frecvente (Pentru companii), word for word
    ("Pentru câți oameni puteți face un atelier?", "Între 4 și 16 persoane. Pentru echipe mai mari, împărțim grupul sau facem mai multe sesiuni."),
    ("Veniți la noi la birou?", "Da, venim cu toate materialele. Putem lucra și în locații partenere AVA sau într-un spațiu ales de voi."),
    ("Colegii trebuie să vorbească despre lucruri personale?", "Nu. Fiecare împărtășește doar cât se simte confortabil. Atelierele sunt gândite să fie sigure pentru toată lumea."),
    ("Emiteți factură?", "Da, emitem factură pe firmă."),
    ("Cât costă?", "Fiecare atelier e gândit pentru echipa voastră, așa că îți trimitem o ofertă personalizată după ce aflăm de ce are nevoie echipa ta și formatul ales."),
]

# the form (doc: nume, firmă, email, telefon, nr. de persoane, dată orientativă, locație, ce vă doriți să obțină echipa: listă + altceva)
OF_H = "Cere o ofertă"
OF_SUB = QA[4][1]
OF_NOTE = "Îți răspundem în maxim 24 de ore."
GOALS = ["Mai puțin stres și oboseală", "Comunicare și încredere", "Să se cunoască mai bine", "O pauză reală", "Să afle ce îi motivează"]   # MINE, from the doc's problems + themes
GOALS_Q = "Ce vă doriți să obțină echipa?"
GDPR = 'Sunt de acord ca datele mele să fie folosite pentru a primi oferta, conform <a href="#confidentialitate">Politicii de confidențialitate</a>.'   # MINE
SEND = "Trimite cererea"                                          # MINE
STEPS = ["Ne spui ce își dorește echipa.", "Îți răspundem în maxim 24 de ore.", "Primești o ofertă gândită pentru voi."]   # MINE

SOURCES = {
    "CompHero": "șablonul paginilor de serviciu: deschiderea aleasă pe Ateliere de grup (aman.com)",
    "CompFormate1Planuri": "notion.com/pricing: formatele una lângă alta, ca planurile, iar temele dedesubt",
    "CompFormate2Nevoi": "headspace.com/work: întâi problemele echipei, mari, cu câte un desen, apoi formatele",
    "CompFormate3Editorial": "Kinfolk, revista: o fotografie mare lângă text, formatele ca un cuprins numerotat",
    "CompFormate4Fisa": "aesop.com, fișa produsului: rânduri cu linie subțire, eticheta în stânga și răspunsul în dreapta",
    "CompDetalii": "șablonul paginilor de serviciu: „Cum funcționează” de pe Ateliere de grup",
    "CompOferta1Vanzari": "stripe.com/contact/sales: textul și pașii în stânga, formularul într-un card în dreapta",
    "CompOferta2Alegeri": "airbnb.com, înscrierea gazdelor: întâi alegi din plăci mari, apoi completezi restul",
    "CompOferta3Liniste": "aman.com, formularul de rezervare: centrat, câmpuri doar cu linie dedesubt, etichete cu serif",
    "CompOferta4Pasi": "typeform.com: câte o întrebare pe rând, cu bara de progres",
    "CompFaq": "șablonul paginilor de serviciu: FAQ 3, carduri (ales pe Acasă)",
}


def h1():
    k, ws = 0, []
    for w in TITLE.split():
        ls = []
        for ch in w:
            ls.append(f'<span class="l" style="--k: {k}">{ch}</span>'); k += 1
        ws.append('<span class="w" aria-hidden="true">' + "".join(ls) + "</span>")
    return f'<h1 class="disp gh" id="gh-h" aria-label="{TITLE}">' + " ".join(ws) + "</h1>"


# ---- hero: the template (Ateliere de grup, hero 2) ----
HERO_HTML = ('<section class="gp g2" aria-labelledby="gh-h" ref="{{ secRef }}">'
             f'<div class="bg">{gh.pic(PHOTO)}</div><div class="in">{h1()}'
             f'<p class="lede up" style="--d: .55s">{LEDE}</p>'
             f'<ul class="pills up" style="--d: .7s">{"".join(f"<li>{m}</li>" for m in PILLS)}</ul>'
             f'<div class="up" style="--d: .85s"><a class="btn" href="#oferta">{CTA}</a></div></div></section>')

# ---- shared section CSS ----
SEC = """
.cs{position:relative;padding:112px 0 120px;--so:cubic-bezier(.22,1,.36,1)}
.cs a{text-decoration:none}
.cs h2{font-size:clamp(40px,4.4vw,64px);line-height:1.05}
.cs h3{margin:0;font:400 26px/1.15 var(--display);font-variation-settings:'opsz' 20;letter-spacing:-.01em;text-wrap:balance}
.cs .intro{margin:20px 0 0;max-width:44ch;font:400 clamp(20px,1.7vw,24px)/1.45 var(--display);font-variation-settings:'opsz' 20;color:#4A382C;text-wrap:pretty}
.cs .lab{margin:0;font:400 italic 21px/1.3 var(--display);font-variation-settings:'opsz' 20;color:var(--terra-d)}
.cs .btn{display:inline-flex;align-items:center;justify-content:center;min-height:52px;padding:0 30px;border-radius:999px;background:#9C472C;color:#F8F1E8;font:500 15px/1 var(--text);letter-spacing:.02em;white-space:nowrap;border:0;cursor:pointer;transition:background-color .25s ease}
.cs .btn:hover{background:#833A22}.cs .btn:focus-visible{outline:2px solid #9C472C;outline-offset:3px}
.cs .chips{display:flex;flex-wrap:wrap;gap:8px;margin:0;padding:0;list-style:none}
.cs .chips li{display:inline-flex;align-items:center;min-height:38px;padding:0 16px;border-radius:999px;background:#F1E7DA;font-size:15px;color:#3A2A20}
@keyframes cs-up{from{opacity:0;translate:0 16px}}
.cs.js:not(.in) .ri{opacity:0}
.cs.js.in .ri{animation:cs-up .8s var(--so) backwards;animation-delay:calc(var(--i,0) * 80ms)}
@media (max-width:980px){.cs{padding:72px 0 80px}.cs h3{font-size:23px}.cs .btn{width:100%;box-sizing:border-box}}
@media (prefers-reduced-motion:reduce){.cs *{animation:none!important;transition:none!important}}
"""

OPTS = {}
helps_ul = lambda cls="": f'<ul class="{cls}">' + "".join(f"<li>{h}</li>" for h in HELPS) + "</ul>"
themes_ul = lambda: '<ul class="chips">' + "".join(f"<li>{t}</li>" for t in THEMES) + "</ul>"

# 1. Notion pricing: the four formats side by side like plans, a note of when it helps above, the themes below.
OPTS["CompFormate1Planuri"] = ("Pentru companii, formate 1: ca planurile", """
.f1{background:linear-gradient(180deg,#F4EDE4 0%,#EDE0CD 100%)}
.f1 .top{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:48px;align-items:end}
.f1 .top .lab{margin-bottom:12px}
.f1 .help{margin:0;padding:0;list-style:none;border-top:1px solid rgba(58,42,32,.18)}
.f1 .help li{padding:11px 0;border-bottom:1px solid rgba(58,42,32,.18);font-size:16.5px;color:#4A382C}
.f1 .plans{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;margin:64px 0 0;padding:0;list-style:none}
.f1 .plans li{display:flex;flex-direction:column;min-height:230px;padding:26px 24px 24px;border-radius:22px;corner-shape:squircle;background:#FBF7F1;box-shadow:0 0 0 1px rgba(58,42,32,.06);transition:translate .4s var(--so),box-shadow .4s ease}
@media (hover:hover){.f1 .plans li:hover{translate:0 -3px;box-shadow:0 0 0 1px rgba(58,42,32,.08),0 22px 40px -28px rgba(58,30,15,.5)}}
.f1 .plans .d{font:400 italic 20px/1 var(--display);font-variation-settings:'opsz' 20;color:var(--terra-d)}
.f1 .plans h3{margin-top:14px;flex:1}
.f1 .plans .pr{margin:20px 0 0;padding-top:16px;border-top:1px solid rgba(58,42,32,.12);font-size:14.5px;color:var(--ink2)}
.f1 .plans .more{margin-top:6px}
.f1 .th{display:flex;align-items:center;flex-wrap:wrap;gap:12px 20px;margin-top:40px}
@media (max-width:980px){
  .f1 .top{grid-template-columns:1fr;gap:28px}
  .f1 .plans{grid-template-columns:1fr 1fr;gap:10px;margin-top:40px}
  .f1 .plans li{min-height:0;padding:18px 16px}.f1 .plans .d{font-size:17px}.f1 .plans h3{font-size:20px;margin-top:8px}
  .f1 .plans .pr{margin-top:14px;padding-top:12px;font-size:13.5px}.f1 .plans .more{display:none}
  .f1 .th{flex-direction:column;align-items:flex-start;margin-top:32px}
}
""", '<section class="cs f1" aria-labelledby="cf-h" ref="{{ secRef }}"><div class="wrap">'
    f'<div class="top"><div><h2 class="disp ri" id="cf-h">{FORMATS_H}</h2><p class="intro ri" style="--i: 1">{BODY}</p></div>'
    f'<div class="ri" style="--i: 2"><p class="lab">{HELPS_H}</p>{helps_ul("help")}</div></div>'
    '<ul class="plans">' + "".join(f'<li class="ri" style="--i: {i + 3}"><span class="d">{d}</span><h3>{n}</h3>'
                                  f'<p class="pr">Preț la cerere</p><a class="more" href="#oferta">{CTA} {ARROW}</a></li>' for i, (d, n) in enumerate(FORMATS))
    + f'</ul><div class="th ri" style="--i: 7"><p class="lab">{THEMES_H}</p>{themes_ul()}</div></div></section>')

# 2. Headspace for Work: the team's problems first, big, each with a small line drawing in clay; then formats and themes.
ICONS = [  # stroke drawings, 48x48: a tired face / two people apart / speech bubbles / a cup
    '<circle cx="24" cy="24" r="17"></circle><path d="M16 21q3 2 6 0M26 21q3 2 6 0M18 32q6-3 12 0"></path>',
    '<circle cx="14" cy="17" r="5"></circle><circle cx="34" cy="17" r="5"></circle><path d="M6 38q0-10 8-10t8 10M26 38q0-10 8-10t8 10"></path>',
    '<path d="M6 12h22v14H16l-6 5v-5H6z"></path><path d="M32 20h10v13h-3v4l-5-4h-8v-6"></path>',
    '<path d="M11 18h22v10q0 10-11 10t-11-10z"></path><path d="M33 21h3q4 0 4 4t-4 4h-3M17 8q-2 3 0 6M23 6q-2 3 0 6"></path>',
]
OPTS["CompFormate2Nevoi"] = ("Pentru companii, formate 2: întâi nevoile", """
.f2{background:linear-gradient(180deg,#F4EDE4 0%,#EDE0CD 100%)}
.f2 .head{max-width:820px}
.f2 .needs{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:20px;margin:52px 0 0;padding:0;list-style:none}
.f2 .needs li{display:flex;flex-direction:column;gap:18px;padding:28px 24px 26px;border-radius:22px;corner-shape:squircle;background:#FBF7F1;box-shadow:0 0 0 1px rgba(58,42,32,.06)}
.f2 .needs svg{width:48px;height:48px;fill:none;stroke:#B4583A;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.f2 .needs p{margin:0;font:400 22px/1.25 var(--display);font-variation-settings:'opsz' 20;text-wrap:balance}
.f2 .low{display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:56px;margin-top:72px}
.f2 .fl{margin:14px 0 0;padding:0;list-style:none;border-top:1px solid rgba(58,42,32,.18)}
.f2 .fl li{display:flex;justify-content:space-between;align-items:baseline;gap:20px;padding:16px 0;border-bottom:1px solid rgba(58,42,32,.18)}
.f2 .fl b{font:400 24px/1.2 var(--display);font-variation-settings:'opsz' 20}
.f2 .fl span{font-size:15px;color:var(--ink2);white-space:nowrap}
.f2 .chips{margin-top:18px}
@media (max-width:980px){
  .f2 .needs{grid-template-columns:1fr 1fr;gap:10px;margin-top:32px}
  .f2 .needs li{gap:12px;padding:18px 16px}.f2 .needs svg{width:38px;height:38px}.f2 .needs p{font-size:18px}
  .f2 .low{grid-template-columns:1fr;gap:40px;margin-top:48px}.f2 .fl b{font-size:20px}
}
""", '<section class="cs f2" aria-labelledby="cf-h" ref="{{ secRef }}"><div class="wrap">'
    f'<div class="head"><h2 class="disp ri" id="cf-h">{HELPS_H}</h2><p class="intro ri" style="--i: 1">{BODY}</p></div>'
    '<ul class="needs">' + "".join(f'<li class="ri" style="--i: {i + 2}"><svg viewBox="0 0 48 48" aria-hidden="true">{ICONS[i]}</svg><p>{h}</p></li>' for i, h in enumerate(HELPS))
    + f'</ul><div class="low"><div class="ri" style="--i: 6"><p class="lab">{FORMATS_H}</p><ul class="fl">'
    + "".join(f"<li><b>{n}</b><span>{d}</span></li>" for d, n in FORMATS)
    + f'</ul></div><div class="ri" style="--i: 7"><p class="lab">{THEMES_H}</p>{themes_ul()}</div></div></div></section>')

# 3. Kinfolk: a tall photo beside the text, the formats as a numbered contents page, the themes in italics.
OPTS["CompFormate3Editorial"] = ("Pentru companii, formate 3: editorial", """
.f3{background:linear-gradient(180deg,#F4EDE4 0%,#EDE0CD 100%)}
.f3 .stage{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:72px;align-items:start}
.f3 .ph{position:sticky;top:96px;aspect-ratio:4/5;border-radius:22px;corner-shape:squircle;overflow:hidden}
.f3 .ph img{display:block;width:100%;height:100%;object-fit:cover}
@keyframes f3-un{from{clip-path:inset(100% 0 0 0)}}
.f3.js:not(.in) .ph{clip-path:inset(100% 0 0 0)}.f3.js.in .ph{animation:f3-un 1.2s var(--so) backwards}
.f3 .help{margin:28px 0 0;font-size:16.5px;line-height:1.7;color:#4A382C}
.f3 .help b{font-weight:500;color:var(--ink)}
.f3 .toc{margin:48px 0 0;padding:0;list-style:none;counter-reset:f}
.f3 .toc li{display:grid;grid-template-columns:56px minmax(0,1fr) auto;align-items:baseline;gap:16px;padding:18px 0;border-top:1px solid rgba(58,42,32,.18);counter-increment:f}
.f3 .toc li:last-child{border-bottom:1px solid rgba(58,42,32,.18)}
.f3 .toc li::before{content:"0" counter(f);font:400 15px/1 var(--text);color:var(--terra-d);font-variant-numeric:tabular-nums}
.f3 .toc b{font:400 28px/1.15 var(--display);font-variation-settings:'opsz' 20}
.f3 .toc span{font:400 italic 18px/1 var(--display);font-variation-settings:'opsz' 20;color:var(--ink2)}
.f3 .th{margin:40px 0 0;font:400 italic 24px/1.5 var(--display);font-variation-settings:'opsz' 20;color:#4A382C;text-wrap:balance}
.f3 .th i{font-style:normal;color:var(--terra-d);margin:0 10px}
@media (max-width:980px){
  .f3 .stage{grid-template-columns:1fr;gap:32px}.f3 .ph{position:static;aspect-ratio:4/3}
  .f3 .toc{margin-top:36px}.f3 .toc li{grid-template-columns:36px minmax(0,1fr);gap:4px 10px}
  .f3 .toc b{font-size:22px}.f3 .toc span{grid-column:2;font-size:16px}.f3 .th{font-size:20px}
}
""", '<section class="cs f3" aria-labelledby="cf-h" ref="{{ secRef }}"><div class="wrap stage">'
    f'<div class="ph">{gh.pic(gh.ROOM2)}</div><div><h2 class="disp ri" id="cf-h">{FORMATS_H}</h2>'
    f'<p class="intro ri" style="--i: 1">{BODY}</p><p class="help ri" style="--i: 2"><b>{HELPS_H}:</b> {", ".join(h[0].lower() + h[1:] for h in HELPS)}.</p>'
    '<ol class="toc ri" style="--i: 3">' + "".join(f"<li><b>{n}</b><span>{d}</span></li>" for d, n in FORMATS) + '</ol>'
    f'<p class="lab ri" style="--i: 4;margin-top:40px">{THEMES_H}</p><p class="th ri" style="--i: 5;margin-top:8px">' + '<i>·</i>'.join(THEMES) + '</p></div></div></section>')

# 4. Aesop product sheet: quiet hairline rows, the label on the left and the answer on the right; the photo stays beside.
OPTS["CompFormate4Fisa"] = ("Pentru companii, formate 4: fișă", """
.f4{background:linear-gradient(180deg,#F4EDE4 0%,#EDE0CD 100%)}
.f4 .stage{display:grid;grid-template-columns:minmax(0,6fr) minmax(0,5fr);gap:80px;align-items:start}
.f4 dl{margin:48px 0 0;border-top:1px solid rgba(58,42,32,.22)}
.f4 dl>div{display:grid;grid-template-columns:200px minmax(0,1fr);gap:24px;padding:22px 0;border-bottom:1px solid rgba(58,42,32,.22)}
.f4 dt{font:400 italic 20px/1.35 var(--display);font-variation-settings:'opsz' 20;color:var(--terra-d)}
.f4 dd{margin:0}
.f4 dd ul{margin:0;padding:0;list-style:none}
.f4 dd li{font-size:16.5px;line-height:1.75;color:#4A382C}
.f4 dd li span{color:var(--ink2)}
.f4 .ph{position:sticky;top:96px;aspect-ratio:3/4;border-radius:22px;corner-shape:squircle;overflow:hidden}
.f4 .ph img{display:block;width:100%;height:100%;object-fit:cover}
@media (max-width:980px){
  .f4 .stage{grid-template-columns:1fr;gap:36px}.f4 .ph{position:static;aspect-ratio:4/3;order:-1}
  .f4 dl{margin-top:32px}.f4 dl>div{grid-template-columns:1fr;gap:6px;padding:18px 0}
}
""", '<section class="cs f4" aria-labelledby="cf-h" ref="{{ secRef }}"><div class="wrap stage"><div>'
    f'<h2 class="disp ri" id="cf-h">{FORMATS_H}</h2><p class="intro ri" style="--i: 1">{BODY}</p><dl>'
    + "".join(f'<div class="ri" style="--i: {i + 2}"><dt>{a}</dt><dd>{b}</dd></div>' for i, (a, b) in enumerate([
        (HELPS_H, helps_ul()),
        (FORMATS_H, "<ul>" + "".join(f"<li>{n} <span>· {d}</span></li>" for d, n in FORMATS) + "</ul>"),
        (THEMES_H, "<ul>" + "".join(f"<li>{t}</li>" for t in THEMES) + "</ul>"),
        ("Preț", "<ul><li>La cerere, cu ofertă personalizată.</li></ul>")]))
    + f'</dl></div><div class="ph ri" style="--i: 1">{gh.pic(gh.BOWL)}</div></div></section>')

# ---- details: the template („Cum funcționează”), the dark card is who leads it; proof = visible placeholders ----
DET_CSS = gp.DET_CSS + """
.gd .co{grid-template-columns:auto minmax(0,1fr) auto}
.gd .co .pt{width:96px;height:96px;border-radius:50%;overflow:hidden;background:linear-gradient(180deg,#E6D5BD 0%,#D4B894 100%)}
.gd .co .pt img{display:block;width:100%;height:100%;object-fit:cover;object-position:50% 8%}
.gd .co .more{color:#F2C79C}
.gd .proof{display:flex;flex-wrap:wrap;gap:12px;margin-top:40px}
.gd .proof span{display:inline-flex;align-items:center;min-height:56px;padding:0 20px;border:1px dashed rgba(156,71,44,.55);border-radius:14px;color:var(--terra-d);font-size:14px;letter-spacing:.02em}
@media (max-width:980px){.gd .co{grid-template-columns:1fr}.gd .co .pt{width:80px;height:80px}.gd .proof span{min-height:48px}}
"""
DET_HTML = ('<section class="gd" aria-labelledby="gd-h" ref="{{ secRef }}"><div class="wrap">'
            f'<h2 class="disp ri" id="gd-h">Cum funcționează</h2><p class="how ri" style="--i: 1">{HOW}</p><dl>'
            + "".join(f'<div class="ri" style="--i: {i + 2}"><dt>{a}</dt><dd>{b}</dd></div>' for i, (a, b) in enumerate(FACTS))
            + '</dl><div class="proof ri" style="--i: 6">' + "".join(f"<span>{p}</span>" for p in PROOF) + '</div>'
            f'<aside class="co ri" style="--i: 2" aria-label="{WHO_H}"><div class="pt"><img src="{DUO}" alt="Alessia Văideanu"></div>'
            f'<div><p class="q">{WHO_H}</p><p>{WHO}</p></div><a class="more" href="#despre">Povestea mea {ARROW}</a></aside></div></section>')


# ---- the form: fields shared by all four variants ----
def field(name, label, kind="text", extra="", cls=""):
    return (f'<label class="fi {cls}"><span class="fl">{label}</span>'
            f'<input type="{kind}" name="{name}"{extra}></label>')


FIELDS = {
    "nume": field("nume", "Nume", extra=' autocomplete="name" required'),
    "firma": field("firma", "Firmă", extra=' autocomplete="organization" required'),
    "email": field("email", "Email", "email", ' autocomplete="email" required'),
    "telefon": field("telefon", 'Telefon <small>(opțional)</small>', "tel", ' autocomplete="tel"'),
    "persoane": field("persoane", "Număr de persoane", "number", ' min="1" inputmode="numeric" required'),
    "data": field("data", "Dată orientativă", "date"),
    "locatie": field("locatie", "Locație", extra=' placeholder="la birou, în București…"'),
}


PLUS = '<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M14 24h20M24 14v20"></path></svg>'


def goals(cls="goals", big=False):
    ic = ['<svg viewBox="0 0 48 48" aria-hidden="true">' + ICONS[i] + "</svg>" for i in range(4)] + ['<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M24 8l4 10 11 1-8 7 3 11-10-6-10 6 3-11-8-7 11-1z"></path></svg>']
    return (f'<fieldset class="{cls}"><legend class="fl">{GOALS_Q}</legend><div class="opts">'
            + "".join(f'<label class="ch"><input type="checkbox" name="scop" value="{g}">{ic[i] if big else ""}<span>{g}</span></label>' for i, g in enumerate(GOALS))
            + f'<label class="ch alt"><input type="checkbox" name="scop" value="altceva">{PLUS if big else ""}<span>Altceva</span></label></div>'
            '<label class="fi altx"><span class="fl">Spune-ne ce</span><textarea name="altceva" rows="3"></textarea></label></fieldset>')


GDPR_HTML = f'<label class="ok"><input type="checkbox" name="gdpr" required><span>{GDPR}</span></label>'
SUBMIT = f'<button class="btn" type="submit">{SEND}</button>'

FORM_CSS = """
.of form{margin:0}
.of .fi{display:flex;flex-direction:column;gap:7px;min-width:0}
.of .fl{font-size:14px;font-weight:500;color:#4A382C;padding:0}
.of .fl small{font-weight:400;color:var(--ink2);font-size:13px}
.of input:not([type=checkbox]),.of textarea{box-sizing:border-box;width:100%;min-height:50px;padding:12px 14px;border:1px solid rgba(58,42,32,.22);border-radius:12px;background:#FFFCF7;font:400 16px/1.4 var(--text);color:var(--ink);transition:border-color .2s,box-shadow .2s}
.of textarea{resize:vertical;min-height:96px}
.of input::placeholder{color:#9A8676}
.of input:not([type=checkbox]):focus,.of textarea:focus{outline:0;border-color:#9C472C;box-shadow:0 0 0 3px rgba(156,71,44,.18)}
.of fieldset{margin:0;padding:0;border:0;min-width:0}
.of legend{margin-bottom:10px}
.of .opts{display:flex;flex-wrap:wrap;gap:8px}
.of .ch{position:relative;display:inline-flex;align-items:center;gap:10px;min-height:44px;padding:0 16px;border-radius:999px;background:#F1E7DA;font-size:15px;color:#3A2A20;cursor:pointer;transition:background-color .2s,color .2s}
.of .ch input{position:absolute;opacity:0;width:1px;height:1px;pointer-events:none}
.of .ch:hover{background:#E9DCCA}
.of .ch:has(input:checked){background:#3A2A20;color:#F4EDE4}
.of .ch:has(input:focus-visible){outline:2px solid #9C472C;outline-offset:2px}
.of .altx{display:none;margin-top:12px}
.of form:has(.alt input:checked) .altx{display:flex}
.of .ok{display:flex;align-items:flex-start;gap:12px;font-size:14px;line-height:1.5;color:#4A382C;cursor:pointer}
.of .ok input{flex:none;width:20px;height:20px;margin:1px 0 0;accent-color:#9C472C}
.of .ok a{color:var(--terra-d);text-decoration:underline;text-underline-offset:3px}
.of .note{margin:12px 0 0;font-size:14px;color:var(--ink2)}
.of .send{display:flex;align-items:center;flex-wrap:wrap;gap:12px 20px}
.of .send .note{margin:0}
"""


def form(*parts, cls=""):
    return f'<form class="{cls}" action="#" onSubmit="{{{{ noop }}}}">' + "".join(parts) + "</form>"


# 1. Stripe, contact sales: left the words and what happens next; right the form in a card.
OPTS["CompOferta1Vanzari"] = ("Pentru companii, oferta 1: ca la Stripe", FORM_CSS + """
.o1{background:#EDE0CD}
.o1 .stage{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:72px;align-items:start}
.o1 .steps{margin:40px 0 0;padding:0;list-style:none;counter-reset:s}
.o1 .steps li{position:relative;padding:0 0 22px 52px;counter-increment:s;font-size:16.5px;line-height:1.5;color:#4A382C}
.o1 .steps li::before{content:counter(s);position:absolute;left:0;top:-3px;display:grid;place-items:center;width:32px;height:32px;border-radius:50%;box-shadow:inset 0 0 0 1px rgba(156,71,44,.5);color:var(--terra-d);font:400 italic 17px/1 var(--display)}
.o1 .steps li:not(:last-child)::after{content:"";position:absolute;left:16px;top:34px;bottom:2px;width:1px;background:rgba(58,42,32,.18)}
.o1 .card{padding:36px;border-radius:24px;corner-shape:squircle;background:#FBF7F1;box-shadow:0 0 0 1px rgba(58,42,32,.06),0 30px 60px -44px rgba(70,35,15,.5)}
.o1 .grid{display:grid;grid-template-columns:1fr 1fr;gap:18px 16px}
.o1 .grid .w2{grid-column:1/-1}
.o1 fieldset{margin-top:24px}
.o1 .ok{margin-top:24px}.o1 .send{margin-top:24px}
@media (max-width:980px){
  .o1 .stage{grid-template-columns:1fr;gap:36px}.o1 .steps{margin-top:28px}
  .o1 .card{padding:22px 18px}.o1 .grid{grid-template-columns:1fr}
}
""", '<section class="cs of o1" id="oferta" aria-labelledby="of-h" ref="{{ secRef }}"><div class="wrap stage">'
    f'<div><h2 class="disp ri" id="of-h">{OF_H}</h2><p class="intro ri" style="--i: 1">{OF_SUB}</p>'
    '<ol class="steps ri" style="--i: 2">' + "".join(f"<li>{s}</li>" for s in STEPS) + '</ol></div>'
    '<div class="card ri" style="--i: 2">' + form(
        '<div class="grid">', FIELDS["nume"], FIELDS["firma"], FIELDS["email"], FIELDS["telefon"], FIELDS["persoane"], FIELDS["data"],
        FIELDS["locatie"].replace('class="fi "', 'class="fi w2"'), '</div>', goals(), GDPR_HTML,
        f'<div class="send">{SUBMIT}<p class="note">{OF_NOTE}</p></div>') + '</div></div></section>')

# 2. Airbnb host sign-up: first you pick from big tiles (what the team should get), then the rest of the form below.
OPTS["CompOferta2Alegeri"] = ("Pentru companii, oferta 2: întâi alegi", FORM_CSS + """
.o2{background:#EDE0CD}
.o2 .head{max-width:760px;margin:0 auto;text-align:center}
.o2 .head .intro{margin-left:auto;margin-right:auto}
.o2 form{max-width:1000px;margin:52px auto 0}
.o2 .goals legend{width:100%;margin-bottom:16px;text-align:center;font:400 26px/1.2 var(--display);font-variation-settings:'opsz' 20;color:var(--ink)}
.o2 .opts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.o2 .ch{flex-direction:column;align-items:flex-start;justify-content:space-between;gap:20px;min-height:130px;padding:20px;border-radius:18px;corner-shape:squircle;background:#FBF7F1;box-shadow:0 0 0 1px rgba(58,42,32,.1);font:400 19px/1.25 var(--display);font-variation-settings:'opsz' 20}
.o2 .ch svg{width:34px;height:34px;fill:none;stroke:#B4583A;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.o2 .ch:hover{background:#FFFCF7;box-shadow:0 0 0 1px rgba(58,42,32,.3)}
.o2 .ch:has(input:checked){background:#FFFCF7;color:var(--ink);box-shadow:0 0 0 2px #3A2A20}
.o2 .ch:has(input:checked)::after{content:"";position:absolute;right:16px;top:16px;width:22px;height:22px;border-radius:50%;background:#3A2A20 url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath d='M4 8.5l2.5 2.5L12 5.5' fill='none' stroke='%23F4EDE4' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center/14px no-repeat}
.o2 .rest{margin-top:28px;padding:32px;border-radius:24px;corner-shape:squircle;background:#FBF7F1;box-shadow:0 0 0 1px rgba(58,42,32,.06)}
.o2 .grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px 16px}
.o2 .grid .w2{grid-column:span 2}
.o2 .bot{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:20px 32px;margin-top:24px}
.o2 .ok{max-width:52ch}
@media (max-width:980px){
  .o2 form{margin-top:36px}.o2 .goals legend{font-size:22px}
  .o2 .opts{grid-template-columns:1fr 1fr;gap:8px}.o2 .ch{min-height:110px;padding:14px;font-size:16.5px}
  .o2 .rest{padding:22px 18px}.o2 .grid{grid-template-columns:1fr}.o2 .grid .w2{grid-column:auto}
  .o2 .bot{flex-direction:column;align-items:stretch}.o2 .send{flex-direction:column;align-items:stretch;text-align:center}
}
""", '<section class="cs of o2" id="oferta" aria-labelledby="of-h" ref="{{ secRef }}"><div class="wrap">'
    f'<div class="head"><h2 class="disp ri" id="of-h">{OF_H}</h2><p class="intro ri" style="--i: 1">{OF_SUB}</p></div>'
    '<div class="ri" style="--i: 2">' + form(goals(big=True),
        '<div class="rest"><div class="grid">', FIELDS["nume"], FIELDS["firma"], FIELDS["email"], FIELDS["telefon"],
        FIELDS["persoane"], FIELDS["data"], FIELDS["locatie"].replace('class="fi "', 'class="fi w2"'), '</div>',
        f'<div class="bot">{GDPR_HTML}<div class="send">{SUBMIT}<p class="note">{OF_NOTE}</p></div></div></div>') + '</div></div></section>')

# 3. Aman, enquiry: centred and quiet, fields drawn only with a line underneath, serif labels.
OPTS["CompOferta3Liniste"] = ("Pentru companii, oferta 3: liniștit", FORM_CSS + """
.o3{background:linear-gradient(180deg,#EDE0CD 0%,#E6D5BD 100%)}
.o3 .in{max-width:720px;margin:0 auto;text-align:center}
.o3 .intro{margin-left:auto;margin-right:auto}
.o3 form{margin-top:48px;text-align:left}
.o3 .grid{display:grid;grid-template-columns:1fr 1fr;gap:26px 40px}
.o3 .fl{font:400 italic 18px/1.3 var(--display);font-variation-settings:'opsz' 20;color:var(--terra-d)}
.o3 .fl small{font:400 13px var(--text);color:var(--ink2)}
.o3 input:not([type=checkbox]),.o3 textarea{min-height:44px;padding:8px 0;border:0;border-bottom:1px solid rgba(58,42,32,.35);border-radius:0;background:transparent}
.o3 input:not([type=checkbox]):focus,.o3 textarea:focus{box-shadow:0 1px 0 0 #9C472C;border-color:#9C472C}
.o3 fieldset{margin-top:40px;text-align:center}
.o3 legend{width:100%}
.o3 .opts{justify-content:center}
.o3 .ch{background:transparent;box-shadow:inset 0 0 0 1px rgba(58,42,32,.3)}
.o3 .ch:hover{background:rgba(251,247,241,.6)}
.o3 .ok{max-width:56ch;margin:40px auto 0}
.o3 .send{flex-direction:column;margin-top:28px}
@media (max-width:980px){.o3 form{margin-top:32px}.o3 .grid{grid-template-columns:1fr;gap:20px}.o3 .send{align-items:stretch;text-align:center}}
""", '<section class="cs of o3" id="oferta" aria-labelledby="of-h" ref="{{ secRef }}"><div class="wrap"><div class="in">'
    f'<h2 class="disp ri" id="of-h">{OF_H}</h2><p class="intro ri" style="--i: 1">{OF_SUB}</p>'
    '<div class="ri" style="--i: 2">' + form('<div class="grid">', FIELDS["nume"], FIELDS["firma"], FIELDS["email"], FIELDS["telefon"],
        FIELDS["persoane"], FIELDS["data"], FIELDS["locatie"].replace('class="fi "', 'class="fi" style="grid-column: 1 / -1"'), '</div>',
        goals(), GDPR_HTML, f'<div class="send">{SUBMIT}<p class="note">{OF_NOTE}</p></div>') + '</div></div></div></section>')

# 4. Typeform: one question at a time in a dark card, a progress bar, back / next.
STEP_H = ["Ce vă doriți?", "Despre echipă", "Cum vă contactăm"]   # MINE
OPTS["CompOferta4Pasi"] = ("Pentru companii, oferta 4: pas cu pas", FORM_CSS + """
.o4{background:#EDE0CD}
.o4 .stage{display:grid;grid-template-columns:minmax(0,4fr) minmax(0,7fr);gap:64px;align-items:center}
.o4 .card{position:relative;padding:40px 44px 36px;border-radius:26px;corner-shape:squircle;background:#3A2A20;color:#F4EDE4;box-shadow:0 40px 80px -50px rgba(46,28,19,.8)}
.o4 .bar{height:3px;border-radius:3px;background:rgba(244,237,228,.16);overflow:hidden}
.o4 .bar i{display:block;height:100%;width:calc(var(--s,1) * 33.34%);background:#F2C79C;transition:width .5s var(--so)}
.o4 .cnt{margin:14px 0 0;font-size:13.5px;color:#D8C6B2;font-variant-numeric:tabular-nums}
.o4 .st{display:none;min-height:300px;flex-direction:column}
.o4 .st.on{display:flex}
@keyframes o4-in{from{opacity:0;translate:24px 0}}
@media (prefers-reduced-motion:no-preference){.o4 .st.on{animation:o4-in .45s var(--so)}}
.o4 .st h3{margin:18px 0 24px;font-size:32px;color:#F4EDE4}
.o4 .fl{color:#EFE3D3}.o4 .fl small{color:#BFA994}
.o4 legend{display:none}
.o4 input:not([type=checkbox]),.o4 textarea{background:rgba(244,237,228,.06);border-color:rgba(244,237,228,.24);color:#F4EDE4;color-scheme:dark}
.o4 input::placeholder{color:#A8917D}
.o4 input:not([type=checkbox]):focus,.o4 textarea:focus{border-color:#F2C79C;box-shadow:0 0 0 3px rgba(242,199,156,.2)}
.o4 .ch{background:rgba(244,237,228,.08);color:#F4EDE4;box-shadow:inset 0 0 0 1px rgba(244,237,228,.2)}
.o4 .ch:hover{background:rgba(244,237,228,.14)}
.o4 .ch:has(input:checked){background:#F4EDE4;color:#2E1D14}
.o4 .grid{display:grid;grid-template-columns:1fr 1fr;gap:18px 16px}
.o4 .ok{margin-top:20px;color:#D8C6B2}.o4 .ok a{color:#F2C79C}
.o4 .nav{display:flex;align-items:center;justify-content:space-between;gap:16px;margin-top:auto;padding-top:28px}
.o4 .back{display:inline-flex;align-items:center;min-height:44px;padding:0 4px;border:0;background:none;color:#EFE3D3;font:500 15px var(--text);cursor:pointer;text-decoration:underline;text-underline-offset:5px}
.o4 .back[hidden]{display:inline-flex;visibility:hidden}
.o4 .btn{background:#F4EDE4;color:#2E1D14}.o4 .btn:hover{background:#FFF8EE}.o4 .btn:focus-visible{outline-color:#F2C79C}
.o4 .card .note{color:#BFA994}
@media (max-width:980px){
  .o4 .stage{grid-template-columns:1fr;gap:32px}.o4 .card{padding:26px 20px 24px}
  .o4 .st{min-height:0}.o4 .st h3{font-size:26px}.o4 .grid{grid-template-columns:1fr}
  .o4 .nav{flex-direction:column-reverse;align-items:stretch}.o4 .nav .btn{width:100%}
}
""", '<section class="cs of o4" id="oferta" aria-labelledby="of-h" ref="{{ secRef }}"><div class="wrap stage">'
    f'<div><h2 class="disp ri" id="of-h">{OF_H}</h2><p class="intro ri" style="--i: 1">{OF_SUB}</p><p class="note ri" style="--i: 2">{OF_NOTE}</p></div>'
    '<div class="card ri" style="--i: 2; --s: 1"><div class="bar"><i></i></div><p class="cnt" aria-live="polite">Pasul <b class="n">1</b> din 3</p>'
    + form(
        f'<div class="st on" data-s="1"><h3>{STEP_H[0]}</h3>{goals()}<div class="nav"><button type="button" class="back" hidden>Înapoi</button><button type="button" class="btn" onClick="{{{{ next }}}}">Mai departe</button></div></div>',
        f'<div class="st" data-s="2"><h3>{STEP_H[1]}</h3><div class="grid">{FIELDS["persoane"]}{FIELDS["data"]}{FIELDS["locatie"].replace('class="fi "', 'class="fi" style="grid-column: 1 / -1"')}</div>'
        f'<div class="nav"><button type="button" class="back" onClick="{{{{ back }}}}">Înapoi</button><button type="button" class="btn" onClick="{{{{ next }}}}">Mai departe</button></div></div>',
        f'<div class="st" data-s="3"><h3>{STEP_H[2]}</h3><div class="grid">{FIELDS["nume"]}{FIELDS["firma"]}{FIELDS["email"]}{FIELDS["telefon"]}</div>{GDPR_HTML}'
        f'<div class="nav"><button type="button" class="back" onClick="{{{{ back }}}}">Înapoi</button>{SUBMIT}</div></div>')
    + '</div></div></section>')

FAQ_HTML = ('<section class="fq f3" id="intrebari" aria-labelledby="fq-h" ref="{{ secRef }}"><div class="wrap">'
            f'<div class="head ri"><h2 class="disp" id="fq-h">{fq.H}</h2></div><div class="cards"><div class="acc ri" style="--i: 1">'
            + "".join(f'<details name="faq-companii"{" open" if i == 0 else ""}><summary><span class="qq">{q}</span>{fq.ICON}</summary>'
                      f'<div class="ans"><p>{a}</p></div></details>' for i, (q, a) in enumerate(QA))
            + f'</div><aside class="other ri" style="--i: 2" aria-label="{fq.ASK}"><p class="ask">{fq.ASK}</p><p class="reply">{fq.REPLY}</p>'
            f'<div class="links">{fq.WRITE}{fq.ALL}</div></aside></div></div></section>')

STEPPER = """
    next: function (e) { self.go(1); },
    back: function (e) { self.go(-1); },
    noop: function (e) { e.preventDefault(); },"""
GO = """
  go(d) {
    var s = this.sec, c = s.querySelector('.card'), cur = +(c.style.getPropertyValue('--s') || 1), n = Math.max(1, Math.min(3, cur + d));
    c.style.setProperty('--s', n);
    s.querySelectorAll('.st').forEach(function (x) { x.classList.toggle('on', +x.getAttribute('data-s') === n); });
    s.querySelector('.cnt .n').textContent = n;
    var f = s.querySelector('.st.on input, .st.on button.btn'); if (f) f.focus({ preventScroll: true });
  }"""


def script():
    return ("class Component extends DCLogic {\n  componentDidMount() {" + ENTER + "\n  }\n"
            "  componentWillUnmount() { if (this.io) this.io.disconnect(); }\n" + GO + "\n"
            "  renderVals() { var self = this; if (!this.cb) this.cb = {" + STEPPER + " secRef: function (el) { self.sec = el; } }; return this.cb; }\n}")


def page(name, title, css, html, w, h):
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
<div class="pg" data-src="{SOURCES[name]}">
{html}
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{w},"height":{h}}}}}'>
{script()}
</script>
</body>
</html>
"""


ALL_OPTS = dict(OPTS)
ALL_OPTS["CompDetalii"] = ("Pentru companii: cum funcționează + cine facilitează", DET_CSS, DET_HTML)
ALL_OPTS["CompFaq"] = ("Pentru companii: întrebări frecvente", gp.FAQ_CSS, FAQ_HTML)
for k in list(ALL_OPTS):
    t, css, html = ALL_OPTS[k]
    if k.startswith(("CompFormate", "CompOferta")):
        ALL_OPTS[k] = (t, SEC + css, html)

# preview heights, measured in the browser (desktop 1440, phone 390)
H = {"CompHero": (905, 789)}
H.update({"CompFormate1Planuri": (892, 1188), "CompFormate2Nevoi": (1047, 1228), "CompFormate3Editorial": (1015, 1298),
          "CompFormate4Fisa": (1063, 1346), "CompOferta1Vanzari": (1023, 1749), "CompOferta2Alegeri": (1220, 1769),
          "CompOferta3Liniste": (1213, 1494), "CompOferta4Pasi": (647, 949), "CompDetalii": (932, 1301), "CompFaq": (961, 1178)})

if __name__ == "__main__":
    gh.SOURCES["CompHero"] = SOURCES["CompHero"]
    hero_css = gh.OPTS["GrupHero2Aman"][2]
    for suffix, w, h in (("", 1440, H["CompHero"][0]), ("Mobil", 390, H["CompHero"][1])):
        f = os.path.join(P, f"CompHero{suffix}.dc.html")
        open(f, "w", encoding="utf-8").write(gh.page("CompHero", "Pentru companii: deschiderea" + (" · mobil" if suffix else ""), "dark", hero_css, HERO_HTML, w, h))
        if not suffix:
            subprocess.run([sys.executable, os.path.join(HERE, "dc2html.py"), f, os.path.join(HERE, "opt-CompHero.html")], check=True, capture_output=True)
    for name, (title, css, html) in ALL_OPTS.items():
        for suffix, w, h in (("", 1440, H[name][0]), ("Mobil", 390, H[name][1])):
            f = os.path.join(P, f"{name}{suffix}.dc.html")
            open(f, "w", encoding="utf-8").write(page(name, title + (" · mobil" if suffix else ""), css, html, w, h))
            if not suffix:
                subprocess.run([sys.executable, os.path.join(HERE, "dc2html.py"), f, os.path.join(HERE, f"opt-{name}.html")], check=True, capture_output=True)
    print("wrote", ["CompHero"] + list(ALL_OPTS))
