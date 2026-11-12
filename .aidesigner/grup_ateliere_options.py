"""Subpaginile „Ce oferim”, part 2: every upcoming workshop on „Ateliere de grup” (Vali, 12 nov: 15 noiembrie, 6 și 13 decembrie).
Four directions, each from a real site. The hero's button („Vezi următoarele ateliere”) lands here (#ateliere).

usage: python3 .aidesigner/grup_ateliere_options.py
writes .aidesigner/canvas/project/GrupAteliere1..4*.dc.html (+ Mobil twins) and local previews .aidesigner/opt-GrupAteliere*.html

Copy: grup_hero_options.EVENTS (docs/continut-site.md, Evenimente). Button: „Mă înscriu” (doc), solid, no arrow (Vali, 12 nov:
solid buttons carry no arrow; on phones they span the card, text centred). Sold out (Vali, 12 nov: there is no waiting list):
no disabled button, which reads as broken and can't be reached by keyboard; the ticket keeps its „Sold out” stamp and the
button's place goes to a quiet link to the next workshop that still has places (mine, to approve: „Vezi următorul atelier”).
Unknown time / place stay visible placeholders.
Motion per DESIGN.md §8: the site's scroll reveal, siblings 80ms apart; hover lifts 3px; reduced motion = still.
"""
import calendar, os, subprocess, sys
from about_options2 import P, HERE, FONTS, BASE_CSS, ARROW
from grup_hero_options import EVENTS, COMMON as HERO_COMMON, ROOM, BOWL, HANDS, ROOM2, pic
from cf_pagina_options import ENTER

H2 = '<h2 class="disp" id="ga-h">Atelierele care urmează</h2>'
SOURCES = {
    "GrupAteliere1Lista": "lu.ma: lista de evenimente a unui calendar, cu data mare în stânga și o linie care le leagă",
    "GrupAteliere2Carduri": "airbnb.com/experiences: cardurile cu poză, câte unul pentru fiecare dată",
    "GrupAteliere3Bilete": "dice.fm: biletele cu cotor, iar „Sold out” e o ștampilă de lut, ca ștampila AVA",
    "GrupAteliere4Calendar": "cal.com: calendarul pe luni; alegi o zi marcată și vezi atelierul ei",
}
PHOTOS = [BOWL, HANDS, ROOM2]   # real, October; no themed (Christmas) photos yet


DOWN = '<svg class="ar dn" viewBox="0 0 16 16" aria-hidden="true"><path d="M8 3V13M4 9L8 13L12 9" fill="none" stroke="currentColor" style="stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round"></path></svg>'


def aid(e):
    return f'atelier-{e["day"]}-{e["mo"]}'


def btn(e, cls="btn"):
    if e["sold"]:
        nxt = next((x for x in EVENTS[EVENTS.index(e) + 1:] if not x["sold"]), None)
        return f'<a class="alt" href="#{aid(nxt)}">Vezi următorul atelier {DOWN}</a>' if nxt else ""
    return f'<a class="{cls}" href="#inscriere">Mă înscriu</a>'


def when(e):
    return f'{e["wd"]}, {e["day"]} {e["mon"]} · {e["time"]}'


def ph(v):
    """[PLACEHOLDER] values get the dashed placeholder look"""
    return f'<span class="todo">{v}</span>' if v.startswith("[") else v


SOLD = '<span class="badge">Sold out</span>'

