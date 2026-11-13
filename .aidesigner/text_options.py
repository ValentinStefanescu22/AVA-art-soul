"""The text pages (Vali, 12 nov): one reading template for Înscriere, plată și anulare · Termeni și condiții · Politica de
confidențialitate · Cookies (footer links), and the FAQ page. Four variants each.

Lectura1..4  the reading template, shown with „Înscriere, plată și anulare”: the doc only gives the policy (place
             confirmed after full payment; no refunds; 24h notice keeps a place / reschedules; retreats get their own
             rules; OUG 34/2014 to check with the accountant), so the wording is MINE, to approve, and the legal points
             stay visible placeholders until the accountant / a lawyer checks them. The other legal pages use the same
             template once their text exists (the doc has none yet).
Faq1..4      every question on the site in one page, by category: the general FAQ (doc, „FAQ”) + each service page's.

usage: python3 .aidesigner/text_options.py
"""
import os, subprocess, sys
from about_options2 import P, HERE, ARROW
import grup_hero_options as gh
import grup_page_options as gp
import companii_options as co
import consiliere_options as cs
import servicii_options as sv
from footer_options import PFA
from cf_pagina_options import ENTER

# ---------------- the reading template, with „Înscriere, plată și anulare” ----------------
DOC_T = "Înscriere, plată și anulare"
UPDATED = "Ultima actualizare: [DATA]"
SUMMARY = ["Locul tău e confirmat după plata integrală, în avans.", "Banii nu se returnează.",
           "Dacă ne anunți cu cel puțin 24 de ore înainte, îți păstrăm locul la următorul atelier (la consiliere, reprogramăm ședința)."]   # MINE, from the doc's policy
SECTIONS = [  # (id, title, paragraphs, margin note for variant 3)   MINE, from the doc's policy and CLAUDE.md
    ("inscriere", "Cum te înscrii",
     ["La atelierele de grup te înscrii din pagina atelierului, cu butonul „Mă înscriu”, și plătești online, cu cardul.",
      "Ședințele de consiliere și atelierele private le programezi din calendarul de pe pagina lor. [METODA DE PLATĂ PENTRU CONSILIERE: ONLINE SAU TRANSFER BANCAR]"],
     "Te înscrii de pe pagina atelierului."),
    ("confirmare", "Când e locul tău confirmat",
     ["Locul tău e confirmat doar după plata integrală, în avans. Imediat după plată primești un email cu toate detaliile, inclusiv adresa exactă a atelierului."],
     "După plată, locul e al tău."),
    ("anulare", "Dacă nu mai poți ajunge",
     ["Fiind o afacere la început de drum, fiecare loc ocupat contează. De aceea suma achitată nu se returnează.",
      "Dacă ne anunți cu cel puțin 24 de ore înainte, îți păstrăm un loc la următorul atelier. La consiliere, reprogramăm ședința.",
      "Dacă anunți mai târziu sau nu ajungi, atelierul sau ședința se consideră efectuate."],
     "Anunță-ne cu 24 de ore înainte și nu pierzi nimic."),
    ("retreaturi", "Retreaturi",
     ["Retreaturile au reguli separate (avans, termene de plată, anulare), pe care le publicăm odată cu fiecare retreat."],
     "Reguli separate, la lansare."),
    ("retragere", "Dreptul de retragere",
     ["[DE VERIFICAT CU CONTABILA: excepția de la dreptul de retragere de 14 zile pentru servicii de agrement la o dată anume (OUG 34/2014) și formularea pentru ședințele de consiliere.]"],
     "De completat după verificare."),
    ("contact", "Date de contact",
     [PFA.replace(" · ", "<br>")],
     "Cine suntem."),
]
# Vali (12 nov): the page's text now lives in docs/texte-legale.md; take it from there so the 4 variants stay in sync
import legal_pages as lp
_NOTES = {t: n for _, t, _, n in SECTIONS}
_NOTES["Dacă anulăm noi"] = "Atunci alegi tu."   # MINE
_INS = lp.PAGES[DOC_T]
SUMMARY = _INS["summary"]
SECTIONS = [(k, t, [h], _NOTES.get(t, "")) for k, t, h in _INS["sections"]]
PAGES = [("faq", "Întrebări frecvente"), ("inscrieri", DOC_T), ("termeni", "Termeni și condiții"),
         ("confidentialitate", "Politica de confidențialitate"), ("cookies", "Cookies")]


def ph(t):
    """[PLACEHOLDER] spans keep the dashed look"""
    import re
    return re.sub(r"\[([^\]]+)\]", r'<span class="todo">[\1]</span>', t)


