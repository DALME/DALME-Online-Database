<template>
  <q-menu touch-position context-menu transition-show="scale" transition-hide="scale">
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
