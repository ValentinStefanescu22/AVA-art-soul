import type { ImageKey } from "@/generated/images";

// „Următorul atelier”: cardul + povestea foto. Text copiat din .aidesigner/canvas/project/UrmatorulA.dc.html
// (varianta sold out); varianta cu locuri libere din UrmatorulB.dc.html. Datele atelierului (dată, oră, zonă, preț,
// locuri, descriere) vin din src/content/ateliere.ts.

type Photo = { image: ImageKey; alt: string; position: string };

export const URMATORUL = {
  title: "Următorul atelier",
  soldOut: "Sold out",
  /** „15 noiembrie 2026, duminică, ora 17:00 (3 ore)” */
  at: "ora",
  hours: (n: number) => `${n} ore`,
  /** Visible placeholders while a workshop's time or place isn't decided (as on the Ateliere de grup tickets). */
  todoTime: "[ORA]",
  todoZone: "[LOCAȚIA]",
  facts: { where: "Unde", price: "Preț", seats: "Locuri", facilitator: "Facilitează" },
  lei: (n: number) => `${n} lei`,
  facilitator: "Alessia, AVA Art & Soul",
  note: (lei: number) => `${lei} lei, include toate materialele, îndrumarea și o băutură și o gustare făcute în casă.`,
  seatsTaken: (n: number) => `Toate cele ${n} locuri sunt ocupate`,
  seatsFree: (n: number) => `Doar ${n} locuri`,
  seatsCall: (n: number) => `Doar ${n} locuri, rezervă-ți locul acum`,
  signUp: "Mă înscriu",
  seeNext: "Vezi următoarele ateliere",
  /** „Următoarele: 6 și 13 decembrie.” */
  nextList: (days: string) => `Următoarele: ${days}.`,
  and: "și",
  story: {
    prev: "Cadrul anterior",
    next: "Cadrul următor",
    /** Last frame, after the description. */
    end: "Piesa modelată și pictată de tine rămâne a ta, după ardere.",
    nextWorkshops: "Următoarele ateliere",
    avatarImage: "alessia-stamp" as ImageKey,
    /** One per frame: cover, the description in three parts, the last frame. */
    photos: [
      {
        image: "atelier-hero",
        alt: "Masa atelierului din octombrie: oameni care lucrează lutul, cu ceai și prăjitură",
        position: "62% 50%",
      },
      {
        image: "servicii-companii",
        alt: "Doi participanți își dau din mână în mână un bol de lut, la atelierul din octombrie",
        position: "40% 50%",
      },
      {
        image: "placeholder-pictat",
        alt: "O femeie pictează un bol de ceramică cu pensula (fotografie provizorie)",
        position: "42% 50%",
      },
      {
        image: "atelier-hero",
        alt: "Prăjitură făcută în casă și căni pe masa atelierului din octombrie",
        position: "52% 60%",
      },
      {
        image: "placeholder-piese",
        alt: "Boluri de ceramică arse, în culori diferite (fotografie provizorie)",
        position: "50% 50%",
      },
    ] satisfies Photo[],
  },
  // propus de Claude, de aprobat: shown only when no workshop date is set.
  empty: {
    text: "Data următorului atelier o anunț în curând.",
    link: "Vezi atelierele de grup",
  },
} as const;