def body(sec, margin=False, num=True):
    out = []
    for i, (k, t, ps, note) in enumerate(sec):
        n = f'<span class="nm">{i + 1:02d}</span>' if num else ""
        txt = "".join(p if p.startswith("<") else f"<p>{ph(p)}</p>" for p in ps)
        out.append(f'<section class="s" id="{k}"><h2>{n}{t}</h2>' + (f'<div class="pair"><div>{txt}</div><aside class="mg">{note}</aside></div>' if margin else txt) + "</section>")
    return "".join(out)


def toc(sec, cls="toc"):
    return f'<nav class="{cls}" aria-label="Cuprins"><p class="tl">Cuprins</p><ol>' + "".join(f'<li><a href="#{k}">{t}</a></li>' for k, t, _, _ in sec) + "</ol></nav>"


TEXT_CSS = """
.tx{position:relative;background:linear-gradient(180deg,#F4EDE4 0%,#EDE0CD 100%);padding:150px 0 120px;--so:cubic-bezier(.22,1,.36,1)}
.tx a{text-decoration:none}
.tx .gh{font-size:clamp(44px,5vw,72px);line-height:1.05}
.tx .upd{margin:14px 0 0;font-size:14px;color:var(--ink2)}
.tx .s{scroll-margin-top:100px}
.tx .s h2{margin:0 0 14px;font:400 28px/1.2 var(--display);font-variation-settings:'opsz' 20;letter-spacing:-.01em;text-wrap:balance}
.tx .s p{margin:0 0 14px;font-size:17px;line-height:1.75;color:#3F2F25;text-wrap:pretty;max-width:66ch}
.tx .nm{display:inline-block;min-width:44px;font:400 15px/1 var(--text);color:var(--terra-d);font-variant-numeric:tabular-nums;vertical-align:5px}
.tx .todo{display:inline;padding:1px 6px;border:1px dashed rgba(156,71,44,.55);border-radius:6px;color:var(--terra-d);font-size:.92em;-webkit-box-decoration-break:clone;box-decoration-break:clone}
.tx .toc .tl{margin:0 0 12px;font:400 italic 19px/1.2 var(--display);font-variation-settings:'opsz' 20;color:var(--terra-d)}
.tx .toc ol{margin:0;padding:0;list-style:none;counter-reset:t}
.tx .toc li{counter-increment:t}
.tx .toc a{display:flex;gap:10px;padding:8px 0;font-size:15px;color:#4A382C;border-bottom:1px solid rgba(58,42,32,.1);transition:color .2s}
.tx .toc a::before{content:counter(t,decimal-leading-zero);color:var(--ink2);font-variant-numeric:tabular-nums}
.tx .toc a:hover,.tx .toc a[aria-current="true"]{color:var(--terra-d)}
.tx .sum{margin:0;padding:24px 26px;border-radius:20px;corner-shape:squircle;background:#FBF7F1;box-shadow:0 0 0 1px rgba(58,42,32,.06)}
.tx .sum p.tl{margin:0 0 10px;font:400 italic 20px/1.2 var(--display);font-variation-settings:'opsz' 20;color:var(--terra-d)}
.tx .sum ul{margin:0;padding:0;list-style:none}
.tx .sum li{position:relative;padding:6px 0 6px 22px;font-size:16px;line-height:1.55;color:#3F2F25}
.tx .sum li::before{content:"";position:absolute;left:2px;top:15px;width:8px;height:8px;border-radius:50%;background:#B4583A}
@media (max-width:980px){.tx{padding:112px 0 72px}.tx .s h2{font-size:23px}.tx .s p{font-size:16px}.tx .nm{min-width:34px}}
"""

LECT = {}
# 1. stripe.com/legal: a sticky table of contents on the left, the numbered text on the right.
LECT["Lectura1Cuprins"] = ("Paginile de text 1: cu cuprins alături", """
.l1 .stage{display:grid;grid-template-columns:260px minmax(0,1fr);gap:80px;align-items:start;margin-top:56px}
.l1 .toc{position:sticky;top:110px}
.l1 .art .s+.s{margin-top:44px;padding-top:36px;border-top:1px solid rgba(58,42,32,.14)}
.l1 .sum{margin-bottom:48px}
@media (max-width:980px){.l1 .stage{grid-template-columns:minmax(0,1fr);gap:28px;margin-top:28px}.l1 .toc{position:static}.l1 .art .s+.s{margin-top:32px;padding-top:28px}}
""", lambda: f'<div class="wrap"><h1 class="disp gh" id="gh-h">{DOC_T}</h1><p class="upd">{ph(UPDATED)}</p><div class="stage">{toc(SECTIONS)}'
    f'<article class="art"><div class="sum"><p class="tl">Pe scurt</p><ul>{"".join(f"<li>{x}</li>" for x in SUMMARY)}</ul></div>{body(SECTIONS)}</article></div></div>')

