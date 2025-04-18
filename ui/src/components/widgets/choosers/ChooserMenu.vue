<template>
  <q-menu :class="dark ? 'dark' : ''" anchor="top right" self="top left">
    <q-list class="text-grey-9 choser-menu" bordered separator>
      <q-item v-if="!asItem && label" class="q-pr-sm" dense>
        <q-item-section class="text-weight-bold">{{ label }}</q-item-section>
        <q-item-section avatar>
          <q-btn @click="$emit('clearFilters')" color="grey-6" icon="close" size="xs" dense flat />
        </q-item-section>
      </q-item>

      <q-item
        v-if="searchable"
        :class="`${asItem ? 'chooser-filter-st' : 'chooser-filter'} ${
          loading || nully(itemData) ? 'standalone' : ''
        }`"
        dense
      >
        <q-input
          v-model="search"
          :dark="dark"
          autocapitalize="off"
          autocomplete="off"
          autocorrect="off"
          class="chooser-filter-box"
          debounce="300"
          placeholder="Type to search"
          spellcheck="false"
          borderless
          dense
          hide-bottom-space
          square
        >
          <template #append>
            <q-icon
              v-if="search && !loading"
              @click="search = ''"
              class="cursor-pointer"
              name="mdi-close"
            />
            <AdaptiveSpinner
              v-if="loading"
              :adaptive="false"
              class="q-mr-sm"
              color="indigo-3"
              size="20px"
              type="bars"
            />
          </template>
        </q-input>
      </q-item>

      <template v-if="showSelected && !nully(selected)">
        <component
          :is="itemComponent"
          :dark="dark"
          :item="selected"
          item-class="chooser-selected"
        />
      </template>
      <q-list class="chooser-items-container" separator>
        <template v-for="(item, idx) in itemData" :key="idx">
          <component :is="itemComponent" @item-chosen="selectItem" :dark="dark" :item="item" />
        </template>
      </q-list>
    </q-list>
  </q-menu>
</template>

<script>
import { filter as rFilter } from "ramda";
import { computed, defineComponent, onBeforeMount, ref, watch } from "vue";

import { AdaptiveSpinner } from "@/components";
import { nully } from "@/utils";

import ItemTicket from "./ItemTicket.vue";
import ItemUser from "./ItemUser.vue";

export default defineComponent({
  name: "ChooserMenu",
  components: {
    AdaptiveSpinner,
    ItemUser,
    ItemTicket,
  },
  props: {
    asItem: {
      type: Boolean,
      default: false,
    },
    dark: {
      type: Boolean,
      default: false,
    },
    type: {
      type: String,
      required: true,
    },
    label: {
      type: String,
      required: false,
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
    fetcher: {
      type: Function,
      required: true,
    },
  },
  emits: ["itemChosen", "clearFilters"],
  setup(props, context) {
    const show = ref(false);
    const itemComponent = computed(() => (props.type === "users" ? "ItemUser" : "ItemTicket"));
    const search = ref("");
    const selected = ref(null);
    const loading = ref(false);
    const items = ref([]);

    const selectItem = (item) => {
      selected.value = item;
      context.emit("itemChosen", item[props.returnField]);
    };

    const itemData = computed(() => {
      if (props.showSelected && !nully(selected.value)) {
        return rFilter(
          (item) => item[props.returnField] !== selected.value[props.returnField],
          items.value,
        );
      } else {
        return items.value;
      }
    });

    onBeforeMount(() => {
      if (props.fetcher && !props.searchable) {
        loading.value = true;
        props.fetcher().then((data) => {
          items.value = data;
          loading.value = false;
        });
      } else if (props.searchable) {
        watch(
          () => search.value,
          () => {
            loading.value = true;
            props.fetcher(search.value).then((data) => {
              items.value = data;
              loading.value = false;
            });
          },
        );
      }
    });

    return {
      itemComponent,
      show,
      selectItem,
      selected,
      itemData,
      nully,
      loading,
      search,
    };
  },
});
</script>

<style lang="scss" scoped>
.choser-menu {
  min-width: 250px;
}
.chooser-avatar-image {
  padding: 3px;
}
.chooser-user-detail {
  margin-top: 0;
}
.chooser-filter,
.chooser-filter-st {
  padding: 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
}
.chooser-filter-st {
  border-top-right-radius: 4px;
  border-top-left-radius: 4px;
}
.chooser-filter-st.standalone {
  border-bottom-right-radius: 4px;
  border-bottom-left-radius: 4px;
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
.q-menu.dark {
  background-color: var(--dark-bg-base-colour);
}
.q-menu.dark .q-item {
  color: var(--dark-menu-text-colour);
  border-color: var(--dark-border-base-colour);
}
.q-menu.dark .q-list--bordered,
.q-menu.dark .q-card--bordered {
  border-color: var(--dark-border-base-colour);
}
.q-menu.dark .chooser-filter,
.q-menu.dark .chooser-filter-st {
  background-color: var(--dark-bg-base-colour);
}
.q-menu.dark .q-item__label--caption {
  color: var(--dark-secondary-text-colour);
}
</style>
