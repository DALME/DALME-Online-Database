module.exports = {
  root: true,

  parserOptions: {
    parser: "@babel/eslint-parser",
    ecmaVersion: 2018,
    sourceType: "module",
    requireConfigFile: false,
  },

  env: {
    browser: true,
  },

  extends: ["eslint:recommended", "plugin:vue/vue3-essential", "prettier"],

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
    indent: "off", // eslint and prettier clash over indentation, e.g. switch statements
    "no-debugger": process.env.NODE_ENV === "production" ? "error" : "off",
    "prefer-promise-reject-errors": "off",
    "linebreak-style": ["error", "unix"],
    "no-unused-vars": "off",
    "max-len": ["error", {"code": 100, "ignoreUrls": true}],
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
};
