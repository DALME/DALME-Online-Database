<template>
  <q-btn
    fab
    icon="save"
    :loading="submitting"
    :disable="!valid"
    :color="!valid ? 'grey' : mouseoverSubmit ? 'red' : 'green'"
    :text-color="!valid ? 'black' : 'white'"
    @click="handleSubmit"
    @mouseover="mouseoverSubmit = true"
    @mouseleave="mouseoverSubmit = false"
  >
    <template v-slot:loading>
      <q-spinner-facebook />
    </template>
  </q-btn>
</template>

<script>
import { computed, defineComponent } from "vue";
import { useActor } from "@xstate/vue";

import { useEditing } from "@/use";

export default defineComponent({
  name: "EditSubmit",
  setup() {
    const {
      focus,
      forms,
      mouseoverSubmit,
      submitting,
      machine: { send },
    } = useEditing();

    const valid = computed(() => {
      if (focus.value) {
        if (focus.value === "inline") return true;
        const { state } = useActor(forms.value[focus.value]);
        if (state.value.context.validated) return true;
      }
      return false;
    });

    const handleSubmit = () => {
      send("SAVE_FOCUS");
    };

    return {
      handleSubmit,
      mouseoverSubmit,
      submitting,
      valid,
    };
  },
});
</script>
