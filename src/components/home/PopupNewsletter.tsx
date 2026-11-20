"use client";

import { useEffect, useRef, type PointerEvent } from "react";
import { Close, Vase } from "@/components/icons";
import { NewsletterForm } from "@/components/layout/NewsletterForm";
import { shouldCloseAfterDrag } from "@/components/layout/MobileMenu";
import { LAYOUT_COPY } from "@/content/ro/layout";
import { POPUP_COPY } from "@/content/ro/home/popup";
import type { Locale } from "@/lib/i18n";
import { href } from "@/lib/routes";
import s from "./popup-newsletter.module.css";

const KEY = "ava.popup.newsletter";
const DELAY_MS = 8000;
const SCROLL_SHARE = 0.4;

/**
 * The newsletter pop-up of Acasă: shown once per visitor, after ~8 s or when 40% of the page has been scrolled,
 * never over another open dialog (the mobile menu) and never after subscribing in the footer. A native <dialog>;
 * on phones a bottom sheet you drag down to close.
 */
export function PopupNewsletter({ lang }: { lang: Locale }) {
  const dlg = useRef<HTMLDialogElement>(null);
  const opener = useRef<HTMLElement | null>(null);

  useEffect(() => {
    let done = false; // opened already, or subscribed: don't show it again in this page view
    try {
      if (localStorage.getItem(KEY)) return;
    } catch {
      // blocked storage: carry on, the `done` flag still keeps it to one time per page view
    }
    const stop = () => {
      done = true;
      clearTimeout(timer);
      window.removeEventListener("scroll", onScroll);
      window.removeEventListener("ava:subscribed", stop);
    };
    const show = () => {
      const d = dlg.current;
      if (done || !d || document.querySelector("dialog[open]")) return; // the menu is open: a later trigger retries
      stop();
      try {
        localStorage.setItem(KEY, "1");
      } catch {
        // see above
      }
      opener.current = document.activeElement as HTMLElement | null; // Safari doesn't focus tapped buttons
      d.showModal();
      d.focus({ preventScroll: true });
    };
    const onScroll = () => {
      const range = document.documentElement.scrollHeight - window.innerHeight;
      if (range > 0 && window.scrollY / range >= SCROLL_SHARE) show();
    };
    const timer = setTimeout(show, DELAY_MS);
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("ava:subscribed", stop);
    return stop;
  }, []);

  const close = () => {
    const d = dlg.current;
    if (!d?.open) return;
    d.style.removeProperty("--dy");
    d.close();
  };

  const onGrab = (e: PointerEvent<HTMLDivElement>) => {
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

  return (
    <dialog
      ref={dlg}
      className={s.pop}
      aria-labelledby="pp-nl-title"
      tabIndex={-1}
      // A click on the dialog element itself (not its content) is a click on the backdrop.
      onClick={(e) => e.target === dlg.current && close()}
      onCancel={() => dlg.current?.style.removeProperty("--dy")}
      onClose={() => opener.current?.focus({ preventScroll: true })}
    >
      <div className={s.grab} aria-hidden="true" onPointerDown={onGrab} />
      <button className={s.x} type="button" aria-label={POPUP_COPY.close} onClick={close}>
        <Close />
      </button>
      <div className={s.tx}>
        <svg className={s.seal} viewBox="0 0 120 120" width="104" height="104" aria-hidden="true">
          <defs>
            <path id="pp-nl-seal-ring" d="M60,60 m-44,0 a44,44 0 1,1 88,0 a44,44 0 1,1 -88,0" />
          </defs>
          <circle cx="60" cy="60" r="57" fill="none" stroke="currentColor" strokeWidth={1.4} />
          <circle cx="60" cy="60" r="34" fill="none" stroke="currentColor" strokeWidth={1.1} />
          <text style={{ font: "600 7.4px var(--font-text)" }} fill="currentColor">
            <textPath href="#pp-nl-seal-ring" textLength={272} lengthAdjust="spacing">
              {LAYOUT_COPY.footer.sealText}
            </textPath>
          </text>
          <svg x="38" y="34" width="44" height="52" viewBox="0 0 64 80">
            <Vase />
          </svg>
        </svg>
        <h2 className={s.title} id="pp-nl-title">
          {POPUP_COPY.title}
        </h2>
        <p className={s.sub}>{POPUP_COPY.lead}</p>
        <p className={s.big}>
          <b>
            5<small>%</small>
          </b>
          <span>{POPUP_COPY.discount}</span>
        </p>
        <NewsletterForm
          id="pp-nl"
          copy={LAYOUT_COPY.newsletter}
          privacyHref={href(lang, "confidentialitate")}
          styles={s}
        />
        <button className={s.later} type="button" onClick={close}>
          {POPUP_COPY.later}
        </button>
      </div>
    </dialog>
  );
}
