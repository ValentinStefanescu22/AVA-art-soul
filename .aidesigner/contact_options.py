"""Contact, the page (Vali, 12 nov). Four variants of the whole page (header + contact); the footer comes at assembly.
Copy: docs/continut-site.md, „Contact”: the form (nume, email, telefon opțional, „Ce te interesează?”, mesaj, bifă GDPR),
email / telefon-WhatsApp / Instagram, the area (București only, Vali 13 nov; no exact address, CLAUDE.md), „Îți răspundem în maxim
24 de ore.”. The form posts to Web3Forms in code; here sending shows the thank-you state. Other pages link here with the
topic preselected (#contact?subiect=companii), noted for the build.
Mine, to approve (MINE): the GDPR line, „Trimite mesajul”, the thank-you line, the chat lines in variant 4, „Dragă Alessia,”.
"""
import os, subprocess, sys
from about_options2 import P, HERE, ARROW, DUO
import grup_hero_options as gh
import companii_options as co
from cf_pagina_options import ENTER

TITLE = "Contact"
REPLY = "Îți răspundem în maxim 24 de ore."
EMAIL, PHONE, PHONE_TXT, IG = "ava.events.26@gmail.com", "+40730301996", "0730 301 996", "@ava.art.soul"
WHERE = "București"   # Vali (13 nov): without the area
TOPICS = ["Atelier de grup", "Pentru companii", "Consiliere", "Atelier privat", "Retreat", "Colaborare", "Altceva"]
TOPIC_Q = "Ce te interesează?"
GDPR = 'Sunt de acord ca datele mele să fie folosite ca să primesc un răspuns, conform <a href="#confidentialitate">Politicii de confidențialitate</a>.'   # MINE
SEND = "Trimite mesajul"                                                     # MINE
THANKS = "Mulțumesc! Mesajul a ajuns. " + REPLY                              # MINE (+ doc)

ICO = {
    "mail": '<path d="M4 7h16v11H4z"></path><path d="M4 8l8 6 8-6"></path>',
    "wa": '<path d="M5 19l1.2-3.6A7.5 7.5 0 1 1 9 18.3z"></path><path d="M9.5 9.5c.3 1.8 2 3.6 4 4l1-1.2 1.6.8c-.2 1.1-1 1.7-2 1.7-3 0-5.8-2.8-5.8-5.8 0-1 .6-1.8 1.7-2l.8 1.6z"></path>',
    "ig": '<rect x="4.5" y="4.5" width="15" height="15" rx="4.5"></rect><circle cx="12" cy="12" r="3.6"></circle><circle cx="16.6" cy="7.4" r=".6"></circle>',
    "pin": '<path d="M12 20s-6-5.6-6-10a6 6 0 0 1 12 0c0 4.4-6 10-6 10z"></path><circle cx="12" cy="10" r="2.2"></circle>',
}


def ic(k):
    return f'<svg class="ico" viewBox="0 0 24 24" aria-hidden="true">{ICO[k]}</svg>'


CHANNELS = [("mail", "Email", EMAIL, f"mailto:{EMAIL}"), ("wa", "Telefon / WhatsApp", PHONE_TXT, f"https://wa.me/{PHONE[1:]}"),
            ("ig", "Instagram", IG, "https://www.instagram.com/ava.art.soul/"), ("pin", "Unde", WHERE, "")]


def field(name, label, kind="text", extra=""):
    tag = (f'<textarea name="{name}" rows="5"{extra}></textarea>' if kind == "area" else f'<input type="{kind}" name="{name}"{extra}>')
    return f'<label class="fi"><span class="fl">{label}</span>{tag}</label>'


F = {"nume": field("nume", "Nume", extra=' autocomplete="name" required'),
     "email": field("email", "Email", "email", ' autocomplete="email" required'),
     "tel": field("telefon", 'Telefon <small>(opțional)</small>', "tel", ' autocomplete="tel"'),
     "msg": field("mesaj", "Mesaj", "area", " required"),
     "msg_opt": field("mesaj", 'Mesaj <small>(opțional)</small>', "area")}   # Contact 5 (Vali, 13 nov)