# 2. basecamp.com/about/policies: one centred column, plain words, the summary first, generous measure.
LECT["Lectura2Coloana"] = ("Paginile de text 2: o singură coloană", """
.l2 .in{max-width:720px;margin:0 auto}
.l2 .head{text-align:center;padding-bottom:40px;border-bottom:1px solid rgba(58,42,32,.16)}
.l2 .sum{margin:40px 0 56px;background:#3A2A20;box-shadow:none}
.l2 .sum p.tl{color:#F2C79C}.l2 .sum li{color:#EFE3D3}.l2 .sum li::before{background:#F2C79C}
.l2 .s+.s{margin-top:48px}
.l2 .s h2{display:flex;align-items:baseline}
@media (max-width:980px){.l2 .head{padding-bottom:28px}.l2 .sum{margin:28px 0 40px;padding:20px}.l2 .s+.s{margin-top:36px}}
""", lambda: f'<div class="wrap"><div class="in"><div class="head"><h1 class="disp gh" id="gh-h">{DOC_T}</h1><p class="upd">{ph(UPDATED)}</p></div>'
    f'<div class="sum"><p class="tl">Pe scurt</p><ul>{"".join(f"<li>{x}</li>" for x in SUMMARY)}</ul></div>{body(SECTIONS)}</div></div>')

# 3. Tumblr's terms of service: the full text, and beside each section a one-line plain summary in the margin.
LECT["Lectura3Margine"] = ("Paginile de text 3: rezumat pe margine", """
.l3 .in{max-width:1080px}
.l3 .lead{margin:20px 0 0;max-width:52ch;font:400 22px/1.45 var(--display);font-variation-settings:'opsz' 20;color:#4A382C}
.l3 .art{margin-top:56px}
.l3 .s{padding:36px 0;border-top:1px solid rgba(58,42,32,.16)}
.l3 .pair{display:grid;grid-template-columns:minmax(0,1fr) 280px;gap:56px}
.l3 .mg{position:relative;align-self:start;padding:14px 16px 14px 18px;border-radius:14px;background:rgba(111,123,92,.12);font:400 italic 18px/1.4 var(--display);font-variation-settings:'opsz' 20;color:#4F5A43}
.l3 .mg::before{content:"Pe scurt";display:block;margin-bottom:4px;font:600 11px/1 var(--text);letter-spacing:.12em;text-transform:uppercase;color:#6F7B5C}
@media (max-width:980px){.l3 .pair{grid-template-columns:1fr;gap:12px}.l3 .mg{order:-1}.l3 .lead{font-size:19px}.l3 .art{margin-top:32px}.l3 .s{padding:28px 0}}
""", lambda: f'<div class="wrap in"><h1 class="disp gh" id="gh-h">{DOC_T}</h1><p class="upd">{ph(UPDATED)}</p>'
    f'<p class="lead">Regulile, scrise clar. Lângă fiecare parte găsești și varianta pe scurt.</p>'   # MINE
    f'<article class="art">{body(SECTIONS, margin=True)}</article></div>')

# 4. apple.com/legal: tabs across all the text pages on top, quiet text, the page you're on underlined.
# Vali (13 nov): this one, without „Pe scurt”; the legal pages use it too (legal_pages.py, through lect4).
def tabs(cur):
    return '<ul class="tabs">' + "".join(f'<li><a href="#{k}"{" aria-current=" + chr(34) + "page" + chr(34) if k == cur else ""}>{t}</a></li>' for k, t in PAGES) + "</ul>"


def tabs_css(root):
    return TABS_CSS.replace(".l4", root)


def lect4(title, upd, sec, cur):
    return ('<div class="wrap">' + tabs(cur)
            + f'<h1 class="disp gh" id="gh-h">{title}</h1><p class="upd">{upd}</p><article class="art">{body(sec, num=False)}</article></div>')


