<template>
  <q-btn
    v-if="linkable && showLink"
    icon="mdi-eye-outline"
    size="sm"
    dense
    no-caps
    flat
    :ripple="false"
    @click="$emit('navigate')"
  />
  <q-btn
    v-if="cancellable && showCancel"
    icon="mdi-undo-variant"
    color="orange-6"
    size="sm"
    dense
    no-caps
    flat
    :ripple="false"
    @click="$emit('cancel')"
  />
  <q-btn
    v-if="showMain"
    :icon="mainIcon"
    :color="mainColor"
    size="sm"
    dense
    no-caps
    flat
    :ripple="false"
    @click="$emit('action')"
  />
  <AdaptiveSpinner v-if="showSpinner" type="pie" color="green-6" size="140px" class="q-mr-xs" />
</template>

<script>
import { defineComponent } from "vue";
import { AdaptiveSpinner } from "@/components";

export default defineComponent({
  name: "EditButtons",
  props: {
    linkable: String,
    cancellable: {
      type: Boolean,
      default: false,
    },
    showLink: Boolean,
    showCancel: Boolean,
    showMain: Boolean,
    showSpinner: Boolean,
    mainIcon: String,
    mainColor: {
      type: String,
      default: "grey-5",
    },
  },
  emits: ["action", "cancel", "navigate"],
  components: { AdaptiveSpinner },
});
</script>
