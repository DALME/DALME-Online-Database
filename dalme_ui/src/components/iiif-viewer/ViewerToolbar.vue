<template>
  <q-toolbar dense class="text-primary">
    <q-btn flat round dense icon="menu" />
    <q-toolbar-title>{{ title }}</q-toolbar-title>
    <q-btn-group class="q-mr-sm">
      <q-btn dense icon="first_page" />
      <q-btn dense icon="navigate_before" />
      <q-btn dense icon="navigate_next" />
      <q-btn dense icon="last_page" />
    </q-btn-group>
    <q-btn dense size="md" label="Folios" icon="grid_view" class="q-mr-sm" />
    <q-btn dense label="Info" icon="info" class="q-mr-sm" />
    <q-btn dense icon="fullscreen" />
  </q-toolbar>
</template>

<script>
import {
  //computed,
  inject,
  defineComponent,
  onBeforeMount,
  // onBeforeUnmount,
  // onMounted,
  ref,
  watch,
} from "vue";

export default defineComponent({
  name: "ViewerToolbar",

  setup() {
    const folios = inject("folios");
    const { currentFolio } = inject("currentFolio");
    const title = ref("");

    watch(currentFolio, () => {
      title.value = `Folio ${folios.value[currentFolio.value].name}`;
    });

    onBeforeMount(() => {
      title.value = `Folio ${folios.value[currentFolio.value].name}`;
    });

    return {
      title,
    };
  },
});
</script>
