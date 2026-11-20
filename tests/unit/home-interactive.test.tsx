// @vitest-environment jsdom
import { act, fireEvent, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { Testimoniale } from "@/components/home/Testimoniale";
import { dayList, storyLines, UrmatorulAtelier } from "@/components/home/UrmatorulAtelier";
import { ATELIERE } from "@/content/ateliere";
import { TESTIMONIALE } from "@/content/testimoniale";

// A fake IntersectionObserver we can drive by hand: `show()` tells every live observer its elements are on screen.
const live = new Set<{ cb: IntersectionObserverCallback; els: Set<Element> }>();
class FakeIO {
  entry: { cb: IntersectionObserverCallback; els: Set<Element> };
  constructor(cb: IntersectionObserverCallback) {
    this.entry = { cb, els: new Set() };
    live.add(this.entry);
  }
  observe = (el: Element) => void this.entry.els.add(el);
  unobserve = (el: Element) => void this.entry.els.delete(el);
  disconnect = () => void live.delete(this.entry);
}
const show = () =>
  act(() =>
    live.forEach(({ cb, els }) =>
      cb(
        [...els].map((target) => ({ target, isIntersecting: true }) as IntersectionObserverEntry),
        {} as never,
      ),
    ),
  );
const observed = () => [...live].flatMap((e) => [...e.els]);

let reduce = false;
beforeEach(() => {
  live.clear();
  reduce = false;
  vi.stubGlobal("IntersectionObserver", FakeIO);
  vi.stubGlobal("matchMedia", () => ({ matches: reduce }));
});
afterEach(() => vi.useRealTimers());

/** Pretend today is `ymd` (Bucharest). */
const today = (ymd: string) => {
  vi.useFakeTimers({ toFake: ["Date"] });
  vi.setSystemTime(new Date(`${ymd}T10:00:00Z`));
};
// jsdom has no AnimationEvent, so React listens for the prefixed name: fire both.
const animationEnd = (el: Element) =>
  act(() => {
    fireEvent.animationEnd(el);
    fireEvent(el, new Event("webkitAnimationEnd", { bubbles: true }));
  });
const textIs = (t: string) => (_: string, el: Element | null) => el?.tagName === "P" && el.textContent === t;

describe("<UrmatorulAtelier>", () => {
  it("shows the nearest upcoming workshop, with visible placeholders for its time and place", () => {
    today("2026-11-20");
    render(<UrmatorulAtelier lang="ro" />);
    expect(screen.getByText(textIs("6 decembrie 2026, duminică, ora [ORA] (3 ore)"))).toBeInTheDocument();
    expect(screen.getAllByText("[LOCAȚIA]").length).toBeGreaterThan(0);
    expect(screen.getByText("Doar 8 locuri")).toBeInTheDocument();
    expect(screen.getByText(textIs("Următoarele: 13 decembrie."))).toBeInTheDocument();
    expect(screen.queryByText("Sold out")).not.toBeInTheDocument();
  });

  it("offers „Mă înscriu” while there are seats, linking to Ateliere de grup until a payment link exists", () => {
    today("2026-11-20");
    render(<UrmatorulAtelier lang="ro" />);
    const links = screen.getAllByRole("link", { name: /Mă înscriu/ });
    expect(links.length).toBeGreaterThan(0);
    for (const a of links) expect(a).toHaveAttribute("href", "/ro/ce-oferim/ateliere-de-grup");
  });

  it("says „Sold out” when every seat is taken, and points to the next dates instead", () => {
    today("2026-11-15");
    render(<UrmatorulAtelier lang="ro" />);
    expect(screen.getAllByText("Sold out").length).toBeGreaterThan(0);
    expect(screen.getByText("Toate cele 8 locuri sunt ocupate")).toBeInTheDocument();
    expect(screen.getByText(textIs("15 noiembrie 2026, duminică, ora 17:00 (3 ore)"))).toBeInTheDocument();
    expect(screen.getAllByText("Cotroceni, sector 5").length).toBeGreaterThan(0);
    expect(screen.queryByRole("link", { name: /Mă înscriu/ })).not.toBeInTheDocument();
    expect(screen.getByRole("link", { name: "Vezi următoarele ateliere" })).toHaveAttribute(
      "href",
      "/ro/ce-oferim/ateliere-de-grup",
    );
    expect(screen.getByText(textIs("Următoarele: 6 și 13 decembrie."))).toBeInTheDocument();
  });

  it("falls back calmly when no workshop is planned", () => {
    today("2030-01-01");
    render(<UrmatorulAtelier lang="ro" />);
    expect(screen.getByRole("heading", { name: "Următorul atelier" })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /Vezi atelierele de grup/ })).toHaveAttribute(
      "href",
      "/ro/ce-oferim/ateliere-de-grup",
    );
    expect(screen.queryByRole("link", { name: /Mă înscriu/ })).not.toBeInTheDocument();
  });

  it("cuts the description into story frames where the sentence pauses, as in the design", () => {
    expect(storyLines(ATELIERE[0]!.description)).toEqual([
      "O seară liniștită cu lut, culoare și oameni noi. Modelăm împreună,",
      "apoi îți pictezi piesa cu underglaze, culori speciale pentru ceramică,",
      "iar între timp povestim și ne bucurăm de o băutură și o gustare făcute în casă.",
    ]);
    expect(storyLines(ATELIERE[1]!.description)).toHaveLength(3);
    expect(dayList(ATELIERE.slice(1))).toBe("6 și 13 decembrie");
    expect(dayList(ATELIERE)).toBe("15 noiembrie, 6 și 13 decembrie");
  });

  it("steps the story with the arrows and moves on by itself when a bar fills", () => {
    today("2026-11-20");
    const { container } = render(<UrmatorulAtelier lang="ro" />);
    const first = storyLines(ATELIERE[1]!.description)[0]!;
    const frame = () => screen.getByText(first).closest("div")!;
    expect(frame()).toHaveAttribute("inert");
    fireEvent.click(screen.getAllByRole("button", { name: "Cadrul următor" })[0]!);
    expect(frame()).not.toHaveAttribute("inert");
    fireEvent.click(screen.getAllByRole("button", { name: "Cadrul anterior" })[0]!);
    expect(frame()).toHaveAttribute("inert");

    show();
    animationEnd(container.querySelector("span > i")!);
    expect(frame()).not.toHaveAttribute("inert");
  });

  it("never starts the story by itself with reduced motion", () => {
    reduce = true;
    today("2026-11-20");
    render(<UrmatorulAtelier lang="ro" />);
    expect(observed()).toHaveLength(0);
  });
});