def topics(cls="topics", multi=False):
    """multi (Vali, 13 nov, on Contact 5): checkboxes, pick several; at least one is checked in go()"""
    kind = "checkbox" if multi else "radio"
    return (f'<fieldset class="{cls}"><legend class="fl">{TOPIC_Q}{" <small>(poți alege mai multe)</small>" if multi else ""}</legend><div class="opts">'
            + "".join(f'<label class="ch"><input type="{kind}" name="subiect" value="{t}"{" required" if i == 0 and not multi else ""}><span>{t}</span></label>' for i, t in enumerate(TOPICS))
            + "</div></fieldset>")


OK = f'<label class="ok"><input type="checkbox" name="gdpr" required><span>{GDPR}</span></label>'
SUBMIT = f'<div class="send"><button class="btn" type="submit">{SEND}</button><p class="note">{REPLY}</p></div>'
DONE = f'<p class="done" role="status" hidden>{THANKS}</p>'


def form(*parts, cls=""):
    return f'<form class="{cls}" action="#" novalidate onSubmit="{{{{ send }}}}">' + "".join(parts) + DONE + "</form>"


def channel_list(cls="chl"):
    return (f'<ul class="{cls}">' + "".join(
        f'<li>{ic(k)}<span><small>{n}</small>' + (f'<a href="{h}">{v}</a>' if h else f"<b>{v}</b>") + "</span></li>" for k, n, v, h in CHANNELS) + "</ul>")


COMMON = co.FORM_CSS + """
.ct{position:relative;background:linear-gradient(180deg,#F4EDE4 0%,#EDE0CD 100%);padding:150px 0 112px;--so:cubic-bezier(.22,1,.36,1)}
.ct a{text-decoration:none}
.ct .lede{margin:18px 0 0;color:#4A382C}
.ct .ico{width:22px;height:22px;flex:none;fill:none;stroke:currentColor;stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round}
.ct .btn{border:0;cursor:pointer}
.ct .ch input[type=radio]{position:absolute;opacity:0;width:1px;height:1px}
.ct .opts{display:flex;flex-wrap:wrap;gap:8px}
.ct .done{margin:18px 0 0;padding:16px 18px;border-radius:14px;background:rgba(111,123,92,.14);color:#3F4A35;font-size:16px}
.ct form.sent .fi,.ct form.sent fieldset,.ct form.sent .ok,.ct form.sent .send,.ct form.sent .grid{display:none}
.ct .chl{margin:0;padding:0;list-style:none}
.ct .chl li{display:flex;align-items:center;gap:16px;padding:16px 0;border-bottom:1px solid rgba(58,42,32,.14)}
.ct .chl li:first-child{border-top:1px solid rgba(58,42,32,.14)}
.ct .chl .ico{color:var(--terra-d)}
.ct .chl small{display:block;font-size:13px;color:var(--ink2)}
.ct .chl a,.ct .chl b{font:400 21px/1.3 var(--display);font-variation-settings:'opsz' 20;color:var(--ink);font-weight:400}
.ct .chl a{background:linear-gradient(currentColor,currentColor) 0 100%/0 1px no-repeat;transition:background-size .3s var(--so)}
.ct .chl a:hover{background-size:100% 1px}
.ct .ok{margin-top:18px}.ct .send{margin-top:20px}
@keyframes ct-up{from{opacity:0;translate:0 16px}}
@media (max-width:980px){.ct{padding:112px 0 72px}.ct .send{flex-direction:column;align-items:stretch;text-align:center}.ct .btn{width:100%}.ct .chl a,.ct .chl b{font-size:18px;word-break:break-word}}
@media (prefers-reduced-motion:reduce){.ct *{animation:none!important;transition:none!important}}
"""
COMMON = COMMON.replace(".of ", ".ct ").replace(".of{", ".ct{")

HEAD = f'<h1 class="disp gh" id="gh-h">{TITLE}</h1><p class="lede up" style="--d: .3s">{REPLY}</p>'
OPTS = {}

