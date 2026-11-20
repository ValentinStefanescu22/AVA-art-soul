// The header's look at a given scroll position, as a pure function so it can be tested without a browser.

export type HeaderState = {
  /** "1" once the page has scrolled a little: the bar becomes the floating pill. */
  sc: "0" | "1";
  /** "dark" while the pill is over the dark hero (cream text), "light" over the light page (ink text). */
  tone: "dark" | "light";
  /** How far the bar has risen from under Acasă's announcement strip (px). */
  y: number;
};

/**
 * @param scrollY        window.scrollY
 * @param top            px the bar starts below the top (Acasă's announcement strip; 0 elsewhere)
 * @param darkBottom     where the dark hero ends, in viewport px (null: the page has no dark hero)
 */
export function headerState(scrollY: number, top: number, darkBottom: number | null): HeaderState {
  return {
    sc: scrollY > 8 ? "1" : "0",
    // The pill sits ~12px from the top and is ~60px tall: it turns light once the dark area ends above its middle.
    tone: darkBottom !== null && darkBottom > 48 ? "dark" : "light",
    y: Math.min(Math.max(scrollY, 0), top),
  };
}

/**
 * Where the dark hero ends, in viewport px. A hero marks itself with `data-hx-dark`; one that fades to light
 * can say where the header should turn, with the CSS variable --hx-dark (px from the hero's top).
 */
export function darkBottomOf(hero: Element | null): number | null {
  if (!hero) return null;
  const r = hero.getBoundingClientRect();
  const off = parseFloat(getComputedStyle(hero).getPropertyValue("--hx-dark"));
  return r.top + (Number.isNaN(off) ? r.height : off);
}
