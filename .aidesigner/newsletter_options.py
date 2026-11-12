"""Acasă: the closing block (newsletter + contact) and the newsletter pop-up (Vali, 11 nov). Three of each:
Final1 Închis      dark 'lut ars' band that bookends the dark hero; form on the right, contact row underneath.
Final2 Carte poștală  a postcard: message on the left, the brand stamp + the email 'address line' on the right.
Final3 Cu poză     real October photo on the left, form + contact on the right.
Popup1 Cu poză     modal, photo + form (mobile: bottom sheet).
Popup2 Colț        small card bottom-right, no backdrop, Alessia's stamp photo (mobile: floating card at the bottom).
Popup3 Plic        modal with the brand stamp and a large '5%' (mobile: bottom sheet).
Copy: block 7 of Acasă ('Află primele despre atelierele noi' + contact), Evenimente (5% discount, 'Lasă-ne emailul'),
Contact (email, phone, Instagram). Mine, to approve: the 5% line wording, field label, consent text, 'Nu acum', thank-you.
Pop-up rules (production, not in these mocks): after ~8 s or 40% scroll, whichever first; once per visitor; after
'Nu acum' / × not again for 30 days; never after subscribing or on legal / checkout pages. The mocks open after 1.2 s.

Vali chose Final 2 + Pop-up 3 (11 nov); final2_options.py makes the Final 2 variants.

usage: python3 .aidesigner/newsletter_options.py
"""
import os, re, subprocess, sys
from about_options2 import P, HERE, FONTS, BASE_CSS, ARROW, BG, DUO_SQ

VASE = re.search(r"^VASE = '(.*)'$", open(os.path.join(HERE, "hero_options.py"), encoding="utf-8").read(), re.M).group(1)
PHOTO = "/_blob/988e3a505fd5ae1db56d481b3d1e33b1"   # real, October workshop
PHOTO_ALT = "Atelierul din octombrie: oameni în jurul unei mese cu lut, ceai și prăjitură"
PHOTO2 = "/_blob/42c18be93cd80d91d6d1d16793e790c6"  # real, October: a bowl passed between hands
PHOTO2_ALT = "Doi participanți își dau din mână în mână un bol de lut, la atelierul din octombrie"

NL_H = "Rămâi aproape…"   # Vali (11 nov): like „Ține-mă la curent”, but more elegant; was „Află primele despre atelierele noi”
NL_5 = "Vești despre atelierele noi, înaintea tuturor, și 5% discount la următorul eveniment."  # block 7 + Evenimente
NL_SUB = "Vești despre atelierele noi, înaintea tuturor."
LABEL = "Emailul tău"
BTN = "Abonează-te"
CONSENT = 'Sunt de acord să primesc emailuri de la AVA Art &amp; Soul. Am citit <a href="#confidentialitate">Politica de confidențialitate</a>.'
NOT_NOW = "Nu acum"
CONTACT = [("Email", "ava.events.26@gmail.com", "mailto:ava.events.26@gmail.com"),
           ("Telefon / WhatsApp", "0730 301 996", "tel:+40730301996"),
           ("Instagram", "@ava.art.soul", "https://www.instagram.com/ava.art.soul/")]
CLOSE = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 4l8 8M12 4l-8 8" style="fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round"></path></svg>'


def bind(n):
    return "{{ " + n + " }}"


def form(fid, line=False):
    return (f'<form class="nf{" line" if line else ""}" action="#" novalidate onSubmit="{bind("submit")}">'
            f'<label class="lbl" for="{fid}">{LABEL}</label>'
            f'<div class="row"><input id="{fid}" type="email" name="email" autocomplete="email" inputmode="email" required placeholder="nume@exemplu.ro">'
            f'<button class="btn" type="submit"><span class="t1">{BTN}</span><span class="t2">Se trimite…</span></button></div>'
            f'<label class="ok"><input type="checkbox" name="acord" required><span>{CONSENT}</span></label>'
            f'<p class="done" role="status"></p></form>')