TABS_CSS = """
.l4 .tabs{display:flex;gap:4px;margin:0 0 44px;padding:0;list-style:none;border-bottom:1px solid rgba(58,42,32,.16);overflow-x:auto;scrollbar-width:none}
.l4 .tabs a{display:flex;align-items:center;min-height:48px;padding:0 16px;font-size:14.5px;font-weight:500;color:var(--ink2);white-space:nowrap;box-shadow:inset 0 -2px 0 transparent;transition:color .2s}
.l4 .tabs a:hover{color:var(--ink)}
.l4 .tabs a[aria-current="page"]{color:var(--ink);box-shadow:inset 0 -2px 0 #3A2A20}
@media (max-width:980px){.l4 .tabs{margin:0 -20px 28px;padding:0 20px}}
"""
LECT["Lectura4File"] = ("Paginile de text 4: file între pagini", TABS_CSS + """
.l4 .art{max-width:760px;margin-top:48px}
.l4 .s+.s{margin-top:40px}
@media (max-width:980px){.l4 .art{margin-top:28px}.l4 .s+.s{margin-top:32px}}
""", lambda: lect4(DOC_T, ph(UPDATED), SECTIONS, "inscrieri"))

# ---------------- the FAQ page: every question, by category ----------------
FAQ_GEN = [  # docs/continut-site.md, „FAQ”, word for word (the first one from its note: „Trebuie să știu să lucrez cu lutul? (Nu.)”)
    ("Trebuie să știu să lucrez cu lutul?", "Nu."),
    ("Ce să port? Mă murdăresc?", "Puțin, poate, și face parte din farmec. Stai liniștit(ă), lutul se ia ușor de pe haine și de pe piele cu apă caldă."),
    ("Când și de unde îmi iau piesa?", "Piesele trec prin uscare și ardere, așa că le poți ridica după 4–6 săptămâni, din locul în care s-a ținut atelierul."),
    ("Pot oferi un atelier cadou? Aveți vouchere?", "Da, scrie-mi și pregătim împreună un cadou potrivit, pentru un atelier de grup sau unul privat."),
    ("Care e diferența dintre consiliere și terapie?", "Consilierea în dezvoltare personală e pentru momentele în care vrei să te cunoști mai bine, să iei o decizie sau să-ți găsești direcția. Psihoterapia se adresează suferinței emoționale intense sau de durată, iar ea poate fi oferită doar de un psihoterapeut autorizat. Dacă simt că ai nevoie de altfel de sprijin, îți spun sincer și te ajut să găsești specialistul potrivit."),
    ("Cum mă înscriu și cum plătesc?", "Apeși pe „Mă înscriu” la atelierul care îți place și completezi formularul. Plata se face prin transfer bancar, iar locul tău e confirmat după plata integrală."),
    ("Ce se întâmplă dacă nu mai pot ajunge?", "Dacă mă anunți cu cel puțin 24 de ore înainte, îți păstrez locul la următorul atelier sau reprogramăm ședința. Dacă anunți mai târziu, suma achitată nu se returnează."),
    ("Faceți ateliere private pentru grupuri de prieteni sau aniversări?", "Da, cu drag. Scrie-mi câți sunteți și ce ocazie sărbătoriți, iar eu îți propun un atelier pe măsură."),
]
CATS = [("generale", "Generale", FAQ_GEN), ("grup", "Ateliere de grup", gp.QA), ("companii", "Pentru companii", co.QA),
        ("consiliere", "Consiliere 1:1", cs.QA), ("privat", "Atelier privat 1:1", sv.PRIV_QA), ("scoli", "Școli și copii", sv.SC_QA)]
F_H = "Întrebări frecvente"
F_LEDE = "Tot ce ne întrebați des, într-un singur loc."           # MINE
SEARCH_PH = "Caută o întrebare…"                                  # MINE
NONE = "Nu am găsit nimic. Scrie-ne și îți răspundem în maxim 24 de ore."   # MINE + doc
ICON = '<span class="ic" aria-hidden="true"><svg viewBox="0 0 16 16"><path class="h" d="M3 8H13"></path><path class="v" d="M8 3V13"></path></svg></span>'


def qa_list(items, cat, open_first=False):
    return "".join(f'<details class="q" data-c="{cat}"{" open" if open_first and i == 0 else ""}><summary><span>{q}</span>{ICON}</summary><div class="a"><p>{a}</p></div></details>'
                   for i, (q, a) in enumerate(items))


