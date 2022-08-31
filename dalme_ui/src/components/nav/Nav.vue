<template>
  <q-header class="shadow-6">
    <q-toolbar class="q-pl-sm q-pr-none">
      <q-btn flat dense class="q-pl-xs">
        <q-avatar square color="white" size="34px">
          <img src="~assets/dalme_logo.svg" alt="DALME" />
        </q-avatar>
      </q-btn>
      <q-toolbar-title><strong>DALME</strong> DB</q-toolbar-title>
      <q-form class="q-mx-xs">
        <q-input
          dark
          dense
          standout
          hide-bottom-space
          v-model="searchQuery"
          autocomplete="off"
          autocorrect="off"
          autocapitalize="off"
          spellcheck="false"
        >
          <template v-slot:append>
            <q-icon
              v-if="searchQuery === ''"
              name="search"
              color="blue-grey-7"
            />
            <q-icon
              v-else
              name="highlight_off"
              class="cursor-pointer"
              color="blue-grey-7"
              @click="searchQuery = ''"
            />
          </template>
        </q-input>
      </q-form>
      <q-separator dark vertical color="tbar-separator" />
      <q-btn
        flat
        stretch
        dense
        icon="live_help"
        padding="0 15px"
        color="blue-grey-3"
      >
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
      <q-separator dark vertical color="tbar-separator" />
      <q-btn
        flat
        stretch
        dense
        padding="0 15px"
        icon="account_circle"
        color="blue-grey-3"
      >
        <q-menu fit anchor="bottom right" self="top right">
          <div class="col q-px-md q-mt-md q-mb-sm user-menu">
            <div class="row q-mb-sm justify-center">
              <q-avatar v-if="!isEmpty(avatar) && !isNil(avatar)" size="50px">
                <img :src="avatar" />
              </q-avatar>
              <q-avatar v-else size="50px" icon="account_circle" />
            </div>
            <div class="row justify-center">
              <q-item-label class="text-subtitle2 text-weight-bold">
                {{ fullName }}
              </q-item-label>
            </div>
            <div class="row justify-center">
              <q-item-label caption>{{ username }}</q-item-label>
            </div>
          </div>
          <q-list padding class="text-grey-9 q-pt-none">
            <q-separator spaced />
            <q-item dense clickable v-close-popup>
              <q-item-section class="col-auto q-mr-xs">
                <q-icon name="portrait" size="sm" />
              </q-item-section>
              <q-item-section>Profile</q-item-section>
            </q-item>
            <q-item dense clickable v-close-popup>
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
      <q-separator dark vertical color="tbar-separator" />
      <q-btn
        flat
        stretch
        dense
        color="blue-grey-3"
        :icon="isFullscreen ? 'fullscreen_exit' : 'fullscreen'"
        padding="0 15px"
        @click="toggleFullscreen"
      />
    </q-toolbar>
  </q-header>
  <q-drawer
    :model-value="true"
    :mini="sidebarCollapsed && miniSidebar"
    @mouseover="miniSidebar = false"
    @mouseout="miniSidebar = true"
    :mini-to-overlay="sidebarCollapsed"
    bordered
    class="bg-grey-2 text-blue-grey-9 shadow-6"
    :width="220"
  >
    <q-list>
      <template v-for="(route, idx) in navRoutes" :key="idx">
        <NavLink
          v-if="!route.children"
          v-bind="{ to: route.name, icon: route.props.icon }"
        />
        <q-expansion-item
          :model-value="navStore.currentSection == route.name"
          v-else
          expand-separator
          :label="route.name"
          :class="navStore.currentSection === route.name ? 'mini-exp-open' : ''"
          :header-class="
            navStore.currentSection === route.name
              ? 'icon-adj text-light-blue-10 text-weight-bold'
              : 'icon-adj'
          "
        >
          <template v-slot:header>
            <q-item-section avatar>
              <q-icon :name="route.props.icon" size="20px" />
            </q-item-section>
            <q-item-section>{{ route.name }}</q-item-section>
          </template>
          <NavLink
            v-for="(child, idx) in route.children"
            v-bind="{ to: child.name, icon: child.props.icon }"
            :key="idx"
          />
        </q-expansion-item>
      </template>
      <q-space />
      <q-separator />
      <q-item class="bg-grey-4">
        <q-item-section avatar class="q-mini-drawer-only mini-prefs-icon">
          <q-icon name="settings" size="20px" color="grey-6" />
        </q-item-section>
        <q-item-section>
          <q-item dense class="q-pl-none q-pr-sm">
            <q-item-section>
              <q-item-label class="q-pl-sm text-caption">
                Show tooltips
              </q-item-label>
            </q-item-section>
            <q-item-section avatar>
              <q-toggle
                dense
                checked-icon="visibility"
                unchecked-icon="visibility_off"
                color="green"
                v-model="showTips"
              />
            </q-item-section>
          </q-item>
          <q-item dense class="q-pl-none q-pr-sm">
            <q-item-section>
              <q-item-label class="q-pl-sm text-caption">
                Compact sidebar
              </q-item-label>
            </q-item-section>
            <q-item-section avatar>
              <q-toggle
                dense
                checked-icon="visibility"
                unchecked-icon="visibility_off"
                color="green"
                v-model="sidebarCollapsed"
              />
            </q-item-section>
          </q-item>
        </q-item-section>
      </q-item>
    </q-list>
  </q-drawer>
