<template>
  <div class="row text-grey-7 toolbar">
    <template v-for="(els, section) in settings.elements.toolbar" :key="section">
      <q-btn-group flat class="editor-tb-group">
        <template v-for="(el, idx) in els" :key="idx">
          <q-btn flat size="xs" :icon="el.icon" class="editor-tb-button">
            <TeiTagMenu
              action="create"
              :tag="el.tags[0]"
              :attributes="el.tags[0].attributes"
              :icon="el.icon"
              :label="el.label"
              :description="el.description"
            />
          </q-btn>
        </template>
      </q-btn-group>
      <q-separator vertical inset class="q-mx-xs" />
    </template>
    <div class="editor-tb-right">
      <q-btn-dropdown flat icon="settings" size="sm" class="editor-tb-button">
        <q-list dense bordered padding>
          <q-item>
            <q-item-section>
              <q-item-label class="text-overline">Editor Preferences</q-item-label>
            </q-item-section>
          </q-item>
          <template v-for="(setting, idx) in settings.preferences" :key="idx">
            <q-item v-if="setting.group === 'Record Editor' && setting.dataType != 'JSON'">
              <q-item-section>
                <q-item-label overline><span v-text="setting.label"></span></q-item-label>
                <q-item-label caption lines="2"
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
                  :min="settings.getOptions(setting.name).min"
                  :max="settings.getOptions(setting.name).max"
                  label
                  dense
                  label-always
                  class="editor-prefs-slider"
                />
                <q-select
                  v-else
                  v-model="setting.value"
                  :options="settings.getOptions(setting.name)"
                  dense
                  options-dense
                  map-options
                  outlined
                />
              </q-item-section>
            </q-item>
          </template>
        </q-list>
      </q-btn-dropdown>
      <q-btn
        flat
        class="editor-tb-button"
        icon="code"
        size="sm"
        :icon-right="view.showTagMenu ? 'arrow_drop_up' : 'arrow_drop_down'"
        @click="view.showTagMenu = !view.showTagMenu"
      />
    </div>
  </div>
</template>

<script>
import { defineComponent } from "vue";
import { useStores } from "@/use";
import TeiTagMenu from "./TeiTagMenu.vue";

export default defineComponent({
  name: "ToolBar",
  components: { TeiTagMenu },

  setup() {
    const { view, settings } = useStores();

    return {
      view,
      settings,
    };
  },
});
</script>

<style lang="scss">
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