def contact(cls="ct"):
    return f'<ul class="{cls}">' + "".join(f'<li><span>{l}</span><a href="{h}">{v}</a></li>' for l, v, h in CONTACT) + "</ul>"


def seal(uid, size=120):
    ring = "AVA · ART &amp; SOUL · AUTOCUNOAȘTERE PRIN CREAȚIE · "
    vase = VASE.replace('<svg viewBox="0 0 64 80" aria-hidden="true">', '<svg x="38" y="34" width="44" height="52" viewBox="0 0 64 80">')
    return (f'<svg class="seal" viewBox="0 0 120 120" width="{size}" height="{size}" aria-hidden="true">'
            f'<defs><path id="{uid}" d="M60,60 m-44,0 a44,44 0 1,1 88,0 a44,44 0 1,1 -88,0"></path></defs>'
            f'<circle cx="60" cy="60" r="57" style="fill:none;stroke:currentColor;stroke-width:1.4"></circle>'
            f'<circle cx="60" cy="60" r="34" style="fill:none;stroke:currentColor;stroke-width:1.1"></circle>'
            f'<text style="font:600 7.4px var(--text);fill:currentColor"><textPath href="#{uid}" textLength="272" lengthAdjust="spacing">{ring}</textPath></text>'
            f'{vase}</svg>')


COMMON = """
.btn{display:inline-flex;align-items:center;justify-content:center;gap:10px;min-height:52px;padding:0 26px;border:0;border-radius:999px;background:var(--ink);color:#F4EDE4;font:500 15px/1 var(--text);letter-spacing:.02em;cursor:pointer;transition:background .2s,transform .15s;white-space:nowrap}
.btn:hover{background:#2A1D15}.btn:active{transform:scale(.97)}
.btn:focus-visible,.nf input:focus-visible,.x:focus-visible,.later:focus-visible,.ok a:focus-visible,.ct a:focus-visible{outline:2px solid #9C472C;outline-offset:3px}
.btn .t2{display:none}.nf[data-busy] .btn .t1{display:none}.nf[data-busy] .btn .t2{display:inline}.nf[data-busy] .btn{opacity:.7;cursor:progress}
.nf{display:flex;flex-direction:column;gap:10px;max-width:520px}
.nf .lbl{font-size:14px;font-weight:600;letter-spacing:.02em}
.nf .row{display:flex;gap:8px}
.nf input[type=email]{flex:1;min-width:0;min-height:52px;box-sizing:border-box;padding:0 20px;border:1px solid rgba(58,42,32,.28);border-radius:999px;background:#FFFDF9;color:var(--ink);font:400 16px var(--text)}
.nf input[type=email]::placeholder{color:#7E6857}
.nf .ok{display:flex;gap:10px;align-items:flex-start;margin-top:4px;font-size:13.5px;line-height:1.45;color:var(--ink2);cursor:pointer}
.nf .ok input{flex:none;width:18px;height:18px;margin:1px 0 0;accent-color:#9C472C}
.nf .ok a{color:inherit;text-underline-offset:3px}
.nf .done{display:none;margin:0;font:400 italic 22px/1.3 var(--display);font-variation-settings:'opsz' 20}
.nf[data-sent]>*:not(.done){display:none}.nf[data-sent] .done{display:block}
.nf[data-err] .ok span,.nf[data-err] input[type=email]:invalid{color:#9C472C;border-color:#9C472C}
.ct{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:16px 48px}
.ct li{display:flex;flex-direction:column;gap:2px}
.ct span{font-size:13px;color:var(--ink2);letter-spacing:.02em}
.ct a{display:inline-flex;align-items:center;min-height:36px;color:var(--ink);font-weight:500;text-decoration:none;font-variant-numeric:tabular-nums;background:linear-gradient(currentColor,currentColor) 0 calc(100% - 6px)/0 1px no-repeat;transition:background-size .3s cubic-bezier(.2,.7,.2,1)}
.ct a:hover{background-size:100% 1px}
.nl{padding:120px 0}
.nl h2{font-size:clamp(40px,4.6vw,66px);line-height:1.02}
.nl .five{margin:18px 0 0;font-size:18px;color:var(--ink2);max-width:36ch}
@media (max-width:820px){.nl{padding:76px 0}.nl h2{font-size:clamp(36px,10vw,46px)}.nf .row{flex-direction:column}.nf .btn{width:100%}.ct{flex-direction:column;gap:10px}}
"""

