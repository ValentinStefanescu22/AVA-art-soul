"""Fonturi pentru text (Vali, 13 nov): one canvas page to compare body fonts next to the Bodoni Moda titles.
  FonturiComparator   the same piece of the site (Povestea, a ticket, an FAQ row, a form field); pick a font, it all changes.
  FonturiToate        every font at once, one card each, the same sample.
Fonts: the current one (Hanken Grotesk), the 9 from Vali's list, and 8 I propose that don't read as template defaults.
All have the latin-ext subset (ș, ț with the comma), checked against Google Fonts on 13 nov. Liter has one weight only.
The sample text is the site's own (Povestea, the FAQ, the December workshop). The notes on each font are mine.

usage: python3 .aidesigner/fonturi_text.py
"""
import os, subprocess, sys
from about_options2 import P, HERE

# (name, css family, google query, group, note)
FONTS = [
    ("Hanken Grotesk", "'Hanken Grotesk'", "Hanken+Grotesk:wght@400;500;600", "acum",
     "Cel de acum (ales pe 5 nov): grotesc cald, cu forme rotunde."),
    ("Liter", "'Liter'", "Liter", "lista",
     "Curat și puțin rece. Are o singură greutate: aldinele și butoanele ar fi îngroșate fals."),
    ("Bricolage Grotesque", "'Bricolage Grotesque'", "Bricolage+Grotesque:wght@400;500;600", "lista",
     "Multă personalitate, făcut mai ales pentru titluri; în text lung obosește."),
    ("Geist", "'Geist'", "Geist:wght@400;500;600", "lista",
     "Fontul de interfață al Vercel: precis, foarte „tech”."),
    ("Chivo", "'Chivo'", "Chivo:wght@400;500;600", "lista",
     "Grotesc solid, puțin industrial."),
    ("Instrument Sans", "'Instrument Sans'", "Instrument+Sans:wght@400;500;600", "lista",
     "Curat, cu puțină căldură; din lista ta, cel mai potrivit."),
    ("Newsreader", "'Newsreader'", "Newsreader:wght@400;500;600", "lista",
     "Serif de lectură; lângă Bodoni sunt două fonturi cu serife."),
    ("Trirong", "'Trirong'", "Trirong:wght@400;500;600", "lista",
     "Serif cu contrast, desenat pentru thailandeză și latină."),
    ("Barlow Condensed", "'Barlow Condensed'", "Barlow+Condensed:wght@400;500;600", "lista",
     "Îngust, pentru titluri scurte, nu pentru paragrafe."),
    ("Inter", "'Inter'", "Inter:wght@400;500;600", "lista",
     "Standardul interfețelor; îl vezi pe mii de site-uri și aplicații."),
    ("Jost", "'Jost'", "Jost:wght@400;500;600", "propus",
     "Era în PDF-ul de identitate AVA. Geometric, în stilul Futura: Bodoni + Futura e perechea clasică a revistelor de modă."),
    ("Albert Sans", "'Albert Sans'", "Albert+Sans:wght@400;500;600", "propus",
     "Geometric, inspirat de designul scandinav: cald și aerisit."),
    ("Familjen Grotesk", "'Familjen Grotesk'", "Familjen+Grotesk:wght@400;500;600", "propus",
     "Grotesc cu mici ciudățenii în forme (g, a, y): are personalitate fără să strige."),
    ("Schibsted Grotesk", "'Schibsted Grotesk'", "Schibsted+Grotesk:wght@400;500;600", "propus",
     "Făcut pentru un grup de presă norvegian: solid, ușor de citit în text lung."),
    ("Red Hat Text", "'Red Hat Text'", "Red+Hat+Text:wght@400;500;600", "propus",
     "Varianta pentru text a fontului Red Hat, desenată pentru paragrafe: deschisă, prietenoasă."),
    ("Atkinson Hyperlegible Next", "'Atkinson Hyperlegible Next'", "Atkinson+Hyperlegible+Next:wght@400;500;600", "propus",
     "Desenat de Braille Institute pentru cititori cu vedere slabă: fiecare literă se deosebește clar."),
    ("Karla", "'Karla'", "Karla:wght@400;500;600", "propus",
     "Grotesc puțin excentric, cald, cu caracter."),
    ("Literata", "'Literata'", "Literata:wght@400;500;600", "propus",
     "Serif de carte (fontul Google Play Books), dacă vrei textul lung să se citească „ca într-o carte”."),
]
GROUPS = [("acum", "Acum"), ("lista", "Din lista ta"), ("propus", "Propuse de mine")]

