<template>
  <LoginModal v-if="showLogin" />
  <q-layout
    id="layout"
    view="hHh Lpr lFr"
    :class="!reAuthenticate && showLogin ? 'login-background' : null"
  >
    <Nav v-if="reAuthenticate || !showLogin" />
    <EditIndex v-if="reAuthenticate || !showLogin" />
    <q-page-container v-if="reAuthenticate || !showLogin">
      <router-view />
      <EditPanel v-if="isAdmin" />
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, provide, ref, onMounted } from "vue";
import { useAuthStore } from "@/stores/auth";
import { usePrefStore } from "@/stores/preferences";
import { useRoute } from "vue-router";
import { storeToRefs } from "pinia";

import { EditPanel, LoginModal, Nav } from "@/components";
import {
  provideAPI,
  provideEditing,
  providePermissions,
  provideTooltips,
  provideTransport,
} from "@/use";

export default defineComponent({
  name: "MainLayout",
  components: {
    EditPanel,
    LoginModal,
    Nav,
  },
  setup() {
    const $authStore = useAuthStore();
    const $prefStore = usePrefStore();
    const $route = useRoute();
    const { reAuthenticate, hasCredentials } = storeToRefs($authStore);

    const showLogin = ref(!hasCredentials.value || reAuthenticate.value);
    const updateShowLogin = (val) => {
      showLogin.value = val;
    };

    const prefSubscription = (action) => {
      let unsubscribe = () => {};
      if (action === "subscribe") {
        unsubscribe = $prefStore.$subscribe(
          (mutation) => {
            $prefStore.updatePreferences(
              $authStore.userId,
              $route.name,
              mutation,
            );
          },
          { detached: true },
        );
      } else {
        unsubscribe();
      }
    };

    provideAPI();
    provideEditing();
    provideTooltips();
    provideTransport();
    const permissions = providePermissions();
    const { isAdmin } = permissions;

    provide("showLogin", { showLogin, updateShowLogin });
    provide("reAuthenticate", reAuthenticate);
    provide("prefSubscription", prefSubscription);

    onMounted(() => {
      if ($route.query.logout) {
        prefSubscription();
        $authStore.logout();
      }

      if (!showLogin.value) {
        prefSubscription("subscribe");
      }
    });

    return {
      isAdmin,
      showLogin,
      reAuthenticate,
    };
  },
});
</script>

<style lang="scss" scoped>
.login-background {
  background-image: url(/static/images/map_bg.png);
  background-color: #ddd5c3;
  background-repeat: no-repeat;
  background-position: center;
  background-size: cover;
  background-attachment: fixed;
  height: 100vh;
  min-height: 100vh;
  width: 100%;
  padding: 0;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
