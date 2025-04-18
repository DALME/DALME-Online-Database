<template>
  <q-page>
    <template v-for="(modal, cuid) in modals" :key="cuid">
      <FormModal v-if="modal.kind === 'form'" :cuid="cuid" :x-pos="xPos" :y-pos="yPos" />
      <PageModal v-else :cuid="cuid" :x-pos="xPos" :y-pos="yPos" />
    </template>
    <slot></slot>
  </q-page>
</template>

<script>
import { keys } from "ramda";
import { computed, defineComponent } from "vue";

import { FormModal, PageModal } from "@/components";
import { useEditing } from "@/use";

const X_ORIGIN = window.innerWidth / 3;
const X_OFFSET = 20;
const Y_OFFSET = 40;

export default defineComponent({
  name: "PageContainer",
  components: {
    PageModal,
    FormModal,
  },
  setup() {
    const { modals } = useEditing();

    const cuids = computed(() => keys(modals.value));
    const xPos = computed(() => X_ORIGIN + cuids.value.length * X_OFFSET);
    const yPos = computed(() => cuids.value.length * Y_OFFSET);

    return {
      modals,
      xPos,
      yPos,
    };
  },
});
</script>
