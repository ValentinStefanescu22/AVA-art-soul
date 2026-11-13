"""Ce oferim, the last three service pages (Vali, 12 nov: „hai să facem și restul paginilor de servicii”), on the template
(the „Ateliere de grup” page: hero 2 Aman · „Cum funcționează” · FAQ 3 cards).

Atelier privat 1:1
  PrivHero, PrivDetalii, PrivFaq   the template, this page's copy
  PrivAteliere1..4                 NEW, four variants: the two workshops (stagiul de modelaj · autocunoaștere prin lut și joacă)
  The booking calendar is the one chosen on Consiliere 1:1 (same Cal.com embed), so it is not redesigned here.
Pentru școli și copii
  ScoliHero, ScoliDetalii, ScoliFaq the template; the doc has no other content for a new section.
Retreaturi (Vali, 12 nov: only „În curând”)
  Retreat1..4                      NEW, four variants of the whole „coming soon” page, with the newsletter sign-up.

usage: python3 .aidesigner/servicii_options.py
Copy: docs/continut-site.md. Mine, to approve (MINE below). Photos: the Ce oferim ones are provisional (Unsplash).
CLAUDE.md: the children's note („nu înlocuiesc terapia logopedică…”) stays on the private workshop, word for word.
"""
import os, subprocess, sys
from about_options2 import P, HERE, FONTS, BASE_CSS, ARROW, BG
import grup_hero_options as gh
import grup_page_options as gp
import faq_options as fq
import companii_options as co
from ce_facem2_options import IMG, ALT, POS
from cf_pagina_options import ENTER


def ph(k):
    return (IMG[k], ALT[k], POS[k])


def h1(title):
    k, ws = 0, []
    for w in title.split():
        ls = []
        for ch in w:
            ls.append(f'<span class="l" style="--k: {k}">{ch}</span>'); k += 1
        ws.append('<span class="w" aria-hidden="true">' + "".join(ls) + "</span>")
    return f'<h1 class="disp gh" id="gh-h" aria-label="{title}">' + " ".join(ws) + "</h1>"


def hero(title, lede, pills, cta, href, photo):
    return ('<section class="gp g2" aria-labelledby="gh-h" ref="{{ secRef }}">'
            f'<div class="bg">{gh.pic(photo)}</div><div class="in">{h1(title)}<p class="lede up" style="--d: .55s">{lede}</p>'
            f'<ul class="pills up" style="--d: .7s">{"".join(f"<li>{m}</li>" for m in pills)}</ul>'
            f'<div class="up" style="--d: .85s"><a class="btn" href="{href}">{cta}</a></div></div></section>')


def details(how, facts, card_q, card_p, card_btn, card_href, extra=""):
    return ('<section class="gd" aria-labelledby="gd-h" ref="{{ secRef }}"><div class="wrap">'
            f'<h2 class="disp ri" id="gd-h">Cum funcționează</h2><p class="how ri" style="--i: 1">{how}</p><dl>'
            + "".join(f'<div class="ri" style="--i: {i + 2}"><dt>{a}</dt><dd>{b}</dd></div>' for i, (a, b) in enumerate(facts))
            + f'</dl><aside class="co ri" style="--i: 2" aria-label="{card_q}"><div><p class="q">{card_q}</p><p>{card_p}</p></div>'
            f'<a class="btn-c" href="{card_href}">{card_btn}</a></aside>{extra}</div></section>')


def faq(qa, name):
    return ('<section class="fq f3" id="intrebari" aria-labelledby="fq-h" ref="{{ secRef }}"><div class="wrap">'
            f'<div class="head ri"><h2 class="disp" id="fq-h">{fq.H}</h2></div><div class="cards"><div class="acc ri" style="--i: 1">'
            + "".join(f'<details name="faq-{name}"{" open" if i == 0 else ""}><summary><span class="qq">{q}</span>{fq.ICON}</summary>'
                      f'<div class="ans"><p>{a}</p></div></details>' for i, (q, a) in enumerate(qa))
            + f'</div><aside class="other ri" style="--i: 2" aria-label="{fq.ASK}"><p class="ask">{fq.ASK}</p><p class="reply">{fq.REPLY}</p>'
            f'<div class="links">{fq.WRITE}{fq.ALL}</div></aside></div></div></section>')


