import { ATELIERE, type Atelier } from "@/content/ateliere";
import { dateParts, todayInBucharest, upcoming } from "@/lib/dates";

const a = (id: string, date: string): Atelier => ({ ...ATELIERE[0]!, id, date });

describe("dates", () => {
  it("writes them the Romanian way", () => {
    expect(dateParts("2026-12-06")).toEqual({ weekday: "duminică", day: "6", month: "decembrie", year: "2026" });
  });

  it("uses Bucharest's day, not the server's", () => {
    // 23:30 UTC on 5 Dec is already 6 Dec in Bucharest (UTC+2).
    expect(todayInBucharest(new Date("2026-12-05T23:30:00Z"))).toBe("2026-12-06");
  });

  it("lists the coming workshops nearest first, keeping today's", () => {
    const list = [a("c", "2026-12-13"), a("past", "2026-11-15"), a("b", "2026-12-06")];
    expect(upcoming(list, "2026-12-06").map((x) => x.id)).toEqual(["b", "c"]);
    expect(upcoming(list, "2027-01-01")).toEqual([]);
  });
});

describe("content/ateliere.ts (the file Vali edits)", () => {
  it.each(ATELIERE)("$id is well formed", (w) => {
    expect(w.date).toMatch(/^\d{4}-\d{2}-\d{2}$/);
    expect(Number.isNaN(Date.parse(w.date))).toBe(false);
    if (w.time !== null) expect(w.time).toMatch(/^([01]\d|2[0-3]):[0-5]\d$/);
    expect(w.priceLei).toBeGreaterThan(0);
    expect(w.seats).toBeGreaterThan(0);
    if (w.paymentLink !== null) expect(w.paymentLink).toMatch(/^https:\/\/(buy|checkout)\.stripe\.com\//);
  });

  it("has unique ids", () => {
    expect(new Set(ATELIERE.map((w) => w.id)).size).toBe(ATELIERE.length);
  });
});
