"""The small pages after an action (Vali, 12 nov). Only three are needed:
  after paying for a workshop   Stripe sends people back here (the Payment Link's „after payment” redirect,
                                /ro/multumim?atelier=<slug>, so the page knows which workshop): four variants.
  after booking a session       Cal.com's „redirect on booking” lands here: in the ticket layout (2, chosen 13 nov).
  404                           a wrong address: in the ticket layout too.
The contact / offer forms and the newsletter thank people in place, so they need no page.
No exact address on these pages (CLAUDE.md: it goes in the confirmation email). All copy is MINE, to approve, except the
24h rule (doc) and „Vino doar cu curiozitate” (Ateliere de grup FAQ). The sample workshop is 6 decembrie.

usage: python3 .aidesigner/confirmari_options.py
"""
import os, subprocess, sys
from about_options2 import P, HERE, ARROW, DUO
import grup_hero_options as gh
from cf_pagina_options import ENTER

E = gh.EVENTS[1]   # sample: 6 decembrie
TITLE = "Mulțumim! Locul tău e confirmat."
LEAD = "Ți-am trimis pe email confirmarea plății și toate detaliile atelierului, inclusiv adresa exactă."
NEXT = [("Verifică emailul", "Dacă nu-l găsești, uită-te și în Spam sau Promoții."),
        ("Vino așa cum ești", "Cu haine comode, pe care nu te deranjează să le murdărești cu lut. Vino doar cu curiozitate, de restul ne ocupăm noi."),
        ("Dacă nu mai poți ajunge", "Anunță-ne cu cel puțin 24 de ore înainte și îți păstrăm locul la următorul atelier.")]
CAL = "Adaugă în calendar"
HOME = f'<a class="more" href="#acasa">Înapoi la pagina principală {ARROW}</a>'
IG = f'<a class="more" href="https://www.instagram.com/ava.art.soul/">Urmărește-ne pe Instagram {ARROW}</a>'
CAL_ICO = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="4" y="5.5" width="16" height="14" rx="2.5"></rect><path d="M4 10h16M8.5 3.5v4M15.5 3.5v4M12 13v4M10 15h4"></path></svg>'
CHECK = '<svg class="ck" viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="32" r="28"></circle><path d="M20 33l8 8 16-17"></path></svg>'
WHEN = f'{E["wd"]}, {E["day"]} {E["mon"]} · {E["time"]}'
WHERE = "Adresa exactă e în email"


def ph(v):
    import re
    return re.sub(r"\[([^\]]+)\]", r'<span class="todo">[\1]</span>', v)


def steps(cls="nx"):
    return f'<ol class="{cls}">' + "".join(f"<li><b>{a}</b><span>{b}</span></li>" for a, b in NEXT) + "</ol>"


def cal_btn(cls="btn"):
    return f'<a class="{cls} cal" href="#adauga-in-calendar">{CAL_ICO}{CAL}</a>'   # in code: an .ics built from content/evenimente.ts


