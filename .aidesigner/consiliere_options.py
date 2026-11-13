"""Ce oferim › Consiliere 1:1 (Vali, 12 nov), on the service template (the „Ateliere de grup” page):
  ConsHero        the chosen hero (2, Aman), this page's copy. No new variants.
  ConsIntrebari1..4  NEW, four variants: „Te regăsești aici?” (the doc's four questions).
  ConsDetalii     „Cum funcționează” as on Ateliere de grup; the dark card is the free first meeting; then the
                  „Consiliere sau psihoterapie?” delimitation, word for word (CLAUDE.md: it must stay).
  ConsProgramare1..4 NEW, four variants: the booking calendar. All four are layouts Cal.com's free embed can do
                  (month view, week view, column view) or our own two cards in front of it; dates and times are samples.
  ConsFaq         the page's FAQ in the FAQ 3 cards.

usage: python3 .aidesigner/consiliere_options.py
Copy: docs/continut-site.md, „Consiliere 1:1”. Never „psiholog / psihoterapeut / terapie” as a service; the delimitation
text is the doc's. Mine, to approve (MINE below): the pills, „Programează discuția”, the booking's labels („Alege
ședința”, „Continuă”, „Ai ales:”), the type names' short lines.
Photo: the consiliere photo from Ce oferim is provisional (Unsplash).
"""
import datetime as dt, os, subprocess, sys
from about_options2 import P, HERE, FONTS, BASE_CSS, ARROW, DUO
import grup_hero_options as gh
import grup_page_options as gp
import faq_options as fq
import companii_options as co
from ce_facem2_options import IMG
from cf_pagina_options import ENTER

TITLE = "Consiliere 1:1"
LEDE = ("Te susțin în drumul tău și te ghidez spre versiunea ta autentică. Te ajut să explorezi ce te frământă, "
        "să îți atingi obiectivele propuse și să formezi relații sănătoase cu cei din jur.")
PILLS = ["60–90 de minute", "online sau față în față", "180 lei / oră", "prima discuție gratuită"]   # MINE, from the doc
CTA = "Programează o ședință"
PHOTO = (IMG["consiliere"], "Două persoane stau la masă, cu câte o cană în mâini (fotografie provizorie)", "50% 50%")
Q_H = "Te regăsești aici?"
QS = ["Treci printr-o schimbare și nu știi încă ce loc ocupă ea în viața ta?",
      "Simți că ai rămas pe loc, deși îți dorești să mergi mai departe?",
      "Îți dorești să te cunoști mai bine, să înțelegi ce simți și de ce?",
      "Te întrebi încotro vrei să mergi și ce contează cu adevărat pentru tine?"]
HOW = "Tot ce îmi spui rămâne confidențial."
FACTS = [("Durată", "60–90 de minute."), ("Unde", "Online sau față în față, cum îți e mai bine."),
         ("Ritm", "Săptămânal, apoi bilunar sau lunar, în funcție de nevoia ta."), ("Preț", "180 lei / oră.")]
FIRST_H = "Prima întâlnire"
FIRST = "Programează o discuție de cunoaștere de 15 minute, gratuită, online."
FIRST_BTN = "Programează discuția"                                # MINE
DELIM_H = "Consiliere sau psihoterapie?"
DELIM = ("Consilierea în dezvoltare personală nu înlocuiește psihoterapia sau tratamentul medical. "
         "Consilierea în dezvoltare personală se adresează persoanelor fără tulburări psihice.")
QA = [  # Întrebări frecvente (Consiliere 1:1), word for word
    ("Câte ședințe îmi trebuie?", "Depinde de tine și de ce vrei să lucrezi. Sunt oameni care vin pentru câteva întâlniri, alții pentru un proces mai lung. Stabilim împreună după prima ședință și ne adaptăm pe parcurs în funcție de ce ai nevoie."),
    ("Ne vedem online sau față în față?", "Ambele variante, cum îți e mai bine."),
    ("Ce discutăm rămâne între noi?", "Da. Tot ce îmi spui rămâne confidențial."),
    ("Ce se întâmplă dacă am nevoie de psihoterapie?", "Dacă simțim pe parcurs că ai nevoie de alt fel de sprijin, îți spun sincer și te ajut să găsești un specialist potrivit."),
    ("Cum plătesc?", "Prin transfer bancar, la rezervarea locului."),
    ("Ce se întâmplă dacă nu mai pot ajunge?", "Dacă anulezi cu cel puțin 24 de ore înainte, reprogramăm ședința. Dacă anunți mai târziu sau nu ajungi, ședința se consideră efectuată."),
]
# booking
B_H = CTA
B_SUB = "Prima întâlnire: " + FIRST[0].lower() + FIRST[1:]
TYPES = [("free", "Discuție de cunoaștere", "15 minute · online · gratuită"),
         ("full", "Ședință de consiliere", "60–90 de minute · online sau față în față · 180 lei / oră")]
TYPE_H, GO, PICKED = "Alege ședința", "Continuă", "Ai ales:"      # MINE
WD = ["luni", "marți", "miercuri", "joi", "vineri", "sâmbătă", "duminică"]
MO = {11: ("noiembrie", "nov"), 12: ("decembrie", "dec")}
BASE = ["10:00", "11:30", "13:00", "17:00", "18:30"]
DAYS = [d for d in (dt.date(2026, 11, 16) + dt.timedelta(i) for i in range(40)) if d.weekday() < 5][:20]


def slots(d):
    return [t for i, t in enumerate(BASE) if (d.day + i) % 3]


def dlabel(d, short=False):
    return f'{WD[d.weekday()][:2].capitalize() if short else WD[d.weekday()]}, {d.day} {MO[d.month][1]}'


