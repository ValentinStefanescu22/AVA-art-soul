"""Pagina „Despre noi”, part 3: Formări (studies and training). Four directions, each modelled on a real website.

usage: python3 .aidesigner/formari_options.py
writes .aidesigner/canvas/project/Formari1..4*.dc.html (+ Mobil twins) and local previews .aidesigner/opt-Formari*.html
Copy: docs/continut-site.md, „Despre noi” → „Lista de formări”. Each line is split into what / where / when; the words stay hers.
The heading „Formări” is proposed by Claude (from „Lista de formări”), to be approved.
"""
import os, subprocess, sys
from about_options2 import P, HERE, FONTS, BASE_CSS, STATIC_JS

ITEMS = [
    ("Consilier pentru dezvoltare personală", "Sandonia Institute", "2026", "cert"),
    ("Licență în Psihologie", "Universitatea Transilvania Brașov", "2026", "cap"),
    ("Masterat: Psihodiagnoză, Psihoterapie Experiențială Unificatoare și Dezvoltare Personală", "FPSE, Universitatea din București", "în curs", "book"),
    ("Ceramică", "Cursuri de specializare la Brașov", "3+ ani", "vase"),
]
ICON = {  # 24px line icons, stroke = currentColor
    "cert": '<circle cx="12" cy="9" r="5.5"></circle><path d="M8.6 13.4L7.2 21L12 18.6L16.8 21L15.4 13.4"></path>',
    "cap": '<path d="M2 9.2L12 4.5L22 9.2L12 13.9Z"></path><path d="M6 11.2V16C7.6 17.7 9.6 18.6 12 18.6S16.4 17.7 18 16V11.2"></path><path d="M22 9.2V14.5"></path>',
    "book": '<path d="M3 5.6C5.6 4.6 9 4.7 12 6.6C15 4.7 18.4 4.6 21 5.6V19C18.4 18.1 15 18.2 12 20C9 18.2 5.6 18.1 3 19Z"></path><path d="M12 6.6V20"></path>',
    "vase": '<path d="M9 3H15"></path><path d="M10 3.5C10 5.5 10.4 6.2 9.6 7.2C7 9 5.5 11.5 5.5 15C5.5 18 7.4 20.5 8.8 21.5H15.2C16.6 20.5 18.5 18 18.5 15C18.5 11.5 17 9 14.4 7.2C13.6 6.2 14 5.5 14 3.5"></path><path d="M6.4 12.4Q12 14 17.6 12.4"></path>',
}


def icon(k, cls="ic"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true"><g fill="none" stroke="currentColor" '
            f'style="stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round">{ICON[k]}</g></svg>')


H2 = '<h2 class="disp" id="fm-h">Formări</h2>'
SOURCES = {
    "Formari1LinkedIn": "linkedin.com: secțiunea „Licențe și certificări” de pe profil",
    "Formari2ReadCv": "read.cv: profilurile-CV minimaliste (anul în stânga, rândul în dreapta)",
    "Formari3Airbnb": "airbnb.com: profilul gazdei, fapte scurte cu iconițe",
    "Formari4Wallet": "apple.com/wallet: cardurile și biletele din Apple Wallet",
}
COMMON = """
.fm{position:relative;overflow:hidden}
.fm h2{font-size:clamp(40px,4.2vw,60px);line-height:1.05}
.fm .yr{font-variant-numeric:tabular-nums}
"""
OPTS = {}

# 1. LinkedIn: one card, one row per credential: a tile with an icon (instead of a school logo), title, where, when.
OPTS["Formari1LinkedIn"] = ("Formări 1: listă cu iconițe", """
.fl{background:#F4EDE4;padding:112px 0 120px}
.fl .stage{display:grid;grid-template-columns:minmax(0,4fr) minmax(0,8fr);gap:0 72px;align-items:start}
.fl .card{margin:0;padding:6px 36px;list-style:none;background:#FBF7F0;border-radius:28px;corner-shape:squircle;box-shadow:0 1px 0 rgba(58,42,32,.05),0 24px 48px -32px rgba(58,42,32,.35)}
.fl li{display:grid;grid-template-columns:56px minmax(0,1fr);gap:0 22px;padding:28px 0}
.fl li+li{border-top:1px solid rgba(58,42,32,.12)}
.fl .tile{display:grid;place-items:center;width:56px;height:56px;border-radius:16px;corner-shape:squircle;background:#EADBC6;color:var(--ink)}
.fl .ic{width:26px;height:26px}
.fl .t{margin:4px 0 0;font:600 18px/1.4 var(--text);text-wrap:pretty}
.fl .w{margin:4px 0 0;color:var(--ink2);font-size:16px}
.fl .yr{display:block;margin-top:2px;color:var(--ink2);font-size:14.5px}
@media (max-width:980px){.fl{padding:72px 0 80px}.fl .stage{grid-template-columns:1fr;gap:28px}.fl .card{padding:2px 20px;border-radius:22px}.fl li{grid-template-columns:48px minmax(0,1fr);gap:0 16px;padding:22px 0}.fl .tile{width:48px;height:48px;border-radius:14px}.fl .ic{width:22px;height:22px}.fl .t{font-size:17px}}
""", '<section class="fm fl" aria-labelledby="fm-h"><div class="wrap stage">' + H2 + '<ul class="card">'
   + "".join(f'<li><span class="tile">{icon(k)}</span><div><p class="t">{t}</p><p class="w">{w}</p><span class="yr">{d}</span></div></li>' for t, w, d, k in ITEMS)
   + "</ul></div></section>")