LINKS = "\n".join(f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family={q}&amp;display=swap">' for _, _, q, _, _ in FONTS)
LINKS = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400..900;1,6..96,400..900&amp;display=swap">\n'
         + LINKS)

# the site's own copy
POV_Q = "Cum ai ajuns la lut și ce simțeai când lucrai cu el?"
POV_A = ("În primul an de facultate am simțit nevoia de o activitate care să mă ajute să mă reconectez cu latura mea creativă și ludică, "
         "pe care am reprimat-o din ce în ce mai mult pe măsură ce creșteam. <b>Așa am ajuns la lut, fără să știu cât de mult avea să-mi schimbe drumul.</b> "
         "Lucrând cu el, simțeam liniște și curiozitate, iar acum este modalitatea care mă ajută să mă apropii mai mult de copilul meu interior.")
EV_T, EV_M = "Atelier de ceramică &amp; socializare", "duminică, 6 decembrie · ora 17:00 · Cotroceni, sector 5 · 200 lei"
FQ_Q, FQ_A = "Trebuie să știu să lucrez cu lutul?", "Deloc. Majoritatea celor care vin la atelierele mele ating lutul pentru prima dată. Te ghidez pas cu pas."
DIA = "ș ț ă â î · Ș Ț Ă Â Î · 0123456789 · 180 lei / oră"