SOURCES = {
    "ConsHero": "șablonul paginilor de serviciu: deschiderea aleasă pe Ateliere de grup (aman.com)",
    "ConsIntrebari1Calm": "calm.com: rânduri mari, centrate, care se aprind pe rând pe măsură ce derulezi",
    "ConsIntrebari2Carduri": "theschooloflife.com: întrebările ca niște cartonașe numerotate, în culori calde",
    "ConsIntrebari3Mesaje": "Mesaje (Apple): Alessia te întreabă, bulă cu bulă, ca într-o conversație",
    "ConsIntrebari4Portret": "Cereal Magazine: portretul lângă o listă liniștită, cu linii subțiri",
    "ConsDetalii": "șablonul paginilor de serviciu: „Cum funcționează” de pe Ateliere de grup",
    "ConsProgramare1Luna": "cal.com, vederea pe lună: detaliile în stânga, calendarul la mijloc, orele în dreapta",
    "ConsProgramare2Saptamana": "Google Calendar, vederea pe săptămână (cal.com o are ca „week view”)",
    "ConsProgramare3Coloane": "doctolib.fr: zilele pe coloane, fiecare cu orele ei (cal.com o are ca „column view”)",
    "ConsProgramare4Alegi": "calendly.com: întâi alegi tipul de ședință din două carduri, apoi ziua și ora",
    "ConsFaq": "șablonul paginilor de serviciu: FAQ 3, carduri (ales pe Acasă)",
}


def h1():
    k, ws = 0, []
    for w in TITLE.split():
        ls = []
        for ch in w:
            ls.append(f'<span class="l" style="--k: {k}">{ch}</span>'); k += 1
        ws.append('<span class="w" aria-hidden="true">' + "".join(ls) + "</span>")
    return f'<h1 class="disp gh" id="gh-h" aria-label="{TITLE}">' + " ".join(ws) + "</h1>"


HERO_HTML = ('<section class="gp g2" aria-labelledby="gh-h" ref="{{ secRef }}">'
             f'<div class="bg">{gh.pic(PHOTO)}</div><div class="in">{h1()}'
             f'<p class="lede up" style="--d: .55s">{LEDE}</p>'
             f'<ul class="pills up" style="--d: .7s">{"".join(f"<li>{m}</li>" for m in PILLS)}</ul>'
             f'<div class="up" style="--d: .85s"><a class="btn" href="#programare">{CTA}</a></div></div></section>')

MORE = f'<a class="more" href="#programare">{CTA} {ARROW}</a>'
OPTS = {}

# 1. Calm: big centred lines that light up one by one as they pass the middle of the screen (scroll-driven, CSS only).
OPTS["ConsIntrebari1Calm"] = ("Consiliere, te regăsești aici? 1: rânduri care se aprind", """
.q1{background:linear-gradient(180deg,#F4EDE4 0%,#EDE0CD 100%);text-align:center}
.q1 h2{margin-bottom:56px}
.q1 ol{max-width:900px;margin:0 auto;padding:0;list-style:none}
.q1 li{margin:0;padding:22px 0;font:400 clamp(28px,3vw,42px)/1.25 var(--display);font-variation-settings:'opsz' 20;letter-spacing:-.01em;text-wrap:balance}
.q1 li+li{border-top:1px solid rgba(58,42,32,.12)}
@supports (animation-timeline: view()){
  @keyframes q1-lit{0%,100%{opacity:.22}35%,65%{opacity:1}}
  @media (prefers-reduced-motion:no-preference){.q1 li{animation:q1-lit linear both;animation-timeline:view();animation-range:cover}}
}
.q1 .more{margin-top:44px}
@media (max-width:980px){.q1 h2{margin-bottom:28px}.q1 li{padding:18px 0;font-size:24px}}
""", '<section class="cs q1" aria-labelledby="cq-h" ref="{{ secRef }}"><div class="wrap">'
    f'<h2 class="disp ri" id="cq-h">{Q_H}</h2><ol>' + "".join(f"<li>{q}</li>" for q in QS) + f'</ol><div class="ri">{MORE}</div></div></section>')

# 2. The School of Life: each question a numbered card, in warm colours of the palette.
CARD_COL = [("#FBF7F1", "#3A2A20"), ("#E9DCC8", "#3A2A20"), ("#4F5A43", "#F4EDE4"), ("#3A2A20", "#F4EDE4")]
OPTS["ConsIntrebari2Carduri"] = ("Consiliere, te regăsești aici? 2: cartonașe", """
.q2{background:linear-gradient(180deg,#F4EDE4 0%,#EDE0CD 100%)}
.q2 .head{display:flex;align-items:end;justify-content:space-between;gap:20px;flex-wrap:wrap;margin-bottom:44px}
.q2 .head .more{margin:0}
.q2 ul{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;margin:0;padding:0;list-style:none}
.q2 li{display:flex;flex-direction:column;justify-content:space-between;gap:40px;min-height:300px;padding:26px 24px;border-radius:22px;corner-shape:squircle;background:var(--bg);color:var(--fg);transition:translate .4s var(--so)}
@media (hover:hover){.q2 li:hover{translate:0 -4px}}
.q2 li span{font:400 italic 20px/1 var(--display);font-variation-settings:'opsz' 20;opacity:.75}
.q2 li p{margin:0;font:400 25px/1.25 var(--display);font-variation-settings:'opsz' 20;text-wrap:pretty}
@media (max-width:980px){
  .q2 .head{margin-bottom:28px}
  .q2 ul{display:flex;gap:10px;margin:0 -20px;padding:0 20px 8px;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none}
  .q2 li{flex:0 0 76%;min-height:260px;scroll-snap-align:start}.q2 li p{font-size:22px}
}
""", '<section class="cs q2" aria-labelledby="cq-h" ref="{{ secRef }}"><div class="wrap">'
    f'<div class="head"><h2 class="disp ri" id="cq-h">{Q_H}</h2><div class="ri" style="--i: 1">{MORE}</div></div><ul>'
    + "".join(f'<li class="ri" style="--i: {i + 1}; --bg: {CARD_COL[i][0]}; --fg: {CARD_COL[i][1]}"><span>0{i + 1}</span><p>{q}</p></li>' for i, q in enumerate(QS))
    + "</ul></div></section>")