COMMON = HERO_COMMON + """
.ga{background:linear-gradient(180deg,#F4EDE4 0%,#EDE0CD 100%);padding:96px 0 112px}
.ga h2{font-size:clamp(40px,4.4vw,64px);line-height:1.05}
.ga .t{margin:0;font:400 26px/1.15 var(--display);font-variation-settings:'opsz' 20;letter-spacing:-.01em;text-wrap:balance}
.ga .w{margin:6px 0 0;font-size:15px;color:var(--ink2);font-variant-numeric:tabular-nums}
.ga .d{margin:12px 0 0;font-size:16px;line-height:1.6;color:#4A382C;text-wrap:pretty}
.ga .pr{font:400 24px/1 var(--display);font-variation-settings:'opsz' 20;font-variant-numeric:tabular-nums;white-space:nowrap}
.ga .todo{display:inline-block;padding:0 6px;border:1px dashed rgba(156,71,44,.55);border-radius:6px;color:var(--terra-d);font-size:.92em;letter-spacing:.02em}
.ga .badge{display:inline-flex;align-items:center;min-height:28px;padding:0 12px;border-radius:999px;border:1px solid #9C472C;color:#9C472C;font-size:13px;font-weight:600;letter-spacing:.02em}
.ga .btn{white-space:nowrap;justify-content:center}
.ga .alt{justify-self:start;align-self:start;display:inline-flex;align-items:center;gap:8px;min-height:44px;color:var(--ink);font-weight:500;white-space:nowrap;
  background:linear-gradient(currentColor,currentColor) 0 calc(100% - 9px)/100% 1px no-repeat;transition:background-size .3s var(--so)}
.ga .alt:hover{background-size:0 1px;background-position:100% calc(100% - 9px)}
.ga .alt .dn{transition:transform .3s var(--so)}.ga .alt:hover .dn{transform:translateY(3px)}
.ga .alt:focus-visible{outline:2px solid #9C472C;outline-offset:3px}
.a4 .pane .alt{color:#F2C79C}
.ga .card{transition:translate .4s var(--so),box-shadow .4s ease}
@media (hover:hover){.ga .card:hover{translate:0 -3px;box-shadow:0 0 0 1px rgba(58,42,32,.08),0 22px 40px -28px rgba(58,30,15,.5)}}
.ga .sold{opacity:.78}
@keyframes ga-up{from{opacity:0;translate:0 16px}}
.ga.js:not(.in) .ri{opacity:0}
.ga.js.in .ri{animation:ga-up .8s var(--so) backwards;animation-delay:calc(var(--i,0) * 80ms)}
@media (max-width:980px){.ga{padding:64px 0 80px}.ga .t{font-size:23px}.ga .card .btn{align-self:stretch;width:100%;box-sizing:border-box}}
@media (prefers-reduced-motion:reduce){.ga *{animation:none!important;transition:none!important}}
"""

OPTS = {}

# 1. lu.ma calendar: the big date on the left, a thin line linking the dates, the details in a light card on the right.
OPTS["GrupAteliere1Lista"] = ("Atelierele care urmează 1: listă de calendar", """
.a1 h2{margin-bottom:48px}
.a1 ol{position:relative;margin:0;padding:0;list-style:none;max-width:980px}
.a1 ol::before{content:"";position:absolute;left:59px;top:18px;bottom:18px;width:1px;background:rgba(58,42,32,.18)}
.a1 li{position:relative;display:grid;grid-template-columns:120px minmax(0,1fr);gap:32px;align-items:start}
.a1 li+li{margin-top:20px}
.a1 .dt{position:relative;z-index:1;display:flex;flex-direction:column;align-items:center;padding:10px 0;background:#F1E7DA;border-radius:18px;corner-shape:squircle}
.a1 .dt b{font:400 52px/1 var(--display);font-variation-settings:'opsz' 72;font-variant-numeric:tabular-nums}
.a1 .dt span{font-size:14px;color:var(--ink2)}
.a1 .card{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:20px 32px;align-items:center;padding:26px 28px;border-radius:22px;corner-shape:squircle;background:#FBF7F1;box-shadow:0 0 0 1px rgba(58,42,32,.06)}
.a1 .side{display:flex;flex-direction:column;align-items:flex-end;gap:14px}
.a1 .t .badge{margin-left:10px;vertical-align:4px}
@media (max-width:980px){
  .a1 h2{margin-bottom:28px}
  .a1 ol::before{left:31px}
  .a1 li{grid-template-columns:64px minmax(0,1fr);gap:14px}
  .a1 .dt{padding:8px 0;border-radius:14px}.a1 .dt b{font-size:32px}.a1 .dt span{font-size:12.5px}
  .a1 .card{grid-template-columns:1fr;padding:20px}
  .a1 .side{flex-direction:row;align-items:center;justify-content:space-between;flex-wrap:wrap}
  .a1 .t .badge{display:flex;width:max-content;margin:8px 0 0}
}
""", '<section class="gp ga a1" id="ateliere" aria-labelledby="ga-h" ref="{{ secRef }}"><div class="wrap">' + H2 + "<ol>" + "".join(
    f'<li class="ri{" sold" if e["sold"] else ""}" id="{aid(e)}" style="--i: {i}"><p class="dt" aria-hidden="true"><b>{e["day"]}</b><span>{e["mo"]}</span></p>'
    f'<article class="card"><div><h3 class="t">{e["title"]}{SOLD if e["sold"] else ""}</h3><p class="w">{when(e)} · {ph(e["where"])}</p>'
    f'<p class="d">{e["line"]}</p></div><div class="side"><span class="pr">{e["price"]}</span>{btn(e)}</div></article></li>'
    for i, e in enumerate(EVENTS)) + "</ol></div></section>")

