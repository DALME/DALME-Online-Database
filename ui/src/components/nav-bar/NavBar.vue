<template>
  <q-header class="no-shadow">
    <div class="main-toolbar row flex-center q-px-lg q-py-xs">
      <q-btn
        icon="mdi-menu"
        class="tb-button q-mr-md"
        :class="{ 'edit-on': ongoingEdit }"
        @click="appDrawerOpen = !appDrawerOpen"
      >
        <ToolTip>Open App menu.</ToolTip>
      </q-btn>

      <q-icon :name="pageIcon" color="grey-4" size="26px" />

      <q-breadcrumbs
        separator-color="bc-colour"
        gutter="xs"
        class="menu-breadcrumb q-ml-md q-mr-auto"
      >
        <template v-for="(route, idx) in breadcrumbs" :key="idx">
          <q-breadcrumbs-el
            v-if="idx == breadcrumbs.length - 1"
            :label="route"
            class="text-grey-5 text-weight-bold"
          />
          <q-breadcrumbs-el v-else :label="route" :to="{ name: route }" class="text-grey-5" />
        </template>
      </q-breadcrumbs>

      <q-space />

      <div class="q-mr-xs dalme-logotype">
        <strong>DALME</strong><span class="dalme-logotype-db">DB</span>
      </div>

      <q-btn
        icon="mdi-magnify"
        icon-right="mdi-tab-search"
        label="Search..."
        no-caps
        class="tb-button q-mx-md tb-search-button"
      >
        <ToolTip>Search DALME.</ToolTip>
      </q-btn>

      <q-separator vertical dark class="q-mr-md" />

      <template v-for="(route, idx) in topRoutes" :key="idx">
        <q-btn-group
          v-if="route.path == 'tickets'"
          class="tb-button q-mr-sm"
          :class="ui.currentSection === route.children[0].name ? 'disabled' : ''"
        >
          <q-btn
            :to="{ name: route.children[0].name }"
            :icon="route.meta.icon"
            :disable="ui.currentSection === route.children[0].name"
          >
            <ToolTip>{{ route.label }}</ToolTip>
          </q-btn>
          <q-btn
            icon="mdi-plus"
            class="btn-dropdown-like"
            :disable="ui.currentSection === route.children[0].name"
          >
            <ToolTip>Create new issue ticket.</ToolTip>
          </q-btn>
        </q-btn-group>

        <q-btn-dropdown
          v-else-if="route.dropdown == true"
          :icon="route.meta.icon"
          class="tb-button q-mr-sm"
          menu-anchor="bottom right"
          menu-self="top right"
          :menu-offset="[0, 5]"
          content-class="popup-menu dark"
        >
          <q-list>
            <template v-for="(child, i) in route.children" :key="i">
              <q-item
                :to="{ name: child.name ? child.name : child.children[0].name }"
                dense
                clickable
                v-close-popup
                :disable="ui.currentSubsection === child.meta.navPath[1]"
              >
                <q-item-section class="col-auto q-mr-xs">
                  <q-icon :name="child.meta.icon" size="xs" />
                </q-item-section>
                <q-item-section>
                  {{ child.label ? child.label : child.children[0].label }}
                </q-item-section>
              </q-item>
              <q-separator v-if="child.separator" spaced />
            </template>
          </q-list>
        </q-btn-dropdown>

        <q-btn
          v-else
          :to="{ name: route.name ? route.name : route.children[0].name }"
          :icon="route.meta.icon"
          class="tb-button q-mr-sm"
          :disable="
            route.name
              ? ui.currentSection === route.name
              : ui.currentSection === route.children[0].name
          "
        >
          <ToolTip>{{ route.label }}</ToolTip>
        </q-btn>
      </template>

      <q-btn dense round class="q-pr-none" @click="userDrawerOpen = !userDrawerOpen">
        <q-avatar v-if="!nully(auth.user.avatar)" size="34px">
          <q-img :src="auth.user.avatar" fit="cover" ratio="1" />
        </q-avatar>
        <q-icon v-else name="mdi-account-circle" size="lg" color="blue-grey-5" />
      </q-btn>
    </div>

    <div class="menu-container row bg-grey-2 q-mb-md">
      <q-toolbar class="row text-grey-9 bg-grey-2 menu-bar">
        <q-btn
          v-for="(route, idx) in menuRoutes"
          :key="idx"
          no-wrap
          class="text-grey-9 menu-button"
          :class="
            route.name
              ? ui.currentSection === route.name
                ? 'active'
                : ''
              : ui.currentSection === route.children[0].name
                ? 'active'
                : ''
          "
          :to="{ name: route.name ? route.name : route.children[0].name }"
          :active="
            route.name
              ? ui.currentSection === route.name
              : ui.currentSection === route.children[0].name
          "
        >
          <q-icon :name="route.meta.icon" color="grey-7" size="19px" />
          <span :data-content="route.name" class="q-pl-sm text-menu">
            {{ route.name ? route.name : route.children[0].name }}
          </span>
        </q-btn>

        <q-space />

        <q-btn
          size="12px"
          :text-color="preferences.tooltipsOn.value ? 'green-7' : 'grey-7'"
          :icon="
            preferences.tooltipsOn.value
              ? 'mdi-tooltip-remove-outline'
              : 'mdi-tooltip-check-outline'
          "
          class="mc-button"
          :class="{ 'bg-green-1': preferences.tooltipsOn.value }"
          @click="preferences.tooltipsOn.value = !preferences.tooltipsOn.value"
        >
          <ToolTip>Tooltips</ToolTip>
        </q-btn>
        <q-btn
          size="13px"
          :text-color="isFullscreen ? 'indigo-7' : 'grey-7'"
          :icon="isFullscreen ? 'mdi-fullscreen-exit' : 'mdi-fullscreen'"
          class="mc-button"
          :class="{ 'bg-indigo-1': isFullscreen }"
          @click="toggleFullscreen"
        >
          <ToolTip>Full screen</ToolTip>
        </q-btn>
      </q-toolbar>
    </div>
  </q-header>
