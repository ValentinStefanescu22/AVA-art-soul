import { expect, test } from "./pages";

// E3: Despre noi and Ce oferim, in a real browser (what jsdom can't check: layout, hydration, JS switched off).

test.describe("Ce oferim tabs", () => {
  test("switch with the keyboard, and the line glides under the chosen tab", async ({ page, problems }) => {
    await page.goto("/ro/ce-oferim");
    const tabs = page.getByRole("tablist", { name: "Pentru cine" }).getByRole("tab");
    await expect(tabs).toHaveCount(3);
    await tabs.first().focus();
    await page.keyboard.press("ArrowRight");
    await expect(tabs.nth(1)).toBeFocused();
    await expect(tabs.nth(1)).toHaveAttribute("aria-selected", "true");
    await expect(page.getByRole("tabpanel")).toHaveCount(1);
    await expect(page.getByRole("tabpanel").getByRole("link")).toHaveAttribute("href", "/ro/ce-oferim/pentru-companii");
    // the bar glides (0.6s) until it sits exactly under the chosen tab
    const tab = (await tabs.nth(1).boundingBox())!;
    const bar = page.locator("[role=tablist] > span");
    await expect
      .poll(async () => {
        const b = (await bar.boundingBox())!;
        return Math.abs(b.x - tab.x) + Math.abs(b.width - tab.width);
      })
      .toBeLessThan(1);
    expect(problems).toEqual([]);
  });

  test("without JavaScript every service is still there, one panel under the other", async ({ browser }) => {
    const ctx = await browser.newContext({ javaScriptEnabled: false });
    const page = await ctx.newPage();
    await page.goto("/ro/ce-oferim");
    await expect(page.getByRole("tabpanel")).toHaveCount(3);
    for (const p of ["ateliere-de-grup", "pentru-companii", "scoli-si-copii"])
      await expect(page.locator(`[role=tabpanel] a[href="/ro/ce-oferim/${p}"]`)).toBeVisible();
    await ctx.close();
  });
});

test("Despre noi: the header stays cream over the dark opening and turns ink once „Povestea” fades to paper", async ({
  page,
}) => {
  await page.goto("/ro/despre-noi");
  const header = page.locator("header").first();
  await expect(header).toHaveAttribute("data-tone", "dark");
  // „Povestea” turns paper 210px below its top; its title sits 320px below it. Title 100px from the top: light.
  await page.evaluate(() => scrollTo(0, document.getElementById("pv-h")!.getBoundingClientRect().top + scrollY - 100));
  await expect(header).toHaveAttribute("data-tone", "light");
});
