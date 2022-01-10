<template>
  <LoginModal @on-reauthenticate="onReauthenticate" :show="showLoginModal" />
  <q-layout id="layout" view="lHh Lpr lFf">
    <Nav />
    <EditIndex />
    <q-page-container class="main-container">
      <router-view />
      <EditPanel />
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, ref } from "vue";

import { EditIndex, EditPanel, LoginModal, Nav } from "@/components";
import { provideEditing, provideTransport, provideWindowIndex } from "@/use";

export default defineComponent({
  name: "MainLayout",
  components: {
    EditIndex,
    EditPanel,
    LoginModal,
    Nav,
  },
  setup() {
    // Reauthentication modal reactivity.
    const showLoginModal = ref(false);
    const onReauthenticate = (value) => (showLoginModal.value = value);

    provideEditing();
    provideTransport();
    provideWindowIndex();

    return {
      onReauthenticate,
      showLoginModal,
    };
  },
});
</script>
