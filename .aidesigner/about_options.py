"""Generate the 'Cine sunt, pe scurt' (About) section options as canvas artboards.

usage: python3 .aidesigner/about_options.py   (writes .aidesigner/canvas/project/Despre*.dc.html)
Each artboard = the bottom edge of the chosen hero (for context) + one design of the About section.
Copy is from docs/continut-site.md (Pagina Acasă, block 2; Despre noi bio and credentials).
"""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "canvas", "project")
src = open(os.path.join(P, "Acasa.dc.html"), encoding="utf-8").read()
FONTS = re.search(r'<link rel="stylesheet" href="https://fonts.googleapis.com/css2\?[^"]*">', src).group(0)

BG = "/_blob/a36432dd59596088ec01e9f25409bd5d"        # hero clay
STAMP_PHOTO = "/_blob/61696ece195f787b8ccb139b396a6450"  # alessia-stamp.webp (square, face centred)
CUTOUT = "/_blob/eea66386c5e507e37343fcb18e98611a"       # alessia.webp (transparent cut-out)
ATELIER = "/_blob/988e3a505fd5ae1db56d481b3d1e33b1"      # workshop photo

ARROW = '<svg class="ar" viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8H13M9 4L13 8L9 12" fill="none" stroke="currentColor" style="stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round"></path></svg>'
LEAD = "Sunt Alessia și cred că mâinile știu uneori lucruri pe care mintea încă nu le-a spus."
BODY = "Fac ateliere în care lutul e doar începutul: restul e despre tine, despre ce simți și despre oamenii cu care împarți masa."
ROLE = "Artist ceramist și consilier acreditat în dezvoltare personală"
CREDS = [
    ("Consilier pentru dezvoltare personală", "curs acreditat Sandonia Institute, 2026"),
    ("Licență în Psihologie", "Universitatea Transilvania Brașov, 2026"),
    ("Masterat în curs", "FPSE, Universitatea din București"),
    ("Ceramică", "3+ ani de experiență, cursuri de specializare la Brașov"),
]
LINK = f'<a class="more" href="#povestea">Povestea mea {ARROW}</a>'


def ring(id_, r, size, text, cls="ring-t", fit=False):
    c = size / 2
    tl = f' textLength="{2 * 3.14159 * r - 4:.1f}" lengthAdjust="spacing"' if fit else ""  # fit: text fills the circle exactly
    return (f'<svg class="spin" viewBox="0 0 {size} {size}" aria-hidden="true"><defs><path id="{id_}" d="M{c} {c}m-{r} 0a{r} {r} 0 1 1 {2*r} 0a{r} {r} 0 1 1 -{2*r} 0"></path></defs>'
            f'<text class="{cls}"><textPath href="#{id_}"{tl}>{text}</textPath></text></svg>')


RING_TXT = "AVA · ART &amp; SOUL · AUTOCUNOAȘTERE PRIN CREAȚIE · AVA · ART &amp; SOUL · AUTOCUNOAȘTERE PRIN CREAȚIE ·"

