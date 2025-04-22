<template>
  <q-item v-if="item" clickable dense>
    <q-item-section avatar>
      <q-icon :name="icon" />
    </q-item-section>
    <q-item-section v-if="label">{{ label }}</q-item-section>
    <ChooserMenu
      @clear-filters="$emit('clearFilters')"
      @item-chosen="(v) => $emit('itemChosen', v)"
      :as-item="item"
      :dark="dark"
      :fetcher="fetcher"
      :label="label"
      :return-field="returnField"
      :searchable="searchable"
      :show-avatar="showAvatar"
      :show-selected="showSelected"
      :type="type"
    />
  </q-item>
  <q-btn
    v-else
    @click="show = !show"
    :class="toggle ? 'text-capitalize' : 'text-capitalize no-toggle'"
    :icon="icon && !label ? icon : null"
    :icon-right="toggle ? (show ? 'arrow_drop_up' : 'arrow_drop_down') : 'none'"
    :label="label"
    content-class="menu-shadow"
    dense
    flat
  >
    <ToolTip v-if="tooltip">{{ tooltip }}</ToolTip>
    <ChooserMenu
      @clear-filters="$emit('clearFilters')"
      @item-chosen="(v) => $emit('itemChosen', v)"
      :as-item="item"
      :dark="dark"
      :fetcher="fetcher"
      :label="label"
      :return-field="returnField"
      :searchable="searchable"
      :show-avatar="showAvatar"
      :show-selected="showSelected"
      :type="type"
    />
  </q-btn>
</template>

<script>
import { computed, defineAsyncComponent, defineComponent, ref } from "vue";

import ChooserMenu from "./ChooserMenu.vue";
import { ticketFetcher, userFetcher } from "./fetchers.js";

export default defineComponent({
  name: "GeneralChooser",
  components: {
    ChooserMenu,
    ToolTip: defineAsyncComponent(() => import("@/components/widgets/ToolTip.vue")),
  },
  props: {
    item: {
      type: Boolean,
      default: false,
    },
    dark: {
      type: Boolean,
      default: false,
    },
    toggle: {
      type: Boolean,
      default: true,
    },
    type: {
      type: String,
      required: true,
    },
    label: {
      type: String,
      default: null,
    },
    tooltip: {
      type: String,
      required: false,
      default: null,
    },
    icon: {
      type: String,
      default: null,
    },
    returnField: {
      type: String,
      default: "id",
    },
    showAvatar: {
      type: Boolean,
      default: true,
    },
    searchable: {
      type: Boolean,
      default: true,
    },
    showSelected: {
      type: Boolean,
      default: false,
    },
  },

  emits: ["itemChosen", "clearFilters"],
  setup(props) {
    const show = ref(false);
    const fetcher = computed(() => (props.type === "users" ? userFetcher : ticketFetcher));

    return {
      show,
      fetcher,
    };
  },
});
</script>
