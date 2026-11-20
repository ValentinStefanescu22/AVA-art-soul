import AxeBuilder from "@axe-core/playwright";
import { builtPages, expect, test } from "./pages";

// axe checks contrast, labels, landmarks, alt text, ARIA… on every page, on desktop and both phones.
for (const path of builtPages()) {
  test(`${path} has no accessibility violations`, async ({ page }) => {
    await page.goto(path);
    const { violations } = await new AxeBuilder({ page })
      .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa", "best-practice"])
      .analyze();
    expect(violations.map((v) => `${v.id}: ${v.help} (${v.nodes.length})`)).toEqual([]);
  });
}