BASE_CSS = f"""body{{margin:0;background:#F4EDE4}}
.pg{{--ink:#3A2A20;--ink2:#6B5444;--paper:#F4EDE4;--sand:#E6D5BD;--terra-d:#9C472C;--clay:#C07A4E;--display:'Bodoni Moda',Georgia,serif;--text:'Literata',Georgia,serif;--script:'Pinyon Script',cursive;background:var(--paper);color:var(--ink);font:400 17px/1.6 var(--text);-webkit-font-smoothing:antialiased;overflow-x:clip}}
.pg a{{color:inherit}}
.pg a:focus-visible{{outline:2px solid var(--terra-d);outline-offset:4px;border-radius:4px}}
.disp{{font-family:var(--display);font-weight:400;font-variation-settings:'opsz' 20;letter-spacing:-.01em;text-wrap:balance}}
.ar{{width:16px;height:16px;flex:none;transition:transform .3s cubic-bezier(.2,.7,.2,1)}}
/* the bottom of the hero, for context */
.heroend{{position:relative;height:120px;background:#8A4A30 url({BG}) center 85%/cover no-repeat}}
.heroend::before{{content:"";position:absolute;inset:0;background:rgba(42,20,12,.45)}}
.heroend svg{{position:absolute;left:0;right:0;bottom:-1px;width:100%;height:120px}}
.sec{{padding:96px 0 120px}}
.wrap{{max-width:1240px;margin:0 auto;padding:0 40px;box-sizing:border-box}}
.kicker{{display:flex;align-items:center;gap:14px;margin:0;font:500 12px/1 var(--text);letter-spacing:.24em;text-transform:uppercase;color:var(--terra-d)}}
.kicker::before{{content:"";width:34px;height:1px;background:currentColor}}
.lead{{margin:22px 0 0;font-size:clamp(30px,2.9vw,42px);line-height:1.25}}
.body{{margin:22px 0 0;max-width:50ch;color:var(--ink2);text-wrap:pretty}}
.more{{display:inline-flex;align-items:center;gap:10px;min-height:44px;margin-top:22px;font-weight:500;text-decoration:none;background:linear-gradient(currentColor,currentColor) 0 calc(100% - 9px)/100% 1px no-repeat;transition:background-size .3s cubic-bezier(.2,.7,.2,1)}}
.more:hover{{background-size:0 1px;background-position:100% calc(100% - 9px)}}
.more:hover .ar{{transform:translateX(4px)}}
.spin{{animation:spin 80s linear infinite}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
.ring-t{{font:500 12.5px var(--text);letter-spacing:.34em;fill:var(--ink)}}
@media (max-width:820px){{.wrap{{padding:0 20px}}.sec{{padding:64px 0 84px}}.heroend{{height:72px}}.heroend svg{{height:72px}}}}
@media (prefers-reduced-motion:reduce){{.spin{{animation:none}}.pg *{{transition:none!important}}}}
"""
HERO_END = '<div class="heroend" aria-hidden="true"><svg viewBox="0 0 1440 120" preserveAspectRatio="none"><path d="M0 86C240 62 480 62 720 86C960 110 1200 110 1440 86L1440 120L0 120Z" style="fill:#F4EDE4"></path></svg></div>'

OPTS = {}

# 1. refined stamp with portrait
OPTS["Despre1Stampila"] = ("Despre 1: ștampila cu portret", f"""
.grid{{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:96px;align-items:center}}
.seal{{position:relative;width:100%;max-width:440px;aspect-ratio:1;justify-self:center;margin:0}}
.seal .spin{{position:absolute;inset:0;width:100%;height:100%}}
.seal::before{{content:"";position:absolute;inset:3%;border-radius:50%;box-shadow:inset 0 0 0 1px rgba(58,42,32,.22)}}
.seal .ph{{position:absolute;inset:15%;border-radius:50%;overflow:hidden;background:radial-gradient(circle at 50% 30%,#EFE1CC,#DCC2A0 55%,#C9A47E);box-shadow:0 30px 60px -30px rgba(58,42,32,.45),inset 0 0 0 1px rgba(58,42,32,.25)}}
.seal img{{width:100%;height:100%;object-fit:cover}}
.creds{{margin:34px 0 0;padding:0;list-style:none;border-top:1px solid rgba(58,42,32,.16)}}
.creds li{{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.2fr);gap:24px;padding:14px 0;border-bottom:1px solid rgba(58,42,32,.16);font-size:15px}}
.creds b{{font-weight:500}}
.creds span{{color:var(--ink2)}}
@media (max-width:820px){{.grid{{grid-template-columns:1fr;gap:44px}}.seal{{max-width:300px}}.creds li{{grid-template-columns:1fr;gap:2px}}}}
""", f"""<div class="wrap grid">
<figure class="seal">{ring('r1', 196, 440, RING_TXT)}<div class="ph"><img src="{STAMP_PHOTO}" alt="Alessia Văideanu, fondatoarea AVA Art &amp; Soul"></div></figure>
<div>
<p class="kicker">Despre noi</p>
<h2 class="lead disp">{LEAD}</h2>
<p class="body">{BODY}</p>
<ul class="creds">{''.join(f'<li><b>{a}</b><span>{b}</span></li>' for a, b in CREDS)}</ul>
{LINK}
</div>
</div>""")