# 3. Apple Messages: Alessia asks, bubble by bubble, with a typing pause before each.
OPTS["ConsIntrebari3Mesaje"] = ("Consiliere, te regăsești aici? 3: mesaje", """
.q3{background:linear-gradient(180deg,#F4EDE4 0%,#EDE0CD 100%)}
.q3 .stage{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,6fr);gap:72px;align-items:center}
.q3 .chat{display:flex;flex-direction:column;align-items:flex-start;gap:10px;padding:32px;border-radius:28px;corner-shape:squircle;background:#FBF7F1;box-shadow:0 0 0 1px rgba(58,42,32,.06),0 30px 60px -44px rgba(70,35,15,.5)}
.q3 .who{display:flex;align-items:center;gap:12px;margin-bottom:10px;font-size:14px;color:var(--ink2)}
.q3 .who b{display:block;font-size:15px;color:var(--ink);font-weight:600}
.q3 .av{width:44px;height:44px;border-radius:50%;overflow:hidden;background:linear-gradient(180deg,#E6D5BD 0%,#D4B894 100%)}
.q3 .av img{display:block;width:100%;height:100%;object-fit:cover;object-position:50% 8%}
.q3 .b{max-width:86%;margin:0;padding:13px 18px;border-radius:22px 22px 22px 6px;background:#EFE3D3;font-size:17px;line-height:1.45;color:#3A2A20}
.q3 .dots{display:inline-flex;gap:4px;padding:14px 16px;border-radius:22px 22px 22px 6px;background:#EFE3D3}
.q3 .dots i{width:7px;height:7px;border-radius:50%;background:#9A8676;animation:q3-dot 1s ease-in-out infinite}
.q3 .dots i:nth-child(2){animation-delay:.15s}.q3 .dots i:nth-child(3){animation-delay:.3s}
@keyframes q3-dot{50%{translate:0 -3px;opacity:.5}}
@keyframes q3-pop{from{opacity:0;scale:.92;translate:0 8px}}
@keyframes q3-gone{to{opacity:0;height:0;padding:0;margin:-5px 0}}
.q3.js:not(.in) .b,.q3.js:not(.in) .dots{opacity:0}
.q3.js.in .b{transform-origin:0 100%;animation:q3-pop .45s cubic-bezier(.3,1.32,.5,1) backwards;animation-delay:calc(.4s + var(--n) * 1.1s)}
.q3.js.in .dots{animation:q3-pop .3s ease backwards,q3-gone .2s ease forwards;animation-delay:calc(var(--n) * 1.1s - .3s),calc(.35s + var(--n) * 1.1s)}
.q3 .more{margin-top:28px}
@media (prefers-reduced-motion:reduce){.q3 .dots{display:none}}
@media (max-width:980px){.q3 .stage{grid-template-columns:1fr;gap:28px}.q3 .chat{padding:20px 16px}.q3 .b{max-width:92%;font-size:16px}}
""", '<section class="cs q3" aria-labelledby="cq-h" ref="{{ secRef }}"><div class="wrap stage">'
    f'<div><h2 class="disp ri" id="cq-h">{Q_H}</h2><p class="intro ri" style="--i: 1">{LEDE}</p><div class="ri" style="--i: 2">{MORE}</div></div>'
    f'<div class="chat ri" style="--i: 1"><div class="who"><span class="av"><img src="{DUO}" alt=""></span><span><b>Alessia Văideanu</b>consilier în dezvoltare personală</span></div>'
    + "".join(f'<span class="dots" aria-hidden="true" style="--n: {i}"><i></i><i></i><i></i></span><p class="b" style="--n: {i}">{q}</p>' for i, q in enumerate(QS))
    + "</div></div></section>")