FAQ_CSS = """
.fz{position:relative;background:linear-gradient(180deg,#F4EDE4 0%,#EDE0CD 100%);padding:150px 0 120px;--so:cubic-bezier(.22,1,.36,1)}
.fz a{text-decoration:none}
.fz .lede{margin:18px 0 0;color:#4A382C}
.fz .q{border-radius:16px;corner-shape:squircle;background:#FBF7F1;box-shadow:0 0 0 1px rgba(58,42,32,.06);transition:box-shadow .3s}
.fz .q+.q{margin-top:8px}
.fz .q[open]{box-shadow:0 0 0 1px rgba(58,42,32,.1),0 18px 36px -28px rgba(58,30,15,.45)}
.fz summary{display:flex;align-items:center;justify-content:space-between;gap:16px;min-height:60px;padding:14px 20px;cursor:pointer;list-style:none;font:400 20px/1.3 var(--display);font-variation-settings:'opsz' 20}
.fz summary::-webkit-details-marker{display:none}
.fz summary:focus-visible{outline:2px solid #9C472C;outline-offset:2px;border-radius:16px}
.fz .ic{flex:none;display:grid;place-items:center;width:32px;height:32px;border-radius:50%;box-shadow:inset 0 0 0 1px rgba(58,42,32,.22)}
.fz .ic svg{width:14px;height:14px;fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round}
.fz .ic .v{transition:opacity .25s}.fz .q[open] .ic .v{opacity:0}
.fz .a{padding:0 20px 18px}.fz .a p{margin:0;max-width:64ch;font-size:16.5px;line-height:1.65;color:#4A382C}
.fz .a a{color:var(--terra-d);text-decoration:underline;text-underline-offset:3px}
@media (prefers-reduced-motion:no-preference){.fz .q[open] .a{animation:fz-in .35s var(--so)}}
@keyframes fz-in{from{opacity:0;translate:0 -4px}}
.fz .cat{scroll-margin-top:100px}
.fz .cat h2{margin:0 0 16px;font:400 30px/1.2 var(--display);font-variation-settings:'opsz' 20}
.fz .cat+.cat{margin-top:52px}
.fz .chips{display:flex;flex-wrap:wrap;gap:8px}
.fz .chip{min-height:44px;padding:0 18px;border:0;border-radius:999px;background:#E9DCCA;font:500 15px/1 var(--text);color:#4A382C;cursor:pointer;white-space:nowrap}
.fz .chip[aria-pressed="true"]{background:#3A2A20;color:#F4EDE4}
.fz .chip:focus-visible{outline:2px solid #9C472C;outline-offset:2px}
.fz .ask{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px 28px;margin-top:56px;padding:28px 32px;border-radius:22px;corner-shape:squircle;background:#3A2A20;color:#F4EDE4}
.fz .ask p{margin:0;font:400 italic 24px/1.3 var(--display);font-variation-settings:'opsz' 20}
.fz .ask small{display:block;margin-top:4px;font:400 15px var(--text);color:#D8C6B2}
.fz .ask a{display:inline-flex;align-items:center;justify-content:center;min-height:52px;padding:0 28px;border-radius:999px;background:#F4EDE4;color:#2E1D14;font:500 15px/1 var(--text)}
.fz .none{display:none;margin:24px 0 0;padding:28px;border:1px dashed rgba(58,42,32,.25);border-radius:18px;text-align:center;color:var(--ink2)}
@media (max-width:980px){.fz{padding:112px 0 72px}.fz summary{font-size:18px;padding:12px 16px}.fz .a{padding:0 16px 16px}.fz .cat h2{font-size:25px}.fz .ask{padding:22px 20px}.fz .ask a{width:100%}
  .fz .chips{flex-wrap:nowrap;overflow-x:auto;margin:0 -20px;padding:0 20px 4px;scrollbar-width:none}}
@media (prefers-reduced-motion:reduce){.fz *{animation:none!important;transition:none!important}}
"""
ASK = f'<div class="ask"><p>Ai altă întrebare?<small>Îți răspundem în maxim 24 de ore.</small></p><a href="#contact">Scrie-ne</a></div>'
HEADF = f'<h1 class="disp gh" id="gh-h">{F_H}</h1><p class="lede up" style="--d: .3s">{F_LEDE}</p>'


def cat_chips():
    return '<div class="chips" role="group" aria-label="Categorii">' + "".join(
        f'<button type="button" class="chip" data-f="{k}" aria-pressed="{"true" if i == 0 else "false"}" onClick="{{{{ filt }}}}">{n}</button>' for i, (k, n, _) in enumerate(CATS)) + "</div>"


FAQ = {}
# 1. Airbnb Help Center: the categories as chips on top, one category's questions at a time.
FAQ["Faq1Categorii"] = ("Întrebări frecvente 1: pe categorii", """
.f1z .in{max-width:880px}
.f1z .chips{margin:36px 0 28px}
.f1z .q{display:none}
""" + "".join(f'.f1z[data-f="{k}"] .q[data-c="{k}"]{{display:block}}' for k, _, _ in CATS), lambda: f'<div class="wrap in">{HEADF}<div class="up" style="--d: .45s">{cat_chips()}</div>'
    + "".join(qa_list(q, k, True) for k, _, q in CATS) + f'{ASK}</div>')

