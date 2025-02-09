<template>
  <q-item clickable v-close-popup dense :class="itemClass" @click="$emit('itemChosen', item)">
    <q-item-section v-if="item.icon" side>
      <q-icon :name="item.icon.name" :color="item.icon.color" :size="item.icon.size" />
    </q-item-section>
    <q-item-section>
      {{ item.label }}
    </q-item-section>
  </q-item>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "ItemGeneric",
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
  },
  emits: ["itemChosen"],
  setup() {
    return {};
  },
});
</script>