</template>

<script>
import { openURL, useQuasar } from "quasar";
import { isEmpty, isNil } from "ramda";
import { computed, defineComponent, inject, provide, ref, watch } from "vue";
import { useAuthStore } from "@/stores/auth";
import { usePrefStore } from "@/stores/preferences";
import { useNavStore } from "@/stores/navigation";
import { storeToRefs } from "pinia";
import { navRoutes } from "@/router";

import { Dialog, NavLink } from "@/components";
import { useTooltips } from "@/use";

export default defineComponent({
  name: "Nav",
  components: {
    NavLink,
  },
  setup() {
    const $q = useQuasar();
    const $authStore = useAuthStore();
    const $prefStore = usePrefStore();
    const navStore = useNavStore();
    const { fullName, username, avatar } = storeToRefs($authStore);
    const { ui } = storeToRefs($prefStore);

    const sidebarCollapsed = computed({
      get() {
        return ui.value.sidebarCollapsed;
      },
      set(newValue) {
        ui.value.sidebarCollapsed = newValue;
      },
    });

    const miniSidebar = ref(sidebarCollapsed.value ? true : false);
    const { showTips } = useTooltips();
    const submitting = ref(false);
    const isFullscreen = ref(false);
    const searchQuery = ref("");
    const currentSubsection = ref(navStore.currentSubsection);

    const prefSubscription = inject("prefSubscription");

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
          OkayButtonLabel: "Log out",
          CancelButtonColour: "blue-grey-5",
        },
      }).onOk(() => {
        prefSubscription();
        $authStore.logout();
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

    provide("currentSubsection", currentSubsection);

    watch(
      () => navStore.currentSubsection,
      () => {
        console.log("changed", navStore.currentSubsection);
        currentSubsection.value = navStore.currentSubsection;
      },
    );

    return {
      darkMode: $q.dark,
      logout,
      sidebarCollapsed,
      miniSidebar,
      navRoutes,
      navStore,
      showTips,
      submitting,
      isFullscreen,
      isNil,
      isEmpty,
      toggleFullscreen,
      searchQuery,
      fullName,
      username,
      avatar,
      openKB,
    };
  },
});
</script>

<style scoped lang="scss">
.q-list {
  display: flex;
  flex-direction: column;
  height: 100%;
}
.q-toolbar {
  background-color: #2f333c;
  background-image: linear-gradient(78deg, #11587c 1%, #1b1b1b);
  background-size: cover;
}
.tbar-separator {
  background: rgb(87 112 125 / 49%);
}
.user-menu {
  min-width: 200px;
}
.q-expansion-item--expanded {
  background: #ffffff;
  color: #616161;
}
.q-list--separator > .q-item-type + .q-item-type {
  border-top: 1px dotted rgba(0, 0, 0, 0.12);
}
.mini-prefs-icon {
  height: 64px;
  padding: 8px 2px;
}
</style>