# 4. Cereal: the portrait beside a quiet, numbered hairline list.
OPTS["ConsIntrebari4Portret"] = ("Consiliere, te regăsești aici? 4: portret", """
.q4{background:linear-gradient(180deg,#F4EDE4 0%,#EDE0CD 100%)}
.q4 .stage{display:grid;grid-template-columns:minmax(0,4fr) minmax(0,7fr);gap:80px;align-items:center}
.q4 .fig{margin:0;aspect-ratio:4/5;border-radius:22px;corner-shape:squircle;overflow:hidden;background:linear-gradient(180deg,#E6D5BD 0%,#D4B894 100%)}
.q4 .fig img{display:block;width:100%;height:100%;object-fit:cover;object-position:50% 6%}
@keyframes q4-un{from{clip-path:inset(100% 0 0 0)}}
.q4.js:not(.in) .fig{clip-path:inset(100% 0 0 0)}.q4.js.in .fig{animation:q4-un 1.2s var(--so) backwards}
.q4 ol{margin:40px 0 0;padding:0;list-style:none;counter-reset:q}
.q4 li{display:grid;grid-template-columns:48px minmax(0,1fr);gap:12px;padding:20px 0;border-top:1px solid rgba(58,42,32,.18);counter-increment:q;font:400 23px/1.35 var(--display);font-variation-settings:'opsz' 20;text-wrap:pretty}
.q4 li:last-child{border-bottom:1px solid rgba(58,42,32,.18)}
.q4 li::before{content:"0" counter(q);padding-top:6px;font:400 14px/1 var(--text);color:var(--terra-d);font-variant-numeric:tabular-nums}
.q4 .more{margin-top:28px}
@media (max-width:980px){.q4 .stage{grid-template-columns:1fr;gap:32px}.q4 .fig{width:min(100%,340px)}.q4 ol{margin-top:24px}.q4 li{grid-template-columns:34px minmax(0,1fr);font-size:20px;padding:16px 0}}
""", '<section class="cs q4" aria-labelledby="cq-h" ref="{{ secRef }}"><div class="wrap stage">'
    f'<figure class="fig"><img src="{DUO}" alt="Alessia Văideanu"></figure><div><h2 class="disp ri" id="cq-h">{Q_H}</h2><ol>'
    + "".join(f'<li class="ri" style="--i: {i + 1}">{q}</li>' for i, q in enumerate(QS)) + f'</ol><div class="ri" style="--i: 5">{MORE}</div></div></div></section>')

# ---- details: the template; dark card = the free first meeting; then the delimitation, quiet ----
DET_CSS = gp.DET_CSS + """
.gd .co .btn-c{min-width:0}
.gd .dl2{display:grid;grid-template-columns:minmax(0,4fr) minmax(0,8fr);gap:40px;margin-top:56px;padding:32px 0 0;border-top:1px solid rgba(58,42,32,.22)}
.gd .dl2 h3{margin:0;font:400 italic 26px/1.25 var(--display);font-variation-settings:'opsz' 20;color:var(--terra-d)}
.gd .dl2 p{margin:0;max-width:62ch;font-size:16.5px;line-height:1.65;color:#4A382C;text-wrap:pretty}
@media (max-width:980px){.gd .dl2{grid-template-columns:1fr;gap:10px;margin-top:40px;padding-top:24px}.gd .dl2 h3{font-size:22px}}
"""
DET_HTML = ('<section class="gd" aria-labelledby="gd-h" ref="{{ secRef }}"><div class="wrap">'
            f'<h2 class="disp ri" id="gd-h">Cum funcționează</h2><p class="how ri" style="--i: 1">{HOW}</p><dl>'
            + "".join(f'<div class="ri" style="--i: {i + 2}"><dt>{a}</dt><dd>{b}</dd></div>' for i, (a, b) in enumerate(FACTS))
            + f'</dl><aside class="co ri" style="--i: 2" aria-label="{FIRST_H}"><div><p class="q">{FIRST_H}</p><p>{FIRST}</p></div>'
            f'<a class="btn-c" href="#programare">{FIRST_BTN}</a></aside>'
            f'<div class="dl2 ri" style="--i: 3"><h3>{DELIM_H}</h3><p>{DELIM}</p></div></div></section>')

# ---- booking: shared pieces ----
def types_html(cls="types", big=False):
    return (f'<div class="{cls}" role="group" aria-label="{TYPE_H}">'
            + "".join(f'<button type="button" class="type" data-k="{k}" aria-pressed="{"true" if k == "free" else "false"}" onClick="{{{{ pickType }}}}">'
                      f'<b>{n}</b><span>{d}</span></button>' for k, n, d in TYPES) + "</div>")


def slot_list(d, cls="slots"):
    return (f'<div class="{cls}" data-d="{d.isoformat()}"{"" if d == DAYS[0] else " hidden"}>'
            + "".join(f'<button type="button" class="slot" data-d="{d.isoformat()}" data-l="{dlabel(d)} · {t}" aria-pressed="false" onClick="{{{{ pickSlot }}}}">{t}</button>' for t in slots(d))
            + "</div>")


SUM = (f'<div class="sum"><p aria-live="polite"><span class="pk">{PICKED}</span> <b class="lab">alege o oră</b></p>'
       f'<button type="button" class="btn go" aria-disabled="true" onClick="{{{{ goOn }}}}">{GO}</button></div>')
SAMPLE = '<p class="smp">Zilele și orele de aici sunt exemple; în site vin din calendarul Alessiei.</p>'


def month(y, m):
    import calendar
    avail = {d.day for d in DAYS if d.month == m}
    cells = ["<span></span>"] * calendar.monthrange(y, m)[0]
    for day in range(1, calendar.monthrange(y, m)[1] + 1):
        d = dt.date(y, m, day)
        if day in avail:
            cells.append(f'<button type="button" class="day" data-d="{d.isoformat()}" aria-pressed="{"true" if d == DAYS[0] else "false"}" aria-label="{dlabel(d)}" onClick="{{{{ pickDay }}}}">{day}</button>')
        else:
            cells.append(f'<span class="day">{day}</span>')
    head = "".join(f"<abbr>{w}</abbr>" for w in ["L", "Ma", "Mi", "J", "V", "S", "D"])
    return f'<div class="mon" data-m="{m}"{"" if m == 11 else " hidden"}><div class="grid">{head}{"".join(cells)}</div></div>'


