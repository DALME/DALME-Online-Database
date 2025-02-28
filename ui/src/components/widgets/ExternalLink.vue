<template>
  <q-item
    clickable
    tag="a"
    target="_blank"
    :href="url"
    :class="`${inline ? 'external-link-inline' : 'external-link'}`"
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
    title: String,
    caption: String,
    url: {
      type: String,
      default: "#",
    },
    icon: String,
    inline: Boolean,
  },
});
</script>

<style lang="css">
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