# 1. linear.app/contact: the form on the left in a card, the quiet contact details on the right.
OPTS["Contact1Coloane"] = ("Contact 1: două coloane", """
.c1x .stage{display:grid;grid-template-columns:minmax(0,7fr) minmax(0,4fr);gap:72px;align-items:start;margin-top:48px}
.c1x .card{padding:36px;border-radius:24px;corner-shape:squircle;background:#FBF7F1;box-shadow:0 0 0 1px rgba(58,42,32,.06),0 30px 60px -44px rgba(70,35,15,.5)}
.c1x .grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px}
.c1x fieldset{margin-top:24px}
.c1x .fi+.fi,.c1x form>.fi{margin-top:20px}
.c1x .side{position:sticky;top:110px}
.c1x .grid .fi{margin-top:0!important}
@media (max-width:980px){.c1x .stage{grid-template-columns:1fr;gap:40px;margin-top:28px}.c1x .card{padding:22px 18px}.c1x .grid{grid-template-columns:1fr}.c1x .side{position:static;order:-1}}
""", '<section class="gp ct c1x" aria-labelledby="gh-h" ref="{{ secRef }}"><div class="wrap">' + HEAD
    + '<div class="stage"><div class="card up" style="--d: .45s">' + form('<div class="grid">', F["nume"], F["email"], F["tel"], '</div>', topics(), F["msg"], OK, SUBMIT)
    + f'</div><aside class="side up" style="--d: .6s" aria-label="Alte căi">{channel_list()}</aside></div></div></section>')

# 2. apple.com/contact: the ways to reach you first, as big cards you can tap; the form below for longer messages.
OPTS["Contact2Canale"] = ("Contact 2: întâi căile de contact", """
.c2x .head{text-align:center}.c2x .lede{margin-left:auto;margin-right:auto}
.c2x .cards{display:grid;grid-template-columns:1.5fr 1fr 1fr 1fr;gap:14px;margin:48px 0 0;padding:0;list-style:none}
.c2x .cards a,.c2x .cards div{display:flex;flex-direction:column;gap:28px;height:100%;box-sizing:border-box;padding:24px;border-radius:22px;corner-shape:squircle;background:#FBF7F1;box-shadow:0 0 0 1px rgba(58,42,32,.06);color:var(--ink);transition:translate .4s var(--so),box-shadow .4s}
@media (hover:hover){.c2x .cards a:hover{translate:0 -3px;box-shadow:0 0 0 1px rgba(58,42,32,.08),0 22px 40px -28px rgba(58,30,15,.5)}}
.c2x .cards a:focus-visible{outline:2px solid #9C472C;outline-offset:3px}
.c2x .cards .ico{width:32px;height:32px;color:var(--terra-d)}
.c2x .cards small{display:block;font-size:13.5px;color:var(--ink2)}
.c2x .cards b{display:block;margin-top:4px;font:400 20px/1.3 var(--display);font-variation-settings:'opsz' 20;font-weight:400}
.c2x .wide{max-width:820px;margin:64px auto 0}
.c2x .wide h2{font-size:clamp(32px,3vw,44px);text-align:center}
.c2x .grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;margin-top:28px}
.c2x fieldset,.c2x form>.fi{margin-top:22px}
@media (max-width:980px){.c2x .cards{grid-template-columns:1fr 1fr;gap:8px;margin-top:28px}.c2x .cards li:first-child{grid-column:1/-1}.c2x .cards a,.c2x .cards div{gap:16px;padding:16px}.c2x .cards b{font-size:16px}.c2x .wide{margin-top:48px}.c2x .grid{grid-template-columns:1fr}}
""", '<section class="gp ct c2x" aria-labelledby="gh-h" ref="{{ secRef }}"><div class="wrap"><div class="head">' + HEAD + '</div><ul class="cards">'
    + "".join(f'<li class="up" style="--d: {.4 + i * .08:.2f}s">' + (f'<a href="{h}">' if h else "<div>") + f'{ic(k)}<span><small>{n}</small><b>{v}</b></span>' + ("</a>" if h else "</div>") + "</li>"
              for i, (k, n, v, h) in enumerate(CHANNELS))
    + '</ul><div class="wide up" style="--d: .8s"><h2 class="disp">Sau scrie-ne aici</h2>'   # MINE
    + form('<div class="grid">', F["nume"], F["email"], F["tel"], '</div>', topics(), F["msg"], OK, SUBMIT) + "</div></div></section>")

