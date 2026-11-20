import { Bodoni_Moda, Literata, Pinyon_Script } from "next/font/google";

// next/font downloads the files at build time and serves them from our own domain: no request to Google at runtime.
// latin-ext is required for ș and ț (comma below).

/** Titles. Always used with font-variation-settings: 'opsz' 20 (see globals.css), or the hairlines vanish on screen. */
export const bodoni = Bodoni_Moda({
  subsets: ["latin", "latin-ext"],
  axes: ["opsz"],
  style: ["normal", "italic"],
  display: "swap",
  variable: "--font-bodoni",
});

/** Body text. */
export const literata = Literata({
  subsets: ["latin", "latin-ext"],
  axes: ["opsz"],
  style: ["normal", "italic"],
  display: "swap",
  variable: "--font-literata",
});

/** Only for "Art & Soul" and rare accents, never long text. Not preloaded: it is never the first thing on screen. */
export const pinyon = Pinyon_Script({
  subsets: ["latin", "latin-ext"],
  weight: "400",
  display: "swap",
  preload: false,
  variable: "--font-pinyon",
});
