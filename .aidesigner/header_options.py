"""Sticky header + burger menu, 3 variants (Vali, 11 nov: „headerul să ne urmărească… liquid glass, clean… și burger menu-ul").

usage: python3 .aidesigner/header_options.py
writes .aidesigner/canvas/project/HeaderSticky{1Pastila,2Bara,3Insule}(Mobil).dc.html + local previews opt-HeaderSticky*.html

Each artboard is a real window (1440x900 / 390x844) with its own scroll: inside it the chosen sections are imported
(hero, Despre, Ce oferim, Următorul atelier), the hero's own bar is hidden and the variant's header takes its place.
At the top it looks exactly like today's header; once you scroll it turns into glass and follows you.
The announcement strip stays the hero's and scrolls away with it.

1 Pastila  floats as a centred glass pill            · Apple Liquid Glass (iOS 26 floating tab bars); sheet like Apple Maps
2 Bara     full-width glass bar, hides going down,     · apple.com product nav (glass bar) + medium.com (hide on scroll);
           comes back going up                          sheet with a second level for „Ce oferim", like apple.com mobile
3 Insule   splits into two glass islands; on desktop   · iPhone Dynamic Island
           the nav folds into the right island's menu

Mobile menu = bottom sheet with a grabber (drag down to close) and a × button, as CLAUDE.md asks.
Mine, to approve: „Meniu", „Închide meniul", „Înapoi", „Toate serviciile".
ponytail: no real refraction (SVG displacement on backdrop works only in Chrome); glass = blur + saturate + highlights.
"""
import os
from about_options2 import P, HERE, FONTS

VASE = '<svg viewBox="0 0 64 80" aria-hidden="true"><g fill="none" stroke="currentColor" style="stroke-linecap:round;stroke-linejoin:round"><path d="M22 6H42" style="stroke-width:5"></path><path d="M26 7C26 13 27 15 25 18C17 24 12 31 12 43C12 55 19 64 24 72H40C45 64 52 55 52 43C52 31 47 24 39 18C37 15 38 13 38 7" style="stroke-width:3.6"></path><path d="M14.5 35Q32 40 49.5 35M12.6 48Q32 53 51.4 48" style="stroke-width:3.2"></path></g></svg>'
ARROW = '<svg class="ar" viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8H13M9 4L13 8L9 12" fill="none" stroke="currentColor" style="stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round"></path></svg>'
CHEV = '<svg class="chev" viewBox="0 0 16 16" aria-hidden="true"><path d="M6 3L11 8L6 13" fill="none" stroke="currentColor" style="stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round"></path></svg>'
BACK = '<svg class="chev" viewBox="0 0 16 16" aria-hidden="true"><path d="M10 3L5 8L10 13" fill="none" stroke="currentColor" style="stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round"></path></svg>'
X = '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M5 5L15 15M15 5L5 15" fill="none" stroke="currentColor" style="stroke-width:1.6;stroke-linecap:round"></path></svg>'

NAV = [("#top", "Acasă"), ("#despre", "Despre noi"), ("#ce-facem", "Ce oferim"), ("#evenimente", "Evenimente"),
       ("#galerie", "Galerie"), ("#contact", "Contact")]
SERV = ["Ateliere de grup", "Pentru companii", "Consiliere 1:1", "Atelier privat 1:1", "Retreaturi", "Pentru școli și copii"]
SECTIONS = ["HeroAnuntCentrat", "CopertaH", "CeFacem5Acordeon", "UrmatorulA"]

LOGO = f'<a class="hx-logo" href="#top" aria-label="AVA Art &amp; Soul, pagina principală">{VASE}<span><span class="w">AVA</span><span class="s">ART &amp; SOUL</span></span></a>'
NAVHTML = '<nav class="hx-nav" aria-label="Meniu principal"><ul>' + "".join(
    f'<li><a href="{h}"{" aria-current=\"page\"" if t == "Acasă" else ""}>{t}</a></li>' for h, t in NAV) + "</ul></nav>"
DD = ('<li class="dd" onPointerMove="{{ ddMove }}" onPointerLeave="{{ ddLeave }}" onKeyDown="{{ ddKey }}">'
      f'<a href="#ce-facem" aria-haspopup="true">Ce oferim{CHEV}</a><div class="dd-panel glass"><ul>'
      + "".join(f'<li><a href="#ce-facem"><span>{s}</span></a></li>' for s in SERV)
      + f'</ul><a class="all" href="#ce-facem"><span>Toate serviciile</span>{ARROW}</a></div></li>')
