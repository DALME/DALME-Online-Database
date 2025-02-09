<template>
  <q-item v-if="item" clickable dense ref="anchor">
    <q-item-section avatar>
      <q-icon :name="icon" />
    </q-item-section>
    <q-item-section>{{ label }}</q-item-section>
  </q-item>
  <q-btn-dropdown
    v-else
    ref="anchor"
    flat
    dense
    :label="label"
    menu-anchor="bottom right"
    menu-self="top right"
    class="text-capitalize"
    content-class="menu-shadow"
  >
    <ToolTip v-if="tooltip">{{ tooltip }}</ToolTip>

    <q-list bordered separator class="text-grey-9 choser-menu">
      <q-item v-if="header" dense class="q-pr-sm">
        <q-item-section class="text-weight-bold">{{ header }}</q-item-section>
        <q-item-section avatar>
          <q-btn flat dense size="xs" color="grey-6" icon="close" @click="$emit('clearFilters')" />
        </q-item-section>
      </q-item>

      <q-item v-if="showFilter" dense class="chooser-filter">
        <q-input
          :dark="dark"
          borderless
          square
          dense
          hide-bottom-space
          v-model="chooserFilter"
          debounce="300"
          autocomplete="off"
          autocorrect="off"
          autocapitalize="off"
          spellcheck="false"
          placeholder="Type to search"
          class="chooser-filter-box"
        >
          <template v-slot:append>
            <q-icon
              v-if="chooserFilter && !loading"
              name="mdi-close"
              class="cursor-pointer"
              @click="chooserFilter = ''"
            />
            <AdaptiveSpinner
              v-if="loading"
              type="bars"
              size="20px"
              :adaptive="false"
              color="indigo-3"
              class="q-mr-sm"
            />
          </template>
        </q-input>
      </q-item>

      <template v-if="showSelected && !isEmpty(selected)">
        <q-item dense class="bg-indigo-1 text-indigo-5 text-weight-bold chooser-selected">
          <slot name="chooser-selected-item" v-bind="selected" />
        </q-item>
      </template>
      <q-list separator>
        <q-item
          v-for="(item, idx) in itemData"
          :key="idx"
          clickable
          v-close-popup
          dense
          @click="selectItem(item)"
        >
          <slot name="chooser-item" v-bind="item" />
        </q-item>
      </q-list>
    </q-list>
  </q-btn-dropdown>
</template>

<script>
import { filter as rFilter, isEmpty } from "ramda";
import { computed, defineComponent, defineAsyncComponent, ref, watch } from "vue";
import { AdaptiveSpinner } from "@/components";
import { nully } from "@/utils";

export default defineComponent({
  name: "ChooserWidget",
  props: {
    item: {
      type: Boolean,
      default: false,
    },
    dark: {
      type: Boolean,
      default: false,
    },
    shadow: {
      type: Boolean,
      default: false,
    },
    label: {
      type: String,
      required: false,
    },
    name: {
      type: String,
      required: false,
    },
    tooltip: {
      type: String,
      required: false,
    },
    icon: {
      type: String,
      required: false,
      default: null,
    },
    header: {
      type: String,
      required: false,
    },
    returnField: {
      type: String,
      required: false,
      default: "id",
    },
    showAvatar: {
      type: Boolean,
      required: false,
      default: true,
    },
    showFilter: {
      type: Boolean,
      required: false,
      default: true,
    },
    showSelected: {
      type: Boolean,
      required: false,
      default: false,
    },
    toggle: {
      type: Boolean,
      default: false,
    },
    fetcher: {
      type: Function,
      required: true,
    },
    items: {
      type: Array,
      required: true,
    },
    loading: {
      type: Boolean,
      default: false,
    },
  },
  components: {
    AdaptiveSpinner,
    ToolTip: defineAsyncComponent(() => import("@/components/widgets/ToolTip.vue")),
  },
  emits: ["itemChosen", "clearFilters"],
  setup(props, context) {
    const anchor = ref(null);
    const chooserFilter = ref("");
    const selected = ref({});

    const selectItem = (item) => {
      selected.value = item;
      context.emit("itemChosen", item[props.returnField]);
    };

    const itemData = computed(() => {
      if (props.showSelected && !isEmpty(selected.value)) {
        return rFilter((item) => item.id !== selected.value.id, props.items);
      } else {
        return props.items;
      }
    });

    watch(chooserFilter, () => props.fetcher(chooserFilter.value));

    return {
      anchor,
      chooserFilter,
      isEmpty,
      selectItem,
      selected,
      itemData,
      nully,
    };
  },
});
</script>

<style lang="scss">
.choser-menu {
  min-width: 250px;
}
.chooser-avatar-image {
  padding: 3px;
}
.chooser-user-detail {
  margin-top: 0;
}
.chooser-filter {
  padding: 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
}
.chooser-filter-box {
  width: 100%;
}
.chooser-filter-box input.q-field__native {
  padding-left: 17px;
  padding-right: 17px;
}
.chooser-filter-box .q-field__append.q-field__marginal {
  padding-right: 8px;
}
.chooser-selected {
  border-top: none !important;
}
</style>
