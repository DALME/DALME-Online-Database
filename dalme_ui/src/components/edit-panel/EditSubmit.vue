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
import { defineComponent } from "vue";

import { useEditing } from "@/use";

export default defineComponent({
  name: "EditSubmit",
  setup() {
    const {
      // focus,
      // forms,
      mouseoverSubmit,
      submitting,
      machine: { send },
    } = useEditing();

    // TODO: Doesn't work!
    // const valid = computed(() => {
    //   if (focus.value) {
    //     if (focus.value === "inline") return true;
    //     const actor = forms.value[focus.value];
    //     return useSelector(actor, (state) => state.context.validated);
    //   }
    //   return false;
    // });
    const valid = true;

    const handleSubmit = () => send("SAVE_FOCUS");

    return {
      handleSubmit,
      mouseoverSubmit,
      submitting,
      valid,
    };
  },
});
</script>
