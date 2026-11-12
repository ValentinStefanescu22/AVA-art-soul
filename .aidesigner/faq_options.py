"""Acasă: 'Întrebări frecvente' (Vali, 11 nov: nothing extravagant, clean, clear, fits the page). Three variants:
F1 Două coloane   heading + 'other question?' on the left, the accordion on the right (dividers).
F2 Centrat        one centred column, numbered questions.
F3 Carduri        each question a soft card; the last card is 'Ai altă întrebare?'.
The accordion is native <details> (one open at a time via name=), animated with ::details-content where supported.
Copy: docs/continut-site.md, 'Întrebări frecvente (Acasă)'. 'Îți răspundem în maxim 24 de ore.' is from Contact.
Mine (to approve): 'Ai altă întrebare?', 'Scrie-mi', 'Toate întrebările'.

usage: python3 .aidesigner/faq_options.py
"""
import os, subprocess, sys
from about_options2 import P, HERE, FONTS, BASE_CSS, ARROW

H = "Întrebări frecvente"
QA = [
    ("Trebuie să știu să lucrez cu lutul?",
     "Deloc. Majoritatea celor care vin la atelierele mele ating lutul pentru prima dată. Te ghidez pas cu pas."),
    ("Pot veni singur(ă)?",
     "Sigur. Mulți vin singuri și pleacă făcând parte dintr-o comunitate."),
    ("Nu știu ce mi se potrivește. De unde încep?",
     'Dacă vrei să încerci, un <a href="#ateliere-de-grup">atelier de grup</a> e cel mai simplu început. Dacă vrei ceva doar pentru tine, '
     'alege un <a href="#atelier-privat">atelier privat</a> sau o <a href="#consiliere">ședință de consiliere</a>. '
     'Poți explora opțiunile pe site sau <a href="#contact">îmi poți scrie</a> și te ajut să alegi.'),
]
ASK = "Ai altă întrebare?"
REPLY = "Îți răspundem în maxim 24 de ore."
WRITE = f'<a class="more" href="#contact">Scrie-mi {ARROW}</a>'
ALL = f'<a class="more" href="#faq">Toate întrebările {ARROW}</a>'
ICON = ('<span class="ic" aria-hidden="true"><svg viewBox="0 0 16 16"><path class="h" d="M3 8H13"></path><path class="v" d="M8 3V13"></path></svg></span>')


def acc(num=False):
    out = []
    for i, (q, a) in enumerate(QA):
        n = f'<span class="n">{i + 1:02d}</span>' if num else ""
        out.append(f'<details name="faq-acasa"{" open" if i == 0 else ""}><summary>{n}<span class="qq">{q}</span>{ICON}</summary>'
                   f'<div class="ans"><p>{a}</p></div></details>')
    return '<div class="acc">' + "".join(out) + "</div>"


COMMON = """
.pg{interpolate-size:allow-keywords}
.fq{padding:120px 0 128px;background:#F4EDE4}
.fq h2{font-size:clamp(44px,5vw,72px);line-height:1}
.fq .acc details{border-top:1px solid rgba(58,42,32,.18)}
.fq .acc details:last-child{border-bottom:1px solid rgba(58,42,32,.18)}
.fq summary{list-style:none;display:flex;align-items:center;gap:20px;min-height:44px;padding:26px 0;cursor:pointer;font:400 25px/1.3 var(--display);font-variation-settings:'opsz' 20;letter-spacing:-.005em;text-wrap:balance}
.fq summary::-webkit-details-marker{display:none}
.fq summary .qq{flex:1}
.fq .ic{flex:none;display:grid;place-items:center;width:40px;height:40px;border-radius:50%;border:1px solid rgba(58,42,32,.25);transition:background .25s,color .25s,border-color .25s}
.fq .ic svg{width:14px;height:14px;fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;overflow:visible}
.fq .ic .v{transform-origin:center;transition:transform .3s cubic-bezier(.2,.7,.2,1)}
.fq details[open] .ic .v{transform:scaleY(0)}
.fq summary:hover .ic{background:var(--ink);border-color:var(--ink);color:#F4EDE4}
.fq summary:focus-visible{outline:2px solid #9C472C;outline-offset:4px;border-radius:4px}
.fq .ans p{margin:0;padding:0 64px 30px 0;max-width:60ch;color:var(--ink2);text-wrap:pretty}
.fq .ans a{color:var(--ink);text-decoration:underline;text-decoration-color:rgba(58,42,32,.35);text-underline-offset:4px;transition:text-decoration-color .2s}
.fq .ans a:hover{text-decoration-color:currentColor}
.fq .ans a:focus-visible,.fq .more:focus-visible{outline:2px solid #9C472C;outline-offset:3px}
.fq details::details-content{block-size:0;overflow:clip;transition:block-size .4s cubic-bezier(.2,.7,.2,1),content-visibility .4s allow-discrete}
.fq details[open]::details-content{block-size:auto}
.fq .ask{margin:0;font:400 italic 24px/1.3 var(--display);font-variation-settings:'opsz' 20}
.fq .reply{margin:6px 0 0;font-size:15px;color:var(--ink2)}
.fq .links{display:flex;flex-wrap:wrap;gap:0 28px}
.fq .more{color:var(--ink)}
@media (max-width:820px){.fq{padding:76px 0 84px}.fq h2{font-size:clamp(40px,11vw,52px)}.fq summary{font-size:21px;padding:20px 0;gap:14px}.fq .ic{width:36px;height:36px}.fq .ans p{padding:0 0 24px}}
@media (prefers-reduced-motion:reduce){.fq details::details-content{transition:none}.fq .ic .v{transition:none}}
"""

