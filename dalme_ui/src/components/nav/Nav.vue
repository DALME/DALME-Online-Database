<template>
  <q-header class="no-shadow">
    <div class="main-toolbar row flex-center q-px-lg q-py-xs">
      <q-btn flat dense class="q-pl-xs">
        <q-avatar square color="white" size="34px">
          <img src="~assets/dalme_logo.svg" alt="DALME" />
        </q-avatar>
      </q-btn>
      <q-form class="q-mx-md">
        <q-input
          dark
          dense
          standout
          hide-bottom-space
          v-model="searchQuery"
          debounce="300"
          autocomplete="off"
          autocorrect="off"
          autocapitalize="off"
          spellcheck="false"
          placeholder="Search..."
          class="menu-search"
        >
          <template v-slot:append>
            <q-icon
              v-if="searchQuery === ''"
              name="search"
              size="18px"
              color="blue-grey-5"
            />
            <q-icon
              v-else
              name="highlight_off"
              class="cursor-pointer"
              size="18px"
              color="blue-grey-5"
              @click="searchQuery = ''"
            />
          </template>
        </q-input>
      </q-form>
      <q-space />
      <div style="font-size: 21px" class="q-mr-md text-blue-grey-3">
        <strong>DALME</strong> DB
      </div>
      <q-btn flat dense color="blue-grey-2" class="q-mr-sm q-pr-none">
        <q-icon name="help_outline" size="sm" />
        <q-icon name="arrow_drop_down" size="xs" style="margin-left: -3px" />
        <q-menu anchor="bottom right" self="top right">
          <q-list padding class="text-grey-9">
            <q-item
              dense
              clickable
              v-close-popup
              @click="openKB"
              class="q-pr-lg"
            >
              <q-item-section class="col-auto q-mr-xs">
                <q-icon name="article" size="sm" />
              </q-item-section>
              <q-item-section>Knowledge Base</q-item-section>
            </q-item>

            <q-item dense clickable v-close-popup @click="search_help">
              <q-item-section class="col-auto q-mr-xs">
                <q-icon name="quiz" size="sm"></q-icon>
              </q-item-section>
              <q-item-section>Search Help</q-item-section>
            </q-item>

            <q-separator spaced></q-separator>

            <q-item dense clickable v-close-popup @click="report_issue">
              <q-item-section class="col-auto q-mr-xs">
                <q-icon name="bug_report" size="sm"></q-icon>
              </q-item-section>
              <q-item-section>Report Issue</q-item-section>
            </q-item>
          </q-list>
        </q-menu>
      </q-btn>

      <q-btn flat dense color="blue-grey-2" size="12px" class="q-pr-none">
        <q-avatar
          v-if="!isEmpty(auth.avatar) && !isNil(auth.avatar)"
          size="24px"
        >
          <img :src="auth.avatar" />
        </q-avatar>
        <q-icon v-else name="account_circle" size="sm" />
        <q-icon name="arrow_drop_down" size="xs" style="margin-left: -3px" />
        <q-menu fit anchor="bottom right" self="top right">
          <div class="col q-px-md q-mt-md q-mb-sm user-menu">
            <div class="row q-mb-sm justify-center">
              <q-avatar
                v-if="!isEmpty(auth.avatar) && !isNil(auth.avatar)"
                size="50px"
              >
                <img :src="auth.avatar" />
              </q-avatar>
              <q-avatar v-else size="50px" icon="account_circle" />
            </div>
            <div class="row justify-center">
              <q-item-label class="text-subtitle2 text-weight-bold">
                {{ auth.fullName }}
              </q-item-label>
            </div>
            <div class="row justify-center">
              <q-item-label caption>{{ auth.username }}</q-item-label>
            </div>
          </div>
          <q-list padding class="text-grey-9 q-pt-none">
            <q-separator spaced />
            <q-item
              :to="{ name: 'User', params: { username: auth.username } }"
              dense
              clickable
              v-close-popup
            >
              <q-item-section class="col-auto q-mr-xs">
                <q-icon name="portrait" size="sm" />
              </q-item-section>
              <q-item-section>Profile</q-item-section>
            </q-item>
            <q-item
              :to="{
                name: 'User',
                params: { username: auth.username, prefs: true },
              }"
              dense
              clickable
              v-close-popup
            >
              <q-item-section class="col-auto q-mr-xs">
                <q-icon name="manage_accounts" size="sm" />
              </q-item-section>
              <q-item-section>Preferences</q-item-section>
            </q-item>
            <q-separator class="q-mb-sm" />
            <q-item
              dense
              clickable
              v-close-popup
              @click="logout"
              :loading="submitting"
            >
              <q-item-section class="col-auto q-mr-xs">
                <q-icon name="logout" size="sm" />
                <template v-slot:loading>
                  <q-spinner-facebook />
                </template>
              </q-item-section>
              <q-item-section>Log out</q-item-section>
            </q-item>
          </q-list>
        </q-menu>
      </q-btn>
    </div>
    <div class="menu-container row bg-grey-2 q-mb-md">
      <div class="q-pl-content col-grow">
        <transition name="collapse">
          <div v-if="!compactMode" class="title-bar row q-pt-none text-grey-9">
            <q-icon :name="pageIcon" color="grey-7" size="sm" class="pg-icn" />
            <q-breadcrumbs
              separator-color="grey-9"
              gutter="xs"
              class="menu-breadcrumb q-ml-xs q-mr-auto text-indigo-6"
            >
              <template v-for="(route, idx) in breadcrumbs" :key="idx">
                <q-breadcrumbs-el
                  v-if="idx < breadcrumbs.length - 1"
                  :label="route"
                  :to="{ name: route }"
                />
                <q-breadcrumbs-el
                  v-else
                  class="text-weight-bold"
                  :label="route"
                />
              </template>
              <q-spinner-facebook v-if="globalLoading" size="sm" />
            </q-breadcrumbs>
          </div>
        </transition>
        <q-toolbar class="row text-grey-9 bg-grey-2 menu-bar">
          <template v-for="(route, idx) in navRoutes" :key="idx">
            <q-btn
              v-if="!route.children"
              dense
              flat
              no-caps
              no-wrap
              :class="
                nav.currentSection === route.name
                  ? 'text-grey-9 menu-button active'
                  : 'text-grey-9 menu-button'
              "
              size="sm"
              :to="{ name: route.name }"
              :active="nav.currentSection === route.name"
            >
              <q-icon :name="route.meta.icon" color="grey-7" size="19px" />
              <span :data-content="route.name" class="q-pl-sm text-menu">
                {{ route.name }}
              </span>
            </q-btn>

            <q-btn
              v-else
              dense
              flat
              no-caps
              no-wrap
              :class="
                nav.currentSection === route.name
                  ? 'text-grey-9 menu-button active'
                  : 'text-grey-9 menu-button'
              "
              size="sm"
              :active="nav.currentSection === route.name"
            >
              <q-icon :name="route.meta.icon" color="grey-7" size="19px" />
              <span :data-content="route.name" class="q-pl-sm text-menu">
                {{ route.name }}
              </span>
              <q-menu
                class="menu-shadow"
                transition-show="scale"
                transition-hide="scale"
              >
                <q-list dense bordered style="min-width: 100px">
                  <NavLink
                    v-for="(child, idx) in route.children"
                    v-bind="{ to: child.name, icon: child.meta.icon }"
                    :key="idx"
                  />
                </q-list>
              </q-menu>
            </q-btn>
          </template>
        </q-toolbar>
      </div>
      <div class="q-pr-content col-auto">
        <div class="row flex-center title-bar-end">
          <q-btn
            flat
            dense
            size="12px"
            :color="showTips ? 'green-7' : 'grey-7'"
            class="page-header-button q-mr-sm"
            :class="{ 'bg-green-1': showTips }"
            @click="showTips = !showTips"
          >
            <q-icon
              :name="showTips ? 'o_speaker_notes_off' : 'o_speaker_notes'"
              size="16px"
            />
            <Tooltip>Tooltips</Tooltip>
          </q-btn>
          <q-btn
            flat
            dense
            size="12px"
            :color="compactMode ? 'indigo-7' : 'grey-7'"
            :icon="compactMode ? 'present_to_all' : 'present_to_all'"
            class="page-header-button q-mr-sm"
            :class="{ 'rotate-180': compactMode, 'bg-indigo-1': compactMode }"
            :disable="compactModeDisable"
            @click="compactMode = !compactMode"
          >
            <Tooltip>Compact mode</Tooltip>
          </q-btn>
          <q-btn
            flat
            dense
            size="12px"
            :color="isFullscreen ? 'indigo-7' : 'grey-7'"
            :icon="isFullscreen ? 'fullscreen_exit' : 'fullscreen'"
            class="page-header-button"
            :class="{ 'bg-indigo-1': isFullscreen }"
            @click="toggleFullscreen"
          >
            <Tooltip>Full screen</Tooltip>
          </q-btn>
        </div>
      </div>
    </div>
    <div
      class="strip-approach"
      :style="stripApproachStyle"
      @mouseenter="editPanel.stripApproachHover = true"
      @mouseleave="editPanel.stripApproachHover = false"
    />
  </q-header>
