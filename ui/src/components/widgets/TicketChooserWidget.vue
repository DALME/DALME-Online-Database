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

    <template v-slot:chooser-item="item">
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
  </ChooserWidget>
</template>

<script>
import { isEmpty } from "ramda";
import { defineComponent, ref } from "vue";
import { API as apiInterface, requests } from "@/api";
import { ticketListSchema } from "@/schemas";
import { ChooserWidget } from "@/components";
import { nully } from "@/utils";

export default defineComponent({
  name: "TicketChooserWidget",
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
  setup(props) {
    const { loading, success, data, fetchAPI } = apiInterface();
    const itemList = ref([]);

    const fetchData = async (filter) => {
      if (isEmpty(filter)) {
        itemList.value = [];
      } else {
        await fetchAPI(requests.tickets.getTickets(`id&search=${filter}&limit=10&offset=0`));
        if (success.value) {
          await ticketListSchema.validate(data.value.data, { stripUnknown: true }).then((value) => {
            itemList.value = value;
            loading.value = false;
          });
        }
      }
    };

    const ticketIcon = (status) => {
      let name = status == 0 ? "record" : "check";
      return props.dark ? `mdi-${name}-circle` : `mdi-${name}-circle-outline`;
    };

    return {
      fetchData,
      itemList,
      nully,
      ticketIcon,
    };
  },
});
</script>
