<template>
  <LoginModal v-if="showLogin" />
  <q-layout
    id="layout"
    view="hHr Lpr lFr"
    :class="!reAuthenticate && showLogin ? 'login-background' : null"
  >
    <Nav v-if="reAuthenticate || !showLogin" />
    <EditPanel v-if="reAuthenticate || !showLogin" />
    <q-page-container v-if="reAuthenticate || !showLogin">
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, provide, ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import { EditPanel, LoginModal, Nav } from "@/components";
import {
  provideAPI,
  provideEditing,
  provideEventHandling,
  provideTooltips,
  provideTransport,
  provideStores,
} from "@/use";

export default defineComponent({
  name: "MainLayout",
  components: {
    EditPanel,
    LoginModal,
    Nav,
  },
  setup() {
    const { initEventHandler } = provideEventHandling();
    const { auth, prefs, ui, hasCredentials, reAuthenticate } = provideStores();
    const $route = useRoute();
    const showLogin = ref(!hasCredentials.value || reAuthenticate.value);
    const updateShowLogin = (val) => (showLogin.value = val);

    const prefSubscription = (action) => {
      let unsubscribe = () => {};
      if (action === "subscribe") {
        unsubscribe = prefs.$subscribe(
          (mutation) => {
            prefs.updatePreferences(auth.userId, $route.name, mutation);
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

    provide("showLogin", { showLogin, updateShowLogin });
    provide("prefSubscription", prefSubscription);

    onMounted(() => {
      // initEventHandler();

      if ($route.query.logout) {
        prefSubscription();
        auth.logout();
      }

      if (!showLogin.value) prefSubscription("subscribe");
      ui.resizeListener();
    });

    return {
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
