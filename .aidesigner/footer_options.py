"""Acasă: newsletter + footer in one closing block (Vali, 11 nov). Four variants, each from a real site (footers checked live):
Footer1Aesop      aesop.com: dark band, link columns, the newsletter as the last, wider column; legal row underneath.
Footer2EastFork   eastfork.com: the offer as a big sentence with the email field, link columns below; on brand sand.
Footer3Heath      heathceramics.com: newsletter with 'what are you interested in' preferences, small caps column labels;
                  here inside the chosen postcard (Final 2), which straddles the seam into a dark footer.
Footer4HelenLevi  helenlevi.com: full-bleed photo, round stamp logo in the middle, one quiet row of links.
Footer content: CLAUDE.md (menu, 'Ce oferim' pages, legal pages, ANPC, PFA data, Instagram) + Contact from the document.
Mine, to approve: the column labels 'Navigare', 'Informații'; 'Ce te interesează?' is the label of the document's contact form.
ANPC: the final site needs ANPC's official SAL pictogram (image + link); here it is a text badge.

usage: python3 .aidesigner/footer_options.py
"""
import os, subprocess, sys
from about_options2 import P, HERE, ARROW
from newsletter_options import (NL_SUB, FINALS, COMMON as NL_COMMON, page as nl_page, form, contact, seal, NL_H, NL_5, VASE, PHOTO, PHOTO_ALT, CONTACT, bind)

NAV = [("Acasă", "#top"), ("Despre noi", "#despre"), ("Ce oferim", "#ce-facem"), ("Evenimente", "#evenimente"), ("Galerie", "#galerie"), ("Contact", "#contact")]
SERV = [("Ateliere de grup", "#ateliere-de-grup"), ("Pentru companii", "#companii"), ("Consiliere 1:1", "#consiliere"),
        ("Atelier privat 1:1", "#atelier-privat"), ("Retreaturi", "#retreaturi"), ("Pentru școli și copii", "#scoli")]
INFO = [("Întrebări frecvente", "#faq"), ("Înscrieri, plată și anulare", "#inscrieri"), ("Termeni și condiții", "#termeni"),
        ("Politica de confidențialitate", "#confidentialitate"), ("Cookies", "#cookies")]
PFA = "VAIDEANU ALESSIA-ALEXANDRA PFA · CUI 55380756 · Reg. Com. F2026038934007 · Sediu: [ADRESA SEDIULUI] · ava.events.26@gmail.com"
ANPC = '<a class="anpc" href="https://anpc.ro/ce-este-sal/">ANPC · SAL</a>'
LANG = '<div class="lng" role="group" aria-label="Limba site-ului"><a href="#ro" aria-current="true">RO</a><a href="#en" lang="en">EN</a></div>'
LOGO = (f'<a class="flogo" href="#top" aria-label="AVA Art &amp; Soul, pagina principală">{VASE}'
        '<span><span class="w">AVA</span><span class="s">ART &amp; SOUL</span></span></a>')
TAG = '<p class="tag">autocunoaștere prin creație</p>'
INTERESTS = ["Ateliere de grup", "Retreaturi", "Pentru companii", "Consiliere 1:1"]


def col(title, items, cls=""):
    return (f'<nav class="col {cls}" aria-label="{title}"><p class="ch">{title}</p><ul>'
            + "".join(f'<li><a href="{h}">{t}</a></li>' for t, h in items) + "</ul></nav>")


def contact_col(title="Contact"):
    return (f'<div class="col cc"><p class="ch">{title}</p><ul>' + "".join(f'<li><a href="{h}">{v}</a></li>' for _, v, h in CONTACT)
            + "<li><span>București</span></li></ul></div>")


def legal():
    return f'<div class="legal"><p>© 2026 AVA Art &amp; Soul · {PFA}</p><div class="lr">{ANPC}{LANG}</div></div>'