# 3. Paperless Post: the message as a letter on paper, „Dragă Alessia,” on top and your name as the signature.
OPTS["Contact3Scrisoare"] = ("Contact 3: o scrisoare", """
.c3x .stage{display:grid;grid-template-columns:minmax(0,4fr) minmax(0,7fr);gap:72px;align-items:start}
.c3x .paper{position:relative;padding:48px 52px 40px;background:#FFFCF6;border-radius:6px;box-shadow:0 2px 0 rgba(58,42,32,.04),0 40px 70px -40px rgba(70,35,15,.5);rotate:.6deg;
  background-image:repeating-linear-gradient(180deg,transparent 0 35px,rgba(58,42,32,.08) 35px 36px);background-position:0 26px}
@keyframes c3-in{from{opacity:0;rotate:-3deg;translate:0 30px}}
@media (prefers-reduced-motion:no-preference){.c3x .paper{animation:c3-in 1.1s var(--so) .3s backwards}}
.c3x .dear{margin:0 0 18px;font:400 italic 30px/1.2 var(--display);font-variation-settings:'opsz' 20}
.c3x legend{font:400 italic 18px/1.4 var(--display);font-variation-settings:'opsz' 20;color:var(--terra-d)}
.c3x .ch{background:transparent;box-shadow:inset 0 0 0 1px rgba(58,42,32,.28)}
.c3x .ch:has(input:checked){box-shadow:none}
.c3x textarea{margin-top:18px;min-height:216px;border:0;border-radius:0;background:transparent;padding:6px 0;font:400 20px/36px var(--display);font-variation-settings:'opsz' 20}
.c3x textarea:focus{box-shadow:none}
.c3x .msg .fl{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
.c3x .sig{display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;margin-top:26px}
.c3x .sig .fl{font:400 italic 16px/1.4 var(--display);font-variation-settings:'opsz' 20;color:var(--ink2)}
.c3x .sig input{border:0;border-bottom:1px solid rgba(58,42,32,.4);border-radius:0;background:transparent;padding:6px 0}
.c3x .sig input:focus{box-shadow:0 1px 0 #9C472C}
.c3x .yours{margin:28px 0 0;font:400 italic 18px/1 var(--display);font-variation-settings:'opsz' 20;color:var(--ink2)}
@media (max-width:980px){.c3x .stage{grid-template-columns:1fr;gap:32px}.c3x .paper{padding:28px 20px 24px;rotate:0deg}.c3x .dear{font-size:25px}.c3x .sig{grid-template-columns:1fr}}
""", '<section class="gp ct c3x" aria-labelledby="gh-h" ref="{{ secRef }}"><div class="wrap stage"><div>' + HEAD
    + f'<div class="up" style="--d: .5s;margin-top:36px">{channel_list()}</div></div><div class="paper">'
    + form('<p class="dear" aria-hidden="true">Dragă Alessia,</p>', topics(), F["msg"].replace('class="fi"', 'class="fi msg"'),
           '<p class="yours" aria-hidden="true">Cu drag,</p><div class="sig grid">', F["nume"], F["email"], F["tel"], '</div>', OK, SUBMIT)
    + "</div></div></section>")