# =================== Atelier privat 1:1 ===================
PRIV_TITLE = "Atelier privat 1:1"
PRIV_LEDE = "Lutul, tu și eu. Un atelier de modelaj, în ritmul tău, fără grup și fără grabă. Pentru adult sau copil."
PRIV_PILLS = ["pentru adult sau copil", "60 sau 90 de minute", "pentru 1 sau 2 persoane", "și ca voucher-cadou"]   # MINE, from the doc
PRIV_CTA = "Alege atelierul"                                      # MINE
THERAPY = "Atelierele noastre nu înlocuiesc terapia logopedică, ocupațională sau kinetoterapia, dar le pot completa frumos."
OPTIONS = "Pentru o persoană sau pentru două (cupluri, mamă-fiică), și ca voucher-cadou."
OFFERS = [
    dict(k="modelaj", name="Stagiul de modelaj 1:1", short="tehnici și proiecte personale", photo=gh.CLAY,
         lists=[("Este pentru tine dacă:", ["Îți dorești să înveți tehnici specifice de modelaj.", "Vrei să aduci la viață proiecte personale.",
                                           "Îți dorești să realizezi obiecte sau proiecte complexe, care necesită timp și mai multă atenție."])],
         dur="60 de minute ședința, 4 ședințe pe lună", price=("600 lei", "480 lei"), incl="Prețul include și materialele și arderea piesei.",
         btn="Rezervă stagiul de modelaj privat", note=""),
    dict(k="autocunoastere", name="Autocunoaștere prin lut și joacă", short="pentru adult sau pentru copilul tău", photo=gh.HANDS,
         lists=[("Pentru tine, dacă:", ["Îți e greu să pui în cuvinte ce simți?", "Te deschizi greu în fața altora, mai ales într-un grup?",
                                       "Te simți inconfortabil când trebuie să fii vulnerabil, dar îți dorești totuși să te cunoști mai bine?"]),
                ("Pentru copilul tău, dacă:", ["Îi e greu să comunice ce simte sau ce gândește?", "Are nevoie să-și dezvolte motricitatea fină sau grosieră?",
                                              "Lucrează la coordonarea mișcărilor și are nevoie de o activitate care să-i placă?",
                                              "Se simte mai în largul lui când se joacă decât când vorbește?"])],
         dur="90 de minute", price=("250 lei", "220 lei"), incl="Prețul include materialele. Arderea piesei este opțională.",
         btn="Rezervă atelierul de autocunoaștere prin lut", note=THERAPY),
]
PA_H = "Alege atelierul"                                           # MINE
PRIV_QA = [  # Întrebări frecvente (Atelier privat 1:1), word for word
    ("Trebuie să știu să modelez?", "Nu. Aici nu contează cât de frumos iese, ci ce descoperi pe drum."),
    ("De la ce vârstă pot veni copiii?", "De la 5 ani."),
    ("Pot să stau lângă copilul meu în timpul atelierului?", "Recomandăm să-l lași singur, iar la final îți povestim cum a fost."),
    ("Înlocuiește atelierul terapia de care are nevoie copilul meu?", THERAPY),
    ("Pot oferi un atelier privat cadou?", "Da, scrie-ne."),
    ("Când primesc piesa?", "După uscare și ardere, în aproximativ 4-6 săptămâni."),
]


def lists(o, cls="ls"):
    return "".join(f'<div class="{cls}"><p class="lt">{h}</p><ul>' + "".join(f"<li>{x}</li>" for x in xs) + "</ul></div>" for h, xs in o["lists"]) \
        + (f'<p class="th">{o["note"]}</p>' if o["note"] else "")


def facts(o):
    a, c = o["price"]
    return ('<dl class="fx">'
            f'<div><dt>Durată</dt><dd>{o["dur"]}</dd></div>'
            f'<div><dt>Opțiuni</dt><dd>{OPTIONS}</dd></div>'
            f'<div><dt>Preț</dt><dd><span class="pp"><b>{a}</b> adult</span><span class="pp"><b>{c}</b> copil</span><small>{o["incl"]}</small></dd></div></dl>')


def btn(o):
    return f'<a class="btn" href="#programare">{o["btn"]}</a>'


PA_CSS = """
.pa{background:linear-gradient(180deg,#F4EDE4 0%,#EDE0CD 100%)}
.pa .lt{margin:0 0 10px;font:400 italic 20px/1.3 var(--display);font-variation-settings:'opsz' 20;color:var(--terra-d)}
.pa .ls ul{margin:0;padding:0;list-style:none}
.pa .ls li{position:relative;padding:8px 0 8px 22px;font-size:16.5px;line-height:1.5;color:#4A382C;border-top:1px solid rgba(58,42,32,.1)}
.pa .ls li::before{content:"";position:absolute;left:2px;top:17px;width:8px;height:8px;border-radius:50%;box-shadow:inset 0 0 0 1.5px #B4583A}
.pa .ls+.ls{margin-top:24px}
.pa .th{margin:20px 0 0;padding:14px 16px;border-radius:14px;background:rgba(111,123,92,.12);font-size:15px;line-height:1.55;color:#4F5A43}
.pa .fx{margin:0;border-top:1px solid rgba(58,42,32,.18)}
.pa .fx>div{display:grid;grid-template-columns:96px minmax(0,1fr);gap:16px;padding:14px 0;border-bottom:1px solid rgba(58,42,32,.18)}
.pa .fx dt{font:400 italic 18px/1.4 var(--display);font-variation-settings:'opsz' 20;color:var(--terra-d)}
.pa .fx dd{margin:0;font-size:15.5px;line-height:1.55;color:#4A382C}
.pa .pp{display:inline-flex;align-items:baseline;gap:6px;margin-right:18px;color:var(--ink2);font-variant-numeric:tabular-nums}
.pa .pp b{font:400 26px/1.2 var(--display);font-variation-settings:'opsz' 20;color:var(--ink)}
.pa .fx small{display:block;margin-top:4px;font-size:14px;color:var(--ink2)}
.pa .act{margin-top:24px}
@media (max-width:980px){.pa .fx>div{grid-template-columns:1fr;gap:2px}.pa .pp b{font-size:23px}.pa .btn{white-space:normal;text-align:center;line-height:1.3;padding:12px 20px}.pa .col,.pa .row>*,.pa .pane>*{min-width:0}}
"""

