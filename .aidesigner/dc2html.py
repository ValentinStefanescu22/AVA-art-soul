"""Turn a canvas .dc.html artboard into a plain HTML page for the local design-preview server.

usage: python3 .aidesigner/dc2html.py .aidesigner/canvas/project/Acasa.dc.html .aidesigner/acasa.html
ponytail: handles {{ }} attributes, refs, events, setState and <dc-import> (each child gets its own component,
bound to its own subtree; string attributes become props); no <sc-for>/<sc-if>.
"""
import html, json, os, re, sys

src, out = sys.argv[1], sys.argv[2]
DIR = os.path.dirname(src)
helmets, mounts = [], []   # mounts: (script, props)


def attr(m):
    name, val = m.group(1), m.group(2)
    if name == "ref":
        return f' data-dc-ref="{val.strip("{} ")}"'
    if re.fullmatch(r"on[A-Z]\w+", name):
        return f' data-dc-on-{name[2:].lower()}="{val.strip("{} ")}"'
    return f' data-dc-t-{name}="{val}"'


def load(path, extra_props):
    s = open(path, encoding="utf-8").read()
    helmet = re.search(r"<helmet>(.*?)</helmet>", s, re.S).group(1)
    if helmet not in helmets:
        helmets.append(helmet)
    body = re.search(r"<x-dc>(.*?)</x-dc>", s, re.S).group(1).replace(helmet, "").replace("<helmet></helmet>", "")
    assert not re.search(r"<(sc-for|sc-if)\b", body), "unsupported DC tag"
    script = re.search(r'<script type="text/x-dc"[^>]*>(.*?)</script>', s, re.S)
    props = json.loads(html.unescape(re.search(r"data-props='([^']*)'", s).group(1)))
    defaults = {k: v["default"] for k, v in props.items() if isinstance(v, dict) and "default" in v}
    defaults.update(extra_props)
    idx = len(mounts)
    mounts.append((script.group(1) if script else "class Component extends DCLogic { renderVals(){ return {}; } }", defaults))

    def child(m):
        attrs = dict(re.findall(r'([\w-]+)="([^"]*)"', m.group(1)))
        name = attrs.pop("name")
        attrs.pop("hint-size", None)
        props = {re.sub(r"-(\w)", lambda x: x.group(1).upper(), k): v for k, v in attrs.items() if "{{" not in v}
        return load(os.path.join(DIR, name + ".dc.html"), props)

    body = re.sub(r'\s([\w:-]+)="([^"]*\{\{[^"]*)"', attr, body)   # own holes first, then splice children in
    body = re.sub(r"<dc-import\b([^>]*)></dc-import>", child, body)
    return f'<div data-dc-mount="{idx}" style="display:contents">{body}</div>'


page = load(src, {})
shim = """
class DCLogic { constructor(p){ this.props = p; this.state = {}; } setState(s){ Object.assign(this.state, s); this.__apply(); } }
function dcMount(i, Component, props){
  const root = document.querySelector('[data-dc-mount="' + i + '"]'), dc = new Component(props); let bound = false;
  dc.__apply = function(){
    const v = dc.renderVals();
    for (const el of root.querySelectorAll('*')) {
      if (el.closest('[data-dc-mount]') !== root) continue;
      for (const a of [...el.attributes]) {
        if (a.name.startsWith('data-dc-t-')) {
          const n = a.name.slice(10), val = a.value.replace(/\\{\\{\\s*([\\w.]+)\\s*\\}\\}/g, (_, k) => v[k]);
          if (!n.startsWith('aria-') && (val === 'true' || val === 'false')) val === 'true' ? el.setAttribute(n, '') : el.removeAttribute(n);
          else el.setAttribute(n, val);
        } else if (!bound && a.name === 'data-dc-ref') v[a.value](el);
        else if (!bound && a.name.startsWith('data-dc-on-')) el.addEventListener(a.name.slice(11), e => v[a.value](e));
      }
    }
    bound = true;
  };
  dc.__apply(); dc.componentDidMount && dc.componentDidMount();
}
""" + "".join(f"(function(){{\n{scr}\ndcMount({i}, Component, {json.dumps(p)});\n}})();\n" for i, (scr, p) in enumerate(mounts))

open(out, "w", encoding="utf-8").write(
    f'<!doctype html>\n<html lang="ro">\n<head>\n<meta charset="utf-8">\n'
    f'<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
    f"<title>Acasă (previzualizare)</title>\n{''.join(helmets)}\n</head>\n<body>\n{page}\n<script>{shim}</script>\n</body>\n</html>\n"
)
print("wrote", out)