# 4. Intercom's messenger: Alessia asks, you answer in the chat; the same fields, one bubble at a time.
CHAT = [("Bună! Sunt Alessia. " + TOPIC_Q, "t"), ("Cum te numești și unde îți pot răspunde?", "c"), ("Spune-mi mai multe.", "m")]   # MINE
OPTS["Contact4Chat"] = ("Contact 4: ca o conversație", """
.c4x .stage{display:grid;grid-template-columns:minmax(0,4fr) minmax(0,6fr);gap:72px;align-items:start}
.c4x .win{border-radius:28px;corner-shape:squircle;background:#FBF7F1;box-shadow:0 0 0 1px rgba(58,42,32,.06),0 40px 80px -50px rgba(70,35,15,.6);overflow:hidden}
.c4x .bar{display:flex;align-items:center;gap:12px;padding:16px 20px;background:#3A2A20;color:#F4EDE4}
.c4x .bar .av{width:40px;height:40px;border-radius:50%;overflow:hidden;background:linear-gradient(180deg,#E6D5BD 0%,#D4B894 100%)}
.c4x .bar .av img{display:block;width:100%;height:100%;object-fit:cover;object-position:50% 8%}
.c4x .bar b{display:block;font-size:15px}.c4x .bar small{font-size:13px;color:#D8C6B2}
.c4x .bar small::before{content:"";display:inline-block;width:7px;height:7px;margin-right:6px;border-radius:50%;background:#8FA06E;vertical-align:1px}
.c4x form{padding:22px 20px 22px}
.c4x .q{max-width:82%;margin:0 0 12px;padding:12px 16px;border-radius:20px 20px 20px 6px;background:#EFE3D3;font-size:16px;line-height:1.45}
.c4x .a{margin:0 0 22px auto;max-width:92%;padding:14px;border-radius:20px 20px 6px 20px;background:#FFFCF7;box-shadow:inset 0 0 0 1px rgba(58,42,32,.1)}
.c4x .a .grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.c4x .a .grid .fi:last-child{grid-column:1/-1}
.c4x legend{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
.c4x .ch{min-height:40px;font-size:14.5px}
@keyframes c4-pop{from{opacity:0;scale:.94;translate:0 8px}}
@media (prefers-reduced-motion:no-preference){.c4x .q,.c4x .a{animation:c4-pop .5s cubic-bezier(.3,1.32,.5,1) backwards;animation-delay:calc(.5s + var(--n) * .25s);transform-origin:0 100%}.c4x .a{transform-origin:100% 100%}}
.c4x .ok{margin-top:6px}
@media (max-width:980px){.c4x .stage{grid-template-columns:1fr;gap:28px}.c4x form{padding:16px 12px}.c4x .a{max-width:100%}.c4x .a .grid{grid-template-columns:1fr}}
""", '<section class="gp ct c4x" aria-labelledby="gh-h" ref="{{ secRef }}"><div class="wrap stage"><div>' + HEAD
    + f'<div class="up" style="--d: .5s;margin-top:36px">{channel_list()}</div></div><div class="win up" style="--d: .4s">'
    f'<div class="bar"><span class="av"><img src="{DUO}" alt=""></span><span><b>Alessia Văideanu</b><small>{REPLY}</small></span></div>'
    + form(f'<p class="q" style="--n: 0">{CHAT[0][0]}</p><div class="a" style="--n: 1">{topics()}</div>',
           f'<p class="q" style="--n: 2">{CHAT[1][0]}</p><div class="a" style="--n: 3"><div class="grid">{F["nume"]}{F["email"]}{F["tel"]}</div></div>',
           f'<p class="q" style="--n: 4">{CHAT[2][0]}</p><div class="a" style="--n: 5">{F["msg"]}</div>', OK, SUBMIT)
    + "</div></div></section>")

# 5. typeform.com, like the „Cere o ofertă” form chosen on Pentru companii: one question at a time in the dark card, a progress bar.
STEPS5 = [TOPIC_Q, "Spune-mi mai multe", "Cum îți răspund?"]   # 2 and 3 MINE
O4_CSS = co.OPTS["CompOferta4Pasi"][1].replace(co.FORM_CSS, "").replace(".o4", ".c5x")
NAV = '<div class="nav"><button type="button" class="back" onClick="{{ back }}">Înapoi</button><button type="button" class="btn" onClick="{{ next }}">Mai departe</button></div>'
OPTS["Contact5Pasi"] = ("Contact 5: pas cu pas (ca la Pentru companii)", O4_CSS + """
.c5x h3{margin:0;font:400 26px/1.15 var(--display);font-variation-settings:'opsz' 20;letter-spacing:-.01em}
.c5x .stage{align-items:start}
.c5x .side .chl{margin-top:36px}
.c5x textarea{min-height:180px}
.c5x .hint{margin:8px 0 0;font-size:15px;color:rgba(244,237,228,.72)}   /* MINE */
.c5x .st .fi+.fi{margin-top:16px}.c5x .st .grid .fi{margin-top:0}
.c5x .st[data-s="1"] .back{display:none}.c5x .st[data-s="1"] .nav{justify-content:flex-end}
.c5x form.sent .st{display:none!important}
.c5x form.sent .done{background:rgba(244,237,228,.1);color:#F4EDE4}
.c5x .card:has(form.sent){--s:3!important}
@media (max-width:980px){.c5x .side .chl{margin-top:24px}}
""", '<section class="gp ct c5x" aria-labelledby="gh-h" ref="{{ secRef }}"><div class="wrap stage"><div class="side">' + HEAD
    + f'<div class="up" style="--d: .5s">{channel_list()}</div></div>'
    + '<div class="card up" style="--d: .4s; --s: 1"><div class="bar"><i></i></div><p class="cnt" aria-live="polite">Pasul <b class="n">1</b> din 3</p>'
    + form(f'<div class="st on" data-s="1"><h3>{STEPS5[0]}</h3><p class="hint">Poți alege mai multe.</p>{topics(multi=True)}{NAV}</div>',
           f'<div class="st" data-s="2"><h3>{STEPS5[1]}</h3>{F["msg_opt"]}{NAV}</div>',
           f'<div class="st" data-s="3"><h3>{STEPS5[2]}</h3><div class="grid">{F["nume"]}{F["email"]}</div>{F["tel"]}{OK}'
           f'<div class="nav"><button type="button" class="back" onClick="{{{{ back }}}}">Înapoi</button><button class="btn" type="submit">{SEND}</button></div></div>')
    + "</div></div></section>")

