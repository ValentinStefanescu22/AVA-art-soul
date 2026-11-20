// What people said after a workshop, shown on Acasă („Ce spun oamenii”). The file Vali updates.
// To add one: copy a block, paste the words exactly as the person wrote them (with their consent), keep the order you
// want them shown in. The carousel counts them by itself.

export type Testimonial = {
  quote: string;
  /** First name only. */
  name: string;
};

export const TESTIMONIALE: Testimonial[] = [
  { quote: "Foarte frumos și cozy, chiar am reușit să reflect asupra mea cât timp lucram cu lutul.", name: "Costin" },
  {
    quote:
      "A fost o experiență foarte plăcută și relaxantă. Pauzele de socializare dintre activități au fost exact ce trebuia.",
    name: "Mario",
  },
  {
    quote:
      "Mi-a plăcut «intenția» cu care am pornit atelierul și faptul că acum obiectul semnifică ceva cu adevărat deosebit pentru fiecare.",
    name: "Mădălina",
  },
  { quote: "O activitate foarte relaxantă într-un cadru intim și frumos. Revin cu siguranță!", name: "Adina" },
];
