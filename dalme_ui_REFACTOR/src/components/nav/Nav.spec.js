/* global describe, expect, it  */
import ElementPlus from "element-plus";
import { mount } from "@vue/test-utils";
import VueMq from "vue3-mq";

import router from "@/router";
import { Nav } from "./Nav.vue";

describe("Nav.vue", () => {
  it("should render the correct routes in the menu.", async () => {
    router.push("/");
    await router.isReady();

    const wrapper = mount(Nav, {
      global: {
        plugins: [
          router,
          ElementPlus,
          [VueMq, { breakpoints: { sm: 600, md: 960, lg: 1280 } }],
        ],
      },
    });

    expect(wrapper.vm.$route).toBeInstanceOf(Object);
    expect(wrapper.html()).toBe("<div></div>");
  });
});
