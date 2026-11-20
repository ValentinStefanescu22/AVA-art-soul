import { headerState } from "@/components/layout/headerState";
import { shouldCloseAfterDrag } from "@/components/layout/MobileMenu";
import { pageAt, sectionOf } from "@/lib/routes";
import { subscribe, validateNewsletter } from "@/lib/newsletter";

describe("header state", () => {
  it("is the full bar at the very top and the pill once you scroll", () => {
    expect(headerState(0, 0, null).sc).toBe("0");
    expect(headerState(9, 0, null).sc).toBe("1");
  });

  it("uses cream text over the dark hero and ink text once past it", () => {
    expect(headerState(0, 0, 700).tone).toBe("dark");
    expect(headerState(800, 0, -100).tone).toBe("light");
    expect(headerState(0, 0, null).tone).toBe("light"); // a page without a dark hero
  });

  it("rises from under Acasă's announcement strip, never further", () => {
    expect(headerState(10, 42, null).y).toBe(10);
    expect(headerState(500, 42, null).y).toBe(42);
    expect(headerState(-30, 42, null).y).toBe(0); // iOS rubber-band scroll above the top
  });
});

describe("which page and menu entry a URL belongs to", () => {
  it("finds the page", () => {
    expect(pageAt("/ro")).toBe("acasa");
    expect(pageAt("/ro/ce-oferim/consiliere")).toBe("consiliere");
    expect(pageAt("/en/despre-noi/")).toBe("despreNoi");
    expect(pageAt("/ro/nu-exista")).toBeNull();
  });

  it("puts service pages under Ce oferim", () => {
    expect(sectionOf("consiliere")).toBe("ceOferim");
    expect(sectionOf("contact")).toBe("contact");
  });
});

describe("mobile menu drag", () => {
  it("closes after a long drag or a quick flick, springs back otherwise", () => {
    expect(shouldCloseAfterDrag(120, 400)).toBe(true);
    expect(shouldCloseAfterDrag(60, 50)).toBe(true); // 1.2 px/ms
    expect(shouldCloseAfterDrag(40, 400)).toBe(false);
  });
});

describe("newsletter", () => {
  it("asks for a real email and the consent", () => {
    expect(validateNewsletter({ email: "ana@exemplu.ro", consent: true })).toEqual({});
    expect(validateNewsletter({ email: "ana@exemplu", consent: true })).toEqual({ email: true });
    expect(validateNewsletter({ email: " ana@exemplu.ro ", consent: false })).toEqual({ consent: true });
  });

  it("refuses to pretend in production while MailerLite isn't connected", async () => {
    expect(await subscribe("ana@exemplu.ro", { url: "", dev: false })).toEqual({ ok: false, reason: "unavailable" });
  });

  it("posts the email to the MailerLite form endpoint", async () => {
    const fetchImpl = vi.fn(async () => new Response(JSON.stringify({ success: true }), { status: 200 }));
    const res = await subscribe(" ana@exemplu.ro ", { url: "https://assets.mailerlite.com/x", fetchImpl, dev: false });
    expect(res).toEqual({ ok: true });
    const body = (fetchImpl.mock.calls[0] as unknown as [string, RequestInit])[1].body as FormData;
    expect(body.get("fields[email]")).toBe("ana@exemplu.ro");
  });

  it("reports network trouble instead of failing silently", async () => {
    const down = vi.fn(async () => Promise.reject(new TypeError("offline")));
    expect(await subscribe("a@b.ro", { url: "https://x.test", fetchImpl: down, dev: false })).toEqual({
      ok: false,
      reason: "network",
    });
    const refused = vi.fn(async () => new Response(JSON.stringify({ success: false }), { status: 200 }));
    expect((await subscribe("a@b.ro", { url: "https://x.test", fetchImpl: refused, dev: false })).ok).toBe(false);
  });
});