CSS = """
body{margin:0;background:#F4EDE4}
.pg{--ink:#3A2A20;--ink2:#6B5444;--body:#4A382C;--terra-d:#9C472C;--display:'Bodoni Moda',Georgia,serif;--f:'Hanken Grotesk';
  background:#F4EDE4;color:var(--ink);font:400 17px/1.6 var(--f),system-ui,sans-serif;-webkit-font-smoothing:antialiased;overflow-x:clip}
.pg *{box-sizing:border-box}
.wrap{max-width:1240px;margin:0 auto;padding:0 40px}
.disp{margin:0;font-family:var(--display);font-weight:400;font-variation-settings:'opsz' 20;letter-spacing:-.012em;text-wrap:balance}
.top{padding-top:96px;padding-bottom:40px}
.pg a{color:inherit;text-decoration:none}
.top h1{font-size:clamp(44px,5vw,72px);line-height:1.05}
.top p{margin:16px 0 0;max-width:62ch;color:var(--body);font-family:'Hanken Grotesk',system-ui,sans-serif}
.pg .btn{color:#F8F1E8}
.btn{display:inline-flex;align-items:center;justify-content:center;min-height:48px;padding:0 26px;border-radius:999px;background:#9C472C;color:#F8F1E8;font:500 15px/1 var(--f),sans-serif;letter-spacing:.02em}
.meta{font-size:14px;color:#833A22;font-variant-numeric:tabular-nums}
.dia{font-size:15px;color:var(--ink2);letter-spacing:.02em}
@media (max-width:820px){.wrap{padding:0 20px}.top{padding-top:64px;padding-bottom:28px}.btn{width:100%}}
/* comparator: the section's own font-family follows --f, so its text inherits the picked font */
.cmp{font-family:var(--f),system-ui,sans-serif}
.cmp .bar{position:sticky;top:0;z-index:2;padding:14px 0;background:rgba(244,237,228,.94);backdrop-filter:blur(8px);border-bottom:1px solid rgba(58,42,32,.12)}
.cmp .grp{display:flex;align-items:center;flex-wrap:wrap;gap:6px 8px}
.cmp .grp+.grp{margin-top:8px}
.cmp .gl{min-width:118px;font:400 italic 16px/1 var(--display);color:var(--terra-d)}
.cmp .pick{min-height:40px;padding:0 14px;border:0;border-radius:999px;background:#E9DCCA;color:#3A2A20;font-size:15px;cursor:pointer;transition:background-color .2s,color .2s}
.cmp .pick:hover{background:#E0D0BB}
.cmp .pick[aria-pressed="true"]{background:#3A2A20;color:#F4EDE4}
.cmp .pick:focus-visible{outline:2px solid #9C472C;outline-offset:2px}
.cmp .now{display:flex;align-items:baseline;justify-content:space-between;flex-wrap:wrap;gap:8px 24px;padding:40px 0 8px}
.cmp .now b{font:500 30px/1.2 var(--f),sans-serif}
.cmp .now span{max-width:60ch;font:400 italic 18px/1.4 var(--display);color:var(--ink2)}
.cmp .stage{display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:56px;padding:40px 0 112px;border-top:1px solid rgba(58,42,32,.14)}
.cmp h2{font-size:clamp(40px,4.4vw,60px);line-height:1.05}
.cmp h3{margin:28px 0 14px;font:400 italic 30px/1.25 var(--display);color:var(--terra-d)}
.cmp .read p{margin:0;font-size:19px;line-height:1.75;color:var(--body);text-wrap:pretty}
.cmp .read b{font-weight:600;color:var(--ink)}
.cmp .side{display:flex;flex-direction:column;gap:16px}
.cmp .tk{padding:24px 26px;border-radius:20px;background:#FBF7F1;box-shadow:0 0 0 1px rgba(58,42,32,.06)}
.cmp .tk h4{margin:6px 0 16px;font:400 26px/1.15 var(--display);font-variation-settings:'opsz' 20}
.cmp .fq{padding:20px 24px;border-radius:20px;background:#FBF7F1;box-shadow:0 0 0 1px rgba(58,42,32,.06)}
.cmp .fq p{margin:0}.cmp .fq .q{font:400 22px/1.3 var(--display)}.cmp .fq .a{margin-top:8px;font-size:16.5px;line-height:1.65;color:var(--body)}
.cmp .fi{display:flex;flex-direction:column;gap:6px;font-size:14px;font-weight:500}
.cmp .fi span.in{display:flex;align-items:center;min-height:48px;padding:0 16px;border-radius:12px;background:#FFFDF9;box-shadow:inset 0 0 0 1px rgba(58,42,32,.18);font-weight:400;font-size:16px;color:var(--ink2)}
.cmp .pills{display:flex;flex-wrap:wrap;gap:8px;margin:0;padding:0;list-style:none}
.cmp .pills li{display:inline-flex;align-items:center;min-height:36px;padding:0 14px;border-radius:999px;background:#E9DCCA;font-size:14px}
@media (max-width:980px){.cmp .stage{grid-template-columns:minmax(0,1fr);gap:32px;padding:28px 0 72px}
  .cmp .grp{flex-wrap:nowrap;overflow-x:auto;margin:0 -20px;padding:0 20px;scrollbar-width:none}.cmp .gl{min-width:auto;white-space:nowrap}.cmp .pick{white-space:nowrap}
  .cmp .read p{font-size:18px}.cmp .now b{font-size:24px}}
/* all at once */
.all .gh{margin:56px 0 18px;font:400 italic 26px/1.2 var(--display);color:var(--terra-d)}
.all .gh:first-of-type{margin-top:0}
.all .cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
.all .card{display:flex;flex-direction:column;gap:14px;padding:26px 26px 28px;border-radius:22px;background:#FBF7F1;box-shadow:0 0 0 1px rgba(58,42,32,.06);font-family:var(--f),sans-serif}
.all .card.cur{box-shadow:inset 0 0 0 2px #3A2A20}
.all .nm{display:flex;align-items:baseline;justify-content:space-between;gap:12px;padding-bottom:12px;border-bottom:1px solid rgba(58,42,32,.12)}
.all .nm b{font-size:22px;font-weight:500;line-height:1.2}
.all .nm small{flex:none;font:400 italic 14px/1 var(--display);color:var(--terra-d)}
.all .note{margin:0;font:400 italic 15.5px/1.45 var(--display);color:var(--ink2)}
.all h4{margin:4px 0 0;font:400 26px/1.15 var(--display);font-variation-settings:'opsz' 20}
.all .card p.t{margin:0;font-size:17px;line-height:1.65;color:var(--body)}
.all .card .row{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-top:auto;padding-top:6px}
.all .card .btn{min-height:44px;padding:0 20px}
.all{padding-bottom:112px}
@media (max-width:980px){.all .cards{grid-template-columns:minmax(0,1fr)}.all{padding-bottom:72px}.all .card .btn{width:auto}}
"""


