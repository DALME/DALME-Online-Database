<template>
  <LoginModal :show="showLoginModal" />
  <q-layout id="layout" view="lHh Lpr lFf">
    <Nav />
    <EditIndex />
    <q-page-container class="main-container">
      <router-view />
      <EditPanel v-if="isAdmin" />
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, ref } from "vue";

import { EditIndex, EditPanel, LoginModal, Nav } from "@/components";
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
    EditIndex,
    EditPanel,
    LoginModal,
    Nav,
  },
  setup() {
    const showLoginModal = ref(false);
    provideAPI(showLoginModal);

    provideEditing();
    provideTooltips();
    provideTransport();
    const permissions = providePermissions();
    const { isAdmin } = permissions;

    return {
      isAdmin,
      showLoginModal,
    };
  },
});
</script>