BOOK_CSS = """
.bk .type{display:flex;flex-direction:column;align-items:flex-start;gap:4px;width:100%;padding:14px 16px;border:0;border-radius:14px;background:transparent;box-shadow:inset 0 0 0 1px rgba(58,42,32,.18);text-align:left;font:inherit;color:inherit;cursor:pointer;transition:box-shadow .2s,background-color .2s}
.bk .type b{font:400 20px/1.2 var(--display);font-variation-settings:'opsz' 20}
.bk .type span{font-size:14px;color:var(--ink2)}
.bk .type:hover{background:rgba(251,247,241,.7)}
.bk .type[aria-pressed="true"]{background:#FFFCF7;box-shadow:inset 0 0 0 2px #3A2A20}
.bk .type:focus-visible,.bk .day:focus-visible,.bk .slot:focus-visible,.bk .nav button:focus-visible{outline:2px solid #9C472C;outline-offset:2px}
.bk .slot{display:inline-flex;align-items:center;justify-content:center;min-height:44px;padding:0 14px;border:0;border-radius:12px;background:#FFFCF7;box-shadow:inset 0 0 0 1px rgba(156,71,44,.45);font:500 15px/1 var(--text);color:#9C472C;font-variant-numeric:tabular-nums;cursor:pointer;transition:background-color .2s,color .2s}
.bk .slot:hover{background:#F7E9DE}
.bk .slot[aria-pressed="true"]{background:#9C472C;color:#F8F1E8;box-shadow:none}
.bk [hidden]{display:none!important}
.bk .sum{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px 20px}
.bk .sum p{margin:0;font-size:15px;color:var(--ink2)}
.bk .sum b{font-weight:600;color:var(--ink)}
.bk .go[aria-disabled="true"]{background:#CDBBA6;color:#FBF7F1;cursor:not-allowed}
.bk .smp{margin:16px 0 0;font-size:13px;color:var(--ink2)}
.bk .mon .grid{display:grid;grid-template-columns:repeat(7,1fr);gap:4px;text-align:center}
.bk abbr{padding-bottom:8px;font-size:12px;color:var(--ink2);text-decoration:none}
.bk .day{display:grid;place-items:center;aspect-ratio:1;max-height:56px;border:0;border-radius:50%;background:none;font:400 15px/1 var(--text);color:rgba(58,42,32,.35);font-variant-numeric:tabular-nums}
.bk button.day{cursor:pointer;color:var(--ink);font-weight:600;background:#EFE2D0;transition:background-color .2s,color .2s}
.bk button.day:hover{background:#E6D3BC}
.bk button.day[aria-pressed="true"]{background:#3A2A20;color:#F4EDE4}
.bk .mhead{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px}
.bk .mhead p{margin:0;font:400 22px/1 var(--display);font-variation-settings:'opsz' 20}
.bk .nav{display:flex;gap:6px}
.bk .nav button{display:grid;place-items:center;width:40px;height:40px;border:0;border-radius:50%;background:#EFE2D0;color:var(--ink);cursor:pointer}
.bk .nav button[aria-disabled="true"]{opacity:.35;cursor:default}
.bk .nav svg{width:16px;height:16px}
.bk.t-free .only-full,.bk.t-full .only-free{display:none}
"""
PREV = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M10 3L5 8l5 5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"></path></svg>'
NEXT = PREV.replace('M10 3L5 8l5 5', 'M6 3l5 5-5 5')
MHEAD = (f'<div class="mhead"><p class="mname">noiembrie 2026</p><div class="nav"><button type="button" class="pv" aria-label="Luna trecută" aria-disabled="true" onClick="{{{{ prevM }}}}">{PREV}</button>'
         f'<button type="button" class="nx" aria-label="Luna următoare" onClick="{{{{ nextM }}}}">{NEXT}</button></div></div>')
HEAD = f'<h2 class="disp ri" id="bk-h">{B_H}</h2><p class="intro ri" style="--i: 1">{B_SUB}</p>'


def sec(cls, inner):
    return f'<section class="cs bk {cls} t-free" id="programare" aria-labelledby="bk-h" ref="{{{{ secRef }}}}"><div class="wrap">{inner}</div></section>'


# 1. Cal.com month view: details on the left, the month in the middle, the day's times on the right.
OPTS["ConsProgramare1Luna"] = ("Consiliere, programare 1: luna (cal.com)", BOOK_CSS + """
.b1{background:#EDE0CD}
.b1 .box{display:grid;grid-template-columns:minmax(0,3.2fr) minmax(0,4.4fr) minmax(0,2.4fr);margin-top:48px;border-radius:24px;corner-shape:squircle;background:#FBF7F1;box-shadow:0 0 0 1px rgba(58,42,32,.06),0 30px 60px -44px rgba(70,35,15,.5);overflow:hidden}
.b1 .box>div{padding:28px}
.b1 .info{border-right:1px solid rgba(58,42,32,.1)}
.b1 .who{display:flex;align-items:center;gap:12px;margin-bottom:20px;font-size:14px;color:var(--ink2)}
.b1 .av{width:44px;height:44px;border-radius:50%;overflow:hidden;background:linear-gradient(180deg,#E6D5BD 0%,#D4B894 100%)}
.b1 .av img{display:block;width:100%;height:100%;object-fit:cover;object-position:50% 8%}
.b1 .types{display:grid;gap:8px}
.b1 .times{border-left:1px solid rgba(58,42,32,.1)}
.b1 .times .dn{margin:0 0 14px;font:400 italic 19px/1.2 var(--display);font-variation-settings:'opsz' 20;color:var(--terra-d)}
.b1 .slots{display:grid;gap:8px}
.b1 .sum{margin-top:20px}
@media (max-width:980px){.b1 .box{grid-template-columns:1fr;margin-top:32px}.b1 .box>div{padding:20px 16px}.b1 .info,.b1 .times{border:0}.b1 .times{border-top:1px solid rgba(58,42,32,.1)}.b1 .slots{grid-template-columns:repeat(3,1fr)}.b1 .sum{flex-direction:column;align-items:stretch}}
""", sec("b1", HEAD + '<div class="box ri" style="--i: 2">'
    f'<div class="info"><div class="who"><span class="av"><img src="{DUO}" alt=""></span>Alessia Văideanu</div>{types_html()}</div>'
    f'<div class="cal">{MHEAD}{month(2026, 11)}{month(2026, 12)}</div>'
    f'<div class="times"><p class="dn">{dlabel(DAYS[0])}</p>' + "".join(slot_list(d) for d in DAYS) + '</div></div>'
    f'<div class="ri" style="--i: 3;margin-top:20px">{SUM}{SAMPLE}</div>'))

