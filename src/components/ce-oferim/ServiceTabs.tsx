"use client";

import Link from "next/link";
import { useLayoutEffect, useRef, useState, useSyncExternalStore, type CSSProperties, type KeyboardEvent } from "react";
import { Arrow, People, Sun, Vase } from "@/components/icons";
import { Picture } from "@/components/ui/Picture";
import type { ServiceTab } from "@/content/ro/ce-oferim";
import type { Locale } from "@/lib/i18n";
import { href } from "@/lib/routes";
import s from "./service-tabs.module.css";

const ICONS = { vase: Vase, people: People, sun: Sun };
const noSubscribe = () => () => {};

/** Which tab an arrow / Home / End key moves to from tab `i` of `n` (wraps around); null for any other key. */
export function nextTab(key: string, i: number, n: number): number | null {
  if (key === "ArrowRight") return (i + 1) % n;
  if (key === "ArrowLeft") return (i - 1 + n) % n;
  if (key === "Home") return 0;
  if (key === "End") return n - 1;
  return null;
}

/**
 * „Pentru tine · Pentru companii · Pentru școli și copii”: tabs over the service cards (WAI-ARIA tabs pattern:
 * arrows move between tabs, Tab goes into the panel). Before JavaScript runs, every panel is shown one under the
 * other, so nothing is out of reach without it; afterwards only the chosen one, with a line gliding under its tab.
 */
export function ServiceTabs({ lang, label, tabs }: { lang: Locale; label: string; tabs: readonly ServiceTab[] }) {
  const [sel, setSel] = useState(0);
  // false while the server HTML is shown, true once React runs in the browser
  const live = useSyncExternalStore(
    noSubscribe,
    () => true,
    () => false,
  );
  const tabRefs = useRef<(HTMLButtonElement | null)[]>([]);
  const bar = useRef<HTMLSpanElement>(null);

  // The line under the chosen tab: placed now, after a resize, and once the web fonts have changed the tab widths.
  useLayoutEffect(() => {
    const place = () => {
      const t = tabRefs.current[sel];
      if (!t || !bar.current) return;
      bar.current.style.setProperty("--x", `${t.offsetLeft}px`);
      bar.current.style.setProperty("--w", `${t.offsetWidth}px`);
    };
    place();
    window.addEventListener("resize", place);
    document.fonts?.ready.then(place);
    return () => window.removeEventListener("resize", place);
  }, [sel]);

  const onKey = (e: KeyboardEvent) => {
    const to = nextTab(e.key, sel, tabs.length);
    if (to === null) return;
    e.preventDefault();
    setSel(to);
    tabRefs.current[to]?.focus();
  };

  return (
    <div data-live={live || undefined}>
      <div className={s.tabs} role="tablist" aria-label={label} onKeyDown={onKey}>
        {tabs.map((t, i) => {
          const Icon = ICONS[t.icon];
          return (
            <button
              key={t.id}
              ref={(el) => {
                tabRefs.current[i] = el;
              }}
              className={s.tb}
              type="button"
              role="tab"
              id={`cf-t-${t.id}`}
              aria-controls={`cf-p-${t.id}`}
              aria-selected={i === sel}
              tabIndex={i === sel ? 0 : -1}
              onClick={() => setSel(i)}
            >
              <span className={s.ic}>
                <Icon />
              </span>
              {t.label}
            </button>
          );
        })}
        <span className={s.bar} ref={bar} aria-hidden="true" />
      </div>
      {tabs.map((t, i) => (
        <div
          key={t.id}
          className={s.pn}
          role="tabpanel"
          id={`cf-p-${t.id}`}
          aria-labelledby={`cf-t-${t.id}`}
          hidden={live && i !== sel}
        >
          <div className={t.cards.length > 1 ? s.grid : s.one}>
            {t.cards.map((c, k) => (
              <Link key={c.page} className={s.cd} href={href(lang, c.page)} style={{ "--i": k } as CSSProperties}>
                <span className={s.ph}>
                  <Picture
                    image={c.image}
                    alt={c.alt}
                    sizes={t.cards.length > 1 ? "(max-width: 980px) 100vw, 300px" : "(max-width: 980px) 100vw, 640px"}
                    style={{ objectPosition: c.focus }}
                    // the first photo is the first big thing on the phone screen (LCP): load it right away
                    priority={i === 0 && k === 0}
                  />
                </span>
                {/* a div, not a span: the list of formats can't sit inside a span */}
                <div className={s.tx}>
                  <span className={s.n}>{c.name}</span>
                  <span className={s.ln}>{c.line}</span>
                  {c.formats && (
                    <ul className={s.fm}>
                      {c.formats.map((f) => (
                        <li key={f}>{f}</li>
                      ))}
                    </ul>
                  )}
                  <span className={s.m}>{c.meta}</span>
                  <span className={s.more}>
                    {c.link} <Arrow className={s.ar} />
                  </span>
                </div>
              </Link>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
