<template>
  <div class="row text-grey-7 toolbar">
    <template v-for="(els, section) in editorStore.toolbar" :key="section">
      <q-btn-group class="editor-tb-group" flat>
        <template v-for="(el, idx) in els" :key="idx">
          <q-btn :icon="el.icon" class="editor-tb-button" size="xs" flat>
            <TeiTagMenu @insert="insertTag" :el-data="el" :tag-data="el.tags[0]" action="create" />
          </q-btn>
        </template>
      </q-btn-group>
      <q-separator class="q-mx-xs" inset vertical />
    </template>
    <div class="editor-tb-right">
      <q-btn-dropdown class="editor-tb-button" icon="settings" size="sm" flat>
        <q-list bordered dense padding>
          <q-item>
            <q-item-section>
              <q-item-label class="text-overline">Editor Preferences</q-item-label>
            </q-item-section>
          </q-item>
          <template v-for="(pref, idx) in Preferences.all()" :key="idx">
            <q-item v-if="pref.group === 'Record Editor' && pref.dataType != 'JSON'">
              <q-item-section>
                <q-item-label overline><span v-text="pref.label"></span></q-item-label>
                <q-item-label lines="2" caption
                  ><span v-text="pref.description"></span
                ></q-item-label>
              </q-item-section>
              <q-item-section side>
                <q-toggle
                  v-if="pref.dataType === 'BOOL'"
                  @update:model-value="Preferences.set(pref.name, !pref.value)"
                  :model-value="pref.value"
                  class="editor-prefs-toggle"
                />
                <q-slider
                  v-else-if="pref.dataType === 'INT'"
                  @update:model-value="(newValue) => Preferences.set(pref.name, newValue)"
                  :max="fontSizeOptions.max"
                  :min="fontSizeOptions.min"
                  :model-value="pref.value"
                  class="editor-prefs-slider"
                  dense
                  label
                  label-always
                />
                <q-select
                  v-else
                  @update:model-value="(newValue) => Preferences.set(pref.name, newValue)"
                  :model-value="pref.value"
                  :options="themeOptions"
                  dense
                  map-options
                  options-dense
                  outlined
                />
              </q-item-section>
            </q-item>
          </template>
        </q-list>
      </q-btn-dropdown>
      <q-btn
        @click="Records.showTagMenu = !Records.showTagMenu"
        :icon-right="Records.showTagMenu ? 'arrow_drop_up' : 'arrow_drop_down'"
        class="editor-tb-button"
        icon="code"
        size="sm"
        flat
      />
    </div>
  </div>
</template>

<script>
import { defineComponent, inject } from "vue";

import { Preferences, Records } from "@/models";
import { useConstants, useStores } from "@/use";

import TeiTagMenu from "./TeiTagMenu.vue";

export default defineComponent({
  name: "ToolBar",
  components: { TeiTagMenu },

  setup() {
    const { editorStore } = useStores();
    const { fontSizeOptions, themeOptions } = useConstants();
    const insertTag = inject("insertTag");

    return {
      Records,
      Preferences,
      insertTag,
      editorStore,
      fontSizeOptions,
      themeOptions,
    };
  },
});
</script>

<style lang="scss" scoped>
.text-overline {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-weight: 700;
}
.editor-prefs-toggle {
  align-self: end;
}
.editor-prefs-slider {
  min-width: 150px;
}
.editor-tb-right,
.editor-tb-group {
  padding: 6px 0 6px 0;
}
.editor-tb-button {
  padding: 4px 10px;
}
.editor-tb-right .q-btn-dropdown--simple * + .q-btn-dropdown__arrow {
  margin-left: 0;
}
</style>
