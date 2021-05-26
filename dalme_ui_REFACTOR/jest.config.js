module.exports = {
  injectGlobals: true,
  testEnvironment: "jsdom",
  moduleFileExtensions: ["js", "vue", "json", "node"],
  moduleNameMapper: {
    "@/(.*)$": "<rootDir>/src/$1",
  },
  setupFiles: ["./jest.setup.js"],
  transform: {
    "^.+\\.js$": "babel-jest",
    "^.+\\.vue$": "vue-jest",
  },
};
