// @vitest-environment jsdom
import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import CeOferimPage from "@/app/[lang]/ce-oferim/page";
import DespreNoiPage from "@/app/[lang]/despre-noi/page";
import { nextTab, ServiceTabs } from "@/components/ce-oferim/ServiceTabs";
import { CE_OFERIM } from "@/content/ro/ce-oferim";
import { DESPRE } from "@/content/ro/despre-noi";
import { href, PAGES, SERVICE_PAGES } from "@/lib/routes";

const params = Promise.resolve({ lang: "ro" });

describe("nextTab", () => {
  it("moves with the arrows, wrapping around, and jumps with Home / End", () => {
    expect(nextTab("ArrowRight", 0, 3)).toBe(1);
    expect(nextTab("ArrowRight", 2, 3)).toBe(0);
    expect(nextTab("ArrowLeft", 0, 3)).toBe(2);
    expect(nextTab("Home", 2, 3)).toBe(0);
    expect(nextTab("End", 0, 3)).toBe(2);
    expect(nextTab("Enter", 1, 3)).toBeNull();
  });
});

describe("<ServiceTabs>", () => {
  const tabs = CE_OFERIM.tabs;
  const panel = (i: number) => document.getElementById(`cf-p-${tabs[i]!.id}`)!;

  it("shows only the chosen panel and switches on click", async () => {
    render(<ServiceTabs lang="ro" label={CE_OFERIM.tabsLabel} tabs={tabs} />);
    expect(screen.getByRole("tab", { name: tabs[0]!.label })).toHaveAttribute("aria-selected", "true");
    expect(panel(0)).toBeVisible();
    expect(panel(1)).not.toBeVisible();
    await userEvent.click(screen.getByRole("tab", { name: tabs[1]!.label }));
    expect(screen.getByRole("tab", { name: tabs[1]!.label })).toHaveAttribute("aria-selected", "true");
    expect(panel(0)).not.toBeVisible();
    expect(panel(1)).toBeVisible();
  });

  it("follows the WAI-ARIA tabs pattern: one tab in the Tab order, arrows move between tabs", async () => {
    render(<ServiceTabs lang="ro" label={CE_OFERIM.tabsLabel} tabs={tabs} />);
    const all = screen.getAllByRole("tab");
    expect(all.map((t) => t.tabIndex)).toEqual([0, -1, -1]);
    await userEvent.tab();
    expect(all[0]).toHaveFocus();
    await userEvent.keyboard("{ArrowLeft}");
    expect(all[2]).toHaveFocus();
    expect(all[2]).toHaveAttribute("aria-selected", "true");
    expect(panel(2)).toBeVisible();
    // Tab leaves the tab list and goes into the panel's first link
    await userEvent.tab();
    expect(document.activeElement).toBe(within(panel(2)).getAllByRole("link")[0]);
  });

  it("links every service page exactly once", () => {
    render(<ServiceTabs lang="ro" label={CE_OFERIM.tabsLabel} tabs={tabs} />);
    const hrefs = tabs.flatMap((t) => t.cards.map((c) => href("ro", c.page))).sort();
    expect(hrefs).toEqual(SERVICE_PAGES.map((p) => href("ro", p)).sort());
    for (const h of hrefs) expect(document.querySelectorAll(`a[href="${h}"]`)).toHaveLength(1);
  });
});

describe("Ce oferim page", () => {
  it("has one h1 and keeps the missing „De ce” text as a visible placeholder", async () => {
    render(await CeOferimPage({ params }));
    expect(screen.getAllByRole("heading", { level: 1 })).toHaveLength(1);
    expect(screen.getByRole("heading", { level: 1, name: CE_OFERIM.title })).toBeInTheDocument();
    expect(screen.getByText(/^\[.*\]$/)).toBeVisible();
  });
});

describe("Despre noi page", () => {
  it("has one h1 (the name, read whole despite the letter animation) and every section", async () => {
    render(await DespreNoiPage());
    expect(screen.getAllByRole("heading", { level: 1 })).toHaveLength(1);
    expect(screen.getByRole("heading", { level: 1, name: DESPRE.hero.name })).toBeInTheDocument();
    expect(screen.getAllByRole("heading", { level: 3 })).toHaveLength(DESPRE.povestea.qa.length);
    for (const t of [DESPRE.povestea.title, DESPRE.formari.title, DESPRE.comunitate.title])
      expect(screen.getByRole("heading", { level: 2, name: t })).toBeInTheDocument();
    for (const p of DESPRE.comunitate.people) expect(screen.getByText(p.name)).toBeInTheDocument();
    expect(screen.getByRole("img", { name: DESPRE.hero.photoAlt })).toBeInTheDocument();
  });

  it("marks where the header turns light: on „Povestea”, whose top is still dark", async () => {
    const { container } = render(await DespreNoiPage());
    expect(container.querySelectorAll("[data-hx-dark]")).toHaveLength(1);
    expect(container.querySelector("[data-hx-dark]")).toHaveAttribute("id", "povestea");
  });
});

it("both pages are real routes, no longer placeholders", async () => {
  const { PENDING } = await import("@/app/[lang]/[...slug]/page");
  expect(PENDING).not.toContain("despreNoi");
  expect(PENDING).not.toContain("ceOferim");
  expect(PAGES.despreNoi.indexed && PAGES.ceOferim.indexed).toBe(true);
});
