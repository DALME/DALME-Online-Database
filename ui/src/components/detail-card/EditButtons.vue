<template>
  <q-btn
    v-if="linkable && showLink"
    @click="$emit('navigate')"
    :ripple="false"
    color="grey-5"
    icon="mdi-eye-outline"
    size="sm"
    dense
    flat
    no-caps
  />
  <q-btn
    v-if="cancellable && showCancel"
    @click="$emit('cancel')"
    :ripple="false"
    color="orange-6"
    icon="mdi-undo-variant"
    size="sm"
    dense
    flat
    no-caps
  />
  <q-btn
    v-if="showMain"
    @click="$emit('action')"
    :color="mainColor"
    :icon="mainIcon"
    :ripple="false"
    size="sm"
    dense
    flat
    no-caps
  />
  <AdaptiveSpinner v-if="showSpinner" class="q-mr-xs" color="green-6" size="14px" type="pie" />
</template>

<script>
import { defineComponent } from "vue";

import { AdaptiveSpinner } from "@/components";

export default defineComponent({
  name: "EditButtons",
  components: { AdaptiveSpinner },
  props: {
    linkable: {
      type: String,
      default: null,
    },
    cancellable: {
      type: Boolean,
      default: false,
    },
    showLink: Boolean,
    showCancel: Boolean,
    showMain: Boolean,
    showSpinner: Boolean,
    mainIcon: {
      type: String,
      required: true,
    },
    mainColor: {
      type: String,
      default: "grey-5",
    },
  },
  emits: ["action", "cancel", "navigate"],
});
</script>