FINALS = {}
FINALS["Final1Inchis"] = ("Final 1: bandă închisă", "Aesop (footerul închis, cu abonare)", """
.n1{background:#3A2A20;color:#F4EDE4}
.n1 .grid{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:80px;align-items:end}
.n1 .five{color:#D9C7B4}
.n1 .nf .lbl{color:#F4EDE4}
.n1 .nf input[type=email]{background:rgba(244,237,228,.06);border-color:rgba(244,237,228,.32);color:#F4EDE4}
.n1 .nf input[type=email]::placeholder{color:#A8927E}
.n1 .btn{background:#F4EDE4;color:#3A2A20}.n1 .btn:hover{background:#FFF8EE}
.n1 .nf .ok{color:#D9C7B4}.n1 .nf .done{color:#F2C79C}
.n1 .nf[data-err] .ok span{color:#F2C79C}
.n1 .bottom{margin-top:88px;padding-top:30px;border-top:1px solid rgba(244,237,228,.16)}
.n1 .ct span{color:#BFA992}.n1 .ct a{color:#F4EDE4}
@media (max-width:820px){.n1 .grid{grid-template-columns:1fr;gap:36px}.n1 .bottom{margin-top:56px}}
""", f"""<section class="nl n1" id="newsletter" aria-labelledby="nl-h" ref="{bind("rootRef")}"><div class="wrap">
<div class="grid"><div><h2 class="disp" id="nl-h">{NL_H}</h2><p class="five">{NL_5}</p></div>{form("nl-e1")}</div>
<div class="bottom">{contact()}</div>
</div></section>""")

FINALS["Final2CartePostala"] = ("Final 2: carte poștală", "cărțile poștale + ștampila din hero; Framer: Envelope Popup", """
.n2{background:linear-gradient(180deg,#F4EDE4 0%,#EDE0CD 100%)}
.n2 .card{position:relative;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);max-width:1060px;margin:0 auto;padding:56px 0;border-radius:16px;corner-shape:squircle;background:#FBF7F0;box-shadow:0 1px 0 rgba(58,42,32,.06),0 40px 80px -56px rgba(70,35,15,.55)}
.n2 .l{padding:0 56px;border-right:1px solid rgba(58,42,32,.16)}
.n2 .sig{margin:30px 0 0;font:400 40px/1 var(--script);color:#9C472C}
.n2 .r{position:relative;padding:118px 56px 0}
.n2 .seal{position:absolute;top:-8px;right:48px;color:#9C472C;transform:rotate(-8deg)}
.n2 .nf.line .row{flex-direction:column;align-items:flex-start;gap:20px}
.n2 .nf.line input[type=email]{width:100%;flex:none;padding:0 2px;border:0;border-bottom:1px solid rgba(58,42,32,.4);border-radius:0;background:none;font:400 22px var(--display);font-variation-settings:'opsz' 20}
.n2 .nf.line input[type=email]:focus-visible{outline:none;border-bottom:2px solid #9C472C}
.n2 .ct{justify-content:center;margin-top:44px;text-align:center}
.n2 .ct li{align-items:center}
@media (max-width:820px){.n2 .card{grid-template-columns:1fr;padding:36px 0 32px}.n2 .l{padding:0 24px 28px;border-right:0;border-bottom:1px solid rgba(58,42,32,.16)}.n2 .sig{margin-top:18px;font-size:28px}.n2 .l{padding-bottom:36px}
.n2 .r{padding:28px 24px 0}.n2 .seal{width:84px;height:84px;top:-36px;right:16px}.n2 .l h2{padding-right:70px}.n2 .ct{justify-content:flex-start;text-align:left;margin-top:36px}.n2 .ct li{align-items:flex-start}}
""", f"""<section class="nl n2" id="newsletter" aria-labelledby="nl-h" ref="{bind("rootRef")}"><div class="wrap">
<div class="card"><div class="l"><h2 class="disp" id="nl-h">{NL_H}</h2><p class="five">{NL_5}</p><p class="sig">– Alessia Văideanu</p></div>
<div class="r">{seal("sr2")}{form("nl-e2", line=True)}</div></div>
{contact()}
</div></section>""")

