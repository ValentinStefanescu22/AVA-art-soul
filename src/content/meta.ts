import type { Locale } from "@/lib/i18n";
import type { PageKey } from "@/lib/routes";

export type PageMeta = { title: string; description: string };

// Search-result title and description of every page. Propus de Claude (20 nov 2026), de aprobat de Alessia.
// Titles get " · AVA Art & Soul" appended by the layout (except the home page, which carries the name itself).
// Descriptions: 70–160 characters, checked by tests/unit/meta.test.ts.
export const META: { ro: Record<PageKey, PageMeta> } & Partial<
  Record<Exclude<Locale, "ro">, Record<PageKey, PageMeta>>
> = {
  ro: {
    acasa: {
      title: "AVA Art & Soul · Ateliere de ceramică și consiliere în București",
      description:
        "Ateliere creative cu lut, consiliere în dezvoltare personală și retreaturi în București, cu Alessia Văideanu. Autocunoaștere prin creație.",
    },
    despreNoi: {
      title: "Despre noi",
      description:
        "Sunt Alessia Văideanu, artist ceramist și consilier acreditat în dezvoltare personală. Povestea AVA Art & Soul și comunitatea din jurul ei.",
    },
    ceOferim: {
      title: "Ce oferim",
      description:
        "Ateliere de grup, ateliere pentru companii, consiliere 1:1, ateliere private, retreaturi și ateliere pentru școli și copii, în București.",
    },
    ateliereDeGrup: {
      title: "Ateliere de ceramică în grup",
      description:
        "În fiecare lună ne strângem în jurul lutului, cu o temă nouă. 3 ore, gustare și băutură incluse, fără experiență. Vezi datele și înscrie-te.",
    },
    pentruCompanii: {
      title: "Ateliere de ceramică pentru companii",
      description:
        "Teambuilding și wellbeing cu lut pentru echipe: o pauză reală de la stres, în care colegii se descoperă ca oameni. Cere o ofertă personalizată.",
    },
    consiliere: {
      title: "Consiliere 1:1 în dezvoltare personală",
      description:
        "Ședințe individuale de consiliere în dezvoltare personală cu Alessia Văideanu, online sau față în față, în București. Programează o ședință.",
    },
    atelierPrivat: {
      title: "Atelier privat de ceramică 1:1",
      description:
        "Un atelier de ceramică doar pentru tine: modelaj privat sau autocunoaștere prin artă, în ritmul tău, cu Alessia Văideanu. Rezervă-ți locul.",
    },
    retreaturi: {
      title: "Retreaturi",
      description:
        "Retreaturi de creație și autocunoaștere prin artă cu AVA Art & Soul. Le pregătim acum: lasă-ne emailul și te anunțăm primul la lansare.",
    },
    scoliCopii: {
      title: "Ateliere de ceramică pentru școli și copii",
      description:
        "Ateliere de modelaj în lut pentru copii de la 6 ani și pentru școli (Școala altfel, Săptămâna verde): 60 de minute, cu materialele incluse.",
    },
    evenimente: {
      title: "Evenimente",
      description:
        "Evenimentele pe care le pregătește AVA Art & Soul în București. Abonează-te la newsletter și afli primul când anunțăm ceva nou.",
    },
    galerie: {
      title: "Galerie",
      description:
        "Fotografii din atelierele AVA Art & Soul: oameni, lut și piesele modelate împreună, de la ateliere de grup la evenimente pentru companii.",
    },
    contact: {
      title: "Contact",
      description:
        "Scrie-ne pentru ateliere, consiliere sau colaborări. Îți răspundem în maxim 24 de ore, pe email, telefon sau Instagram @ava.art.soul.",
    },
    intrebariFrecvente: {
      title: "Întrebări frecvente",
      description:
        "Răspunsuri despre ateliere, înscriere și plată, anulare, consiliere, ateliere pentru companii și pentru copii la AVA Art & Soul.",
    },
    inscriere: {
      title: "Înscriere, plată și anulare",
      description:
        "Cum te înscrii la atelierele AVA Art & Soul, cum plătești (online sau prin transfer bancar) și ce se întâmplă dacă nu mai poți ajunge.",
    },
    termeni: {
      title: "Termeni și condiții",
      description:
        "Termenii și condițiile de folosire a site-ului AVA Art & Soul și de participare la ateliere, ședințe de consiliere și evenimente.",
    },
    confidentialitate: {
      title: "Politica de confidențialitate",
      description:
        "Ce date personale colectează AVA Art & Soul, de ce, cât timp le păstrăm și ce drepturi ai conform GDPR. Pe scurt și pe înțeles.",
    },
    cookies: {
      title: "Cookies",
      description:
        "Site-ul AVA Art & Soul nu folosește cookies de marketing sau de urmărire. Află ce măsurăm, fără cookies, și cum îți protejăm datele.",
    },
    multumim: {
      title: "Mulțumim!",
      description:
        "Plata a fost primită și locul tău e confirmat. Detaliile, inclusiv adresa exactă, îți vin pe email.",
    },
    programareFacuta: {
      title: "Programarea e făcută",
      description: "Programarea ta la AVA Art & Soul e înregistrată. Confirmarea și detaliile îți vin pe email.",
    },
  },
};
