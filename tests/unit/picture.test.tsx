// @vitest-environment jsdom
import { render, screen } from "@testing-library/react";
import { Picture } from "@/components/ui/Picture";

describe("<Picture>", () => {
  it("offers AVIF first, then WebP, at several widths", () => {
    const { container } = render(<Picture image="hero-lut" alt="Lut sculptat în valuri" sizes="100vw" />);
    const sources = container.querySelectorAll("source");
    expect([...sources].map((s) => s.getAttribute("type"))).toEqual(["image/avif", "image/webp"]);
    expect(sources[0]?.getAttribute("srcset")).toMatch(/ 480w, .* 2880w$/);
  });

  it("reserves its space and lazy-loads by default", () => {
    render(<Picture image="hero-lut" alt="Lut sculptat în valuri" sizes="100vw" />);
    const img = screen.getByAltText("Lut sculptat în valuri");
    expect(img).toHaveAttribute("width", "2880");
    expect(img).toHaveAttribute("height", "1615");
    expect(img).toHaveAttribute("loading", "lazy");
  });

  it("loads the hero image immediately when it is the page's main image", () => {
    render(<Picture image="hero-lut" alt="Lut" sizes="100vw" priority />);
    const img = screen.getByAltText("Lut");
    expect(img).toHaveAttribute("loading", "eager");
    expect(img).toHaveAttribute("fetchpriority", "high");
  });

  it("keeps an explicit empty alt for decorative images", () => {
    const { container } = render(<Picture image="hero-lut" alt="" sizes="100vw" />);
    expect(container.querySelector("img")).toHaveAttribute("alt", "");
  });
});
