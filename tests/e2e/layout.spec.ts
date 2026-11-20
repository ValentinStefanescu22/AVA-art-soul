import { expect, test } from "./pages";

// The parts every page shares: header, phone menu, footer, scroll reveal. Tested on the home page.

test.describe("desktop header", () => {
  test.skip(({ isMobile }) => isMobile, "desktop navigation");

  test("turns into the floating pill once you scroll", async ({ page }) => {
    await page.goto("/ro");
    const header = page.locator("header").first();
    await expect(header).toHaveAttribute("data-sc", "0");
    await page.mouse.wheel(0, 400);
    await expect(header).toHaveAttribute("data-sc", "1");
  });

  test("opens „Ce oferim” on hover and with the keyboard; Escape closes it", async ({ page }) => {
    await page.goto("/ro");
    const nav = page.getByRole("navigation", { name: "Meniu principal" });
    const service = nav.getByRole("link", { name: "Consiliere 1:1" });
    await expect(service).toBeHidden();
    await nav.getByRole("link", { name: /^Ce oferim/ }).hover();
    await expect(service).toBeVisible();

    await page.mouse.move(0, 600);
    await nav.getByRole("link", { name: /^Ce oferim/ }).focus();
    await page.keyboard.press("ArrowDown");
    await expect(nav.getByRole("link", { name: "Ateliere de grup" })).toBeFocused();
    await page.keyboard.press("Escape");
    await expect(nav.getByRole("link", { name: /^Ce oferim/ })).toBeFocused();
    await expect(service).toBeHidden();
  });
});

test.describe("phone menu", () => {
  test.skip(({ isMobile }) => !isMobile, "the burger only exists below 1020px");

  test("opens from the burger and closes with ✕, Escape or the backdrop", async ({ page }) => {
    await page.goto("/ro");
    const menu = page.getByRole("dialog", { name: "Meniu" });
    const burger = page.getByRole("button", { name: "Deschide meniul" });

    await burger.click();
    await expect(menu).toBeVisible();
    await page.getByRole("button", { name: "Închide meniul" }).click();
    await expect(menu).toBeHidden();

    await burger.click();
    await expect(menu).toBeVisible();
    await page.keyboard.press("Escape");
    await expect(menu).toBeHidden();
    await expect(burger).toBeFocused(); // focus comes back to where it was

    await burger.click();
    await page.mouse.click(10, 10); // the dimmed page above the sheet
    await expect(menu).toBeHidden();
  });

  test("lists the services under Ce oferim and navigates", async ({ page }) => {
    await page.goto("/ro");
    await page.getByRole("button", { name: "Deschide meniul" }).click();
    const menu = page.getByRole("dialog", { name: "Meniu" });
    await menu.getByText("Ce oferim").click();
    await expect(menu.getByRole("link", { name: "Pentru școli și copii" })).toBeVisible();
    await menu.getByRole("link", { name: "Contact" }).click();
    await expect(page).toHaveURL(/\/ro\/contact$/);
  });

  test("every tap target is at least 44px (CLAUDE.md)", async ({ page }) => {
    await page.goto("/ro");
    await page.getByRole("button", { name: "Deschide meniul" }).click();
    const small = await page.$$eval(
      "header a, header button, dialog a, dialog button, dialog summary",
      (els) =>
        els
          .filter((e) => (e as HTMLElement).offsetParent !== null && !e.hasAttribute("tabindex"))
          .map((e) => ({
            t: e.textContent?.trim() || e.getAttribute("aria-label"),
            h: e.getBoundingClientRect().height,
          }))
          .filter((x) => x.h < 43.5), // sub-pixel rounding
    );
    expect(small).toEqual([]);
  });
});

test("the skip link lets keyboard users jump past the menu", async ({ page, isMobile }) => {
  test.skip(isMobile, "keyboard");
  await page.goto("/ro");
  await page.keyboard.press("Tab");
  const skip = page.getByRole("link", { name: "Sari la conținut" });
  await expect(skip).toBeFocused();
  await expect(skip).toBeInViewport();
  await page.keyboard.press("Enter");
  await expect(page.locator("main")).toBeFocused();
});

test("footer blocks reveal when they reach the screen", async ({ page }) => {
  await page.goto("/ro");
  const card = page.locator("footer [data-reveal]").first();
  await card.scrollIntoViewIfNeeded();
  await expect(card).toHaveAttribute("data-reveal", "in");
  await expect(card).toHaveCSS("opacity", "1", { timeout: 3000 });
});

test("nothing is hidden for visitors who asked for less motion", async ({ browser }) => {
  const ctx = await browser.newContext({ reducedMotion: "reduce" });
  const page = await ctx.newPage();
  await page.goto("/ro");
  await page.waitForTimeout(500); // the reveal script runs right after hydration
  expect(await page.locator('[data-reveal="wait"]').count()).toBe(0);
  await ctx.close();
});

test("the newsletter explains what is wrong (launch checklist 12)", async ({ page }) => {
  await page.goto("/ro");
  const form = page.locator("footer form");
  await form.scrollIntoViewIfNeeded();
  await form.getByRole("button", { name: "Abonează-te" }).click();
  await expect(form.getByText("Scrie o adresă de email validă")).toBeVisible();
  await expect(form.getByLabel("Emailul tău")).toBeFocused();
});

test.describe("newsletter pop-up (Acasă)", () => {
  test("opens once, after scrolling 40% of the page, and closes with Escape", async ({ page }) => {
    await page.goto("/ro?popup");
    const popup = page.getByRole("dialog").filter({ hasText: "Rămâi aproape" });
    await expect(popup).toBeHidden();
    await page.evaluate(() => window.scrollTo(0, document.documentElement.scrollHeight * 0.45));
    await expect(popup).toBeVisible();
    await page.keyboard.press("Escape");
    await expect(popup).toBeHidden();
    await page.reload();
    await page.evaluate(() => window.scrollTo(0, document.documentElement.scrollHeight * 0.45));
    await page.waitForTimeout(500);
    await expect(popup).toBeHidden(); // never twice for the same visitor
  });
});
