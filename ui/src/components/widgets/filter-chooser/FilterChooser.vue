<template>
  <q-btn
    flat
    dense
    :label="label"
    class="text-capitalize"
    content-class="menu-shadow"
    :icon-right="show ? 'arrow_drop_up' : 'arrow_drop_down'"
    @click="show = !show"
  >
    <ToolTip v-if="tooltip">{{ tooltip }}</ToolTip>
    <q-menu anchor="bottom middle" self="top middle">
      <q-list bordered separator class="text-grey-9 choser-menu">
        <template v-if="ready">
          <q-item dense class="q-pr-sm">
            <q-item-section class="text-weight-bold"> Filter by {{ label }} </q-item-section>
            <q-item-section avatar>
              <q-btn
                flat
                dense
                size="xs"
                color="grey-6"
                icon="close"
                @click="$emit('clearFilters')"
              />
            </q-item-section>
          </q-item>

          <q-item v-if="searchable" dense class="chooser-filter">
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
                  name="mdi-close-circle"
                  class="cursor-pointer"
                  color="grey-5"
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

          <template v-if="showSelected && !nully(selectedVal)">
            <template v-if="selection === 'single'">
              <component :is="itemComponent" :item="selected" :class="classSelected" />
            </template>
            <template v-else>
              <template v-for="(item, idx) in selected" :key="idx">
                <component :is="itemComponent" :item="item" :class="classSelected" />
              </template>
            </template>
          </template>
          <q-list separator v-if="!loading && !nully(itemData)" class="chooser-items-container">
            <template v-for="(item, idx) in itemData" :key="idx">
              <template v-if="item.isGroup">
                <q-item
                  clickable
                  dense
                  :class="groupIsActive(item.label) ? item.classSelected : item.class"
                >
                  <q-item-section>{{ item.label }}</q-item-section>
                  <q-item-section side>
                    <q-icon name="mdi-chevron-right" size="xs" color="grey-6" />
                  </q-item-section>
                  <q-menu>
                    <q-list bordered separator class="text-grey-9">
                      <template v-for="(opt, oidx) in item.options" :key="oidx">
                        <component
                          :is="itemComponent"
                          :item="opt"
                          :item-class="getItemClass(opt)"
                          @item-chosen="selectItem"
                        />
                      </template>
                    </q-list>
                  </q-menu>
                </q-item>
              </template>
              <template v-else>
                <component
                  :is="itemComponent"
                  :item="item"
                  :item-class="getItemClass(item)"
                  @item-chosen="selectItem"
                />
              </template>
            </template>
          </q-list>
        </template>
        <template v-else>
          <q-item dense>
            <q-skeleton type="text" height="28px" width="90%" />
          </q-item>
          <q-item dense>
            <q-skeleton type="text" height="28px" width="80%" />
          </q-item>
          <q-item dense>
            <q-skeleton type="text" height="28px" width="90%" />
          </q-item>
          <q-item dense>
            <q-skeleton type="text" height="28px" width="60%" />
          </q-item>
        </template>
      </q-list>
    </q-menu>
  </q-btn>
</template>

<script>
import { filter as rFilter } from "ramda";
import {
  computed,
  defineComponent,
  defineAsyncComponent,
  inject,
  onBeforeMount,
  ref,
  watch,
} from "vue";
import { AdaptiveSpinner } from "@/components";
import { nully, isNumber } from "@/utils";
import ItemGeneric from "./ItemGeneric.vue";
import ItemUser from "./ItemUser.vue";
import ItemTicket from "./ItemTicket.vue";
import { groupBy, prop } from "ramda";

