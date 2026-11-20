import type { PageKey } from "@/lib/routes";
import type { ImageKey } from "@/generated/images";

// „Ce oferim”: acordeonul de fotografii. Text copiat din .aidesigner/canvas/project/CeFacem5Acordeon.dc.html
export const CE_OFERIM = {
  title: "Ce oferim",
  lede: "Pentru tine sau pentru echipa ta.",
  panels: [
    {
      page: "ateliereDeGrup",
      image: "placeholder-grup",
      position: "50% 45%",
      alt: "Un grup lucrează la roata olarului într-un atelier de ceramică (fotografie provizorie)",
      name: "Ateliere de grup",
      meta: "3 ore · max. 8 persoane · de la 200 lei",
      text: "În fiecare lună ne strângem în jurul lutului, cu o temă nouă de fiecare dată.",
      cta: "Vezi următoarele ateliere",
    },
    {
      page: "atelierPrivat",
      image: "placeholder-privat",
      position: "50% 35%",
      alt: "O femeie modelează un bol de lut la masă (fotografie provizorie)",
      name: "Atelier privat 1:1",
      meta: "pentru adulți și copii · de la 220 lei",
      text: "Lutul, tu și eu. Un atelier de modelaj, în ritmul tău, fără grup și fără grabă.",
      cta: "Rezervă un atelier privat",
    },
    {
      page: "consiliere",
      image: "placeholder-consiliere",
      position: "50% 50%",
      alt: "Două persoane stau la masă, cu câte o cană în mâini (fotografie provizorie)",
      name: "Consiliere 1:1",
      meta: "60–90 min · online sau față în față · 180 lei / oră",
      text: "Te susțin în drumul tău și te ghidez spre versiunea ta autentică.",
      cta: "Programează o ședință",
    },
    {
      page: "pentruCompanii",
      image: "placeholder-companii",
      position: "50% 40%",
      alt: "Mâini care își dau din mână în mână un vas de lut (fotografie provizorie)",
      name: "Pentru companii",
      meta: "4–16 persoane · la voi sau în locații partenere · ofertă personalizată",
      text: "Ateliere de autocunoaștere și conectare pentru echipe, în care lutul este unealta.",
      cta: "Cere o ofertă",
    },
    {
      page: "retreaturi",
      image: "placeholder-retreat",
      position: "50% 60%",
      alt: "Cabană de lemn într-o pădure de pini (fotografie provizorie)",
      name: "Retreaturi",
      meta: "în curând",
      text: "Câteva zile departe de oraș, cu lut, natură, liniște și oameni care caută același lucru ca tine.",
      cta: "Anunță-mă la lansare",
    },
    {
      page: "scoliCopii",
      image: "placeholder-copii",
      position: "60% 35%",
      alt: "Un copil zâmbește, cu un vas de lut în mâini (fotografie provizorie)",
      name: "Pentru școli și copii",
      meta: "de la 6 ani · 60 min · 50 lei / copil",
      text: "Modelaj în lut pentru școli și afterschool, în joacă: copiii învață despre argilă și își iau piesa acasă.",
      cta: "Află mai multe",
    },
  ],
} as const satisfies {
  title: string;
  lede: string;
  panels: readonly {
    page: PageKey;
    image: ImageKey;
    position: string;
    alt: string;
    name: string;
    meta: string;
    text: string;
    cta: string;
  }[];
};
