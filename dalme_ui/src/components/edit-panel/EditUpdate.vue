<template>
  <q-btn
    fab
    icon="edit"
    text-color="black"
    :disable="disabled"
    :color="disabled ? 'grey' : 'amber'"
  />
</template>

<script>
import { computed, defineComponent, inject, toRefs } from "vue";

export default defineComponent({
  name: "EditUpdate",
  setup() {
    const editing = inject("editing");
    const { detail, locked, mode, submitting } = toRefs(editing);

    const disabled = computed(
      () =>
        locked.value ||
        !detail.value ||
        mode.value == "inline" || // Probably not needed here, but for clarity.
        submitting.value,
    );

    return {
      disabled,
    };
  },
});
</script>
