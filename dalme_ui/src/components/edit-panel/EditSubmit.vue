<template>
  <q-btn
    fab
    icon="save"
    :disable="disabled"
    :color="disabled ? 'grey' : 'green'"
    :text-color="disabled ? 'black' : 'white'"
    @click="submitEdit"
  />
</template>

<script>
import { computed, defineComponent, inject, toRefs } from "vue";

export default defineComponent({
  name: "EditSubmit",
  setup(_, context) {
    const editing = inject("editing");
    const { enableSave, locked, submitting } = toRefs(editing);

    const disabled = computed(
      () => !locked.value || (submitting.value && !enableSave.value),
    );

    const submitEdit = () => {
      submitting.value = true;
      enableSave.value = false;
      context.emit("submitEdit");
    };

    return {
      disabled,
      submitEdit,
    };
  },
});
</script>
