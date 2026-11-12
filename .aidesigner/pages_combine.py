"""Despre noi and Ce oferim, assembled like Acasă (Vali, 11 nov) with <dc-import>, one source of truth per section.
Same header as Acasă (Header 1, the glass pill that follows you), same footer (Footer 3), same scroll reveals.
The joins are hidden the same way: transparent section roots, each section starts in the colour the previous one
ended in, one rhythm of space instead of two paddings stacked. On Despre noi the brown hero melts into Povestea through
an eased OKLab gradient (cf_pagina_options.eased_gradient, the one on the Ce oferim hero), long enough not to show a band.

usage: python3 .aidesigner/pages_combine.py   (re-run after any section generator; scoping is idempotent)
writes canvas/project/{DespreNoi,CeFacem}(Mobil).dc.html + local previews despre-noi.html, ce-facem.html
"""
import os, subprocess
from about_options2 import P, HERE
from acasa_combine import scope_file, page, STATIC, PAPER, SAND, REVEAL, REVEAL_CSS, REVEAL_MOUNT, REVEAL_UNMOUNT
from header_options import acasa_parts
from cf_pagina_options import eased_gradient

HX_CSS, HX_HEAD, HX_SHEET, hx_js = acasa_parts()

# (file, scope, preview height) in page order
PAGES = {
    "DespreNoi": dict(title="Despre noi", cls="dn", heights=(4544, 5876), dark=".s-pov .pr", current=("#despre", "Despre noi"),
                      sections=[("DespreNoiDeschidere", "s-dnhero"), ("Povestea4Interviu", "s-pov"), ("Formari3DCentrat", "s-form"),
                                ("Comunitate5Carduri", "s-com"), ("Footer3Heath", "s-footer")]),
    "CeFacem": dict(title="Ce oferim", cls="cf", heights=(2843, 4600), dark=".s-cfhero .c1", current=("#ce-facem", "Ce oferim"),
                    sections=[("CFPagina1Comutator", "s-cfhero"), ("CFDeCe", "s-dece"), ("Footer3Heath", "s-footer")]),
}

# shared by both pages: the page's own header replaces the sections' ones and sits at the very top (no announcement strip)
COMMON = (".pgx .pg{background:transparent!important}.pgx .pg .hx-dock{display:none}.pgx>.hx-dock .hx{top:0!important}"
          "html{scroll-padding-top:88px}"
          f".pgx .s-footer .f3{{padding-top:72px;background:linear-gradient(180deg,{SAND} 0,{SAND} 276px,#3A2A20 276px)}}"
          f"@media (max-width:820px){{.pgx .s-footer .f3{{padding-top:40px;background:linear-gradient(180deg,{SAND} 0,{SAND} 184px,#3A2A20 184px)}}}}")

# Despre noi: hero (dark) → Povestea starts in the hero's last brown and eases to paper before its title → Formări paper→sand
# → Comunitatea sand → footer sand. --hx-dark: the header turns light where the fade passes its middle.
DN_CSS = (
    ".dn .s-dnhero .dnh{padding-bottom:40px!important}"
    f".dn .s-pov .pr{{background:{eased_gradient(0, 420, c0='#22140D', c1=PAPER, head='', tail=PAPER + ' 100%')};padding:320px 0 104px;--hx-dark:210px}}"
    f".dn .s-form .fq{{background:linear-gradient(180deg,{PAPER} 0%,{SAND} 100%);padding:88px 0 104px}}"
    f".dn .s-com .ck5{{background:{SAND};padding:88px 0 104px}}"
    "@media (max-width:980px){"
    ".dn .s-dnhero .dnh{padding-bottom:32px!important}"
    f".dn .s-pov .pr{{background:{eased_gradient(0, 340, c0='#22140D', c1=PAPER, head='', tail=PAPER + ' 100%')};padding:250px 0 72px;--hx-dark:170px}}"
    ".dn .s-form .fq,.dn .s-com .ck5{padding:56px 0 72px}}"
)
# Ce oferim: the hero already fades brown → cream and ends in #EFE4D4; „De ce” carries it on to the footer's sand.
CF_CSS = (
    ".cf .s-cfhero .c1{--hx-dark:565px}"
    f".cf .s-dece .cw{{background:linear-gradient(180deg,#EFE4D4 0%,{SAND} 100%);padding:88px 0 104px}}"
    "@media (max-width:980px){.cf .s-cfhero .c1{--hx-dark:480px}.cf .s-dece .cw{padding:56px 0 72px}}"
)

# the sections with their own scroll reveal (Povestea, Formări, Comunitatea, Ce oferim) keep it; the footer gets Acasă's
FOOT_SEL = ".s-footer .f3 .card,.s-footer .f3 .grid>*"


def header(href, label):
    h = HX_HEAD.replace(' aria-current="page"', "")
    a = f'<a href="{href}" aria-haspopup="true">' if href == "#ce-facem" else f'<a href="{href}">{label}</a>'
    b = a.replace("<a ", '<a aria-current="page" ', 1)
    assert a in h
    return h.replace(a, b, 1)


def sheet(href):
    s = HX_SHEET.replace(' aria-current="page"', "")
    if href == "#despre":
        s = s.replace('<a href="#despre" onClick', '<a href="#despre" aria-current="page" onClick', 1)
    return s


if __name__ == "__main__":
    for name, pg in PAGES.items():
        for f, sc in pg["sections"]:
            print(("scoped " if scope_file(f, sc) else "already scoped ") + f)
        cls, (dh, mh) = pg["cls"], pg["heights"]
        mount = REVEAL_MOUNT.replace(REVEAL, FOOT_SEL).replace("main.acasa", "main.pgx")
        css = (COMMON + (DN_CSS if cls == "dn" else CF_CSS)
               + REVEAL_CSS.replace(".acasa.rv-on", ".pgx.rv-on") + HX_CSS)
        imports = "\n".join(f'<dc-import name="{f}" hint-size="100%,1000px"></dc-import>' for f, _ in pg["sections"])
        body = (f'<main class="pgx {cls} hxv v1" style="background: #F4EDE4">\n{header(*pg["current"])}\n{imports}\n'
                f'{sheet(pg["current"][0])}\n</main>')
        out = os.path.join(P, name + ".dc.html")
        open(out, "w", encoding="utf-8").write(page(pg["title"], body, 1440, dh, hx_js(mount, REVEAL_UNMOUNT, pg["dark"]), css))
        open(os.path.join(P, name + "Mobil.dc.html"), "w", encoding="utf-8").write(
            page(pg["title"] + ": mobil", f'<div style="width: 390px; background: #F4EDE4">\n<dc-import name="{name}" hint-size="390px,{mh}px"></dc-import>\n</div>',
                 390, mh, STATIC))
        local = {"DespreNoi": "despre-noi.html", "CeFacem": "ce-facem.html"}[name]
        subprocess.run(["python3", os.path.join(HERE, "dc2html.py"), out, os.path.join(HERE, local)], check=True)
        print("wrote", name, dh, mh)