PA = {}
# 1. apple.com/compare: the two side by side, the same rows lined up, so the differences show at a glance.
PA["PrivAteliere1Comparat"] = ("Atelier privat, cele două ateliere 1: comparate", PA_CSS + """
.p1 .cols{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:48px}
.p1 .col{display:flex;flex-direction:column;padding:12px 12px 28px;border-radius:24px;corner-shape:squircle;background:#FBF7F1;box-shadow:0 0 0 1px rgba(58,42,32,.06)}
.p1 .im{aspect-ratio:16/9;border-radius:16px;overflow:hidden}.p1 .im img{display:block;width:100%;height:100%;object-fit:cover}
.p1 .bd{display:flex;flex-direction:column;flex:1;padding:24px 16px 0}
.p1 h3{font-size:30px}
.p1 .sh{margin:6px 0 24px;font-size:15px;color:var(--ink2)}
.p1 .who{flex:1;margin-bottom:28px}
@media (max-width:980px){.p1 .cols{grid-template-columns:1fr;gap:12px;margin-top:32px}.p1 .bd{padding:18px 8px 0}.p1 h3{font-size:25px}}
""", '<section class="cs pa p1" id="ateliere" aria-labelledby="pa-h" ref="{{ secRef }}"><div class="wrap">'
    f'<h2 class="disp ri" id="pa-h">{PA_H}</h2><div class="cols">' + "".join(
        f'<article class="col ri" style="--i: {i + 1}"><div class="im">{gh.pic(o["photo"])}</div><div class="bd"><h3>{o["name"]}</h3><p class="sh">{o["short"]}</p>'
        f'<div class="who">{lists(o)}</div>{facts(o)}<div class="act">{btn(o)}</div></div></article>' for i, o in enumerate(OFFERS))
    + "</div></div></section>")

# 2. apple.com/shop/buy: a segmented switch chooses the workshop; the details on the left, price and button in a card.
def seg(items, group, cls="seg"):
    return (f'<div class="{cls}" role="tablist">' + "".join(
        f'<button type="button" role="tab" data-g="{group}" data-k="{k}" aria-selected="{"true" if i == 0 else "false"}" onClick="{{{{ tab }}}}">{n}</button>'
        for i, (k, n) in enumerate(items)) + "</div>")


PA["PrivAteliere2Comutator"] = ("Atelier privat, cele două ateliere 2: comutator", PA_CSS + """
.p2 .head{display:flex;align-items:end;justify-content:space-between;flex-wrap:wrap;gap:20px 40px}
.p2 .seg{display:inline-flex;padding:4px;border-radius:999px;background:#E9DCCA}
.p2 .seg button{min-height:44px;padding:0 20px;border:0;border-radius:999px;background:none;font:500 15px/1 var(--text);color:#4A382C;cursor:pointer;transition:background-color .25s,color .25s}
.p2 .seg button[aria-selected="true"]{background:#3A2A20;color:#F4EDE4}
.p2 .seg button:focus-visible{outline:2px solid #9C472C;outline-offset:2px}
.p2 .pane{display:none;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:48px;margin-top:44px}
.p2 .pane.on{display:grid}
@keyframes p2-in{from{opacity:0;translate:0 10px}}
@media (prefers-reduced-motion:no-preference){.p2 .pane.on{animation:p2-in .4s var(--so)}}
.p2 .card{align-self:start;padding:28px;border-radius:24px;corner-shape:squircle;background:#FBF7F1;box-shadow:0 0 0 1px rgba(58,42,32,.06),0 30px 60px -44px rgba(70,35,15,.5)}
.p2 .card h3{margin-bottom:18px}
.p2 .card .btn{width:100%;box-sizing:border-box;white-space:normal;text-align:center;line-height:1.3;padding:12px 24px}
.p2 .im{aspect-ratio:16/9;margin-bottom:28px;border-radius:20px;overflow:hidden}.p2 .im img{display:block;width:100%;height:100%;object-fit:cover}
@media (max-width:980px){.p2 .seg{display:flex;width:100%;box-sizing:border-box}.p2 .seg button{flex:1;padding:0 10px;font-size:14px}.p2 .pane{grid-template-columns:1fr;gap:24px;margin-top:28px}.p2 .card{padding:20px}}
""", '<section class="cs pa p2" id="ateliere" aria-labelledby="pa-h" ref="{{ secRef }}"><div class="wrap">'
    f'<div class="head"><h2 class="disp ri" id="pa-h">{PA_H}</h2><div class="ri" style="--i: 1">{seg([(o["k"], o["name"]) for o in OFFERS], "of")}</div></div>'
    + "".join(f'<div class="pane{" on" if i == 0 else ""}" role="tabpanel" data-g="of" data-p="{o["k"]}"><div><div class="im">{gh.pic(o["photo"])}</div>{lists(o)}</div>'
              f'<div class="card"><h3>{o["name"]}</h3>{facts(o)}<div class="act">{btn(o)}</div></div></div>' for i, o in enumerate(OFFERS))
    + "</div></section>")

