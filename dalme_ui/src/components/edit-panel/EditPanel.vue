<template>
  <q-page-sticky position="bottom-right" :offset="position" class="z-max">
    <q-fab
      text-color="white"
      icon="keyboard_arrow_left"
      direction="left"
      class="parent"
      :disable="dragging"
      v-touch-pan.prevent.mouse="move"
    >
      <!-- ADD -->
      <EditCreate @submit-edit="handleSubmitEdit" />

      <!-- UPDATE -->
      <EditUpdate @submit-edit="handleSubmitEdit" />

      <!-- DELETE -->

      <!-- SUBMIT -->
      <EditSubmit @submit-edit="handleSubmitEdit" />
    </q-fab>
  </q-page-sticky>
</template>

<script>
import { defineComponent, inject, provide, ref, toRefs } from "vue";

import { default as EditCreate } from "./EditCreate.vue";
import { default as EditSubmit } from "./EditSubmit.vue";
import { default as EditUpdate } from "./EditUpdate.vue";
import { default as machine } from "./machines";

export default defineComponent({
  name: "EditPanel",
  components: {
    EditCreate,
    EditSubmit,
    EditUpdate,
  },
  setup() {
    const editing = inject("editing");

    const { enableSave, mode, submitting } = toRefs(editing);
    // TODO: Thread to children fabs. Won't be necessary if machine handles it.
    // TODO: https://vueuse.org/core/usedraggable/#usage ?
    const dragging = ref(false);
    const position = ref([30, 30]);

    provide("machine", machine);

    // Flipping `submitting = true` will trigger the editing watcher registered
    // by any component and call their submit handling function. They then have
    // the responsibility of resetting this ref as and when they see fit.
    const handleSubmitEdit = () => {
      if (!submitting.value) {
        submitting.value = true;
        enableSave.value = false;
      }
    };

    // TODO: Resize
    const move = (event) => {
      dragging.value = event.isFirst !== true && event.isFinal !== true;
      position.value = [
        position.value[0] - event.delta.x,
        position.value[1] - event.delta.y,
      ];
    };

    return {
      dragging,
      handleSubmitEdit,
      mode,
      move,
      position,
    };
  },
});
</script>

<style lang="scss">
.parent {
  background-color: #2f333c;
  background-image: linear-gradient(59deg, #11587c 54.62%, #1b1b1b);
}
</style>
