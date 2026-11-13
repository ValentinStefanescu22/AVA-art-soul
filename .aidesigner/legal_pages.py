"""The legal pages on the canvas, read straight from docs/texte-legale.md (Vali, 12 nov: „Da, pe canvas”), so the text
lives in one place: edit the doc, re-run this. Laid out in reading template 1 (table of contents on the left) until a
template is chosen; text_options.py takes the „Înscriere” page from here too, so its four variants stay in sync.

usage: python3 .aidesigner/legal_pages.py
writes .aidesigner/canvas/project/Legal{Inscriere,Termeni,Confidentialitate,Cookies}(Mobil).dc.html + opt-Legal*.html
"""
import os, re, subprocess, sys
from about_options2 import P, HERE

DOC = os.path.join(HERE, "..", "docs", "texte-legale.md")
KEYS = {"Înscriere, plată și anulare": "LegalInscriere", "Termeni și condiții": "LegalTermeni",
        "Politica de confidențialitate": "LegalConfidentialitate", "Cookies": "LegalCookies"}
HREF = {"inscriere-plata-si-anulare": "#inscrieri", "termeni-si-conditii": "#termeni", "politica-de-confidentialitate": "#confidentialitate", "cookies": "#cookies"}


def inline(t):
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"\*(.+?)\*", r"<i>\1</i>", t)
    t = re.sub(r"\[([^\]]+)\]\(#([^)]+)\)", lambda m: f'<a href="{HREF.get(m.group(2), "#" + m.group(2))}">{m.group(1)}</a>', t)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', t)
    return re.sub(r"\[([^\]]+)\]", r'<span class="todo">[\1]</span>', t)


def blocks(lines):
    """paragraphs, '- ' lists, '| ' tables; lines ending without blank join into one paragraph (<br> kept for addresses)"""
    out, i = [], 0
    while i < len(lines):
        l = lines[i]
        if not l.strip():
            i += 1
        elif l.startswith("- "):
            items = []
            while i < len(lines) and lines[i].startswith("- "):
                items.append(inline(lines[i][2:])); i += 1
            out.append("<ul>" + "".join(f"<li>{x}</li>" for x in items) + "</ul>")
        elif l.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                if not re.match(r"^\|[-| ]+\|$", lines[i]):
                    rows.append([c.strip() for c in lines[i].strip("|").split("|")])
                i += 1
            head, body = rows[0], rows[1:]
            out.append('<div class="tw"><table><thead><tr>' + "".join(f"<th>{inline(h)}</th>" for h in head) + "</tr></thead><tbody>"
                       + "".join("<tr>" + "".join(f'<td data-l="{head[j]}">{inline(c)}</td>' for j, c in enumerate(r)) + "</tr>" for r in body) + "</tbody></table></div>")
        else:
            para = []
            while i < len(lines) and lines[i].strip() and not lines[i].startswith(("- ", "|")):
                para.append(inline(lines[i].strip())); i += 1
            out.append("<p>" + "<br>".join(para) + "</p>")
    return "".join(out)


def slug(t):
    t = t.lower()
    for a, b in zip("ăâîșțş", "aaistts"):
        t = t.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", re.sub(r"^\d+\.\s*", "", t)).strip("-")


def parse():
    """{title: dict(updated, summary[list], sections[(id, title, html)])} from the doc's '## ' pages"""
    text = open(DOC, encoding="utf-8").read()
    pages = {}
    for chunk in re.split(r"\n## ", text)[1:]:
        title, _, rest = chunk.partition("\n")
        title = title.strip()
        if title not in KEYS:
            continue
        rest = rest.split("\n---")[0]
        upd = re.search(r"^\*(Ultima actualizare:.*)\*$", rest, re.M)
        summ = re.search(r"\*\*Pe scurt\*\*\n((?:- .*\n?)+)", rest)
        secs = []
        for s in re.split(r"\n### ", rest)[1:]:
            st, _, sb = s.partition("\n")
            secs.append((slug(st), re.sub(r"^\d+\.\s*", "", st.strip()), blocks(sb.strip("\n").split("\n"))))
        pages[title] = dict(updated=inline(upd.group(1)) if upd else "",
                            summary=[inline(x[2:]) for x in summ.group(1).strip().split("\n")] if summ else [], sections=secs)
    return pages


