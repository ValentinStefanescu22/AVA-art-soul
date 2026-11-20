// Acasă, the hero „Ștampila în lut” (source: .aidesigner/canvas/project/HeroAnuntCentrat.dc.html).

export const HERO = {
  strip: {
    label: "Următorul atelier",
    soldOut: "Sold out",
    signUp: "Mă înscriu",
    at: "ora",
  },
  soul: "Art & Soul",
  /** Read only by screen readers, before the visible title: the page's name. */
  titleHidden: "AVA Art & Soul: ",
  title: ["Creație.", "Conexiune.", "Autocunoaștere."],
  lede: "Ateliere cu lut, consiliere și retreaturi pentru momentele în care ai nevoie să te auzi din nou. Pentru tine sau pentru echipa ta.",
  forYou: "Pentru tine",
  forCompanies: "Pentru companii",
  sealText: "AVA · ART & SOUL · AUTOCUNOAȘTERE PRIN CREAȚIE · ",
  /** The clay photo is decoration: the title says what the page is. */
  photoAlt: "",
} as const;

/** Visible placeholders for details not decided yet (CLAUDE.md: never invent them). */
export const PLACEHOLDER = { time: "[ORA]", zone: "[LOCAȚIA]" } as const;