# 3. Monocle: long features with the photo once on the left, once on the right.
PA["PrivAteliere3Alternat"] = ("Atelier privat, cele două ateliere 3: alternat", PA_CSS + """
.p3 .row{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,6fr);gap:72px;align-items:start;margin-top:64px}
.p3 .row:nth-of-type(even) .im{order:2}
.p3 .im{position:sticky;top:96px;aspect-ratio:4/5;border-radius:24px;corner-shape:squircle;overflow:hidden}.p3 .im img{display:block;width:100%;height:100%;object-fit:cover}
.p3 .n{display:block;margin-bottom:10px;font:400 italic 20px/1 var(--display);font-variation-settings:'opsz' 20;color:var(--terra-d)}
.p3 h3{font-size:clamp(32px,3vw,44px);margin-bottom:28px}
.p3 .fx{margin-top:28px}
@media (max-width:980px){.p3 .row{grid-template-columns:1fr;gap:24px;margin-top:40px}.p3 .row:nth-of-type(even) .im{order:0}.p3 .im{position:static;aspect-ratio:4/3}.p3 h3{font-size:28px;margin-bottom:20px}}
""", '<section class="cs pa p3" id="ateliere" aria-labelledby="pa-h" ref="{{ secRef }}"><div class="wrap">'
    f'<h2 class="disp ri" id="pa-h">{PA_H}</h2>' + "".join(
        f'<article class="row"><div class="im ri">{gh.pic(o["photo"])}</div><div class="ri" style="--i: 1"><span class="n">0{i + 1}</span><h3>{o["name"]}</h3>'
        f'{lists(o)}{facts(o)}<div class="act">{btn(o)}</div></div></article>' for i, o in enumerate(OFFERS))
    + "</div></section>")

# 4. The photo accordion chosen on Acasă (Ce oferim): two big rows, one open at a time.
PA["PrivAteliere4Acordeon"] = ("Atelier privat, cele două ateliere 4: acordeon", PA_CSS + """
.p4 .acc{margin-top:44px;border-top:1px solid rgba(58,42,32,.22)}
.p4 details{border-bottom:1px solid rgba(58,42,32,.22)}
.p4 summary{display:grid;grid-template-columns:120px minmax(0,1fr) auto;align-items:center;gap:28px;padding:22px 0;cursor:pointer;list-style:none}
.p4 summary::-webkit-details-marker{display:none}
.p4 summary .th2{width:120px;height:80px;border-radius:14px;overflow:hidden}.p4 summary .th2 img{display:block;width:100%;height:100%;object-fit:cover}
.p4 summary b{display:block;font:400 clamp(28px,2.8vw,40px)/1.1 var(--display);font-variation-settings:'opsz' 20}
.p4 summary span.s{font-size:15px;color:var(--ink2)}
.p4 .ic{display:grid;place-items:center;width:48px;height:48px;border-radius:50%;box-shadow:inset 0 0 0 1px rgba(58,42,32,.25);transition:rotate .35s var(--so),background-color .25s}
.p4 .ic svg{width:16px;height:16px;fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round}
.p4 details[open] .ic{rotate:45deg;background:#3A2A20;color:#F4EDE4}
.p4 summary:focus-visible{outline:2px solid #9C472C;outline-offset:4px;border-radius:8px}
.p4 .bd2{display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:48px;padding:8px 0 36px 148px}
@media (prefers-reduced-motion:no-preference){.p4 details[open] .bd2{animation:cs-up .5s var(--so)}}
@media (max-width:980px){.p4 summary{grid-template-columns:64px minmax(0,1fr) auto;gap:14px}.p4 summary .th2{width:64px;height:64px}.p4 summary b{font-size:22px}.p4 .ic{width:40px;height:40px}.p4 .bd2{grid-template-columns:1fr;gap:24px;padding:4px 0 28px}}
""", '<section class="cs pa p4" id="ateliere" aria-labelledby="pa-h" ref="{{ secRef }}"><div class="wrap">'
    f'<h2 class="disp ri" id="pa-h">{PA_H}</h2><div class="acc ri" style="--i: 1">' + "".join(
        f'<details name="priv"{" open" if i == 0 else ""}><summary><span class="th2">{gh.pic(o["photo"])}</span><span><b>{o["name"]}</b><span class="s">{o["short"]}</span></span>'
        '<span class="ic" aria-hidden="true"><svg viewBox="0 0 16 16"><path d="M3 8H13M8 3V13"></path></svg></span></summary>'
        f'<div class="bd2"><div>{lists(o)}</div><div>{facts(o)}<div class="act">{btn(o)}</div></div></div></details>' for i, o in enumerate(OFFERS))
    + "</div></div></section>")

PRIV_DET = details("Nu contează cât de frumos iese, ci ce descoperi pe drum.",
                   [("Pentru cine", "Adulți și copii de la 5 ani."), ("Opțiuni", OPTIONS), ("Piesa ta", "După uscare și ardere, în aproximativ 4–6 săptămâni."), ("Unde", '<span class="todo">[UNDE]</span>')],
                   "Vrei să-l oferi cadou?", "Atelierul privat se poate oferi și ca voucher-cadou.", "Scrie-ne", "#contact")   # MINE: the card's two lines