OPTS = {}
OPTS["Faq1DouaColoane"] = ("FAQ 1: două coloane", "Framer: FAQ Pro Accordion (stilul Dividers)", """
.f1 .grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.55fr);gap:96px;align-items:start}
.f1 .l{position:sticky;top:40px}
.f1 .l h2{margin-bottom:36px}
.f1 .l .links{margin-top:18px}
.f1 .acc details:first-child{border-top:0}
.f1 .acc summary{padding-top:22px}.f1 .acc details:first-child summary{padding-top:0}
@media (max-width:820px){.f1 .grid{grid-template-columns:1fr;gap:36px}.f1 .l{position:static;display:contents}.f1 .l h2{order:-2;margin:0}.f1 .l .side{order:2}
.f1 .acc details:first-child summary{padding-top:4px}}
""", f"""<section class="fq f1" id="intrebari" aria-labelledby="fq-h"><div class="wrap grid">
<div class="l"><h2 class="disp" id="fq-h">{H}</h2><div class="side"><p class="ask">{ASK}</p><p class="reply">{REPLY}</p><div class="links">{WRITE}{ALL}</div></div></div>
{acc()}
</div></section>""")

OPTS["Faq2Centrat"] = ("FAQ 2: centrat, numerotat", "Framer: Minimal Accordion (întrebări numerotate)", """
.f2 .wrap{max-width:900px}
.f2 h2{text-align:center;margin-bottom:56px}
.f2 .n{flex:none;width:44px;font:400 italic 22px/1 var(--display);font-variation-settings:'opsz' 20;color:#9C472C;font-variant-numeric:tabular-nums}
.f2 .ans p{padding-left:64px}
.f2 .foot{display:flex;flex-direction:column;align-items:center;text-align:center;margin-top:52px}
.f2 .foot .links{justify-content:center;margin-top:8px}
@media (max-width:820px){.f2 h2{text-align:left;margin-bottom:28px}.f2 .n{width:32px;font-size:19px}.f2 .ans p{padding-left:46px}.f2 .foot{align-items:flex-start;text-align:left;margin-top:40px}.f2 .foot .links{justify-content:flex-start}}
""", f"""<section class="fq f2" id="intrebari" aria-labelledby="fq-h"><div class="wrap">
<h2 class="disp" id="fq-h">{H}</h2>
{acc(num=True)}
<div class="foot"><p class="ask">{ASK}</p><p class="reply">{REPLY}</p><div class="links">{WRITE}{ALL}</div></div>
</div></section>""")

OPTS["Faq3Carduri"] = ("FAQ 3: carduri", "Framer: FAQ Image Accordion (stilul Cards)", """
.f3{background:linear-gradient(180deg,#F4EDE4 0%,#EDE0CD 100%)}
.f3 .head{display:flex;justify-content:space-between;align-items:flex-end;gap:32px;margin-bottom:48px}
.f3 .cards{display:grid;grid-template-columns:minmax(0,1fr) 340px;gap:14px;align-items:start}
.f3 .acc{display:flex;flex-direction:column;gap:12px}
.f3 .acc details,.f3 .acc details:last-child{border:0;border-radius:22px;corner-shape:squircle;background:#FBF7F0;padding:0 30px;box-shadow:0 1px 0 rgba(58,42,32,.05);transition:box-shadow .3s,background .3s}
.f3 .acc details[open]{background:#FFFDF9;box-shadow:0 1px 0 rgba(58,42,32,.05),0 24px 48px -36px rgba(70,35,15,.45)}
.f3 .acc summary{padding:24px 0}
.f3 .other{position:sticky;top:40px;display:flex;flex-direction:column;padding:32px 30px 30px;border-radius:22px;corner-shape:squircle;background:#3A2A20;color:#F4EDE4}
.f3 .other .reply{color:#D9C7B4}
.f3 .other .links{flex-direction:column;align-items:flex-start;margin-top:14px}.f3 .other .more{margin-top:8px}
.f3 .other .more{color:#F2C79C}
@media (max-width:820px){.f3 .head{margin-bottom:28px}.f3 .cards{grid-template-columns:1fr}.f3 .acc details,.f3 .acc details:last-child{padding:0 20px}.f3 .other{position:static;padding:26px 22px 22px}}
""", f"""<section class="fq f3" id="intrebari" aria-labelledby="fq-h"><div class="wrap">
<div class="head"><h2 class="disp" id="fq-h">{H}</h2></div>
<div class="cards">{acc()}<aside class="other" aria-label="{ASK}"><p class="ask">{ASK}</p><p class="reply">{REPLY}</p><div class="links">{WRITE}{ALL}</div></aside></div>
</div></section>""")

JS = """class Component extends DCLogic {
  renderVals() { return {}; }
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
    for name, (title, src, css, html) in OPTS.items():
        for suffix, w, h in (("", 1440, 800), ("Mobil", 390, 1000)):
            f = os.path.join(P, f"{name}{suffix}.dc.html")
            open(f, "w", encoding="utf-8").write(page(title + (" · mobil" if suffix else ""), css, html, w, h))
        subprocess.run([sys.executable, os.path.join(HERE, "dc2html.py"), os.path.join(P, f"{name}.dc.html"), os.path.join(HERE, f"opt-{name}.html")], check=True)
    names = list(OPTS)
    open(os.path.join(HERE, "faq-mobil.html"), "w").write('<!doctype html><meta charset="utf-8"><title>FAQ mobil</title><style>body{margin:0;padding:10px;background:#1b1b1b;display:flex;gap:12px;color:#ddd;font:13px system-ui}figure{margin:0;flex:none}iframe{width:390px;height:1100px;border:0;display:block}</style>' + "".join(f'<figure><figcaption>{n}</figcaption><iframe src="opt-{n}.html"></iframe></figure>' for n in names))