COMMON = """
.cf2{position:relative;background:linear-gradient(180deg,#F4EDE4 0%,#EDE0CD 100%);padding:150px 0 120px;--so:cubic-bezier(.22,1,.36,1)}
.cf2 a{text-decoration:none}
.cf2 h1{font-size:clamp(40px,4.6vw,64px);line-height:1.05}
.cf2 .lead{margin:20px 0 0;max-width:40ch;font:400 clamp(20px,1.7vw,24px)/1.45 var(--display);font-variation-settings:'opsz' 20;color:#4A382C;text-wrap:pretty}
.cf2 .todo{display:inline-block;padding:0 6px;border:1px dashed rgba(156,71,44,.55);border-radius:6px;color:var(--terra-d);font-size:.92em}
.cf2 .btn{display:inline-flex;align-items:center;justify-content:center;gap:10px;min-height:52px;padding:0 26px;border-radius:999px;background:#9C472C;color:#F8F1E8;font:500 15px/1 var(--text);letter-spacing:.02em;transition:background-color .25s}
.cf2 .btn:hover{background:#833A22}.cf2 .btn:focus-visible{outline:2px solid #9C472C;outline-offset:3px}
.cf2 .btn svg{width:18px;height:18px;fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}
.cf2 .nx{margin:0;padding:0;list-style:none;counter-reset:n}
.cf2 .nx li{position:relative;padding:14px 0 14px 50px;border-top:1px solid rgba(58,42,32,.14);counter-increment:n}
.cf2 .nx li::before{content:counter(n);position:absolute;left:0;top:13px;display:grid;place-items:center;width:32px;height:32px;border-radius:50%;box-shadow:inset 0 0 0 1px rgba(156,71,44,.5);color:var(--terra-d);font:400 italic 17px/1 var(--display)}
.cf2 .nx b{display:block;font:400 21px/1.3 var(--display);font-variation-settings:'opsz' 20;font-weight:400}
.cf2 .nx span{display:block;margin-top:2px;font-size:16px;line-height:1.55;color:#4A382C}
.cf2 .links{display:flex;flex-wrap:wrap;gap:4px 28px;margin-top:20px}
.cf2 .ck{width:76px;height:76px;fill:none;stroke:#6F7B5C;stroke-width:2.4;stroke-linecap:round;stroke-linejoin:round}
.cf2 .ck circle{stroke-dasharray:180;stroke-dashoffset:0}.cf2 .ck path{stroke-dasharray:40;stroke-dashoffset:0}
@keyframes cf2-draw{from{stroke-dashoffset:180}}@keyframes cf2-tick{from{stroke-dashoffset:40}}
@media (prefers-reduced-motion:no-preference){.cf2 .ck circle{animation:cf2-draw .9s var(--so) .2s backwards}.cf2 .ck path{animation:cf2-tick .5s var(--so) .9s backwards}}
@media (max-width:980px){.cf2{padding:112px 0 72px}.cf2 .btn{width:100%;box-sizing:border-box}.cf2 .links{flex-direction:column}}
@media (prefers-reduced-motion:reduce){.cf2 *{animation:none!important;transition:none!important}}
"""

OPTS = {}
# 1. Stripe Checkout's success page: a quiet tick that draws itself, the sentence, then what happens next. Centred.
V1_CSS = """
.c1c .in{max-width:680px;margin:0 auto;text-align:center}
.c1c .lead{margin-left:auto;margin-right:auto}
.c1c .ck{display:block;margin:0 auto 28px}
.c1c .card{margin:40px 0 0;padding:8px 28px 18px;border-radius:22px;corner-shape:squircle;background:#FBF7F1;box-shadow:0 0 0 1px rgba(58,42,32,.06);text-align:left}
.c1c .card .nx li:first-child{border-top:0}
.c1c .act{display:flex;flex-direction:column;align-items:center;gap:8px;margin-top:32px}
@media (max-width:980px){.c1c .card{padding:4px 18px 12px}.c1c .act{align-items:stretch;text-align:center}.c1c .act .more{justify-content:center}}
"""


def v1(title, lead, body, act):
    return (f'<section class="gp cf2 c1c" aria-labelledby="gh-h" ref="{{{{ secRef }}}}"><div class="wrap"><div class="in">{CHECK}'
            f'<h1 class="disp" id="gh-h">{title}</h1><p class="lead up" style="--d: .3s">{lead}</p>{body}<div class="act up" style="--d: .6s">{act}</div></div></div></section>')


OPTS["Confirmare1Bifa"] = ("După plată 1: o bifă și pașii", V1_CSS, v1(TITLE, LEAD,
    f'<div class="card up" style="--d: .45s"><p class="sr" style="margin:16px 0 0;font:400 italic 19px/1.3 var(--display);color:var(--terra-d)">{E["title"]} · {ph(WHEN)}</p>{steps()}</div>',
    cal_btn() + HOME))

