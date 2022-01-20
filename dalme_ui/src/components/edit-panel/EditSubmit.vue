<template>
  <q-btn
    fab
    icon="save"
    :loading="submitting"
    :disable="disabled"
    :color="disabled ? 'grey' : mouseoverSubmit ? 'red' : 'green'"
    :text-color="disabled ? 'black' : 'white'"
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
import { defineComponent } from "vue";

import { useEditing } from "@/use";

export default defineComponent({
  name: "EditSubmit",
  emits: ["onSubmitEdit"],
  setup() {
    const {
      disabled,
      focus,
      mouseoverSubmit,
      submitting,
      machine: { send },
    } = useEditing();

    const handleSubmit = () => {
      if (focus.value) {
        send("SAVE_FOCUS");
      }
    };

    return {
      disabled,
      handleSubmit,
      mouseoverSubmit,
      submitting,
    };
  },
});
</script>
