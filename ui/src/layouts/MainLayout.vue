<template>
  <LoginModal />
  <q-layout id="layout" view="lHr lpR lFr" :class="{ 'login-background': showMap }">
    <template v-if="render">
      <NavBar />
      <AppDrawer />
      <UserDrawer />
      <q-page-container>
        <router-view />
      </q-page-container>
    </template>
    <template v-else>
      <iframe
        id="login-background-page"
        ref="pageBackdrop"
        :class="{ 'q-transparent': !pageBackdropLoaded }"
        :src="originPage"
      >
      </iframe>
    </template>
  </q-layout>
</template>

<script>
import { computed, defineComponent, provide, ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import { find, isNotNil, propEq } from "ramda";
import { LoginModal, NavBar, UserDrawer, AppDrawer } from "@/components";
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
    const pageBackdrop = ref(null);

    // const render = computed(() => auth.authorized || auth.reauthenticate);
    const render = computed(() => auth.authorized && !auth.reauthenticate);
    const originPage = window.localStorage.getItem("origin_background");
    const showMap = computed(() => auth.authenticate && !originPage);
    const pageBackdropLoaded = ref(originPage ? false : true);

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
    provide("userDrawerEl", userDrawerEl);
    provide("pageBackdropLoaded", pageBackdropLoaded);

    onMounted(() => {
      console.log("auth.currentState main mounted", auth.authorized, auth.reauthenticate);
      if ($route.query.logout) {
        auth.logout();
      }

      ui.resizeListener();

      document.addEventListener("click", outsideDrawerClick);

      if (!render.value && originPage) {
        pageBackdrop.value.onload = () => {
          pageBackdropLoaded.value = true;
        };
      }
    });

    return {
      auth,
      render,
      showMap,
      originPage,
      pageBackdrop,
      pageBackdropLoaded,
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
#login-background-page {
  border: none;
  width: 100vw;
  height: 100vh;
}
</style>
