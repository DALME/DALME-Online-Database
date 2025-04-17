module.exports = {
  root: true,

  parserOptions: {
    ecmaVersion: 2022, // Allows for the parsing of modern ECMAScript features
  },

  env: {
    node: true,
    browser: true,
    "vue/setup-compiler-macros": true,
  },

  extends: [
    "eslint:recommended",
    "plugin:vue/vue3-essential", // Priority A: Essential (Error Prevention)
    "prettier",
  ],

  plugins: ["vue", "prettier", "unused-imports"],

  globals: {
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
    quotes: ["error", "double", { "avoidEscape": true }],
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
};
