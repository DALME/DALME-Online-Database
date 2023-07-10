<template>
  <q-item v-if="item" clickable dense ref="anchor">
    <q-item-section avatar>
      <q-icon :name="icon" />
    </q-item-section>
    <q-item-section>{{ label }}</q-item-section>
  </q-item>
  <q-btn v-else ref="anchor" :label="label" :icon="icon ? icon : 'none'">
    <TooltipWidget v-if="tooltip">{{ tooltip }}</TooltipWidget>
    <q-inner-loading :showing="loading">
      <q-spinner-facebook size="20px"></q-spinner-facebook>
    </q-inner-loading>
  </q-btn>

  <q-menu
    v-if="anchor"
    cover
    :target="anchor"
    class="chooser-widget popup-menu filtered"
    :class="dark ? 'dark' : ''"
  >
    <q-item v-if="header" dense class="header">
      <q-item-section>{{ header }}</q-item-section>
      <q-item-section v-if="clearFilters" avatar>
        <q-btn flat dense size="xs" icon="mdi-close" @click="clearFilters" />
      </q-item-section>
    </q-item>

    <q-item v-if="showFilter" dense class="filter">
      <q-input
        :dark="dark"
        outlined
        dense
        hide-bottom-space
        v-model="chooserFilter"
        debounce="300"
        autocomplete="off"
        autocorrect="off"
        autocapitalize="off"
        spellcheck="false"
        :placeholder="`Filter ${target}`"
      >
        <template v-slot:append>
          <q-icon
            v-if="chooserFilter"
            name="mdi-close"
            class="cursor-pointer"
            @click="chooserFilter = ''"
          />
        </template>
      </q-input>
    </q-item>

    <template v-if="showSelected && !isEmpty(selected)">
      <q-item dense>
        <template v-if="target === 'users'">
          <q-item-section v-if="showAvatar" side>
            <q-avatar size="22px">
              <img v-if="notNully(selected.avatar)" :src="selected.avatar" />
              <q-icon v-else size="22px" name="mdi-account-circle" />
            </q-avatar>
          </q-item-section>
          <q-item-section class="text-roboto">
            <q-item-label>
              {{ selected.username }}
              <span class="text-detail">
                {{ selected.fullName }}
              </span>
            </q-item-label>
          </q-item-section>
        </template>

        <template v-if="target === 'tickets'">
          <q-item-section side>
            <q-icon
              :name="ticketIcon(selected.status)"
              :color="selected.status == 0 ? 'light-green-8' : 'purple-6'"
              size="16px"
            />
          </q-item-section>
          <q-item-section class="text-roboto">
            <q-item-label>
              <span class="text-detail q-mr-sm">
                {{ `#${selected.id}` }}
              </span>
              {{ selected.subject }}
            </q-item-label>
          </q-item-section>
        </template>
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
        <template v-if="target === 'users'">
          <q-item-section v-if="showAvatar" side>
            <q-avatar size="22px">
              <img v-if="notNully(item.avatar)" :src="item.avatar" />
              <q-icon v-else size="22px" name="mdi-account-circle" />
            </q-avatar>
          </q-item-section>
          <q-item-section class="text-roboto">
            <q-item-label>
              {{ item.username }}
              <span class="text-detail">
                {{ item.fullName }}
              </span>
            </q-item-label>
          </q-item-section>
        </template>

        <template v-if="target === 'tickets'">
          <q-item-section side>
            <q-icon
              :name="ticketIcon(item.status)"
              :color="item.status == 0 ? 'light-green-6' : 'deep-purple-4'"
              size="16px"
            />
          </q-item-section>
          <q-item-section class="text-roboto">
            <q-item-label>
              <span class="text-detail q-mr-sm">
                {{ `#${item.id}` }}
              </span>
              {{ item.subject }}
            </q-item-label>
          </q-item-section>
        </template>
      </q-item>
    </q-list>
  </q-menu>
</template>

<script>
import { filter as rFilter, isEmpty } from "ramda";
import { computed, defineComponent, defineAsyncComponent, onMounted, ref, watch } from "vue";
import { API as apiInterface, requests } from "@/api";
import { ticketListSchema, userListSchema } from "@/schemas";
import { notNully } from "@/utils";

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
    clearFilters: {
      type: Function,
      required: false,
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
    target: {
      type: String,
      required: true,
    },
    toggle: {
      type: Boolean,
      default: false,
    },
  },
  components: {
    TooltipWidget: defineAsyncComponent(() => import("@/components/widgets/TooltipWidget.vue")),
  },
  emits: ["itemChosen"],
  setup(props, context) {
    const { loading, success, data, fetchAPI } = apiInterface();
    const anchor = ref(null);
    const itemList = ref([]);
    const chooserFilter = ref("");
    const selected = ref({});

    const selectItem = (item) => {
      selected.value = item;
      context.emit("itemChosen", item[props.returnField]);
    };

    const itemData = computed(() => {
      if (props.showSelected && !isEmpty(selected.value)) {
        return rFilter((item) => item.id !== selected.value.id, itemList.value);
      } else {
        return itemList.value;
      }
    });

    const fetchData = async () => {
      const query = isEmpty(chooserFilter.value)
        ? "id&limit=0&offset=0"
        : `id&search=${chooserFilter.value}&limit=0&offset=0`;

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
        await schema.validate(data.value.data, { stripUnknown: true }).then((value) => {
          itemList.value = value;
          loading.value = false;
        });
    };

    const ticketIcon = (status) => {
      let name = status == 0 ? "record" : "check";
      return props.dark ? `mdi-${name}-circle` : `mdi-${name}-circle-outline`;
    };

    onMounted(async () => await fetchData());

    watch(chooserFilter, () => fetchData());

    return {
      anchor,
      chooserFilter,
      isEmpty,
      loading,
      selectItem,
      selected,
      itemData,
      notNully,
      ticketIcon,
    };
  },
});
</script>
