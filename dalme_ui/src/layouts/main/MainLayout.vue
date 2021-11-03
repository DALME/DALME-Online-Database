<template>
  <LoginModal @reauthenticate="onReauthenticate" :show="showLoginModal" />
  <q-layout view="lHh Lpr lFf">
    <Nav />
    <Transport v-if="showTransport" />
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { computed, defineComponent, provide, ref } from "vue";
import { useManualRefHistory } from "@vueuse/core";

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

    // CRUD history transport reactivity.
    const tracked = ref({ id: null, field: null, new: null, old: null });
    const transport = useManualRefHistory(tracked, {
      clone: true,
    });
    provide("transport", transport);
    provideTransport(transport, tracked);
    const showTransport = computed(() =>
      transport.canUndo.value ? true : false,
    );

    return { onReauthenticate, showLoginModal, showTransport, transport };
  },
});
</script>
