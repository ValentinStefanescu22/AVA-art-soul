// @vitest-environment jsdom
import { render, screen } from "@testing-library/react";
import { Hero, stripDate } from "@/components/home/Hero";
import { imprint, springStep } from "@/components/home/HeroStamp";
import { ATELIERE } from "@/content/ateliere";
import { HERO } from "@/content/ro/home/hero";

beforeEach(() => {
  vi.stubGlobal(
    "IntersectionObserver",
    class {
      observe() {}
      disconnect() {}
    },
  );
  vi.stubGlobal("matchMedia", () => ({ matches: true }));
});
afterEach(() => vi.useRealTimers());

describe("the woodsprite light", () => {
  it("settles on its target without overshooting (critically damped spring)", () => {
    const p = { x: 0, v: 0 };
    let max = 0;
    for (let i = 0; i < 120; i++) {
      springStep(p, 100, 1 / 60);
      max = Math.max(max, p.x);
    }
    expect(p.x).toBeCloseTo(100, 0);
    expect(max).toBeLessThanOrEqual(100.5);
  });

  it("throws the imprint's shadow away from the light, longer when the light is low", () => {
    const near = imprint(10, 0, 100, 1); // light just right of the stamp's centre
    const far = imprint(300, 0, 100, 1);
    expect(near.ux).toBeLessThan(0); // shadow goes left
    expect(far.shade).toBeGreaterThan(near.shade);
    expect(imprint(10, 0, 100, 0).shade).toBe(0); // nothing before the stamp is pressed
  });
});

describe("<Hero>", () => {
  it("writes the strip's date the Romanian way, with a visible placeholder for an unset time", () => {
    const w = { ...ATELIERE[1]!, date: "2026-12-06", time: null };
    expect(stripDate(w)).toBe("duminică, 6 decembrie, ora [ORA]");
    expect(stripDate({ ...w, time: "17:00" })).toBe("duminică, 6 decembrie, ora 17:00");
  });

  it("announces the next workshop and links the strip to Ateliere de grup", () => {
    vi.useFakeTimers({ toFake: ["Date"] });
    vi.setSystemTime(new Date("2026-11-20T10:00:00Z"));
    render(<Hero lang="ro" />);
    expect(screen.getByText("duminică, 6 decembrie, ora [ORA]")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /Mă înscriu/ })).toHaveAttribute("href", "/ro/ce-oferim/ateliere-de-grup");
  });

  it("hides the strip when nothing is scheduled", () => {
    vi.useFakeTimers({ toFake: ["Date"] });
    vi.setSystemTime(new Date("2030-01-01T10:00:00Z"));
    const { container } = render(<Hero lang="ro" />);
    expect(container.querySelector("[data-hx-strip]")).toBeNull();
  });

  it("has one h1 with the brand for screen readers, and both main actions", () => {
    render(<Hero lang="ro" />);
    expect(screen.getByRole("heading", { level: 1 })).toHaveTextContent(HERO.titleHidden + "Creație.");
    expect(screen.getByRole("link", { name: HERO.forYou })).toHaveAttribute("href", "/ro/ce-oferim");
    expect(screen.getByRole("link", { name: HERO.forCompanies })).toHaveAttribute(
      "href",
      "/ro/ce-oferim/pentru-companii",
    );
  });

  it("loads the clay photo first (it is the page's largest image)", () => {
    const { container } = render(<Hero lang="ro" />);
    expect(container.querySelector("img")).toHaveAttribute("fetchpriority", "high");
  });
});