# =================== Pentru școli și copii ===================
SC_TITLE = "Pentru școli și copii"
SC_LEDE = ("Modelaj în lut, gândit într-un mod ludic și educațional: copiii învață despre argilă și tehnici de modelare, "
           "păstrând totodată distracția și curiozitatea momentului.")
SC_PILLS = ["de la 6 ani", "60 de minute", "50 lei / copil", "Școala altfel · Săptămâna verde"]   # MINE, from the doc
SC_FACTS = [("Vârstă", "De la 6 ani."), ("Durată", "60 de minute."),
            ("Preț", "50 lei / copil. 10% reducere pentru grupuri de minimum 20 de copii."),
            ("Materiale", "Ne ocupăm noi de materiale, iar cei mici își pot lua obiectul modelat acasă.")]
SC_QA = [("Pentru ce vârste sunt atelierele?", "De la 6 ani."), ("Veniți la noi la școală sau la afterschool?", "Da, venim cu toate materialele."),
         ("Cât durează un atelier?", "O oră.")]
SC_DET = details("Pentru Școala altfel, Săptămâna verde sau afterschool: venim cu toate materialele.",
                 SC_FACTS, "Vreți un atelier la voi?", "Spune-ne câți copii sunt și ce perioadă vă convine.", "Scrie-ne", "#contact")   # MINE: card lines

# =================== Retreaturi: „În curând” ===================
RT_TITLE = "Retreaturi"
RT_LEDE = "Câteva zile departe de oraș, cu lut, natură, liniște și oameni care caută același lucru ca tine."
RT_SOON = "În curând"
RT_TEXT = "Următorul retreat e în pregătire. Lasă-ne emailul și beneficiază de un extra discount la lansare."
RT_BTN = "Anunță-mă la lansare"                                   # the label on Acasă
RT_GDPR = 'Sunt de acord să primesc emailuri de la AVA Art &amp; Soul. Te poți dezabona oricând. <a href="#confidentialitate">Politica de confidențialitate</a>'   # MINE
RT_PHOTO = ph("retreat")


def signup(cls=""):
    return (f'<form class="nl {cls}" action="#" onSubmit="{{{{ noop }}}}"><label class="fi"><span class="fl">Email</span>'
            '<span class="row"><input type="email" name="email" autocomplete="email" required placeholder="numele@email.ro">'
            f'<button class="btn" type="submit">{RT_BTN}</button></span></label>'
            f'<label class="ok"><input type="checkbox" name="gdpr" required><span>{RT_GDPR}</span></label></form>')


NL_CSS = co.FORM_CSS.replace(".of", ".rt") + """
.rt .nl{max-width:560px}
.rt .nl .row{display:flex;gap:8px}
.rt .nl input[type=email]{flex:1}
.rt .nl .btn{flex:none;min-height:50px}
.rt .nl .ok{margin-top:14px}
.rt .soon{display:inline-flex;align-items:center;min-height:34px;padding:0 16px;border-radius:999px;font-size:14px;font-weight:600;letter-spacing:.04em}
@media (max-width:980px){.rt .nl .row{flex-direction:column}.rt .nl .btn{width:100%}}
"""
RT = {}
# 1. The template hero (Aman), with the sign-up inside it: the whole page is one quiet screen.
RT["Retreat1Ecran"] = ("Retreaturi 1: un singur ecran", "dark", NL_CSS + """
.rt.g2{min-height:900px}
.rt.g2 .soon{margin-bottom:22px;background:rgba(244,237,228,.12);box-shadow:inset 0 0 0 1px rgba(244,237,228,.35);color:#F4EDE4;-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px)}
.rt.g2 .nl{margin:34px auto 0;text-align:left}
.rt.g2 .t2{margin:18px auto 0;max-width:40ch;color:#EFE3D3;font-size:17px;line-height:1.6}
.rt.g2 .fl{color:#EFE3D3}
.rt.g2 input[type=email]{background:rgba(244,237,228,.1);border-color:rgba(244,237,228,.35);color:#F4EDE4}
.rt.g2 input::placeholder{color:#CDB9A4}
.rt.g2 .ok{color:#E2D3C1}.rt.g2 .ok a{color:#F2C79C}
.rt.g2 .btn{margin:0;background:#F4EDE4;color:#2E1D14}
.rt.g2 .in{padding-bottom:240px}
""", '<section class="gp g2 rt" aria-labelledby="gh-h" ref="{{ secRef }}">'
    f'<div class="bg">{gh.pic(RT_PHOTO)}</div><div class="in"><span class="soon up" style="--d: .2s">{RT_SOON}</span>{h1(RT_TITLE)}'
    f'<p class="lede up" style="--d: .55s">{RT_LEDE}</p><p class="t2 up" style="--d: .7s">{RT_TEXT}</p><div class="up" style="--d: .85s">{signup()}</div></div></section>')