# 2. Airbnb Experiences: one photo card per date, three in a row; on the phone they scroll sideways and snap.
OPTS["GrupAteliere2Carduri"] = ("Atelierele care urmează 2: carduri cu poză", """
.a2 .head{display:flex;justify-content:space-between;align-items:end;gap:20px;margin-bottom:40px}
.a2 .head p{margin:0;font-size:15px;color:var(--ink2)}
.a2 ul{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px;margin:0;padding:0;list-style:none}
.a2 .card{display:flex;flex-direction:column;height:100%;border-radius:22px;corner-shape:squircle;overflow:hidden;background:#FBF7F1;box-shadow:0 0 0 1px rgba(58,42,32,.06)}
.a2 .ph{position:relative;aspect-ratio:4/3;overflow:hidden}
.a2 .ph img{transition:transform 1.2s var(--so)}
@media (hover:hover){.a2 .card:hover .ph img{transform:scale(1.04)}}
.a2 .chip{position:absolute;left:14px;top:14px;display:flex;flex-direction:column;align-items:center;min-width:58px;padding:7px 10px 6px;border-radius:14px;background:rgba(251,247,241,.94);color:var(--ink);box-shadow:0 6px 20px -8px rgba(0,0,0,.35)}
.a2 .chip b{font:400 28px/1 var(--display);font-variation-settings:'opsz' 20;font-variant-numeric:tabular-nums}
.a2 .chip span{font-size:12.5px;color:var(--ink2)}
.a2 .ph .badge{position:absolute;right:14px;top:14px;background:#FBF7F1}
.a2 .bd{display:flex;flex-direction:column;flex:1;padding:22px 22px 24px}
.a2 .d{flex:1}
.a2 .ft{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;margin-top:20px}
.a2 .btn{min-height:46px;padding:0 20px;font-size:14.5px}
@media (max-width:980px){
  .a2 .head{flex-direction:column;align-items:start;margin-bottom:24px}
  .a2 ul{display:flex;gap:12px;margin:0 -20px;padding:0 20px 8px;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none}
  .a2 li{flex:0 0 82%;scroll-snap-align:start}
}
""", '<section class="gp ga a2" id="ateliere" aria-labelledby="ga-h" ref="{{ secRef }}"><div class="wrap">'
    f'<div class="head ri">{H2}<p>{len(EVENTS)} ateliere în calendar · maxim 8 persoane fiecare</p></div><ul>' + "".join(
    f'<li class="ri{" sold" if e["sold"] else ""}" id="{aid(e)}" style="--i: {i + 1}"><article class="card"><div class="ph">{pic(PHOTOS[i])}'
    f'<p class="chip" aria-hidden="true"><b>{e["day"]}</b><span>{e["mo"]}</span></p>{SOLD if e["sold"] else ""}</div>'
    f'<div class="bd"><h3 class="t">{e["title"]}</h3><p class="w">{when(e)}<br>{ph(e["where"])}</p><p class="d">{e["line"]}</p>'
    f'<div class="ft"><span class="pr">{e["price"]}</span>{btn(e)}</div></div></article></li>'
    for i, e in enumerate(EVENTS)) + "</ul></div></section>")