CSS = NL_COMMON + """
.ft{position:relative}
.ft a{color:inherit}
.flogo{display:inline-flex;align-items:center;gap:12px;min-height:44px;text-decoration:none}
.flogo svg{width:22px;height:28px}
.flogo>span{display:flex;flex-direction:column;gap:5px;line-height:1}
.flogo .w{font:400 24px/1 var(--display);font-variation-settings:'opsz' 20;letter-spacing:.3em}
.flogo .s{font:500 9px/1 var(--text);letter-spacing:.3em}
.tag{margin:10px 0 0;font:400 italic 18px/1.3 var(--display);font-variation-settings:'opsz' 20}
.col .ch{margin:0 0 12px;font-size:13px;font-weight:600;letter-spacing:.04em}
.col ul{list-style:none;margin:0;padding:0;display:flex;flex-direction:column}
.col li a,.col li span{display:inline-flex;align-items:center;min-height:34px;font-size:15px;text-decoration:none}
.col li a{background:linear-gradient(currentColor,currentColor) 0 calc(100% - 6px)/0 1px no-repeat;transition:background-size .3s cubic-bezier(.2,.7,.2,1)}
.col li a:hover{background-size:100% 1px}
.legal{display:flex;justify-content:space-between;align-items:center;gap:16px 32px;flex-wrap:wrap;margin-top:56px;padding-top:22px;font-size:13px}
.legal p{margin:0;max-width:72ch}
.legal .lr{display:flex;align-items:center;gap:20px}
.anpc{display:inline-flex;align-items:center;min-height:36px;padding:0 14px;border:1px solid currentColor;border-radius:8px;font-size:12px;font-weight:600;letter-spacing:.08em;text-decoration:none}
.lng{display:flex;gap:4px}.lng a{display:grid;place-items:center;min-width:40px;min-height:40px;border-radius:999px;font-size:13px;font-weight:600;letter-spacing:.06em;text-decoration:none;opacity:.6}
.lng a[aria-current]{opacity:1;box-shadow:inset 0 0 0 1px currentColor}
.ft a:focus-visible{outline:2px solid currentColor;outline-offset:3px}
/* form on dark */
.dk{color:#F4EDE4}
.dk .five,.dk .nf .ok,.dk .legal,.dk .col li span{color:#D9C7B4}
.dk .col .ch{color:#BFA992}
.dk .nf .lbl{color:#F4EDE4}
.dk .nf input[type=email]{background:rgba(244,237,228,.06);border-color:rgba(244,237,228,.32);color:#F4EDE4}
.dk .nf input[type=email]::placeholder{color:#A8927E}
.dk .btn{background:#F4EDE4;color:#3A2A20}.dk .btn:hover{background:#FFF8EE}
.dk .nf .done{color:#F2C79C}.dk .nf[data-err] .ok span{color:#F2C79C}
.dk .btn:focus-visible,.dk .nf input:focus-visible,.dk .ok a:focus-visible{outline-color:#F2C79C}
@media (max-width:820px){.cc{grid-column:1/-1}.legal{flex-direction:column;align-items:flex-start;margin-top:40px}.col li a,.col li span{min-height:40px}}
"""

V = {}

# ---------- 1. Aesop ----------
V["Footer1Aesop"] = ("Footer 1: coloane + newsletter (Aesop)", "aesop.com", """
.f1{background:#3A2A20;padding:96px 0 32px}
.f1 .top{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:64px}
.f1 .grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr)) minmax(0,2fr);gap:40px}
.f1 .nlc h2{font:400 32px/1.1 var(--display);font-variation-settings:'opsz' 20;letter-spacing:-.01em;margin:0}
.f1 .nlc .five{margin:10px 0 22px;font-size:16px}
.f1 .nlc .nf .row{flex-direction:column}.f1 .nlc .btn{align-self:flex-start}
.f1 .legal{border-top:1px solid rgba(244,237,228,.16)}
.f1 .tag{color:#D9C7B4}
@media (max-width:1100px){.f1 .grid{grid-template-columns:repeat(2,minmax(0,1fr))}.f1 .nlc{grid-column:1/-1;order:-1;margin-bottom:12px}}
@media (max-width:820px){.f1{padding:64px 0 28px}.f1 .top{margin-bottom:40px}.f1 .grid{gap:32px 20px}.f1 .nlc .btn{align-self:stretch}}
""", f"""<footer class="ft f1 dk" id="newsletter" aria-label="Subsol" ref="{bind("rootRef")}"><div class="wrap">
<div class="top"><div>{LOGO}{TAG}</div></div>
<div class="grid">{col("Navigare", NAV)}{col("Ce oferim", SERV)}{col("Informații", INFO)}{contact_col()}
<div class="nlc"><h2>{NL_H}</h2><p class="five">{NL_5}</p>{form("ft-e1")}</div></div>
{legal()}
</div></footer>""")

