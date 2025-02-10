<template>
  <q-item clickable v-close-popup dense :class="cls" @click="$emit('itemChosen', item)">
    <q-item-section v-if="showAvatar" side>
      <q-avatar v-if="!nully(item.avatar)" size="34px">
        <img :src="item.avatar" class="chooser-avatar-image" />
      </q-avatar>
      <q-icon v-else size="34px" name="mdi-account-circle" :color="dark ? 'grey-9' : 'grey-4'" />
    </q-item-section>
    <q-item-section class="text-roboto">
      <q-item-label>{{ item.fullName }}</q-item-label>
      <q-item-label caption class="chooser-user-detail">{{ item.username }}</q-item-label>
    </q-item-section>
  </q-item>
</template>

<script>
import { computed, defineComponent } from "vue";
import { nully } from "@/utils";

export default defineComponent({
  name: "ItemUser",
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
    showAvatar: {
      type: Boolean,
      default: true,
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

    return {
      nully,
      cls,
    };
  },
});
</script>
