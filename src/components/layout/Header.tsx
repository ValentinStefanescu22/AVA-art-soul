"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useRef, type CSSProperties, type KeyboardEvent, type PointerEvent } from "react";
import { Arrow, Chevron, ChevronBack, Vase } from "@/components/icons";
import type { LAYOUT_COPY, NAV, SERVICES } from "@/content/ro/layout";
import type { Locale } from "@/lib/i18n";
import { href, pageAt, sectionOf, SERVICE_PAGES } from "@/lib/routes";
import { darkBottomOf, headerState } from "./headerState";
import { MobileMenu, type MobileMenuHandle } from "./MobileMenu";
import s from "./header.module.css";

export type HeaderProps = {
  lang: Locale;
  nav: typeof NAV;
  services: typeof SERVICES;
  copy: typeof LAYOUT_COPY;
  instagram: { handle: string; href: string };
};

/** Height of Acasă's announcement strip, above the bar (42px once the real Acasă hero arrives in E2). */
const ACASA_STRIP_PX = 0;

export function Header({ lang, nav, services, copy, instagram }: HeaderProps) {
  const pathname = usePathname();
  const page = pageAt(pathname);
  const section = page ? sectionOf(page) : null;
  const isService = page !== null && (SERVICE_PAGES as readonly string[]).includes(page);
  const top = page === "acasa" ? ACASA_STRIP_PX : 0;

  const hx = useRef<HTMLElement>(null);
  const menu = useRef<MobileMenuHandle>(null);

  // Follow the scroll (once per frame): pill or full bar, cream or ink text, and the rise from under the strip.
  useEffect(() => {
    let raf = 0;
    const tick = () => {
      raf = 0;
      const el = hx.current;
      if (!el) return;
      const st = headerState(window.scrollY, top, darkBottomOf(document.querySelector("[data-hx-dark]")));
      el.dataset.sc = st.sc;
      el.dataset.tone = st.tone;
      el.style.setProperty("--y", `${st.y}px`);
    };
    const onScroll = () => {
      if (!raf) raf = requestAnimationFrame(tick);
    };
    tick();
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll, { passive: true });
    return () => {
      cancelAnimationFrame(raf);
      window.removeEventListener("scroll", onScroll);
      window.removeEventListener("resize", onScroll);
    };
  }, [pathname, top]);

  // „Ce oferim” dropdown. The safe triangle follows the pointer while it is above the panel.
  const ddEsc = useRef<((e: globalThis.KeyboardEvent) => void) | null>(null);
  const onDdMove = (e: PointerEvent<HTMLLIElement>) => {
    const li = e.currentTarget;
    const panel = li.querySelector<HTMLElement>(`.${s.panel}`);
    if (!panel) return;
    // Escape must also close a panel opened by hover, where focus is elsewhere: listen only while the pointer is here.
    if (!ddEsc.current) {
      ddEsc.current = (k) => k.key === "Escape" && li.setAttribute("data-shut", "");
      document.addEventListener("keydown", ddEsc.current);
    }
    const r = panel.getBoundingClientRect();
    if (e.clientY < r.top) {
      panel.style.setProperty("--sx", `${e.clientX - r.left}px`);
      panel.style.setProperty("--sh", `${r.top - e.clientY + 2}px`);
    }
  };
  const onDdLeave = (e: PointerEvent<HTMLLIElement>) => {
    e.currentTarget.removeAttribute("data-shut");
    if (ddEsc.current) document.removeEventListener("keydown", ddEsc.current);
    ddEsc.current = null;
  };
  const onDdKey = (e: KeyboardEvent<HTMLLIElement>) => {
    const li = e.currentTarget;
    const trigger = li.querySelector<HTMLAnchorElement>(":scope > a");
    const items = [...li.querySelectorAll<HTMLAnchorElement>(`.${s.panel} a`)];
    const i = items.indexOf(document.activeElement as HTMLAnchorElement);
    if (e.key === "Escape") {
      li.setAttribute("data-shut", "");
      trigger?.focus();
    } else if (e.key === "ArrowDown") {
      e.preventDefault();
      li.removeAttribute("data-shut");
      (items[i + 1] ?? items[0])?.focus();
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      (i > 0 ? items[i - 1] : trigger)?.focus();
    }
  };
  useEffect(() => () => void (ddEsc.current && document.removeEventListener("keydown", ddEsc.current)), []);

  const current = (key: string) => (section === key ? ({ "aria-current": "page" } as const) : {});

  return (
    <>
      <div className={s.dock}>
        <header ref={hx} className={s.hx} data-sc="0" style={{ "--top": `${top}px` } as CSSProperties}>
          <div className={`${s.bar} ${s.glass}`}>
            <Link className={s.logo} href={href(lang, "acasa")}>
              <Vase />
              <span>
                <span className={s.word}>AVA</span> <span className={s.sub}>ART &amp; SOUL</span>
              </span>
            </Link>

            <nav className={s.nav} aria-label={copy.mainNav}>
              <ul>
                {nav.map(({ page: key, label }) =>
                  key === "ceOferim" ? (
                    <li
                      key={key}
                      className={s.dd}
                      onPointerMove={onDdMove}
                      onPointerLeave={onDdLeave}
                      onKeyDown={onDdKey}
                    >
                      <Link href={href(lang, key)} aria-haspopup="true" {...current(key)}>
                        {label}
                        <Chevron className={s.ddChev} />
                      </Link>
                      <div className={`${s.panel} ${s.glass}`}>
                        <ul>
                          {services.map((sv) => (
                            <li key={sv.page}>
                              <Link href={href(lang, sv.page)}>
                                <span>{sv.label}</span>
                              </Link>
                            </li>
                          ))}
                        </ul>
                        <Link className={s.all} href={href(lang, "ceOferim")}>
                          <span>{copy.allServices}</span>
                          <Arrow className={s.arrow} />
                        </Link>
                      </div>
                    </li>
                  ) : (
                    <li key={key}>
                      <Link href={href(lang, key)} {...current(key)}>
                        {label}
                      </Link>
                    </li>
                  ),
                )}
              </ul>
            </nav>

            <div className={s.end}>
              {isService && (
                // On phones the way back to the list of services stays in the pill, wherever you scroll.
                <Link className={s.back} href={href(lang, "ceOferim")}>
                  <ChevronBack />
                  {copy.back}
                </Link>
              )}
              <button
                className={s.burger}
                type="button"
                aria-label={copy.openMenu}
                aria-haspopup="dialog"
                onClick={(e) => menu.current?.open(e.currentTarget)}
              >
                <span className={s.l1} />
                <span className={s.l2} />
                <span className={s.srOnly}>{copy.menu}</span>
              </button>
            </div>
          </div>
        </header>
      </div>
      <MobileMenu
        ref={menu}
        lang={lang}
        nav={nav}
        services={services}
        copy={copy}
        instagram={instagram}
        section={section}
      />
    </>
  );
}