# 3. dice.fm tickets: each workshop is a ticket with a torn-off stub (date + price); sold out = a clay stamp pressed on it.
OPTS["GrupAteliere3Bilete"] = ("Atelierele care urmează 3: bilete", """
.a3 h2{margin-bottom:44px}
.a3 ul{display:grid;gap:18px;margin:0;padding:0;list-style:none;max-width:1040px}
.a3 .card{position:relative;display:grid;grid-template-columns:170px minmax(0,1fr);border-radius:20px;corner-shape:squircle;background:#FBF7F1;box-shadow:0 0 0 1px rgba(58,42,32,.06)}
/* the stub, cut off by a dotted seam with two half-circle notches */
.a3 .stub{position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;padding:24px 12px;border-right:2px dotted rgba(58,42,32,.22);text-align:center}
.a3 .stub::before,.a3 .stub::after{content:"";position:absolute;right:-13px;width:24px;height:24px;border-radius:50%;background:#F2E8DB}
.a3 .stub::before{top:-12px}.a3 .stub::after{bottom:-12px}
.a3 .stub .wd{font-size:13px;color:var(--ink2)}
.a3 .stub b{font:400 56px/1 var(--display);font-variation-settings:'opsz' 72;font-variant-numeric:tabular-nums}
.a3 .stub .mo{font:400 italic 18px/1 var(--display);font-variation-settings:'opsz' 20;color:var(--terra-d)}
.a3 .stub .pr{margin-top:10px;font-size:20px}
.a3 .bd{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:16px 28px;align-items:center;padding:26px 30px}
/* sold out: a round clay stamp, pressed on when the ticket comes into view */
.a3 .stamp{position:absolute;left:29px;top:50%;display:grid;place-items:center;width:112px;height:112px;margin-top:-56px;border-radius:50%;color:#9C472C;
  box-shadow:inset 0 0 0 2px rgba(156,71,44,.8),inset 0 0 0 6px rgba(251,247,241,1),inset 0 0 0 7px rgba(156,71,44,.6);background:rgba(251,247,241,.86);font:400 italic 22px/1 var(--display);font-variation-settings:'opsz' 20;rotate:-12deg;pointer-events:none}
@keyframes a3-press{0%{opacity:0;scale:1.6}60%{opacity:1;scale:.94}100%{scale:1}}
.a3.js:not(.in) .stamp{opacity:0}
.a3.js.in .stamp{animation:a3-press .6s cubic-bezier(.3,1.32,.5,1) .7s backwards}
@media (max-width:980px){
  .a3 h2{margin-bottom:28px}
  .a3 .card{grid-template-columns:1fr}
  .a3 .stub{flex-direction:row;flex-wrap:wrap;justify-content:flex-start;align-items:baseline;gap:4px 8px;padding:16px 20px 14px;border-right:0;border-bottom:2px dotted rgba(58,42,32,.22);text-align:left}
  .a3 .stub::before,.a3 .stub::after{top:auto;bottom:-13px;right:auto}
  .a3 .stub::before{left:-12px}.a3 .stub::after{right:-12px;left:auto}
  .a3 .stub b{order:-1;font-size:40px}.a3 .stub .wd{order:1}.a3 .stub .pr{order:2;margin:0 0 0 auto;font-size:18px}
  .a3 .bd{grid-template-columns:1fr;padding:18px 20px 22px}
  .a3 .stamp{left:auto;right:16px;top:12px;width:80px;height:80px;margin:0;font-size:16px}
}
""", None)


def bilete(deco=lambda e: "", cls="a3"):
    """the tickets; deco(e) adds decoration inside a ticket (the Christmas variants, grup_craciun_options.py)"""
    return (f'<section class="gp ga {cls}" id="ateliere" aria-labelledby="ga-h" ref="{{{{ secRef }}}}"><div class="wrap">' + H2 + "<ul>" + "".join(
    f'<li class="ri{" sold" if e["sold"] else ""}{" xmas" if deco(e) else ""}" id="{aid(e)}" style="--i: {i}"><article class="card">'
    f'<p class="stub"><span class="wd">{e["wd"]}</span><b>{e["day"]}</b><span class="mo">{e["mon"]}</span><span class="pr">{e["price"]}</span></p>'
    f'<div class="bd"><div><h3 class="t">{e["title"]}</h3><p class="w">{e["time"] if not e["time"].startswith("[") else ph(e["time"])} · {ph(e["where"])}</p><p class="d">{e["line"]}</p></div>{btn(e)}</div>'
    + ('<span class="stamp" aria-label="Sold out">Sold out</span>' if e["sold"] else "") + deco(e) + "</article></li>"
    for i, e in enumerate(EVENTS)) + "</ul></div></section>")


