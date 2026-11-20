"use client";

import { usePathname } from "next/navigation";
import { useEffect } from "react";

/** How many earlier siblings also reveal: they come in one after another, 80ms apart, at most 4 steps. */
export function revealIndex(el: Element): number {
  let i = 0;
  for (let s = el.previousElementSibling; s; s = s.previousElementSibling) if (s.hasAttribute("data-reveal")) i++;
  return Math.min(i, 4);
}

/**
 * Scroll reveal (CLAUDE.md, „Animații”): blocks marked `data-reveal` fade in and rise 16px once, when they reach the
 * screen. Only blocks that start BELOW the screen are hidden, and only by this script: without JavaScript, with
 * reduced motion, or for whatever is already visible when the page opens, nothing is ever hidden.
 * Mounted once in the layout; re-runs after every client-side navigation.
 */
export function RevealObserver() {
  const pathname = usePathname();
  useEffect(() => {
    if (!("IntersectionObserver" in window) || matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const io = new IntersectionObserver(
      (entries) => {
        for (const e of entries) {
          if (!e.isIntersecting) continue;
          e.target.setAttribute("data-reveal", "in");
          io.unobserve(e.target);
        }
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.12 },
    );
    const fold = window.innerHeight;
    // Blocks already waiting are picked up again too: the effect can re-run (React dev mode runs it twice) after
    // the previous observer was disconnected, and a hidden block must never be left without one.
    document.querySelectorAll<HTMLElement>('[data-reveal=""], [data-reveal="wait"]').forEach((el) => {
      if (el.dataset.reveal === "" && el.getBoundingClientRect().top < fold) return;
      el.style.setProperty("--rv-i", String(revealIndex(el)));
      el.setAttribute("data-reveal", "wait");
      io.observe(el);
    });
    return () => io.disconnect();
  }, [pathname]);
  return null;
}
