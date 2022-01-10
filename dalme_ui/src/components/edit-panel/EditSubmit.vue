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
import { defineComponent } from "vue";

import { useEditing } from "@/use";

export default defineComponent({
  name: "EditSubmit",
  emits: ["onSubmitEdit"],
  setup(_, context) {
    const { disabled, focusActor } = useEditing();

    const submitEdit = () => {
      context.emit("onSubmitEdit", { actor: focusActor });
    };

    return {
      disabled,
      submitEdit,
    };
  },
});
</script>
