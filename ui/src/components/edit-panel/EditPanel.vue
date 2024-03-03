<template>
  <div
    class="edit-panel-strip"
    :class="{ 'edit-on': ongoingEdit }"
    :style="stripStyle"
    @mouseover="showStrip = true"
    @mouseleave="showStrip = false"
  >
    <TooltipWidget anchor="center left" self="center right" text="Editing tools" :offset="[5, 0]" />
    <q-icon name="more_vert" />
    <q-btn
      :icon="stripKeepOpen ? 'lock' : 'lock_open'"
      :class="stripKeepOpen ? 'on' : ''"
      square
      @click.stop="stripKeepOpen = !stripKeepOpen"
    />
    <div class="q-mini-drawer-hide strip-button-container">
      <EditCreate />
      <EditUpdate />
      <q-btn
        icon="edit_note"
        :class="{ 'edit-on': currentPageEditOn }"
        :disable="!showEditPageBtn"
        square
        @click="eventBus.emit('toggleEditor')"
      />
      <EditSubmit />
    </div>
    <q-btn
      :icon="drawerExpanded ? 'list_alt' : 'list_alt'"
      :class="drawerExpanded ? 'on' : ''"
      :disabled="!ongoingEdit"
      class="drawer-control"
      square
      @click.stop="drawerExpanded = !drawerExpanded"
    />
  </div>
  <transition name="collapse">
    <div v-show="drawerExpanded" class="edit-content-holder" :style="holderStyle">
      <WindowIndex />
      <PageIndex />
      <InlineIndex />
    </div>
  </transition>
</template>

<script>
import { computed, defineComponent, onMounted } from "vue";
import { useEditing, useEventHandling, useStores } from "@/use";
import { default as EditCreate } from "./EditCreate.vue";
import { default as EditSubmit } from "./EditSubmit.vue";
import { default as EditUpdate } from "./EditUpdate.vue";
import { default as PageIndex } from "./PageIndex.vue";
import { default as InlineIndex } from "./InlineIndex.vue";
import { default as WindowIndex } from "./WindowIndex.vue";
import { TooltipWidget } from "@/components";

export default defineComponent({
  name: "EditPanel",
  components: {
    EditCreate,
    EditSubmit,
    EditUpdate,
    PageIndex,
    InlineIndex,
    WindowIndex,
    TooltipWidget,
  },
  setup() {
    const {
      isAdmin,
      showEditPageBtn,
      currentPageEditOn,
      drawerExpanded,
      stripExpanded,
      stripKeepOpen,
      stripApproachHover,
      pageIndexShow,
      inlineIndexShow,
      windowIndexShow,
    } = useStores();
    const { eventBus } = useEventHandling();
    const { hideEditing, showEditing } = useEditing();

    const showStrip = computed({
      get: () => stripExpanded.value,
      set: (value) => {
        if (!stripKeepOpen.value) stripExpanded.value = value;
      },
    });

    const right = computed(() => (showStrip.value ? 0 : stripApproachHover.value ? -223 : -250));
    const stripStyle = computed(() => `top: 60px; right: ${right.value}px`);
    const holderStyle = computed(() => {
      let r = showStrip.value ? 0 : -250;
      return `top: 60px; right: ${r}px`;
    });

    const ongoingEdit = computed(
      () => pageIndexShow.value || inlineIndexShow.value || windowIndexShow.value,
    );

    const openEditing = () => (showStrip.value = true);
    const closeEditing = () => (showStrip.value = false);

    onMounted(() => {
      hideEditing.value = closeEditing;
      showEditing.value = openEditing;
    });

    return {
      showEditPageBtn,
      currentPageEditOn,
      drawerExpanded,
      isAdmin,
      holderStyle,
      showStrip,
      stripStyle,
      stripKeepOpen,
      eventBus,
      ongoingEdit,
    };
  },
});
</script>

