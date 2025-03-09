<template>
  <q-menu anchor="top right" self="top left" :class="dark ? 'dark' : ''">
    <q-list bordered separator class="text-grey-9 choser-menu">
      <q-item v-if="!asItem && label" dense class="q-pr-sm">
        <q-item-section class="text-weight-bold">{{ label }}</q-item-section>
        <q-item-section avatar>
          <q-btn flat dense size="xs" color="grey-6" icon="close" @click="$emit('clearFilters')" />
        </q-item-section>
      </q-item>

      <q-item
        v-if="searchable"
        dense
        :class="`${asItem ? 'chooser-filter-st' : 'chooser-filter'} ${
          loading || nully(itemData) ? 'standalone' : ''
        }`"
      >
        <q-input
          :dark="dark"
          borderless
          square
          dense
          hide-bottom-space
          v-model="search"
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
              v-if="search && !loading"
              name="mdi-close"
              class="cursor-pointer"
              @click="search = ''"
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

      <template v-if="showSelected && !nully(selected)">
        <component :is="itemComponent" :item="selected" :dark="dark" itemClass="chooser-selected" />
      </template>
      <q-list separator class="chooser-items-container">
        <template v-for="(item, idx) in itemData" :key="idx">
          <component :is="itemComponent" :item="item" :dark="dark" @item-chosen="selectItem" />
        </template>
      </q-list>
    </q-list>
  </q-menu>
</template>

<script>
import { filter as rFilter } from "ramda";
import { computed, defineComponent, onBeforeMount, ref, watch } from "vue";
import { AdaptiveSpinner } from "@/components";
import ItemUser from "./ItemUser.vue";
import ItemTicket from "./ItemTicket.vue";
import { nully } from "@/utils";

export default defineComponent({
  name: "ChooserMenu",
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
    label: String,
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
  components: {
    AdaptiveSpinner,
    ItemUser,
    ItemTicket,
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
