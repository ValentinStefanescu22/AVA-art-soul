// @vitest-environment jsdom
import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { Header } from "@/components/layout/Header";
import { CONTACT, LAYOUT_COPY, NAV, SERVICES } from "@/content/ro/layout";

let path = "/ro";
vi.mock("next/navigation", () => ({ usePathname: () => path }));

// jsdom has no <dialog> behaviour: give it the two methods the menu uses.
beforeAll(() => {
  HTMLDialogElement.prototype.showModal = function () {
    this.setAttribute("open", "");
  };
  HTMLDialogElement.prototype.close = function () {
    this.removeAttribute("open");
  };
});

const renderAt = (p: string) => {
  path = p;
  return render(<Header lang="ro" nav={NAV} services={SERVICES} copy={LAYOUT_COPY} instagram={CONTACT.instagram} />);
};

describe("<Header>", () => {
  it("marks the current page in the menu", () => {
    renderAt("/ro/contact");
    const nav = screen.getByRole("navigation", { name: LAYOUT_COPY.mainNav });
    expect(within(nav).getByRole("link", { name: "Contact" })).toHaveAttribute("aria-current", "page");
    expect(within(nav).getByRole("link", { name: "Acasă" })).not.toHaveAttribute("aria-current");
  });

  it("marks Ce oferim on a service page and offers the way back to it", () => {
    renderAt("/ro/ce-oferim/consiliere");
    const nav = screen.getByRole("navigation", { name: LAYOUT_COPY.mainNav });
    expect(within(nav).getByRole("link", { name: /^Ce oferim/ })).toHaveAttribute("aria-current", "page");
    const back = screen.getAllByRole("link", { name: LAYOUT_COPY.back }).find((a) => !nav.contains(a));
    expect(back).toHaveAttribute("href", "/ro/ce-oferim");
  });

  it("shows no back link outside the service pages", () => {
    renderAt("/ro/contact");
    const nav = screen.getByRole("navigation", { name: LAYOUT_COPY.mainNav });
    expect(screen.getAllByRole("link", { name: /Ce oferim/ }).every((a) => nav.contains(a))).toBe(true);
  });

  it("lists every service in the dropdown", () => {
    renderAt("/ro");
    for (const s of SERVICES) expect(screen.getAllByRole("link", { name: s.label }).length).toBeGreaterThan(0);
  });

  it("opens the phone menu from the burger and closes it with ✕", async () => {
    renderAt("/ro");
    const user = userEvent.setup();
    const dialog = document.querySelector("dialog")!;
    await user.click(screen.getByRole("button", { name: LAYOUT_COPY.openMenu }));
    expect(dialog).toHaveAttribute("open");
    await user.click(screen.getByRole("button", { name: LAYOUT_COPY.closeMenu }));
    expect(dialog).not.toHaveAttribute("open");
  });
});
