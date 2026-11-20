import { readdirSync, readFileSync } from "node:fs";
import path from "node:path";

// The content rules from CLAUDE.md, as a test: if a text breaks one, `npm test` fails and names the file.

/** Sentences where a normally forbidden word is correct (the legal delimitations required by CLAUDE.md). */
const ALLOWED_PHRASES = [
  "terapia ocupațională", // copii: „nu înlocuiesc logopedia, terapia ocupațională sau kinetoterapia”
  "terapii experiențiale și artterapie", // Alessia studiază (not a service she offers)
  // Her degrees, named as the diplomas name them (approved canvas copy): facts, not titles or services she offers.
  "cu licență în Psihologie", // Acasă, „Despre”
  "Am absolvit Psihologia", // Despre noi, the opening
  "Licență în Psihologie", // Despre noi, „Formări”
  "Psihodiagnoză, Psihoterapie Experiențială Unificatoare și Dezvoltare Personală", // Despre noi, „Formări”: the master's programme
];

const RULES: { name: string; pattern: RegExp }[] = [
  { name: "ș/ț must use comma below, not cedilla (ş ţ)", pattern: /[şţŞŢ]/ },
  { name: "Alessia is not a psychologist", pattern: /psiholog/i },
  { name: "Alessia is not a psychotherapist", pattern: /psihoterapeut/i },
  { name: "„terapie” / „art-terapie” is not a service offered", pattern: /\b(art-?)?terapi(e|a|i|ei)\b/i },
  { name: "the workshop address is never published", pattern: /Elefterie/i },
  {
    name: "collaborators are „colaboratoare”, not team or co-founders",
    pattern: /co-?fondatoare|co-?organizatoare|echipa AVA|echipa noastră/i,
  },
];

export function contentViolations(text: string): string[] {
  let t = text;
  for (const phrase of ALLOWED_PHRASES) t = t.split(phrase).join("");
  return RULES.filter((r) => r.pattern.test(t)).map((r) => r.name);
}

function sourceFiles(dir: string): string[] {
  return readdirSync(dir, { recursive: true, withFileTypes: true })
    .filter((e) => e.isFile() && /\.(ts|tsx)$/.test(e.name))
    .map((e) => path.join(e.parentPath, e.name))
    .filter((f) => !f.includes(`${path.sep}generated${path.sep}`));
}

describe("content rules (CLAUDE.md)", () => {
  it("catch what they should (self-check)", () => {
    expect(contentViolations("Sunt psiholog")).toHaveLength(1);
    expect(contentViolations("ședințe de art-terapie")).toHaveLength(1);
    expect(contentViolations("Atelier de ceramică şi pictură")).toHaveLength(1);
    expect(contentViolations("Strada Elefterie 31")).toHaveLength(1);
    expect(contentViolations("colegele din echipa AVA")).toHaveLength(1);
  });

  it("allow the required legal delimitations", () => {
    expect(contentViolations("Nu înlocuiește psihoterapia sau tratamentul medical.")).toEqual([]);
    expect(contentViolations("Nu înlocuiesc logopedia, terapia ocupațională sau kinetoterapia.")).toEqual([]);
    expect(contentViolations("Studiez terapii experiențiale și artterapie.")).toEqual([]);
    expect(contentViolations("Cere o ofertă pentru echipa ta")).toEqual([]);
  });

  it.each(sourceFiles(path.resolve(import.meta.dirname, "../../src")))("%s follows them", (file) => {
    expect(contentViolations(readFileSync(file, "utf8"))).toEqual([]);
  });
});
