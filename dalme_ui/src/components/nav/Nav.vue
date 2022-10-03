<template>
  <q-header class="bg-grey-1 no-shadow">
    <q-toolbar class="q-px-lg q-py-sm">
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
        <q-avatar v-if="!isEmpty(avatar) && !isNil(avatar)" size="24px">
          <img :src="avatar" />
        </q-avatar>
        <q-icon v-else name="account_circle" size="sm" />
        <q-icon name="arrow_drop_down" size="xs" style="margin-left: -3px" />
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
            <q-item
              :to="{ name: 'User', params: { username: username } }"
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
                params: { username: username, prefs: true },
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
    </q-toolbar>
    <q-toolbar dense class="q-px-content q-pt-sm bg-grey-1 text-grey-9">
      <q-icon :name="pageIcon" color="grey-7" size="sm" class="q-pt-xs" />
      <q-breadcrumbs
        separator-color="grey-9"
        gutter="xs"
        class="menu-breadcrumb q-ml-sm q-mr-auto text-indigo-6"
      >
        <template v-for="(route, idx) in breadcrumbs" :key="idx">
          <q-breadcrumbs-el
            v-if="idx < breadcrumbs.length - 1"
            :label="route"
            :to="{ name: route }"
          />
          <q-breadcrumbs-el v-else class="text-weight-bold" :label="route" />
        </template>
      </q-breadcrumbs>
      <q-item dense class="q-px-sm page-header-button q-mr-sm">
        <q-item-section class="text-caption text-weight-medium">
          Tooltips
        </q-item-section>
        <q-item-section class="items-end">
          <q-toggle
            dense
            checked-icon="visibility"
            unchecked-icon="visibility_off"
            color="green"
            v-model="showTips"
          />
        </q-item-section>
      </q-item>
      <q-btn
        flat
        dense
        size="12px"
        color="grey-7"
        :icon="isFullscreen ? 'fullscreen_exit' : 'fullscreen'"
        @click="toggleFullscreen"
        class="page-header-button"
      />
    </q-toolbar>
    <q-toolbar class="q-px-content bg-grey-1 text-grey-9 menu-bar">
      <template v-for="(route, idx) in navRoutes" :key="idx">
        <q-btn
          v-if="!route.children"
          dense
          flat
          no-caps
          no-wrap
          :class="
            navStore.currentSection === route.name
              ? 'text-grey-9 menu-button active'
              : 'text-grey-9 menu-button'
          "
          size="sm"
          :to="{ name: route.name }"
          :active="navStore.currentSection === route.name"
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
            navStore.currentSection === route.name
              ? 'text-grey-9 menu-button active'
              : 'text-grey-9 menu-button'
          "
          size="sm"
          :active="navStore.currentSection === route.name"
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
  </q-header>
</template>

<script>
import { openURL, useQuasar } from "quasar";
import { isEmpty, isNil } from "ramda";
import { computed, defineComponent, inject, provide, ref, watch } from "vue";
import { useAuthStore } from "@/stores/auth";
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
    const navStore = useNavStore();
    const { fullName, username, avatar } = storeToRefs($authStore);
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

    const breadcrumbs = computed(() => navStore.breadcrumb);
    const pageIcon = computed(() => navStore.currentPageIcon);

    provide("currentSubsection", currentSubsection);

    watch(
      () => navStore.currentSubsection,
      () => (currentSubsection.value = navStore.currentSubsection),
    );

    return {
      avatar,
      breadcrumbs,
      darkMode: $q.dark,
      logout,
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
      pageIcon,
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