FINALS["Final3CuPoza"] = ("Final 3: cu poză", "Framer: Exit Popups (layout cu imagine în stânga), aplicat ca secțiune", """
.n3{background:#F4EDE4}
.n3 .grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:80px;align-items:center}
.n3 .ph{height:560px;border-radius:26px;corner-shape:squircle;overflow:hidden}
.n3 .ph img{display:block;width:100%;height:100%;object-fit:cover;object-position:50% 55%}
.n3 .nf{margin-top:36px}
.n3 .ct{margin-top:48px;padding-top:26px;border-top:1px solid rgba(58,42,32,.16);gap:16px 36px}
@media (max-width:820px){.n3 .grid{grid-template-columns:1fr;gap:32px}.n3 .ph{height:260px;order:2}.n3 .r{order:1}.n3 .nf{margin-top:28px}}
""", f"""<section class="nl n3" id="newsletter" aria-labelledby="nl-h" ref="{bind("rootRef")}"><div class="wrap grid">
<div class="ph"><img src="{PHOTO}" alt="{PHOTO_ALT}"></div>
<div class="r"><h2 class="disp" id="nl-h">{NL_H}</h2><p class="five">{NL_5}</p>{form("nl-e3")}{contact()}</div>
</div></section>""")

# ---------- pop-ups ----------
POP_COMMON = """
.stagebg{position:relative;min-height:100vh;background:#3A2A20 url(""" + BG + """) 50% 50%/cover}
.stagebg.embed{display:none}
.stagebg::after{content:"";position:absolute;inset:0;background:rgba(42,20,12,.35)}
.stagebg .ph-h{position:relative;z-index:1;margin:0;padding:200px 40px 0;text-align:center;color:#F4EDE4;font:400 clamp(44px,6vw,88px)/1 var(--display);font-variation-settings:'opsz' 20}
.replay{position:fixed;left:16px;bottom:16px;z-index:1;min-height:40px;padding:0 16px;border:1px dashed rgba(244,237,228,.6);border-radius:999px;background:rgba(42,20,12,.6);color:#F4EDE4;font:500 13px var(--text);cursor:pointer}
dialog.pop{box-sizing:border-box;margin:auto;padding:0;border:0;border-radius:26px;corner-shape:squircle;background:#FBF7F0;color:var(--ink);box-shadow:0 40px 100px -40px rgba(20,8,4,.7);
opacity:0;transform:translateY(18px) scale(.98);transition:opacity .35s,transform .45s cubic-bezier(.2,.7,.2,1),overlay .35s allow-discrete,display .35s allow-discrete}
dialog.pop[open]{opacity:1;transform:none}
dialog.pop:focus{outline:none}
@starting-style{dialog.pop[open]{opacity:0;transform:translateY(18px) scale(.98)}}
dialog.pop::backdrop{background:rgba(30,14,8,0);transition:background .35s,overlay .35s allow-discrete,display .35s allow-discrete}
dialog.pop[open]::backdrop{background:rgba(30,14,8,.5)}
@starting-style{dialog.pop[open]::backdrop{background:rgba(30,14,8,0)}}
.x{position:absolute;top:14px;right:14px;z-index:2;display:grid;place-items:center;width:44px;height:44px;padding:0;border:0;border-radius:50%;background:rgba(251,247,240,.9);color:var(--ink);cursor:pointer}
.x svg{width:16px;height:16px}.x:hover{background:#fff}
.later{align-self:flex-start;min-height:44px;padding:0;border:0;background:none;color:var(--ink2);font:500 14px var(--text);text-decoration:underline;text-underline-offset:4px;cursor:pointer}
.pop h2{font:400 32px/1.1 var(--display);font-variation-settings:'opsz' 20;letter-spacing:-.01em;margin:0;text-wrap:balance}
.pop .five{margin:12px 0 22px;color:var(--ink2)}
.grab{display:none}
@media (max-width:820px){
.stagebg .ph-h{padding-top:140px;font-size:44px}
dialog.pop{width:100%;max-width:none;max-height:86vh;margin:auto 0 0;border-radius:24px 24px 0 0;transform:translateY(100%);overflow:auto;padding-bottom:env(safe-area-inset-bottom)}
@starting-style{dialog.pop[open]{opacity:0;transform:translateY(100%)}}
dialog.pop[open]{transform:translateY(var(--dy,0px))}
dialog.pop[data-drag]{transition:none}
.grab{display:block;position:sticky;top:0;z-index:3;height:28px;touch-action:none;cursor:grab}
.grab::before{content:"";position:absolute;left:50%;top:10px;width:40px;height:4px;margin-left:-20px;border-radius:2px;background:rgba(58,42,32,.25)}
.pop h2{font-size:27px}.nf .row{flex-direction:column}.nf .btn{width:100%}}
@media (prefers-reduced-motion:reduce){dialog.pop,dialog.pop::backdrop{transition:none}}
"""

