<template>
  <LoginModal />
  <q-layout id="layout" view="lHr lpR lFr" :class="{ 'login-background': showMap }">
    <template v-if="render">
      <NavBar />
      <EditPanel />
      <AppDrawer />
      <UserDrawer />
      <q-page-container>
        <router-view />
      </q-page-container>
    </template>
  </q-layout>
</template>

<script>
import { computed, defineComponent, provide, ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import { find, isNotNil, propEq } from "ramda";
import { EditPanel, LoginModal, NavBar, UserDrawer, AppDrawer } from "@/components";
import {
  provideAPI,
  provideEditing,
  provideEventHandling,
  provideTransport,
  provideStores,
} from "@/use";

export default defineComponent({
  name: "MainLayout",
  components: {
    EditPanel,
    LoginModal,
    NavBar,
    UserDrawer,
    AppDrawer,
  },
  setup() {
    const { initEventHandler } = provideEventHandling(); // eslint-disable-line
    const { auth, ui, userDrawerOpen, appDrawerOpen } = provideStores();
    const $route = useRoute();
    const userDrawerEl = ref(null);

    const render = computed(() => auth.authorized || auth.reauthenticate);
    const showMap = computed(() => auth.authenticate);

    const prefSubscription = (action) => {
      let unsubscribe = () => {};
      if (action === "subscribe") {
        unsubscribe = auth.$subscribe(
          (mutation) => {
            auth.updatePreferences($route.name, mutation);
          },
          { detached: true },
        );
      } else {
        unsubscribe();
      }
    };

    const outsideDrawerClick = (e) => {
      e.stopPropagation();
      const openDrawer = find(propEq(true, "value"))([userDrawerOpen, appDrawerOpen]);
      if (e.target.classList.contains("q-dialog__backdrop") && isNotNil(openDrawer)) {
        openDrawer.value = false;
      }
    };

    provideAPI();
    provideEditing();
    provideTransport();

    provide("prefSubscription", prefSubscription);
    provide("userDrawerEl", userDrawerEl);

    onMounted(() => {
      if ($route.query.logout) {
        prefSubscription();
        auth.logout();
      }

      if (auth.authorized) prefSubscription("subscribe");
      ui.resizeListener();

      document.addEventListener("click", outsideDrawerClick);
    });

    return {
      auth,
      render,
      showMap,
    };
  },
});
</script>

<style lang="scss">
.login-background {
  background-image: url(@/assets/map_bg.png);
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