# ---------- 2. East Fork ----------
V["Footer2EastFork"] = ("Footer 2: oferta mare + coloane (East Fork)", "eastfork.com", """
.f2{background:#E6D5BD;padding:112px 0 32px}
.f2 .offer{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);gap:72px;align-items:end;padding-bottom:72px;border-bottom:1px solid rgba(58,42,32,.2)}
.f2 .offer h2{font:400 clamp(40px,4.4vw,64px)/1.02 var(--display);font-variation-settings:'opsz' 20;letter-spacing:-.012em;margin:0;text-wrap:balance}
.f2 .offer .five{margin:16px 0 0;font-size:18px;color:var(--ink2)}
.f2 .nf input[type=email]{background:#FBF7F0}
.f2 .grid{display:grid;grid-template-columns:minmax(0,1.4fr) repeat(4,minmax(0,1fr));gap:40px;padding-top:56px}
.f2 .col .ch{color:var(--ink2)}
.f2 .legal{border-top:1px solid rgba(58,42,32,.2);color:var(--ink2)}
.f2 .tag{color:var(--ink2)}
@media (max-width:1100px){.f2 .grid{grid-template-columns:repeat(2,minmax(0,1fr))}.f2 .brand{grid-column:1/-1}}
@media (max-width:820px){.f2{padding:72px 0 28px}.f2 .offer{grid-template-columns:1fr;gap:28px;padding-bottom:48px}.f2 .offer h2{font-size:clamp(36px,10vw,44px)}.f2 .grid{gap:32px 20px;padding-top:40px}}
""", f"""<footer class="ft f2" id="newsletter" aria-label="Subsol" ref="{bind("rootRef")}"><div class="wrap">
<div class="offer"><div><h2>{NL_H}</h2><p class="five">{NL_5}</p></div>{form("ft-e2")}</div>
<div class="grid"><div class="brand">{LOGO}{TAG}</div>{col("Navigare", NAV)}{col("Ce oferim", SERV)}{col("Informații", INFO)}{contact_col()}</div>
{legal()}
</div></footer>""")

# ---------- 3. Heath + the chosen postcard ----------
_t, _s, PC_CSS, _h = FINALS["Final2CartePostala"]
chips = ('<fieldset class="pref"><legend>Ce te interesează?</legend><div class="chips">'
         + "".join(f'<label class="chip"><input type="checkbox" name="interes" value="{t}"><span>{t}</span></label>' for t in INTERESTS)
         + "</div></fieldset>")
pc_form = form("ft-e3", line=True)  # Vali (11 nov): no interest chips
V["Footer3Heath"] = ("Footer 3: carte poștală pe cusătură (Heath Ceramics)", "heathceramics.com", PC_CSS.replace(".n2{background:linear-gradient(180deg,#F4EDE4 0%,#EDE0CD 100%)}", "") + """
.f3{padding:96px 0 32px;background:linear-gradient(180deg,#EDE0CD 0,#EDE0CD 300px,#3A2A20 300px)}
.f3 .card{color:var(--ink)}
.f3 .r{padding-top:104px}
.f3 .pref{margin:8px 0 6px;padding:0;border:0}
.f3 .pref legend{padding:0;margin-bottom:10px;font-size:14px;font-weight:600;letter-spacing:.02em}
.f3 .chips{display:flex;flex-wrap:wrap;gap:8px}
.f3 .chip{position:relative;cursor:pointer}
.f3 .chip input{position:absolute;opacity:0;inset:0;margin:0;cursor:pointer}
.f3 .chip span{display:inline-flex;align-items:center;min-height:40px;padding:0 16px;border:1px solid rgba(58,42,32,.28);border-radius:999px;font-size:14px;transition:background .2s,color .2s,border-color .2s}
.f3 .chip input:checked+span{background:var(--ink);border-color:var(--ink);color:#F4EDE4}
.f3 .chip input:focus-visible+span{outline:2px solid #9C472C;outline-offset:2px}
.f3 .grid{display:grid;grid-template-columns:minmax(0,1.4fr) repeat(4,minmax(0,1fr));gap:40px;margin-top:88px}
.f3 .col .ch{font-size:12px;letter-spacing:.14em;text-transform:uppercase}
.f3 .legal{border-top:1px solid rgba(244,237,228,.16)}
.f3 .dk{background:#3A2A20;box-shadow:0 0 0 100vmax #3A2A20;clip-path:inset(0 -100vmax)}
.f3 .tag{color:#D9C7B4}
@media (max-width:1100px){.f3 .grid{grid-template-columns:repeat(2,minmax(0,1fr))}.f3 .brand{grid-column:1/-1}}
@media (max-width:820px){.f3{padding-top:56px;background:linear-gradient(180deg,#EDE0CD 0,#EDE0CD 200px,#3A2A20 200px)}.f3 .r{padding-top:28px}.f3 .grid{gap:32px 20px;margin-top:56px}}
""", f"""<footer class="ft f3 nl n2" id="newsletter" aria-label="Subsol" ref="{bind("rootRef")}"><div class="wrap">
<div class="card"><div class="l"><h2 class="disp" id="nl-h">{NL_H}</h2><p class="five">{NL_5}</p><p class="sig">– Alessia Văideanu</p></div>
<div class="r">{seal("sr-f3")}{pc_form}</div></div>
<div class="dk"><div class="grid"><div class="brand">{LOGO}{TAG}</div>{col("Navigare", NAV)}{col("Ce oferim", SERV)}{col("Informații", INFO)}{contact_col()}</div>
{legal()}</div>
</div></footer>""")