</template>

<script>
import { openURL, useQuasar } from "quasar";
import { isEmpty, isNil } from "ramda";
import { computed, defineComponent, provide, ref, watch } from "vue";
import { navRoutes } from "@/router";
import { ToolTip } from "@/components";
import { useStores } from "@/use";
import { nully } from "@/utils";

export default defineComponent({
  name: "NavBar",
  components: {
    ToolTip,
  },
  setup() {
    const $q = useQuasar();
    const {
      auth,
      globalLoading,
      isFullscreen,
      ui,
      userDrawerOpen,
      appDrawerOpen,
      preferences,
      pageIndexShow,
      inlineIndexShow,
      windowIndexShow,
    } = useStores();

    const submitting = ref(false);
    const searchQuery = ref("");
    const currentSubsection = ref(ui.currentSubsection);
    const ongoingEdit = computed(
      () => pageIndexShow.value || inlineIndexShow.value || windowIndexShow.value,
    );

    window.test = preferences;

    const openKB = () => {
      openURL("https://kb.dalme.org/", null, { target: "_blank" });
    };

    const toggleFullscreen = () => {
      if (!isFullscreen.value) {
        $q.fullscreen.request().then(() => {
          isFullscreen.value = true;
        });
      } else {
        $q.fullscreen.exit().then(() => {
          isFullscreen.value = false;
        });
      }
    };

    const breadcrumbs = computed(() => ui.breadcrumb);
    const pageIcon = computed(() => ui.currentPageIcon);

    provide("currentSubsection", currentSubsection);

    watch(
      () => ui.currentSubsection,
      () => (currentSubsection.value = ui.currentSubsection),
    );

    return {
      auth,
      breadcrumbs,
      darkMode: $q.dark,
      globalLoading,
      menuRoutes: navRoutes("menu"),
      topRoutes: navRoutes("top"),
      ui,
      preferences,
      submitting,
      isFullscreen,
      isNil,
      isEmpty,
      toggleFullscreen,
      searchQuery,
      pageIcon,
      openKB,
      userDrawerOpen,
      appDrawerOpen,
      nully,
      ongoingEdit,
    };
  },
});
</script>