# 2. dice.fm, the ticket after you buy: the same ticket as on Ateliere de grup, now stamped „Confirmat”.
# Vali (13 nov): this one; the booking page and the 404 use the same layout (v2 below).
C2_CSS = """
.c2c .stage{display:grid;grid-template-columns:minmax(0,6fr) minmax(0,5fr);gap:72px;align-items:center}
.c2c .tk{position:relative;display:grid;grid-template-columns:150px minmax(0,1fr);border-radius:20px;corner-shape:squircle;background:#FBF7F1;box-shadow:0 0 0 1px rgba(58,42,32,.06),0 40px 70px -46px rgba(70,35,15,.6);rotate:-1.5deg}
@keyframes c2-in{from{opacity:0;rotate:-6deg;translate:0 40px}}
@media (prefers-reduced-motion:no-preference){.c2c .tk{animation:c2-in 1s var(--so) .2s backwards}}
.c2c .stub{position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;padding:28px 10px;border-right:2px dotted rgba(58,42,32,.22);text-align:center}
.c2c .stub::before,.c2c .stub::after{content:"";position:absolute;right:-13px;width:24px;height:24px;border-radius:50%;background:#F0E5D7}
.c2c .stub::before{top:-12px}.c2c .stub::after{bottom:-12px}
.c2c .stub small{font-size:13px;color:var(--ink2)}
.c2c .stub b{font:400 56px/1 var(--display);font-variation-settings:'opsz' 72}
.c2c .stub i{font:400 italic 18px/1 var(--display);color:var(--terra-d)}
.c2c .bd{padding:28px 30px}
.c2c .bd h2{margin:0;font:400 26px/1.15 var(--display);font-variation-settings:'opsz' 20}
.c2c .bd p{margin:8px 0 0;font-size:15px;color:var(--ink2)}
.c2c .bd .who{margin-top:18px;padding-top:14px;border-top:1px solid rgba(58,42,32,.1);font-size:14px}
.c2c .stamp{position:absolute;right:22px;bottom:-26px;display:grid;place-items:center;width:110px;height:110px;border-radius:50%;color:#4F5A43;background:rgba(251,247,241,.9);
  box-shadow:inset 0 0 0 2px rgba(79,90,67,.85),inset 0 0 0 6px #FBF7F1,inset 0 0 0 7px rgba(79,90,67,.6);font:400 italic 21px/1 var(--display);rotate:-12deg}
@keyframes c2-press{0%{opacity:0;scale:1.6}60%{opacity:1;scale:.94}100%{scale:1}}
@media (prefers-reduced-motion:no-preference){.c2c .stamp{animation:c2-press .6s cubic-bezier(.3,1.32,.5,1) 1s backwards}}
.c2c .act{display:flex;flex-wrap:wrap;align-items:center;gap:12px 28px;margin-top:28px}
.c2c .nx{margin-top:32px}
@media (max-width:980px){.c2c .stage{grid-template-columns:1fr;gap:48px}.c2c .tk{grid-template-columns:96px minmax(0,1fr);rotate:0deg}.c2c .stub b{font-size:40px}.c2c .bd{padding:20px 18px}.c2c .bd h2{font-size:21px}
  .c2c .stamp{width:84px;height:84px;font-size:16px;right:12px;bottom:-30px}.c2c .act{flex-direction:column;align-items:stretch;text-align:center}}
.c2c .stamp.red{color:#9C472C;box-shadow:inset 0 0 0 2px rgba(156,71,44,.85),inset 0 0 0 6px #FBF7F1,inset 0 0 0 7px rgba(156,71,44,.6)}
.c2c .stub b.sm{font-size:44px}@media (max-width:980px){.c2c .stub b.sm{font-size:28px}}
.c2c .go{display:flex;flex-wrap:wrap;gap:8px;margin:32px 0 0;padding:0;list-style:none}
.c2c .go a{display:inline-flex;align-items:center;min-height:44px;padding:0 18px;border-radius:999px;background:#E9DCCA;font-size:15px;font-weight:500;color:#3A2A20;transition:background-color .2s}
.c2c .go a:hover{background:#E0D0BB}
"""


