<template>
  <q-item v-close-popup @click="$emit('itemChosen', item)" :class="cls" clickable dense>
    <q-item-section v-if="item.icon" side>
      <q-icon :color="item.icon.color" :name="item.icon.name" :size="item.icon.size" />
    </q-item-section>
    <q-item-section>
      {{ item.label }}
    </q-item-section>
  </q-item>
</template>

<script>
import { computed, defineComponent } from "vue";

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
  setup(props) {
    const cls = computed(() => {
      const classes = [];
      if (props.dark) classes.push("dark");
      if (props.itemClass) classes.push(props.itemClass);
      return classes.length ? classes.join(" ") : "";
    });

    return { cls };
  },
});
</script>
