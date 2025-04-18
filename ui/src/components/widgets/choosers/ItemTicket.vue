<template>
  <q-item v-close-popup @click="$emit('itemChosen', item)" :class="cls" clickable dense>
    <q-item-section side>
      <q-icon
        :color="item.status == 0 ? 'light-green-6' : 'deep-purple-4'"
        :name="ticketIcon(item.status)"
        size="16px"
      />
    </q-item-section>
    <q-item-section class="text-roboto">
      <q-item-label>
        <span class="text-detail q-mr-sm">{{ `#${item.number}` }}</span>
        {{ item.subject }}
      </q-item-label>
    </q-item-section>
  </q-item>
</template>

<script>
import { computed, defineComponent } from "vue";

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
      default: "",
    },
  },
  emits: ["itemChosen"],
  setup(props) {
    const cls = computed(() => {
      const classes = [];
      if (props.dark) classes.push("dark");
      if (props.itemClass) classes.push(props.itemClass);
      return classes.length ? classes.join(" ") : "";
    });

    const ticketIcon = (status) => {
      let name = status == 0 ? "record" : "check";
      return props.dark ? `mdi-${name}-circle` : `mdi-${name}-circle-outline`;
    };

    return {
      ticketIcon,
      cls,
    };
  },
});
</script>
