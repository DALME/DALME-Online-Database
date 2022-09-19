<template>
  <q-page-sticky
    v-if="isAdmin"
    position="bottom-right"
    :offset="position"
    class="z-max"
  >
    <q-fab
      ref="el"
      text-color="white"
      icon="keyboard_arrow_left"
      direction="left"
      class="parent"
      :color="dragging ? 'grey' : 'initial'"
      :disable="dragging"
      v-touch-pan.vertical.prevent.mouse="move"
      push
      glossy
      square
      padding="md xl md sm"
    >
      <!-- ADD -->
      <EditCreate />

      <!-- UPDATE -->
      <EditUpdate />

      <!-- DELETE -->

      <!-- SUBMIT -->
      <EditSubmit />
    </q-fab>
  </q-page-sticky>
</template>

<script>
import { computed, defineComponent, onMounted, provide, ref } from "vue";

import { useEditing, usePermissions } from "@/use";

import { default as EditCreate } from "./EditCreate.vue";
import { default as EditSubmit } from "./EditSubmit.vue";
import { default as EditUpdate } from "./EditUpdate.vue";

export default defineComponent({
  name: "EditPanel",
  components: {
    EditCreate,
    EditSubmit,
    EditUpdate,
  },
  setup() {
    const { hideEditing, showEditing } = useEditing();
    const {
      permissions: { isAdmin },
    } = usePermissions();

    const el = ref(null);
    const dragging = ref(false);
    const position = ref([-30, 30]);

    const maxH = computed(() => window.innerHeight - 112);

    const move = (event) => {
      dragging.value = event.isFirst !== true && event.isFinal === false;
      position.value = [
        position.value[0],
        0 <= position.value[1] - event.delta.y &&
        position.value[1] - event.delta.y <= maxH.value
          ? position.value[1] - event.delta.y
          : position.value[1],
      ];
    };

    provide("dragging", dragging);

    onMounted(() => {
      hideEditing.value = el.value.hide;
      showEditing.value = el.value.show;
    });

    return {
      el,
      dragging,
      isAdmin,
      move,
      position,
    };
  },
});
</script>

<style lang="scss" scoped>
.parent {
  background-color: #2f333c;
  background-image: linear-gradient(59deg, #11587c 54.62%, #1b1b1b);
}
</style>
