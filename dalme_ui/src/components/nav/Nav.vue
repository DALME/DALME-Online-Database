<template>
  <q-header elevated>
    <q-toolbar>
      <q-btn
        flat
        dense
        round
        icon="menu"
        aria-label="Menu"
        @click.stop="toggleNav"
      />
      <q-toolbar-title class="dalme-logo self-end"> DALME </q-toolbar-title>
    </q-toolbar>
  </q-header>

  <q-drawer v-model="navOpen" show-if-above bordered class="bg-grey-1">
    <q-list>
      <q-item-label header class="text-grey-8"> DALME </q-item-label>

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

      <q-item class="q-mt-auto">
        <q-toggle
          dense
          checked-icon="visibility"
          unchecked-icon="visibility_off"
          color="green"
          v-model="showTips"
        >
          <q-icon name="info" color="grey" size="sm" />
          <q-tooltip
            class="bg-blue z-max"
            anchor="center right"
            self="center left"
            :offset="[10, 10]"
          >
            {{ `Tooltips ${showTips ? "on" : "off"}` }}
          </q-tooltip>
        </q-toggle>
      </q-item>

      <q-item class="logout">
        <q-btn
          color="primary"
          icon="exit_to_app"
          label="Logout"
          size="sm"
          @click.stop="logout"
          :loading="submitting"
        >
          <template v-slot:loading>
            <q-spinner-facebook />
          </template>
        </q-btn>
      </q-item>
    </q-list>
  </q-drawer>
</template>

<script>
import { useQuasar } from "quasar";
import { filter as rFilter, head } from "ramda";
import { defineComponent, ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";

import { NavLink } from "@/components";
import { useNotifier, useTooltips } from "@/use";

export default defineComponent({
  name: "Nav",
  components: {
    NavLink,
  },
  setup() {
    const $q = useQuasar();
    const $router = useRouter();
    const $store = useAuthStore();
    const $notifier = useNotifier();
    const { showTips } = useTooltips();

    const navOpen = ref(false);
    const submitting = ref(false);
    const toggleNav = () => (navOpen.value = !navOpen.value);
    const routes = rFilter(
      (route) => route.nav,
      head($router.options.routes).children,
    );

    const logout = () => {
      submitting.value = true;
      $notifier.auth.logout();
      setTimeout(() => {
        $store.logout();
      }, 300);
    };

    return {
      darkMode: $q.dark,
      logout,
      navOpen,
      routes,
      showTips,
      submitting,
      toggleNav,
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
  background-image: linear-gradient(59deg, #11587c 54.62%, #1b1b1b);
  background-size: cover;
}
</style>
