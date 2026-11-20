// @vitest-environment jsdom
import { act, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { CeOferim } from "@/components/home/CeOferim";
import { Coperta } from "@/components/home/Coperta";
import { FaqAcasa } from "@/components/home/FaqAcasa";
import { COPERTA } from "@/content/ro/home/coperta";
import { CE_OFERIM } from "@/content/ro/home/ce-oferim";
import { FAQ } from "@/content/ro/home/faq";
import { href } from "@/lib/routes";

describe("<Coperta>", () => {
  const [a, b] = COPERTA.roles;
  const btn = (w: string) => screen.getByRole("button", { name: new RegExp(w) });

  it("starts on the first role and switches on click", async () => {
    const { container } = render(<Coperta lang="ro" />);
    expect(btn(a.word)).toHaveAttribute("aria-pressed", "true");
    expect(btn(b.word)).toHaveAttribute("aria-pressed", "false");
    await userEvent.click(btn(b.word));
    expect(btn(b.word)).toHaveAttribute("aria-pressed", "true");
    expect(btn(a.word)).toHaveAttribute("aria-pressed", "false");
    expect(container.querySelector("section")).toHaveAttribute("data-r", "1");
  });

  it("switches with the keyboard (Tab focuses, Enter presses)", async () => {
    render(<Coperta lang="ro" />);
    await userEvent.tab();
    await userEvent.tab(); // first: role a, second: the "Povestea mea" link is after role b
    expect(btn(b.word)).toHaveAttribute("aria-pressed", "true");
    await userEvent.keyboard("{Enter}");
    expect(btn(b.word)).toHaveAttribute("aria-pressed", "true");
  });

  it("links to Despre noi", () => {
    render(<Coperta lang="ro" />);
    expect(screen.getByRole("link", { name: new RegExp(COPERTA.link) })).toHaveAttribute(
      "href",
      href("ro", "despreNoi"),
    );
  });
});

describe("<CeOferim>", () => {
  it("opens the hovered / focused panel and links each to its service page", async () => {
    const { container } = render(<CeOferim lang="ro" />);
    const panels = container.querySelector("[data-a]")!;
    const links = Array.from(panels.querySelectorAll("a"));
    expect(links).toHaveLength(CE_OFERIM.panels.length);
    links.forEach((a, i) => expect(a).toHaveAttribute("href", href("ro", CE_OFERIM.panels[i]!.page)));
    expect(panels).toHaveAttribute("data-a", "0");
    await userEvent.hover(links[3]!);
    expect(panels).toHaveAttribute("data-a", "3");
    expect(links[3]!).toHaveAttribute("data-active", "true");
    expect(links[0]!).toHaveAttribute("data-active", "false");
    act(() => links[5]!.focus());
    expect(panels).toHaveAttribute("data-a", "5");
  });
});

describe("<FaqAcasa>", () => {
  it("renders every question as a <details> sharing one name, first open", () => {
    const { container } = render(<FaqAcasa lang="ro" />);
    const ds = Array.from(container.querySelectorAll("details"));
    expect(ds).toHaveLength(FAQ.items.length);
    expect(new Set(ds.map((d) => d.getAttribute("name"))).size).toBe(1);
    expect(ds[0]).toHaveAttribute("open");
    expect(ds[1]).not.toHaveAttribute("open");
    expect(screen.getByRole("link", { name: "atelier de grup" })).toHaveAttribute("href", href("ro", "ateliereDeGrup"));
    expect(screen.getByRole("link", { name: /Toate întrebările/ })).toHaveAttribute(
      "href",
      href("ro", "intrebariFrecvente"),
    );
  });
});
