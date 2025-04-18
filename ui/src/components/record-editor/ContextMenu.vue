<template>
  <q-menu transition-hide="scale" transition-show="scale" context-menu touch-position>
    <q-list dense separator>
      <template v-for="(el, idx) in teiElements" :key="idx">
        <q-item clickable>
          <q-item-section>
            <q-item-label>{{ el.label }}</q-item-label>
          </q-item-section>
        </q-item>
      </template>
    </q-list>
  </q-menu>
</template>

<script>
import { defineComponent } from "vue";

import { useStores } from "@/use";

export default defineComponent({
  name: "ContextMenu",
  setup() {
    const { editorStore } = useStores();
    const teiElements = editorStore.contextMenu;

    return {
      teiElements,
    };
  },
});
</script>
