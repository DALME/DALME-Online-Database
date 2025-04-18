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
          <template v-for="(setting, idx) in settings.preferences" :key="idx">
            <q-item v-if="setting.group === 'Record Editor' && setting.dataType != 'JSON'">
              <q-item-section>
                <q-item-label overline><span v-text="setting.label"></span></q-item-label>
                <q-item-label lines="2" caption
                  ><span v-text="setting.description"></span
                ></q-item-label>
              </q-item-section>
              <q-item-section side>
                <q-toggle
                  v-if="setting.dataType === 'BOOL'"
                  v-model="setting.value"
                  class="editor-prefs-toggle"
                />
                <q-slider
                  v-else-if="setting.dataType === 'INT'"
                  v-model="setting.value"
                  :max="settings.getOptions(setting.name).max"
                  :min="settings.getOptions(setting.name).min"
                  class="editor-prefs-slider"
                  dense
                  label
                  label-always
                />
                <q-select
                  v-else
                  v-model="setting.value"
                  :options="settings.getOptions(setting.name)"
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
        @click="view.showTagMenu = !view.showTagMenu"
        :icon-right="view.showTagMenu ? 'arrow_drop_up' : 'arrow_drop_down'"
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

import { useStores } from "@/use";

import TeiTagMenu from "./TeiTagMenu.vue";

export default defineComponent({
  name: "ToolBar",
  components: { TeiTagMenu },

  setup() {
    const { view, settings, editorStore } = useStores();
    const insertTag = inject("insertTag");

    return {
      view,
      settings,
      insertTag,
      editorStore,
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
