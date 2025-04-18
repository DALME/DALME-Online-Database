<template>
  <q-item
    :class="`${inline ? 'external-link-inline' : 'external-link'}`"
    :href="url"
    tag="a"
    target="_blank"
    clickable
    dense
  >
    <q-item-section v-if="icon" avatar>
      <q-icon :name="icon" />
    </q-item-section>

    <q-item-section>
      <q-item-label><span v-text="`${title ? title : url}`" /></q-item-label>
      <q-item-label v-if="caption" caption>{{ caption }}</q-item-label>
    </q-item-section>
  </q-item>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "ExternalLink",
  props: {
    title: {
      type: String,
      required: false,
      default: null,
    },
    caption: {
      type: String,
      required: false,
      default: null,
    },
    url: {
      type: String,
      default: "#",
    },
    icon: {
      type: String,
      required: false,
      default: null,
    },
    inline: Boolean,
  },
});
</script>

<style lang="css" scoped>
.external-link {
  padding: 2px;
  border-radius: 3px;
}
.external-link-inline {
  padding: 0 !important;
  display: inline-block !important;
  min-height: 0;
}
.external-link-inline .q-focus-helper {
  background-color: transparent !important;
}
</style>