def v2(title, lead, left, stub, h2, line, who, stamp, act, red=False):
    return (f'<section class="gp cf2 c2c" aria-labelledby="gh-h" ref="{{{{ secRef }}}}"><div class="wrap stage"><div>'
            f'<h1 class="disp" id="gh-h">{title}</h1><p class="lead up" style="--d: .3s">{lead}</p><div class="up" style="--d: .5s">{left}</div></div>'
            f'<div><div class="tk"><p class="stub" style="margin:0"><small>{stub[0]}</small><b{" class=" + chr(34) + "sm" + chr(34) if len(stub[1]) > 2 else ""}>{stub[1]}</b><i>{stub[2]}</i></p>'
            f'<div class="bd"><h2>{h2}</h2><p>{line}</p><p class="who">{who}</p></div>'
            f'<span class="stamp{" red" if red else ""}" aria-label="{stamp}">{stamp}</span></div><div class="act up" style="--d: .8s">{act}</div></div></div></section>')


OPTS["Confirmare2Bilet"] = ("După plată 2: biletul tău", C2_CSS, v2(TITLE, LEAD, steps(), (E["wd"], E["day"], E["mon"]), E["title"],
    f'{ph(E["time"])} · {WHERE}', f'1 loc · {E["price"]} · plătit', "Confirmat", cal_btn() + HOME))

# 3. Airbnb's booking confirmation: a photo of the place beside the words, the details in a short list.
OPTS["Confirmare3Poza"] = ("După plată 3: cu poză", """
.c3c .stage{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,6fr);gap:64px;align-items:start}
.c3c .ph{position:sticky;top:110px;aspect-ratio:4/5;border-radius:24px;corner-shape:squircle;overflow:hidden}
.c3c .ph img{display:block;width:100%;height:100%;object-fit:cover}
@keyframes c3-un{from{clip-path:inset(100% 0 0 0 round 24px)}}
@media (prefers-reduced-motion:no-preference){.c3c .ph{animation:c3-un 1.2s var(--so) .1s backwards}}
.c3c .ph .tag{position:absolute;left:16px;bottom:16px;display:inline-flex;align-items:center;gap:8px;min-height:36px;padding:0 14px;border-radius:999px;background:rgba(251,247,241,.94);font-size:14px;font-weight:500}
.c3c .ph .tag svg{width:16px;height:16px;fill:none;stroke:#4F5A43;stroke-width:2.4;stroke-linecap:round;stroke-linejoin:round}
.c3c dl{display:grid;grid-template-columns:auto minmax(0,1fr);gap:10px 24px;margin:32px 0;padding:22px 0;border-top:1px solid rgba(58,42,32,.16);border-bottom:1px solid rgba(58,42,32,.16)}
.c3c dt{font:400 italic 18px/1.4 var(--display);color:var(--terra-d)}
.c3c dd{margin:0;font-size:16px;line-height:1.55;color:#3F2F25}
.c3c .act{display:flex;flex-wrap:wrap;align-items:center;gap:12px 28px;margin-top:28px}
@media (max-width:980px){.c3c .stage{grid-template-columns:1fr;gap:28px}.c3c .ph{position:relative;top:auto;aspect-ratio:4/3}.c3c .act{flex-direction:column;align-items:stretch;text-align:center}}
""", f'<section class="gp cf2 c3c" aria-labelledby="gh-h" ref="{{{{ secRef }}}}"><div class="wrap stage">'
    f'<div class="ph">{gh.pic(gh.ROOM)}<span class="tag"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8.5l3 3 7-7"></path></svg>Plata e confirmată</span></div><div>'
    f'<h1 class="disp" id="gh-h">{TITLE}</h1><p class="lead up" style="--d: .3s">{LEAD}</p>'
    f'<dl class="up" style="--d: .45s"><dt>Atelier</dt><dd>{E["title"]}</dd><dt>Când</dt><dd>{ph(WHEN)}</dd><dt>Unde</dt><dd>{WHERE}</dd><dt>Plătit</dt><dd>{E["price"]}</dd></dl>'
    f'<div class="up" style="--d: .55s">{steps()}</div><div class="act up" style="--d: .7s">{cal_btn()}{IG}</div></div></div></section>')