NAVHTML = NAVHTML.replace('<li><a href="#ce-facem">Ce oferim</a></li>', DD)
assert DD in NAVHTML
SEG = '<div class="hx-seg" role="group" aria-label="Limba site-ului"><a href="#ro" aria-current="true">RO</a><a href="#en" lang="en">EN</a></div>'
BURGER = ('<button class="hx-burger" type="button" aria-label="Deschide meniul" aria-haspopup="dialog" onClick="{{ openMenu }}">'
          '<span class="l1"></span><span class="l2"></span><span class="t">Meniu</span></button>')
HEADER = f'<div class="hx-dock"><header class="hx"><div class="hx-in">{LOGO}{NAVHTML}<div class="hx-end">{SEG}{BURGER}</div></div></header></div>'

# ---------------------------------------------------------------- shared css
DEMO_CSS = """body{margin:0;background:#2A140C}
.win{position:relative;width:100%;height:100vh;overflow:hidden;background:#F4EDE4;font-family:var(--text)}
.sc{position:absolute;inset:0;overflow-y:auto;overflow-x:hidden;overscroll-behavior:contain;scrollbar-width:thin}
.s-despre .heroend{display:none}.pg.s-despre{padding-top:40px}
"""
HX_CSS = """.hxv{--ink:#3A2A20;--ink2:#6B5444;--paper:#F4EDE4;--cream:#F4EDE4;--terra-d:#9C472C;--glowc:#F2C79C;--display:'Bodoni Moda',Georgia,serif;--text:'Hanken Grotesk',system-ui,sans-serif}
.s-hero .hn .row{display:none}
/* the dock: zero height, sticks to the top of the scroll; the bar inside starts under the strip (42px) and rises to 0 */
.hx-dock{position:sticky;top:0;z-index:50;height:0}
.hx{position:absolute;left:0;right:0;top:calc(42px - var(--y,0px));color:var(--cream);--ease:cubic-bezier(.22,1,.36,1)}
.hx-in{position:relative;display:grid;grid-template-columns:1fr auto 1fr;align-items:center;max-width:1280px;min-height:76px;margin:0 auto;padding:0 40px;box-sizing:border-box;border-radius:0;
  transition:max-width .5s var(--ease),min-height .5s var(--ease),padding .5s var(--ease),margin .5s var(--ease),border-radius .5s var(--ease),background-color .35s ease,box-shadow .35s ease,color .35s ease}
.hx-logo{justify-self:start;display:inline-flex;align-items:center;gap:12px;min-height:44px;color:inherit;text-decoration:none}
.hx-logo svg{width:22px;height:28px}
.hx-logo>span{display:flex;flex-direction:column;line-height:1}
.hx-logo .w{font:400 21px/1 var(--display);font-variation-settings:'opsz' 20;letter-spacing:.18em}
.hx-logo .s{font:500 9.5px/1 var(--text);letter-spacing:.26em;margin-top:5px}
.hx-nav>ul{display:flex;gap:4px;margin:0;padding:0;list-style:none}
.hx-nav>ul>li>a{position:relative;display:inline-flex;align-items:center;min-height:44px;padding:0 14px;font:500 15px/1 var(--text);color:inherit;opacity:.8;text-decoration:none;transition:opacity .2s ease}
.hx-nav>ul>li>a:hover,.hx-nav>ul>li>a[aria-current],.dd:is(:hover,:focus-within)>a{opacity:1}
.hx-nav>ul>li>a[aria-current]::after{content:"";position:absolute;left:50%;bottom:5px;width:4px;height:4px;margin-left:-2px;border-radius:50%;background:currentColor}
.dd{position:relative}
.dd>a .chev{width:12px;height:12px;margin-left:6px;transform:rotate(90deg);opacity:.7}
.dd:is(:hover,:focus-within):not([data-shut])>a .chev{transform:rotate(-90deg)}
.dd-panel{position:absolute;top:calc(100% + 12px);left:50%;z-index:2;width:290px;padding:8px;border-radius:22px;corner-shape:squircle;box-sizing:border-box;
  opacity:0;visibility:hidden;translate:-50% -6px;transition:opacity .18s ease .12s,translate .25s var(--ease) .12s,visibility 0s linear .3s}
.dd:is(:hover,:focus-within):not([data-shut]) .dd-panel{opacity:1;visibility:visible;translate:-50% 0;transition:opacity .2s ease .05s,translate .3s var(--ease) .05s,visibility 0s linear .05s}
/* the safe triangle: from the pointer (set by JS) to the panel's top corners, plus the 12px gap */
.dd-panel::after{content:"";position:absolute;left:0;right:0;bottom:100%;height:var(--sh,56px);clip-path:polygon(var(--sx,50%) 0,0 100%,100% 100%)}
.dd-panel ul{list-style:none;margin:0;padding:0}
.dd-panel a{display:flex;align-items:center;min-height:44px;padding:0 14px;border-radius:14px;color:inherit;font:500 15px/1.2 var(--text);text-decoration:none;transition:background-color .2s ease}
.dd-panel a span{display:inline-block;transform-origin:left center;transition:transform .28s var(--ease)}
.dd-panel a:hover,.dd-panel a:focus-visible{background:color-mix(in srgb,currentColor 9%,transparent)}
.dd-panel a:hover span,.dd-panel a:focus-visible span{transform:scale(1.08)}
.dd-panel .all{justify-content:space-between;margin-top:4px;border-top:1px solid color-mix(in srgb,currentColor 14%,transparent);border-radius:0 0 14px 14px;padding-top:2px;opacity:.85}
.dd-panel .all .ar{width:16px;height:16px;flex:none}
@media (prefers-reduced-motion:reduce){.dd-panel,.dd-panel a span,.dd>a .chev{transition:none!important}}
.hx-end{justify-self:end;display:flex;align-items:center;gap:10px}
.hx-seg{display:flex;padding:3px;border-radius:999px;background:color-mix(in srgb,currentColor 10%,transparent);box-shadow:inset 0 0 0 1px color-mix(in srgb,currentColor 18%,transparent)}
.hx-seg a{display:inline-flex;align-items:center;justify-content:center;min-width:40px;min-height:38px;border-radius:999px;font:500 12px/1 var(--text);letter-spacing:.1em;color:inherit;opacity:.72;text-decoration:none}
.hx-seg a[aria-current]{opacity:1;background:var(--cream);color:var(--ink)}
.hx[data-tone="light"] .hx-seg a[aria-current]{background:var(--ink);color:var(--cream)}
.hx-burger{display:none;position:relative;align-items:center;justify-content:center;width:44px;height:44px;padding:0;border:0;border-radius:999px;background:color-mix(in srgb,currentColor 10%,transparent);color:inherit;cursor:pointer;transition:background-color .3s ease}
.hx-burger .l1,.hx-burger .l2{position:absolute;left:14px;right:14px;height:1.6px;border-radius:2px;background:currentColor;transform-origin:right center;transition:transform .35s var(--ease)}
.hx-burger .l1{transform:translateY(-3.5px)}.hx-burger .l2{transform:translateY(3.5px) scaleX(.6)}
/* Vali (11 nov): clean hover on desktop: the two lines trade lengths, the glass deepens a little */
@media (hover:hover) and (pointer:fine){
  .hx-burger:hover{background:color-mix(in srgb,currentColor 18%,transparent)}
  .hx-burger:hover .l1{transform:translateY(-3.5px) scaleX(.6)}.hx-burger:hover .l2{transform:translateY(3.5px)}
  .hx-burger:active{scale:.96}
}
.hx-burger .t{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
.hx a:focus-visible,.hx button:focus-visible,.sheet a:focus-visible,.sheet button:focus-visible,.sheet summary:focus-visible{outline:2px solid #9C472C;outline-offset:3px;border-radius:999px}
.hx[data-tone="dark"] a:focus-visible,.hx[data-tone="dark"] button:focus-visible{outline-color:var(--glowc)}
/* liquid glass (Vali, 11 nov: less see-through, so the menu stays readable over photos): tint + blur + saturate, a bright rim on top, a faint one below, a soft drop shadow */
.glass{isolation:isolate}
.hx-logo,.hx-end{position:relative}
.glass::before{content:"";position:absolute;inset:0;z-index:-1;border-radius:inherit;pointer-events:none;-webkit-backdrop-filter:blur(22px) saturate(170%);backdrop-filter:blur(22px) saturate(170%);transition:opacity .35s ease,background-color .35s ease,box-shadow .35s ease}
.hx[data-tone="dark"] .glass::before{background-color:rgba(40,20,12,.6);box-shadow:inset 0 1px 0 rgba(255,236,214,.28),inset 0 -1px 0 rgba(255,236,214,.08),inset 0 0 0 1px rgba(255,236,214,.14),0 12px 32px -16px rgba(0,0,0,.6)}
.hx[data-tone="light"]{color:var(--ink)}
.hx[data-tone="light"] .glass::before{background-color:rgba(250,246,240,.84);box-shadow:inset 0 1px 0 rgba(255,255,255,.95),inset 0 -1px 0 rgba(255,255,255,.4),inset 0 0 0 1px rgba(255,255,255,.55),0 14px 34px -18px rgba(70,38,18,.45)}
@media (max-width:1020px){.hx-nav,.hx-seg{display:none}.hx-burger{display:inline-flex}.hx-in{grid-template-columns:1fr auto}}
@media (max-width:820px){.hx-in{padding:0 16px;min-height:68px}}

/* ---- bottom sheet (mobile menu) */
.sheet{position:fixed;inset:auto 0 0 0;width:100%;max-width:none;max-height:min(88vh,720px);margin:0;padding:0;border:0;box-sizing:border-box;overflow:hidden;
  border-radius:26px 26px 0 0;corner-shape:squircle;color:var(--ink);font-family:var(--text);
  transform:translateY(var(--dy,0px));transition:transform .42s cubic-bezier(.22,1,.36,1),display .42s allow-discrete,overlay .42s allow-discrete}
.sheet:not([open]){transform:translateY(100%)}
@starting-style{.sheet[open]{transform:translateY(100%)}}
.sheet[data-drag]{transition:none}
.sheet::backdrop{background:rgba(30,15,8,.34);transition:background .42s,display .42s allow-discrete,overlay .42s allow-discrete}
@starting-style{.sheet[open]::backdrop{background:rgba(30,15,8,0)}}
.sheet:focus{outline:none}
.sh-in{display:flex;flex-direction:column;max-height:inherit;padding:10px 24px calc(24px + env(safe-area-inset-bottom));box-sizing:border-box;overflow-y:auto}
.grab{align-self:center;display:flex;justify-content:center;width:100%;min-height:24px;padding:0;border:0;background:none;cursor:grab;touch-action:none}
.grab::before{content:"";width:40px;height:5px;margin-top:4px;border-radius:3px;background:currentColor;opacity:.22}
.sh-top{display:flex;align-items:center;justify-content:space-between;margin:2px 0 8px}
.sh-top .hx-logo{color:inherit}
.x{display:inline-flex;align-items:center;justify-content:center;width:44px;height:44px;padding:0;border:0;border-radius:50%;background:color-mix(in srgb,currentColor 8%,transparent);color:inherit;cursor:pointer}
.x svg{width:18px;height:18px}
.sh-nav{list-style:none;margin:0;padding:0}
.sh-nav a,.sh-nav summary,.sh-nav button.go{display:flex;align-items:center;justify-content:space-between;width:100%;min-height:52px;padding:0;border:0;background:none;color:inherit;text-decoration:none;cursor:pointer;list-style:none;text-align:left}
.sh-nav summary::-webkit-details-marker{display:none}
.chev{width:16px;height:16px;flex:none;transition:transform .3s cubic-bezier(.22,1,.36,1)}
.sh-sub{list-style:none;margin:0 0 8px;padding:0 0 0 2px}
.sh-sub a{min-height:44px;font:400 16px/1.3 var(--text)}
.sh-foot{display:flex;align-items:center;justify-content:space-between;gap:16px;margin-top:22px;padding-top:18px;border-top:1px solid color-mix(in srgb,currentColor 14%,transparent);font-size:14px}
.sh-foot a{color:inherit;text-underline-offset:4px}
.sheet .hx-seg{display:flex}
.sheet .ar{width:16px;height:16px;flex:none}
.sheet .hx-seg a[aria-current]{background:var(--ink);color:var(--cream)}
@media (prefers-reduced-motion:reduce){.hx-in,.sheet,.sheet::backdrop,.hx-burger,.hx-burger span,.chev{transition:none!important}}
"""
BASE = DEMO_CSS + HX_CSS