# 2. A split screen, like Squarespace's „coming soon” pages: the photo fills one half, the words and the form the other.
RT["Retreat2Jumatate"] = ("Retreaturi 2: jumătate-jumătate", "light", NL_CSS + """
.r2{display:grid;grid-template-columns:1fr 1fr;min-height:900px;padding:96px 0 24px 24px;box-sizing:border-box;background:#F4EDE4}
.r2 .im{position:relative;overflow:hidden;border-radius:24px;corner-shape:squircle}.r2 .im img{position:absolute;inset:0}
@keyframes r2-un{from{clip-path:inset(0 100% 0 0)}}
@media (prefers-reduced-motion:no-preference){.r2 .im{animation:r2-un 1.3s var(--so) .1s backwards}}
.r2 .tx{display:flex;flex-direction:column;justify-content:center;padding:40px 72px 72px}
.r2 .soon{align-self:flex-start;margin-bottom:24px;background:#E9DCCA;color:#9C472C}
.r2 .lede{margin-top:24px;max-width:30ch;color:#4A382C}
.r2 .t2{margin:16px 0 32px;max-width:44ch;font-size:16.5px;line-height:1.6;color:#4A382C}
@media (max-width:980px){.r2{grid-template-columns:1fr;min-height:0;padding:84px 16px 0}.r2 .im{aspect-ratio:4/3}.r2 .tx{padding:36px 20px 64px}}
""", '<section class="gp r2 rt" aria-labelledby="gh-h" ref="{{ secRef }}">'
    f'<div class="im">{gh.pic(RT_PHOTO)}</div><div class="tx"><span class="soon up" style="--d: .3s">{RT_SOON}</span>{h1(RT_TITLE)}'
    f'<p class="lede up" style="--d: .55s">{RT_LEDE}</p><p class="t2 up" style="--d: .7s">{RT_TEXT}</p><div class="up" style="--d: .85s">{signup()}</div></div></section>')

# 3. linear.app waitlists: centred, small and still, the clay rings as the only ornament, no photo.
RINGS = ('<svg class="rings" viewBox="0 0 240 60" aria-hidden="true"><g fill="none" stroke-width="2.2" stroke-linecap="round">'
         '<path d="M4 18q19-12 38 0t38 0 38 0 38 0 38 0 38 0" stroke="#3A2A20"></path><path d="M4 30q19-12 38 0t38 0 38 0 38 0 38 0 38 0" stroke="#B4583A"></path>'
         '<path d="M4 42q19-12 38 0t38 0 38 0 38 0 38 0 38 0" stroke="#3A2A20"></path></g></svg>')
RT["Retreat3Linistit"] = ("Retreaturi 3: liniștit, fără poză", "light", NL_CSS + """
.r3{display:flex;align-items:center;justify-content:center;min-height:900px;padding:150px 24px 96px;box-sizing:border-box;text-align:center;background:radial-gradient(ellipse 70% 60% at 50% 45%,#F7F1E9 0%,#EDE0CD 100%)}
.r3 .in{max-width:640px}
.r3 .rings{display:block;width:180px;margin:0 auto 32px}
.r3 .rings path{stroke-dasharray:300;stroke-dashoffset:0}
@keyframes r3-draw{from{stroke-dashoffset:300}}
@media (prefers-reduced-motion:no-preference){.r3 .rings path{animation:r3-draw 1.8s var(--so) backwards}.r3 .rings path:nth-child(2){animation-delay:.15s}.r3 .rings path:nth-child(3){animation-delay:.3s}}
.r3 .soon{margin-top:20px;box-shadow:inset 0 0 0 1px rgba(156,71,44,.5);color:#9C472C}
.r3 .lede{margin:24px auto 0;max-width:34ch;color:#4A382C}
.r3 .t2{margin:14px auto 36px;max-width:44ch;font-size:16.5px;line-height:1.6;color:var(--ink2)}
.r3 .nl{margin:0 auto;text-align:left}
@media (max-width:980px){.r3{min-height:0;padding:120px 20px 72px}}
""", '<section class="gp r3 rt" aria-labelledby="gh-h" ref="{{ secRef }}"><div class="in">'
    f'{RINGS}{h1(RT_TITLE)}<span class="soon up" style="--d: .45s">{RT_SOON}</span><p class="lede up" style="--d: .55s">{RT_LEDE}</p>'
    f'<p class="t2 up" style="--d: .7s">{RT_TEXT}</p><div class="up" style="--d: .85s">{signup()}</div></div></section>')