OPTS["GrupAteliere3Bilete"] = OPTS["GrupAteliere3Bilete"][:2] + (bilete(),)


# 4. cal.com: the two months side by side, the workshop days marked; pick one to see it. Starts on the first free date.
def month(y, m, name):
    by_day = {int(e["day"]): (i, e) for i, e in enumerate(EVENTS) if e["mo"] == name[:3].lower()}
    cells = []
    for wk in calendar.Calendar(firstweekday=0).monthdayscalendar(y, m):
        for d in wk:
            if not d:
                cells.append('<span></span>')
            elif d in by_day:
                i, e = by_day[d]
                cells.append(f'<button type="button" class="day ev{" so" if e["sold"] else ""}" data-i="{i}" aria-pressed="{"true" if i == FIRST else "false"}" '
                             f'aria-label="{e["wd"]}, {d} {e["mon"]}{", sold out" if e["sold"] else ""}" onClick="{{{{ pick }}}}">{d}</button>')
            else:
                cells.append(f'<span class="day">{d}</span>')
    head = "".join(f"<abbr>{d}</abbr>" for d in ["L", "Ma", "Mi", "J", "V", "S", "D"])
    return f'<div class="mon"><p class="mn">{name} {y}</p><div class="grid">{head}{"".join(cells)}</div></div>'


