import type { ImageKey } from "@/generated/images";

// „Ce spun oamenii”: testimoniale + benzile de fotografii. Text copiat din .aidesigner/canvas/project/OameniB2.dc.html
// The testimonials themselves live in src/content/testimoniale.ts.

type BandItem = { image: ImageKey; alt: string; position: string };

export const OAMENI = {
  title: "Ce spun oamenii",
  gallery: "Vezi toată galeria",
  instagram: (handle: string) => `${handle} pe Instagram`,
  carousel: "carusel",
  carouselLabel: "Testimoniale",
  slide: "testimonial",
  slideLabel: (i: number, n: number) => `${i} din ${n}`,
  dot: (i: number) => `Testimonialul ${i}`,
  prev: "Testimonialul anterior",
  next: "Testimonialul următor",
  stop: "Oprește mișcarea",
  start: "Pornește mișcarea",
  bandTop: [
    {
      image: "atelier-hero",
      alt: "Atelierul din octombrie: opt oameni în jurul unei mese cu lut, ceai și prăjitură",
      position: "50% 55%",
    },
    {
      image: "placeholder-pictat",
      alt: "O femeie pictează un bol de ceramică (fotografie provizorie)",
      position: "40% 50%",
    },
    {
      image: "placeholder-consiliere",
      alt: "Două persoane stau la masă, cu câte o cană în mâini (fotografie provizorie)",
      position: "50% 50%",
    },
    {
      image: "placeholder-piese",
      alt: "Boluri de ceramică arse, în culori diferite (fotografie provizorie)",
      position: "50% 40%",
    },
    {
      image: "servicii-companii",
      alt: "Doi participanți își dau din mână în mână un bol de lut, la atelierul din octombrie",
      position: "40% 50%",
    },
    {
      image: "placeholder-copii",
      alt: "Un copil zâmbește, cu un vas de lut în mâini (fotografie provizorie)",
      position: "60% 35%",
    },
  ] satisfies BandItem[],
  bandBottom: [
    {
      image: "placeholder-privat",
      alt: "Mâini care modelează un bol de lut (fotografie provizorie)",
      position: "50% 40%",
    },
    {
      image: "placeholder-grup",
      alt: "Un grup lucrează lutul într-un atelier de ceramică (fotografie provizorie)",
      position: "50% 45%",
    },
    {
      image: "servicii-grup",
      alt: "Masa atelierului din octombrie văzută de sus, cu lut, căni și pensule",
      position: "50% 50%",
    },
    {
      image: "placeholder-companii",
      alt: "Mâini care își dau din mână în mână un vas de lut (fotografie provizorie)",
      position: "50% 45%",
    },
    {
      image: "placeholder-retreat",
      alt: "Cabană de lemn într-o pădure de pini (fotografie provizorie)",
      position: "50% 60%",
    },
    {
      image: "placeholder-pictat",
      alt: "O femeie pictează un bol de ceramică (fotografie provizorie)",
      position: "40% 50%",
    },
  ] satisfies BandItem[],
} as const;