<style lang="scss">
.main-toolbar {
  background-color: #2f333c;
  background-image: linear-gradient(180deg, #072034 10%, #1b1b1b);
  background-size: cover;
  height: 60px;
}
.main-toolbar .tb-button {
  border: 1px solid rgb(51, 67, 84);
  color: rgb(97, 115, 139);
  height: 32px;
  width: 32px;
  padding-left: 6px;
  padding-right: 6px;
  font-size: 11px;
}
.main-toolbar .tb-button:before {
  box-shadow: none;
}
.main-toolbar .tb-button .q-icon {
  font-size: 20px;
}
.main-toolbar .tb-button.q-btn-group {
  padding: 0;
}
.main-toolbar .tb-button:hover:not(.q-btn-group, .disabled),
.main-toolbar .tb-button.q-btn-group:not(.disabled) .q-btn:hover {
  border-color: rgb(87, 115, 144);
  color: rgb(132, 159, 195);
  background-color: #1d3446;
}
.main-toolbar .tb-button.q-btn-group:hover:not(.disabled) {
  border-color: rgb(87, 115, 144);
}
.main-toolbar .tb-button.q-btn-group.disabled,
.main-toolbar .tb-button.disabled:not(.q-btn-group) {
  box-shadow:
    inset -1px -1px 0px 1px rgb(87 111 128 / 15%),
    inset 1px 1px 0px 1px black;
  opacity: 1 !important;
  background: #13293a;
}
.main-toolbar .tb-button .q-focus-helper {
  opacity: 0 !important;
}
.main-toolbar .tb-button.q-btn-group,
.main-toolbar .tb-button.q-btn-dropdown {
  width: auto;
}
.main-toolbar .tb-button.q-btn-group .q-btn-dropdown__arrow,
.main-toolbar .tb-button.q-btn-dropdown .q-btn-dropdown__arrow {
  margin-left: 2px;
  width: 12px;
}
.main-toolbar .tb-button.q-btn-group .q-btn {
  padding: 0 6px;
  height: 30px;
  font-size: 11px;
}
.main-toolbar
  .tb-button.q-btn-dropdown--split
  .q-btn-dropdown__arrow-container:not(.q-btn--outline) {
  border-left: none;
  padding-left: 4px;
}
.main-toolbar
  .tb-button.q-btn-dropdown--split
  .q-btn-dropdown__arrow-container:not(.q-btn--outline):before {
  height: 20px;
  border-left: 1px solid #334354;
  margin-top: 5px;
}
.main-toolbar .tb-button.q-btn-group .q-btn.btn-dropdown-like {
  padding: 0 2px;
}
.main-toolbar .tb-button .btn-dropdown-like:before {
  height: 20px;
  border-left: 1px solid #334354;
  margin-top: 5px;
  z-index: 1;
}
.tb-search-button {
  padding-left: 10px;
  padding-right: 10px;
  width: 20% !important;
  align-items: baseline;
}
.tb-search-button span.block {
  font-size: 14px;
}
.tb-search-button .q-btn__content {
  width: 100%;
}
.tb-search-button .q-btn__content .q-icon.on-right {
  margin-left: auto;
  padding-left: 10px;
  border-left: 1px solid rgb(51, 67, 84);
}
.main-toolbar .q-separator {
  height: 26px;
  align-self: center;
  background: rgb(51, 67, 84);
}
.dalme-logotype {
  color: rgb(119, 142, 172);
  font-size: 16px;
}
.dalme-logotype-db {
  color: rgb(97, 115, 139);
  margin-left: 5px;
}
.text-bc-colour {
  color: rgb(87, 115, 144);
  margin-left: 8px;
  margin-right: 4px;
}
.breadcrumb-container {
  align-items: center;
}
.menu-breadcrumb {
  font-size: 16px;
  margin-left: 10px;
}
.menu-bar {
  padding: 0;
  gap: 8px;
  min-height: 40px;
}
.menu-button {
  position: relative;
  display: flex;
  padding: 0px 9px 0px 6px;
  font-size: 14px !important;
  font-weight: 500;
  line-height: 30px;
  text-align: center;
  white-space: nowrap;
  cursor: pointer;
  background-color: transparent;
  border: 0;
  border-radius: 6px;
  align-items: center;
  list-style: none !important;
  text-transform: none;
  min-height: 2em;
}
.menu-button::before {
  box-shadow: none;
}
.menu-button.active::after {
  position: absolute;
  right: 50%;
  bottom: calc(50% - 24px);
  width: 100%;
  height: 4px;
  content: "";
  background: #3f51b5;
  border-radius: 6px;
  transform: translate(50%, -50%);
}
.menu-button.active {
  font-weight: 700;
}
.menu-button [data-content]::before {
  display: block;
  height: 0;
  font-weight: 600;
  visibility: hidden;
  content: attr(data-content);
}
.menu-container {
  border-bottom: 1px solid rgb(209, 209, 209);
  padding-right: 24px;
  padding-left: 24px;
}
.q-header {
  background-color: white;
}
.user-menu {
  min-width: 200px;
}
.mc-button {
  border: 1px solid rgb(209, 209, 209);
  border-radius: 4px;
  height: 32px;
  width: 32px;
  z-index: 1;
  text-transform: none;
  min-height: 2em;
  padding: 0.285em;
}
.mc-button::before {
  box-shadow: none;
}
.main-toolbar .tb-button.edit-on {
  color: #745050;
  border-color: #543333;
  background-color: rgba(70, 29, 29, 0.29);
}
.main-toolbar .tb-button.edit-on:hover {
  border-color: rgb(125 71 71);
  color: rgb(195 132 132);
  background-color: #461d1d9c;
}
</style>