# ---------------------------------------------------------------- variants
V = {}
V["1Pastila"] = dict(
    title="Header 1: pastilă de sticlă", src="Apple Liquid Glass (iOS 26: bare care plutesc) · meniul ca foaia din Apple Maps",
    css="""
/* scrolled: the bar narrows into a floating pill */
.hx[data-sc="1"] .hx-in{max-width:960px;min-height:60px;margin-top:12px;padding:0 10px 0 22px;border-radius:999px}
.hx:not([data-sc="1"]) .hx-in.glass::before{opacity:0}
.hx[data-sc="1"] .hx-nav>ul>li>a{padding:0 12px;font-size:14.5px}
@media (max-width:820px){.hx[data-sc="1"] .hx-in{max-width:calc(100% - 20px);min-height:56px;margin-top:10px;padding:0 6px 0 16px}}
/* sheet: frosted glass, big serif links */
.v1 .sheet{background:rgba(250,246,240,.78);-webkit-backdrop-filter:blur(28px) saturate(170%);backdrop-filter:blur(28px) saturate(170%);box-shadow:inset 0 1px 0 rgba(255,255,255,.9),0 -20px 60px -30px rgba(40,20,10,.5)}
.v1 .sh-nav>li>a,.v1 .sh-nav summary{font:400 30px/1.15 var(--display);font-variation-settings:'opsz' 20;letter-spacing:-.01em;min-height:56px}
.v1 .sh-nav a[aria-current]{color:var(--terra-d)}
.v1 .sh-nav details[open] .chev{transform:rotate(90deg)}
""",
    sheet=lambda: f"""<ul class="sh-nav">
<li><a href="#top" aria-current="page" onClick="{{{{ closeMenu }}}}">Acasă</a></li>
<li><a href="#despre" onClick="{{{{ closeMenu }}}}">Despre noi</a></li>
<li><details><summary>Ce oferim {CHEV}</summary><ul class="sh-sub">{"".join(f'<li><a href="#ce-facem" onClick="{{{{ closeMenu }}}}">{s}</a></li>' for s in SERV)}</ul></details></li>
<li><a href="#evenimente" onClick="{{{{ closeMenu }}}}">Evenimente</a></li>
<li><a href="#galerie" onClick="{{{{ closeMenu }}}}">Galerie</a></li>
<li><a href="#contact" onClick="{{{{ closeMenu }}}}">Contact</a></li>
</ul>
<div class="sh-foot">{SEG}<a href="https://www.instagram.com/ava.art.soul/">@ava.art.soul</a></div>""")

