<template>
  <q-btn
    flat
    :dense="dense"
    :label="label"
    :color="color"
    :icon="icon ? icon : 'none'"
    :icon-right="toggleIcon ? 'arrow_drop_down' : 'none'"
    :class="buttonClasses"
    no-caps
    padding="5px 5px"
  >
    <TooltipWidget v-if="toolTip">{{ toolTip }}</TooltipWidget>
    <q-menu
      anchor="bottom right"
      self="top right"
      class="menu-shadow outlined-item height-50"
    >
      <q-list :separator="separator" class="text-grey-9">
        <q-item v-if="showHeader" dense class="q-pr-sm">
          <q-item-section class="text-weight-bold">
            {{ headerText }}
          </q-item-section>
          <q-item-section v-if="clearFilters" avatar>
            <q-btn
              flat
              dense
              size="xs"
              color="grey-6"
              icon="close"
              @click="clearFilters"
            />
          </q-item-section>
        </q-item>
        <q-item v-if="showFilter" dense class="q-py-xs">
          <q-input
            dense
            borderless
            hide-bottom-space
            v-model="chooserFilter"
            debounce="300"
            autocomplete="off"
            autocorrect="off"
            autocapitalize="off"
            spellcheck="false"
            :placeholder="`Filter ${target}`"
            class="menu-item-search full-width"
          >
            <template v-slot:append>
              <q-icon
                v-if="chooserFilter"
                name="close"
                class="cursor-pointer"
                size="12px"
                color="blue-grey-5"
                @click="chooserFilter = ''"
              />
            </template>
          </q-input>
        </q-item>
        <q-item
          v-if="showSelectedItem && !isEmpty(selectedItem)"
          :dense="dense"
          class="bg-indigo-1 text-indigo-5"
        >
          <template v-if="target === 'users'">
            <q-item-section v-if="showAvatar" side>
              <q-avatar
                v-if="
                  !isEmpty(selectedItem.avatar) && !isNil(selectedItem.avatar)
                "
                size="22px"
              >
                <img :src="selectedItem.avatar" />
              </q-avatar>
              <q-icon v-else name="account_circle" size="22px" />
            </q-item-section>
            <q-item-section class="text-weight-bold">
              <span class="q-mr-sm">{{ selectedItem.username }}</span>
              <span class="text-detail text-weight-medium">
                {{ selectedItem.fullName }}
              </span>
            </q-item-section>
          </template>
          <template v-if="target === 'tickets'">
            <q-item-section>
              <div class="row items-center">
                <q-icon
                  :name="
                    selectedItem.status == 0
                      ? 'error_outline'
                      : 'check_circle_outline'
                  "
                  :color="selectedItem.status == 0 ? 'green-8' : 'purple-8'"
                  class="q-mr-sm"
                />
                <span
                  class="text-grey-6 q-mr-sm"
                  v-text="'#' + selectedItem.id"
                />
                <span
                  class="text-grey-8 text-weight-bold q-mr-sm"
                  v-text="selectedItem.subject"
                />
              </div>
            </q-item-section>
          </template>
        </q-item>
        <q-item
          v-for="(item, idx) in itemData"
          :key="idx"
          clickable
          v-close-popup
          :dense="dense"
          :class="menuClasses"
          @click="selectItem(item)"
        >
          <template v-if="target === 'users'">
            <q-item-section v-if="showAvatar" side>
              <q-avatar
                v-if="!isEmpty(item.avatar) && !isNil(item.avatar)"
                size="22px"
              >
                <img :src="item.avatar" />
              </q-avatar>
              <q-icon v-else name="account_circle" size="22px" />
            </q-item-section>
            <q-item-section class="text-weight-medium text-grey-8">
              <span class="q-mr-sm">{{ item.username }}</span>
              <span class="text-detail text-weight-regular">
                {{ item.fullName }}
              </span>
            </q-item-section>
          </template>
          <template v-if="target === 'tickets'">
            <q-item-section>
              <div class="row items-center">
                <q-icon
                  :name="
                    item.status == 0 ? 'error_outline' : 'check_circle_outline'
                  "
                  :color="item.status == 0 ? 'green-8' : 'purple-8'"
                  class="q-mr-sm"
                />
                <span class="text-grey-6 q-mr-sm" v-text="'#' + item.id" />
                <span
                  class="text-grey-8 text-weight-bold q-mr-sm"
                  v-text="item.subject"
                />
              </div>
            </q-item-section>
          </template>
        </q-item>
      </q-list>
    </q-menu>
    <q-inner-loading :showing="loading">
      <q-spinner-facebook size="20px" color="grey-6"></q-spinner-facebook>
    </q-inner-loading>
  </q-btn>
