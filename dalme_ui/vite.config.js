import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  base: "/ui/",
  server: {
    hmr: {
      protocol: "wss",
      host: "127.0.0.1.xip.io",
      path: "hmr",
      port: "8000",
    },
  },
});
