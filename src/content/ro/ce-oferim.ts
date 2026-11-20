import type { ImageKey } from "@/generated/images";
import type { PageKey } from "@/lib/routes";

// Ce oferim. Texts exactly as on the approved canvas page „Ce oferim: lucru” (CFPagina1Comutator, CFDeCe).
// The photos are provisional (Unsplash, assets/images/placeholder/SURSE.txt) until AVA's own photo shoot.

export type ServiceCard = {
  page: PageKey;
  name: string;
  line: string;
  meta: string;
  link: string;
  image: ImageKey;
  alt: string;
  /** object-position of the photo inside its frame */
  focus: string;
  /** Formats listed on the wide card (Pentru companii). */
  formats?: readonly string[];
};

export type ServiceTab = { id: string; label: string; icon: "vase" | "people" | "sun"; cards: readonly ServiceCard[] };

export const CE_OFERIM = {
  title: "Ce oferim",
  lede: "Ateliere cu lut, consiliere și retreaturi pentru momentele în care ai nevoie să te auzi din nou. Pentru tine sau pentru echipa ta.",
  tabsLabel: "Pentru cine",
  tabs: [
    {
      id: "tine",
      label: "Pentru tine",
      icon: "vase",
      cards: [
        {
          page: "ateliereDeGrup",
          name: "Ateliere de grup",
          line: "În fiecare lună ne strângem în jurul lutului, cu o temă nouă de fiecare dată.",
          meta: "3 ore · max. 8 persoane · de la 200 lei",
          link: "Vezi următoarele ateliere",
          image: "placeholder-grup",
          alt: "Un grup lucrează la roata olarului într-un atelier de ceramică (fotografie provizorie)",
          focus: "50% 45%",
        },
        {
          page: "atelierPrivat",
          name: "Atelier privat 1:1",
          line: "Lutul, tu și eu. Un atelier de modelaj, în ritmul tău, fără grup și fără grabă.",
          meta: "pentru adulți și copii · de la 220 lei",
          link: "Află mai multe",
          image: "placeholder-privat",
          alt: "O femeie modelează un bol de lut la masă (fotografie provizorie)",
          focus: "50% 35%",
        },
        {
          page: "consiliere",
          name: "Consiliere 1:1",
          line: "Te susțin în drumul tău și te ghidez spre versiunea ta autentică.",
          meta: "60–90 min · online sau față în față · 180 lei / oră",
          link: "Află mai multe",
          image: "placeholder-consiliere",
          alt: "Două persoane stau la masă, cu câte o cană în mâini (fotografie provizorie)",
          focus: "50% 50%",
        },
        {
          page: "retreaturi",
          name: "Retreaturi",
          line: "Câteva zile departe de oraș, cu lut, natură, liniște și oameni care caută același lucru ca tine.",
          meta: "în curând",
          link: "Anunță-mă la lansare",
          image: "placeholder-retreat",
          alt: "Cabană de lemn într-o pădure de pini (fotografie provizorie)",
          focus: "50% 60%",
        },
      ],
    },
    {
      id: "companii",
      label: "Pentru companii",
      icon: "people",
      cards: [
        {
          page: "pentruCompanii",
          name: "Pentru companii",
          line: "Evenimente de autocunoaștere și conectare pentru echipe, în care lutul este unealta.",
          meta: "4–16 persoane · la voi sau în locații partenere · ofertă personalizată",
          link: "Cere o ofertă",
          image: "placeholder-companii",
          alt: "Mâini care își dau din mână în mână un vas de lut (fotografie provizorie)",
          focus: "50% 40%",
          formats: [
            "Atelier de 3 ore modelaj în lut",
            "Jumătate de zi cu lut și teme de wellbeing",
            "Program lunar de wellbeing",
            "Teambuilding la cerere",
          ],
        },
      ],
    },
    {
      id: "copii",
      label: "Pentru școli și copii",
      icon: "sun",
      cards: [
        {
          page: "scoliCopii",
          name: "Pentru școli și copii",
          line: "Modelaj în lut pentru școli și afterschool, în joacă: copiii învață despre argilă și își iau piesa acasă.",
          meta: "de la 6 ani · de la 50 lei / copil",
          link: "Află mai multe",
          image: "placeholder-copii",
          alt: "Un copil zâmbește, cu un vas de lut în mâini (fotografie provizorie)",
          focus: "60% 35%",
        },
      ],
    },
  ] satisfies readonly ServiceTab[],
  deCe: {
    title: "De ce să alegi AVA Art & Soul?",
    // Still to come from Vali: stays visible as a placeholder until then (CLAUDE.md: never invent it).
    text: "[TEXTUL PENTRU „DE CE SĂ ALEGI AVA ART & SOUL?”: VINE DE LA VALI]",
  },
};
