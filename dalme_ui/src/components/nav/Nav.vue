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
      <NavLink
        v-for="(route, idx) in routes"
        :key="idx"
        v-bind="{ name: route.name, icon: route.props.icon }"
      />
      <q-item class="logout">
        <q-btn
          color="primary"
          icon="exit_to_app"
          label="Logout"
          size="sm"
          @click="logout"
        />
      </q-item>
    </q-list>
  </q-drawer>
</template>

<script>
import { head } from "ramda";
import { defineComponent, ref } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";

import { NavLink } from "@/components";
import notifications from "@/notifications";

export default defineComponent({
  name: "Nav",
  components: {
    NavLink,
  },
  setup() {
    const $router = useRouter();
    const $store = useStore();

    const navOpen = ref(false);
    const toggleNav = () => (navOpen.value = !navOpen.value);
    const routes = head($router.options.routes).children;

    const logout = () => {
      notifications.auth.logout();
      setTimeout(() => {
        $store.dispatch("auth/logout");
      }, 300);
    };

    return {
      logout,
      navOpen,
      routes,
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