PAGES = parse()
# preview heights, measured in the browser (desktop 1440, phone 390); re-measure after big text changes
H = {"LegalInscriere": (2426, 2878), "LegalTermeni": (4570, 5967), "LegalConfidentialitate": (3640, 5423), "LegalCookies": (1961, 2429)}

LEGAL_CSS = """
.tx .s ul{margin:0 0 14px;padding:0 0 0 2px;list-style:none;max-width:66ch}
.tx .s li{position:relative;padding:4px 0 4px 22px;font-size:17px;line-height:1.65;color:#3F2F25}
.tx .s li::before{content:"";position:absolute;left:2px;top:15px;width:7px;height:7px;border-radius:50%;box-shadow:inset 0 0 0 1.5px #B4583A}
.tx .s a{color:var(--terra-d);text-decoration:underline;text-underline-offset:3px}
.tx .s b{font-weight:600;color:var(--ink)}
.tx .tw{margin:6px 0 18px;overflow-x:auto}
.tx table{width:100%;border-collapse:collapse;font-size:15px;line-height:1.5}
.tx th{padding:10px 12px;text-align:left;font:400 italic 16px/1.3 var(--display);font-variation-settings:'opsz' 20;color:var(--terra-d);border-bottom:1px solid rgba(58,42,32,.25)}
.tx td{padding:12px;vertical-align:top;color:#3F2F25;border-bottom:1px solid rgba(58,42,32,.12)}
.tx td:first-child{font-weight:500;color:var(--ink)}
@media (max-width:980px){.tx .s li{font-size:16px}
  .tx table,.tx tbody,.tx tr,.tx td{display:block}.tx thead{display:none}
  .tx tr{padding:14px 0;border-bottom:1px solid rgba(58,42,32,.16)}.tx td{padding:3px 0;border:0}
  .tx td::before{content:attr(data-l);display:block;font:400 italic 14px/1.3 var(--display);color:var(--terra-d)}}
"""

if __name__ == "__main__":
    import grup_hero_options as gh
    import text_options as to
    gh.script = lambda *a, **k: to.script()
    css1 = to.TEXT_CSS + to.LECT["Lectura1Cuprins"][1] + LEGAL_CSS
    for title, key in KEYS.items():
        pg = PAGES[title]
        sec = pg["sections"]
        html = (f'<section class="gp tx l1" aria-labelledby="gh-h" ref="{{{{ secRef }}}}"><div class="wrap"><h1 class="disp gh" id="gh-h">{title}</h1><p class="upd">{pg["updated"]}</p>'
                f'<div class="stage">{to.toc([(k, t, None, None) for k, t, _ in sec])}<article class="art">'
                + (f'<div class="sum"><p class="tl">Pe scurt</p><ul>{"".join(f"<li>{x}</li>" for x in pg["summary"])}</ul></div>' if pg["summary"] else "")
                + "".join(f'<section class="s" id="{k}"><h2><span class="nm">{i + 1:02d}</span>{t}</h2>{h}</section>' for i, (k, t, h) in enumerate(sec))
                + "</article></div></div></section>")
        gh.SOURCES[key] = "docs/texte-legale.md, în șablonul de lectură 1 (cuprins alături) până alegi șablonul"
        for suffix, w, h in (("", 1440, H[key][0]), ("Mobil", 390, H[key][1])):
            f = os.path.join(P, f"{key}{suffix}.dc.html")
            doc = gh.page(key, title + (" · mobil" if suffix else ""), "light", css1, html, w, h)
            doc = doc.replace('<a href="#ce-facem" aria-haspopup="true" aria-current="page">', '<a href="#ce-facem" aria-haspopup="true">')
            open(f, "w", encoding="utf-8").write(doc)
            if not suffix:
                subprocess.run([sys.executable, os.path.join(HERE, "dc2html.py"), f, os.path.join(HERE, f"opt-{key}.html")], check=True, capture_output=True)
        print("wrote", key, len(sec), "sections")