# 4. Paperless Post: a postcard from the woods; the photo on the front, the words and the form where the address goes.
RT["Retreat4Vedere"] = ("Retreaturi 4: carte poștală", "light", NL_CSS + """
.r4{padding:150px 0 112px;background:linear-gradient(180deg,#F4EDE4 0%,#E6D5BD 100%)}
.r4 .card{position:relative;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);max-width:1100px;margin:0 auto;padding:20px;border-radius:10px;background:#FBF7F1;box-shadow:0 2px 0 rgba(58,42,32,.05),0 40px 70px -40px rgba(70,35,15,.55);rotate:-1deg}
@keyframes r4-in{from{opacity:0;rotate:-5deg;translate:0 40px}}
@media (prefers-reduced-motion:no-preference){.r4 .card{animation:r4-in 1.2s var(--so) .2s backwards}}
.r4 .im{position:relative;min-height:540px;border-radius:4px;overflow:hidden}.r4 .im img{position:absolute;inset:0}
.r4 .tx{position:relative;padding:28px 24px 12px 44px;margin-left:24px;border-left:1px solid rgba(58,42,32,.2)}
.r4 .stamp{position:absolute;right:12px;top:8px;display:grid;place-items:center;width:96px;height:112px;background:#B4583A;color:#F4EDE4;font:400 italic 19px/1.1 var(--display);font-variation-settings:'opsz' 20;text-align:center;
  -webkit-mask:radial-gradient(circle 5px at 50% 0,transparent 98%,#000) 0 -2px/12px 100% repeat-x,radial-gradient(circle 5px at 0 50%,transparent 98%,#000) -2px 0/100% 12px repeat-y;rotate:4deg}
.r4 .gh{font-size:clamp(48px,5vw,72px);margin-top:84px}
.r4 .lede{margin-top:18px;max-width:28ch;color:#4A382C}
.r4 .t2{margin:14px 0 24px;font-size:16px;line-height:1.6;color:#4A382C;max-width:40ch}
.r4 .nl input[type=email]{border:0;border-bottom:1px solid rgba(58,42,32,.4);border-radius:0;background:transparent;padding-left:0}
@media (max-width:980px){.r4{padding:110px 0 64px}.r4 .card{grid-template-columns:1fr;padding:12px;rotate:0deg;margin:0 4px}.r4 .im{min-height:0;aspect-ratio:4/3}
  .r4 .tx{margin:16px 0 0;padding:20px 8px 8px;border-left:0;border-top:1px solid rgba(58,42,32,.2)}.r4 .stamp{width:76px;height:88px;font-size:16px}.r4 .gh{margin-top:72px}}
""", '<section class="gp r4 rt" aria-labelledby="gh-h" ref="{{ secRef }}"><div class="wrap"><div class="card">'
    f'<div class="im">{gh.pic(RT_PHOTO)}</div><div class="tx"><span class="stamp" aria-hidden="true">{RT_SOON}</span>{h1(RT_TITLE)}'
    f'<p class="lede up" style="--d: .55s">{RT_LEDE}</p><p class="t2 up" style="--d: .7s"><b>{RT_SOON}.</b> {RT_TEXT}</p><div class="up" style="--d: .85s">{signup()}</div></div></div></div></section>')

# =================== Evenimente: „În curând” (Vali, 12 nov) ===================
# Evenimente is not the workshops: it lists events Alessia prepares; none is set yet, so it shows „În curând”,
# with the same four layouts as Retreaturi (one choice can serve both pages).
EV_TITLE = "Evenimente"
EV_LEDE = "Evenimente pe care le pregătesc pentru voi, dincolo de atelierele lunare."            # MINE
EV_TEXT = "Fii primul care află de următorul nostru eveniment și primește 5% discount la următorul eveniment."   # doc, Evenimente
EV_BTN = "Abonează-te"                                                                           # the newsletter's button
EV_PHOTO = (BG, "Lut sculptat în valuri, în nuanțe de teracotă", "50% 50%")
EV = {}
for k, (t, tone, css, html) in RT.items():
    h = (html.replace(h1(RT_TITLE), h1(EV_TITLE)).replace(RT_LEDE, EV_LEDE).replace(RT_TEXT, EV_TEXT)
         .replace(f">{RT_BTN}<", f">{EV_BTN}<").replace(gh.pic(RT_PHOTO), gh.pic(EV_PHOTO)))
    assert EV_TEXT in h and EV_BTN in h
    EV[k.replace("Retreat", "Evenimente")] = (t.replace("Retreaturi", "Evenimente"), tone, css, h)

SOURCES = {
    "PrivHero": "șablonul paginilor de serviciu: deschiderea aleasă pe Ateliere de grup (aman.com)",
    "PrivAteliere1Comparat": "apple.com/iphone/compare: cele două una lângă alta, cu aceleași rânduri aliniate",
    "PrivAteliere2Comutator": "apple.com/shop/buy: un comutator alege atelierul, iar prețul și butonul stau într-un card",
    "PrivAteliere3Alternat": "Monocle: articole lungi, cu poza o dată în stânga, o dată în dreapta",
    "PrivAteliere4Acordeon": "acordeonul de poze ales pe Acasă, la „Ce oferim”: două rânduri mari, unul deschis",
    "PrivDetalii": "șablonul paginilor de serviciu: „Cum funcționează” de pe Ateliere de grup",
    "PrivFaq": "șablonul paginilor de serviciu: FAQ 3, carduri (ales pe Acasă)",
    "ScoliHero": "șablonul paginilor de serviciu: deschiderea aleasă pe Ateliere de grup (aman.com)",
    "ScoliDetalii": "șablonul paginilor de serviciu: „Cum funcționează” de pe Ateliere de grup",
    "ScoliFaq": "șablonul paginilor de serviciu: FAQ 3, carduri (ales pe Acasă)",
    "Retreat1Ecran": "șablonul (aman.com): fotografia pe tot ecranul, cu formularul de abonare în ea",
    "Retreat2Jumatate": "squarespace.com, paginile „coming soon”: poza pe o jumătate, textul și formularul pe cealaltă",
    "Retreat3Linistit": "linear.app, listele de așteptare: centrat, mic, liniștit; singurul ornament sunt inelele de lut",
    "Retreat4Vedere": "paperlesspost.com: o carte poștală din pădure, cu timbrul „În curând”",
}

SOURCES.update({k.replace("Retreat", "Evenimente"): v + " (aceeași ca la Retreaturi)" for k, v in list(SOURCES.items()) if k.startswith("Retreat")})