FIRST = next(i for i, e in enumerate(EVENTS) if not e["sold"])
OPTS["GrupAteliere4Calendar"] = ("Atelierele care urmează 4: calendar", """
.a4 h2{margin-bottom:12px}
.a4 .sub{margin:0 0 40px;font-size:15px;color:var(--ink2)}
.a4 .stage{display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:28px;align-items:stretch}
.a4 .cal{display:grid;grid-template-columns:1fr 1fr;gap:32px;padding:28px;border-radius:22px;corner-shape:squircle;background:#FBF7F1;box-shadow:0 0 0 1px rgba(58,42,32,.06)}
.a4 .mn{margin:0 0 14px;font:400 22px/1 var(--display);font-variation-settings:'opsz' 20;text-transform:capitalize}
.a4 .grid{display:grid;grid-template-columns:repeat(7,1fr);gap:4px;text-align:center}
.a4 abbr{padding-bottom:6px;font-size:12px;color:var(--ink2);text-decoration:none}
.a4 .day{display:grid;place-items:center;aspect-ratio:1;border:0;border-radius:50%;background:none;font:400 14.5px/1 var(--text);color:rgba(58,42,32,.42);font-variant-numeric:tabular-nums}
.a4 button.day{position:relative;cursor:pointer;color:var(--ink);font-weight:600;background:#EFE2D0;transition:background-color .25s,color .25s,scale .3s cubic-bezier(.3,1.32,.5,1)}
.a4 button.day::after{content:"";position:absolute;bottom:5px;left:50%;width:4px;height:4px;margin-left:-2px;border-radius:50%;background:#9C472C}
.a4 button.day.so{background:none;text-decoration:line-through;text-decoration-color:rgba(156,71,44,.6);color:var(--ink2)}
.a4 button.day.so::after{background:rgba(58,42,32,.3)}
.a4 button.day:hover{scale:1.08}
.a4 button.day[aria-pressed="true"]{background:#3A2A20;color:#F4EDE4}
.a4 button.day[aria-pressed="true"]::after{background:#F2C79C}
.a4 button.day:focus-visible{outline:2px solid #9C472C;outline-offset:2px}
.a4 .panes{position:relative}
.a4 .pane{display:none;flex-direction:column;height:100%;box-sizing:border-box;padding:28px 28px 26px;border-radius:22px;corner-shape:squircle;background:#3A2A20;color:#F4EDE4}
.a4 .pane.on{display:flex}
@keyframes a4-in{from{opacity:0;translate:0 8px}}
@media (prefers-reduced-motion:no-preference){.a4 .pane.on{animation:a4-in .35s var(--so)}}
.a4 .pane .when{margin:0;font:400 italic 20px/1.3 var(--display);font-variation-settings:'opsz' 20;color:#F2C79C}
.a4 .pane .t{margin-top:10px;font-size:30px}
.a4 .pane .w{color:#D8C6B2}
.a4 .pane .d{flex:1;color:#EFE3D3}
.a4 .pane .ft{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-top:22px}
.a4 .pane .btn{background:#F4EDE4;color:#2E1D14}
.a4 .pane .btn:hover{background:#FFF8EE}
.a4 .pane .btn.wait{background:transparent;color:#F4EDE4;box-shadow:inset 0 0 0 1.5px rgba(244,237,228,.6)}
.a4 .pane .badge{border-color:#F2C79C;color:#F2C79C}
.a4 .pane .todo{border-color:rgba(242,199,156,.6);color:#F2C79C}
@media (max-width:980px){
  .a4 .sub{margin-bottom:24px}
  .a4 .stage{grid-template-columns:1fr;gap:12px}
  .a4 .cal{grid-template-columns:1fr;gap:24px;padding:20px}
  .a4 .pane{padding:22px 20px}.a4 .pane .t{font-size:25px}
}
""", '<section class="gp ga a4" id="ateliere" aria-labelledby="ga-h" ref="{{ secRef }}"><div class="wrap">' + H2
    + '<p class="sub ri">Zilele marcate au atelier. Alege una ca să vezi detaliile.</p>'
    + '<div class="stage"><div class="cal ri" style="--i: 1">' + month(2026, 11, "noiembrie") + month(2026, 12, "decembrie") + '</div>'
    + '<div class="panes ri" style="--i: 2" aria-live="polite">' + "".join(
        f'<article class="pane{" on" if i == FIRST else ""}" data-i="{i}"><p class="when">{when(e)}</p><h3 class="t">{e["title"]}</h3>'
        f'<p class="w">{ph(e["where"])}</p><p class="d">{e["line"]}</p>'
        f'<div class="ft"><span class="pr">{e["price"]}</span>{SOLD if e["sold"] else ""}{btn(e)}</div></article>'
        for i, e in enumerate(EVENTS)) + "</div></div></div></section>")

PICK = """
    pick: function (e) {
      var b = e.currentTarget, s = self.sec, i = b.getAttribute('data-i');
      s.querySelectorAll('button.day.ev').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      s.querySelectorAll('.pane').forEach(function (p) { p.classList.toggle('on', p.getAttribute('data-i') === i); });
    },"""


def script():
    return ("class Component extends DCLogic {\n  componentDidMount() {" + ENTER + "\n  }\n"
            "  componentWillUnmount() { if (this.io) this.io.disconnect(); }\n"
            "  renderVals() { var self = this; if (!this.cb) this.cb = {" + PICK + " secRef: function (el) { self.sec = el; } }; return this.cb; }\n}")


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
{BASE_CSS}{COMMON}{css}</style>
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


# preview heights, measured in the browser (desktop 1440, phone 390)
H = {"GrupAteliere1Lista": (940, 1500), "GrupAteliere2Carduri": (997, 966), "GrupAteliere3Bilete": (1011, 1521), "GrupAteliere4Calendar": (717, 1335)}

if __name__ == "__main__":
    for name, (title, css, html) in OPTS.items():
        for suffix, w, h in (("", 1440, H[name][0]), ("Mobil", 390, H[name][1])):
            f = os.path.join(P, f"{name}{suffix}.dc.html")
            open(f, "w", encoding="utf-8").write(page(name, title + (" · mobil" if suffix else ""), css, html, w, h))
            if not suffix:
                subprocess.run([sys.executable, os.path.join(HERE, "dc2html.py"), f, os.path.join(HERE, f"opt-{name}.html")], check=True, capture_output=True)
        print("wrote", name)
