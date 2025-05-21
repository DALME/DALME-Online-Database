<template>
  <div class="sidebar-item">
    <q-btn
      v-if="editable"
      :label="label"
      :ripple="false"
      class="item-header"
      icon-right="mdi-cog-outline"
      dense
      flat
      no-caps
    >
      <q-menu anchor="bottom right" class="sidebar-item-menu" self="top right">
        <slot name="edit-menu" />
        <q-list dense>
          <q-item>
            <q-item-section>
              <q-item-label>Filter</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
      </q-menu>
    </q-btn>
    <div v-else class="text-detail text-grey-8 text-weight-bold q-mb-sm">
      {{ label }}
    </div>
    <div class="flex text-13 items-center">
      <slot name="content" />
      <span
        v-if="clipboard"
        @click="copyToClipboard(content)"
        class="cursor-pointer flex items-center"
      >
        {{ content }}
        <q-icon class="q-ml-sm" color="grey-6" name="content_copy" size="11px" />
      </span>
      <span v-else>{{ content }}</span>
    </div>
  </div>
</template>

<script>
import { defineComponent, ref } from "vue";

import { copyToClipboard } from "@/utils";

export default defineComponent({
  name: "SidebarItem",
  props: {
    label: {
      type: String,
      required: false,
      default: null,
    },
    content: {
      type: String,
      required: false,
      default: null,
    },
    clipboard: {
      type: Boolean,
      required: false,
      default: false,
    },
    editable: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  setup() {
    const loading = ref(false);

    return {
      copyToClipboard,
      loading,
    };
  },
});
</script>

<style lang="scss" scoped>
.sidebar-item {
  padding-bottom: 12px;
  margin-bottom: 12px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
}
.sidebar-item a {
  color: inherit;
}
.sidebar-item .item-header {
  font-size: 12px;
  font-weight: 700;
  color: #616161 !important;
  padding: 0;
  margin-bottom: 6px;
  width: 100%;
}
.sidebar-item .item-header .q-btn__content {
  width: 100%;
  justify-content: space-between;
  align-items: end;
}
.sidebar-item .item-header i.q-icon {
  font-size: 18px;
}
.sidebar-item .item-header:hover {
  color: #3f51b5 !important;
}
.sidebar-item .item-header:focus .q-focus-helper,
.sidebar-item .item-header:hover .q-focus-helper {
  background: none !important;
}
.sidebar-item .item-header:focus .q-focus-helper:before {
  opacity: 0 !important;
}
.sidebar-item-menu {
  min-width: 200px;
}
</style>