# 2. editorial quote
OPTS["Despre2Citat"] = ("Despre 2: citat editorial", f"""
.q{{max-width:980px;margin:0 auto;text-align:center;display:flex;flex-direction:column;align-items:center}}
.mark{{display:block;height:64px;font:400 120px/1 var(--script);color:var(--clay)}}
.q .lead{{margin-top:6px;font-size:clamp(34px,3.9vw,56px);line-height:1.18;letter-spacing:-.015em}}
.sig{{display:flex;align-items:center;gap:18px;margin-top:40px;text-align:left}}
.av{{position:relative;width:84px;height:84px;flex:none}}
.av img{{width:100%;height:100%;border-radius:50%;object-fit:cover;background:#DCC2A0}}
.av::after{{content:"";position:absolute;inset:-6px;border-radius:50%;box-shadow:inset 0 0 0 1px rgba(58,42,32,.28)}}
.sig .n{{display:block;font:400 44px/1 var(--script);color:var(--ink)}}
.sig .r{{display:block;margin-top:6px;font:500 12px/1.4 var(--text);letter-spacing:.16em;text-transform:uppercase;color:var(--ink2)}}
.q .body{{margin:34px auto 0;max-width:56ch;font-size:18px}}
.rule{{width:1px;height:48px;margin:30px auto 0;background:rgba(58,42,32,.25)}}
@media (max-width:820px){{.sig{{flex-direction:column;text-align:center}}}}
""", f"""<div class="wrap q">
<span class="mark" aria-hidden="true">“</span>
<h2 class="lead disp">{LEAD}</h2>
<div class="sig"><span class="av"><img src="{STAMP_PHOTO}" alt="Alessia Văideanu"></span><span><span class="n">Alessia</span><span class="r">{ROLE}</span></span></div>
<span class="rule" aria-hidden="true"></span>
<p class="body">{BODY}</p>
{LINK}
</div>""")

# 3. cut-out portrait in a clay arch
OPTS["Despre3Arcada"] = ("Despre 3: portret în arcadă", f"""
.grid{{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:96px;align-items:center}}
.arch{{position:relative;width:100%;max-width:420px;aspect-ratio:3/4;justify-self:center;margin:0}}
.arch .in{{position:absolute;inset:0;border-radius:999px 999px 28px 28px;corner-shape:squircle;overflow:hidden;background:radial-gradient(120% 90% at 50% 20%,#D49A6E 0%,#B9744A 45%,#8A4A30 100%);box-shadow:0 40px 70px -40px rgba(58,42,32,.6)}}
.arch .in::before{{content:"";position:absolute;inset:0;background:url({BG}) center/cover;mix-blend-mode:soft-light;opacity:.6}}
.arch img{{position:absolute;left:50%;bottom:0;width:112%;margin-left:-56%;height:auto}}
.arch .line{{position:absolute;inset:-14px;border-radius:999px 999px 38px 38px;box-shadow:inset 0 0 0 1px rgba(58,42,32,.22);pointer-events:none}}
.badge{{position:absolute;right:-34px;top:38%;width:128px;height:128px;border-radius:50%;background:var(--paper);box-shadow:0 14px 30px -16px rgba(58,42,32,.45)}}
.badge .spin{{position:absolute;inset:8px;width:calc(100% - 16px);height:calc(100% - 16px)}}
.badge .ring-t{{font-size:9.5px;letter-spacing:.1em}}
.badge .v{{position:absolute;left:50%;top:50%;width:24px;height:30px;margin:-15px 0 0 -12px;color:var(--terra-d)}}
.cgrid{{display:grid;grid-template-columns:1fr 1fr;margin:34px 0 0;padding:0;list-style:none;border-top:1px solid rgba(58,42,32,.16);border-left:1px solid rgba(58,42,32,.16)}}
.cgrid li{{padding:16px 18px;border-right:1px solid rgba(58,42,32,.16);border-bottom:1px solid rgba(58,42,32,.16);font-size:14.5px;line-height:1.45}}
.cgrid b{{display:block;font:400 19px/1.2 var(--display);font-variation-settings:'opsz' 20;margin-bottom:4px}}
.cgrid span{{color:var(--ink2)}}
@media (max-width:820px){{.grid{{grid-template-columns:1fr;gap:56px}}.arch{{max-width:300px}}.badge{{right:-18px;width:104px;height:104px}}.cgrid{{grid-template-columns:1fr}}}}
""", f"""<div class="wrap grid">
<figure class="arch"><span class="line" aria-hidden="true"></span><div class="in"><img src="{CUTOUT}" alt="Alessia Văideanu, fondatoarea AVA Art &amp; Soul"></div>
<span class="badge" aria-hidden="true">{ring('r3', 46, 112, 'AVA · ART &amp; SOUL · AVA · ART &amp; SOUL ·', fit=True)}<svg class="v" viewBox="0 0 64 80"><g fill="none" stroke="currentColor" style="stroke-linecap:round;stroke-linejoin:round"><path d="M22 6H42" style="stroke-width:5"></path><path d="M26 7C26 13 27 15 25 18C17 24 12 31 12 43C12 55 19 64 24 72H40C45 64 52 55 52 43C52 31 47 24 39 18C37 15 38 13 38 7" style="stroke-width:3.6"></path><path d="M14.5 35Q32 40 49.5 35M12.6 48Q32 53 51.4 48" style="stroke-width:3.2"></path></g></svg></span></figure>
<div>
<p class="kicker">Despre noi</p>
<h2 class="lead disp">{LEAD}</h2>
<p class="body">{BODY}</p>
<ul class="cgrid">{''.join(f'<li><b>{a}</b><span>{b}</span></li>' for a, b in CREDS)}</ul>
{LINK}
</div>
</div>""")