# 4. The handwritten thank-you note Etsy makers slip into a parcel: a few words from Alessia, with her photo.
OPTS["Confirmare4Bilet"] = ("După plată 4: un bilețel de la Alessia", """
.c4c .stage{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,6fr);gap:72px;align-items:center}
.c4c .note{position:relative;padding:44px 44px 36px;background:#FFFCF6;border-radius:6px;box-shadow:0 2px 0 rgba(58,42,32,.04),0 40px 70px -40px rgba(70,35,15,.5);rotate:1.2deg}
@keyframes c4-in{from{opacity:0;rotate:-4deg;translate:0 30px}}
@media (prefers-reduced-motion:no-preference){.c4c .note{animation:c4-in 1.1s var(--so) .2s backwards}}
.c4c .note::before{content:"";position:absolute;left:50%;top:-14px;width:110px;height:28px;margin-left:-55px;background:rgba(230,213,189,.85);rotate:-3deg}
.c4c .note p{margin:0 0 14px;font:400 italic 22px/1.5 var(--display);font-variation-settings:'opsz' 20;color:#3A2A20}
.c4c .sig{display:flex;align-items:center;gap:14px;margin-top:22px}
.c4c .sig span.av{width:56px;height:56px;border-radius:50%;overflow:hidden;background:linear-gradient(180deg,#E6D5BD 0%,#D4B894 100%)}
.c4c .sig img{display:block;width:100%;height:100%;object-fit:cover;object-position:50% 8%}
.c4c .sig b{font:400 34px/1 var(--script);color:#9C472C}
.c4c .act{display:flex;flex-wrap:wrap;align-items:center;gap:12px 28px;margin-top:28px}
.c4c .nx{margin-top:28px}
@media (max-width:980px){.c4c .stage{grid-template-columns:1fr;gap:40px}.c4c .note{padding:30px 22px 24px;rotate:0deg}.c4c .note p{font-size:19px}.c4c .act{flex-direction:column;align-items:stretch;text-align:center}}
""", f'<section class="gp cf2 c4c" aria-labelledby="gh-h" ref="{{{{ secRef }}}}"><div class="wrap stage"><div>'
    f'<h1 class="disp" id="gh-h">{TITLE}</h1><p class="lead up" style="--d: .3s">{LEAD}</p><div class="up" style="--d: .5s">{steps()}</div>'
    f'<div class="act up" style="--d: .7s">{cal_btn()}{HOME}</div></div>'
    f'<div class="note"><p>Mă bucur tare că vii la „{E["title"]}”, pe {E["day"]} {E["mon"]}.</p><p>Pregătesc lutul, culorile și ceva bun de ronțăit. Tu adu doar curiozitatea.</p>'
    f'<div class="sig"><span class="av"><img src="{DUO}" alt=""></span><b>Alessia</b></div></div></div></section>')

# the other two pages, in variant 1's layout until a variant is chosen
BOOK_T = "Programarea e făcută."
BOOK_L = "Ți-am trimis pe email confirmarea și invitația în calendar, cu toate detaliile ședinței."
BOOK_NEXT = [("Verifică emailul", "Dacă e o ședință online, linkul e în invitație."),
             ("Prima discuție e gratuită", "Dacă ai programat discuția de cunoaștere de 15 minute, nu ai nimic de plătit."),
             ("Dacă nu mai poți ajunge", "Anulează sau reprogramează din emailul de confirmare, cu cel puțin 24 de ore înainte.")]
