<template>
  <template v-if="data">
    <template v-for="item in data" :key="item.field">
      <DetailElement :data="item" :field="item.field" />
    </template>
  </template>
  <slot name="extraElements" />
</template>

<script>
import { defineComponent } from "vue";

import { copyToClipboard } from "@/utils";

import DetailElement from "./DetailElement.vue";

export default defineComponent({
  name: "DetailSidebar",
  components: {
    DetailElement,
  },
  props: {
    data: {
      type: Array,
      required: false,
      default: null,
    },
  },
  setup() {
    return { copyToClipboard };
  },
});
</script>

<style lang="scss" scoped>
.detail-sidebar-item {
  padding-bottom: 12px;
  margin-bottom: 12px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
}
.detail-sidebar-item a {
  color: inherit;
}
.detail-sidebar-item .item-header {
  font-size: 12px;
  font-weight: 700;
  color: #616161 !important;
  padding: 0;
  margin-bottom: 6px;
  width: 100%;
}
.detail-sidebar-item .item-header .q-btn__content {
  width: 100%;
  justify-content: space-between;
  align-items: end;
}
.detail-sidebar-item .item-header i.q-icon {
  font-size: 18px;
}
.detail-sidebar-item .item-header:hover {
  color: #3f51b5 !important;
}
.detail-sidebar-item .item-header:focus .q-focus-helper,
.detail-sidebar-item .item-header:hover .q-focus-helper {
  background: none !important;
}
.detail-sidebar-item .item-header:focus .q-focus-helper:before {
  opacity: 0 !important;
}
.detail-sidebar-item-menu {
  min-width: 200px;
}
</style>
