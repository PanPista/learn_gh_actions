import { expect, test } from "@playwright/test";

test("displays a country returned by the country endpoint", async ({ page }) => {
  await page.goto("/");

  await page.getByLabel("Two-letter country code").fill("US");
  await page.getByRole("button", { name: "Get country" }).click();

  await expect(page).toHaveURL(/code=US/);
  await expect(page.locator("form").first().locator("pre")).toContainText(
    "United States",
  );
});

test("displays countries returned by the list endpoint", async ({ page }) => {
  await page.goto("/");

  await page.getByLabel(/Number of countries/).fill("2");
  await page.getByRole("button", { name: "List countries" }).click();

  await expect(page).toHaveURL(/limit=2/);
  await expect(page.locator("form").nth(1).locator("pre")).toContainText(
    "Afghanistan",
  );
});