V["2Bara"] = dict(
    title="Header 2: bară care se retrage", src="apple.com (bara de sticlă de pe paginile de produs) + medium.com (dispare la scroll în jos) · submeniul ca pe apple.com mobil",
    css="""
.hx{transition:transform .45s cubic-bezier(.22,1,.36,1)}
.hx[data-hide="1"]{transform:translateY(-110%)}
.hx[data-sc="1"] .hx-in{max-width:none;min-height:64px;padding:0 max(40px,calc((100% - 1200px)/2))}
.hx:not([data-sc="1"]) .hx-in.glass::before{opacity:0}
.hx[data-sc="1"][data-tone="light"] .hx-in{box-shadow:inset 0 -1px 0 rgba(58,42,32,.1),0 10px 30px -22px rgba(70,38,18,.5)!important}
.hx[data-sc="1"][data-tone="dark"] .hx-in{box-shadow:inset 0 -1px 0 rgba(255,236,214,.14)!important}
@media (max-width:820px){.hx[data-sc="1"] .hx-in{min-height:60px;padding:0 16px}}
/* sheet: paper, two levels */
.v2 .sheet{background:#FBF7F0;box-shadow:0 -20px 60px -30px rgba(40,20,10,.5)}
.v2 .lv{display:flex;width:200%;transition:transform .38s cubic-bezier(.22,1,.36,1)}
.v2 .lv>div{width:50%;flex:none;box-sizing:border-box}
.v2 .lvw{overflow:hidden}
.v2 .sheet[data-lv="2"] .lv{transform:translateX(-50%)}
.v2 .sh-in{overflow-x:hidden}
.v2 .sh-nav>li{border-bottom:1px solid rgba(58,42,32,.1)}
.v2 .sh-nav>li>a,.v2 .sh-nav button.go{font:500 21px/1.2 var(--text);min-height:58px}
.v2 .sh-nav a[aria-current]{color:var(--terra-d)}
.v2 .back{display:inline-flex;align-items:center;gap:6px;min-height:44px;margin:0 0 6px;padding:0;border:0;background:none;color:var(--ink2);font:500 15px var(--text);cursor:pointer}
.v2 .lv2 h3:focus{outline:none}
.v2 .lv2 h3{margin:0 0 6px;font:400 30px/1.15 var(--display);font-variation-settings:'opsz' 20}
.v2 .lv2 .sh-nav a{font:400 18px/1.3 var(--text);min-height:54px}
.v2 .lv2 .all{white-space:nowrap;display:inline-flex;align-items:center;gap:8px;min-height:44px;margin-top:10px;color:var(--terra-d);font-weight:500;text-decoration:none}
.v2 .next{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-top:20px;padding:16px 18px;border-radius:16px;corner-shape:squircle;background:#F1E7DA;color:var(--ink);text-decoration:none}
.v2 .next b{display:block;font:500 15px/1.3 var(--text)}
.v2 .next span{font-size:14px;color:var(--ink2);font-variant-numeric:tabular-nums}
.v2 .next i{flex:none;padding:6px 10px;border-radius:999px;border:1px solid #9C472C;color:#9C472C;font:500 12.5px/1 var(--text);font-style:normal}
""",
    sheet=lambda: f"""<div class="lvw"><div class="lv"><div class="lv1">
<ul class="sh-nav">
<li><a href="#top" aria-current="page" onClick="{{{{ closeMenu }}}}">Acasă</a></li>
<li><a href="#despre" onClick="{{{{ closeMenu }}}}">Despre noi</a></li>
<li><button class="go" type="button" onClick="{{{{ goLevel2 }}}}">Ce oferim {CHEV}</button></li>
<li><a href="#evenimente" onClick="{{{{ closeMenu }}}}">Evenimente</a></li>
<li><a href="#galerie" onClick="{{{{ closeMenu }}}}">Galerie</a></li>
<li><a href="#contact" onClick="{{{{ closeMenu }}}}">Contact</a></li>
</ul>
<a class="next" href="#evenimente" onClick="{{{{ closeMenu }}}}"><span><b>Următorul atelier</b>duminică, 15 noiembrie, ora 17:00</span><i>Sold out</i></a>
<div class="sh-foot">{SEG}<a href="https://www.instagram.com/ava.art.soul/">@ava.art.soul</a></div>
</div><div class="lv2">
<button class="back" type="button" onClick="{{{{ goLevel1 }}}}">{BACK} Înapoi</button>
<h3 tabindex="-1">Ce oferim</h3>
<ul class="sh-nav">{"".join(f'<li><a href="#ce-facem" onClick="{{{{ closeMenu }}}}">{s}</a></li>' for s in SERV)}</ul>
<a class="all" href="#ce-facem" onClick="{{{{ closeMenu }}}}">Toate serviciile {ARROW}</a>
</div></div></div>""")

