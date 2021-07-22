<template>
  <q-header elevated>
    <q-toolbar>
      <q-btn
        flat
        dense
        round
        icon="menu"
        aria-label="Menu"
        @click="toggleNav"
      />
      <q-toolbar-title class="dalme-logo"> DALME </q-toolbar-title>
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
          :content-inset-level="0.333"
          dense
        >
          <NavLink
            v-for="(child, idx) in route.children"
            v-bind="{ name: child.name, icon: child.props.icon }"
            style="font-size: 0.8rem"
            :key="idx"
          />
        </q-expansion-item>
      </template>
      <q-item class="logout">
        <q-btn
          color="primary"
          icon="exit_to_app"
          label="Logout"
          size="sm"
          @click="logout"
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
import { filter as rFilter, head } from "ramda";
import { defineComponent, ref } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";

import { NavLink } from "@/components";
import notifier from "@/notifier";

export default defineComponent({
  name: "Nav",
  components: {
    NavLink,
  },
  setup() {
    const $router = useRouter();
    const $store = useStore();

    const navOpen = ref(false);
    const submitting = ref(false);
    const toggleNav = () => (navOpen.value = !navOpen.value);
    const routes = rFilter(
      (route) => route.nav,
      head($router.options.routes).children,
    );

    const logout = () => {
      submitting.value = true;
      notifier.auth.logout();
      setTimeout(() => {
        $store.dispatch("auth/logout");
      }, 300);
    };

    return {
      logout,
      navOpen,
      routes,
      submitting,
      toggleNav,
    };
  },
});
</script>

<style scoped lang="scss">
.logout {
  margin-top: auto;
}
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
