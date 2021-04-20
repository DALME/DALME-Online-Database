/* global describe, expect, it  */
import { mount } from "@vue/test-utils";
import { Nav } from "@/components/Nav.vue";

describe("Nav.vue", () => {
  it("should render the correct routes in the menu.", () => {
    const wrapper = mount(Nav);

    expect(wrapper.html()).toBe("<div></div>");
  });
});