V["3Insule"] = dict(
    title="Header 3: două insule", src="iPhone Dynamic Island (insula care se deschide în meniu)",
    css="""
/* scrolled: the bar dissolves into two islands; on desktop the nav folds into the right island's menu */
.hx[data-sc="1"] .hx-in{min-height:64px;margin-top:10px;padding:0 20px;grid-template-columns:1fr auto}
.hx-in.glass::before{display:none}
.hx .hx-logo,.hx .hx-end{border-radius:999px;transition:padding .5s var(--ease),background-color .35s,box-shadow .35s}
.hx[data-sc="1"] .hx-logo{padding:8px 18px 8px 14px}
.hx[data-sc="1"] .hx-end{padding:5px}
.hx:not([data-sc="1"]) .island::before{opacity:0}
.hx-nav{transition:opacity .3s ease,visibility .3s}
.hx[data-sc="1"] .hx-nav{opacity:0;visibility:hidden;position:absolute;left:50%;transform:translateX(-50%)}
.hx[data-sc="1"] .hx-burger{display:inline-flex}
.hx[data-sc="1"] .hx-seg{background:none;box-shadow:none}
@media (max-width:820px){.hx[data-sc="1"] .hx-in{padding:0 10px}.hx[data-sc="1"] .hx-logo{padding:6px 14px 6px 10px}}
/* sheet: dark „lut ars"; on desktop the same dialog drops from the right island */
.v3 .sheet{background:#2E1D14;color:#F4EDE4;box-shadow:inset 0 1px 0 rgba(255,236,214,.12),0 -20px 60px -30px rgba(0,0,0,.7)}
.v3 .sh-nav>li>a{font:400 32px/1.15 var(--display);font-variation-settings:'opsz' 20;min-height:56px}
.v3 .sh-nav a[aria-current]{color:var(--glowc)}
.v3 .sh-svc{display:grid;grid-template-columns:1fr 1fr;gap:0 16px;list-style:none;margin:2px 0 6px;padding:0}
.v3 .sh-svc a{display:flex;align-items:center;min-height:40px;font-size:14.5px;color:#D9C7B4;text-decoration:none}
.v3 .sheet .hx-seg a[aria-current]{background:#F4EDE4;color:#3A2A20}
.v3 .sh-foot{color:#D9C7B4}
.v3 .grab::before{opacity:.35}
.v3 .sheet a:focus-visible,.v3 .sheet button:focus-visible{outline-color:var(--glowc)}
@media (min-width:821px){
  .v3 .sheet{inset:86px 24px auto auto;width:400px;max-height:calc(100vh - 110px);border-radius:28px;transform:none;opacity:1;transform-origin:top right;
    transition:opacity .3s ease,scale .38s cubic-bezier(.22,1,.36,1),display .38s allow-discrete,overlay .38s allow-discrete}
  .v3 .sheet:not([open]){opacity:0;scale:.92;transform:none}
  @starting-style{.v3 .sheet[open]{opacity:0;scale:.92;transform:none}}
  .v3 .sheet::backdrop{background:rgba(30,15,8,.12)}
  .v3 .grab{display:none}
}
""",
    sheet=lambda: f"""<ul class="sh-nav">
<li><a href="#top" aria-current="page" onClick="{{{{ closeMenu }}}}">Acasă</a></li>
<li><a href="#despre" onClick="{{{{ closeMenu }}}}">Despre noi</a></li>
<li><a href="#ce-facem" onClick="{{{{ closeMenu }}}}">Ce oferim</a><ul class="sh-svc">{"".join(f'<li><a href="#ce-facem" onClick="{{{{ closeMenu }}}}">{s}</a></li>' for s in SERV)}</ul></li>
<li><a href="#evenimente" onClick="{{{{ closeMenu }}}}">Evenimente</a></li>
<li><a href="#galerie" onClick="{{{{ closeMenu }}}}">Galerie</a></li>
<li><a href="#contact" onClick="{{{{ closeMenu }}}}">Contact</a></li>
</ul>
<div class="sh-foot">{SEG}<a href="mailto:ava.events.26@gmail.com">ava.events.26@gmail.com</a></div>""")

