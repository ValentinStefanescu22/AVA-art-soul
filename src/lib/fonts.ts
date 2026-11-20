import { Bodoni_Moda, Literata, Pinyon_Script } from "next/font/google";

// next/font downloads the files at build time and serves them from our own domain: no request to Google at runtime.
// latin-ext is required for ș and ț (comma below).
//
// Speed (E2, Lighthouse): every preloaded font competes with the hero photo on a slow phone. So only what the first
// screen needs is preloaded (Bodoni upright for the title, Literata for the text); Bodoni italic, used only for
// accents further down, loads normally when a page needs it. Literata italic isn't used anywhere, so it isn't loaded.

/** Titles. Always used with font-variation-settings: 'opsz' 20 (see globals.css), or the hairlines vanish on screen. */
export const bodoni = Bodoni_Moda({
  subsets: ["latin", "latin-ext"],
  axes: ["opsz"],
  style: "normal",
  display: "swap",
  variable: "--font-bodoni",
});

/** Bodoni italic, its own family (--font-display-italic in globals.css), not preloaded. */
export const bodoniItalic = Bodoni_Moda({
  subsets: ["latin", "latin-ext"],
  axes: ["opsz"],
  style: "italic",
  display: "swap",
  preload: false,
  variable: "--font-bodoni-italic",
});

/** Body text. Without the optical-size axis: 95 KB instead of 200 KB to preload, and at text sizes (15–19px) the
 *  default optical size is the right one anyway (E2, Lighthouse). */
export const literata = Literata({
  subsets: ["latin", "latin-ext"],
  style: "normal",
  display: "swap",
  variable: "--font-literata",
});

/** Only for "Art & Soul" and rare accents, never long text. Not preloaded. */
export const pinyon = Pinyon_Script({
  subsets: ["latin", "latin-ext"],
  weight: "400",
  display: "swap",
  preload: false,
  variable: "--font-pinyon",
});
