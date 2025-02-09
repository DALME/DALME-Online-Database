<template>
  <q-item clickable v-close-popup dense :class="itemClass" @click="$emit('itemChosen', item)">
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
  </q-item>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "ItemTicket",
  props: {
    dark: {
      type: Boolean,
      default: false,
    },
    item: {
      type: Object,
      required: true,
    },
    itemClass: {
      type: String,
      required: true,
    },
    showAvatar: {
      type: Boolean,
      required: true,
    },
  },
  emits: ["itemChosen"],
  setup(props) {
    const ticketIcon = (status) => {
      let name = status == 0 ? "record" : "check";
      return props.dark ? `mdi-${name}-circle` : `mdi-${name}-circle-outline`;
    };

    return { ticketIcon };
  },
});
</script>