JS_T = """class Component extends DCLogic {
  componentDidMount() {
    var self = this, last = 0, raf = 0;
    this.tick = function () {
      raf = 0;
      var sc = self.sc, hx = self.hx; if (!hx) return;
      var y = sc ? sc.scrollTop : (window.scrollY || 0);
      hx.style.setProperty('--y', Math.min(y, 42) + 'px');
      hx.setAttribute('data-sc', y > 8 ? '1' : '0');
      var hero = (sc || document).querySelector('/*DARK*/'), hb = 0;
      // dark until the pill leaves the hero; a page whose hero fades to light sets --hx-dark (px from the hero's top) on it
      if (hero) { var r = hero.getBoundingClientRect(), off = parseFloat(getComputedStyle(hero).getPropertyValue('--hx-dark'));
        hb = r.top + (isNaN(off) ? r.height : off) - (sc ? sc.getBoundingClientRect().top : 0); }
      // no hero yet (sections arrive through <dc-import>): stay light-on-dark, as the page opens on the dark hero
      hx.setAttribute('data-tone', !hero || hb > 48 ? 'dark' : 'light');
      if (y > 320 && y - last > 4) hx.setAttribute('data-hide', '1');      // only variant 2 styles data-hide
      else if (last - y > 4 || y < 320) hx.setAttribute('data-hide', '0');
      last = y;
    };
    this.onScroll = function () { if (!raf) raf = requestAnimationFrame(self.tick); };
    this.src = this.sc || window;
    this.src.addEventListener('scroll', this.onScroll, { passive: true });
    this.tick(); this.t2 = setTimeout(this.tick, 400); this.t3 = setTimeout(this.tick, 1500);   // again once the sections are in
    /*MOUNT*/
  }
  componentWillUnmount() { clearTimeout(this.t2); clearTimeout(this.t3); this.src.removeEventListener('scroll', this.onScroll); /*UNMOUNT*/ }
  renderVals() {
    var self = this;
    if (!this.cb) {
      this.shut = function () {
        var d = self.dlg; if (!d) return;
        d.style.removeProperty('--dy'); d.removeAttribute('data-lv');
        if (d.close) d.close();
      };
      this.cb = {
        scRef: function (el) { self.sc = el; },
        hxRef: function (el) { self.hx = el; },
        dlgRef: function (el) { self.dlg = el; },
        openMenu: function () { var d = self.dlg; if (d && d.showModal && !d.open) { d.removeAttribute('data-lv'); d.style.removeProperty('--dy'); d.showModal(); d.focus({ preventScroll: true }); } },
        closeMenu: function () { self.shut(); },
        // „Ce oferim" dropdown: the safe triangle follows the pointer while it is above the panel
        ddMove: function (e) {
          var li = e.currentTarget, p = li.querySelector('.dd-panel'); if (!p) return;
          // Escape must also close a panel opened by hover, where focus is elsewhere: listen only while the pointer is here
          if (!self.ddEsc) { self.ddEsc = function (k) { if (k.key === 'Escape') li.setAttribute('data-shut', ''); }; document.addEventListener('keydown', self.ddEsc); }
          var r = p.getBoundingClientRect();
          if (e.clientY < r.top) { p.style.setProperty('--sx', (e.clientX - r.left) + 'px'); p.style.setProperty('--sh', (r.top - e.clientY + 2) + 'px'); }
        },
        ddLeave: function (e) {
          e.currentTarget.removeAttribute('data-shut');
          if (self.ddEsc) { document.removeEventListener('keydown', self.ddEsc); self.ddEsc = null; }
        },
        ddKey: function (e) {
          var li = e.currentTarget;
          if (e.key === 'Escape') { li.setAttribute('data-shut', ''); li.querySelector('a').focus(); }
          else if (e.key === 'ArrowDown') { e.preventDefault(); li.removeAttribute('data-shut'); var a = li.querySelectorAll('.dd-panel a'), i = [].indexOf.call(a, document.activeElement); (a[i + 1] || a[0]).focus(); }
          else if (e.key === 'ArrowUp') { e.preventDefault(); var b = li.querySelectorAll('.dd-panel a'), j = [].indexOf.call(b, document.activeElement); if (j > 0) b[j - 1].focus(); else li.querySelector('a').focus(); }
        },
        backdrop: function (e) { if (e.target === self.dlg) self.shut(); },
        cancel: function () { self.dlg && self.dlg.style.removeProperty('--dy'); },
        goLevel2: function () { self.dlg.setAttribute('data-lv', '2'); var h = self.dlg.querySelector('.lv2 h3'); h && h.focus({ preventScroll: true }); },
        goLevel1: function () { self.dlg.removeAttribute('data-lv'); var b = self.dlg.querySelector('.go'); b && b.focus({ preventScroll: true }); },
        // drag the grabber down to close (a flick or more than 90px)
        drag: function (e) {
          var d = self.dlg, y0 = e.clientY, t0 = Date.now(), dy = 0;
          d.setAttribute('data-drag', '');
          function mv(ev) { dy = Math.max(0, ev.clientY - y0); d.style.setProperty('--dy', dy + 'px'); }
          function up() {
            window.removeEventListener('pointermove', mv); window.removeEventListener('pointerup', up);
            d.removeAttribute('data-drag');
            var v = dy / Math.max(1, Date.now() - t0);
            if (dy > 90 || v > 0.6) self.shut(); else d.style.setProperty('--dy', '0px');
          }
          window.addEventListener('pointermove', mv); window.addEventListener('pointerup', up);
        }
      };
    }
    return this.cb;
  }
}"""
JS = JS_T.replace("/*MOUNT*/", "").replace("/*UNMOUNT*/", "").replace("/*DARK*/", ".s-hero .hero")


