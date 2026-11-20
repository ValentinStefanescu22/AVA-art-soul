// Despre noi. Texts exactly as on the approved canvas page „Despre noi: lucru” (DespreNoiDeschidere, Povestea4Interviu,
// Formari3DCentrat, Comunitate5Carduri), which took them from docs/continut-site.md.

/** One question of „Povestea”; `mark` is the sentence shown highlighted, `after` the text that follows it. */
type Qa = { q: string; a: { text: string; mark?: string; after?: string } };

export const DESPRE = {
  hero: {
    name: "Alessia Văideanu",
    role: "fondatoare",
    photoAlt: "Alessia Văideanu, fondatoarea AVA Art & Soul",
    lede: "Sunt Alessia, artist ceramist și consilier acreditat în dezvoltare personală.",
    body: "Am absolvit Psihologia și acum sunt masterandă în terapii experiențiale și artterapie. Iubesc să creez evenimente în cadrul cărora oamenii își dau voie să fie prezenți și îi ajut să rămână curioși față de ce prinde formă din mâinile lor, fără presiune și fără să simtă că trebuie să „știe să facă”.",
  },
  povestea: {
    title: "Povestea",
    qa: [
      {
        q: "Cum ai ajuns la lut și ce simțeai când lucrai cu el?",
        a: {
          text: "În primul an de facultate am simțit nevoia de o activitate care să mă ajute să mă reconectez cu latura mea creativă și ludică, pe care am reprimat-o din ce în ce mai mult pe măsură ce creșteam. ",
          mark: "Așa am ajuns la lut, fără să știu cât de mult avea să-mi schimbe drumul.",
          after:
            " Lucrând cu el, simțeam liniște și curiozitate, iar acum este modalitatea care mă ajută să mă apropii mai mult de copilul meu interior.",
        },
      },
      {
        q: "Când ți-ai dat seama că nu e doar despre ceramică, ci despre oameni?",
        a: {
          text: "Cu timpul, mi-am dat seama că modelajul în lut nu este doar un prilej de conectare cu sinele, ci și cu ceilalți oameni cu care stai la masă. ",
          mark: "Când mâinile sunt ocupate, oamenii încep să vorbească altfel: mai sincer, mai blând, mai aproape unii de alții.",
        },
      },
      {
        q: "De ce ai creat AVA Art & Soul?",
        a: {
          text: "AVA a pornit dintr-o pasiune, însă pe parcurs am descoperit că, în timp ce mâinile lucrează, mintea se liniștește, oamenii își dau voie să se relaxeze. Așa a devenit AVA un loc de conectare, comunitate și prezență, unde creăm împreună conștient.",
        },
      },
    ] as readonly Qa[],
  },
  formari: {
    title: "Formări",
    items: [
      { title: "Consilier pentru dezvoltare personală", where: "Sandonia Institute", when: "2026" },
      { title: "Licență în Psihologie", where: "Universitatea Transilvania Brașov", when: "2026" },
      {
        title: "Masterat: Psihodiagnoză, Psihoterapie Experiențială Unificatoare și Dezvoltare Personală",
        where: "FPSE, Universitatea din București",
        when: "în curs",
      },
      { title: "Ceramică", where: "Cursuri de specializare la Brașov", when: "3+ ani" },
    ],
  },
  comunitate: {
    title: "Comunitatea AVA",
    intro:
      "Comunitatea AVA înseamnă oamenii alături de care creez și cei care iau parte la evenimentele noastre. AVA este proiectul meu, dar îmi place să creez experiențe și alături de alți artiști și antreprenori care cred în aceleași lucruri ca mine.",
    people: [
      { name: "Samargiu Casandra", role: "Social Media & Brand Manager" },
      { name: "Ramona Nichifor", role: "Colaboratoare · Artă & Povești" },
      { name: "Iuliana Petrescu", role: "Colaboratoare · Facilitatoare" },
      { name: "Valentin Stefanescu", role: "Specialist IT" },
    ],
  },
} as const;