# 2. read.cv: pure typography. The year sits in its own narrow column, the line to its right; no boxes, no icons.
OPTS["Formari2ReadCv"] = ("Formări 2: CV minimalist", """
.fr{background:#F4EDE4;padding:112px 0 120px}
.fr .stage{display:grid;grid-template-columns:minmax(0,4fr) minmax(0,8fr);gap:0 72px}
.fr ol{margin:0;padding:0;list-style:none}
.fr li{display:grid;grid-template-columns:120px minmax(0,1fr);gap:0 32px;padding:0 0 34px}
.fr .yr{padding-top:3px;color:var(--ink2);font-size:15.5px}
.fr .t{margin:0;font:500 19px/1.45 var(--text);color:var(--ink);text-wrap:pretty}
.fr .w{margin:4px 0 0;color:var(--ink2);font-size:16.5px}
@media (max-width:980px){.fr{padding:72px 0 64px}.fr .stage{grid-template-columns:1fr;gap:32px}.fr li{grid-template-columns:1fr;gap:4px;padding-bottom:28px}.fr .yr{padding:0;font-size:14.5px}.fr .t{font-size:18px}}
""", '<section class="fm fr" aria-labelledby="fm-h"><div class="wrap stage">' + H2 + "<ol>"
   + "".join(f'<li><span class="yr">{d}</span><div><p class="t">{t}</p><p class="w">{w}</p></div></li>' for t, w, d, k in ITEMS)
   + "</ol></div></section>")

# 3. Airbnb host profile: short facts in a two-column grid, each led by a line icon; warm, conversational, no table.
OPTS["Formari3Airbnb"] = ("Formări 3: fapte cu iconițe", """
.fa{background:linear-gradient(180deg,#F4EDE4 0%,#EDE0CD 100%);padding:112px 0 120px}
.fa h2{margin-bottom:48px}
.fa ul{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:44px 72px;margin:0;padding:0;list-style:none}
.fa li{display:grid;grid-template-columns:32px minmax(0,1fr);gap:0 20px;align-items:start}
.fa .ic{width:32px;height:32px;color:var(--terra-d)}
.fa .t{margin:2px 0 0;font:400 22px/1.35 var(--display);font-variation-settings:'opsz' 20;color:var(--ink);text-wrap:pretty}
.fa .w{margin:8px 0 0;color:var(--ink2);font-size:16.5px}
.fa .w .yr{white-space:nowrap}.fa .w .yr::before{content:"·";margin:0 8px}
@media (max-width:980px){.fa{padding:72px 0 80px}.fa h2{margin-bottom:32px}.fa ul{grid-template-columns:1fr;gap:30px}.fa li{grid-template-columns:28px minmax(0,1fr);gap:0 16px}.fa .ic{width:28px;height:28px}.fa .t{font-size:20px}}
""", '<section class="fm fa" aria-labelledby="fm-h"><div class="wrap">' + H2 + "<ul>"
   + "".join(f'<li>{icon(k)}<div><p class="t">{t}</p><p class="w">{w}<span class="yr">{d}</span></p></div></li>' for t, w, d, k in ITEMS)
   + "</ul></div></section>")

# 4. Wallet (see formari_wallet.py): each credential is a pass in the brand's colours, fanned like a hand of cards; hovering one lifts and
#    straightens it (mouse only). Phone: a row that swipes sideways, one pass at a time.
CARD = [("#3A2A20", "#F4EDE4"), ("#9C472C", "#F7EDE2"), ("#4F5A43", "#F1EFE6"), ("#E6D5BD", "#3A2A20")]
ROT = [-4, 2, -2, 4]
# Formari4Wallet moved to formari_wallet.py (Vali chose it, 11 nov; it grew into a family of four).


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
{STATIC_JS}
</script>
</body>
</html>
"""


# preview heights, measured in the browser (desktop 1440, phone 390)
H = {"Formari1LinkedIn": (832, 831), "Formari2ReadCv": (628, 709), "Formari3Airbnb": (580, 731)}

if __name__ == "__main__":
    for name, (title, css, html) in OPTS.items():
        for suffix, w, h in (("", 1440, H[name][0]), ("Mobil", 390, H[name][1])):
            f = os.path.join(P, f"{name}{suffix}.dc.html")
            open(f, "w", encoding="utf-8").write(page(name, title + (" · mobil" if suffix else ""), css, html, w, h))
            if not suffix:
                subprocess.run([sys.executable, os.path.join(HERE, "dc2html.py"), f, os.path.join(HERE, f"opt-{name}.html")], check=True, capture_output=True)
        print("wrote", name)
    names = list(OPTS)
    open(os.path.join(HERE, "formari-mobil.html"), "w").write('<!doctype html><meta charset="utf-8"><title>Formari mobil</title><style>body{margin:0;padding:10px;background:#1b1b1b;display:flex;gap:12px;color:#ddd;font:13px system-ui}figure{margin:0}iframe{width:390px;height:1300px;border:0;display:block}</style>' + "".join(f'<figure><figcaption>{n}</figcaption><iframe src="opt-{n}.html"></iframe></figure>' for n in names))