def js(mount="", unmount="", dark=".s-hero .hero"):
    return JS_T.replace("/*MOUNT*/", mount).replace("/*UNMOUNT*/", unmount).replace("/*DARK*/", dark)


def board(key, v, w, h, mobile):
    n = key[0]
    imports = "\n".join(f'<dc-import name="{s}" hint-size="100%,{960 if s == SECTIONS[0] else 1000}px"></dc-import>' for s in SECTIONS)
    head, sheet = header_html(n), sheet_html(v)
    return page_html(v, n, w, h, mobile, head, sheet, imports)


def header_html(n):
    island = "island glass" if n == "3" else ""
    head = HEADER.replace('<header class="hx">', '<header class="hx" data-sc="0" data-tone="dark" data-hide="0" ref="{{ hxRef }}">') \
                 .replace('<div class="hx-in">', '<div class="hx-in glass">')
    if island:
        head = head.replace('class="hx-logo"', f'class="hx-logo {island}"', 1).replace('<div class="hx-end">', f'<div class="hx-end {island}">')
    return head


def sheet_html(v):
    return (f'<dialog class="sheet" aria-label="Meniu" tabindex="-1" ref="{{{{ dlgRef }}}}" onClick="{{{{ backdrop }}}}" onCancel="{{{{ cancel }}}}">'
             f'<div class="sh-in"><button class="grab" type="button" aria-label="Trage în jos ca să închizi" tabindex="-1" onPointerDown="{{{{ drag }}}}"></button>'
             f'<div class="sh-top">{LOGO}<button class="x" type="button" aria-label="Închide meniul" onClick="{{{{ closeMenu }}}}">{X}</button></div>'
             f'{v["sheet"]()}</div></dialog>')


