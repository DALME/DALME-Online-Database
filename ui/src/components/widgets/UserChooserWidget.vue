<template>
  <ChooserWidget
    :item="item"
    :dark="dark"
    :shadow="shadow"
    :label="label"
    :name="name"
    :tooltip="tooltip"
    :icon="icon"
    :clearFilters="clearFilters"
    :header="header"
    :returnField="returnField"
    :showAvatar="showAvatar"
    :showFilter="showFilter"
    :showSelected="showSelected"
    :toggle="toggle"
    :fetcher="fetchData"
    :items="itemList"
    @item-chosen="(v) => $emit('itemChosen', v)"
  >
    <template v-slot:chooser-selected-item="selected">
      <q-item-section v-if="showAvatar" side>
        <q-avatar v-if="!nully(selected.avatar)" size="34px">
          <img :src="selected.avatar" class="chooser-avatar-image" />
        </q-avatar>
        <q-icon v-else size="34px" name="mdi-account-circle" color="grey-4" />
      </q-item-section>
      <q-item-section class="text-roboto">
        <q-item-label>{{ selected.fullName }}</q-item-label>
        <q-item-label caption class="chooser-user-detail">{{ selected.username }}</q-item-label>
      </q-item-section>
    </template>

    <template v-slot:chooser-item="item">
      <q-item-section v-if="showAvatar" side>
        <q-avatar v-if="!nully(item.avatar)" size="34px">
          <img :src="item.avatar" class="chooser-avatar-image" />
        </q-avatar>
        <q-icon v-else size="34px" name="mdi-account-circle" color="grey-4" />
      </q-item-section>
      <q-item-section class="text-roboto">
        <q-item-label>{{ item.fullName }}</q-item-label>
        <q-item-label caption class="chooser-user-detail">{{ item.username }}</q-item-label>
      </q-item-section>
    </template>
  </ChooserWidget>
</template>

<script>
import { isEmpty } from "ramda";
import { defineComponent, ref } from "vue";
import { API as apiInterface, requests } from "@/api";
import { userListSchema } from "@/schemas";
import { ChooserWidget } from "@/components";
import { nully } from "@/utils";

export default defineComponent({
  name: "UserChooserWidget",
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
    label: String,
    name: String,
    tooltip: String,
    icon: {
      type: String,
      default: null,
    },
    clearFilters: Function,
    header: String,
    returnField: {
      type: String,
      default: "id",
    },
    showAvatar: {
      type: Boolean,
      default: true,
    },
    showFilter: {
      type: Boolean,
      default: true,
    },
    showSelected: {
      type: Boolean,
      default: false,
    },
    toggle: {
      type: Boolean,
      default: false,
    },
  },
  components: {
    ChooserWidget,
  },
  emits: ["itemChosen"],
  setup() {
    const { loading, success, data, fetchAPI } = apiInterface();
    const itemList = ref([]);

    const fetchData = async (filter) => {
      if (isEmpty(filter)) {
        itemList.value = [];
      } else {
        await fetchAPI(requests.users.getUsers(`id&search=${filter}&limit=10&offset=0`));
        if (success.value) {
          await userListSchema.validate(data.value.data, { stripUnknown: true }).then((value) => {
            itemList.value = value;
            loading.value = false;
          });
        }
      }
    };

    return {
      fetchData,
      itemList,
      nully,
    };
  },
});
</script>