SOURCES = {
    "Contact1Coloane": "linear.app/contact: formularul într-un card, datele de contact liniștite alături",
    "Contact2Canale": "apple.com/contact: întâi căile de contact, ca niște carduri pe care apeși, apoi formularul",
    "Contact3Scrisoare": "paperlesspost.com: mesajul ca o scrisoare pe hârtie liniată, cu „Dragă Alessia,” și semnătura",
    "Contact4Chat": "intercom.com, messengerul: Alessia te întreabă, tu răspunzi în conversație",
    "Contact5Pasi": "typeform.com, ca formularul „Cere o ofertă” ales pe Pentru companii: câte o întrebare pe rând, cu bara de progres",
}

SEND_JS = """
    next: function () { self.go(1); }, back: function () { self.go(-1); },
    send: function (e) { e.preventDefault(); var f = e.currentTarget;
      if (!f.checkValidity()) { f.reportValidity(); return; }
      f.classList.add('sent'); var d = f.querySelector('.done'); d.hidden = false; d.setAttribute('tabindex', '-1'); d.focus({ preventScroll: false }); },"""


GO = """
  go(d) {
    var s = this.sec, c = s.querySelector('.card'), cur = +(c.style.getPropertyValue('--s') || 1), st = s.querySelector('.st.on');
    var cb = st && st.querySelectorAll('input[type=checkbox][name=subiect]');
    if (cb && cb.length) cb[0].setCustomValidity(Array.prototype.some.call(cb, function (x) { return x.checked; }) ? '' : 'Alege cel puțin o variantă.');
    if (d > 0 && st) { var bad = Array.prototype.find.call(st.querySelectorAll('input,textarea'), function (x) { return !x.checkValidity(); });
      if (bad) { bad.reportValidity(); return; } }
    var n = Math.max(1, Math.min(3, cur + d)); c.style.setProperty('--s', n);
    s.querySelectorAll('.st').forEach(function (x) { x.classList.toggle('on', +x.getAttribute('data-s') === n); });
    s.querySelector('.cnt .n').textContent = n;
    var f = s.querySelector('.st.on input, .st.on textarea'); if (f) f.focus({ preventScroll: true });
  }"""


def script():
    return ("class Component extends DCLogic {\n  componentDidMount() {" + ENTER + "\n  }\n"
            "  componentWillUnmount() { if (this.io) this.io.disconnect(); }\n" + GO + "\n"
            "  renderVals() { var self = this; if (!this.cb) this.cb = {" + SEND_JS + " secRef: function (el) { self.sec = el; } }; return this.cb; }\n}")


H = {"Contact1Coloane": (1091, 1570), "Contact2Canale": (1293, 1704), "Contact3Scrisoare": (1047, 1717), "Contact4Chat": (1258, 1896), "Contact5Pasi": (789, 1085)}

if __name__ == "__main__":
    gh.SOURCES.update(SOURCES)
    gh.script = lambda *a, **k: script()
    for name, (title, css, html) in OPTS.items():
        for suffix, w, h in (("", 1440, H[name][0]), ("Mobil", 390, H[name][1])):
            f = os.path.join(P, f"{name}{suffix}.dc.html")
            doc = gh.page(name, title + (" · mobil" if suffix else ""), "light", COMMON + css, html, w, h)
            doc = doc.replace('<a href="#ce-facem" aria-haspopup="true" aria-current="page">', '<a href="#ce-facem" aria-haspopup="true">')
            doc = doc.replace('<a href="#contact">Contact</a>', '<a href="#contact" aria-current="page">Contact</a>')
            open(f, "w", encoding="utf-8").write(doc)
            if not suffix:
                subprocess.run([sys.executable, os.path.join(HERE, "dc2html.py"), f, os.path.join(HERE, f"opt-{name}.html")], check=True, capture_output=True)
        print("wrote", name)
