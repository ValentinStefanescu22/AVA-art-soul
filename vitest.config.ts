import react from "@vitejs/plugin-react";
import { fileURLToPath } from "node:url";
import { defineConfig } from "vitest/config";

export default defineConfig({
  plugins: [react()],
  resolve: { alias: { "@": fileURLToPath(new URL("./src", import.meta.url)) } },
  test: {
    globals: true,
    include: ["tests/unit/**/*.test.{ts,tsx}"],
    // Pure logic runs in Node; component tests opt into a browser-like DOM with `// @vitest-environment jsdom`.
    environment: "node",
    setupFiles: ["tests/unit/setup.ts"],
  },
});
