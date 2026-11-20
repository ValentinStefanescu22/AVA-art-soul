import type { Atelier } from "@/content/ateliere";

// Dates on the site are Bucharest dates written the Romanian way: „duminică, 6 decembrie”.
const TZ = "Europe/Bucharest";

/** Noon on that day, so the weekday never shifts with the time zone. */
const at = (ymd: string) => new Date(`${ymd}T12:00:00Z`);

const fmt = (opts: Intl.DateTimeFormatOptions) => new Intl.DateTimeFormat("ro-RO", { timeZone: TZ, ...opts });
const WEEKDAY = fmt({ weekday: "long" });
const DAY = fmt({ day: "numeric" });
const MONTH = fmt({ month: "long" });
const YEAR = fmt({ year: "numeric" });

export type DateParts = { weekday: string; day: string; month: string; year: string };

/** { weekday: "duminică", day: "6", month: "decembrie", year: "2026" } */
export function dateParts(ymd: string): DateParts {
  const d = at(ymd);
  return { weekday: WEEKDAY.format(d), day: DAY.format(d), month: MONTH.format(d), year: YEAR.format(d) };
}

/** Today's date in Bucharest, YYYY-MM-DD. */
export function todayInBucharest(now: Date = new Date()): string {
  return new Intl.DateTimeFormat("en-CA", { timeZone: TZ }).format(now);
}

/** Workshops from today on, nearest first. A workshop stays listed on its own day. */
export function upcoming(list: readonly Atelier[], today: string = todayInBucharest()): Atelier[] {
  return list.filter((a) => a.date >= today).sort((a, b) => a.date.localeCompare(b.date));
}