POPS = {}
POPS["Popup1CuPoza"] = ("Pop-up 1: cu poză", "Framer: Exit Popups (imagine în stânga), Newsletter Modal Pop", """
dialog.p1{width:min(820px,calc(100% - 48px))}
.p1 .in{display:grid;grid-template-columns:330px minmax(0,1fr)}
.p1 .ph{min-height:440px;overflow:hidden;border-radius:26px 0 0 26px}
.p1 .ph img{display:block;width:100%;height:100%;object-fit:cover;object-position:40% 50%}
.p1 .tx{display:flex;flex-direction:column;padding:56px 44px 32px}
.p1 .later{margin-top:10px}
@media (max-width:820px){dialog.p1{width:100%}.p1 .in{grid-template-columns:1fr}.p1 .ph{min-height:0;height:150px;margin:0 16px;border-radius:18px}.p1 .tx{padding:22px 22px 18px}.p1 .x{top:34px;right:24px}}
""", f"""<dialog class="pop p1" tabindex="-1" aria-labelledby="pp-h" ref="{bind("dlgRef")}" onCancel="{bind("cancel")}">
<div class="grab" aria-hidden="true" onPointerDown="{bind("drag")}"></div>
<button class="x" type="button" aria-label="Închide" onClick="{bind("close")}">{CLOSE}</button>
<div class="in"><div class="ph"><img src="{PHOTO2}" alt="{PHOTO2_ALT}"></div>
<div class="tx"><h2 id="pp-h">{NL_H}</h2><p class="five">{NL_5}</p>{form("pp-e1")}<button class="later" type="button" onClick="{bind("close")}">{NOT_NOW}</button></div></div>
</dialog>""", True)

