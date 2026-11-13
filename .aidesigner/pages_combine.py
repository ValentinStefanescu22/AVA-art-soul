"""Despre noi and Ce oferim, assembled like Acasă (Vali, 11 nov) with <dc-import>, one source of truth per section.
Same header as Acasă (Header 1, the glass pill that follows you), same footer (Footer 3), same scroll reveals.
The joins are hidden the same way: transparent section roots, each section starts in the colour the previous one
ended in, one rhythm of space instead of two paddings stacked. On Despre noi the brown hero melts into Povestea through
an eased OKLab gradient (cf_pagina_options.eased_gradient, the one on the Ce oferim hero), long enough not to show a band.

usage: python3 .aidesigner/pages_combine.py   (re-run after any section generator; scoping is idempotent)
writes canvas/project/{DespreNoi,CeFacem}(Mobil).dc.html + local previews despre-noi.html, ce-facem.html
"""
import os, re, subprocess
from about_options2 import P, HERE
from acasa_combine import scope_file, page, STATIC, PAPER, SAND, REVEAL, REVEAL_CSS, REVEAL_MOUNT, REVEAL_UNMOUNT
from header_options import acasa_parts
from cf_pagina_options import eased_gradient

HX_CSS, HX_HEAD, HX_SHEET, hx_js = acasa_parts()

