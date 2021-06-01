<template>
  <LoginModal :show="showLoginModal" />
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
import { provideAPI } from "@/use";

export default defineComponent({
  name: "MainLayout",
  components: {
    LoginModal,
    Nav,
  },
  setup() {
    const showLoginModal = ref(false);
    const reauthenticate = (value) => (showLoginModal.value = value);
    provideAPI(reauthenticate);
    return { reauthenticate, showLoginModal };
  },
});
</script>
