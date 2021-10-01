<template>
  <LoginModal @reauthenticate="onReauthenticate" :show="showLoginModal" />
  <q-layout view="lHh Lpr lFf">
    <Nav />
    <Transport v-if="tracked" />
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, provide, ref } from "vue";

import { LoginModal, Nav, Transport } from "@/components";
import { provideTransport } from "@/use";

export default defineComponent({
  name: "MainLayout",
  components: {
    LoginModal,
    Nav,
    Transport,
  },
  setup() {
    // Reauthentication modal reactivity.
    const showLoginModal = ref(false);
    const onReauthenticate = (value) => (showLoginModal.value = value);

    // CRUD history tracker reactivity.
    const tracked = ref(null);
    provide("tracked", tracked);
    provideTransport(tracked);

    return { onReauthenticate, showLoginModal, tracked };
  },
});
</script>
