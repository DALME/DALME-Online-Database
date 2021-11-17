<template>
  <LoginModal @reauthenticate="onReauthenticate" :show="showLoginModal" />
  <q-layout id="layout" view="lHh Lpr lFf">
    <Nav />
    <Transport v-if="showTransport" />
    <q-page-container class="main-container">
      <router-view />
      <EditPanel />
    </q-page-container>
  </q-layout>
</template>

<script>
import { computed, defineComponent, provide, reactive, ref } from "vue";
import { useManualRefHistory } from "@vueuse/core";

import { EditPanel, LoginModal, Nav, Transport } from "@/components";
import { provideEditing, provideTransport } from "@/use";

export default defineComponent({
  name: "MainLayout",
  components: {
    EditPanel,
    LoginModal,
    Nav,
    Transport,
  },
  setup() {
    // Reauthentication modal reactivity.
    const showLoginModal = ref(false);
    const onReauthenticate = (value) => (showLoginModal.value = value);

    // CRUD editor's panel reactivity.
    const editing = reactive({
      detail: false, // Are we on a object detail view.
      enableSave: true, // Override save disable manually.
      form: null, // The kind of form that needs to be rendered.
      locked: false, // Is CRUD happening at the moment.
      mode: null, // null (normal) || inline || form
      submitting: false, // CRUD is being submitted to the API.
    });
    provide("editing", editing);
    provideEditing(editing);

    // CRUD history transport reactivity.
    const tracked = ref({ id: null, field: null, new: null, old: null });
    const transport = useManualRefHistory(tracked, { clone: true });
    const showTransport = computed(() =>
      transport.canUndo.value ? true : false,
    );
    provide("transport", transport);
    provideTransport(transport, tracked);

    return { onReauthenticate, showLoginModal, showTransport, transport };
  },
});
</script>
