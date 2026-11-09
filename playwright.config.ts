import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./e2e",
  reporter: [
    ["list"],
    ["html", { outputFolder: "playwright-report", open: "never" }],
  ],
  use: {
    baseURL: "http://127.0.0.1:8000",
    browserName: "chromium",
  },
  // webServer: {
  //   command: "PYTHONPATH=. python3 tests/playwright_server.py",
  //   url: "http://127.0.0.1:8000",
  //   reuseExistingServer: false,
  // },
});