TAB = """
    tab: function (e) { var b = e.currentTarget, s = self.sec, g = b.getAttribute('data-g'), k = b.getAttribute('data-k');
      s.querySelectorAll('[role=tab][data-g="' + g + '"]').forEach(function (x) { x.setAttribute('aria-selected', x === b ? 'true' : 'false'); });
      s.querySelectorAll('[data-p][data-g="' + g + '"]').forEach(function (p) { p.classList.toggle('on', p.getAttribute('data-p') === k); }); },
    noop: function (e) { e.preventDefault(); },"""


def script():
    return ("class Component extends DCLogic {\n  componentDidMount() {" + ENTER + "\n  }\n"
            "  componentWillUnmount() { if (this.io) this.io.disconnect(); }\n"
            "  renderVals() { var self = this; if (!this.cb) this.cb = {" + TAB + " secRef: function (el) { self.sec = el; } }; return this.cb; }\n}")


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


TODO_CSS = ".gd .todo{display:inline-block;padding:0 6px;border:1px dashed rgba(156,71,44,.55);border-radius:6px;color:var(--terra-d);font-size:.92em}"
HEROES = {  # name: (title, html, tone, extra css)
    "PrivHero": ("Atelier privat 1:1: deschiderea", hero(PRIV_TITLE, PRIV_LEDE, PRIV_PILLS, PRIV_CTA, "#ateliere", ph("privat")), "dark", ""),
    "ScoliHero": ("Pentru școli și copii: deschiderea", hero(SC_TITLE, SC_LEDE, SC_PILLS, "Scrie-ne", "#contact", ph("copii")), "dark", ""),
}
HEROES.update({k: (t, html, tone, css) for k, (t, tone, css, html) in RT.items()})
HEROES.update({k: (t, html, tone, css) for k, (t, tone, css, html) in EV.items()})
SECTIONS = {k: (t, co.SEC + css, html) for k, (t, css, html) in PA.items()}
SECTIONS.update({
    "PrivDetalii": ("Atelier privat: cum funcționează + cadou", gp.DET_CSS + TODO_CSS, PRIV_DET),
    "PrivFaq": ("Atelier privat: întrebări frecvente", gp.FAQ_CSS, faq(PRIV_QA, "privat")),
    "ScoliDetalii": ("Pentru școli și copii: cum funcționează", gp.DET_CSS, SC_DET),
    "ScoliFaq": ("Pentru școli și copii: întrebări frecvente", gp.FAQ_CSS, faq(SC_QA, "scoli")),
})
H = {"PrivHero": (905, 789), "ScoliHero": (905, 789), "Retreat1Ecran": (900, 933), "Retreat2Jumatate": (900, 1015), "Retreat3Linistit": (900, 830),
     "Retreat4Vedere": (870, 1035), "Evenimente1Ecran": (900, 933), "Evenimente2Jumatate": (900, 1015), "Evenimente3Linistit": (900, 830), "Evenimente4Vedere": (870, 1035), "PrivAteliere1Comparat": (1662, 2736), "PrivAteliere2Comutator": (922, 1236), "PrivAteliere3Alternat": (2058, 2781),
     "PrivAteliere4Acordeon": (933, 1160), "PrivDetalii": (807, 1011), "PrivFaq": (1038, 1286), "ScoliDetalii": (807, 1039), "ScoliFaq": (726, 888)}

if __name__ == "__main__":
    hero_css = gh.OPTS["GrupHero2Aman"][2]
    gh.SOURCES.update(SOURCES)
    for name, (title, html, tone, css) in HEROES.items():
        for suffix, w, h in (("", 1440, H[name][0]), ("Mobil", 390, H[name][1])):
            f = os.path.join(P, f"{name}{suffix}.dc.html")
            doc = gh.page(name, title + (" · mobil" if suffix else ""), tone, hero_css + css, html, w, h)
            doc = doc.replace("secRef: function", "noop: function (e) { e.preventDefault(); }, secRef: function", 1)
            if name.startswith("Evenimente"):   # the menu marks Evenimente, not Ce oferim
                doc = doc.replace('<a href="#ce-facem" aria-haspopup="true" aria-current="page">', '<a href="#ce-facem" aria-haspopup="true">')
                doc = doc.replace('<a href="#evenimente">', '<a href="#evenimente" aria-current="page">')
            open(f, "w", encoding="utf-8").write(doc)
            if not suffix:
                subprocess.run([sys.executable, os.path.join(HERE, "dc2html.py"), f, os.path.join(HERE, f"opt-{name}.html")], check=True, capture_output=True)
    for name, (title, css, html) in SECTIONS.items():
        for suffix, w, h in (("", 1440, H[name][0]), ("Mobil", 390, H[name][1])):
            f = os.path.join(P, f"{name}{suffix}.dc.html")
            open(f, "w", encoding="utf-8").write(page(name, title + (" · mobil" if suffix else ""), css, html, w, h))
            if not suffix:
                subprocess.run([sys.executable, os.path.join(HERE, "dc2html.py"), f, os.path.join(HERE, f"opt-{name}.html")], check=True, capture_output=True)
    print("wrote", list(HEROES) + list(SECTIONS))