</template>

<script>
import { openURL, useQuasar } from "quasar";
import { isEmpty, isNil } from "ramda";
import { computed, defineComponent, inject, provide, ref, watch } from "vue";
import { navRoutes } from "@/router";
import { Dialog, NavLink } from "@/components";
import { Tooltip } from "@/components/utils";
import { useStores, useTooltips } from "@/use";

export default defineComponent({
  name: "Nav",
  components: {
    NavLink,
    Tooltip,
  },
  setup() {
    const $q = useQuasar();
    const {
      auth,
      compactMode,
      compactModeDisable,
      globalLoading,
      isFullscreen,
      nav,
      editPanel,
    } = useStores();

    const { showTips } = useTooltips();
    const submitting = ref(false);
    const searchQuery = ref("");
    const currentSubsection = ref(nav.currentSubsection);
    const prefSubscription = inject("prefSubscription");

    const stripApproachStyle = computed(() =>
      compactMode.value ? "top: 55px" : "top: 95px",
    );

    const openKB = () => {
      openURL("https://kb.dalme.org/", null, { target: "_blank" });
    };

    const logout = () => {
      $q.dialog({
        component: Dialog,
        componentProps: {
          isPersistent: true,
          title: "Log out",
          closeIcon: false,
          message: "Do you want to end your current session?",
          icon: "exit_to_app",
          okayButtonLabel: "Log out",
        },
      }).onOk(() => {
        prefSubscription();
        auth.logout();
      });
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

    const breadcrumbs = computed(() => nav.breadcrumb);
    const pageIcon = computed(() => nav.currentPageIcon);

    provide("currentSubsection", currentSubsection);

    watch(
      () => nav.currentSubsection,
      () => (currentSubsection.value = nav.currentSubsection),
    );

    return {
      auth,
      breadcrumbs,
      compactMode,
      compactModeDisable,
      editPanel,
      darkMode: $q.dark,
      logout,
      globalLoading,
      navRoutes,
      nav,
      showTips,
      submitting,
      isFullscreen,
      isNil,
      isEmpty,
      toggleFullscreen,
      searchQuery,
      stripApproachStyle,
      pageIcon,
      openKB,
    };
  },
});
</script>

<style lang="scss">
.q-header {
  background-color: white;
}
.main-toolbar {
  background-color: #2f333c;
  background-image: linear-gradient(180deg, #072034 10%, #1b1b1b);
  background-size: cover;
}
.user-menu {
  min-width: 200px;
}
.menu-container {
  border-bottom: 1px solid rgb(209, 209, 209);
}
.menu-breadcrumb {
  font-size: 20px;
}
.menu-bar {
  padding: 0;
  gap: 8px;
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
}
.menu-button::before {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  height: 100%;
  min-height: 48px;
  content: "";
  transform: translateX(-50%) translateY(-50%);
}
.menu-button.active::after {
  position: absolute;
  right: 50%;
  bottom: calc(50% - 27px);
  width: 100%;
  height: 2px;
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
.menu-search .q-field__control {
  height: 30px;
  border: 1px solid rgb(87, 96, 106);
}
.menu-search .q-field__native,
.menu-search .q-field__marginal {
  height: 28px;
}
.menu-search .q-field__native::placeholder {
  color: rgb(226, 226, 226);
}
.menu-search.q-field--standout.q-field--dark.q-field--highlighted
  .q-field__native::placeholder {
  color: rgb(20, 20, 20);
}
.menu-search.q-field--standout.q-field--dark .q-field__control {
  background: rgba(255, 255, 255, 0.01);
}
.menu-search.q-field--standout.q-field--dark.q-field--highlighted
  .q-field__control {
  background: rgb(255, 255, 255);
}
.page-header-button {
  border: 1px solid rgb(209, 209, 209);
  border-radius: 4px;
  height: 32px;
  width: 32px;
  z-index: 1;
}
.title-bar {
  height: 45px;
  min-height: 0px;
  align-items: flex-end;
}
.title-bar-end {
  height: 45px;
  align-items: flex-end;
  padding-bottom: 3px;
}
.pg-icn {
  padding-bottom: 2px;
}
.strip-approach {
  position: absolute;
  right: 0;
  top: 95px;
  width: 80px;
  height: 65px;
}
</style>
