"""Acasă, assembled from the chosen sections (Vali, 11 nov) with <dc-import>, so each section stays one source of truth.
A child's <helmet> styles are re-run in the importer, so the sections' class names would collide (.stage, .seal, .btn…).
This script scopes each chosen section's CSS in place under its own class on its root (.pg.s-<key>): it looks the same
alone and inside Acasă. Idempotent; re-run it after any section generator (hero_options.py, oameni_banda.py, …).
The old Acasa.dc.html (round 2 direction) is kept as AcasaRunda2.dc.html on 'Arhivă: runda 2' (canvas.json is edited by hand).

usage: python3 .aidesigner/acasa_combine.py
"""
import os, re
from about_options2 import P, FONTS

# (file, scope, desktop h, mobile h) in page order
SECTIONS = [("HeroAnuntCentrat", "s-hero", 960, 840), ("CopertaH", "s-despre", 1358, 1140),
            ("CeFacem5Acordeon", "s-cefacem", 996, 1183), ("UrmatorulA", "s-urmator", 960, 1366),
            ("OameniB2", "s-oameni", 1277, 986), ("Faq3Carduri", "s-faq", 790, 1060),
            ("Footer3Heath", "s-footer", 1146, 2042), ("Popup3Plic", "s-popup", 0, 0)]
NESTED = ("@media", "@supports", "@starting-style", "@container", "@layer")


def block_end(css, i):
    """index of the '}' closing the '{' at css[i]"""
    depth, q = 0, None
    while i < len(css):
        c = css[i]
        if q:
            if c == "\\": i += 1
            elif c == q: q = None
        elif c in "\"'": q = c
        elif c == "{": depth += 1
        elif c == "}":
            depth -= 1
            if not depth: return i
        i += 1
    raise ValueError("unbalanced css")


def split_top(sel):
    out, depth, cur = [], 0, ""
    for c in sel:
        if c in "([": depth += 1
        elif c in ")]": depth -= 1
        if c == "," and not depth:
            out.append(cur); cur = ""
        else:
            cur += c
    return out + [cur]


def scope_sel(sel, sc):
    out = []
    for s in split_top(sel):
        s = s.strip()
        if re.match(r"(html|body|:root)\b", s) or s.startswith(f".pg.{sc}") or s.startswith(f".{sc} "):
            out.append(s)
        elif re.match(r"\.pg\b", s):
            out.append(f".pg.{sc}" + s[3:])
        elif re.match(r"\.hxv\b", s):          # the header's tokens sit on the root too („pg hxv v1”)
            out.append(f".{sc}.hxv" + s[4:])
        else:
            out.append(f".{sc} {s}")
    return ",".join(out)


def scope(css, sc):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    out, i = [], 0
    while True:
        j = css.find("{", i)
        if j < 0:
            out.append(css[i:]); break
        pre = css[i:j].strip()
        if pre.startswith("@") and ";" in pre:   # statement at-rules (@import …;) before the block
            k = pre.rfind(";") + 1
            out.append(pre[:k]); pre = pre[k:].strip()
        k = block_end(css, j)
        body = css[j + 1:k]
        if pre.startswith(NESTED):
            out.append(pre + "{" + scope(body, sc) + "}")
        elif pre.startswith("@"):
            out.append(pre + "{" + body + "}")
        else:
            out.append(scope_sel(pre, sc) + "{" + body + "}")
        i = k + 1
    return "".join(out)


def scope_file(name, sc):
    f = os.path.join(P, name + ".dc.html")
    src = open(f, encoding="utf-8").read()
    if f'class="pg {sc}' in src:
        return False
    head, rest = src.split("<helmet>", 1)
    helm, tail = rest.split("</helmet>", 1)
    helm = re.sub(r"(<style>)(.*?)(</style>)", lambda m: m.group(1) + scope(m.group(2), sc) + m.group(3), helm, flags=re.S)
    tail = re.sub(r'<div class="pg(?=[ "])', f'<div class="pg {sc}', tail, count=1)   # roots like "pg hxv v1" too
    open(f, "w", encoding="utf-8").write(head + "<helmet>" + helm + "</helmet>" + tail)
    return True


