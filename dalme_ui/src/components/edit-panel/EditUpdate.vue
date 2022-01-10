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
import { defineComponent } from "vue";

export default defineComponent({
  name: "EditUpdate",
  setup() {
    const disabled = true;

    return {
      disabled,
    };
  },
});
</script>