# 2. Stripe docs / Notion help: the categories in a sticky side list, all the questions below each other.
FAQ["Faq2Lista"] = ("Întrebări frecvente 2: toate, cu listă alături", tabs_css(".f2z") + """
.f2z .gh{font-size:clamp(44px,5vw,72px);line-height:1.05}
.f2z .q,.f2z .q[open]{border-radius:0;background:none;box-shadow:none;border-top:1px solid rgba(58,42,32,.14)}
.f2z .q+.q{margin-top:0}.f2z .cat .q:last-child{border-bottom:1px solid rgba(58,42,32,.14)}
.f2z summary{min-height:44px;padding:14px 0;font-size:21px}.f2z summary:focus-visible{border-radius:4px}
.f2z .a{padding:0 0 20px}.f2z .a p{font-size:17px;line-height:1.7;color:#3F2F25}
.f2z .cat h2{margin-bottom:8px}
@media (max-width:980px){.f2z summary{padding:14px 0;font-size:18px}.f2z .a{padding:0 0 16px}}
.f2z .stage{display:grid;grid-template-columns:240px minmax(0,1fr);gap:64px;align-items:start;margin-top:52px}
.f2z .side{position:sticky;top:110px}
.f2z .side ol{margin:0;padding:0;list-style:none}
.f2z .side a{display:flex;justify-content:space-between;gap:10px;padding:10px 0;border-bottom:1px solid rgba(58,42,32,.1);font-size:15px;color:#4A382C}
.f2z .side a small{color:var(--ink2);font-variant-numeric:tabular-nums}
.f2z .side a:hover{color:var(--terra-d)}
@media (max-width:980px){.f2z .stage{grid-template-columns:minmax(0,1fr);gap:24px;margin-top:28px}.f2z .side{position:static}
  .f2z .side ol{display:flex;gap:8px;overflow-x:auto;margin:0 -20px;padding:0 20px 4px;scrollbar-width:none}.f2z .side a{white-space:nowrap;border:0;padding:0 16px;min-height:44px;align-items:center;border-radius:999px;background:#E9DCCA}.f2z .side a small{display:none}}
""", lambda: f'<div class="wrap">{tabs("faq")}{HEADF}<div class="stage"><nav class="side up" style="--d: .45s" aria-label="Categorii"><ol>'
    + "".join(f'<li><a href="#fq-{k}">{n}<small>{len(q)}</small></a></li>' for k, n, q in CATS) + '</ol></nav><div>'
    + "".join(f'<section class="cat" id="fq-{k}"><h2>{n}</h2>{qa_list(q, k)}</section>' for k, n, q in CATS) + f'{ASK}</div></div></div>')

# 3. Intercom Help Center: a big search field first; typing filters every question live, the categories stay as headings.
FAQ["Faq3Cautare"] = ("Întrebări frecvente 3: cu căutare", """
.f3z .in{max-width:880px;margin:0 auto}
.f3z .head{text-align:center}.f3z .lede{margin-left:auto;margin-right:auto}
.f3z .search{position:relative;margin:36px 0 48px}
.f3z .search svg{position:absolute;left:22px;top:50%;width:20px;height:20px;margin-top:-10px;fill:none;stroke:var(--ink2);stroke-width:1.7;stroke-linecap:round}
.f3z .search input{box-sizing:border-box;width:100%;min-height:64px;padding:0 24px 0 56px;border:0;border-radius:999px;background:#FBF7F1;box-shadow:0 0 0 1px rgba(58,42,32,.12),0 24px 48px -36px rgba(70,35,15,.5);font:400 18px var(--text);color:var(--ink)}
.f3z .search input:focus{outline:0;box-shadow:0 0 0 2px #9C472C,0 24px 48px -36px rgba(70,35,15,.5)}
.f3z .q.hide,.f3z .cat.hide{display:none}
.f3z .none.on{display:block}
.f3z mark{background:#F2C79C;color:inherit;border-radius:3px;padding:0 2px}
@media (max-width:980px){.f3z .search{margin:24px 0 36px}.f3z .search input{min-height:56px;font-size:16px}}
""", lambda: f'<div class="wrap in"><div class="head">{HEADF}</div><label class="search up" style="--d: .45s"><span style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)">Caută</span>'
    f'<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"></circle><path d="M16.5 16.5L21 21"></path></svg><input type="search" placeholder="{SEARCH_PH}" onInput="{{{{ find }}}}"></label>'
    + "".join(f'<section class="cat" id="fq-{k}"><h2>{n}</h2>{qa_list(q, k)}</section>' for k, n, q in CATS) + f'<p class="none" role="status">{NONE}</p>{ASK}</div>')