BOOK_DAY = ("luni", "16", "nov")   # the sample: the first free day in the Consiliere calendar
OPTS["ConfirmareProgramare"] = ("După programare (consiliere, atelier privat)", C2_CSS, v2(BOOK_T, BOOK_L,
    '<ol class="nx">' + "".join(f"<li><b>{a}</b><span>{b}</span></li>" for a, b in BOOK_NEXT) + "</ol>", BOOK_DAY,
    "Discuție de cunoaștere", "ora 10:00 · online · 15 minute", "Alessia Văideanu · gratuită", "Programat", HOME))

LOST = '<svg class="ck lost" viewBox="0 0 64 64" aria-hidden="true"><path d="M14 50c-4-6-4-20 4-26 4-3 6-8 6-12h16c0 4 2 9 6 12 8 6 8 20 4 26z"></path><path d="M24 12h16M30 30l-5 8 7 3-4 9"></path></svg>'
GO404 = [("Acasă", "#acasa"), ("Ateliere de grup", "#ateliere-de-grup"), ("Ce oferim", "#ce-facem"), ("Contact", "#contact")]
OPTS["Pagina404"] = ("404: pagina nu există", C2_CSS, v2("Pagina asta s-a crăpat la ardere.", "Adresa nu mai există sau s-a schimbat. Te ajutăm să găsești ce cauți:",
    '<ul class="go">' + "".join(f'<li><a href="{h}">{t}</a></li>' for t, h in GO404) + "</ul>", ("eroare", "404", "pagină"),
    "Pagina nu există", "Poate s-a mutat sau linkul s-a scris greșit.", "AVA Art &amp; Soul", "Crăpat", "", red=True))   # MINE

SOURCES = {
    "Confirmare1Bifa": "pagina de succes Stripe Checkout: o bifă care se desenează, fraza, apoi pașii următori",
    "Confirmare2Bilet": "dice.fm, biletul după cumpărare: același bilet ca pe Ateliere de grup, cu ștampila „Confirmat”",
    "Confirmare3Poza": "airbnb.com, confirmarea rezervării: poza locului lângă text, detaliile într-o listă scurtă",
    "Confirmare4Bilet": "bilețelele scrise de mână pe care meșterii de pe Etsy le pun în colet: câteva rânduri de la Alessia",
    "ConfirmareProgramare": "în așezarea biletului (varianta 2, aleasă de Vali pe 13 nov); o deschide Cal.com după programare",
    "Pagina404": "în așezarea biletului (varianta 2), cu ștampila „Crăpat”",
}


def script():
    return ("class Component extends DCLogic {\n  componentDidMount() {" + ENTER + "\n  }\n"
            "  componentWillUnmount() { if (this.io) this.io.disconnect(); }\n"
            "  renderVals() { var self = this; if (!this.cb) this.cb = { secRef: function (el) { self.sec = el; } }; return this.cb; }\n}")


H = {"Confirmare1Bifa": (1132, 1152), "Confirmare2Bilet": (825, 1182), "Confirmare3Poza": (1124, 1434), "Confirmare4Bilet": (946, 1259), "ConfirmareProgramare": (825, 1045), "Pagina404": (720, 726)}

if __name__ == "__main__":
    gh.SOURCES.update(SOURCES)
    gh.script = lambda *a, **k: script()
    for name, (title, css, html) in OPTS.items():
        for suffix, w, h in (("", 1440, H[name][0]), ("Mobil", 390, H[name][1])):
            f = os.path.join(P, f"{name}{suffix}.dc.html")
            doc = gh.page(name, title + (" · mobil" if suffix else ""), "light", COMMON + css, html, w, h)
            doc = doc.replace('<a href="#ce-facem" aria-haspopup="true" aria-current="page">', '<a href="#ce-facem" aria-haspopup="true">')
            open(f, "w", encoding="utf-8").write(doc)
            if not suffix:
                subprocess.run([sys.executable, os.path.join(HERE, "dc2html.py"), f, os.path.join(HERE, f"opt-{name}.html")], check=True, capture_output=True)
        print("wrote", name)