# 4. workshop photo + portrait badge + signature
OPTS["Despre4Atelier"] = ("Despre 4: atelier și portret", f"""
.grid{{display:grid;grid-template-columns:minmax(0,6fr) minmax(0,6fr);gap:96px;align-items:center}}
.pic{{position:relative;margin:0 0 40px}}
.pic .big{{display:block;width:100%;aspect-ratio:4/5;object-fit:cover;object-position:40% 60%;border-radius:28px;corner-shape:squircle;box-shadow:0 40px 70px -40px rgba(58,42,32,.55)}}
.pic .me{{position:absolute;right:-28px;bottom:-40px;width:172px;height:172px;border-radius:50%;padding:8px;background:var(--paper);box-shadow:0 20px 40px -22px rgba(58,42,32,.5)}}
.pic .me img{{width:100%;height:100%;border-radius:50%;object-fit:cover;background:#DCC2A0}}
.sig{{display:flex;align-items:baseline;gap:16px;margin-top:30px}}
.sig .n{{font:400 52px/1 var(--script);color:var(--terra-d)}}
.sig .r{{font:500 12px/1.4 var(--text);letter-spacing:.14em;text-transform:uppercase;color:var(--ink2);max-width:28ch}}
.creds{{margin:28px 0 0;padding:0;list-style:none;display:grid;gap:8px;font-size:15px;color:var(--ink2)}}
.creds li{{position:relative;padding-left:24px}}
.creds li::before{{content:"";position:absolute;left:0;top:.8em;width:13px;height:1px;background:var(--clay)}}
@media (max-width:820px){{.grid{{grid-template-columns:1fr;gap:56px}}.pic .me{{width:120px;height:120px;right:-8px}}}}
""", f"""<div class="wrap grid">
<figure class="pic"><img class="big" src="{ATELIER}" alt="Participanți modelând lut în jurul mesei, la un atelier AVA"><span class="me"><img src="{STAMP_PHOTO}" alt="Alessia Văideanu"></span></figure>
<div>
<p class="kicker">Despre noi</p>
<h2 class="lead disp">{LEAD}</h2>
<p class="body">{BODY}</p>
<ul class="creds">{''.join(f'<li>{a}, {b}</li>' for a, b in CREDS)}</ul>
<div class="sig"><span class="n">Alessia</span><span class="r">{ROLE}</span></div>
{LINK}
</div>
</div>""")


def page(title, css, html):
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
{HERO_END}
<section class="sec" id="despre" aria-label="Despre noi">
{html}
</section>
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":1440,"height":900}}}}'>
class Component extends DCLogic {{
  renderVals() {{ return {{}}; }}
}}
</script>
</body>
</html>
"""


for name, (title, css, html) in OPTS.items():
    open(os.path.join(P, name + ".dc.html"), "w", encoding="utf-8").write(page(title, css, html))
    print(name)
