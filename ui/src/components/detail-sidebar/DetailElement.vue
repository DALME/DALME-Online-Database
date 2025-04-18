<template>
  <div class="detail-sidebar-item">
    <q-btn
      v-if="editable"
      :label="data?.label || label"
      :ripple="false"
      class="item-header"
      icon-right="mdi-cog-outline"
      dense
      flat
      no-caps
    >
      <q-menu anchor="bottom right" class="detail-sidebar-item-menu" self="top right">
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
      {{ data?.label || label }}
    </div>
    <div class="flex text-13 items-center">
      <slot name="content" />
      <span v-if="data?.clipboard" @click="copyToClipboard(value)" class="cursor-pointer">
        {{ value }}
      </span>
      <span v-else>{{ value }}</span>
    </div>
  </div>
</template>

<script>
import { map as rMap } from "ramda";
import { defineComponent, onBeforeMount, ref } from "vue";

import { copyToClipboard } from "@/utils";

export default defineComponent({
  name: "DetailElement",
  props: {
    data: {
      type: Object,
      required: false,
      default: null,
    },
    field: {
      type: String,
      required: true,
    },
    label: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const value = ref(null);
    const editable = ref(props.data?.editable || false);
    const loading = ref(false);

    if (props.data) {
      onBeforeMount(() => {
        if (props.data.dataType === "FKEY") {
          loading.value = true;
          if (Array.isArray(props.data.value)) {
            value.value = rMap((v) => `${v.value.id}`, props.data.value);
          } else {
            value.value = `${props.data.value.id}`;
          }
          loading.value = false;
        } else {
          value.value = props.data.value;
        }
      });
    }

    return {
      copyToClipboard,
      value,
      editable,
    };
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