# 2. Google Calendar week view: the week as columns over the hours; the free times are blocks you tap.
WEEKS = [DAYS[i:i + 5] for i in range(0, 20, 5)]
HOURS = list(range(10, 20))


def week(ws, n):
    head = '<span></span>' + "".join(f'<span class="wd"><small>{WD[d.weekday()][:2].capitalize()}</small><b>{d.day}</b></span>' for d in ws)
    body = "".join(f'<span class="hr" style="grid-row: {(h - 10) * 2 + 1}">{h}:00</span>' for h in HOURS)
    for c, d in enumerate(ws):
        for t in slots(d):
            hh, mm = map(int, t.split(":"))
            r = (hh - 10) * 2 + (mm // 30) + 1
            body += (f'<button type="button" class="slot" data-d="{d.isoformat()}" data-l="{dlabel(d)} · {t}" aria-pressed="false" onClick="{{{{ pickSlot }}}}" '
                     f'style="grid-column: {c + 2}; grid-row: {r} / span 2">{t}</button>')
    return (f'<div class="wk" data-w="{n}"{"" if n == 0 else " hidden"}><div class="wh">{head}</div>'
            f'<div class="wb">{"".join(f'<i style="grid-row: {(h - 10) * 2 + 1}"></i>' for h in HOURS)}{body}</div></div>')


OPTS["ConsProgramare2Saptamana"] = ("Consiliere, programare 2: săptămâna", BOOK_CSS + """
.b2{background:#EDE0CD}
.b2 .top{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:48px;align-items:end}
.b2 .types{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.b2 .box{margin-top:40px;padding:24px 24px 20px;border-radius:24px;corner-shape:squircle;background:#FBF7F1;box-shadow:0 0 0 1px rgba(58,42,32,.06)}
.b2 .wh,.b2 .wb{display:grid;grid-template-columns:64px repeat(5,minmax(0,1fr));column-gap:8px}
.b2 .wh{padding-bottom:12px;border-bottom:1px solid rgba(58,42,32,.12)}
.b2 .wd{display:flex;align-items:baseline;gap:6px}.b2 .wd small{font-size:13px;color:var(--ink2)}.b2 .wd b{font:400 24px/1 var(--display);font-variation-settings:'opsz' 20}
.b2 .wb{grid-template-rows:repeat(20,26px);margin-top:8px;position:relative}
.b2 .wb>i{grid-column:1/-1;border-top:1px solid rgba(58,42,32,.07)}
.b2 .hr{grid-column:1;font-size:12px;color:var(--ink2);font-variant-numeric:tabular-nums}
.b2 .slot{min-height:0;margin:2px 0;border-radius:10px;font-size:13.5px;z-index:1}
.b2 .mhead{margin-bottom:16px}
.b2 .sum{margin-top:20px}
@media (max-width:980px){
  .b2 .top{grid-template-columns:1fr;gap:20px}.b2 .types{grid-template-columns:1fr}
  .b2 .box{padding:16px 10px;overflow-x:auto}.b2 .wk{min-width:520px}
  .b2 .sum{flex-direction:column;align-items:stretch}
}
""", sec("b2", f'<div class="top"><div>{HEAD}</div><div class="ri" style="--i: 2">{types_html()}</div></div>'
    '<div class="box ri" style="--i: 3">'
    + MHEAD.replace("noiembrie 2026", f"{DAYS[0].day} – {DAYS[4].day} noiembrie").replace("prevM", "prevW").replace("nextM", "nextW").replace("Luna trecută", "Săptămâna trecută").replace("Luna următoare", "Săptămâna următoare")
    + "".join(week(w, n) for n, w in enumerate(WEEKS)) + f'</div><div class="ri" style="--i: 4;margin-top:4px">{SUM}{SAMPLE}</div>'))

# 3. Doctolib: the days as columns, each with its own times underneath; arrows move along the days.
OPTS["ConsProgramare3Coloane"] = ("Consiliere, programare 3: coloane", BOOK_CSS + """
.b3{background:#EDE0CD}
.b3 .stage{display:grid;grid-template-columns:minmax(0,4fr) minmax(0,8fr);gap:56px;align-items:start}
.b3 .types{display:grid;gap:8px;margin-top:32px}
.b3 .box{padding:24px;border-radius:24px;corner-shape:squircle;background:#FBF7F1;box-shadow:0 0 0 1px rgba(58,42,32,.06),0 30px 60px -44px rgba(70,35,15,.5)}
.b3 .cols{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px}
.b3 .col{display:flex;flex-direction:column;gap:8px}
.b3 .col>p{margin:0 0 6px;padding-bottom:10px;border-bottom:1px solid rgba(58,42,32,.12);text-align:center;font-size:13px;color:var(--ink2);line-height:1.3}
.b3 .col>p b{display:block;font:400 22px/1.1 var(--display);font-variation-settings:'opsz' 20;color:var(--ink)}
.b3 .col .none{display:grid;place-items:center;min-height:44px;color:rgba(58,42,32,.3)}
.b3 .sum{margin-top:20px}
@media (max-width:980px){
  .b3 .stage{grid-template-columns:1fr;gap:24px}.b3 .types{margin-top:24px}
  .b3 .box{padding:16px 12px}.b3 .cols{grid-template-columns:repeat(3,minmax(0,1fr));gap:6px}.b3 .col:nth-child(n+4){display:none}
  .b3 .slot{padding:0 4px;font-size:14px}.b3 .sum{flex-direction:column;align-items:stretch}
}
""", sec("b3", '<div class="stage"><div>' + HEAD + f'<div class="ri" style="--i: 2">{types_html()}</div></div>'
    '<div class="ri" style="--i: 3"><div class="box">'
    + MHEAD.replace("noiembrie 2026", f"{DAYS[0].day} – {DAYS[4].day} noiembrie").replace("prevM", "prevW").replace("nextM", "nextW").replace("Luna trecută", "Zilele trecute").replace("Luna următoare", "Zilele următoare")
    + "".join(f'<div class="cols wk" data-w="{n}"{"" if n == 0 else " hidden"}>' + "".join(
        f'<div class="col"><p>{WD[d.weekday()][:3]}.<b>{d.day} {MO[d.month][1]}</b></p>'
        + "".join(f'<button type="button" class="slot" data-d="{d.isoformat()}" data-l="{dlabel(d)} · {t}" aria-pressed="false" onClick="{{{{ pickSlot }}}}">{t}</button>' for t in slots(d))
        + "</div>" for d in w) + "</div>" for n, w in enumerate(WEEKS))
    + f'</div>{SUM}{SAMPLE}</div></div>'))

# 4. Calendly: first two big cards (which meeting), then the day strip and the times.
OPTS["ConsProgramare4Alegi"] = ("Consiliere, programare 4: întâi alegi ședința", BOOK_CSS + """
.b4{background:#EDE0CD}
.b4 .head{max-width:760px;margin:0 auto;text-align:center}.b4 .intro{margin-left:auto;margin-right:auto}
.b4 .types{display:grid;grid-template-columns:1fr 1fr;gap:16px;max-width:900px;margin:48px auto 0}
.b4 .type{gap:10px;min-height:150px;justify-content:flex-end;padding:24px;border-radius:22px;corner-shape:squircle;background:#FBF7F1;box-shadow:0 0 0 1px rgba(58,42,32,.08)}
.b4 .type b{font-size:28px}.b4 .type span{font-size:15px}
.b4 .type[aria-pressed="true"]{background:#3A2A20;color:#F4EDE4;box-shadow:none}
.b4 .type[aria-pressed="true"] span{color:#D8C6B2}
.b4 .box{max-width:900px;margin:16px auto 0;padding:24px;border-radius:22px;corner-shape:squircle;background:#FBF7F1;box-shadow:0 0 0 1px rgba(58,42,32,.06)}
.b4 .strip{display:flex;gap:8px;overflow-x:auto;padding-bottom:6px;scrollbar-width:thin;scroll-snap-type:x proximity}
.b4 .strip .day{flex:0 0 68px;aspect-ratio:auto;max-height:none;height:76px;border-radius:16px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;scroll-snap-align:start}
.b4 .strip .day small{font-size:12px;font-weight:500;opacity:.75}
.b4 .slots{display:flex;flex-wrap:wrap;gap:8px;margin-top:20px}
.b4 .sum{max-width:900px;margin:20px auto 0}
.b4 .smp{max-width:900px;margin-left:auto;margin-right:auto}
@media (max-width:980px){.b4 .types{grid-template-columns:1fr;gap:8px;margin-top:32px}.b4 .type{min-height:0;padding:18px}.b4 .type b{font-size:23px}.b4 .box{padding:16px 12px}.b4 .slots{display:grid;grid-template-columns:repeat(3,1fr)}.b4 .sum{flex-direction:column;align-items:stretch}}
""", sec("b4", f'<div class="head">{HEAD}</div><div class="ri" style="--i: 2">{types_html()}</div>'
    '<div class="box ri" style="--i: 3"><div class="strip" role="group" aria-label="Ziua">'
    + "".join(f'<button type="button" class="day" data-d="{d.isoformat()}" aria-pressed="{"true" if d == DAYS[0] else "false"}" aria-label="{dlabel(d)}" onClick="{{{{ pickDay }}}}"><small>{WD[d.weekday()][:2].capitalize()}</small>{d.day} {MO[d.month][1]}</button>' for d in DAYS)
    + '</div>' + "".join(slot_list(d) for d in DAYS) + f'</div><div class="ri" style="--i: 4">{SUM}{SAMPLE}</div>'))

FAQ_HTML = ('<section class="fq f3" id="intrebari" aria-labelledby="fq-h" ref="{{ secRef }}"><div class="wrap">'
            f'<div class="head ri"><h2 class="disp" id="fq-h">{fq.H}</h2></div><div class="cards"><div class="acc ri" style="--i: 1">'
            + "".join(f'<details name="faq-consiliere"{" open" if i == 0 else ""}><summary><span class="qq">{q}</span>{fq.ICON}</summary>'
                      f'<div class="ans"><p>{a}</p></div></details>' for i, (q, a) in enumerate(QA))
            + f'</div><aside class="other ri" style="--i: 2" aria-label="{fq.ASK}"><p class="ask">{fq.ASK}</p><p class="reply">{fq.REPLY}</p>'
            f'<div class="links">{fq.WRITE}{fq.ALL}</div></aside></div></div></section>')

HANDLERS = """
    pickType: function (e) { var b = e.currentTarget, s = self.sec, k = b.getAttribute('data-k');
      s.querySelectorAll('.type').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      s.classList.toggle('t-free', k === 'free'); s.classList.toggle('t-full', k === 'full'); },
    pickDay: function (e) { var b = e.currentTarget, s = self.sec, d = b.getAttribute('data-d');
      s.querySelectorAll('.day[data-d]').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      s.querySelectorAll('.slots').forEach(function (x) { x.hidden = x.getAttribute('data-d') !== d; });
      var dn = s.querySelector('.dn'); if (dn) dn.textContent = b.getAttribute('aria-label'); },
    pickSlot: function (e) { var b = e.currentTarget, s = self.sec;
      s.querySelectorAll('.slot').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      s.querySelector('.sum .lab').textContent = b.getAttribute('data-l'); s.querySelector('.go').setAttribute('aria-disabled', 'false'); },
    goOn: function (e) { },
    prevM: function () { self.month(-1); }, nextM: function () { self.month(1); },
    prevW: function () { self.weekGo(-1); }, nextW: function () { self.weekGo(1); },"""
METHODS = """
  month(d) { var s = this.sec, ms = s.querySelectorAll('.mon'), i = 0;
    ms.forEach(function (m, k) { if (!m.hidden) i = k; }); i = Math.max(0, Math.min(ms.length - 1, i + d));
    ms.forEach(function (m, k) { m.hidden = k !== i; });
    s.querySelector('.mname').textContent = ['noiembrie 2026', 'decembrie 2026'][i];
    s.querySelector('.pv').setAttribute('aria-disabled', i === 0 ? 'true' : 'false'); s.querySelector('.nx').setAttribute('aria-disabled', i === ms.length - 1 ? 'true' : 'false'); }
  weekGo(d) { var s = this.sec, ws = s.querySelectorAll('.wk'), i = 0;
    ws.forEach(function (w, k) { if (!w.hidden) i = k; }); i = Math.max(0, Math.min(ws.length - 1, i + d));
    ws.forEach(function (w, k) { w.hidden = k !== i; });
    s.querySelector('.mname').textContent = WEEKS[i];
    s.querySelector('.pv').setAttribute('aria-disabled', i === 0 ? 'true' : 'false'); s.querySelector('.nx').setAttribute('aria-disabled', i === ws.length - 1 ? 'true' : 'false'); }"""
WEEK_NAMES = [f"{w[0].day} {MO[w[0].month][0]} – {w[-1].day} {MO[w[-1].month][0]}".replace(f" {MO[w[0].month][0]} –", " –") if w[0].month == w[-1].month
              else f"{w[0].day} {MO[w[0].month][1]} – {w[-1].day} {MO[w[-1].month][1]}" for w in WEEKS]


def script():
    import json
    return ("var WEEKS = " + json.dumps(WEEK_NAMES, ensure_ascii=False) + ";\n"
            "class Component extends DCLogic {\n  componentDidMount() {" + ENTER + "\n  }\n"
            "  componentWillUnmount() { if (this.io) this.io.disconnect(); }\n" + METHODS + "\n"
            "  renderVals() { var self = this; if (!this.cb) this.cb = {" + HANDLERS + " secRef: function (el) { self.sec = el; } }; return this.cb; }\n}")


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


ALL_OPTS = {k: (t, co.SEC + css, html) for k, (t, css, html) in OPTS.items()}
ALL_OPTS["ConsDetalii"] = ("Consiliere: cum funcționează + prima întâlnire", DET_CSS, DET_HTML)
ALL_OPTS["ConsFaq"] = ("Consiliere: întrebări frecvente", gp.FAQ_CSS, FAQ_HTML)
H = {"ConsHero": (905, 789)}
H.update({"ConsIntrebari1Calm": (1042, 757), "ConsIntrebari2Carduri": (695, 606), "ConsIntrebari3Mesaje": (784, 975),
          "ConsIntrebari4Portret": (824, 1150), "ConsDetalii": (917, 1166), "ConsProgramare1Luna": (1043, 1407),
          "ConsProgramare2Saptamana": (1272, 1416), "ConsProgramare3Coloane": (709, 1100), "ConsProgramare4Alegi": (905, 1018), "ConsFaq": (1092, 1357)})

if __name__ == "__main__":
    gh.SOURCES["ConsHero"] = SOURCES["ConsHero"]
    hero_css = gh.OPTS["GrupHero2Aman"][2]
    for suffix, w, h in (("", 1440, H["ConsHero"][0]), ("Mobil", 390, H["ConsHero"][1])):
        f = os.path.join(P, f"ConsHero{suffix}.dc.html")
        open(f, "w", encoding="utf-8").write(gh.page("ConsHero", "Consiliere 1:1: deschiderea" + (" · mobil" if suffix else ""), "dark", hero_css, HERO_HTML, w, h))
        if not suffix:
            subprocess.run([sys.executable, os.path.join(HERE, "dc2html.py"), f, os.path.join(HERE, "opt-ConsHero.html")], check=True, capture_output=True)
    for name, (title, css, html) in ALL_OPTS.items():
        for suffix, w, h in (("", 1440, H[name][0]), ("Mobil", 390, H[name][1])):
            f = os.path.join(P, f"{name}{suffix}.dc.html")
            open(f, "w", encoding="utf-8").write(page(name, title + (" · mobil" if suffix else ""), css, html, w, h))
            if not suffix:
                subprocess.run([sys.executable, os.path.join(HERE, "dc2html.py"), f, os.path.join(HERE, f"opt-{name}.html")], check=True, capture_output=True)
    print("wrote", ["ConsHero"] + list(ALL_OPTS))
