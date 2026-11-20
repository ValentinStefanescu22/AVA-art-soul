// The group workshops (Ateliere de grup), the file Vali updates when Alessia sets a new date.
// The site shows the nearest upcoming one on Acasă (announcement strip + „Următorul atelier”) and all upcoming ones on
// „Ateliere de grup”. Past dates disappear by themselves at the next build (CI rebuilds every night).
//
// To add a workshop: copy a block, change the fields, keep the dates in YYYY-MM-DD. Unknown details stay null and
// show as a visible [PLACEHOLDER] until filled in.

export type Atelier = {
  /** Unique, e.g. "2026-12-06-craciun". Used in links and tests. */
  id: string;
  /** Day of the workshop, YYYY-MM-DD (Bucharest time). */
  date: string;
  /** Start time "HH:MM", or null while it isn't decided ([ORA]). */
  time: string | null;
  durationHours: number;
  title: string;
  /** One or two sentences, shown on the ticket. */
  description: string;
  /** Area or partner place, never the exact address (CLAUDE.md, „Locație”); null while unknown ([LOCAȚIA]). */
  zone: string | null;
  priceLei: number;
  seats: number;
  /** Set by hand for now; from E8 the payment Worker reports the seats left live. */
  soldOut: boolean;
  /** Stripe Payment Link (E8). null until payments are set up. */
  paymentLink: string | null;
};

export const ATELIERE: Atelier[] = [
  {
    id: "2026-11-15-socializare",
    date: "2026-11-15",
    time: "17:00",
    durationHours: 3,
    title: "Atelier de ceramică & socializare",
    description:
      "O seară liniștită cu lut, culoare și oameni noi. Modelăm împreună, apoi îți pictezi piesa cu underglaze, culori speciale pentru ceramică, iar între timp povestim și ne bucurăm de o băutură și o gustare făcute în casă.",
    zone: "Cotroceni, sector 5",
    priceLei: 200,
    seats: 8,
    soldOut: true,
    paymentLink: null,
  },
  {
    id: "2026-12-06-craciun",
    date: "2026-12-06",
    time: null,
    durationHours: 3,
    title: "Atelier cu tematică de Crăciun",
    description:
      "În spiritul sărbătorilor: ceramică și pictură pe ceramică în același atelier, cu pauze de socializare și gustări.",
    zone: null,
    priceLei: 200,
    seats: 8,
    soldOut: false,
    paymentLink: null,
  },
  {
    id: "2026-12-13-craciun",
    date: "2026-12-13",
    time: null,
    durationHours: 3,
    title: "Atelier cu tematică de Crăciun",
    description:
      "În spiritul sărbătorilor: ceramică și pictură pe ceramică în același atelier, cu pauze de socializare și gustări.",
    zone: null,
    priceLei: 200,
    seats: 8,
    soldOut: false,
    paymentLink: null,
  },
];
