<template>
  <transition name="collapse">
    <div v-if="view.showTagMenu" class="col tag-menu" :style="`height: ${editorHeight + 20}px`">
      <q-input
        dense
        borderless
        hide-bottom-space
        v-model="elementFilter"
        debounce="300"
        autocomplete="off"
        autocorrect="off"
        autocapitalize="off"
        spellcheck="false"
        :placeholder="`Filter tags`"
        class="tag-search-box full-width"
      >
        <template v-slot:append>
          <q-icon
            v-if="elementFilter"
            name="close"
            class="cursor-pointer"
            size="12px"
            color="blue-grey-5"
            @click="elementFilter = ''"
          />
        </template>
      </q-input>
      <q-list dense separator>
        <template v-for="(el, idx) in teiElements" :key="idx">
          <q-btn-dropdown
            flat
            no-caps
            auto-close
            split
            align="left"
            :label="el.label"
            content-class="tag-menu-popup outlined-item menu-shadow"
          >
            <q-list dense separator>
              <q-item>
                <q-item-section>
                  <q-item-label class="text-detail text-grey-7 q-py-sm">
                    <q-icon name="o_info" size="14px" color="grey-6" class="q-mr-xs" />
                    <span v-html="el.description" />
                  </q-item-label>
                </q-item-section>
              </q-item>
              <q-item clickable>
                <q-item-section>
                  <q-item-label class="text-grey-9"> Include in shortcuts </q-item-label>
                </q-item-section>
              </q-item>
              <q-item clickable>
                <q-item-section>
                  <q-item-label class="text-grey-9"> Include in context menu </q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
          </q-btn-dropdown>
        </template>
      </q-list>
    </div>
  </transition>
</template>

<script>
import { defineComponent, inject, ref } from "vue";
import { useStores } from "@/use";

export default defineComponent({
  name: "TeiSidebar",
  setup() {
    const { settings, view } = useStores();
    const { editorHeight } = inject("editorDimensions");
    const elementFilter = ref("");
    const teiElements = settings.elements.filter(elementFilter.value);

    return {
      editorHeight,
      elementFilter,
      teiElements,
      view,
    };
  },
});
</script>

<style lang="scss">
.tag-menu {
  overflow: scroll;
  border-left: 1px solid #d1d1d1;
  margin-left: 8px;
  max-width: 300px !important;
}
.tag-menu .q-btn-group {
  width: 100%;
  border-radius: 0;
  border-bottom: 1px solid #d1d1d1;
}
.tag-menu .q-btn-group:last-of-type {
  border-bottom: none;
}
.tag-menu-popup {
  max-width: 200px;
}
.tag-search-box .q-field__control {
  font-size: 13px;
  height: 30px;
  padding: 0px 0px 0px 5px !important;
  border-bottom: 1px solid #d1d1d1;
}
.tag-search-box .q-field__marginal,
.tag-search-box .q-field__native {
  height: 28px;
  padding: 6px 10px;
}
</style>