# (file, scope, preview height) in page order
PAGES = {
    "DespreNoi": dict(title="Despre noi", cls="dn", heights=(4544, 5998), dark=".s-pov .pr", current=("#despre", "Despre noi"),
                      sections=[("DespreNoiDeschidere", "s-dnhero"), ("Povestea4Interviu", "s-pov"), ("Formari3DCentrat", "s-form"),
                                ("Comunitate5Carduri", "s-com"), ("Footer3Heath", "s-footer")]),
    "CeFacem": dict(title="Ce oferim", cls="cf", heights=(2843, 4633), dark=".s-cfhero .c1", current=("#ce-facem", "Ce oferim"),
                    sections=[("CFPagina1Comutator", "s-cfhero"), ("CFDeCe", "s-dece"), ("Footer3Heath", "s-footer")]),
    # Vali (12 nov): hero 2 (Aman) + lista 3 (bilete; the December ones with the light garland, Crăciun 2), then „Cum funcționează”, the FAQ (grup_page_options.py) and the footer
    "AteliereDeGrup": dict(title="Ateliere de grup", cls="ag", heights=(5090, 7113), dark=".s-ghero .g2", current=("#ce-facem", "Ce oferim"),
                           sections=[("GrupHero2Aman", "s-ghero"), ("GrupCraciun2Beculete", "s-glista"), ("GrupSolicita", "s-gsol"), ("GrupDetalii", "s-gdet"),
                                     ("GrupFaq", "s-gfaq"), ("Footer3Heath", "s-footer")]),
    # Vali (13 nov): every page assembled. Services on the same template as Ateliere de grup; the others are one whole-page
    # board each (their own header hidden) + the footer.
    "Consiliere": dict(title="Consiliere 1:1", cls="cn", heights=(5327, 7090), dark=".s-chero .g2", current=("#ce-facem", "Ce oferim"), sheet="Consiliere 1:1",
                       sections=[("ConsHero", "s-chero"), ("ConsIntrebari5Coloane", "s-cq"), ("ConsDetalii", "s-cdet"), ("ConsProgramare1Luna", "s-cbk"),
                                 ("ConsFaq", "s-cfaq"), ("Footer3Heath", "s-footer")]),
    "AtelierPrivat": dict(title="Atelier privat 1:1", cls="ap", heights=(5487, 7356), dark=".s-phero .g2", current=("#ce-facem", "Ce oferim"), sheet="Atelier privat 1:1",
                          sections=[("PrivHero", "s-phero"), ("PrivAteliere4Acordeon", "s-pat"), ("PrivDetalii", "s-pdet"), ("PrivProgramare", "s-pbk"),
                                    ("PrivFaq", "s-pfaq"), ("Footer3Heath", "s-footer")]),
    "ScoliCopii": dict(title="Pentru școli și copii", cls="sk", heights=(3314, 4514), dark=".s-shero .g2", current=("#ce-facem", "Ce oferim"), sheet="Pentru școli și copii",
                       sections=[("ScoliHero", "s-shero"), ("ScoliDetalii", "s-sdet"), ("ScoliFaq", "s-sfaq"), ("Footer3Heath", "s-footer")]),
    "Retreaturi": dict(title="Retreaturi", cls="rp", heights=(1874, 2744), dark=".s-rt .rt", current=("#ce-facem", "Ce oferim"), sheet="Retreaturi",
                       sections=[("Retreat1Ecran", "s-rt"), ("Footer3Heath", "s-footer")]),
    "Evenimente": dict(title="Evenimente", cls="ep", heights=(1889, 2716), dark=".s-ev .rt", current=("#evenimente", "Evenimente"), sheet="Evenimente",
                       sections=[("Evenimente1Ecran", "s-ev"), ("Footer3Heath", "s-footer")]),
    "Galerie": dict(title="Galerie", cls="gp2", heights=(2964, 4338), dark=".no-dark-hero", current=("#galerie", "Galerie"), sheet="Galerie",
                    sections=[("Galerie2Albume", "s-gal"), ("Footer3Heath", "s-footer")]),
    "Contact": dict(title="Contact", cls="cp", heights=(1754, 2896), dark=".no-dark-hero", current=("#contact", "Contact"), sheet="Contact",
                    sections=[("Contact5Pasi", "s-ct"), ("Footer3Heath", "s-footer")]),
    # FAQ: Vali (13 nov), variant 2 (the categories in a list beside, every question one under the other)
    "IntrebariFrecvente": dict(title="Întrebări frecvente", cls="fp", heights=(4626, 5504), dark=".no-dark-hero", current=None, sheet=None,
                               sections=[("Faq2Lista", "s-faqp"), ("Footer3Heath", "s-footer")]),
    "Inscrieri": dict(title="Înscriere, plată și anulare", cls="lp", heights=(2973, 4022), dark=".no-dark-hero", current=None, sheet=None,
                      sections=[("LegalInscriere", "s-lins"), ("Footer3Heath", "s-footer")]),
    "Termeni": dict(title="Termeni și condiții", cls="lp", heights=(4901, 6643), dark=".no-dark-hero", current=None, sheet=None,
                    sections=[("LegalTermeni", "s-lter"), ("Footer3Heath", "s-footer")]),
    "Confidentialitate": dict(title="Politica de confidențialitate", cls="lp", heights=(4279, 6584), dark=".no-dark-hero", current=None, sheet=None,
                              sections=[("LegalConfidentialitate", "s-lconf"), ("Footer3Heath", "s-footer")]),
    "Cookies": dict(title="Cookies", cls="lp", heights=(2590, 3653), dark=".no-dark-hero", current=None, sheet=None,
                    sections=[("LegalCookies", "s-lcook"), ("Footer3Heath", "s-footer")]),
    "Multumim": dict(title="Mulțumim! (după plată)", cls="kp", heights=(1799, 2994), dark=".no-dark-hero", current=None, sheet=None,
                     sections=[("Confirmare2Bilet", "s-conf"), ("Footer3Heath", "s-footer")]),
    "ProgramareFacuta": dict(title="Programarea e făcută", cls="kp", heights=(1799, 2881), dark=".no-dark-hero", current=None, sheet=None,
                             sections=[("ConfirmareProgramare", "s-cprog"), ("Footer3Heath", "s-footer")]),
    "Eroare404": dict(title="404", cls="kp", heights=(1544, 2537), dark=".no-dark-hero", current=None, sheet=None,
                      sections=[("Pagina404", "s-404"), ("Footer3Heath", "s-footer")]),
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


# Ateliere de grup: the hero's photo already melts into paper → tickets paper→sand → „Cum funcționează” sand→paper
# → FAQ paper→sand → footer sand. The header turns light where the photo's fade begins.
AG_CSS = (
    ".ag .s-ghero .g2{--hx-dark:780px}"
    ".ag .s-glista .a3 ul{max-width:none}.ag .s-glista .ga{padding:40px 0 104px}.ag .s-gdet .gd,.ag .s-gfaq .fq{padding:88px 0 104px}"
    "@media (max-width:980px){.ag .s-ghero .g2{--hx-dark:690px}.ag .s-glista .ga{padding:24px 0 72px}.ag .s-gdet .gd,.ag .s-gfaq .fq{padding:56px 0 72px}}"
)
# services: the hero melts into paper; then the sections alternate paper→sand / sand→paper so no seam shows; the FAQ ends in
# the footer's sand. One rhythm of space, as on Ateliere de grup.
def chain(cls, hero, secs):
    css = f".{cls} .s-{hero} .g2{{--hx-dark:780px}}"
    mob = f".{cls} .s-{hero} .g2{{--hx-dark:690px}}"
    for i, sel in enumerate(secs):
        a, b = (PAPER, SAND) if i % 2 == 0 else (SAND, PAPER)
        if i == len(secs) - 1:
            b = SAND
        css += f".{cls} {sel}{{background:linear-gradient(180deg,{a} 0%,{b} 100%);padding:88px 0 104px}}"
        mob += f".{cls} {sel}{{padding:56px 0 72px}}"
    return css + "@media (max-width:980px){" + mob + "}"


CN_CSS = chain("cn", "chero", [".s-cq .cs", ".s-cdet .gd", ".s-cbk .cs", ".s-cfaq .fq"])
AP_CSS = chain("ap", "phero", [".s-pat .cs", ".s-pdet .gd", ".s-pbk .cs", ".s-pfaq .fq"])
SK_CSS = chain("sk", "shero", [".s-sdet .gd", ".s-sfaq .fq"])
# whole-page boards: they already end in sand (#EDE0CD), the footer's colour; the dark „În curând” screens keep their photo
PAGE_CSS = {"dn": DN_CSS, "cf": CF_CSS, "ag": AG_CSS, "cn": CN_CSS, "ap": AP_CSS, "sk": SK_CSS,
            "rp": "", "ep": "", "gp2": "", "cp": "", "fp": "", "lp": "", "kp": ""}


def header(href, label):
    h = HX_HEAD.replace(' aria-current="page"', "")
    if href is None:
        return h
    a = f'<a href="{href}" aria-haspopup="true">' if href == "#ce-facem" else f'<a href="{href}">{label}</a>'
    b = a.replace("<a ", '<a aria-current="page" ', 1)
    assert a in h
    return h.replace(a, b, 1)


def sheet(href, label=None):
    s = HX_SHEET.replace(' aria-current="page"', "")
    if href == "#despre":
        s = s.replace('<a href="#despre" onClick', '<a href="#despre" aria-current="page" onClick', 1)
    elif label:
        m = re.search(r'<a href="#[^"]*" onClick="\{\{ closeMenu \}\}">' + re.escape(label) + "</a>", s)
        assert m, label
        s = s.replace(m.group(0), m.group(0).replace("<a ", '<a aria-current="page" ', 1), 1)
    return s


# ---- links (Vali, 13 nov: „să mergi de la pagină la pagină”) ----
# On the canvas, <a href="Page.dc.html"> moves Play to that artboard. Every link to another page is rewritten here, in the
# assembled pages and in their sections (so a section played alone navigates too); in-page anchors (#programare, #oferta,
# #ateliere…) stay. Run last: section generators write #hashes again. In the Next.js build these become /ro/... routes.
PAGE_OF = {"top": "Acasa", "acasa": "Acasa", "despre": "DespreNoi", "povestea": "DespreNoi", "ce-facem": "CeFacem", "pentru-tine": "CeFacem",
           "evenimente": "Evenimente", "galerie": "Galerie", "contact": "Contact",
           "grup": "AteliereDeGrup", "ateliere-de-grup": "AteliereDeGrup", "companii": "PentruCompanii", "pentru-companii": "PentruCompanii",
           "consiliere": "Consiliere", "privat": "AtelierPrivat", "atelier-privat": "AtelierPrivat", "retreat": "Retreaturi", "retreaturi": "Retreaturi",
           "scoli": "ScoliCopii", "copii": "ScoliCopii", "faq": "IntrebariFrecvente", "inscrieri": "Inscrieri", "termeni": "Termeni",
           "confidentialitate": "Confidentialitate", "cookies": "Cookies",
           "inscriere": "Multumim",               # „Mă înscriu” on a ticket: Stripe in code; here, the page after paying
           "programare-facuta": "ProgramareFacuta"}  # „Continuă” in the booking calendar: Cal.com in code
# the „Ce oferim” submenu (header and phone sheet) all point at #ce-facem: route them by their label
BY_LABEL = {"Ateliere de grup": "AteliereDeGrup", "Pentru companii": "PentruCompanii", "Consiliere 1:1": "Consiliere",
            "Atelier privat 1:1": "AtelierPrivat", "Retreaturi": "Retreaturi", "Pentru școli și copii": "ScoliCopii"}
LINK_RE = re.compile(r'(<a\b[^>]*?\bhref=")#([^"]+)("[^>]*>)(.*?)(</a>)', re.S)


def relink(text):
    def one(m):
        h, label = m.group(2), re.sub(r"<[^>]+>", "", m.group(4)).strip()
        if h == "ce-facem" and label in BY_LABEL:
            dest = BY_LABEL[label]
        elif h == "evenimente" and label == "Sold out":   # the announcement on Acasă is about a workshop
            dest = "AteliereDeGrup"
        else:
            dest = PAGE_OF.get(h)
        return m.group(0) if not dest else m.group(1) + dest + ".dc.html" + m.group(3) + m.group(4) + m.group(5)
    head, sep, rest = text.partition("<x-dc>")
    return head + sep + LINK_RE.sub(one, rest) if sep else text


ACASA = ["Acasa", "HeroAnuntCentrat", "CopertaH", "CeFacem5Acordeon", "UrmatorulA", "OameniB2", "Faq3Carduri", "Popup3Plic"]
COMPANII = ["PentruCompanii", "CompHero", "CompFormate1Planuri", "CompDetalii", "CompOferta4Pasi", "CompFaq"]   # assembled on the canvas (12 nov)
LOCAL = {"Acasa": "acasa.html", "DespreNoi": "despre-noi.html", "CeFacem": "ce-facem.html", "AteliereDeGrup": "ateliere-de-grup.html",
         "PentruCompanii": "pentru-companii.html", "Consiliere": "consiliere.html", "AtelierPrivat": "atelier-privat.html",
         "ScoliCopii": "scoli-si-copii.html", "Retreaturi": "retreaturi.html", "Evenimente": "evenimente.html", "Galerie": "galerie.html",
         "Contact": "contact.html", "IntrebariFrecvente": "intrebari-frecvente.html", "Inscrieri": "inscrieri.html", "Termeni": "termeni.html",
         "Confidentialitate": "confidentialitate.html", "Cookies": "cookies.html", "Multumim": "multumim.html",
         "ProgramareFacuta": "programare-facuta.html", "Eroare404": "404.html"}

if __name__ == "__main__":
    for name, pg in PAGES.items():
        for f, sc in pg["sections"]:
            print(("scoped " if scope_file(f, sc) else "already scoped ") + f)
        cls, (dh, mh) = pg["cls"], pg["heights"]
        dh, mh = dh or 3000, mh or 4000
        mount = REVEAL_MOUNT.replace(REVEAL, FOOT_SEL).replace("main.acasa", "main.pgx")
        css = (COMMON + PAGE_CSS[cls]
               + REVEAL_CSS.replace(".acasa.rv-on", ".pgx.rv-on") + HX_CSS)
        dark = pg["dark"]
        if dark == ".no-dark-hero":   # a light page: the header is dark-on-light from the top (the script treats „no hero” as dark)
            first = pg["sections"][0][1]
            dark, css = "." + first, css + f".{cls} .{first}{{--hx-dark:0px}}"
        imports = "\n".join(f'<dc-import name="{f}" hint-size="100%,1000px"></dc-import>' for f, _ in pg["sections"])
        cur = pg["current"] or (None, None)
        body = (f'<main class="pgx {cls} hxv v1" style="background: #F4EDE4">\n{header(*cur)}\n{imports}\n'
                f'{sheet(cur[0], pg.get("sheet"))}\n</main>')
        out = os.path.join(P, name + ".dc.html")
        open(out, "w", encoding="utf-8").write(page(pg["title"], body, 1440, dh, hx_js(mount, REVEAL_UNMOUNT, dark), css))
        open(os.path.join(P, name + "Mobil.dc.html"), "w", encoding="utf-8").write(
            page(pg["title"] + ": mobil", f'<div style="width: 390px; background: #F4EDE4">\n<dc-import name="{name}" hint-size="390px,{mh}px"></dc-import>\n</div>',
                 390, mh, STATIC))
        print("wrote", name, dh, mh)
    # links, then the local previews (links between the local files, so the site can be walked locally too)
    files = set(ACASA + COMPANII + list(PAGES)) | {f for pg in PAGES.values() for f, _ in pg["sections"]}
    for f in sorted(files):
        p = os.path.join(P, f + ".dc.html")
        t = open(p, encoding="utf-8").read()
        n = relink(t)
        if n != t:
            open(p, "w", encoding="utf-8").write(n)
    for name, local in LOCAL.items():
        out = os.path.join(HERE, local)
        subprocess.run(["python3", os.path.join(HERE, "dc2html.py"), os.path.join(P, name + ".dc.html"), out], check=True)
        t = open(out, encoding="utf-8").read()
        for k, v in LOCAL.items():
            t = t.replace(f'href="{k}.dc.html"', f'href="{v}"').replace(f'data-dc-t-href="{k}.dc.html"', f'data-dc-t-href="{v}"')
        open(out, "w", encoding="utf-8").write(t)
    print("linked", len(files), "files; local previews:", ", ".join(LOCAL.values()))