# 4. Shopify Help Center: big category cards first (with a drawing each); picking one opens its questions below.
CAT_ICON = {"generale": '<circle cx="24" cy="24" r="16"></circle><path d="M19 19a5 5 0 1 1 7 4.6c-1.3.6-2 1.4-2 2.9V28M24 33v.5"></path>',
            "grup": '<circle cx="16" cy="18" r="5"></circle><circle cx="32" cy="18" r="5"></circle><path d="M6 38q0-10 10-10t10 10M22 38q0-10 10-10t10 10"></path>',
            "companii": '<rect x="8" y="16" width="32" height="22" rx="3"></rect><path d="M18 16v-4h12v4M8 26h32"></path>',
            "consiliere": '<path d="M6 12h22v14H16l-6 5v-5H6z"></path><path d="M32 20h10v13h-3v4l-5-4h-8v-6"></path>',
            "privat": '<path d="M14 36c-4-4-4-14 2-18 3-2 4-6 4-8h8c0 2 1 6 4 8 6 4 6 14 2 18z"></path><path d="M20 10h8"></path>',
            "scoli": '<path d="M6 18l18-8 18 8-18 8z"></path><path d="M14 22v9c4 4 16 4 20 0v-9"></path>'}
FAQ["Faq4Carduri"] = ("Întrebări frecvente 4: carduri de categorii", """
.f4z .cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin:44px 0 0}
.f4z .cc{display:flex;flex-direction:column;align-items:flex-start;gap:18px;padding:22px;border:0;border-radius:20px;corner-shape:squircle;background:#FBF7F1;box-shadow:0 0 0 1px rgba(58,42,32,.06);text-align:left;font:inherit;color:inherit;cursor:pointer;transition:translate .35s var(--so),box-shadow .3s,background-color .25s}
@media (hover:hover){.f4z .cc:hover{translate:0 -3px;box-shadow:0 0 0 1px rgba(58,42,32,.1),0 20px 36px -26px rgba(58,30,15,.5)}}
.f4z .cc svg{width:36px;height:36px;fill:none;stroke:#B4583A;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.f4z .cc b{display:block;font:400 23px/1.2 var(--display);font-variation-settings:'opsz' 20;font-weight:400}
.f4z .cc small{display:block;margin-top:2px}
.f4z .cc small{font-size:14px;color:var(--ink2)}
.f4z .cc[aria-pressed="true"]{background:#3A2A20;color:#F4EDE4}.f4z .cc[aria-pressed="true"] small{color:#D8C6B2}.f4z .cc[aria-pressed="true"] svg{stroke:#F2C79C}
.f4z .cc:focus-visible{outline:2px solid #9C472C;outline-offset:3px}
.f4z .list{max-width:880px;margin:44px auto 0}
.f4z .list h2{margin:0 0 16px;font:400 30px/1.2 var(--display);font-variation-settings:'opsz' 20}
.f4z .q,.f4z .list h2[data-c]{display:none}
""" + "".join(f'.f4z[data-f="{k}"] .q[data-c="{k}"],.f4z[data-f="{k}"] .list h2[data-c="{k}"]{{display:block}}' for k, _, _ in CATS) + """
@media (max-width:980px){.f4z .cards{grid-template-columns:1fr 1fr;gap:8px;margin-top:28px}.f4z .cc{padding:16px;gap:12px}.f4z .cc b{font-size:18px}.f4z .cc svg{width:30px;height:30px}.f4z .list{margin-top:32px}.f4z .list h2{font-size:25px}}
""", lambda: f'<div class="wrap">{HEADF}<div class="cards">' + "".join(
        f'<button type="button" class="cc chip-like" data-f="{k}" aria-pressed="{"true" if i == 0 else "false"}" onClick="{{{{ filt }}}}"><svg viewBox="0 0 48 48" aria-hidden="true">{CAT_ICON[k]}</svg>'
        f'<span><b>{n}</b><small>{len(q)} întrebări</small></span></button>' for i, (k, n, q) in enumerate(CATS))
    + '</div><div class="list">' + "".join(f'<h2 data-c="{k}">{n}</h2>' for k, n, _ in CATS) + "".join(qa_list(q, k, True) for k, _, q in CATS) + f'{ASK}</div></div>')