POPS["Popup2Colt"] = ("Pop-up 2: colț discret", "Framer: Timed Popup, Newsletter Card", """
.p2{position:fixed;right:24px;bottom:24px;z-index:5;box-sizing:border-box;width:380px;padding:26px 24px 18px;border-radius:24px;corner-shape:squircle;background:#FBF7F0;color:var(--ink);box-shadow:0 30px 70px -30px rgba(20,8,4,.6);
opacity:0;transform:translateY(24px);visibility:hidden;transition:opacity .35s,transform .45s cubic-bezier(.2,.7,.2,1),visibility 0s .45s}
.p2[data-open]{opacity:1;transform:none;visibility:visible;transition-delay:0s}
.p2 .top{display:flex;gap:14px;align-items:center;margin-bottom:14px;padding-right:40px}
.p2 .av{flex:none;width:52px;height:52px;border-radius:50%;object-fit:cover;box-shadow:0 0 0 2px #F2C79C}
.p2 h2{font-size:23px;line-height:1.15}
.p2 .five{margin:0 0 16px;font-size:15px}
.p2 .x{top:8px;right:8px}
.p2 .nf .row{flex-direction:column}.p2 .btn{width:100%}
.p2 .nf input[type=email]{min-height:48px}.p2 .btn{min-height:48px}
@media (max-width:820px){.p2{left:12px;right:12px;bottom:12px;width:auto;padding:20px 18px 12px;transform:translateY(calc(100% + 24px))}.p2 .top{margin-bottom:10px}.p2 .av{width:44px;height:44px}.p2 h2{font-size:21px}.p2 .five{margin-bottom:12px}
.p2 .nf .lbl{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}}
@media (prefers-reduced-motion:reduce){.p2{transition:none}}
""", f"""<aside class="pop p2" aria-labelledby="pp-h" ref="{bind("dlgRef")}">
<button class="x" type="button" aria-label="Închide" onClick="{bind("close")}">{CLOSE}</button>
<div class="top"><img class="av" src="{DUO_SQ}" alt=""><h2 id="pp-h">{NL_H}</h2></div>
<p class="five">{NL_5}</p>{form("pp-e2")}
</aside>""", False)

POPS["Popup3Plic"] = ("Pop-up 3: plic cu ștampilă", "Framer: Envelope Popup; ștampila din hero", """
dialog.p3{width:min(480px,calc(100% - 48px));overflow:visible}
.p3 .tx{position:relative;display:flex;flex-direction:column;padding:52px 40px 28px}
.p3 .seal{position:absolute;top:-34px;left:34px;color:#9C472C;background:#FBF7F0;border-radius:50%;transform:rotate(-8deg)}
.p3 .x{top:12px;right:12px}
.p3 .sub{margin:10px 0 0;color:var(--ink2)}
.p3 .big{display:flex;align-items:center;gap:16px;margin:18px 0 24px}
.p3 .big b{display:flex;align-items:flex-start;font:400 96px/.8 var(--display);font-variation-settings:'opsz' 96;color:#9C472C;letter-spacing:-.03em}
.p3 .big small{margin:2px 0 0 4px;font:500 34px/1 var(--text);letter-spacing:0}
.p3 .big span{font-size:17px;line-height:1.4;color:var(--ink2);max-width:17ch}
.p3 h2{margin-top:44px}
.p3 .later{margin-top:8px}
@media (max-width:820px){dialog.p3{width:100%;overflow:auto}.p3 .tx{padding:8px 22px 18px}.p3 .seal{position:static;width:76px;height:76px;margin-bottom:6px}.p3 h2{margin-top:6px}.p3 .big b{font-size:72px}}
""", f"""<dialog class="pop p3" tabindex="-1" aria-labelledby="pp-h" ref="{bind("dlgRef")}" onCancel="{bind("cancel")}">
<div class="grab" aria-hidden="true" onPointerDown="{bind("drag")}"></div>
<button class="x" type="button" aria-label="Închide" onClick="{bind("close")}">{CLOSE}</button>
<div class="tx">{seal("sr3", 104)}<h2 id="pp-h">{NL_H}</h2><p class="sub">{NL_SUB}</p>
<p class="big"><b>5<small>%</small></b><span>discount la următorul eveniment</span></p>{form("pp-e3")}<button class="later" type="button" onClick="{bind("close")}">{NOT_NOW}</button></div>
</dialog>""", True)