# ---------- 4. Helen Levi ----------
QUIET = [("Despre noi", "#despre"), ("Ce oferim", "#ce-facem"), ("Evenimente", "#evenimente"), ("Galerie", "#galerie"),
         ("Contact", "#contact"), ("Întrebări frecvente", "#faq"), ("Instagram", "https://www.instagram.com/ava.art.soul/")]
QUIET2 = INFO[1:]
V["Footer4HelenLevi"] = ("Footer 4: fotografie + ștampilă (Helen Levi)", "helenlevi.com", """
.f4{position:relative;overflow:hidden;padding:120px 0 28px;color:#F4EDE4;text-align:center}
.f4 .bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 55%}
.f4::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(30,14,8,.7) 0%,rgba(30,14,8,.78) 55%,rgba(30,14,8,.9) 100%)}
.f4 .nf input[type=email]{background:rgba(30,14,8,.5)}.f4 .nf input[type=email]::placeholder{color:#C9B5A1}
.f4 .wrap{position:relative;z-index:1}
.f4 .seal{color:#F4EDE4;margin:0 auto 28px;display:block}
.f4 h2{font:400 clamp(40px,4.4vw,60px)/1.04 var(--display);font-variation-settings:'opsz' 20;letter-spacing:-.012em;margin:0 auto;max-width:16ch;text-wrap:balance}
.f4 .five{margin:14px auto 30px;font-size:18px}
.f4 .nf{margin:0 auto;text-align:left}
.f4 .quiet{list-style:none;display:flex;flex-wrap:wrap;justify-content:center;gap:0 26px;margin:96px 0 0;padding:0}
.f4 .quiet a{display:inline-flex;align-items:center;min-height:40px;font-size:14px;letter-spacing:.04em;text-decoration:underline;text-decoration-color:rgba(244,237,228,.4);text-underline-offset:5px}
.f4 .quiet a:hover{text-decoration-color:currentColor}
.f4 .legal{justify-content:center;flex-direction:column;margin-top:18px;border-top:0;padding-top:0}
.f4 .legal p{max-width:none}
.f4 .q2{display:flex;flex-wrap:wrap;justify-content:center;gap:0 18px;list-style:none;margin:0;padding:0}
.f4 .q2 a{display:inline-flex;align-items:center;min-height:36px;font-size:13px;text-decoration:none;opacity:.85}
.f4 .q2 a:hover{opacity:1;text-decoration:underline}
@media (max-width:820px){.f4{padding:80px 0 24px}.f4 .seal{width:96px;height:96px}.f4 .quiet{margin-top:64px;gap:0 18px}.f4 .legal{align-items:center}}
""", f"""<footer class="ft f4 dk" id="newsletter" aria-label="Subsol" ref="{bind("rootRef")}"><img class="bg" src="{PHOTO}" alt="" loading="lazy"><div class="wrap">
{seal("sr-f4", 132)}<h2>{NL_H}</h2><p class="five">{NL_5}</p>{form("ft-e4")}
<ul class="quiet">{"".join(f'<li><a href="{h}">{t}</a></li>' for t, h in QUIET)}</ul>
<div class="legal"><ul class="q2">{"".join(f'<li><a href="{h}">{t}</a></li>' for t, h in QUIET2)}</ul><p>© 2026 AVA Art &amp; Soul · {PFA}</p><div class="lr">{ANPC}{LANG}</div></div>
</div></footer>""")

if __name__ == "__main__":
    for name, (title, src, css, html) in V.items():
        for suffix, w, h in (("", 1440, 900), ("Mobil", 390, 1600)):
            open(os.path.join(P, f"{name}{suffix}.dc.html"), "w", encoding="utf-8").write(nl_page(title + (" · mobil" if suffix else ""), CSS + css, html, w, h))
        subprocess.run([sys.executable, os.path.join(HERE, "dc2html.py"), os.path.join(P, f"{name}.dc.html"), os.path.join(HERE, f"opt-{name}.html")], check=True)
    names = list(V)
    open(os.path.join(HERE, "footer.html"), "w").write('<!doctype html><meta charset="utf-8"><title>Footer</title><style>body{margin:0}iframe{width:1440px;height:960px;border:0;display:block;border-bottom:8px solid #222}</style>' + "".join(f'<iframe src="opt-{n}.html"></iframe>' for n in names))
    open(os.path.join(HERE, "footer-mobil.html"), "w").write('<!doctype html><meta charset="utf-8"><title>Footer mobil</title><style>body{margin:0;padding:10px;background:#1b1b1b;display:flex;gap:12px;color:#ddd;font:13px system-ui}figure{margin:0;flex:none}iframe{width:390px;height:2060px;border:0;display:block}</style>' + "".join(f'<figure><figcaption>{n}</figcaption><iframe src="opt-{n}.html"></iframe></figure>' for n in names))
