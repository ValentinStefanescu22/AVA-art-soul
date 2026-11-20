// @vitest-environment jsdom
import { render } from "@testing-library/react";
import { StrictMode } from "react";
import { RevealObserver, revealIndex } from "@/components/ui/RevealObserver";

vi.mock("next/navigation", () => ({ usePathname: () => "/ro" }));

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
  live.forEach(({ cb, els }) =>
    cb(
      [...els].map((target) => ({ target, isIntersecting: true }) as IntersectionObserverEntry),
      {} as never,
    ),
  );

function page() {
  document.body.innerHTML = `<section><div data-reveal="" id="a"></div><div data-reveal="" id="b"></div><p></p><div data-reveal="" id="c"></div></section>`;
  // Everything starts below the fold (jsdom has no layout: fake the positions).
  for (const el of document.querySelectorAll("[data-reveal]"))
    el.getBoundingClientRect = () => ({ top: 2000 }) as DOMRect;
}

beforeEach(() => {
  live.clear();
  vi.stubGlobal("IntersectionObserver", FakeIO);
  vi.stubGlobal("matchMedia", () => ({ matches: false }));
});

describe("scroll reveal", () => {
  it("counts earlier revealing siblings, for the 80ms stagger", () => {
    page();
    expect(["a", "b", "c"].map((id) => revealIndex(document.getElementById(id)!))).toEqual([0, 1, 2]);
  });

  it("hides blocks below the fold, then shows them when they reach the screen", () => {
    page();
    render(<RevealObserver />);
    expect(document.getElementById("a")!.dataset.reveal).toBe("wait");
    show();
    expect(document.getElementById("a")!.dataset.reveal).toBe("in");
  });

  it("never leaves a block hidden when React runs the effect twice (dev mode)", () => {
    page();
    render(
      <StrictMode>
        <RevealObserver />
      </StrictMode>,
    );
    show();
    for (const el of document.querySelectorAll("[data-reveal]")) expect((el as HTMLElement).dataset.reveal).toBe("in");
  });

  it("hides nothing for visitors who asked for less motion", () => {
    page();
    vi.stubGlobal("matchMedia", () => ({ matches: true }));
    render(<RevealObserver />);
    expect(document.querySelectorAll('[data-reveal="wait"]')).toHaveLength(0);
  });
});
