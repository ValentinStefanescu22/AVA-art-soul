import type { PageKey } from "@/lib/routes";

// Texts of the parts every page shares: header, mobile menu, footer.
// Approved by Vali on 11 nov 2026 (menu labels, newsletter line); the rest comes from the approved canvas.

export const NAV: { page: PageKey; label: string }[] = [
  { page: "acasa", label: "Acasă" },
  { page: "despreNoi", label: "Despre noi" },
  { page: "ceOferim", label: "Ce oferim" },
  { page: "evenimente", label: "Evenimente" },
  { page: "galerie", label: "Galerie" },
  { page: "contact", label: "Contact" },
];

export const SERVICES: { page: PageKey; label: string }[] = [
  { page: "ateliereDeGrup", label: "Ateliere de grup" },
  { page: "pentruCompanii", label: "Pentru companii" },
  { page: "consiliere", label: "Consiliere 1:1" },
  { page: "atelierPrivat", label: "Atelier privat 1:1" },
  { page: "retreaturi", label: "Retreaturi" },
  { page: "scoliCopii", label: "Pentru școli și copii" },
];

export const INFO: { page: PageKey; label: string }[] = [
  { page: "intrebariFrecvente", label: "Întrebări frecvente" },
  { page: "inscriere", label: "Înscrieri, plată și anulare" },
  { page: "termeni", label: "Termeni și condiții" },
  { page: "confidentialitate", label: "Politica de confidențialitate" },
  { page: "cookies", label: "Cookies" },
];

export const CONTACT = {
  email: "ava.events.26@gmail.com",
  phone: { display: "0730 301 996", href: "tel:+40730301996" },
  instagram: { handle: "@ava.art.soul", href: "https://www.instagram.com/ava.art.soul/" },
  area: "București",
} as const;

export const LEGAL = {
  company: "VAIDEANU ALESSIA-ALEXANDRA PFA",
  cui: "55380756",
  regCom: "F2026038934007",
  // Placeholder until Vali sends the registered office address (CLAUDE.md, „Legal”).
  office: "[ADRESA SEDIULUI]",
  anpc: { label: "ANPC · SAL", href: "https://anpc.ro/ce-este-sal/" },
} as const;

export const LAYOUT_COPY = {
  brand: "AVA Art & Soul",
  tagline: "autocunoaștere prin creație",
  mainNav: "Meniu principal",
  allServices: "Toate serviciile",
  openMenu: "Deschide meniul",
  menu: "Meniu",
  closeMenu: "Închide meniul",
  dragToClose: "Trage în jos ca să închizi",
  language: "Limba site-ului",
  back: "Ce oferim",
  breadcrumb: "Unde te afli", // propus de Claude, de aprobat (screen-reader label)
  skip: "Sari la conținut", // propus de Claude, de aprobat: visible only when tabbing, first thing on the page
  footer: {
    label: "Subsol",
    newsletterTitle: "Rămâi aproape…",
    newsletterLead: "Vești despre atelierele noi, înaintea tuturor, și 5% discount la următorul eveniment.",
    signature: "– Alessia Văideanu",
    sealText: "AVA · ART & SOUL · AUTOCUNOAȘTERE PRIN CREAȚIE · ",
    columns: { nav: "Navigare", services: "Ce oferim", info: "Informații", contact: "Contact" },
  },
  newsletter: {
    email: "Emailul tău",
    placeholder: "nume@exemplu.ro",
    submit: "Abonează-te",
    sending: "Se trimite…",
    consentBefore: "Sunt de acord să primesc emailuri de la AVA Art & Soul. Am citit ",
    consentLink: "Politica de confidențialitate",
    consentAfter: ".",
    done: "Mulțumesc! Codul de 5% te așteaptă în email.",
    // Error messages: propuse de Claude (20 nov 2026), de aprobat.
    errorEmail: "Scrie o adresă de email validă, de exemplu nume@exemplu.ro.",
    errorConsent: "Bifează acordul, ca să te putem abona.",
    errorNetwork: "Nu am reușit să te abonăm acum. Te rog încearcă din nou peste câteva minute.",
  },
} as const;
