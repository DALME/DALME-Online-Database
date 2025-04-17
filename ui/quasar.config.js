/* eslint-env node */

// Configuration for your app
// https://v2.quasar.dev/quasar-cli-vite/quasar-config-js

import { fileURLToPath } from "node:url";
import { configure } from "quasar/wrappers";

const getDevCSP = () => {
  const defaultSrc =
    "default-src 'self' data: ws://0.0.0.0:8000 https://dam.dalme.org https://ka-f.fontawesome.com/";
  const imgSrc =
    "img-src 'self' https://dam.dalme.org https://tile.openstreetmap.org https://*.basemaps.cartocdn.com https://server.arcgisonline.com";
  const scriptSrc =
    "script-src 'self' 'unsafe-eval' 'unsafe-inline' https://cdn.jsdelivr.net/ https://kit.fontawesome.com/ https://code.jquery.com/ https://cdnjs.cloudflare.com/ https://maxcdn.bootstrapcdn.com/ https://unpkg.com/";
  const styleSrc =
    "style-src 'self' https://fonts.googleapis.com https://stackpath.bootstrapcdn.com/ 'unsafe-inline'";
  const fontSrc = "font-src 'self' https://ka-f.fontawesome.com/ https://fonts.gstatic.com/";
  const frameSrc =
    "frame-src 'self' data: https://dam.dalme.org https://dalme-app-media.s3.amazonaws.com/ https://view.officeapps.live.com";
  return `${defaultSrc}; ${imgSrc}; ${scriptSrc}; ${styleSrc}; ${fontSrc}; ${frameSrc}`;
};

