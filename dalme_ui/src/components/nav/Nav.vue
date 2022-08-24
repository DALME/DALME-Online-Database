<template>
  <q-header elevated>
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
              clickable
              v-close-popup
              @click="go('https://kb.dalme.org/')"
            >
              <q-item-section class="col-auto q-mr-xs">
                <q-icon name="article" size="sm" />
              </q-item-section>
              <q-item-section>Knowledge Base</q-item-section>
            </q-item>

            <q-item clickable v-close-popup @click="search_help">
              <q-item-section class="col-auto q-mr-xs">
                <q-icon name="quiz" size="sm"></q-icon>
              </q-item-section>
              <q-item-section>Search Help</q-item-section>
            </q-item>

            <q-separator spaced></q-separator>

            <q-item clickable v-close-popup @click="report_issue">
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
          <div class="col q-px-md q-mt-md user-menu">
            <div class="row justify-center">
              <q-avatar size="50px" rounded>
                <img :src="avatar" />
              </q-avatar>
            </div>
            <div class="row justify-center">
              <div class="text-capitalize text-subtitle1 text-weight-bold">
                {{ fullName }}
              </div>
            </div>
            <div class="row justify-center">
              <div class="text-caption">{{ username }}</div>
            </div>
          </div>
          <q-list padding class="text-grey-9">
            <q-separator spaced />
            <q-item clickable v-close-popup>
              <q-item-section class="col-auto q-mr-xs">
                <q-icon name="portrait" size="sm" />
              </q-item-section>
              <q-item-section>Profile</q-item-section>
            </q-item>
            <q-item clickable v-close-popup>
              <q-item-section class="col-auto q-mr-xs">
                <q-icon name="manage_accounts" size="sm" />
              </q-item-section>
              <q-item-section>Preferences</q-item-section>
            </q-item>
            <q-item class="q-mt-auto">
              <q-item-section>
                <q-item-label class="q-pl-lg">
                  Tooltips
                  <span :class="showTips ? 'text-bold' : null">on</span>/<span
                    :class="!showTips ? 'text-bold' : null"
                    >off</span
                  >
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
            <q-item class="q-mt-auto">
              <q-item-section>
                <q-item-label class="q-pl-lg">
                  Collapse sidebar
                  <span :class="sidebarCollapsed ? 'text-bold' : null">on</span
                  >/<span :class="!sidebarCollapsed ? 'text-bold' : null"
                    >off</span
                  >
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
            <q-separator spaced />
            <q-item
              clickable
              v-close-popup
              @click="logout"
              :loading="submitting"
            >
              <q-item-section class="col-auto q-mr-xs">
                <q-icon name="exit_to_app" size="sm" />
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
    v-model="navOpen"
    :mini="sidebarCollapsed && miniSidebar"
    @mouseover="miniSidebar = false"
    @mouseout="miniSidebar = true"
    mini-to-overlay
    bordered
    class="bg-grey-1"
  >
    <q-list>
      <template v-for="(route, idx) in routes" :key="idx">
        <NavLink
          v-if="!route.children"
          v-bind="{ name: route.name, icon: route.props.icon }"
        />
        <q-expansion-item
          v-else
          expand-separator
          :icon="route.props.icon"
          :label="route.name"
        >
          <NavLink
            v-for="(child, idx) in route.children"
            v-bind="{ name: child.name, icon: child.props.icon }"
            class="bg-grey-3"
            :key="idx"
          />
        </q-expansion-item>
      </template>
    </q-list>
  </q-drawer>
</template>

<script>
import { useQuasar } from "quasar";
import { filter as rFilter, head } from "ramda";
import { defineComponent, ref, computed, inject } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { usePrefStore } from "@/stores/preferences";
import { storeToRefs } from "pinia";

import { Dialog, NavLink } from "@/components";
import { useTooltips } from "@/use";

export default defineComponent({
  name: "Nav",
  components: {
    NavLink,
  },
  setup() {
    const $q = useQuasar();
    const $router = useRouter();
    const $authStore = useAuthStore();
    const $prefStore = usePrefStore();
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
    const navOpen = ref(true);
    const submitting = ref(false);
    const isFullscreen = ref(false);
    const searchQuery = ref("");
    const routes = rFilter(
      (route) => route.nav,
      head($router.options.routes).children,
    );

    const prefSubscription = inject("prefSubscription");

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

    return {
      darkMode: $q.dark,
      logout,
      navOpen,
      sidebarCollapsed,
      miniSidebar,
      routes,
      showTips,
      submitting,
      isFullscreen,
      toggleFullscreen,
      searchQuery,
      fullName,
      username,
      avatar,
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
  min-width: 250px;
}
</style>
