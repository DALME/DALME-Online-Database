<template>
  <transition name="collapse">
    <div v-if="Records.showTagMenu" :style="`height: ${editorHeight + 1}px`" class="col tag-menu">
      <q-input
        v-model="elementFilter"
        autocapitalize="off"
        autocomplete="off"
        autocorrect="off"
        class="tag-search-box"
        debounce="300"
        placeholder="Search tags"
        spellcheck="false"
        borderless
        dense
        hide-bottom-space
      >
        <template #append>
          <q-icon
            v-if="elementFilter"
            @click="elementFilter = ''"
            class="cursor-pointer"
            color="blue-grey-5"
            name="close"
            size="12px"
          />
        </template>
      </q-input>
      <q-list dense separator>
        <template v-for="(el, idx) in teiElements" :key="idx">
          <q-btn-dropdown
            :label="el.label"
            align="left"
            content-class="tag-menu-popup outlined-item menu-shadow"
            auto-close
            flat
            no-caps
            split
          >
            <q-list dense separator>
              <q-item>
                <q-item-section>
                  <q-item-label class="text-detail text-grey-7 q-py-sm">
                    <q-icon class="q-mr-xs" color="grey-6" name="o_info" size="14px" />
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
import { computed, defineComponent, inject, ref } from "vue";

import { Records } from "@/models";
import { useStores } from "@/use";

export default defineComponent({
  name: "TeiSidebar",
  setup() {
    const { editorStore } = useStores();
    const { editorHeight } = inject("editorDimensions");
    const elementFilter = ref("");
    const teiElements = computed(() => editorStore.elements(elementFilter.value));

    return {
      editorHeight,
      elementFilter,
      teiElements,
      Records,
    };
  },
});
</script>

<style lang="scss" scoped>
.tag-menu {
  overflow: scroll;
  border-left: 1px solid #d1d1d1;
  width: 300px !important;
  position: absolute;
  right: 0;
  background-color: rgb(255 255 255 / 89%);
  backdrop-filter: blur(1px) grayscale(70%);
}
.tag-menu .q-btn-group {
  width: 100%;
  border-radius: 0;
  border-bottom: 1px solid #d1d1d1;
}
.tag-menu .q-btn-group:last-of-type {
  border-bottom: none;
}
:deep(.tag-menu-popup) {
  max-width: 200px;
}
.tag-menu .tag-search-box {
  position: fixed;
  width: 100%;
  max-width: 300px !important;
  background: white;
  z-index: 99;
}
:deep(.tag-search-box .q-field__control) {
  font-size: 13px;
  height: 30px;
  padding: 0px 0px 0px 5px !important;
  border-bottom: 1px solid #d1d1d1;
}
:deep(.tag-search-box .q-field__marginal),
:deep(.tag-search-box .q-field__native) {
  height: 28px;
  padding: 6px 10px;
}
.tag-menu .q-list {
  margin-top: 31px;
}
</style>
