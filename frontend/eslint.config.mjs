import js from "@eslint/js";
import tseslint from "typescript-eslint";
import nextPlugin from "@next/eslint-plugin-next";

export default [
  js.configs.recommended,

  ...tseslint.configs.recommended,

  {
    plugins: {
      "@next/next": nextPlugin,
    },

    rules: {
      "@next/next/no-html-link-for-pages":
        "off",
    },
  },

  {
    ignores: [
        ".next/**",
        "node_modules/**",
        "dist/**",
        "out/**",
        "next-env.d.ts",
        "postcss.config.cjs",
        "tailwind.config.ts",
        "next.config.js",
    ],
  },
];