export default configure((ctx) => {
  return {
    // https://v2.quasar.dev/quasar-cli-vite/prefetch-feature
    // preFetch: true,

    // app boot file (/src/boot)
    // --> boot files are part of "main.js"
    // https://v2.quasar.dev/quasar-cli-vite/boot-files
    boot: ["axios", "markdown", "openLayers"],

    // https://v2.quasar.dev/quasar-cli-vite/quasar-config-js#css
    css: ["app.scss"],

    // https://github.com/quasarframework/quasar/tree/dev/extras
    extras: [
      // "ionicons-v4",
      // "mdi-v7",
      // "fontawesome-v6",
      // "eva-icons",
      // "themify",
      // "line-awesome",
      // "roboto-font-latin-ext", // this or either "roboto-font", NEVER both!
      "fontawesome-v6",
      "mdi-v7",
      "roboto-font", // optional, you are not bound to it
      "material-icons", // optional, you are not bound to it
      "material-icons-outlined",
    ],

    // Full list of options: https://v2.quasar.dev/quasar-cli-vite/quasar-config-js#build
    build: {
      target: {
        browser: ["es2022", "edge88", "firefox78", "chrome87", "safari14"],
        node: "node20",
      },

      vueRouterMode: "history", // available values: "hash", "history"
      // vueRouterBase,
      // vueDevtools,
      // vueOptionsAPI: false,

      // rebuildCache: true, // rebuilds Vite/linter/etc cache on startup

      publicPath: "/db",
      // analyze: true,
      // env: {},
      // rawDefine: {}
      // ignorePublicFolder: true,
      // minify: false,
      // polyfillModulePreload: true,
      // distDir

      extendViteConf(viteConf) {
        viteConf.build = {
          target: "es2022",
          ...viteConf.build,
        };
        viteConf.optimizeDeps.esbuildOptions = {
          target: "es2022",
          supported: { bigint: true },
          ...viteConf.optimizeDeps.esbuildOptions,
        };
        viteConf.resolve.alias = {
          "@": fileURLToPath(new URL("./src", import.meta.url)),
          ...viteConf.resolve.alias,
        };
        if (ctx.dev) {
          viteConf.server.headers = {
            "Content-Security-Policy": getDevCSP(),
            ...viteConf.server.headers,
          };
        }
      },
      // viteVuePluginOptions: {},

      // vitePlugins: [
      //   [ 'package-name', { ..options.. } ]
      // ]
    },

    // Full list of options: https://v2.quasar.dev/quasar-cli-vite/quasar-config-js#devServer
    devServer: {
      host: "0.0.0.0",
      port: 3000,
      hmr: {
        protocol: "ws",
        host: "0.0.0.0",
        port: 3000,
        clientPort: 8000,
        path: "hmr",
      },
    },

    // https://v2.quasar.dev/quasar-cli-vite/quasar-config-js#framework
    framework: {
      cssAddon: true,
      config: {},

      iconset: "fontawesome-v6", // Quasar icon set
      // lang: "en-US", // Quasar language pack

      // For special cases outside of where the auto-import strategy can have an impact
      // (like functional components as one of the examples),
      // you can manually specify Quasar components/directives to be available everywhere:
      //
      // components: [],
      // directives: [],

      // Quasar plugins
      plugins: ["AppFullscreen", "Dialog", "Loading", "LocalStorage", "Meta", "Notify"],
    },

    // animations: "all", // --- includes all animations
    // https://v2.quasar.dev/options/animations
    animations: [
      "fadeIn",
      "fadeOut",
      "slideInDown",
      "slideInLeft",
      "slideInRight",
      "slideInUp",
      "fadeInDown",
      "fadeInLeft",
      "fadeInRight",
      "fadeInUp",
      "fadeOutDown",
      "fadeOutLeft",
      "fadeOutRight",
      "fadeOutUp",
      "slideOutDown",
      "slideOutLeft",
      "slideOutRight",
      "slideOutUp",
    ],

    // https://v2.quasar.dev/quasar-cli-vite/quasar-config-js#sourcefiles
    // sourceFiles: {
    //   rootComponent: "src/App.vue",
    //   router: "src/router/index",
    //   store: "src/store/index",
    //   pwaRegisterServiceWorker: "src-pwa/register-service-worker",
    //   pwaServiceWorker: "src-pwa/custom-service-worker",
    //   pwaManifestFile: "src-pwa/manifest.json",
    //   electronMain: "src-electron/electron-main",
    //   electronPreload: "src-electron/electron-preload"
    //   bexManifestFile: "src-bex/manifest.json
    // },

    // https://v2.quasar.dev/quasar-cli-vite/developing-ssr/configuring-ssr
    ssr: {
      // ssrPwaHtmlFilename: 'offline.html', // do NOT use index.html as name!
      // will mess up SSR

      // extendSSRWebserverConf (esbuildConf) {},
      // extendPackageJson (json) {},

      pwa: false,

      // manualStoreHydration: true,
      // manualPostHydrationTrigger: true,

      prodPort: 3000, // The default port that the production server should use
      // (gets superseded if process.env.PORT is specified at runtime)

      middlewares: [
        "render", // keep this as last one
      ],
    },

    // https://v2.quasar.dev/quasar-cli-vite/developing-pwa/configuring-pwa
    pwa: {
      workboxMode: "generateSW", // or 'injectManifest'
      injectPwaMetaTags: true,
      swFilename: "sw.js",
      manifestFilename: "manifest.json",
      useCredentialsForManifestTag: false,
      // useFilenameHashes: true,
      // extendGenerateSWOptions (cfg) {}
      // extendInjectManifestOptions (cfg) {},
      // extendManifestJson (json) {}
      // extendPWACustomSWConf (esbuildConf) {}
    },

    // Full list of options: https://v2.quasar.dev/quasar-cli-vite/developing-cordova-apps/configuring-cordova
    cordova: {
      // noIosLegacyBuildFlag: true, // uncomment only if you know what you are doing
    },

    // Full list of options: https://v2.quasar.dev/quasar-cli-vite/developing-capacitor-apps/configuring-capacitor
    capacitor: {
      hideSplashscreen: true,
    },

    // Full list of options: https://v2.quasar.dev/quasar-cli-vite/developing-electron-apps/configuring-electron
    electron: {
      // extendElectronMainConf (esbuildConf) {},
      // extendElectronPreloadConf (esbuildConf) {},

      // extendPackageJson (json) {},

      // Electron preload scripts (if any) from /src-electron, WITHOUT file extension
      preloadScripts: ["electron-preload"],

      // specify the debugging port to use for the Electron app when running in development mode
      inspectPort: 5858,

      bundler: "packager", // "packager" or "builder"

      packager: {
        // https://github.com/electron-userland/electron-packager/blob/master/docs/api.md#options
        // OS X / Mac App Store
        // appBundleId: "",
        // appCategoryType: "",
        // osxSign: "",
        // protocol: "myapp://path",
        // Windows only
        // win32metadata: { ... }
      },

      builder: {
        // https://www.electron.build/configuration/configuration

        appId: "ui",
      },
    },

    // Full list of options: https://v2.quasar.dev/quasar-cli-vite/developing-browser-extensions/configuring-bex
    bex: {
      // extendBexScriptsConf (esbuildConf) {},
      // extendBexManifestJson (json) {},

      contentScripts: ["my-content-script"],
    },
  };
});
