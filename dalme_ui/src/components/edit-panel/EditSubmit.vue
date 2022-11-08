<template>
  <q-btn
    icon="save"
    size="11px"
    :disable="!valid"
    :color="valid ? (mouseoverSubmit ? 'red-10' : 'light-green-8') : 'none'"
    :text-color="valid ? (mouseoverSubmit ? 'red-2' : 'light-green-2') : 'none'"
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

    service.onTransition(({ context: { focus, modals } }) => {
      const canSubmit = (focus) => {
        if (isNil(focus)) return false;
        if (focus === "inline") return true;
        const { actor } = modals[focus];
        return actor.getSnapshot().context.validated || false;
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
