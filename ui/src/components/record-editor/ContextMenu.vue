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
    const { settings } = useStores();
    const teiElements = settings.elements.menu;

    return {
      teiElements,
    };
  },
});
</script>

<style lang="scss">
.ace_editor {
  white-space: pre-line;
  line-height: 1.3;
  font-family: "Menlo", "Consolas", monospace;
  margin-top: 10px;
  margin-bottom: 10px;
  background-color: transparent !important;
}
.ace_gutter {
  background: none !important;
}
.editor-panel {
  padding: 0;
  background: linear-gradient(120deg, #fefefe, #efefef) no-repeat 0px/40px 100%;
}
</style>