SOURCES = {
    "Lectura1Cuprins": "stripe.com/legal: cuprinsul lipit în stânga, textul numerotat în dreapta, „Pe scurt” deasupra",
    "Lectura2Coloana": "basecamp.com/about/policies: o singură coloană centrată, cuvinte simple, rezumatul întâi",
    "Lectura3Margine": "termenii Tumblr: textul întreg și, lângă fiecare parte, varianta pe scurt pe margine",
    "Lectura4File": "apple.com/legal: file între toate paginile de text, sus; textul liniștit, fără „Pe scurt” (Vali, 13 nov)",
    "Faq1Categorii": "airbnb.com/help: categoriile ca pastile sus, câte o categorie pe rând",
    "Faq2Lista": "documentația Stripe / Notion Help: categoriile într-o listă alături, toate întrebările una sub alta; cu filele și titlul paginilor de text (apple.com/legal), ales de Vali pe 13 nov",
    "Faq3Cautare": "intercom.com/help: un câmp mare de căutare care filtrează întrebările pe loc",
    "Faq4Carduri": "help.shopify.com: carduri mari de categorii, cu câte un desen; alegi una și se deschid întrebările ei",
}
HANDLERS = """
    filt: function (e) { var b = e.currentTarget, s = self.sec;
      s.querySelectorAll('[data-f][aria-pressed]').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      s.setAttribute('data-f', b.getAttribute('data-f')); },
    find: function (e) { var s = self.sec, v = e.currentTarget.value.trim().toLowerCase(), any = false;
      var norm = function (t) { return t.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g, ''); }, nv = norm(v);
      s.querySelectorAll('.cat').forEach(function (c) { var hit = false;
        c.querySelectorAll('.q').forEach(function (q) { var ok = !nv || norm(q.textContent).indexOf(nv) >= 0; q.classList.toggle('hide', !ok); if (ok) hit = true; if (nv && ok) q.open = norm(q.querySelector('summary').textContent).indexOf(nv) < 0 ? true : q.open; });
        c.classList.toggle('hide', !hit); if (hit) any = true; });
      s.querySelector('.none').classList.toggle('on', !any); },"""


def script():
    # the tabs scroll sideways on phones: bring the current page's tab into view
    tabs = ("\n    var tb = s.querySelector('.tabs'), cur = tb && tb.querySelector('[aria-current]');"
            "\n    if (cur && tb.scrollWidth > tb.clientWidth) tb.scrollLeft = cur.parentNode.offsetLeft - 20;")
    return ("class Component extends DCLogic {\n  componentDidMount() {" + ENTER + tabs + "\n  }\n"
            "  componentWillUnmount() { if (this.io) this.io.disconnect(); }\n"
            "  renderVals() { var self = this; if (!this.cb) this.cb = {" + HANDLERS + " secRef: function (el) { self.sec = el; } }; return this.cb; }\n}")


ALL = {}
for k, (t, css, fn) in LECT.items():
    ALL[k] = (t, TEXT_CSS + lp.LEGAL_CSS + css, f'<section class="gp tx l{k[7]}" aria-labelledby="gh-h" ref="{{{{ secRef }}}}">{fn()}</section>')
for k, (t, css, fn) in FAQ.items():
    ALL[k] = (t, FAQ_CSS + css, f'<section class="gp fz f{k[3]}z" data-f="generale" aria-labelledby="gh-h" ref="{{{{ secRef }}}}">{fn()}</section>')
H = {"Lectura1Cuprins": (2426, 2878), "Lectura2Coloana": (2337, 2391), "Lectura3Margine": (2322, 2971), "Lectura4File": (2000, 2092), "Faq1Categorii": (1665, 1480), "Faq2Lista": (3650, 3689), "Faq3Cautare": (4455, 4177), "Faq4Carduri": (1854, 1850)}

if __name__ == "__main__":
    gh.SOURCES.update(SOURCES)
    gh.script = lambda *a, **k: script()
    for name, (title, css, html) in ALL.items():
        for suffix, w, h in (("", 1440, H[name][0]), ("Mobil", 390, H[name][1])):
            f = os.path.join(P, f"{name}{suffix}.dc.html")
            doc = gh.page(name, title + (" · mobil" if suffix else ""), "light", css, html, w, h)
            doc = doc.replace('<a href="#ce-facem" aria-haspopup="true" aria-current="page">', '<a href="#ce-facem" aria-haspopup="true">')
            open(f, "w", encoding="utf-8").write(doc)
            if not suffix:
                subprocess.run([sys.executable, os.path.join(HERE, "dc2html.py"), f, os.path.join(HERE, f"opt-{name}.html")], check=True, capture_output=True)
        print("wrote", name)