def page_html(v, n, w, h, mobile, head, sheet, imports):
    return f"""<!doctype html>
<html lang="ro">
<head>
<meta charset="utf-8">
<title>{v["title"]}{" · mobil" if mobile else ""}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
{FONTS}
<style>
{BASE}{v["css"]}</style>
</helmet>
<div class="win hxv v{n}" style="height: {h}px">
<div class="sc" ref="{{{{ scRef }}}}">
{head}
{imports}
</div>
{sheet}
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{w},"height":{h}}}}}'>
{JS}
</script>
</body>
</html>
"""


def acasa_parts():
    """Header 1 (chosen, 11 nov) for Acasă: css, the dock, the menu sheet, and js(mount, unmount)."""
    v = V["1Pastila"]
    return HX_CSS + v["css"], header_html("1"), sheet_html(v), js


if __name__ == "__main__":
    import subprocess
    for key, v in V.items():
        for mobile, w, h in ((False, 1440, 900), (True, 390, 844)):
            name = f"HeaderSticky{key}{'Mobil' if mobile else ''}"
            open(os.path.join(P, name + ".dc.html"), "w", encoding="utf-8").write(board(key, v, w, h, mobile))
            subprocess.run(["python3", os.path.join(HERE, "dc2html.py"), os.path.join(P, name + ".dc.html"),
                            os.path.join(HERE, f"opt-{name}.html")], check=True, capture_output=True)
            print("wrote", name)
