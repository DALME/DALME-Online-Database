<template>
  <q-item v-if="item" clickable dense>
    <q-item-section avatar>
      <q-icon :name="icon" />
    </q-item-section>
    <q-item-section v-if="label">{{ label }}</q-item-section>
    <ChooserMenu
      :asItem="item"
      :label="label"
      :dark="dark"
      :type="type"
      :returnField="returnField"
      :showAvatar="showAvatar"
      :searchable="searchable"
      :showSelected="showSelected"
      :fetcher="fetcher"
      @item-chosen="(v) => $emit('itemChosen', v)"
      @clear-filters="$emit('clearFilters')"
    />
  </q-item>
  <q-btn
    v-else
    flat
    dense
    :label="label"
    :icon="icon && !label ? icon : null"
    :class="toggle ? 'text-capitalize' : 'text-capitalize no-toggle'"
    content-class="menu-shadow"
    :icon-right="toggle ? (show ? 'arrow_drop_up' : 'arrow_drop_down') : 'none'"
    @click="show = !show"
  >
    <ToolTip v-if="tooltip">{{ tooltip }}</ToolTip>
    <ChooserMenu
      :asItem="item"
      :dark="dark"
      :type="type"
      :label="label"
      :returnField="returnField"
      :showAvatar="showAvatar"
      :searchable="searchable"
      :showSelected="showSelected"
      :fetcher="fetcher"
      @item-chosen="(v) => $emit('itemChosen', v)"
      @clear-filters="$emit('clearFilters')"
    />
  </q-btn>
</template>

<script>
import { computed, defineComponent, defineAsyncComponent, ref } from "vue";
import ChooserMenu from "./ChooserMenu.vue";
import { ticketFetcher, userFetcher } from "./fetchers.js";

export default defineComponent({
  name: "GeneralChooser",
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
    label: String,
    tooltip: String,
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
  components: {
    ChooserMenu,
    ToolTip: defineAsyncComponent(() => import("@/components/widgets/ToolTip.vue")),
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

<style lang="scss">
.no-toggle > span.q-btn__content > .q-icon:nth-of-type(2) {
  display: none;
}
</style>
