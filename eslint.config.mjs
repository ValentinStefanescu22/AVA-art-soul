import { defineConfig, globalIgnores } from "eslint/config";
import nextVitals from "eslint-config-next/core-web-vitals";
import nextTs from "eslint-config-next/typescript";

export default defineConfig([
  ...nextVitals,
  ...nextTs,
  // Playwright fixtures call a function named `use`, which the React hooks rule mistakes for a hook.
  { files: ["tests/e2e/**"], rules: { "react-hooks/rules-of-hooks": "off" } },
  // CommonJS config files (Lighthouse CI only reads .cjs) are allowed to use require().
  { files: ["**/*.cjs"], rules: { "@typescript-eslint/no-require-imports": "off" } },
  globalIgnores([
    ".next/**",
    "out/**",
    "public/_img/**",
    "src/generated/**",
    ".aidesigner/**",
    "playwright-report/**",
    "test-results/**",
    "next-env.d.ts",
    ".wrangler/**",
  ]),
]);
