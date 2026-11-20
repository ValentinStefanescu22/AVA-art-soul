"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useCallback, useEffect, useImperativeHandle, useRef, type PointerEvent, type Ref } from "react";
import { Chevron, Close, Vase } from "@/components/icons";
import type { Locale } from "@/lib/i18n";
import { href, type PageKey } from "@/lib/routes";
import type { HeaderProps } from "./Header";
import s from "./mobile-menu.module.css";

export type MobileMenuHandle = { open: (opener?: HTMLElement) => void; close: () => void };

/** A drag ends the sheet if it went far enough (90px) or was a quick flick (> 0.6 px/ms). */
export function shouldCloseAfterDrag(distance: number, ms: number): boolean {
  return distance > 90 || distance / Math.max(1, ms) > 0.6;
}

type Props = Omit<HeaderProps, "lang"> & { lang: Locale; section: PageKey | null; ref: Ref<MobileMenuHandle> };

/**
 * The phone menu, a native <dialog>: the browser traps focus inside it, closes it with Escape and returns focus to
 * the burger afterwards; we add the slide, the backdrop click and the drag-to-close grabber.
 */
export function MobileMenu({ lang, nav, services, copy, instagram, section, ref }: Props) {
  const dlg = useRef<HTMLDialogElement>(null);
  const opener = useRef<HTMLElement | null>(null);
  const pathname = usePathname();

  const close = useCallback(() => {
    const d = dlg.current;
    if (!d?.open) return;
    d.style.removeProperty("--dy");
    d.close();
  }, []);
  const open = useCallback((from?: HTMLElement) => {
    const d = dlg.current;
    if (!d || d.open) return;
    // Safari doesn't focus a tapped button, so the browser wouldn't know where to send focus back: remember it.
    opener.current = from ?? (document.activeElement as HTMLElement | null);
    d.style.removeProperty("--dy");
    d.showModal();
    d.focus({ preventScroll: true });
  }, []);
  useImperativeHandle(ref, () => ({ open, close }), [open, close]);

  // A link inside the menu changes the page: close the sheet once we're there.
  useEffect(close, [pathname, close]);

  const onGrab = (e: PointerEvent<HTMLButtonElement>) => {
    const d = dlg.current;
    if (!d) return;
    const y0 = e.clientY;
    const t0 = performance.now();
    let dy = 0;
    d.setAttribute("data-drag", "");
    const move = (ev: globalThis.PointerEvent) => {
      dy = Math.max(0, ev.clientY - y0);
      d.style.setProperty("--dy", `${dy}px`);
    };
    const up = () => {
      window.removeEventListener("pointermove", move);
      window.removeEventListener("pointerup", up);
      d.removeAttribute("data-drag");
      if (shouldCloseAfterDrag(dy, performance.now() - t0)) close();
      else d.style.setProperty("--dy", "0px");
    };
    window.addEventListener("pointermove", move);
    window.addEventListener("pointerup", up);
  };

  const current = (key: PageKey) => (section === key ? ({ "aria-current": "page" } as const) : {});

  return (
    <dialog
      ref={dlg}
      className={s.sheet}
      aria-label={copy.menu}
      tabIndex={-1}
      // A click on the dialog element itself (not its content) is a click on the backdrop.
      onClick={(e) => e.target === dlg.current && close()}
      onCancel={() => dlg.current?.style.removeProperty("--dy")}
      onClose={() => opener.current?.focus({ preventScroll: true })}
    >
      <div className={s.inner}>
        <button className={s.grab} type="button" aria-label={copy.dragToClose} tabIndex={-1} onPointerDown={onGrab} />
        <div className={s.top}>
          <Link className={s.logo} href={href(lang, "acasa")} onClick={close}>
            <Vase />
            <span>
              <span className={s.word}>AVA</span> <span className={s.sub}>ART &amp; SOUL</span>
            </span>
          </Link>
          <button className={s.close} type="button" aria-label={copy.closeMenu} onClick={close}>
            <Close />
          </button>
        </div>
        <ul className={s.nav}>
          {nav.map(({ page, label }) =>
            page === "ceOferim" ? (
              <li key={page}>
                <details>
                  <summary {...(section === page ? { "data-current": "" } : {})}>
                    {label}
                    <Chevron className={s.chev} />
                  </summary>
                  <ul className={s.subnav}>
                    {services.map((sv) => (
                      <li key={sv.page}>
                        <Link href={href(lang, sv.page)} onClick={close}>
                          {sv.label}
                        </Link>
                      </li>
                    ))}
                    <li>
                      <Link href={href(lang, "ceOferim")} onClick={close}>
                        {copy.allServices}
                      </Link>
                    </li>
                  </ul>
                </details>
              </li>
            ) : (
              <li key={page}>
                <Link href={href(lang, page)} onClick={close} {...current(page)}>
                  {label}
                </Link>
              </li>
            ),
          )}
        </ul>
        <div className={s.foot}>
          <a href={instagram.href} rel="noopener">
            {instagram.handle}
          </a>
        </div>
      </div>
    </dialog>
  );
}