JS = """class Component extends DCLogic {
  componentDidMount() {
    var self = this;
    if (this.dlg) this.t = setTimeout(function () { self.open(); }, parseInt(this.props.delay, 10) || 1200);  // production: ~8 s or 40% scroll, once per visitor
  }
  componentWillUnmount() { clearTimeout(this.t); }
  renderVals() {
    var self = this;
    if (!this.cb) {
      this.open = function () {
        var d = self.dlg; if (!d) return;
        if (d.showModal) { d.showModal(); d.focus({ preventScroll: true }); } else d.setAttribute('data-open', '');  // focus the dialog, not the close button
      };
      this.shut = function () {
        var d = self.dlg; if (!d) return;
        d.style.removeProperty('--dy');
        if (d.close) d.close(); else d.removeAttribute('data-open');
      };
      this.cb = {
        stageCls: self.props.embed ? 'embed' : '',  // inside Acasă: no mock background, no replay button
        rootRef: function (el) { self.root = el; },
        dlgRef: function (el) { self.dlg = el; },
        close: function () { self.shut(); },
        cancel: function () { self.dlg && self.dlg.style.removeProperty('--dy'); },
        replay: function () { self.shut(); setTimeout(self.open, 400); },
        // bottom sheet: drag the handle down to close
        drag: function (e) {
          var d = self.dlg, y0 = e.clientY, dy = 0;
          d.setAttribute('data-drag', '');
          function mv(ev) { dy = Math.max(0, ev.clientY - y0); d.style.setProperty('--dy', dy + 'px'); }
          function up() {
            window.removeEventListener('pointermove', mv); window.removeEventListener('pointerup', up);
            d.removeAttribute('data-drag');
            if (dy > 90) self.shut(); else d.style.setProperty('--dy', '0px');
          }
          window.addEventListener('pointermove', mv); window.addEventListener('pointerup', up);
        },
        submit: function (e) {
          e.preventDefault();
          var f = e.currentTarget;
          if (!f.checkValidity()) { f.setAttribute('data-err', ''); f.reportValidity(); return; }
          f.removeAttribute('data-err'); f.setAttribute('data-busy', '');
          var b = f.querySelector('.btn'); b.disabled = true;
          setTimeout(function () {  // mock: production posts to MailerLite
            f.removeAttribute('data-busy'); f.setAttribute('data-sent', '');
            f.querySelector('.done').textContent = 'Mulțumesc! Codul de 5% te așteaptă în email.';
          }, 700);
        }
      };
    }
    return this.cb;
  }
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
    built = []
    for name, (title, src, css, html) in FINALS.items():
        for suffix, w, h in (("", 1440, 800), ("Mobil", 390, 1100)):
            open(os.path.join(P, f"{name}{suffix}.dc.html"), "w", encoding="utf-8").write(page(title + (" · mobil" if suffix else ""), css, html, w, h))
        built.append(name)
    for name, (title, src, css, html, modal) in POPS.items():
        body = (f'<div class="stagebg {bind("stageCls")}" ref="{bind("rootRef")}"><p class="ph-h" aria-hidden="true">AVA Art &amp; Soul</p>'
                f'<button class="replay" type="button" onClick="{bind("replay")}">Arată pop-up-ul din nou (doar în machetă)</button></div>\n{html}')
        for suffix, w, h in (("", 1440, 900), ("Mobil", 390, 844)):
            open(os.path.join(P, f"{name}{suffix}.dc.html"), "w", encoding="utf-8").write(page(title + (" · mobil" if suffix else ""), POP_COMMON + css, body, w, h))
        built.append(name)
    for name in built:
        subprocess.run([sys.executable, os.path.join(HERE, "dc2html.py"), os.path.join(P, f"{name}.dc.html"), os.path.join(HERE, f"opt-{name}.html")], check=True)
    open(os.path.join(HERE, "nl-mobil.html"), "w").write('<!doctype html><meta charset="utf-8"><title>Newsletter mobil</title><style>body{margin:0;padding:10px;background:#1b1b1b;display:flex;gap:12px;color:#ddd;font:13px system-ui}figure{margin:0;flex:none}iframe{width:390px;height:1100px;border:0;display:block}</style>' + "".join(f'<figure><figcaption>{n}</figcaption><iframe src="opt-{n}.html"></iframe></figure>' for n in built))