<style lang="scss">
.edit-panel-strip {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  align-content: center;
  align-items: center;
  height: 41px;
  width: 263px;
  background-color: #ffca82;
  color: #a85e00;
  font-size: 18px;
  // border-radius: 3px 0 0 3px;
  border-left: 1px solid #b88f5c;
  border-bottom: 1px solid #b88f5c;
  // box-shadow: 1px 1px 0px 0px #ffffff7d inset, 0px -1px 0px 0px #5757573d inset,
  //   rgb(79 79 79 / 17%) 0px 0px 20px 6px;
  position: absolute;
  z-index: 5000;
  transition: all 0.5s ease-in-out;
}
.edit-panel-strip > i:first-of-type {
  align-self: center;
  width: 13px;
}
.edit-panel-strip > button,
.edit-panel-strip > a.q-btn {
  width: 27px;
  height: 27px;
  min-height: 20px;
  font-size: 8px;
  padding: 0 0 0 1px;
  border-style: solid;
  border-color: #c87001;
  background-color: #ffe1b8;
  color: #bb894a;
}
.edit-panel-strip > button:first-of-type {
  align-self: center;
  border-radius: 8px 0 0 8px;
  border-width: 1px 0 1px 1px;
  margin-right: -1px;
  box-shadow:
    1px 1px 0px 0px #5757573d inset,
    0px -1px 0px 0px #ffffff7d inset;
}
.edit-panel-strip > button.drawer-control {
  align-self: end;
  border-radius: 8px 8px 0 0;
  border-width: 0 0 1px 0;
  position: absolute;
  right: 98px;
  margin-bottom: -1px;
  box-shadow:
    1px 1px 0px 0px #5757573d inset,
    -1px -1px 0px 0px #ffffff7d inset,
    1px 0px 0px 0px #5757573d,
    -1px 0 0px 0px #ffffff7d;
}
.edit-panel-strip > button.on {
  background-color: #ffca82;
  color: #a85e00;
  box-shadow:
    1px 1px 0px 0px #ffffff7d inset,
    0px -1px 0px 0px #5757573d inset;
}
.edit-panel-strip > button.drawer-control.on {
  border-bottom: none;
  border-top: 1px solid #a55e002b;
  box-shadow:
    1px 1px 0px 0px #ffffff7d inset,
    -1px 0 0px 0px #5757573d inset,
    -1px 0 0px 0px #5757573d,
    1px 0px 0px 0px #ffffff7d;
}
.edit-panel-strip button::before,
.strip-button-container a.q-btn::before {
  box-shadow: none;
}
.edit-panel-strip button.disabled,
.edit-panel-strip button[disabled] {
  opacity: 1 !important;
}
.strip-button-container {
  display: flex;
  flex-direction: row;
  width: 222px;
  height: 35px;
  align-self: end;
  border-left: 1px solid #c87001;
  background-color: #ffdaa8;
}
.strip-button-container button,
.strip-button-container a.q-btn {
  display: flex;
  flex-grow: 1;
  min-height: 30px;
  border-radius: 0;
  padding: 0;
  color: #a85e00;
  background-color: #ffca82;
  width: 55px;
  box-shadow:
    1px 1px 0px 0px #ffffff4d inset,
    -1px -1px 0px 0px #5757573d inset;
}
.strip-button-container button:nth-of-type(1) {
  padding-right: 8px;
}
.strip-button-container button:nth-of-type(2) {
  padding-left: 8px;
}
.strip-button-container a.q-btn .q-fab__icon-holder {
  min-width: 20px;
  min-height: 20px;
  position: inherit;
}
.strip-button-container a.q-btn i {
  font-size: 20px;
}
.strip-button-container button.disabled {
  background-color: #ffe1b8 !important;
  color: #bb894a !important;
  box-shadow:
    1px 1px 0px 0px #5757571f inset,
    -1px -1px 0px 0px #ffffffe8 inset;
}
.edit-content-holder {
  margin-top: 37px;
  width: 223px;
  background-color: #ffffffd1;
  backdrop-filter: blur(5px) grayscale(70%);
  border-bottom: 1px solid #c87001;
  border-left: 1px solid #c87001;
  border-bottom-left-radius: 4px;
  z-index: 9999;
  position: absolute;
  right: 0;
  transition: all 0.5s ease-in-out;
  box-shadow: rgb(79 79 79 / 17%) -7px 10px 20px 0px;
}
.edit-content-holder .q-item:last-of-type {
  border-bottom-left-radius: 3px;
}
.edit-header {
  display: flex;
  height: 22px;
  border-top: 1px solid #c87001;
  border-bottom: 1px solid #c87001;
  border-left: 1px solid #c87001;
  border-top-left-radius: 4px;
  border-bottom-left-radius: 4px;
}
.edit-panel-strip button.orange {
  background-color: #ffca82;
  color: #a85e00;
}
.edit-panel-strip button.orange-on {
  background-color: #ffca82;
  color: #a85e00;
  box-shadow:
    1px 1px 0px 0px #ffffff7d inset,
    0px -1px 0px 0px #5757573d inset;
}
.edit-panel-strip button.orange-off {
  background-color: #ffe1b8;
  color: #bb894a;
  box-shadow:
    1px 1px 0px 0px #5757573d inset,
    0px -1px 0px 0px #ffffff7d inset;
}
.strip-button-container button.disabled.editing {
  background-color: #fdd3c7;
  color: #a74646;
  box-shadow:
    1px 1px 0px 0px #5757572b inset,
    0px -1px 0px 0px #fffefe9c inset;
}
.edit-on {
  background-color: #ffbfac;
  color: #a80000;
}
</style>
