import eslint from "@eslint/js";
import pluginVue from "eslint-plugin-vue";
import eslintPluginPrettierRecommended from "eslint-plugin-prettier/recommended";
import unusedImports from "eslint-plugin-unused-imports";
import process from "node:process";

export default [
  eslint.configs.recommended,
  ...pluginVue.configs["flat/essential"],
  {
    files: ["**/*.js", "**/*.vue"],
    ignores: [
      "/dist",
      "/src-capacitor",
      "/src-cordova",
      "/.quasar",
      "/node_modules",
      "eslint.config.mjs",
      "/quasar.config.*.temporary.compiled*",
    ],
    plugins: {
      "unused-imports": unusedImports,
    },
    languageOptions: {
      ecmaVersion: 2021, // Allows for the parsing of modern ECMAScript features
      globals: {
        "vue/setup-compiler-macros": true,
        ga: "readonly", // Google Analytics
        cordova: "readonly",
        __statics: "readonly",
        __QUASAR_SSR__: "readonly",
        __QUASAR_SSR_SERVER__: "readonly",
        __QUASAR_SSR_CLIENT__: "readonly",
        __QUASAR_SSR_PWA__: "readonly",
        process: "readonly",
        Capacitor: "readonly",
        chrome: "readonly",
      },
    },
    rules: {
      "no-debugger": process.env.NODE_ENV === "production" ? "error" : "off",
      "prefer-promise-reject-errors": "off",
      "linebreak-style": ["error", "unix"],
      "no-unused-vars": "off",
      "max-len": ["error", { code: 100, ignoreUrls: true }],
      "prettier/prettier": [
        "error",
        {
          semi: true,
          doubleQuote: true,
          tabWidth: 2,
          trailingComma: "all",
          printWidth: 100,
        },
      ],
      quotes: ["error", "double"],
      semi: ["error", "always"],
      "unused-imports/no-unused-imports": "error",
      "unused-imports/no-unused-vars": [
        "warn",
        {
          vars: "all",
          varsIgnorePattern: "^_",
          args: "after-used",
          argsIgnorePattern: "^_",
        },
      ],
      "vue/no-multiple-template-root": "off",
    },
  },
  eslintPluginPrettierRecommended,
];