export default defineComponent({
  name: "FilterChooser",
  props: {
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
      required: true,
    },
    tooltip: String,
    returnField: String,
    class: {
      type: String,
      default: "text-grey-8",
    },
    classSelected: {
      type: String,
      default: "text-weight-bold bg-indigo-1 text-indigo-5",
    },
    searchable: {
      type: Boolean,
      default: false,
    },
    showAvatar: {
      type: Boolean,
      default: true,
    },
    showSelected: {
      type: Boolean,
      default: false,
    },
    fetcher: Function,
    items: Array,
    selection: {
      type: String,
      default: "single",
    },
    group: {
      type: Boolean,
      default: false,
    },
  },
  components: {
    AdaptiveSpinner,
    ItemGeneric,
    ItemUser,
    ItemTicket,
    ToolTip: defineAsyncComponent(() => import("@/components/widgets/ToolTip.vue")),
  },
  emits: ["itemChosen", "clearFilters"],
  setup(props, context) {
    const show = ref(false);
    const itemComponent = computed(() => {
      switch (props.type) {
        case "users":
          return "ItemUser";
        case "tickets":
          return "ItemTicket";
        default:
          return "ItemGeneric";
      }
    });
    const activeFilters = inject("activeFilters");
    const options = ref(null);
    const ready = ref(false);
    const activeGroups = props.selection === "single" ? ref(null) : ref([]);
    const selectedVal = props.selection === "single" ? ref(null) : ref([]);
    const selected = props.selection === "single" ? ref(null) : ref([]);
    const search = ref("");
    const loading = ref(false);

    const itemValue = (item) => {
      const raw = props.returnField ? item[props.returnField] : item.value;
      return isNumber(raw) ? raw.toString() : raw;
    };

    const valueInFilters = (value) => {
      return nully(activeFilters.value)
        ? false
        : props.selection === "single"
          ? props.field in activeFilters.value && activeFilters.value[props.field] === value
          : props.field in activeFilters.value && activeFilters.value[props.field].includes(value);
    };

    const getItemClass = (item) => {
      if (props.type === "generic") {
        return valueInFilters(item.value) ? item.classSelected : item.class;
      } else {
        const value = itemValue(item);
        const isSelected =
          props.selection === "single"
            ? selectedVal.value === value
            : selectedVal.value.includes(value);
        return isSelected ? props.classSelected : props.class;
      }
    };

    const groupIsActive = (group) => {
      return props.selection === "single"
        ? activeGroups.value === group
        : activeGroups.value.includes(group);
    };

    const selectItem = (item) => {
      const value = itemValue(item);
      if (item.group) {
        if (props.selection === "single") {
          activeGroups.value = activeGroups.value === item.group ? null : item.group;
        } else {
          if (activeGroups.value.includes(item.group)) {
            activeGroups.value = activeGroups.value.filter((x) => x !== item.group);
          } else {
            activeGroups.value.push(item.group);
          }
        }
      }
      if (props.showSelected) {
        if (props.selection === "single") {
          selectedVal.value = value;
          selected.value = item;
        } else {
          if (selectedVal.value.includes(value)) {
            selectedVal.value = selectedVal.value.filter((x) => x !== value);
            selected.value = selected.value.filter((x) => itemValue(x) !== value);
          } else {
            selectedVal.value.push(value);
            selected.value.push(item);
          }
        }
      }
      context.emit("itemChosen", value);
    };

    onBeforeMount(() => {
      if (props.fetcher && !props.searchable) {
        props.fetcher().then((items) => {
          if (props.group && "group" in items[0]) {
            const groupClass = items[0].class;
            const groupClassSelected = items[0].classSelected;
            const grouped = groupBy(prop("group"), items);
            options.value = Object.keys(grouped).map((key) => ({
              label: key,
              isGroup: true,
              options: grouped[key],
              class: groupClass,
              classSelected: groupClassSelected,
            }));
          } else {
            options.value = items;
          }
          ready.value = true;
        });
      } else {
        options.value = props.items;
        ready.value = true;
      }

      if (props.searchable) {
        watch(
          () => search.value,
          () => {
            loading.value = true;
            props.fetcher(search.value).then((items) => {
              options.value = items;
              loading.value = false;
            });
          },
        );
      }
    });

    const itemData = computed(() => {
      if (props.showSelected && !nully(selectedVal.value)) {
        if (props.selection === "single") {
          return rFilter((item) => itemValue(item) !== selectedVal.value, options.value);
        } else {
          return rFilter((item) => !selectedVal.value.includes(itemValue(item)), options.value);
        }
      } else {
        return options.value;
      }
    });

    return {
      show,
      groupIsActive,
      options,
      ready,
      selectItem,
      valueInFilters,
      search,
      selectedVal,
      selected,
      itemData,
      nully,
      loading,
      itemComponent,
      getItemClass,
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
  margin-top: 0 !important;
}
.chooser-filter {
  padding: 0;
  border-bottom: none;
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
.chooser-items-container {
  border-top: 1px solid rgba(0, 0, 0, 0.12);
}
</style>