COMP_HTML = ('<section class="cmp" ref="{{ secRef }}" style="--f: \'Hanken Grotesk\'">'
             '<div class="wrap top"><h1 class="disp">Fonturi pentru text</h1>'
             '<p>Aceeași bucată din site, cu titlurile în Bodoni Moda. Alege un font de mai jos și se schimbă tot textul de sub titluri: '
             'paragraful lung, biletul, întrebarea, butonul, câmpul de formular.</p></div>'
             '<div class="bar"><div class="wrap">'
             + "".join(f'<div class="grp" role="group" aria-label="{gn}"><span class="gl">{gn}</span>'
                       + "".join(f'<button type="button" class="pick" data-i="{i}" aria-pressed="{"true" if i == 0 else "false"}" onClick="{{{{ pick }}}}" style="font-family: {fam}, sans-serif">{n}</button>'
                                 for i, (n, fam, _, g, _) in enumerate(FONTS) if g == gk) + "</div>" for gk, gn in GROUPS)
             + '</div></div><div class="wrap"><div class="now" aria-live="polite"><b class="fn">Hanken Grotesk</b><span class="fnote">' + FONTS[0][4] + '</span></div>'
             f'<div class="stage"><div class="read"><h2 class="disp">Povestea</h2><h3>{POV_Q}</h3><p>{POV_A}</p></div>'
             f'<div class="side"><div class="tk"><span class="meta">{EV_M}</span><h4>{EV_T}</h4><a class="btn" href="#fonturi">Mă înscriu</a></div>'
             f'<div class="fq"><p class="q">{FQ_Q}</p><p class="a">{FQ_A}</p></div>'
             '<ul class="pills"><li>60–90 de minute</li><li>online sau față în față</li><li>180 lei / oră</li></ul>'
             '<label class="fi">Email<span class="in">nume@exemplu.ro</span></label>'
             f'<p class="dia" style="margin:0">{DIA}</p></div></div></div></section>')

ALL_HTML = ('<section class="all"><div class="wrap top"><h1 class="disp">Toate odată</h1>'
            '<p>Aceeași mostră în fiecare font, cu titlul în Bodoni Moda. Notele de sub nume sunt părerea mea.</p></div><div class="wrap">'
            + "".join(f'<h2 class="gh">{gn}</h2><div class="cards">'
                      + "".join(f'<article class="card{" cur" if g == "acum" else ""}" style="--f: {fam}"><div class="nm"><b>{n}</b><small>{"acum" if g == "acum" else ""}</small></div>'
                                f'<p class="note">{note}</p><span class="meta">{EV_M}</span><h4>{EV_T}</h4><p class="t">{FQ_A}</p>'
                                f'<div class="row"><span class="dia">{DIA}</span><a class="btn" href="#fonturi">Mă înscriu</a></div></article>'
                                for n, fam, _, g, note in FONTS if g == gk) + "</div>" for gk, gn in GROUPS)
            + "</div></section>")

NOTES = __import__("json").dumps([[n, fam, note] for n, fam, _, _, note in FONTS], ensure_ascii=False)
SCRIPT_CMP = ("var FONTS = " + NOTES + ";\nclass Component extends DCLogic {\n"
              "  renderVals() { var self = this; if (!this.cb) this.cb = {\n"
              "    secRef: function (el) { self.sec = el; },\n"
              "    pick: function (e) { var b = e.currentTarget, s = self.sec, i = +b.getAttribute('data-i');\n"
              "      s.querySelectorAll('.pick').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });\n"
              "      s.style.setProperty('--f', FONTS[i][1]); s.querySelector('.fn').textContent = FONTS[i][0]; s.querySelector('.fnote').textContent = FONTS[i][2]; }\n"
              "  }; return this.cb; }\n}")
SCRIPT_ALL = "class Component extends DCLogic {\n  renderVals() { return {}; }\n}"


def page(title, html, script, w, h):
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
{LINKS}
<style>{CSS}</style>
</helmet>
<div class="pg">
{html}
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{w},"height":{h}}}}}'>
{script}
</script>
</body>
</html>
"""


H = {"FonturiComparator": (1218, 1907), "FonturiToate": (4198, 9975)}
BOARDS = {"FonturiComparator": ("Fonturi pentru text: comparator", COMP_HTML, SCRIPT_CMP),
          "FonturiToate": ("Fonturi pentru text: toate odată", ALL_HTML, SCRIPT_ALL)}

if __name__ == "__main__":
    for name, (title, html, script) in BOARDS.items():
        for suffix, w, h in (("", 1440, H[name][0]), ("Mobil", 390, H[name][1])):
            f = os.path.join(P, f"{name}{suffix}.dc.html")
            open(f, "w", encoding="utf-8").write(page(title + (" · mobil" if suffix else ""), html, script, w, h))
            if not suffix:
                subprocess.run([sys.executable, os.path.join(HERE, "dc2html.py"), f, os.path.join(HERE, f"opt-{name}.html")], check=True, capture_output=True)
        print("wrote", name)
