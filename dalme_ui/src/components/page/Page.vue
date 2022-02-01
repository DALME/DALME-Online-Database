<template>
  <q-page>
    <FormModal
      v-for="cuid in cuids"
      :key="cuid"
      :cuid="cuid"
      :x-pos="xPos"
      :y-pos="yPos"
    />
    <slot></slot>
  </q-page>
</template>

<script>
import { keys } from "ramda";
import { computed, defineComponent } from "vue";

import { FormModal } from "@/components";
import { useEditing } from "@/use";

const X_ORIGIN = window.innerWidth / 3;
const X_OFFSET = 20;
const Y_OFFSET = 25;

export default defineComponent({
  name: "Page",
  components: {
    FormModal,
  },
  setup() {
    const { forms } = useEditing();

    const cuids = computed(() => keys(forms.value));
    const xPos = computed(() => X_ORIGIN + cuids.value.length * X_OFFSET);
    const yPos = computed(() => cuids.value.length * Y_OFFSET);

    return {
      cuids,
      xPos,
      yPos,
    };
  },
});
</script>