def page(title, body, w, h, script, extra=""):
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
<style>body{{margin:0;background:#F4EDE4}}{extra}</style>
</helmet>
{body}
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{w},"height":{h}}}}}'>
{script}
</script>
</body>
</html>
"""


# Vali (11 nov): the joins must not show that the page was assembled from modules. So, on Acasă only:
# one continuous background (each section starts with the colour the previous one ended on: paper #F4EDE4 / sand #EDE0CD,
# 'Cine sunt' dips to the brand sand #E6D5BD), and one rhythm of space between sections instead of two paddings stacked.
PAPER, SAND, DEEP = "#F4EDE4", "#EDE0CD", "#E6D5BD"
ACASA_CSS = (
    ".s-despre .heroend{display:none}.pg.s-despre{padding-top:40px}"   # the hero already ends in its own wave (paper)
    ".pg{background:transparent!important}"
    f".acasa .s-despre .cv{{background:radial-gradient(ellipse 55% 60% at 50% 38%,#F6EEE3 0%,rgba(246,238,227,0) 70%),linear-gradient(180deg,{PAPER} 0%,{SAND} 45%,{DEEP} 100%)}}"
    f".acasa .s-cefacem .cf{{background:linear-gradient(180deg,{DEEP} 0%,{PAPER} 100%)}}"
    f".acasa .s-urmator .ua{{background:linear-gradient(180deg,{PAPER} 0%,{SAND} 100%)}}"
    f".acasa .s-oameni .og{{background:linear-gradient(180deg,{SAND} 0%,{PAPER} 100%)}}"
    f".acasa .s-faq .fq{{background:linear-gradient(180deg,{PAPER} 0%,{SAND} 100%)}}"
    ".acasa .s-cefacem .cf,.acasa .s-urmator .ua,.acasa .s-oameni .og,.acasa .s-faq .fq{padding-top:88px;padding-bottom:104px}"
    f".acasa .s-footer .f3{{padding-top:72px;background:linear-gradient(180deg,{SAND} 0,{SAND} 276px,#3A2A20 276px)}}"
    "@media (max-width:820px){"
    ".acasa .s-cefacem .cf,.acasa .s-urmator .ua,.acasa .s-oameni .og,.acasa .s-faq .fq{padding-top:56px;padding-bottom:72px}"
    f".acasa .s-footer .f3{{padding-top:40px;background:linear-gradient(180deg,{SAND} 0,{SAND} 184px,#3A2A20 184px)}}}}"
)
STATIC = "class Component extends DCLogic {\n  renderVals() { return {}; }\n}"

# Vali (11 nov): subtle scroll reveals. Each block fades in and rises 16px once, ease-out, as it enters the screen;
# siblings follow 80ms apart. Uses the `translate` property (not `transform`) and an animation (not a transition),
# so it never overrides a section's own hover transforms or transitions. Without JS or with reduced motion nothing is hidden.
REVEAL = (".s-despre .cv>.name,.s-despre .stage>.rb,.s-despre .stage>.fig,.s-despre .cap>*,.s-cefacem .cf .head,.s-cefacem .cf .panels,"
          ".s-urmator .ua .l>*,.s-urmator .ua .sw,.s-oameni .og>.wrap,.s-oameni .og>.stage,.s-faq .fq .head,"
          ".s-faq .acc>details,.s-faq .other,.s-footer .f3 .card,.s-footer .f3 .grid>*")
REVEAL_CSS = ("@keyframes rv-in{from{opacity:0;translate:0 16px}to{opacity:1;translate:none}}"
              ".acasa.rv-on .rv{opacity:0}.acasa.rv-on .rv.in{animation:rv-in .8s cubic-bezier(.22,1,.36,1) both}"
              # Vali (11 nov): the two roles in 'Despre' glide in from their own side, a little slower
              "@keyframes rv-l{from{opacity:0;translate:-48px 0}to{opacity:1;translate:none}}"
              "@keyframes rv-r{from{opacity:0;translate:48px 0}to{opacity:1;translate:none}}"
              ".acasa.rv-on .s-despre .rb.a.in{animation:rv-l 1.1s cubic-bezier(.22,1,.36,1) .15s both}"
              ".acasa.rv-on .s-despre .rb.b.in{animation:rv-r 1.1s cubic-bezier(.22,1,.36,1) .3s both}")
REVEAL_MOUNT = """(function (self) {
    if (!window.IntersectionObserver || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    self.io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); self.io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
    var setup = function () {
      var main = document.querySelector('main.acasa');
      if (!main) return;
      main.classList.add('rv-on');
      main.querySelectorAll('REVEAL_SEL').forEach(function (el) {
        if (el.classList.contains('in')) return;
        var i = 0, s = el.previousElementSibling;
        while (s) { if (s.matches('REVEAL_SEL')) i++; s = s.previousElementSibling; }
        el.style.animationDelay = Math.min(i, 4) * 80 + 'ms';
        el.classList.add('rv');
        self.io.observe(el);
      });
    };
    setup(); self.t = setTimeout(setup, 800);   // sections arrive through <dc-import>; catch late ones
    })(this);""".replace("REVEAL_SEL", REVEAL)
REVEAL_UNMOUNT = "clearTimeout(this.t); if (this.io) this.io.disconnect();"

# Vali (11 nov): Header 1 (glass pill) follows the page; its menu is the bottom sheet. Source: header_options.py
from header_options import acasa_parts
HX_CSS, HX_HEAD, HX_SHEET, hx_js = acasa_parts()
ACASA_JS = hx_js(REVEAL_MOUNT, REVEAL_UNMOUNT)
HX_CSS += "html{scroll-padding-top:88px}"   # anchors land below the pill

if __name__ == "__main__":
    for name, sc, _, _ in SECTIONS:
        print(("scoped " if scope_file(name, sc) else "already scoped ") + name)
    dh, mh = 7021, 8193   # measured in the browser (Literata, 13 nov) (section boards' own heights differ a little once stacked)
    imports = "\n".join(
        f'<dc-import name="Popup3Plic" embed="1" delay="8000" hint-size="100%,0px"></dc-import>' if n == "Popup3Plic"
        else f'<dc-import name="{n}" hint-size="100%,{d}px"></dc-import>' for n, _, d, _ in SECTIONS)
    open(os.path.join(P, "Acasa.dc.html"), "w", encoding="utf-8").write(
        page("Acasă", f'<main class="acasa hxv v1" style="background: #F4EDE4">\n{HX_HEAD}\n{imports}\n{HX_SHEET}\n</main>', 1440, dh, ACASA_JS,
             ACASA_CSS + REVEAL_CSS + HX_CSS))
    open(os.path.join(P, "AcasaMobil.dc.html"), "w", encoding="utf-8").write(
        page("Acasă: mobil", f'<div style="width: 390px; background: #F4EDE4">\n<dc-import name="Acasa" hint-size="390px,{mh}px"></dc-import>\n</div>', 390, mh, STATIC))
    print("Acasa", dh, "AcasaMobil", mh)
