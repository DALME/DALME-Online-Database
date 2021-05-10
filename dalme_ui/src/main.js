import ElementPlus from "element-plus";
import "element-plus/lib/theme-chalk/index.css";
import { createApp } from "vue";
import VueMq from "vue3-mq";

import App from "@/App.vue";
import router from "@/router";
import store from "@/store";

const app = createApp(App);

app.use(router);
app.use(store);
app.use(ElementPlus);
app.use(VueMq, {
  breakpoints: {
    sm: 600,
    md: 960,
    lg: 1280,
  },
});
app.mount("#app");
