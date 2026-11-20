import type { PageKey } from "@/lib/routes";

// Întrebări frecvente pe Acasă. Text copiat din .aidesigner/canvas/project/Faq3Carduri.dc.html
// Răspunsul e o listă de bucăți: text simplu sau link către o pagină.
type Part = string | { page: PageKey; text: string };

export const FAQ = {
  title: "Întrebări frecvente",
  items: [
    {
      q: "Trebuie să știu să lucrez cu lutul?",
      a: ["Deloc. Majoritatea celor care vin la atelierele mele ating lutul pentru prima dată. Te ghidez pas cu pas."],
    },
    {
      q: "Pot veni singur(ă)?",
      a: ["Sigur. Mulți vin singuri și pleacă făcând parte dintr-o comunitate."],
    },
    {
      q: "Nu știu ce mi se potrivește. De unde încep?",
      a: [
        "Dacă vrei să încerci, un ",
        { page: "ateliereDeGrup", text: "atelier de grup" },
        " e cel mai simplu început. Dacă vrei ceva doar pentru tine, alege un ",
        { page: "atelierPrivat", text: "atelier privat" },
        " sau o ",
        { page: "consiliere", text: "ședință de consiliere" },
        ". Poți explora opțiunile pe site sau ",
        { page: "contact", text: "îmi poți scrie" },
        " și te ajut să alegi.",
      ],
    },
  ],
  other: {
    ask: "Ai altă întrebare?",
    reply: "Îți răspundem în maxim 24 de ore.",
    write: "Scrie-mi",
    all: "Toate întrebările",
  },
} as const satisfies {
  title: string;
  items: readonly { q: string; a: readonly Part[] }[];
  other: Record<string, string>;
};
