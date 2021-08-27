<template>
  <LoginModal @reauthenticate="onReauthenticate" :show="showLoginModal" />
  <q-layout view="lHh Lpr lFf">
    <Nav />
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, ref } from "vue";

import { LoginModal, Nav } from "@/components";

export default defineComponent({
  name: "MainLayout",
  components: {
    LoginModal,
    Nav,
  },
  setup() {
    const showLoginModal = ref(false);
    const onReauthenticate = (value) => (showLoginModal.value = value);
    return { onReauthenticate, showLoginModal };
  },
});
</script>
