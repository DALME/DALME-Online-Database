<template>
  <q-btn
    fab
    icon="save"
    :disable="!valid"
    :color="valid ? (mouseoverSubmit ? 'red' : 'green') : 'grey'"
    :text-color="valid ? 'white' : 'black'"
    @click.stop="handleSubmit"
    @mouseover="mouseoverSubmit = true"
    @mouseleave="mouseoverSubmit = false"
  >
    <template v-slot:loading>
      <q-spinner-facebook />
    </template>
  </q-btn>
</template>

<script>
import { isNil } from "ramda";
import { defineComponent, ref } from "vue";

import { useEditing } from "@/use";

export default defineComponent({
  name: "EditSubmit",
  setup() {
    const {
      mouseoverSubmit,
      submitting,
      machine: { send, service },
    } = useEditing();

    const valid = ref(false);
    service.onTransition(({ context: { focus, forms } }) => {
      const canSubmit = (focus) => {
        if (isNil(focus)) return false;
        if (focus === "inline") return true;
        const actor = forms[focus];
        return actor.getSnapshot().context.validated;
      };
      valid.value = canSubmit(focus);
    });

    const handleSubmit = () => {
      // Button will always disabled if state is invalid, but just in case.
      if (valid.value) {
        send("SAVE_FOCUS");
      }
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