</template>

<script>
import { filter as rFilter, isEmpty, isNil } from "ramda";
import {
  computed,
  defineComponent,
  defineAsyncComponent,
  onMounted,
  ref,
  watch,
} from "vue";
import { requests } from "@/api";
import { ticketListSchema, userListSchema } from "@/schemas";
import { useAPI } from "@/use";

export default defineComponent({
  name: "ChooserWidget",
  props: {
    bordered: {
      type: Boolean,
      required: false,
      default: true,
    },
    useButton: {
      type: Boolean,
      required: false,
      default: false,
    },
    clearFilters: {
      type: Function,
      required: false,
    },
    classes: {
      type: String,
      required: false,
    },
    menuClasses: {
      type: String,
      required: false,
      default: "text-no-wrap",
    },
    color: {
      type: String,
      required: false,
      default: null,
    },
    dense: {
      type: Boolean,
      required: false,
      default: true,
    },
    label: {
      type: String,
      required: false,
    },
    headerText: {
      type: String,
      required: false,
      default: "Filter...",
    },
    icon: {
      type: String,
      required: false,
      default: null,
    },
    returnField: {
      type: String,
      required: false,
      default: "id",
    },
    separator: {
      type: Boolean,
      required: false,
      default: true,
    },
    showAvatar: {
      type: Boolean,
      required: false,
      default: true,
    },
    showHeader: {
      type: Boolean,
      required: false,
      default: false,
    },
    showFilter: {
      type: Boolean,
      required: false,
      default: true,
    },
    showSelectedItem: {
      type: Boolean,
      required: false,
      default: false,
    },
    target: {
      type: String,
      required: true,
    },
    toggleIcon: {
      type: Boolean,
      required: false,
      default: false,
    },
    toolTip: {
      type: String,
      required: false,
    },
  },
  components: {
    TooltipWidget: defineAsyncComponent(() =>
      import("@/components/widgets/TooltipWidget.vue"),
    ),
  },
  emits: ["itemChosen"],
  setup(props, context) {
    const { apiInterface } = useAPI();
    const { loading, success, data, fetchAPI } = apiInterface();
    const itemList = ref([]);
    const chooserFilter = ref("");
    const selectedItem = ref({});

    const selectItem = (item) => {
      selectedItem.value = item;
      context.emit("itemChosen", item[props.returnField]);
    };

    const buttonClasses = computed(() => {
      let classes = props.classes ? props.classes.split(" ") : [];
      if (!props.toggleIcon) classes.push("no-toggle-icon");
      if (!props.icon) classes.push("no-icon");
      return classes.join(" ");
    });

    const itemData = computed(() => {
      if (props.showSelectedItem && !isEmpty(selectedItem.value)) {
        return rFilter(
          (item) => item.id !== selectedItem.value.id,
          itemList.value,
        );
      } else {
        return itemList.value;
      }
    });

    const fetchData = async () => {
      const query = isEmpty(chooserFilter.value)
        ? "ordering=-is_active,id&limit=0&offset=0"
        : `ordering=-is_active,id&search=${chooserFilter.value}&limit=0&offset=0`;

      const request = {
        users: requests.users.getUsers(query),
        tickets: requests.tickets.getTickets(query),
      }[props.target];

      const schema = {
        users: userListSchema,
        tickets: ticketListSchema,
      }[props.target];

      await fetchAPI(request);
      if (success.value)
        await schema
          .validate(data.value.data, { stripUnknown: true })
          .then((value) => {
            itemList.value = value;
            loading.value = false;
          });
    };

    onMounted(async () => await fetchData());

    watch(chooserFilter, () => fetchData());

    return {
      buttonClasses,
      context,
      chooserFilter,
      isEmpty,
      isNil,
      loading,
      selectItem,
      selectedItem,
      itemData,
    };
  },
});
</script>