describe("<Testimoniale>", () => {
  const dot = (i: number) => screen.getByRole("button", { name: `Testimonialul ${i}` });
  const current = () => TESTIMONIALE.findIndex((_, i) => dot(i + 1).getAttribute("aria-current") === "true") + 1;
  const tick = () => animationEnd(dot(current()).querySelector("i")!);

  it("moves with the arrows, the dots and ← →, wrapping around", async () => {
    render(<Testimoniale lang="ro" />);
    const user = userEvent.setup();
    expect(current()).toBe(1);
    await user.click(screen.getByRole("button", { name: "Testimonialul următor" }));
    expect(current()).toBe(2);
    await user.click(screen.getByRole("button", { name: "Testimonialul anterior" }));
    await user.click(screen.getByRole("button", { name: "Testimonialul anterior" }));
    expect(current()).toBe(TESTIMONIALE.length);
    await user.click(dot(3));
    expect(current()).toBe(3);
    await user.keyboard("{ArrowLeft}");
    expect(current()).toBe(2);
    await user.keyboard("{ArrowRight}{ArrowRight}");
    expect(current()).toBe(4);
  });

  it("auto-advances quietly, then announces changes and stops for good once the visitor takes control", async () => {
    const { container } = render(<Testimoniale lang="ro" />);
    const region = screen.getByRole("region", { name: "Testimoniale" });
    expect(region).toHaveAttribute("aria-roledescription", "carusel");
    const sls = container.querySelector("[aria-live]")!;
    expect(sls).toHaveAttribute("aria-live", "off");
    tick();
    expect(current()).toBe(2);
    await userEvent.setup().click(screen.getByRole("button", { name: "Testimonialul următor" }));
    expect(current()).toBe(3);
    expect(sls).toHaveAttribute("aria-live", "polite");
    tick();
    expect(current()).toBe(3);
  });

  it("never moves by itself with reduced motion", () => {
    reduce = true;
    const { container } = render(<Testimoniale lang="ro" />);
    expect(container.querySelector("[aria-live]")).toHaveAttribute("aria-live", "polite");
    tick();
    expect(current()).toBe(1);
  });

  it("„Oprește mișcarea” pauses everything and can start it again", async () => {
    const { container } = render(<Testimoniale lang="ro" />);
    const user = userEvent.setup();
    const toggle = screen.getByRole("button", { name: "Oprește mișcarea" });
    expect(toggle).toHaveAttribute("aria-pressed", "false");
    await user.click(toggle);
    expect(toggle).toHaveAttribute("aria-pressed", "true");
    expect(toggle).toHaveAccessibleName("Pornește mișcarea");
    expect(container.querySelector("section")).toHaveAttribute("data-still");
    await user.click(toggle);
    expect(container.querySelector("section")).not.toHaveAttribute("data-still");
  });
});
